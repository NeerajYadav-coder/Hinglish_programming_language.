"""Unit and integration tests for Step 10B: Hinglish CLI & Real Project Experience."""

import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from hinglish.runtime import install_import_hook, run_file


class TestStep10bCLI(unittest.TestCase):
    """Verifies CLI subcommands, shorthands, exit codes, stdin, and multi-file projects."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.repo_root = Path(__file__).parent.parent.resolve()
        cls.hello_hin = cls.repo_root / "examples" / "hello.hin"
        cls.real_project_main = cls.repo_root / "examples" / "real_project" / "main.hin"

    def _run_cli(self, args: list, input_data: str = None, cwd: Path = None) -> subprocess.CompletedProcess:
        """Helper to run the CLI via python -m hinglish in a subprocess."""
        cmd = [sys.executable, "-m", "hinglish"] + args
        env = dict(os.environ)
        if "PYTHONPATH" in env:
            env["PYTHONPATH"] = f"{self.repo_root}:{env['PYTHONPATH']}"
        else:
            env["PYTHONPATH"] = str(self.repo_root)
        return subprocess.run(
            cmd,
            input=input_data,
            capture_output=True,
            text=True,
            cwd=str(cwd or self.repo_root),
            env=env,
            check=False,
        )

    # -------------------------------------------------------------------------
    # 1. Subcommands & Shorthands
    # -------------------------------------------------------------------------

    def test_subcommand_run(self) -> None:
        """Verifies 'hinglish run file.hin' executes correctly."""
        res = self._run_cli(["run", str(self.hello_hin)])
        self.assertEqual(res.returncode, 0)
        self.assertIn("Namaste duniya!", res.stdout)

    def test_subcommand_tokens(self) -> None:
        """Verifies 'hinglish tokens file.hin' produces token table."""
        res = self._run_cli(["tokens", str(self.hello_hin)])
        self.assertEqual(res.returncode, 0)
        self.assertIn("Tokens for", res.stdout)
        self.assertIn("IDENTIFIER", res.stdout)

    def test_subcommand_ast(self) -> None:
        """Verifies 'hinglish ast file.hin' produces AST dump."""
        res = self._run_cli(["ast", str(self.hello_hin)])
        self.assertEqual(res.returncode, 0)
        self.assertIn("Hinglish AST for", res.stdout)
        self.assertIn("Program", res.stdout)

    def test_subcommand_transpile(self) -> None:
        """Verifies 'hinglish transpile file.hin' writes valid Python to stdout."""
        res = self._run_cli(["transpile", str(self.hello_hin)])
        self.assertEqual(res.returncode, 0)
        self.assertIn("if naam == 'Neeraj':", res.stdout)

    def test_transpile_output_flag(self) -> None:
        """Verifies 'hinglish transpile file.hin -o out.py' writes to file."""
        with tempfile.TemporaryDirectory() as td:
            out_file = Path(td) / "output.py"
            res = self._run_cli(["transpile", str(self.hello_hin), "-o", str(out_file)])
            self.assertEqual(res.returncode, 0)
            self.assertTrue(out_file.is_file())
            content = out_file.read_text(encoding="utf-8")
            self.assertIn("print('Namaste duniya!')", content)

    def test_transpile_output_overwrite_guard(self) -> None:
        """Verifies transpilation rejects overwriting source file."""
        res = self._run_cli(["transpile", str(self.hello_hin), "-o", str(self.hello_hin)])
        self.assertEqual(res.returncode, 1)
        self.assertIn("cannot overwrite the source file", res.stderr)

    def test_shorthand_backward_compatibility(self) -> None:
        """Verifies existing shorthand syntax continues working identically."""
        # Direct file
        res = self._run_cli([str(self.hello_hin)])
        self.assertEqual(res.returncode, 0)
        self.assertIn("Namaste duniya!", res.stdout)

        # --tokens
        res = self._run_cli(["--tokens", str(self.hello_hin)])
        self.assertEqual(res.returncode, 0)
        self.assertIn("Tokens for", res.stdout)

        # --ast
        res = self._run_cli(["--ast", str(self.hello_hin)])
        self.assertEqual(res.returncode, 0)
        self.assertIn("Program", res.stdout)

        # --transpile
        res = self._run_cli(["--transpile", str(self.hello_hin)])
        self.assertEqual(res.returncode, 0)
        self.assertIn("print('Namaste duniya!')", res.stdout)

    # -------------------------------------------------------------------------
    # 2. Stdin Pipeline Support
    # -------------------------------------------------------------------------

    def test_stdin_piped_execution(self) -> None:
        """Verifies piping code into hinglish executes without arguments."""
        code = 'x = 25\ndikhao(f"Piped value: {x * 2}")\n'
        res = self._run_cli([], input_data=code)
        self.assertEqual(res.returncode, 0)
        self.assertIn("Piped value: 50", res.stdout)

    def test_stdin_explicit_dash(self) -> None:
        """Verifies 'hinglish -' executes from standard input."""
        code = 'dikhao("Explicit dash stdin ok")\n'
        res = self._run_cli(["-"], input_data=code)
        self.assertEqual(res.returncode, 0)
        self.assertIn("Explicit dash stdin ok", res.stdout)

    # -------------------------------------------------------------------------
    # 3. Exit Codes
    # -------------------------------------------------------------------------

    def test_exit_code_success(self) -> None:
        """Exit code 0 on successful execution."""
        res = self._run_cli([str(self.hello_hin)])
        self.assertEqual(res.returncode, 0)

    def test_exit_code_missing_file(self) -> None:
        """Exit code 1 on file not found."""
        res = self._run_cli(["non_existent_file.hin"])
        self.assertEqual(res.returncode, 1)
        self.assertIn("File not found", res.stderr)

    def test_exit_code_syntax_error(self) -> None:
        """Exit code 1 on Hinglish syntax error."""
        with tempfile.NamedTemporaryFile("w", suffix=".hin", delete=False) as tf:
            tf.write("10 = x\n")
            temp_path = tf.name
        try:
            res = self._run_cli([temp_path])
            self.assertEqual(res.returncode, 1)
            self.assertIn("HinglishSyntaxError", res.stderr)
        finally:
            if os.path.exists(temp_path):
                os.unlink(temp_path)

    def test_exit_code_runtime_error(self) -> None:
        """Exit code 1 on runtime exception."""
        with tempfile.NamedTemporaryFile("w", suffix=".hin", delete=False) as tf:
            tf.write("x = 10 / 0\n")
            temp_path = tf.name
        try:
            res = self._run_cli([temp_path])
            self.assertEqual(res.returncode, 1)
            self.assertIn("ZeroDivisionError", res.stderr)
        finally:
            if os.path.exists(temp_path):
                os.unlink(temp_path)

    def test_exit_code_missing_subcommand_arg(self) -> None:
        """Exit code 2 on missing required argument for subcommand."""
        res = self._run_cli(["run"])
        self.assertEqual(res.returncode, 2)
        self.assertIn("requires a script file argument", res.stderr)

        res2 = self._run_cli(["tokens"])
        self.assertEqual(res2.returncode, 2)

    def test_exit_code_unrecognized_argument(self) -> None:
        """Exit code 2 on unrecognized CLI option."""
        res = self._run_cli(["--completely-bogus-flag"])
        self.assertEqual(res.returncode, 2)

    # -------------------------------------------------------------------------
    # 4. Multi-File Project & Working Directory Independence
    # -------------------------------------------------------------------------

    def test_real_project_execution(self) -> None:
        """Verifies examples/real_project/main.hin executes and prints expected results."""
        self.assertTrue(self.real_project_main.is_file())
        res = self._run_cli([str(self.real_project_main)])
        self.assertEqual(res.returncode, 0)
        self.assertIn("=== Hinglish Order Platform v1.0.0 ===", res.stdout)
        self.assertIn("Order 1 total (with tax): Rs. 92040.00", res.stdout)
        self.assertIn("High value orders: ['ORD-001', 'ORD-002']", res.stdout)
        self.assertIn("Async settlement:", res.stdout)
        self.assertIn("=== Hinglish Real Project Completed Successfully ===", res.stdout)

    def test_working_directory_independence(self) -> None:
        """Verifies running project from a completely different directory resolves imports."""
        with tempfile.TemporaryDirectory() as external_dir:
            res = self._run_cli([str(self.real_project_main)], cwd=Path(external_dir))
            self.assertEqual(res.returncode, 0)
            self.assertIn("=== Hinglish Order Platform v1.0.0 ===", res.stdout)
            self.assertIn("Successfully", res.stdout)

    def test_multi_file_source_mapped_tracebacks(self) -> None:
        """Verifies runtime errors in imported modules map back to .hin line numbers."""
        with tempfile.TemporaryDirectory() as td:
            p = Path(td)
            helper = p / "helper.hin"
            helper.write_text("kaam do_calculation(x):\n    wapas x / 0\n", encoding="utf-8")
            caller = p / "caller.hin"
            caller.write_text("se helper laao do_calculation\nres = do_calculation(42)\n", encoding="utf-8")

            res = self._run_cli([str(caller)], cwd=p)
            self.assertEqual(res.returncode, 1)
            # Check both caller and helper are in traceback
            self.assertIn("caller.hin", res.stderr)
            self.assertIn("line 2", res.stderr)
            self.assertIn("helper.hin", res.stderr)
            self.assertIn("line 2", res.stderr)
            self.assertIn("ZeroDivisionError", res.stderr)
            self.assertIn("wapas x / 0", res.stderr)

    # -------------------------------------------------------------------------
    # 5. Python Interoperability
    # -------------------------------------------------------------------------

    def test_python_to_hinglish_import(self) -> None:
        """Verifies a native Python module can import .hin files using import hook."""
        install_import_hook()
        real_project_dir = str(self.repo_root / "examples" / "real_project")
        if real_project_dir not in sys.path:
            sys.path.insert(0, real_project_dir)

        import config  # imports config.hin
        import utils   # imports utils.hin

        self.assertEqual(config.APP_NAME, "Hinglish Order Platform")
        self.assertIn("1.0.0", config.get_app_info())
        formatted = utils.mudra_format(500.0)
        self.assertEqual(formatted, "Rs. 500.00")

    def test_repl_invocation_with_pipe(self) -> None:
        """Verifies 'hinglish repl' handles input stream and exits cleanly."""
        res = self._run_cli(["repl"], input_data="dikhao('hello from repl')\nexit()\n")
        self.assertEqual(res.returncode, 0)
        self.assertIn("hello from repl", res.stdout)


if __name__ == "__main__":
    unittest.main()
