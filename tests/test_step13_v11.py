"""Comprehensive unit and integration test suite for Step 13: Hinglish v1.1.

Covers:
1. Feature A: Inline Conditional Expressions (<expr> agar <cond> warna <fallback>)
2. Feature B: Recursive Directory Support in CLI (format, lint, exit codes, -o safety)
3. Feature C: Bilingual Built-in Aliases (lambai, ginti, jod, sab, koi)
4. Feature D: Comprehension Syntax Diagnostics Hints (detecting Python 'for ... in')
"""

import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

import hinglish
from hinglish import compile as compile_hinglish
from hinglish import format_source, lint_source, parse, run, tokenize
from hinglish.ast import IfExp, Program
from hinglish.cli import create_parser, discover_hin_files, main
from hinglish.exceptions import HinglishError, HinglishSyntaxError
from hinglish.keywords import DEFAULT_KEYWORD_REGISTRY


class TestStep13InlineConditionals(unittest.TestCase):
    """Verifies parsing, compilation, runtime evaluation, formatting, and linting of IfExp."""

    def test_ast_node_creation_and_properties(self) -> None:
        """Verifies IfExp AST node structure and compatibility properties."""
        node = IfExp(body="a", condition="cond", orelse="b")
        self.assertEqual(node.body, "a")
        self.assertEqual(node.condition, "cond")
        self.assertEqual(node.orelse, "b")
        # Compatibility properties
        self.assertEqual(node.test, "cond")
        self.assertEqual(node.true_expression, "a")
        self.assertEqual(node.false_expression, "b")

    def test_parser_creates_ifexp(self) -> None:
        """Verifies parser generates an IfExp AST node."""
        code = 'x = "yes" agar sahi warna "no"\n'
        tree = parse(code)
        self.assertIsInstance(tree, Program)
        stmt = tree.body[0]
        self.assertIsInstance(stmt.value, IfExp)
        self.assertEqual(stmt.value.body.value, "yes")
        self.assertEqual(stmt.value.condition.value, True)
        self.assertEqual(stmt.value.orelse.value, "no")

    def test_compiler_transpilation(self) -> None:
        """Verifies compiler emits Python ternary expression."""
        code = 'x = "yes" agar is_ready warna "no"\n'
        py = compile_hinglish(code)
        self.assertIn("'yes' if is_ready else 'no'", py)

    def test_runtime_evaluation_true_branch(self) -> None:
        """Verifies true branch is evaluated when condition is truthy."""
        code = """
kaam get_msg(flag):
    wapas "haan" agar flag warna "naa"

res = get_msg(sahi)
"""
        ctx = run(code)
        self.assertEqual(ctx["res"], "haan")

    def test_runtime_evaluation_false_branch(self) -> None:
        """Verifies false branch is evaluated when condition is falsy."""
        code = """
kaam get_msg(flag):
    wapas "haan" agar flag warna "naa"

res = get_msg(galat)
"""
        ctx = run(code)
        self.assertEqual(ctx["res"], "naa")

    def test_lazy_evaluation_true_branch(self) -> None:
        """Verifies false branch is NOT evaluated when condition is true (lazy evaluation)."""
        code = """
# If orelse were eagerly evaluated, this would raise ZeroDivisionError
x = 42 agar sahi warna (1 / 0)
"""
        ctx = run(code)
        self.assertEqual(ctx["x"], 42)

    def test_lazy_evaluation_false_branch(self) -> None:
        """Verifies true branch is NOT evaluated when condition is false (lazy evaluation)."""
        code = """
# If body were eagerly evaluated, this would raise ZeroDivisionError
x = (1 / 0) agar galat warna 99
"""
        ctx = run(code)
        self.assertEqual(ctx["x"], 99)

    def test_right_associative_chaining(self) -> None:
        """Verifies chained conditionals evaluate right-associatively like Python."""
        code = """
kaam classify(score):
    wapas "A" agar score >= 90 warna "B" agar score >= 75 warna "C"

r1 = classify(95)
r2 = classify(80)
r3 = classify(60)
"""
        ctx = run(code)
        self.assertEqual(ctx["r1"], "A")
        self.assertEqual(ctx["r2"], "B")
        self.assertEqual(ctx["r3"], "C")

    def test_arithmetic_precedence(self) -> None:
        """Verifies arithmetic operators bind tighter than inline conditional."""
        code = """
x = 10 + 5 agar 2 > 1 warna 100 * 2
y = 10 + 5 agar 1 > 2 warna 100 * 2
"""
        ctx = run(code)
        self.assertEqual(ctx["x"], 15)
        self.assertEqual(ctx["y"], 200)

    def test_formatter_roundtrip(self) -> None:
        """Verifies source formatter formats and preserves conditional expressions."""
        src = 'val="A"   agar  x > 0   warna   "B"\n'
        formatted = format_source(src)
        self.assertEqual(formatted, 'val = "A" agar x > 0 warna "B"\n')
        # Idempotent
        self.assertEqual(format_source(formatted), formatted)

    def test_formatter_chained_conditionals(self) -> None:
        """Verifies formatting of chained conditional expressions."""
        src = 'val = "A" agar x == 1 warna "B" agar x == 2 warna "C"\n'
        formatted = format_source(src)
        self.assertEqual(formatted, src)

    def test_linter_checks_conditional_branches(self) -> None:
        """Verifies linter inspects body, condition, and orelse for undefined names."""
        code1 = 'x = undefined_a agar sahi warna 10\n'
        diags1 = lint_source(code1)
        self.assertTrue(any("undefined_a" in d.message for d in diags1))

        code2 = 'x = 10 agar undefined_cond warna 20\n'
        diags2 = lint_source(code2)
        self.assertTrue(any("undefined_cond" in d.message for d in diags2))

        code3 = 'x = 10 agar sahi warna undefined_b\n'
        diags3 = lint_source(code3)
        self.assertTrue(any("undefined_b" in d.message for d in diags3))

        clean_code = 'y = 10\nx = y agar y > 0 warna 0\n'
        diags_clean = lint_source(clean_code)
        self.assertEqual(len(diags_clean), 0)


class TestStep13RecursiveCLI(unittest.TestCase):
    """Verifies recursive directory discovery and safety for hinglish lint and format."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.repo_root = Path(__file__).parent.parent.resolve()

    def _run_cli(self, args: list, input_data: str = None) -> subprocess.CompletedProcess:
        cmd = [sys.executable, "-m", "hinglish.cli"] + args
        return subprocess.run(
            cmd,
            input=input_data,
            capture_output=True,
            text=True,
            cwd=str(self.repo_root),
            check=False,
        )

    def test_discover_hin_files_helper(self) -> None:
        """Verifies discover_hin_files discovers *.hin, ignores non-.hin, sorts deterministically."""
        with tempfile.TemporaryDirectory() as td:
            base = Path(td)
            sub = base / "nested" / "sub"
            sub.mkdir(parents=True)

            (base / "b.hin").write_text('dikhao("b")\n', encoding="utf-8")
            (base / "a.hin").write_text('dikhao("a")\n', encoding="utf-8")
            (base / "readme.txt").write_text("ignore me\n", encoding="utf-8")
            (sub / "c.hin").write_text('dikhao("c")\n', encoding="utf-8")
            (sub / "helper.py").write_text("# ignore me\n", encoding="utf-8")

            files, has_dir, err, code = discover_hin_files([str(base)])
            self.assertIsNone(err)
            self.assertEqual(code, 0)
            self.assertTrue(has_dir)
            self.assertEqual(len(files), 3)

            rel_names = [f.relative_to(base).as_posix() for f in files]
            # Must be deterministically sorted
            self.assertEqual(rel_names, ["a.hin", "b.hin", "nested/sub/c.hin"])

    def test_cli_lint_directory_clean(self) -> None:
        """Verifies hinglish lint <dir> succeeds on clean files."""
        with tempfile.TemporaryDirectory() as td:
            base = Path(td)
            (base / "f1.hin").write_text('dikhao("f1")\n', encoding="utf-8")
            sub = base / "sub"
            sub.mkdir()
            (sub / "f2.hin").write_text('dikhao("f2")\n', encoding="utf-8")

            res = self._run_cli(["lint", str(base)])
            self.assertEqual(res.returncode, 0)
            self.assertEqual(res.stdout.strip(), "")

    def test_cli_lint_directory_with_errors(self) -> None:
        """Verifies hinglish lint <dir> returns 1 when any file has errors."""
        with tempfile.TemporaryDirectory() as td:
            base = Path(td)
            (base / "f1.hin").write_text('dikhao("f1")\n', encoding="utf-8")
            (base / "f2.hin").write_text('dikhao(unknown_variable_xyz)\n', encoding="utf-8")

            res = self._run_cli(["lint", str(base)])
            self.assertEqual(res.returncode, 1)
            self.assertIn("error H001: undefined name 'unknown_variable_xyz'", res.stdout)

    def test_cli_lint_nonexistent_directory(self) -> None:
        """Verifies hinglish lint on nonexistent directory exits with code 2."""
        res = self._run_cli(["lint", "definitely_nonexistent_dir_12345/"])
        self.assertEqual(res.returncode, 2)
        self.assertIn("File not found", res.stderr)

    def test_cli_format_directory_in_place(self) -> None:
        """Verifies hinglish format <dir> recursively formats files in place."""
        with tempfile.TemporaryDirectory() as td:
            base = Path(td)
            f1 = base / "unformatted1.hin"
            f1.write_text("x=10+20\n", encoding="utf-8")

            sub = base / "sub"
            sub.mkdir()
            f2 = sub / "unformatted2.hin"
            f2.write_text("y=a   agar   b   warna   c\n", encoding="utf-8")

            res = self._run_cli(["format", str(base)])
            self.assertEqual(res.returncode, 0)
            self.assertEqual(f1.read_text(encoding="utf-8"), "x = 10 + 20\n")
            self.assertEqual(f2.read_text(encoding="utf-8"), "y = a agar b warna c\n")

    def test_cli_format_directory_check_flag(self) -> None:
        """Verifies hinglish format <dir> --check reports unformatted files and exits 1."""
        with tempfile.TemporaryDirectory() as td:
            base = Path(td)
            f = base / "unformatted.hin"
            f.write_text("x=10+20\n", encoding="utf-8")

            res = self._run_cli(["format", str(base), "--check"])
            self.assertEqual(res.returncode, 1)
            self.assertIn("File would be reformatted", res.stderr)
            # File should not be modified
            self.assertEqual(f.read_text(encoding="utf-8"), "x=10+20\n")

    def test_cli_format_rejects_output_with_directory(self) -> None:
        """Verifies hinglish format <dir> -o out.hin is rejected with exit code 2."""
        with tempfile.TemporaryDirectory() as td:
            base = Path(td)
            (base / "test.hin").write_text("x = 1\n", encoding="utf-8")

            res = self._run_cli(["format", str(base), "-o", "out.hin"])
            self.assertEqual(res.returncode, 2)
            self.assertIn("-o/--output cannot be used with multiple files or directory targets", res.stderr)

    def test_cli_format_rejects_output_with_multiple_files(self) -> None:
        """Verifies hinglish format file1.hin file2.hin -o out.hin is rejected with exit code 2."""
        with tempfile.TemporaryDirectory() as td:
            base = Path(td)
            f1 = base / "a.hin"
            f2 = base / "b.hin"
            f1.write_text("x = 1\n", encoding="utf-8")
            f2.write_text("y = 2\n", encoding="utf-8")

            res = self._run_cli(["format", str(f1), str(f2), "-o", "out.hin"])
            self.assertEqual(res.returncode, 2)
            self.assertIn("-o/--output cannot be used with multiple files or directory targets", res.stderr)


class TestStep13BilingualBuiltins(unittest.TestCase):
    """Verifies bilingual built-in aliases: lambai, ginti, jod, sab, koi."""

    def test_default_globals_registration(self) -> None:
        """Verifies aliases are registered in runtime default globals."""
        from hinglish.runtime.context import get_default_globals
        g = get_default_globals()
        self.assertIn("lambai", g)
        self.assertIn("ginti", g)
        self.assertIn("jod", g)
        self.assertIn("sab", g)
        self.assertIn("koi", g)

        self.assertEqual(g["lambai"], len)
        self.assertEqual(g["ginti"], range)
        self.assertEqual(g["jod"], sum)
        self.assertEqual(g["sab"], all)
        self.assertEqual(g["koi"], any)

    def test_user_definitions_can_safely_shadow_aliases(self) -> None:
        """Verifies user variables and functions can shadow aliases without compiler corruption."""
        code = """
kaam jod(a, b):
    wapas a + b

res = jod(10, 20)

ginti = 1
jabtak ginti <= 3:
    ginti += 1
"""
        ctx = run(code)
        self.assertEqual(ctx["res"], 30)
        self.assertEqual(ctx["ginti"], 4)

    def test_runtime_execution_of_builtins(self) -> None:
        """Verifies runtime behavior of bilingual builtins."""
        code = """
numbers = [10, 20, 30]
n = lambai(numbers)
total = jod(numbers)
r_list = [x har x mein ginti(1, 4)]
all_true = sab([sahi, sahi])
all_false = sab([sahi, galat])
any_true = koi([galat, sahi])
any_false = koi([galat, galat])
"""
        ctx = run(code)
        self.assertEqual(ctx["n"], 3)
        self.assertEqual(ctx["total"], 60)
        self.assertEqual(ctx["r_list"], [1, 2, 3])
        self.assertEqual(ctx["all_true"], True)
        self.assertEqual(ctx["all_false"], False)
        self.assertEqual(ctx["any_true"], True)
        self.assertEqual(ctx["any_false"], False)

    def test_linter_recognizes_builtins_without_warnings(self) -> None:
        """Verifies linter does not flag bilingual aliases as undefined variables."""
        code = """
items = [1, 2, 3]
x = lambai(items)
y = jod(items)
z = sab([sahi])
w = koi([galat])
har i mein ginti(3):
    dikhao(i)
"""
        diags = lint_source(code)
        self.assertEqual(len(diags), 0)


class TestStep13ComprehensionDiagnostics(unittest.TestCase):
    """Verifies targeted syntax hints when Python 'for ... in' is used in comprehensions."""

    def test_list_comprehension_python_for_hint(self) -> None:
        """Verifies [x for x in xs] raises helpful Hinglish comprehension hint."""
        code = "[x for x in numbers]\n"
        with self.assertRaises(HinglishSyntaxError) as ctx:
            parse(code)
        err_msg = str(ctx.exception)
        self.assertIn("Python-style 'for ... in ...' is not used in Hinglish comprehensions", err_msg)
        self.assertIn("[x har x mein xs]", err_msg)

    def test_set_comprehension_python_for_hint(self) -> None:
        """Verifies {x for x in xs} raises helpful Hinglish comprehension hint."""
        code = "{x for x in numbers}\n"
        with self.assertRaises(HinglishSyntaxError) as ctx:
            parse(code)
        err_msg = str(ctx.exception)
        self.assertIn("Python-style 'for ... in ...' is not used in Hinglish comprehensions", err_msg)
        self.assertIn("{x har x mein xs}", err_msg)

    def test_dict_comprehension_python_for_hint(self) -> None:
        """Verifies {k: v for k, v in items} raises helpful Hinglish comprehension hint."""
        code = "{k: v for k, v in items}\n"
        with self.assertRaises(HinglishSyntaxError) as ctx:
            parse(code)
        err_msg = str(ctx.exception)
        self.assertIn("Python-style 'for ... in ...' is not used in Hinglish comprehensions", err_msg)
        self.assertIn("{k: v har x mein xs}", err_msg)

    def test_generator_comprehension_python_for_hint(self) -> None:
        """Verifies (x for x in xs) raises helpful Hinglish comprehension hint."""
        code = "(x for x in numbers)\n"
        with self.assertRaises(HinglishSyntaxError) as ctx:
            parse(code)
        err_msg = str(ctx.exception)
        self.assertIn("Python-style 'for ... in ...' is not used in Hinglish comprehensions", err_msg)
        self.assertIn("(x har x mein xs)", err_msg)

    def test_valid_hinglish_comprehensions_remain_intact(self) -> None:
        """Verifies standard Hinglish comprehensions work cleanly and execute as expected."""
        code = """
xs = [1, 2, 3]
doubles = [x * 2 har x mein xs]
evens_set = {x har x mein xs agar x % 2 == 0}
squared_dict = {f"k_{x}": x * x har x mein xs}
gen_list = [v har v mein (y * 10 har y mein xs)]
"""
        ctx = run(code)
        self.assertEqual(ctx["doubles"], [2, 4, 6])
        self.assertEqual(ctx["evens_set"], {2})
        self.assertEqual(ctx["squared_dict"], {"k_1": 1, "k_2": 4, "k_3": 9})
        self.assertEqual(ctx["gen_list"], [10, 20, 30])


if __name__ == "__main__":
    unittest.main()
