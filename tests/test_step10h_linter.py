"""Unit tests for Step 10H: Hinglish Linter & Static Analysis."""

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from hinglish import lint_source
from hinglish.linter import Diagnostic, HinglishLinter, Severity, lint_file
from hinglish.lsp.analyzer import HinglishAnalyzer
from hinglish.lsp.documents import Document
from hinglish.lsp.protocol import DiagnosticSeverity


class TestStep10hLinter(unittest.TestCase):
    """Verifies static analysis rules, scope engine, CLI, and LSP diagnostics."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.repo_root = Path(__file__).parent.parent.resolve()

    def _run_cli(self, args: list, input_data: str = None) -> subprocess.CompletedProcess:
        """Helper to invoke CLI in subprocess."""
        cmd = [sys.executable, "-m", "hinglish.cli"] + args
        return subprocess.run(
            cmd,
            input=input_data,
            capture_output=True,
            text=True,
            cwd=str(self.repo_root),
            check=False,
        )

    # -------------------------------------------------------------------------
    # 1. Core Diagnostic & Public API
    # -------------------------------------------------------------------------

    def test_diagnostic_structure_and_formatting(self) -> None:
        """Verifies Diagnostic dataclass, format_cli, and serialization."""
        d = Diagnostic(
            rule_id="H001",
            message="undefined name 'test_var'",
            severity=Severity.ERROR,
            line=5,
            column=10,
            end_line=5,
            end_column=18,
            filename="script.hin",
        )
        self.assertEqual(d.format_cli(), "script.hin:5:10: error H001: undefined name 'test_var'")
        d_dict = d.to_dict()
        self.assertEqual(d_dict["rule_id"], "H001")
        self.assertEqual(d_dict["severity"], "error")
        self.assertEqual(d_dict["line"], 5)
        self.assertEqual(d_dict["column"], 10)

    def test_diagnostic_determinism_and_sorting(self) -> None:
        """Verifies that diagnostics sort deterministically by location and rule."""
        code = """
kaam test():
    wapas 10
    dikhao("unreachable")
    dikhao(kuch_bhi)
"""
        diags1 = lint_source(code)
        diags2 = lint_source(code)
        self.assertEqual(diags1, diags2)
        # Verify ordered by line
        lines = [d.line for d in diags1]
        self.assertEqual(lines, sorted(lines))

    def test_public_api_export(self) -> None:
        """Verifies top-level export of lint_source."""
        import hinglish
        self.assertTrue(hasattr(hinglish, "lint_source"))
        self.assertTrue(callable(hinglish.lint_source))

    # -------------------------------------------------------------------------
    # 2. Rule H001: Undefined Name
    # -------------------------------------------------------------------------

    def test_rule_h001_undefined_variable(self) -> None:
        """Verifies detection of unassigned and unimported variable reads."""
        code = "dikhao(naam_jo_nahi_hai)"
        diags = lint_source(code)
        self.assertEqual(len(diags), 1)
        self.assertEqual(diags[0].rule_id, "H001")
        self.assertEqual(diags[0].severity, Severity.ERROR.value)
        self.assertIn("naam_jo_nahi_hai", diags[0].message)

    def test_rule_h001_builtins_not_flagged(self) -> None:
        """Verifies that Hinglish builtins and Python builtins are resolved cleanly."""
        code = """
s1 = lambai("namaste")
k = kram(10)
x = purnank("42")
y = dashamlav("3.14")
s2 = akshar(100)
total = kul_jod([1, 2, 3])
top = adhiktam(10, 20)
low = nyuntam(5, 2)
dikhao(s1, k, x, y, s2, total, top, low)
"""
        diags = lint_source(code)
        self.assertEqual(len(diags), 0)

    def test_rule_h001_literals_and_aliases_not_flagged(self) -> None:
        """Verifies sahi, galat, kuch_nahi, shunya are not flagged as undefined."""
        code = """
a = sahi
b = galat
c = kuch_nahi
d = shunya
chapo(a, b, c, d)
"""
        diags = lint_source(code)
        self.assertEqual(len(diags), 0)

    # -------------------------------------------------------------------------
    # 3. Rule H002: Unused Variable
    # -------------------------------------------------------------------------

    def test_rule_h002_unused_local_variable(self) -> None:
        """Verifies unused local variable in function scope is flagged."""
        code = """
kaam hisab():
    vyarth = 100
    kul = 200
    wapas kul
"""
        diags = lint_source(code)
        self.assertEqual(len(diags), 1)
        self.assertEqual(diags[0].rule_id, "H002")
        self.assertIn("vyarth", diags[0].message)

    def test_rule_h002_module_level_variables_not_flagged(self) -> None:
        """Verifies module-level exports/constants are not flagged as unused variables."""
        code = """
MAX_RETRIES = 5
DEBUG = sahi
dikhao("Ready")
"""
        diags = lint_source(code)
        self.assertEqual(len(diags), 0)

    def test_rule_h002_ignored_underscore_and_self(self) -> None:
        """Verifies _, _tmp, self, cls are not flagged as unused."""
        code = """
kaam process():
    _ = 10
    _temp = 20
    wapas 1

varg Worker:
    kaam run(self):
        wapas 42
"""
        diags = lint_source(code)
        self.assertEqual(len(diags), 0)

    # -------------------------------------------------------------------------
    # 4. Rule H003: Unused Import
    # -------------------------------------------------------------------------

    def test_rule_h003_unused_module_import(self) -> None:
        """Verifies unused 'laao' is flagged."""
        code = """
laao math
dikhao("Namaste")
"""
        diags = lint_source(code)
        self.assertEqual(len(diags), 1)
        self.assertEqual(diags[0].rule_id, "H003")
        self.assertIn("math", diags[0].message)

    def test_rule_h003_unused_from_import_and_aliases(self) -> None:
        """Verifies unused 'se ... laao ... jaise ...' is flagged."""
        code = """
se math laao sqrt jaise s
dikhao("No math used")
"""
        diags = lint_source(code)
        self.assertEqual(len(diags), 1)
        self.assertEqual(diags[0].rule_id, "H003")
        self.assertIn("s", diags[0].message)

    def test_rule_h003_used_import_not_flagged(self) -> None:
        """Verifies referenced imports are clean."""
        code = """
laao math
se os laao path
dikhao(math.pi)
dikhao(path.exists("test"))
"""
        diags = lint_source(code)
        self.assertEqual(len(diags), 0)

    # -------------------------------------------------------------------------
    # 5. Rule H004: Duplicate Definition
    # -------------------------------------------------------------------------

    def test_rule_h004_duplicate_functions(self) -> None:
        """Verifies duplicate function definitions in same scope trigger H004."""
        code = """
kaam greet():
    chhod_do

kaam greet():
    chhod_do
"""
        diags = lint_source(code)
        self.assertEqual(len(diags), 1)
        self.assertEqual(diags[0].rule_id, "H004")
        self.assertIn("duplicate function definition 'greet'", diags[0].message)

    def test_rule_h004_duplicate_classes(self) -> None:
        """Verifies duplicate class definitions in same scope trigger H004."""
        code = """
varg Item:
    chhod_do

varg Item:
    chhod_do
"""
        diags = lint_source(code)
        self.assertEqual(len(diags), 1)
        self.assertEqual(diags[0].rule_id, "H004")
        self.assertIn("duplicate class definition 'Item'", diags[0].message)

    # -------------------------------------------------------------------------
    # 6. Rule H005: Unreachable Code
    # -------------------------------------------------------------------------

    def test_rule_h005_after_return(self) -> None:
        """Verifies statement following wapas is flagged."""
        code = """
kaam test():
    wapas 10
    dikhao("never")
"""
        diags = lint_source(code)
        self.assertEqual(len(diags), 1)
        self.assertEqual(diags[0].rule_id, "H005")
        self.assertIn("wapas", diags[0].message)

    def test_rule_h005_after_raise_and_break(self) -> None:
        """Verifies statements following uthav and ruko are flagged."""
        code = """
kaam err():
    uthav ValueError("boom")
    dikhao("unreachable")

kaam loop():
    jabtak sahi:
        ruko
        dikhao("unreachable in loop")
"""
        diags = lint_source(code)
        h005_diags = [d for d in diags if d.rule_id == "H005"]
        self.assertEqual(len(h005_diags), 2)

    # -------------------------------------------------------------------------
    # 7. Rule H006: Constant Condition
    # -------------------------------------------------------------------------

    def test_rule_h006_constant_agar_and_jabtak(self) -> None:
        """Verifies trivially constant conditions in agar and jabtak."""
        code = """
agar sahi:
    dikhao("yes")

warna_agar galat:
    dikhao("no")

jabtak galat:
    dikhao("never")
"""
        diags = lint_source(code)
        h006_diags = [d for d in diags if d.rule_id == "H006"]
        self.assertEqual(len(h006_diags), 3)

    # -------------------------------------------------------------------------
    # 8. Rule H007: Shadowed Name
    # -------------------------------------------------------------------------

    def test_rule_h007_shadowed_builtin_function(self) -> None:
        """Verifies variable and parameter shadowing built-in functions."""
        code = """
kaam f(dikhao):
    lambai = 10
    wapas lambai
"""
        diags = lint_source(code)
        h007_diags = [d for d in diags if d.rule_id == "H007"]
        self.assertEqual(len(h007_diags), 2)
        msgs = " ".join([d.message for d in h007_diags])
        self.assertIn("dikhao", msgs)
        self.assertIn("lambai", msgs)

    # -------------------------------------------------------------------------
    # 9. Advanced Scope Analysis Scenarios
    # -------------------------------------------------------------------------

    def test_scope_globals_sarvavyapi(self) -> None:
        """Verifies sarvavyapi properly writes to and reads from module scope."""
        code = """
counter = 0

kaam increment():
    sarvavyapi counter
    counter = counter + 1

increment()
dikhao(counter)
"""
        diags = lint_source(code)
        self.assertEqual(len(diags), 0)

    def test_scope_nonlocals_asthanik(self) -> None:
        """Verifies asthanik resolves to outer function scope."""
        code = """
kaam outer():
    val = 10
    kaam inner():
        asthanik val
        val = val + 5
    inner()
    wapas val

dikhao(outer())
"""
        diags = lint_source(code)
        self.assertEqual(len(diags), 0)

    def test_scope_forward_references_in_module(self) -> None:
        """Verifies that calling a function defined lower down in module scope works."""
        code = """
kaam run_pipeline():
    step_one()
    step_two()

kaam step_one():
    dikhao("1")

kaam step_two():
    dikhao("2")

run_pipeline()
"""
        diags = lint_source(code)
        self.assertEqual(len(diags), 0)

    def test_scope_comprehensions(self) -> None:
        """Verifies comprehension clauses bind their loop targets cleanly."""
        code = """
items = [1, 2, 3]
squares = [x * x har x mein items agar x > 1]
mapped = {f"k_{k}": v * 2 har k, v mein [(1, 10), (2, 20)]}
dikhao(squares, mapped)
"""
        diags = lint_source(code)
        self.assertEqual(len(diags), 0)

    def test_scope_pattern_matching_captures(self) -> None:
        """Verifies structural pattern matching captures bind pattern variables."""
        code = """
status = [10, 20, 30]
milaao status:
    vichaar [head, *tail]:
        dikhao(head)
        dikhao(tail)
    vichaar other:
        dikhao(other)
"""
        diags = lint_source(code)
        self.assertEqual(len(diags), 0)

    def test_scope_walrus_operator(self) -> None:
        """Verifies walrus operator assignment binds in outer scope."""
        code = """
numbers = [1, 2, 3]
results = [(total := n * 2) har n mein numbers]
dikhao(total)
dikhao(results)
"""
        diags = lint_source(code)
        self.assertEqual(len(diags), 0)

    def test_scope_exception_and_context_managers(self) -> None:
        """Verifies target bindings in pakdo ... jaise and saath ... jaise."""
        code = """
koshish:
    saath khol("test.txt") jaise fp:
        dikhao(fp)
pakdo Exception jaise exc:
    dikhao(exc)
"""
        diags = lint_source(code)
        self.assertEqual(len(diags), 0)

    # -------------------------------------------------------------------------
    # 10. CLI Integration
    # -------------------------------------------------------------------------

    def test_cli_lint_clean_file(self) -> None:
        """Verifies CLI exit code 0 on clean file."""
        with tempfile.NamedTemporaryFile("w", suffix=".hin", delete=False) as f:
            f.write('dikhao("Clean code")\n')
            temp_path = Path(f.name)

        try:
            res = self._run_cli(["lint", str(temp_path)])
            self.assertEqual(res.returncode, 0)
            self.assertEqual(res.stdout.strip(), "")
        finally:
            temp_path.unlink(missing_ok=True)

    def test_cli_lint_warnings_without_check(self) -> None:
        """Verifies CLI exit code 0 on warnings when --check is not specified."""
        with tempfile.NamedTemporaryFile("w", suffix=".hin", delete=False) as f:
            f.write('kaam f():\n    unused = 10\n    dikhao(1)\n')
            temp_path = Path(f.name)

        try:
            res = self._run_cli(["lint", str(temp_path)])
            self.assertEqual(res.returncode, 0)
            self.assertIn("warning H002", res.stdout)
        finally:
            temp_path.unlink(missing_ok=True)

    def test_cli_lint_warnings_with_check(self) -> None:
        """Verifies CLI exit code 1 on warnings when --check is specified."""
        with tempfile.NamedTemporaryFile("w", suffix=".hin", delete=False) as f:
            f.write('kaam f():\n    unused = 10\n    dikhao(1)\n')
            temp_path = Path(f.name)

        try:
            res = self._run_cli(["lint", "--check", str(temp_path)])
            self.assertEqual(res.returncode, 1)
            self.assertIn("warning H002", res.stdout)
        finally:
            temp_path.unlink(missing_ok=True)

    def test_cli_lint_errors(self) -> None:
        """Verifies CLI exit code 1 on error-level diagnostics."""
        with tempfile.NamedTemporaryFile("w", suffix=".hin", delete=False) as f:
            f.write('dikhao(unknown_name)\n')
            temp_path = Path(f.name)

        try:
            res = self._run_cli(["lint", str(temp_path)])
            self.assertEqual(res.returncode, 1)
            self.assertIn("error H001", res.stdout)
        finally:
            temp_path.unlink(missing_ok=True)

    def test_cli_lint_multiple_files(self) -> None:
        """Verifies multi-file linting across multiple arguments."""
        f1 = tempfile.NamedTemporaryFile("w", suffix=".hin", delete=False)
        f2 = tempfile.NamedTemporaryFile("w", suffix=".hin", delete=False)
        try:
            f1.write('dikhao("Clean 1")\n')
            f1.close()
            f2.write('dikhao("Clean 2")\n')
            f2.close()

            res = self._run_cli(["lint", f1.name, f2.name])
            self.assertEqual(res.returncode, 0)
        finally:
            Path(f1.name).unlink(missing_ok=True)
            Path(f2.name).unlink(missing_ok=True)

    def test_cli_lint_stdin(self) -> None:
        """Verifies reading code from stdin '-'."""
        code = 'dikhao(bad_var)\n'
        res = self._run_cli(["lint", "-"], input_data=code)
        self.assertEqual(res.returncode, 1)
        self.assertIn("<stdin>:1:8: error H001: undefined name 'bad_var'", res.stdout)

    def test_cli_lint_missing_file_error(self) -> None:
        """Verifies exit code 2 when target file does not exist."""
        res = self._run_cli(["lint", "definitely_does_not_exist_xyz.hin"])
        self.assertEqual(res.returncode, 2)
        self.assertIn("File not found", res.stderr)

    # -------------------------------------------------------------------------
    # 11. LSP Integration
    # -------------------------------------------------------------------------

    def test_lsp_diagnostics_integration(self) -> None:
        """Verifies that LSP analyzer emits proper DiagnosticSeverity and codes."""
        analyzer = HinglishAnalyzer()
        doc = Document(uri="file:///test.hin", text="kaam f():\n    unused_v = 1\n    dikhao(1)\n")
        lsp_diags = analyzer.get_diagnostics(doc)
        self.assertEqual(len(lsp_diags), 1)
        self.assertEqual(lsp_diags[0].code, "H002")
        self.assertEqual(lsp_diags[0].severity, DiagnosticSeverity.Warning)
        self.assertEqual(lsp_diags[0].source, "hinglish-lint")

    def test_lsp_syntax_error_resilience(self) -> None:
        """Verifies syntax errors are reported as Error without crashing the analyzer."""
        analyzer = HinglishAnalyzer()
        doc = Document(uri="file:///test.hin", text="kaam (\n")
        lsp_diags = analyzer.get_diagnostics(doc)
        self.assertEqual(len(lsp_diags), 1)
        self.assertEqual(lsp_diags[0].severity, DiagnosticSeverity.Error)
        self.assertEqual(lsp_diags[0].code, "syntax-error")


if __name__ == "__main__":
    unittest.main()
