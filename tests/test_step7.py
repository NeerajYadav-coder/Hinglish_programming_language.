"""Comprehensive Test Suite for Step 7: Decorators, Comprehensions, Lambda, and Generators."""

import io
import sys
import unittest
from pathlib import Path

from hinglish.ast import (
    ClassDefinition,
    DictComprehension,
    FunctionDefinition,
    GeneratorExpression,
    LambdaExpression,
    ListComprehension,
    SetComprehension,
    SetLiteral,
    Yield,
    YieldFrom,
)
from hinglish.compiler import HinglishCompiler
from hinglish.exceptions import HinglishSyntaxError
from hinglish.parser import parse
from hinglish.runtime import run, run_file


class TestStep7LanguageFeatures(unittest.TestCase):
    """Verifies end-to-end lexer, parser, compiler, and runtime for Step 7 additions."""

    def setUp(self) -> None:
        self.compiler = HinglishCompiler()

    def _compile(self, source: str) -> str:
        """Helper to parse and compile Hinglish source to Python."""
        ast_tree = parse(source)
        return self.compiler.compile(ast_tree)

    # -------------------------------------------------------------------------
    # A. Decorators Tests
    # -------------------------------------------------------------------------

    def test_decorator_function_ast_and_compilation(self) -> None:
        """Function definition preserves decorators list in AST and compiles with @ syntax."""
        src = """
kaam dec(f):
    wapas f

@dec
kaam greet(naam):
    wapas f"Hello {naam}"
"""
        tree = parse(src)
        self.assertEqual(len(tree.body), 2)
        func_node = tree.body[1]
        self.assertIsInstance(func_node, FunctionDefinition)
        self.assertEqual(len(func_node.decorators), 1)

        py = self.compiler.compile(tree)
        self.assertIn("@dec\ndef greet(naam):", py)

        ns = run(src)
        self.assertEqual(ns["greet"]("Neeraj"), "Hello Neeraj")

    def test_decorator_with_arguments(self) -> None:
        """Decorator factories taking arguments compile and execute correctly."""
        src = """
kaam multiply_output(factor):
    kaam decorator(fn):
        kaam wrapper(x):
            wapas fn(x) * factor
        wapas wrapper
    wapas decorator

@multiply_output(5)
kaam calculate(n):
    wapas n + 2

natija = calculate(3)
"""
        ns = run(src)
        self.assertEqual(ns["natija"], 25)

    def test_chained_decorators(self) -> None:
        """Multiple stacked decorators apply in bottom-up order."""
        src = """
kaam wrap_b(fn):
    kaam wrapper():
        wapas f"<b>{fn()}</b>"
    wapas wrapper

kaam wrap_i(fn):
    kaam wrapper():
        wapas f"<i>{fn()}</i>"
    wapas wrapper

@wrap_b
@wrap_i
kaam message():
    wapas "Namaste"

html = message()
"""
        tree = parse(src)
        func_node = tree.body[2]
        self.assertEqual(len(func_node.decorators), 2)

        ns = run(src)
        self.assertEqual(ns["html"], "<b><i>Namaste</i></b>")

    def test_class_decorators(self) -> None:
        """Decorators applied to class definitions modify or wrap the class."""
        src = """
kaam mark_audited(cls):
    cls.audited = sahi
    wapas cls

@mark_audited
varg Khata:
    kaam __init__(self, balance):
        self.balance = balance

k = Khata(500)
"""
        tree = parse(src)
        cls_node = tree.body[1]
        self.assertIsInstance(cls_node, ClassDefinition)
        self.assertEqual(len(cls_node.decorators), 1)

        ns = run(src)
        self.assertTrue(ns["Khata"].audited)
        self.assertEqual(ns["k"].balance, 500)

    def test_method_decorators_and_python_builtins(self) -> None:
        """Builtin Python decorators (@property, @staticmethod, @classmethod) work seamlessly."""
        src = """
varg Rectangle:
    kaam __init__(self, w, h):
        self.w = w
        self.h = h

    @property
    kaam area(self):
        wapas self.w * self.h

    @staticmethod
    kaam default_name():
        wapas "Rectangle"

r = Rectangle(4, 5)
area_val = r.area
name_val = Rectangle.default_name()
"""
        ns = run(src)
        self.assertEqual(ns["area_val"], 20)
        self.assertEqual(ns["name_val"], "Rectangle")

    def test_decorator_syntax_error_invalid_target(self) -> None:
        """A decorator followed by a non-definition raises HinglishSyntaxError."""
        src = """
@decorator
agar x > 5:
    dikhao(x)
"""
        with self.assertRaises(HinglishSyntaxError):
            parse(src)

    # -------------------------------------------------------------------------
    # B. Comprehensions Tests
    # -------------------------------------------------------------------------

    def test_list_comprehension_basic_and_filter(self) -> None:
        """List comprehensions compile and evaluate correctly with single and multiple filters."""
        src = """
numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
evens = [x har x mein numbers agar x % 2 == 0]
squares = [x * x har x mein numbers agar x > 3 agar x < 8]
"""
        tree = parse(src)
        self.assertIsInstance(tree.body[1].value, ListComprehension)
        self.assertIsInstance(tree.body[2].value, ListComprehension)

        ns = run(src)
        self.assertEqual(ns["evens"], [2, 4, 6, 8, 10])
        self.assertEqual(ns["squares"], [16, 25, 36, 49])

    def test_list_comprehension_multiple_generators(self) -> None:
        """Nested/multi-loop list comprehensions compile correctly."""
        src = """
pairs = [f"{x}{y}" har x mein ["A", "B"] har y mein [1, 2]]
"""
        tree = parse(src)
        comp = tree.body[0].value
        self.assertIsInstance(comp, ListComprehension)
        self.assertEqual(len(comp.clauses), 2)

        ns = run(src)
        self.assertEqual(ns["pairs"], ["A1", "A2", "B1", "B2"])

    def test_dict_comprehension(self) -> None:
        """Dict comprehensions compile and build dictionaries."""
        src = """
cube_map = {x: x * x * x har x mein [1, 2, 3, 4] agar x % 2 == 0}
"""
        tree = parse(src)
        self.assertIsInstance(tree.body[0].value, DictComprehension)

        ns = run(src)
        self.assertEqual(ns["cube_map"], {2: 8, 4: 64})

    def test_set_comprehension_and_set_literal(self) -> None:
        """Set comprehensions and set literals are correctly parsed and differentiated."""
        src = """
mod_set = {x % 3 har x mein [1, 2, 3, 4, 5, 6]}
plain_set = {10, 20, 30, 20, 10}
empty_dict = {}
"""
        tree = parse(src)
        self.assertIsInstance(tree.body[0].value, SetComprehension)
        self.assertIsInstance(tree.body[1].value, SetLiteral)

        ns = run(src)
        self.assertEqual(ns["mod_set"], {0, 1, 2})
        self.assertEqual(ns["plain_set"], {10, 20, 30})
        self.assertEqual(ns["empty_dict"], {})

    def test_generator_expression(self) -> None:
        """Generator expressions create lazy generator objects."""
        src = """
gen = (x * 10 har x mein [1, 2, 3])
first = next(gen)
second = next(gen)
rest = list(gen)
"""
        tree = parse(src)
        self.assertIsInstance(tree.body[0].value, GeneratorExpression)

        ns = run(src)
        self.assertEqual(ns["first"], 10)
        self.assertEqual(ns["second"], 20)
        self.assertEqual(ns["rest"], [30])

    # -------------------------------------------------------------------------
    # C. Lambda / Anonymous Functions Tests
    # -------------------------------------------------------------------------

    def test_lambda_basic_and_ast(self) -> None:
        """Lambda expressions parse into LambdaExpression AST nodes and execute."""
        src = """
add = sookshm a, b: a + b
res = add(10, 20)
"""
        tree = parse(src)
        self.assertIsInstance(tree.body[0].value, LambdaExpression)
        self.assertEqual(tree.body[0].value.params, ["a", "b"])

        ns = run(src)
        self.assertEqual(ns["res"], 30)

    def test_lambda_zero_arguments(self) -> None:
        """Lambda with no parameters (sookshm: <expr>) works properly."""
        src = """
get_const = sookshm: 42
val = get_const()
"""
        tree = parse(src)
        self.assertIsInstance(tree.body[0].value, LambdaExpression)
        self.assertEqual(tree.body[0].value.params, [])

        ns = run(src)
        self.assertEqual(ns["val"], 42)

    def test_lambda_inline_immediate_call(self) -> None:
        """Parenthesized lambda can be immediately invoked."""
        src = """
ans = (sookshm x: x * 3 + 1)(7)
"""
        ns = run(src)
        self.assertEqual(ns["ans"], 22)

    def test_lambda_in_higher_order_functions(self) -> None:
        """Lambdas pass cleanly to built-in higher-order functions such as sorted()."""
        src = """
data = [{"id": 3, "score": 75}, {"id": 1, "score": 90}, {"id": 2, "score": 85}]
sorted_data = sorted(data, key=sookshm item: item["score"])
"""
        ns = run(src)
        self.assertEqual(ns["sorted_data"][0]["id"], 3)
        self.assertEqual(ns["sorted_data"][1]["id"], 2)
        self.assertEqual(ns["sorted_data"][2]["id"], 1)

    def test_lambda_closures(self) -> None:
        """Lambdas correctly close over variables in enclosing scopes."""
        src = """
kaam make_multiplier(n):
    wapas sookshm x: x * n

double = make_multiplier(2)
triple = make_multiplier(3)

v1 = double(10)
v2 = triple(10)
"""
        ns = run(src)
        self.assertEqual(ns["v1"], 20)
        self.assertEqual(ns["v2"], 30)

    # -------------------------------------------------------------------------
    # D. Generators & Yield Tests
    # -------------------------------------------------------------------------

    def test_generator_yield_and_iteration(self) -> None:
        """Functions with upaj produce Python generator objects and support lazy evaluation."""
        src = """
kaam count_up_to(limit):
    curr = 1
    jabtak curr <= limit:
        upaj curr
        curr = curr + 1

gen = count_up_to(3)
p1 = next(gen)
p2 = next(gen)
p3 = next(gen)
"""
        tree = parse(src)
        fn_body = tree.body[0].body
        # While loop has yield
        while_body = fn_body[1].body
        self.assertIsInstance(while_body[0].expr, Yield)

        ns = run(src)
        self.assertEqual(ns["p1"], 1)
        self.assertEqual(ns["p2"], 2)
        self.assertEqual(ns["p3"], 3)

    def test_bare_yield(self) -> None:
        """Bare upaj statement/expression yields None."""
        src = """
kaam pause_signal():
    upaj
    upaj 99

g = pause_signal()
val1 = next(g)
val2 = next(g)
"""
        tree = parse(src)
        fn_body = tree.body[0].body
        self.assertIsInstance(fn_body[0].expr, Yield)
        self.assertIsNone(fn_body[0].expr.value)

        ns = run(src)
        self.assertIsNone(ns["val1"])
        self.assertEqual(ns["val2"], 99)

    def test_yield_from_delegation(self) -> None:
        """upaj se delegates yielding to sub-generators."""
        src = """
kaam sub_seq():
    upaj 20
    upaj 30

kaam main_seq():
    upaj 10
    upaj se sub_seq()
    upaj 40

items = [x har x mein main_seq()]
"""
        tree = parse(src)
        fn_body = tree.body[1].body
        self.assertIsInstance(fn_body[1].expr, YieldFrom)

        ns = run(src)
        self.assertEqual(ns["items"], [10, 20, 30, 40])

    def test_generator_lazy_evaluation(self) -> None:
        """Infinite generator can be consumed partially without hanging."""
        src = """
kaam infinite_sequence():
    val = 1
    jabtak sahi:
        upaj val
        val = val + 1

collected = []
har x mein infinite_sequence():
    collected.append(x)
    agar x >= 5:
        ruko
"""
        ns = run(src)
        self.assertEqual(ns["collected"], [1, 2, 3, 4, 5])

    # -------------------------------------------------------------------------
    # E. Execution of Step 7 Canonical Examples
    # -------------------------------------------------------------------------

    def test_run_canonical_examples(self) -> None:
        """Executes all 4 Step 7 canonical example files from disk."""
        examples_dir = Path(__file__).resolve().parent.parent / "examples"
        example_files = [
            "decorators.hin",
            "comprehensions.hin",
            "lambda.hin",
            "generators.hin",
        ]

        for fname in example_files:
            file_path = examples_dir / fname
            self.assertTrue(file_path.exists(), f"Example file {fname} should exist")

            saved_stdout = sys.stdout
            sys.stdout = io.StringIO()
            try:
                ns = run_file(file_path)
                out = sys.stdout.getvalue()
                self.assertIsNotNone(ns, f"Namespace returned for {fname}")
                self.assertGreater(len(out), 0, f"Expected output from {fname}")
            finally:
                sys.stdout = saved_stdout


if __name__ == "__main__":
    unittest.main()
