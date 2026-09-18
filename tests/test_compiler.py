"""Comprehensive unit tests for the Hinglish Compiler and Python code generation."""

import ast
import io
import sys
import unittest
from pathlib import Path

from hinglish.compiler import HinglishCompiler, compile
from hinglish.parser import parse


class TestHinglishCompiler(unittest.TestCase):
    """Test suite verifying AST to Python 3 code generation, syntax validity, and semantic equivalence."""

    def assert_valid_python(self, py_code: str) -> None:
        """Helper to ensure generated code can be parsed by Python's ast module."""
        try:
            ast.parse(py_code)
        except SyntaxError as err:
            self.fail(f"Generated Python code is not valid syntax:\n{py_code}\nError: {err}")

    def test_variable_assignment(self) -> None:
        source = 'naam = "Neeraj"\numar = 25\nx += 1\n'
        py = compile(source)
        self.assert_valid_python(py)
        self.assertIn("naam = 'Neeraj'", py)
        self.assertIn("umar = 25", py)
        self.assertIn("x += 1", py)

    def test_literals_code_gen(self) -> None:
        source = "a = 42\nb = 3.14\nc = 3j\nd = 'namaste'\ne = sahi\nf = galat\ng = kuch_nahi\n"
        py = compile(source)
        self.assert_valid_python(py)
        self.assertIn("a = 42", py)
        self.assertIn("b = 3.14", py)
        self.assertIn("c = 3j", py)
        self.assertIn("d = 'namaste'", py)
        self.assertIn("e = True", py)
        self.assertIn("f = False", py)
        self.assertIn("g = None", py)

    def test_operator_precedence_and_parentheses(self) -> None:
        # (x + 2) * 3 must retain parentheses
        source = "natija = (x + 2) * 3\n"
        py = compile(source)
        self.assert_valid_python(py)
        self.assertIn("(x + 2) * 3", py)

        # x + 2 * 3 does not need outer parentheses
        source2 = "natija = x + 2 * 3\n"
        py2 = compile(source2)
        self.assert_valid_python(py2)
        self.assertIn("x + 2 * 3", py2)

        # 2 ** 3 ** 2
        source3 = "natija = 2 ** 3 ** 2\n"
        py3 = compile(source3)
        self.assert_valid_python(py3)
        self.assertIn("2 ** 3 ** 2", py3)

    def test_comparisons_and_boolean_operations(self) -> None:
        source = "shart = x > 5 aur y < 10 ya nahi z\n"
        py = compile(source)
        self.assert_valid_python(py)
        self.assertIn("x > 5 and y < 10 or not z", py)

    def test_builtin_function_mapping(self) -> None:
        source = 'dikhao("Namaste", naam, end="\\n")\n'
        py = compile(source)
        self.assert_valid_python(py)
        self.assertIn("print('Namaste', naam, end='\\n')", py)

    def test_if_elif_else_statement(self) -> None:
        source = (
            'agar umar >= 18:\n'
            '    dikhao("bada")\n'
            'warna_agar umar >= 16:\n'
            '    dikhao("learner")\n'
            'warna:\n'
            '    dikhao("chhota")\n'
        )
        py = compile(source)
        self.assert_valid_python(py)
        self.assertIn("if umar >= 18:\n    print('bada')", py)
        self.assertIn("elif umar >= 16:\n    print('learner')", py)
        self.assertIn("else:\n    print('chhota')", py)

    def test_while_loop(self) -> None:
        source = (
            'ginti = 1\n'
            'jabtak ginti <= 5:\n'
            '    dikhao(ginti)\n'
            '    ginti += 1\n'
        )
        py = compile(source)
        self.assert_valid_python(py)
        self.assertIn("while ginti <= 5:\n    print(ginti)\n    ginti += 1", py)

    def test_for_loop(self) -> None:
        source = (
            'har x mein [1, 2, 3]:\n'
            '    dikhao(x)\n'
        )
        py = compile(source)
        self.assert_valid_python(py)
        self.assertIn("for x in [1, 2, 3]:\n    print(x)", py)

    def test_function_definition_and_return(self) -> None:
        source = (
            'kaam jod(a, b):\n'
            '    natija = a + b\n'
            '    wapas natija\n'
        )
        py = compile(source)
        self.assert_valid_python(py)
        self.assertIn("def jod(a, b):\n    natija = a + b\n    return natija", py)

    def test_pass_break_continue(self) -> None:
        source = "chhod_do\nruko\naage_bado\n"
        py = compile(source)
        self.assert_valid_python(py)
        self.assertEqual(py.strip(), "pass\nbreak\ncontinue")

    def test_lists_dicts_tuples(self) -> None:
        source = "soochi = [1, 2, 'teen']\nkosh = {'a': 1, 'b': 2}\ntup = (10, 20)\n"
        py = compile(source)
        self.assert_valid_python(py)
        self.assertIn("soochi = [1, 2, 'teen']", py)
        self.assertIn("kosh = {'a': 1, 'b': 2}", py)
        self.assertIn("tup = (10, 20)", py)

    def test_indexing_and_slices(self) -> None:
        source = "a = shehar[0]\nb = shehar[1:5]\nc = shehar[::2]\n"
        py = compile(source)
        self.assert_valid_python(py)
        self.assertIn("a = shehar[0]", py)
        self.assertIn("b = shehar[1:5]", py)
        self.assertIn("c = shehar[::2]", py)

    def test_attribute_access(self) -> None:
        source = "naam = vyakti.pata.shehar\nvyakti.dikhao()\n"
        py = compile(source)
        self.assert_valid_python(py)
        self.assertIn("naam = vyakti.pata.shehar", py)
        self.assertIn("vyakti.dikhao()", py)

    def test_imports_and_from_imports(self) -> None:
        source = (
            "laao math\n"
            "laao math jaise m\n"
            "se math laao sqrt jaise s\n"
        )
        py = compile(source)
        self.assert_valid_python(py)
        self.assertIn("import math", py)
        self.assertIn("import math as m", py)
        self.assertIn("from math import sqrt as s", py)

    def test_nested_blocks(self) -> None:
        source = (
            'agar a:\n'
            '    agar b:\n'
            '        dikhao("nested")\n'
            '    warna:\n'
            '        dikhao("else nested")\n'
        )
        py = compile(source)
        self.assert_valid_python(py)
        expected = (
            "if a:\n"
            "    if b:\n"
            "        print('nested')\n"
            "    else:\n"
            "        print('else nested')"
        )
        self.assertIn(expected, py)

    def test_semantic_execution(self) -> None:
        """Executes transpiled code to verify semantic correctness."""
        source = (
            'kaam factorial(n):\n'
            '    agar n <= 1:\n'
            '        wapas 1\n'
            '    wapas n * factorial(n - 1)\n'
            '\n'
            'ans = factorial(5)\n'
        )
        py = compile(source)
        self.assert_valid_python(py)

        env = {}
        exec(py, env)
        self.assertEqual(env["ans"], 120)

    def test_hello_world_execution_capture(self) -> None:
        """Transpiles hello.hin and verifies stdout matches expected output."""
        example_path = Path(__file__).parent.parent / "examples" / "hello.hin"
        source = example_path.read_text(encoding="utf-8")
        py = compile(source)
        self.assert_valid_python(py)

        captured_stdout = io.StringIO()
        old_stdout = sys.stdout
        try:
            sys.stdout = captured_stdout
            exec(py, {})
        finally:
            sys.stdout = old_stdout

        output = captured_stdout.getvalue().strip()
        self.assertEqual(output, "Namaste duniya!")

    def test_compile_all_example_files(self) -> None:
        example_dir = Path(__file__).parent.parent / "examples"
        hin_files = list(example_dir.glob("*.hin"))
        self.assertTrue(len(hin_files) >= 3)

        for hin_file in hin_files:
            content = hin_file.read_text(encoding="utf-8")
            py = compile(content)
            self.assert_valid_python(py)


if __name__ == "__main__":
    unittest.main()
