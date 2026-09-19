"""Hinglish runtime debugger implementing Python bdb hooks and source-mapped debugging.

Provides:
- Source-level breakpoint management for .hin files
- Step over, step into, step out, continue, pause, and stop controls
- Accurate call stack translation from Python frames to Hinglish source positions
- Local and global variable inspection
- Runtime exception interception at Hinglish source lines
- Multi-file debugging via native Hinglish import hooks
"""

import bdb
import linecache
import os
import sys
import threading
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Set, Tuple

from ..compiler import HinglishCompiler
from ..parser import parse
from ..runtime.context import get_default_globals
from ..runtime.engine import _MODULE_SOURCE_CACHE, register_source
from ..runtime.importer import install_import_hook
from .protocol import Breakpoint, Scope, Source, StackFrame, Variable


class HinglishDebugger(bdb.Bdb):
    """Debugger subclassing bdb.Bdb with Hinglish source mapping."""

    def __init__(
        self,
        on_stopped: Optional[Callable[[str, int, Optional[str]], None]] = None,
        on_terminated: Optional[Callable[[int], None]] = None,
        on_output: Optional[Callable[[str, str], None]] = None,
    ) -> None:
        super().__init__()
        self.on_stopped = on_stopped
        self.on_terminated = on_terminated
        self.on_output = on_output

        # File -> (py_to_hin, hin_to_py)
        self.file_line_maps: Dict[str, Tuple[Dict[int, int], Dict[int, int]]] = {}
        # File -> set of Hinglish line breakpoints
        self.hin_breakpoints: Dict[str, Set[int]] = {}

        # Thread synchronization
        self._action_event = threading.Event()
        self._next_action = "continue"
        self.stop_on_entry = False
        self.started = False
        self.is_running = False
        self.is_terminated = False
        self.current_frame = None
        self._frame_cache: Dict[int, Any] = {}
        self._next_breakpoint_id = 1

    # -------------------------------------------------------------------------
    # Source & Breakpoint Registration
    # -------------------------------------------------------------------------

    def register_file(self, file_path: str, source_code: Optional[str] = None) -> None:
        """Registers and compiles a Hinglish file, generating bidirectional line maps."""
        resolved = str(Path(file_path).resolve())
        if resolved in self.file_line_maps:
            return

        if source_code is None:
            source_code = Path(resolved).read_text(encoding="utf-8")

        tree = parse(source_code)
        compiler = HinglishCompiler()
        py_code, py_to_hin = compiler.compile_with_map(tree)
        hin_to_py: Dict[int, int] = {}
        for py_l, hin_l in py_to_hin.items():
            if hin_l not in hin_to_py:
                hin_to_py[hin_l] = py_l

        self.file_line_maps[resolved] = (py_to_hin, hin_to_py)
        self.file_line_maps[file_path] = (py_to_hin, hin_to_py)
        register_source(resolved, source_code, py_to_hin)

        # Populate linecache for bdb and tracebacks
        src_lines = source_code.splitlines(keepends=True)
        linecache.cache[resolved] = (len(source_code), None, src_lines, resolved)
        linecache.cache[file_path] = (len(source_code), None, src_lines, file_path)

    def set_breakpoints(
        self, file_path: str, hin_lines: List[int]
    ) -> List[Breakpoint]:
        """Sets breakpoints for a given Hinglish file at specified lines."""
        resolved = str(Path(file_path).resolve())
        self.register_file(resolved)

        # Clear existing breakpoints for this file in bdb
        self.clear_all_file_breaks(resolved)
        self.clear_all_file_breaks(file_path)

        py_to_hin, hin_to_py = self.file_line_maps.get(resolved, ({}, {}))
        verified_breakpoints: List[Breakpoint] = []
        registered_hin_lines: Set[int] = set()

        for h_line in hin_lines:
            # Map Hinglish line to nearest Python line
            py_line = hin_to_py.get(h_line)
            if py_line is None:
                candidates = [py for py, hin in py_to_hin.items() if hin >= h_line]
                py_line = min(candidates) if candidates else None

            if py_line is not None:
                # Set in bdb on both resolved and file_path
                self.set_break(resolved, py_line)
                if file_path != resolved:
                    self.set_break(file_path, py_line)
                registered_hin_lines.add(h_line)

                bp_id = self._next_breakpoint_id
                self._next_breakpoint_id += 1
                verified_breakpoints.append(
                    Breakpoint(
                        id=bp_id,
                        verified=True,
                        line=h_line,
                        source=Source(path=resolved, name=Path(resolved).name),
                    )
                )
            else:
                bp_id = self._next_breakpoint_id
                self._next_breakpoint_id += 1
                verified_breakpoints.append(
                    Breakpoint(
                        id=bp_id,
                        verified=False,
                        line=h_line,
                        source=Source(path=resolved, name=Path(resolved).name),
                        message="Cannot map line to executable statement",
                    )
                )

        self.hin_breakpoints[resolved] = registered_hin_lines
        self.hin_breakpoints[file_path] = registered_hin_lines
        return verified_breakpoints

    def get_hin_line(self, filename: str, py_line: int) -> int:
        """Translates a Python line number back to its Hinglish line number."""
        resolved = str(Path(filename).resolve()) if filename else ""
        maps = self.file_line_maps.get(resolved) or self.file_line_maps.get(filename)
        if maps:
            return maps[0].get(py_line, py_line)
        # Check runtime source cache
        cached = _MODULE_SOURCE_CACHE.get(resolved) or _MODULE_SOURCE_CACHE.get(filename)
        if cached:
            _, lmap = cached
            return lmap.get(py_line, py_line)
        return py_line

    # -------------------------------------------------------------------------
    # Execution & Control
    # -------------------------------------------------------------------------

    def start_debugging(
        self,
        program_path: str,
        args: Optional[List[str]] = None,
        stop_on_entry: bool = False,
    ) -> None:
        """Launches the Hinglish program under debugger control on a worker thread."""
        self.stop_on_entry = stop_on_entry
        self.started = False
        self.is_running = True
        self.is_terminated = False
        self._action_event.clear()

        resolved = str(Path(program_path).resolve())
        self.register_file(resolved)

        source_code = Path(resolved).read_text(encoding="utf-8")
        tree = parse(source_code)
        compiler = HinglishCompiler()
        py_source, _ = compiler.compile_with_map(tree)
        code_obj = compile(py_source, resolved, "exec")

        # Install import hook for multi-file .hin imports
        install_import_hook()
        # Ensure target file directory is in sys.path
        target_dir = str(Path(resolved).parent)
        if target_dir not in sys.path:
            sys.path.insert(0, target_dir)

        globals_dict = get_default_globals()
        globals_dict["__file__"] = resolved
        globals_dict["__name__"] = "__main__"

        def _runner() -> None:
            exit_code = 0
            try:
                self.reset()
                # Run the code object under Bdb
                self.run(code_obj, globals_dict)
            except bdb.BdbQuit:
                pass
            except SystemExit as se:
                exit_code = se.code if isinstance(se.code, int) else 0
            except Exception as exc:
                exit_code = 1
                if self.on_output:
                    self.on_output(f"Unhandled Exception: {type(exc).__name__}: {exc}\n", "stderr")
            finally:
                self.is_running = False
                self.is_terminated = True
                if self.on_terminated:
                    self.on_terminated(exit_code)

        thread = threading.Thread(target=_runner, daemon=True, name="HinglishDebuggerThread")
        thread.start()

    def resume_continue(self) -> None:
        """Resumes program execution until next breakpoint or exit."""
        self._next_action = "continue"
        self._action_event.set()

    def step_over(self) -> None:
        """Steps over the current statement."""
        self._next_action = "next"
        self._action_event.set()

    def step_into(self) -> None:
        """Steps into the callable or next statement."""
        self._next_action = "step"
        self._action_event.set()

    def step_out(self) -> None:
        """Steps out of the current function to its caller."""
        self._next_action = "return"
        self._action_event.set()

    def pause(self) -> None:
        """Pauses program execution at the next line."""
        self.set_step()

    def stop(self) -> None:
        """Terminates debugging execution immediately."""
        self._next_action = "quit"
        self.set_quit()
        self._action_event.set()

    # -------------------------------------------------------------------------
    # Bdb Callbacks
    # -------------------------------------------------------------------------

    def set_continue(self) -> None:
        """Resumes execution while preserving trace hook for exceptions and breakpoints."""
        self._set_stopinfo(self.botframe, None, -1)
        # Do not call stop_trace() so exceptions and imported module breakpoints are intercepted

    def dispatch_call(self, frame: Any, arg: Any) -> Any:
        """Ensures function calls within .hin modules remain traced."""
        super().dispatch_call(frame, arg)
        co_filename = frame.f_code.co_filename
        if co_filename.endswith(".hin") or co_filename in _MODULE_SOURCE_CACHE:
            return self.trace_dispatch
        return self.trace_dispatch

    def dispatch_exception(self, frame: Any, arg: Tuple[Any, Any, Any]) -> Any:
        """Intercepts exceptions occurring in user code."""
        exc_type, exc_val, _ = arg
        if exc_type is bdb.BdbQuit:
            return None

        co_filename = frame.f_code.co_filename
        if co_filename.endswith(".hin") or co_filename in _MODULE_SOURCE_CACHE:
            self.user_exception(frame, arg)
            if self.quitting:
                raise bdb.BdbQuit()
        return self.trace_dispatch

    def user_line(self, frame: Any) -> None:
        """Called by Bdb when about to execute a line of code."""
        co_filename = frame.f_code.co_filename

        # If not a .hin file, skip tracing unless stepping
        if not co_filename.endswith(".hin") and co_filename not in _MODULE_SOURCE_CACHE:
            if self._next_action == "continue":
                self.set_continue()
                return

        hin_line = self.get_hin_line(co_filename, frame.f_lineno)

        # Stop on entry handling
        if not self.started:
            self.started = True
            is_bp = self._is_breakpoint_hit(co_filename, hin_line, frame.f_lineno)
            if not self.stop_on_entry and not is_bp:
                self.set_continue()
                return

        # Determine if we should pause
        is_breakpoint = self._is_breakpoint_hit(co_filename, hin_line, frame.f_lineno)
        reason = "breakpoint" if is_breakpoint else "step"

        self._pause_at_frame(frame, reason, hin_line)

    def user_exception(self, frame: Any, exc_info: Tuple[Any, Any, Any]) -> None:
        """Called by Bdb when an exception occurs."""
        exc_type, exc_val, _ = exc_info
        if exc_type is bdb.BdbQuit:
            return

        co_filename = frame.f_code.co_filename
        hin_line = self.get_hin_line(co_filename, frame.f_lineno)
        msg = f"{exc_type.__name__}: {exc_val}"
        self._pause_at_frame(frame, "exception", hin_line, text=msg)

    def _is_breakpoint_hit(self, filename: str, hin_line: int, py_line: int) -> bool:
        """Checks if a breakpoint was hit at this line."""
        resolved = str(Path(filename).resolve()) if filename else ""
        breaks = self.hin_breakpoints.get(resolved) or self.hin_breakpoints.get(filename)
        if breaks and hin_line in breaks:
            return True
        return self.get_break(filename, py_line)

    def _pause_at_frame(
        self, frame: Any, reason: str, hin_line: int, text: Optional[str] = None
    ) -> None:
        """Halts execution at the current frame and signals the DAP client."""
        self.current_frame = frame
        self._action_event.clear()

        if self.on_stopped:
            self.on_stopped(reason, hin_line, text)

        # Block until the client sends a continue / step / quit command
        self._action_event.wait()

        # Apply user action
        if self._next_action == "continue":
            self.set_continue()
        elif self._next_action == "next":
            self.set_next(frame)
        elif self._next_action == "step":
            self.set_step()
        elif self._next_action == "return":
            self.set_return(frame)
        elif self._next_action == "quit":
            self.set_quit()
            raise bdb.BdbQuit()

    # -------------------------------------------------------------------------
    # Stack Trace & Inspection
    # -------------------------------------------------------------------------

    def get_stack_frames(self) -> List[StackFrame]:
        """Returns the call stack frames translated into Hinglish source coordinates."""
        frames: List[StackFrame] = []
        self._frame_cache.clear()

        f = self.current_frame
        frame_id = 1

        while f is not None:
            co_file = f.f_code.co_filename
            func_name = f.f_code.co_name
            if func_name == "<module>":
                func_name = "(module)"

            py_line = f.f_lineno
            hin_line = self.get_hin_line(co_file, py_line)

            # Expose user .hin files and imported .hin modules
            if co_file.endswith(".hin") or co_file in _MODULE_SOURCE_CACHE:
                frames.append(
                    StackFrame(
                        id=frame_id,
                        name=func_name,
                        source=Source(path=co_file, name=Path(co_file).name),
                        line=hin_line,
                        column=1,
                    )
                )
                self._frame_cache[frame_id] = f
                frame_id += 1

            f = f.f_back

        return frames

    def get_scopes(self, frame_id: int) -> List[Scope]:
        """Returns Locals and Globals scopes for a given frame."""
        return [
            Scope(name="Locals", variables_reference=frame_id * 10 + 1),
            Scope(name="Globals", variables_reference=frame_id * 10 + 2),
        ]

    def get_variables(self, var_ref: int) -> List[Variable]:
        """Returns variables within the requested scope reference."""
        frame_id = var_ref // 10
        scope_type = var_ref % 10  # 1: Locals, 2: Globals

        frame = self._frame_cache.get(frame_id, self.current_frame)
        if frame is None:
            return []

        var_dict = frame.f_locals if scope_type == 1 else frame.f_globals
        variables: List[Variable] = []

        # Internal keys to filter out from user view
        ignored_keys = {
            "__builtins__",
            "__file__",
            "__doc__",
            "__cached__",
            "__loader__",
            "__spec__",
            "__annotations__",
            "__package__",
        }

        for k, v in var_dict.items():
            if k in ignored_keys:
                continue

            try:
                v_str = repr(v)
                if len(v_str) > 200:
                    v_str = v_str[:197] + "..."
            except Exception:
                v_str = "<unprintable>"

            t_str = type(v).__name__
            variables.append(
                Variable(
                    name=k,
                    value=v_str,
                    type=t_str,
                    variables_reference=0,
                )
            )

        # Sort variables alphabetically
        variables.sort(key=lambda var: var.name)
        return variables

    def evaluate_expression(
        self, expression: str, frame_id: Optional[int] = None
    ) -> Tuple[bool, str, str]:
        """Evaluates an expression safely within the context of the active frame."""
        frame = self._frame_cache.get(frame_id, self.current_frame) if frame_id else self.current_frame
        if frame is None:
            return False, "No active stack frame", ""

        try:
            val = eval(expression, frame.f_globals, frame.f_locals)
            return True, repr(val), type(val).__name__
        except Exception as err:
            return False, f"{type(err).__name__}: {err}", "error"
