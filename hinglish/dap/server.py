"""Debug Adapter Protocol (DAP) server handling JSON message routing over stdio.

Dispatches:
- initialize, launch, configurationDone
- setBreakpoints, setExceptionBreakpoints
- threads, stackTrace, scopes, variables
- continue, next, stepIn, stepOut, pause, disconnect, terminate
"""

import sys
import threading
from typing import Any, BinaryIO, Dict, Optional

from .debugger import HinglishDebugger
from .protocol import (
    DapMessageBuilder,
    read_dap_message,
    write_dap_message,
)


class HinglishDebugAdapterServer:
    """Server managing DAP communication between VS Code and HinglishDebugger."""

    def __init__(
        self,
        in_stream: Optional[BinaryIO] = None,
        out_stream: Optional[BinaryIO] = None,
    ) -> None:
        self.in_stream: BinaryIO = in_stream or sys.stdin.buffer
        self.out_stream: BinaryIO = out_stream or sys.stdout.buffer
        self.builder = DapMessageBuilder()
        self._write_lock = threading.Lock()
        self.is_running = False

        self.debugger = HinglishDebugger(
            on_stopped=self._handle_debugger_stopped,
            on_terminated=self._handle_debugger_terminated,
            on_output=self._handle_debugger_output,
        )

        self._launch_args: Dict[str, Any] = {}
        self._config_done = False

    def send_response(
        self,
        request: Dict[str, Any],
        body: Optional[Dict[str, Any]] = None,
        success: bool = True,
        message: Optional[str] = None,
    ) -> None:
        """Constructs and writes a DAP response."""
        res = self.builder.response(request, body=body, success=success, message=message)
        with self._write_lock:
            write_dap_message(self.out_stream, res)

    def send_event(self, event_name: str, body: Optional[Dict[str, Any]] = None) -> None:
        """Constructs and writes a DAP event."""
        evt = self.builder.event(event_name, body=body)
        with self._write_lock:
            write_dap_message(self.out_stream, evt)

    # -------------------------------------------------------------------------
    # Debugger Callbacks
    # -------------------------------------------------------------------------

    def _handle_debugger_stopped(
        self, reason: str, line: int, text: Optional[str] = None
    ) -> None:
        """Called when debugger pauses execution."""
        body: Dict[str, Any] = {
            "reason": reason,
            "threadId": 1,
            "allThreadsStopped": True,
        }
        if text:
            body["text"] = text
            body["description"] = text
        self.send_event("stopped", body)

    def _handle_debugger_terminated(self, exit_code: int) -> None:
        """Called when debugger finishes execution."""
        self.send_event("terminated")
        self.send_event("exited", {"exitCode": exit_code})

    def _handle_debugger_output(self, output: str, category: str = "console") -> None:
        """Called when debugger outputs text."""
        self.send_event("output", {"category": category, "output": output})

    # -------------------------------------------------------------------------
    # Message Dispatch
    # -------------------------------------------------------------------------

    def handle_message(self, message: Dict[str, Any]) -> None:
        """Dispatches an incoming DAP request."""
        msg_type = message.get("type")
        command = message.get("command")
        args = message.get("arguments", {})

        if msg_type != "request":
            return

        if command == "initialize":
            capabilities = {
                "supportsConfigurationDoneRequest": True,
                "supportsFunctionBreakpoints": False,
                "supportsConditionalBreakpoints": False,
                "supportsEvaluateForHovers": True,
                "supportsStepBack": False,
                "supportsSetVariable": False,
                "supportsRestartRequest": False,
                "supportsExceptionInfoRequest": True,
            }
            self.send_response(message, body=capabilities)
            self.send_event("initialized")

        elif command == "launch":
            self._launch_args = args
            self.send_response(message, success=True)
            # If configurationDone was already received, or if client does not send it, start
            if self._config_done:
                self._start_execution()

        elif command == "setBreakpoints":
            source = args.get("source", {})
            file_path = source.get("path", "")
            lines = args.get("lines")
            if lines is None:
                lines = [bp.get("line", 1) for bp in args.get("breakpoints", [])]

            verified_bps = self.debugger.set_breakpoints(file_path, lines)
            self.send_response(
                message,
                body={"breakpoints": [bp.to_dict() for bp in verified_bps]},
            )

        elif command == "setExceptionBreakpoints":
            self.send_response(message, body={"breakpoints": []})

        elif command == "configurationDone":
            self._config_done = True
            self.send_response(message, success=True)
            if self._launch_args:
                self._start_execution()

        elif command == "threads":
            self.send_response(
                message,
                body={"threads": [{"id": 1, "name": "Hinglish Main Thread"}]},
            )

        elif command == "stackTrace":
            frames = self.debugger.get_stack_frames()
            self.send_response(
                message,
                body={
                    "stackFrames": [f.to_dict() for f in frames],
                    "totalFrames": len(frames),
                },
            )

        elif command == "scopes":
            frame_id = args.get("frameId", 1)
            scopes = self.debugger.get_scopes(frame_id)
            self.send_response(
                message,
                body={"scopes": [s.to_dict() for s in scopes]},
            )

        elif command == "variables":
            var_ref = args.get("variablesReference", 0)
            variables = self.debugger.get_variables(var_ref)
            self.send_response(
                message,
                body={"variables": [v.to_dict() for v in variables]},
            )

        elif command == "evaluate":
            expr = args.get("expression", "")
            frame_id = args.get("frameId")
            ok, val_str, type_str = self.debugger.evaluate_expression(expr, frame_id)
            if ok:
                self.send_response(
                    message,
                    body={
                        "result": val_str,
                        "type": type_str,
                        "variablesReference": 0,
                    },
                )
            else:
                self.send_response(
                    message,
                    success=False,
                    message=val_str,
                )

        elif command == "continue":
            self.send_response(message, body={"allThreadsContinued": True})
            self.debugger.resume_continue()

        elif command == "next":
            self.send_response(message, body={})
            self.debugger.step_over()

        elif command == "stepIn":
            self.send_response(message, body={})
            self.debugger.step_into()

        elif command == "stepOut":
            self.send_response(message, body={})
            self.debugger.step_out()

        elif command == "pause":
            self.send_response(message, body={})
            self.debugger.pause()

        elif command in ("disconnect", "terminate"):
            self.send_response(message, body={})
            self.debugger.stop()
            self.is_running = False

        else:
            self.send_response(
                message,
                success=False,
                message=f"Command '{command}' is not supported.",
            )

    def _start_execution(self) -> None:
        """Starts debugger execution using the stored launch arguments."""
        prog = self._launch_args.get("program", "")
        stop_on_entry = self._launch_args.get("stopOnEntry", False)
        args = self._launch_args.get("args", [])
        self.debugger.start_debugging(prog, args=args, stop_on_entry=stop_on_entry)

    def run(self) -> None:
        """Main stdio loop reading and handling DAP messages."""
        self.is_running = True
        try:
            while self.is_running:
                message = read_dap_message(self.in_stream)
                if message is None:
                    break
                self.handle_message(message)
        except (KeyboardInterrupt, SystemExit):
            pass
        finally:
            self.is_running = False
            self.debugger.stop()


def main() -> None:
    """Entry point for hinglish-dap console command."""
    server = HinglishDebugAdapterServer()
    server.run()


if __name__ == "__main__":
    main()
