"""Unit tests for Step 10A: Hinglish Packaging & Installability."""

import io
import subprocess
import sys
import unittest
from pathlib import Path

import hinglish
from hinglish.cli import main


class TestStep10aPackaging(unittest.TestCase):
    """Verifies package metadata, versioning, dependencies, and CLI entry point."""

    def test_version_accessibility(self) -> None:
        """Verifies hinglish.__version__ is 1.1.0."""
        self.assertEqual(hinglish.__version__, "1.1.0")
        self.assertIsInstance(hinglish.__version__, str)

    def test_package_exports(self) -> None:
        """Verifies core symbols are properly exposed at top-level."""
        self.assertTrue(callable(hinglish.tokenize))
        self.assertTrue(callable(hinglish.parse))
        self.assertTrue(callable(hinglish.compile))
        self.assertTrue(callable(hinglish.run))
        self.assertTrue(callable(hinglish.run_file))
        self.assertTrue(callable(hinglish.start_repl))
        self.assertIn("HinglishREPL", hinglish.__all__)

    def test_zero_runtime_dependencies(self) -> None:
        """Verifies that pyproject.toml declares dependencies = []."""
        pyproject_path = Path(__file__).parent.parent / "pyproject.toml"
        self.assertTrue(pyproject_path.is_file())
        content = pyproject_path.read_text(encoding="utf-8")
        self.assertIn("dependencies = []", content)
        self.assertIn('name = "hinglish-lang"', content)
        self.assertIn('version = "1.1.0"', content)
        self.assertIn('hinglish = "hinglish.cli:main"', content)

    def test_cli_version_flag_programmatically(self) -> None:
        """Verifies CLI main function handles --version flag."""
        stdout_buf = io.StringIO()
        stderr_buf = io.StringIO()
        saved_stdout, saved_stderr = sys.stdout, sys.stderr
        try:
            sys.stdout = stdout_buf
            sys.stderr = stderr_buf
            with self.assertRaises(SystemExit) as ctx:
                main(["--version"])
            self.assertEqual(ctx.exception.code, 0)
            output = stdout_buf.getvalue() or stderr_buf.getvalue()
            self.assertIn("1.1.0", output)
        finally:
            sys.stdout = saved_stdout
            sys.stderr = saved_stderr

    def test_cli_help_flag_programmatically(self) -> None:
        """Verifies CLI main function handles --help flag."""
        stdout_buf = io.StringIO()
        stderr_buf = io.StringIO()
        saved_stdout, saved_stderr = sys.stdout, sys.stderr
        try:
            sys.stdout = stdout_buf
            sys.stderr = stderr_buf
            with self.assertRaises(SystemExit) as ctx:
                main(["--help"])
            self.assertEqual(ctx.exception.code, 0)
            output = stdout_buf.getvalue() or stderr_buf.getvalue()
            self.assertIn("hinglish", output)
        finally:
            sys.stdout = saved_stdout
            sys.stderr = saved_stderr

    def test_python_module_invocation_version(self) -> None:
        """Verifies python3 -m hinglish --version."""
        res = subprocess.run(
            [sys.executable, "-m", "hinglish", "--version"],
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(res.returncode, 0)
        output = res.stdout or res.stderr
        self.assertIn("1.1.0", output)

    def test_python_module_invocation_file(self) -> None:
        """Verifies python3 -m hinglish <file.hin> execution."""
        hello_file = Path(__file__).parent.parent / "examples" / "hello.hin"
        self.assertTrue(hello_file.is_file())
        res = subprocess.run(
            [sys.executable, "-m", "hinglish", str(hello_file)],
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(res.returncode, 0)
        self.assertIn("Namaste duniya!", res.stdout)

    def test_python_module_inspection_flags(self) -> None:
        """Verifies python3 -m hinglish --tokens, --ast, --transpile flags."""
        hello_file = Path(__file__).parent.parent / "examples" / "hello.hin"

        # --tokens
        tok_res = subprocess.run(
            [sys.executable, "-m", "hinglish", "--tokens", str(hello_file)],
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(tok_res.returncode, 0)
        self.assertIn("IDENTIFIER", tok_res.stdout)

        # --ast
        ast_res = subprocess.run(
            [sys.executable, "-m", "hinglish", "--ast", str(hello_file)],
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(ast_res.returncode, 0)
        self.assertIn("Program", ast_res.stdout)

        # --transpile
        trans_res = subprocess.run(
            [sys.executable, "-m", "hinglish", "--transpile", str(hello_file)],
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(trans_res.returncode, 0)
        self.assertIn("if naam == 'Neeraj':", trans_res.stdout)


if __name__ == "__main__":
    unittest.main()
