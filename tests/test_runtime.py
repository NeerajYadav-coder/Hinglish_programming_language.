"""Comprehensive unit tests for the Hinglish Runtime, Execution Engine, and REPL."""

import io
import sys
import unittest
from pathlib import Path

from hinglish.runtime import HinglishREPL, run, run_file


class TestHinglishRuntime(unittest.TestCase):
    """Test suite covering direct execution, namespace state, REPL, tracebacks, and example files."""

    def run_and_capture_output(self, source: str) -> str:
        """Helper to execute Hinglish code and capture standard output."""
        captured = io.StringIO()
        old_stdout = sys.stdout
        try:
            sys.stdout = captured
            run(source)
        finally:
            sys.stdout = old_stdout
        return captured.getvalue()

    def test_simple_assignment_and_output(self) -> None:
        source = 'naam = "Neeraj"\ndikhao("Namaste", naam)\n'
        out = self.run_and_capture_output(source)
        self.assertEqual(out.strip(), "Namaste Neeraj")

    def test_arithmetic_execution(self) -> None:
        source = "x = 10\ny = 5\nz = (x + y) * 2\n"
        env = run(source)
        self.assertEqual(env["x"], 10)
        self.assertEqual(env["y"], 5)
        self.assertEqual(env["z"], 30)

    def test_if_else_execution(self) -> None:
        source = (
            'umar = 20\n'
            'agar umar >= 18:\n'
            '    status = "adult"\n'
            'warna:\n'
            '    status = "minor"\n'
        )
        env = run(source)
        self.assertEqual(env["status"], "adult")

    def test_while_loop_execution(self) -> None:
        source = (
            'ginti = 1\n'
            'kul = 0\n'
            'jabtak ginti <= 5:\n'
            '    kul += ginti\n'
            '    ginti += 1\n'
        )
        env = run(source)
        self.assertEqual(env["ginti"], 6)
        self.assertEqual(env["kul"], 15)

    def test_for_loop_execution(self) -> None:
        source = (
            'shehar_soochi = ["Delhi", "Mumbai", "Pune"]\n'
            'lambai_kul = 0\n'
            'har shehar mein shehar_soochi:\n'
            '    lambai_kul += 1\n'
        )
        env = run(source)
        self.assertEqual(env["lambai_kul"], 3)

    def test_function_and_recursion(self) -> None:
        source = (
            'kaam fib(n):\n'
            '    agar n <= 0:\n'
            '        wapas 0\n'
            '    warna_agar n == 1:\n'
            '        wapas 1\n'
            '    wapas fib(n - 1) + fib(n - 2)\n'
            '\n'
            'ans = fib(7)\n'
        )
        env = run(source)
        self.assertEqual(env["ans"], 13)

    def test_imports_and_standard_library(self) -> None:
        source = (
            'laao math jaise m\n'
            'root = m.sqrt(81)\n'
        )
        env = run(source)
        self.assertEqual(env["root"], 9.0)

    def test_repl_persistent_state(self) -> None:
        repl = HinglishREPL()
        repl.run_line("x = 100")
        repl.run_line("y = 50")
        res = repl.run_line("x + y")
        self.assertEqual(res, 150)
        self.assertEqual(repl.namespace["x"], 100)
        self.assertEqual(repl.namespace["y"], 50)

    def test_repl_multiline_block(self) -> None:
        repl = HinglishREPL()
        repl.run_line("kaam greet(naam):")
        self.assertTrue(repl.in_block)
        repl.run_line("    wapas 'Namaste ' + naam")
        self.assertTrue(repl.in_block)
        repl.run_line("")  # Empty line signals block completion
        self.assertFalse(repl.in_block)

        res = repl.run_line("greet('Neeraj')")
        self.assertEqual(res, "Namaste Neeraj")

    def test_runtime_exception_source_mapping(self) -> None:
        source = (
            'x = 10\n'
            'y = 0\n'
            'z = x / y\n'  # Line 3 causes ZeroDivisionError
        )
        with self.assertRaises(RuntimeError) as ctx:
            run(source, filename="test_error.hin")
        err_msg = str(ctx.exception)
        self.assertIn("Hinglish Runtime Error in 'test_error.hin'", err_msg)
        self.assertIn("line 3", err_msg)
        self.assertIn("ZeroDivisionError", err_msg)
        self.assertIn("z = x / y", err_msg)

    def test_run_file_hello_example(self) -> None:
        example_path = Path(__file__).parent.parent / "examples" / "hello.hin"
        captured = io.StringIO()
        old_stdout = sys.stdout
        try:
            sys.stdout = captured
            run_file(example_path)
        finally:
            sys.stdout = old_stdout
        self.assertEqual(captured.getvalue().strip(), "Namaste duniya!")

    def test_run_file_control_flow_example(self) -> None:
        example_path = Path(__file__).parent.parent / "examples" / "control_flow.hin"
        captured = io.StringIO()
        old_stdout = sys.stdout
        try:
            sys.stdout = captured
            run_file(example_path)
        finally:
            sys.stdout = old_stdout
        out = captured.getvalue()
        self.assertIn("Aap vote de sakte hain.", out)
        self.assertIn("Ginti number: 3", out)
        self.assertIn("Shehar ka naam: Bengaluru", out)

    def test_run_file_functions_example(self) -> None:
        example_path = Path(__file__).parent.parent / "examples" / "functions.hin"
        captured = io.StringIO()
        old_stdout = sys.stdout
        try:
            sys.stdout = captured
            run_file(example_path)
        finally:
            sys.stdout = old_stdout
        out = captured.getvalue()
        self.assertIn("15 + 25 ka jod: 40", out)
        self.assertIn("Kul 30 se bada hai!", out)


if __name__ == "__main__":
    unittest.main()
