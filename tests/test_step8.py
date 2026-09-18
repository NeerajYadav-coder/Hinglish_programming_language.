"""Comprehensive Test Suite for Step 8: Async Programming & Advanced Python Syntax."""

import asyncio
import io
import sys
import unittest
from pathlib import Path

from hinglish.ast import (
    AnnAssign,
    AssignmentExpression,
    Await,
    For,
    FunctionDefinition,
    Match,
    MatchAs,
    MatchCase,
    MatchClass,
    MatchMapping,
    MatchOr,
    MatchSequence,
    MatchSingleton,
    MatchStar,
    MatchValue,
    Parameter,
    Starred,
    With,
)
from hinglish.compiler import HinglishCompiler
from hinglish.exceptions import HinglishSyntaxError
from hinglish.parser import parse
from hinglish.runtime import run, run_file


class TestStep8LanguageFeatures(unittest.TestCase):
    """Verifies end-to-end lexer, parser, compiler, and runtime for Step 8 additions."""

    def setUp(self) -> None:
        self.compiler = HinglishCompiler()

    def _compile(self, source: str) -> str:
        """Helper to parse and compile Hinglish source to Python."""
        ast_tree = parse(source)
        return self.compiler.compile(ast_tree)

    # -------------------------------------------------------------------------
    # 1. Async / Await Tests
    # -------------------------------------------------------------------------

    def test_async_function_ast_and_compilation(self) -> None:
        """Verifies async function parsing, AST structure, and compilation."""
        src = """
asamanantar kaam fetch(x: int) -> int:
    wapas x + 1
"""
        tree = parse(src)
        self.assertEqual(len(tree.body), 1)
        func_node = tree.body[0]
        self.assertIsInstance(func_node, FunctionDefinition)
        self.assertTrue(func_node.is_async)

        py = self.compiler.compile(tree)
        self.assertIn("async def fetch(x: int) -> int:", py)

    def test_async_await_execution(self) -> None:
        """Verifies coroutine awaiting and execution with asyncio.run()."""
        src = """
laao asyncio

asamanantar kaam add_delay(a, b):
    intezaar asyncio.sleep(0.001)
    wapas a + b

asamanantar kaam main():
    val = intezaar add_delay(15, 27)
    wapas val

ans = asyncio.run(main())
"""
        ns = run(src)
        self.assertEqual(ns["ans"], 42)

    def test_async_class_methods(self) -> None:
        """Verifies async methods defined within classes."""
        src = """
laao asyncio

varg Worker:
    kaam __init__(self, name):
        self.name = name

    asamanantar kaam perform(self, task):
        intezaar asyncio.sleep(0.001)
        wapas f"{self.name} completed {task}"

asamanantar kaam main():
    w = Worker("Worker-1")
    wapas intezaar w.perform("indexing")

result = asyncio.run(main())
"""
        ns = run(src)
        self.assertEqual(ns["result"], "Worker-1 completed indexing")

    def test_async_for_and_generator(self) -> None:
        """Verifies async generator (upaj) and async for (har intezaar)."""
        src = """
laao asyncio

asamanantar kaam count_up(limit):
    i = 1
    jabtak i <= limit:
        intezaar asyncio.sleep(0.001)
        upaj i
        i = i + 1

asamanantar kaam main():
    nums = []
    har intezaar n mein count_up(3):
        nums.append(n)
    wapas nums

result = asyncio.run(main())
"""
        ns = run(src)
        self.assertEqual(ns["result"], [1, 2, 3])

    def test_async_with_context_manager(self) -> None:
        """Verifies async context manager and async with (saath intezaar)."""
        src = """
laao asyncio

varg AsyncResource:
    kaam __init__(self):
        self.opened = galat
        self.closed = galat

    asamanantar kaam __aenter__(self):
        intezaar asyncio.sleep(0.001)
        self.opened = sahi
        wapas self

    asamanantar kaam __aexit__(self, exc_type, exc, tb):
        intezaar asyncio.sleep(0.001)
        self.closed = sahi

asamanantar kaam main():
    r = AsyncResource()
    saath intezaar r jaise res:
        state_inside = res.opened
    wapas (state_inside, r.closed)

result = asyncio.run(main())
"""
        ns = run(src)
        self.assertEqual(ns["result"], (True, True))

    def test_decorated_async_function(self) -> None:
        """Verifies decorators applied to async functions."""
        src = """
laao asyncio

kaam my_dec(f):
    asamanantar kaam wrapper(*args, **kwargs):
        res = intezaar f(*args, **kwargs)
        wapas res * 2
    wapas wrapper

@my_dec
asamanantar kaam calc(n):
    wapas n + 5

ans = asyncio.run(calc(10))
"""
        ns = run(src)
        self.assertEqual(ns["ans"], 30)

    # -------------------------------------------------------------------------
    # 2. Advanced Function Parameters Tests
    # -------------------------------------------------------------------------

    def test_positional_only_parameters(self) -> None:
        """Verifies positional-only parameter syntax and enforcement."""
        src = """
kaam pos_func(a, b, /, c=10):
    wapas a + b + c

val = pos_func(1, 2, 3)
"""
        py = self._compile(src)
        self.assertIn("def pos_func(a, b, /, c=10):", py)
        ns = run(src)
        self.assertEqual(ns["val"], 6)

    def test_keyword_only_parameters(self) -> None:
        """Verifies bare * and keyword-only parameter enforcement."""
        src = """
kaam kw_func(a, *, key1, key2=100):
    wapas a + key1 + key2

val = kw_func(5, key1=20)
"""
        py = self._compile(src)
        self.assertIn("def kw_func(a, *, key1, key2=100):", py)
        ns = run(src)
        self.assertEqual(ns["val"], 125)

    def test_full_complex_parameter_signature(self) -> None:
        """Verifies comprehensive signature mixing /, *, *args, **kwargs, defaults, and annotations."""
        src = """
kaam complex_func(p1: int, p2: int = 1, /, std: int = 2, *args: int, kw1: str, kw2: int = 10, **kwargs) -> tuple:
    wapas (p1, p2, std, args, kw1, kw2, kwargs)

res = complex_func(10, 20, 30, 40, 50, kw1="hello", kw2=99, extra="custom")
"""
        ns = run(src)
        self.assertEqual(
            ns["res"],
            (10, 20, 30, (40, 50), "hello", 99, {"extra": "custom"}),
        )

    def test_parameter_order_syntax_errors(self) -> None:
        """Verifies syntax errors when parameter order is invalid."""
        # Non-default after default in positional
        with self.assertRaises(HinglishSyntaxError):
            parse("kaam f(a=1, b): pass")

        # Multiple '/'
        with self.assertRaises(HinglishSyntaxError):
            parse("kaam f(a, /, b, /): pass")

        # Parameter after **kwargs
        with self.assertRaises(HinglishSyntaxError):
            parse("kaam f(**kwargs, a): pass")

    # -------------------------------------------------------------------------
    # 3. Type Annotations Tests
    # -------------------------------------------------------------------------

    def test_variable_and_function_annotations(self) -> None:
        """Verifies variable and function type annotations and AST nodes."""
        src = """
x: int = 100
uninit: str

kaam multiply(a: float, b: float) -> float:
    wapas a * b
"""
        tree = parse(src)
        self.assertIsInstance(tree.body[0], AnnAssign)
        self.assertIsInstance(tree.body[1], AnnAssign)
        func_node = tree.body[2]
        self.assertIsInstance(func_node, FunctionDefinition)
        self.assertIsNotNone(func_node.returns)

        py = self.compiler.compile(tree)
        self.assertIn("x: int = 100", py)
        self.assertIn("uninit: str", py)
        self.assertIn("def multiply(a: float, b: float) -> float:", py)

        ns = run(src)
        self.assertEqual(ns["x"], 100)
        self.assertIn("return", ns["multiply"].__annotations__)

    # -------------------------------------------------------------------------
    # 4. Walrus Operator (:=) Tests
    # -------------------------------------------------------------------------

    def test_walrus_operator_expressions(self) -> None:
        """Verifies assignment expression (:=) parsing, compilation, and evaluation."""
        src = """
data = [10, 20, 30, 40, 50]
agar (n := lambai(data)) > 3:
    dikhao(f"length is {n}")

# In loop condition
i = 0
squares = []
jabtak (i := i + 1) <= 3:
    squares.append(i * i)
"""
        tree = parse(src)
        py = self.compiler.compile(tree)
        self.assertIn("(n := len(data))", py)
        self.assertIn("(i := i + 1)", py)

        ns = run(src)
        self.assertEqual(ns["n"], 5)
        self.assertEqual(ns["squares"], [1, 4, 9])

    # -------------------------------------------------------------------------
    # 5. Advanced Unpacking Tests
    # -------------------------------------------------------------------------

    def test_tuple_and_extended_unpacking_targets(self) -> None:
        """Verifies tuple target unpacking including extended *rest assignment."""
        src = """
# Basic multi-target
a, b = 10, 20

# Extended unpacking with middle star
first, *mid, last = [1, 2, 3, 4, 5]

# Leading star
*head, tail = (100, 200, 300)
"""
        ns = run(src)
        self.assertEqual(ns["a"], 10)
        self.assertEqual(ns["b"], 20)
        self.assertEqual(ns["first"], 1)
        self.assertEqual(ns["mid"], [2, 3, 4])
        self.assertEqual(ns["last"], 5)
        self.assertEqual(ns["head"], [100, 200])
        self.assertEqual(ns["tail"], 300)

    def test_literal_and_call_unpacking(self) -> None:
        """Verifies * and ** unpacking in list, dict, and function call arguments."""
        src = """
# List literal unpacking
base_l = [2, 3]
full_l = [1, *base_l, 4]

# Dict literal unpacking
d1 = {"a": 1, "b": 2}
merged_d = {**d1, "b": 20, **{"c": 30}}

# Function call unpacking
kaam sum_three(x, y, z):
    wapas x + y + z

args = [10, 20]
kwargs = {"z": 30}
ans = sum_three(*args, **kwargs)
"""
        ns = run(src)
        self.assertEqual(ns["full_l"], [1, 2, 3, 4])
        self.assertEqual(ns["merged_d"], {"a": 1, "b": 20, "c": 30})
        self.assertEqual(ns["ans"], 60)

    # -------------------------------------------------------------------------
    # 6. Structural Pattern Matching Tests (milaao / vichaar)
    # -------------------------------------------------------------------------

    def test_pattern_matching_literals_and_wildcard(self) -> None:
        """Verifies literal value patterns and wildcard '_' in milaao / vichaar."""
        src = """
kaam match_val(v):
    milaao v:
        vichaar 1:
            wapas "one"
        vichaar "two":
            wapas "two_str"
        vichaar _:
            wapas "default"

r1 = match_val(1)
r2 = match_val("two")
r3 = match_val(99)
"""
        tree = parse(src)
        self.assertIsInstance(tree.body[0].body[0], Match)

        ns = run(src)
        self.assertEqual(ns["r1"], "one")
        self.assertEqual(ns["r2"], "two_str")
        self.assertEqual(ns["r3"], "default")

    def test_pattern_matching_singletons_and_or(self) -> None:
        """Verifies singleton patterns (sahi, galat, shunya) and alternatives (|)."""
        src = """
kaam match_bool_or(v):
    milaao v:
        vichaar sahi:
            wapas "true_branch"
        vichaar galat:
            wapas "false_branch"
        vichaar shunya:
            wapas "none_branch"
        vichaar 401 | 403 | 404:
            wapas "http_error"
        vichaar _:
            wapas "other"

t_res = match_bool_or(sahi)
f_res = match_bool_or(galat)
n_res = match_bool_or(shunya)
e_res = match_bool_or(404)
"""
        ns = run(src)
        self.assertEqual(ns["t_res"], "true_branch")
        self.assertEqual(ns["f_res"], "false_branch")
        self.assertEqual(ns["n_res"], "none_branch")
        self.assertEqual(ns["e_res"], "http_error")

    def test_pattern_matching_sequences_and_guards(self) -> None:
        """Verifies sequence patterns with star and guard conditions (agar)."""
        src = """
kaam match_seq(lst):
    milaao lst:
        vichaar [x, y] agar x == y:
            wapas f"equal_{x}"
        vichaar [head, *tail]:
            wapas f"head_{head}_len_{lambai(tail)}"
        vichaar _:
            wapas "other"

res1 = match_seq([7, 7])
res2 = match_seq([10, 20, 30, 40])
res3 = match_seq([])
"""
        ns = run(src)
        self.assertEqual(ns["res1"], "equal_7")
        self.assertEqual(ns["res2"], "head_10_len_3")
        self.assertEqual(ns["res3"], "other")

    def test_pattern_matching_mappings(self) -> None:
        """Verifies mapping patterns with keys and **rest."""
        src = """
kaam match_map(m):
    milaao m:
        vichaar {"status": 200, "data": d}:
            wapas f"ok_{d}"
        vichaar {"status": code, **rest}:
            wapas f"err_{code}"
        vichaar _:
            wapas "unknown"

res1 = match_map({"status": 200, "data": "payload"})
res2 = match_map({"status": 500, "extra": "db_fail"})
"""
        ns = run(src)
        self.assertEqual(ns["res1"], "ok_payload")
        self.assertEqual(ns["res2"], "err_500")

    def test_pattern_matching_class_and_as_capture(self) -> None:
        """Verifies class patterns and 'jaise' pattern captures."""
        src = """
varg Point:
    __match_args__ = ("x", "y")
    kaam __init__(self, x, y):
        self.x = x
        self.y = y

kaam match_point(p):
    milaao p:
        vichaar Point(0, 0):
            wapas "origin"
        vichaar Point(x, y) jaise pt agar x == y:
            wapas f"diagonal_{pt.x}"
        vichaar Point(x, y):
            wapas f"point_{x}_{y}"
        vichaar _:
            wapas "not_a_point"

p_orig = match_point(Point(0, 0))
p_diag = match_point(Point(4, 4))
p_arb = match_point(Point(1, 9))
"""
        ns = run(src)
        self.assertEqual(ns["p_orig"], "origin")
        self.assertEqual(ns["p_diag"], "diagonal_4")
        self.assertEqual(ns["p_arb"], "point_1_9")

    # -------------------------------------------------------------------------
    # 7. Canonical Examples Test
    # -------------------------------------------------------------------------

    def test_run_canonical_examples(self) -> None:
        """Executes all 5 Step 8 canonical example files from disk."""
        examples_dir = Path(__file__).parent.parent / "examples"
        expected_files = [
            "async.hin",
            "advanced_functions.hin",
            "match_case.hin",
            "annotations.hin",
            "unpacking.hin",
        ]
        for filename in expected_files:
            file_path = examples_dir / filename
            self.assertTrue(file_path.is_file(), f"Missing example file: {filename}")
            ns = run_file(file_path)
            self.assertIsNotNone(ns)


if __name__ == "__main__":
    unittest.main()
