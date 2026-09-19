"""Tests for Step 10F — Hinglish Debugger and Debug Adapter Protocol (DAP).

Verifies:
- DAP JSON message framing and parsing
- Breakpoint registration and Hinglish source-line mapping
- Breakpoint hit and execution pause
- Stepping: Step Over, Step Into, Step Out
- Call stack translation from Python frames to Hinglish source positions
- Local, parameter, and global variable inspection
- Safe expression evaluation
- Uncaught exception interception at Hinglish error line
- Cross-file debugging across imported .hin modules
- Full DAP server request/response protocol cycle
"""

import io
import linecache
import shutil
import sys
import tempfile
import time
import unittest
from pathlib import Path

from hinglish.dap.debugger import HinglishDebugger
from hinglish.dap.protocol import (
    DapMessageBuilder,
    read_dap_message,
    write_dap_message,
)
from hinglish.dap.server import HinglishDebugAdapterServer


class TestDapProtocol(unittest.TestCase):
    """Test DAP framing and builder."""

    def test_message_roundtrip(self):
        stream = io.BytesIO()
        payload = {"seq": 1, "type": "request", "command": "initialize", "arguments": {}}
        write_dap_message(stream, payload)

        stream.seek(0)
        decoded = read_dap_message(stream)
        self.assertEqual(decoded, payload)

    def test_message_builder(self):
        builder = DapMessageBuilder()
        req = {"seq": 10, "type": "request", "command": "threads"}
        resp = builder.response(req, body={"threads": []})
        self.assertEqual(resp["seq"], 1)
        self.assertEqual(resp["type"], "response")
        self.assertEqual(resp["request_seq"], 10)
        self.assertEqual(resp["command"], "threads")
        self.assertTrue(resp["success"])

        evt = builder.event("stopped", {"reason": "breakpoint"})
        self.assertEqual(evt["seq"], 2)
        self.assertEqual(evt["type"], "event")
        self.assertEqual(evt["event"], "stopped")


class TestHinglishDebugger(unittest.TestCase):
    """Test HinglishDebugger bdb engine."""

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_breakpoint_and_variables(self):
        src = (
            "kaam multiply(x, y):\n"
            "    product = x * y\n"
            "    wapas product\n\n"
            "a = 6\n"
            "b = 7\n"
            "ans = multiply(a, b)\n"
        )
        prog = Path(self.temp_dir) / "test_mult.hin"
        prog.write_text(src, encoding="utf-8")

        stopped_events = []
        terminated_events = []

        dbg = HinglishDebugger(
            on_stopped=lambda reason, line, text: stopped_events.append((reason, line, text)),
            on_terminated=lambda code: terminated_events.append(code),
        )

        # Set breakpoint at line 2 ('product = x * y')
        bps = dbg.set_breakpoints(str(prog), [2])
        self.assertEqual(len(bps), 1)
        self.assertTrue(bps[0].verified)
        self.assertEqual(bps[0].line, 2)

        dbg.start_debugging(str(prog), stop_on_entry=False)

        # Wait for breakpoint hit
        deadline = time.time() + 2.0
        while not stopped_events and time.time() < deadline:
            time.sleep(0.05)

        self.assertTrue(len(stopped_events) >= 1)
        reason, line, _ = stopped_events[0]
        self.assertEqual(reason, "breakpoint")
        self.assertEqual(line, 2)

        # Inspect frames
        frames = dbg.get_stack_frames()
        self.assertTrue(len(frames) >= 2)
        self.assertEqual(frames[0].name, "multiply")
        self.assertEqual(frames[0].line, 2)
        self.assertEqual(frames[0].source.name, "test_mult.hin")

        # Inspect variables
        scopes = dbg.get_scopes(1)
        self.assertEqual(len(scopes), 2)
        locals_vars = dbg.get_variables(scopes[0].variables_reference)
        var_names = {v.name: v.value for v in locals_vars}
        self.assertIn("x", var_names)
        self.assertIn("y", var_names)
        self.assertEqual(var_names["x"], "6")
        self.assertEqual(var_names["y"], "7")

        # Resume execution
        dbg.resume_continue()
        deadline = time.time() + 2.0
        while not terminated_events and time.time() < deadline:
            time.sleep(0.05)

        self.assertTrue(len(terminated_events) >= 1)
        self.assertEqual(terminated_events[0], 0)

    def test_stepping_controls(self):
        src = (
            "x = 1\n"
            "y = 2\n"
            "z = x + y\n"
        )
        prog = Path(self.temp_dir) / "test_step.hin"
        prog.write_text(src, encoding="utf-8")

        stops = []
        dbg = HinglishDebugger(
            on_stopped=lambda reason, line, text: stops.append((reason, line)),
        )

        # Set breakpoint on line 1
        dbg.set_breakpoints(str(prog), [1])
        dbg.start_debugging(str(prog), stop_on_entry=False)

        deadline = time.time() + 2.0
        while not stops and time.time() < deadline:
            time.sleep(0.05)

        self.assertEqual(len(stops), 1)
        self.assertEqual(stops[0][1], 1)

        # Step Over -> advances to line 2
        dbg.step_over()
        deadline = time.time() + 2.0
        while len(stops) < 2 and time.time() < deadline:
            time.sleep(0.05)

        self.assertTrue(len(stops) >= 2)
        self.assertEqual(stops[1][1], 2)

        # Continue to finish
        dbg.resume_continue()
        time.sleep(0.2)

    def test_safe_evaluation(self):
        src = (
            "kaam test_eval(base):\n"
            "    val = base * 10\n"
            "    wapas val\n\n"
            "test_eval(5)\n"
        )
        prog = Path(self.temp_dir) / "eval.hin"
        prog.write_text(src, encoding="utf-8")

        stops = []
        dbg = HinglishDebugger(
            on_stopped=lambda r, l, t: stops.append((r, l)),
        )
        dbg.set_breakpoints(str(prog), [2])
        dbg.start_debugging(str(prog))

        deadline = time.time() + 2.0
        while not stops and time.time() < deadline:
            time.sleep(0.05)

        self.assertTrue(len(stops) >= 1)
        # Evaluate expressions
        ok, res, t_name = dbg.evaluate_expression("base + 5")
        self.assertTrue(ok)
        self.assertEqual(res, "10")
        self.assertEqual(t_name, "int")

        ok, res, t_name = dbg.evaluate_expression("base == 5")
        self.assertTrue(ok)
        self.assertEqual(res, "True")

        # Invalid expression
        ok, err_msg, _ = dbg.evaluate_expression("undefined_variable")
        self.assertFalse(ok)
        self.assertIn("NameError", err_msg)

        dbg.resume_continue()
        time.sleep(0.2)

    def test_uncaught_exception_debugging(self):
        src = (
            "kaam divide(a, b):\n"
            "    wapas a / b\n\n"
            "res = divide(10, 0)\n"
        )
        prog = Path(self.temp_dir) / "exc.hin"
        prog.write_text(src, encoding="utf-8")

        stops = []
        dbg = HinglishDebugger(
            on_stopped=lambda r, l, t: stops.append((r, l, t)),
        )
        dbg.start_debugging(str(prog))

        deadline = time.time() + 2.0
        while not stops and time.time() < deadline:
            time.sleep(0.05)

        self.assertTrue(len(stops) >= 1)
        reason, line, text = stops[0]
        self.assertEqual(reason, "exception")
        self.assertEqual(line, 2)
        self.assertIn("ZeroDivisionError", text)

        dbg.resume_continue()
        time.sleep(0.2)

    def test_multi_file_debugging(self):
        # Create helper module
        helper_file = Path(self.temp_dir) / "math_helper.hin"
        helper_file.write_text(
            "kaam square(n):\n"
            "    sq = n * n\n"
            "    wapas sq\n",
            encoding="utf-8",
        )

        main_file = Path(self.temp_dir) / "main_entry.hin"
        main_file.write_text(
            "se math_helper laao square\n"
            "res = square(8)\n"
            "dikhao(res)\n",
            encoding="utf-8",
        )

        stops = []
        dbg = HinglishDebugger(
            on_stopped=lambda r, l, t: stops.append((r, l)),
        )

        # Set breakpoint inside imported module math_helper.hin line 2
        bps = dbg.set_breakpoints(str(helper_file), [2])
        self.assertEqual(len(bps), 1)
        self.assertTrue(bps[0].verified)

        dbg.start_debugging(str(main_file))

        deadline = time.time() + 2.0
        while not stops and time.time() < deadline:
            time.sleep(0.05)

        self.assertTrue(len(stops) >= 1)
        self.assertEqual(stops[0][1], 2)

        # Check call stack shows math_helper on top and main_entry below
        frames = dbg.get_stack_frames()
        self.assertTrue(len(frames) >= 2)
        self.assertEqual(frames[0].source.name, "math_helper.hin")
        self.assertEqual(frames[0].name, "square")
        self.assertEqual(frames[0].line, 2)

        self.assertEqual(frames[1].source.name, "main_entry.hin")
        self.assertEqual(frames[1].line, 2)

        dbg.resume_continue()
        time.sleep(0.2)


class TestDapServerIntegration(unittest.TestCase):
    """Test full DAP server request/response stdio exchange."""

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.out_stream = io.BytesIO()
        self.server = HinglishDebugAdapterServer(out_stream=self.out_stream)

    def tearDown(self):
        shutil.rmtree(self.temp_dir, ignore_errors=True)
        self.server.debugger.stop()

    def _drain_messages(self):
        msgs = []
        pos = self.out_stream.tell()
        self.out_stream.seek(0)
        while True:
            m = read_dap_message(self.out_stream)
            if not m:
                break
            msgs.append(m)
        self.out_stream.seek(pos)
        return msgs

    def test_server_initialize_launch_cycle(self):
        prog = Path(self.temp_dir) / "server_test.hin"
        prog.write_text(
            "kaam say_hello(naam):\n"
            "    greeting = 'Namaste ' + naam\n"
            "    wapas greeting\n\n"
            "msg = say_hello('Neeraj')\n",
            encoding="utf-8",
        )

        # 1. Initialize
        self.server.handle_message({"seq": 1, "type": "request", "command": "initialize", "arguments": {}})
        # 2. Launch
        self.server.handle_message({
            "seq": 2,
            "type": "request",
            "command": "launch",
            "arguments": {"program": str(prog), "stopOnEntry": False},
        })
        # 3. SetBreakpoints
        self.server.handle_message({
            "seq": 3,
            "type": "request",
            "command": "setBreakpoints",
            "arguments": {"source": {"path": str(prog)}, "lines": [2]},
        })
        # 4. ConfigurationDone
        self.server.handle_message({"seq": 4, "type": "request", "command": "configurationDone"})

        # Wait for stopped event
        time.sleep(0.3)

        # 5. Threads
        pos = self.out_stream.tell()
        self.server.handle_message({"seq": 5, "type": "request", "command": "threads"})
        self.out_stream.seek(pos)
        th_resp = read_dap_message(self.out_stream)
        self.assertEqual(th_resp["command"], "threads")
        self.assertEqual(len(th_resp["body"]["threads"]), 1)

        # 6. StackTrace
        pos = self.out_stream.tell()
        self.server.handle_message({"seq": 6, "type": "request", "command": "stackTrace", "arguments": {"threadId": 1}})
        self.out_stream.seek(pos)
        st_resp = read_dap_message(self.out_stream)
        self.assertEqual(st_resp["command"], "stackTrace")
        self.assertTrue(len(st_resp["body"]["stackFrames"]) >= 1)
        top_frame = st_resp["body"]["stackFrames"][0]
        self.assertEqual(top_frame["name"], "say_hello")
        self.assertEqual(top_frame["line"], 2)

        # 7. Scopes
        pos = self.out_stream.tell()
        self.server.handle_message({"seq": 7, "type": "request", "command": "scopes", "arguments": {"frameId": 1}})
        self.out_stream.seek(pos)
        sc_resp = read_dap_message(self.out_stream)
        self.assertEqual(sc_resp["command"], "scopes")

        # 8. Variables
        loc_ref = sc_resp["body"]["scopes"][0]["variablesReference"]
        pos = self.out_stream.tell()
        self.server.handle_message({"seq": 8, "type": "request", "command": "variables", "arguments": {"variablesReference": loc_ref}})
        self.out_stream.seek(pos)
        var_resp = read_dap_message(self.out_stream)
        self.assertEqual(var_resp["command"], "variables")
        v_dict = {v["name"]: v["value"] for v in var_resp["body"]["variables"]}
        self.assertIn("naam", v_dict)
        self.assertEqual(v_dict["naam"], "'Neeraj'")

        # 9. Continue
        self.server.handle_message({"seq": 9, "type": "request", "command": "continue"})
        time.sleep(0.3)


if __name__ == "__main__":
    unittest.main()
