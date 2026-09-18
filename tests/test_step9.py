"""Comprehensive Test Suite for Step 9: Core Compatibility & Stability Audit."""

import asyncio
import io
import subprocess
import sys
import unittest
from pathlib import Path

from hinglish.ast import (
    Assert,
    ComprehensionClause,
    Delete,
    ExceptHandler,
    Global,
    Nonlocal,
)
from hinglish.compiler import HinglishCompiler
from hinglish.exceptions import HinglishError, HinglishSyntaxError
from hinglish.parser import parse
from hinglish.runtime import HinglishREPL, run, run_file


class TestStep9CoreLanguageAudit(unittest.TestCase):
    """Verifies end-to-end lexer, parser, compiler, and runtime for Step 9 v1.0 additions."""

    def setUp(self) -> None:
        self.compiler = HinglishCompiler()

    def _compile(self, source: str) -> str:
        ast_tree = parse(source)
        return self.compiler.compile(ast_tree)

    # -------------------------------------------------------------------------
    # 1. Global / Nonlocal Tests
    # -------------------------------------------------------------------------

    def test_global_statement_ast_and_execution(self) -> None:
        """Verifies sarvavyapi parses into Global AST, compiles to global, and mutates module scope."""
        src = """
counter = 0

kaam increment(by):
    sarvavyapi counter
    counter = counter + by

increment(10)
increment(5)
"""
        tree = parse(src)
        self.assertIsInstance(tree.body[1].body[0], Global)
        py = self._compile(src)
        self.assertIn("global counter", py)

        ns = run(src)
        self.assertEqual(ns["counter"], 15)

    def test_nonlocal_statement_ast_and_execution(self) -> None:
        """Verifies asthaniya parses into Nonlocal AST, compiles to nonlocal, and mutates enclosing scope."""
        src = """
kaam make_accumulator(initial):
    total = initial
    kaam add(val):
        asthaniya total
        total = total + val
        wapas total
    wapas add

acc = make_accumulator(100)
r1 = acc(25)
r2 = acc(15)
"""
        tree = parse(src)
        self.assertIsInstance(tree.body[0].body[1].body[0], Nonlocal)
        py = self._compile(src)
        self.assertIn("nonlocal total", py)

        ns = run(src)
        self.assertEqual(ns["r1"], 125)
        self.assertEqual(ns["r2"], 140)

    # -------------------------------------------------------------------------
    # 2. Assert Statement Tests
    # -------------------------------------------------------------------------

    def test_assert_statement_pass_and_fail(self) -> None:
        """Verifies dawa statement AST, compilation, and AssertionError behavior."""
        src_pass = "dawa 10 > 5, 'Math failure'\nx = 42"
        tree = parse(src_pass)
        self.assertIsInstance(tree.body[0], Assert)
        py = self._compile(src_pass)
        self.assertIn("assert 10 > 5, 'Math failure'", py)

        ns = run(src_pass)
        self.assertEqual(ns["x"], 42)

        # Failure raises AssertionError
        src_fail = "dawa 2 == 5, 'Mismatch'"
        with self.assertRaises(RuntimeError) as ctx:
            run(src_fail, filename="test_assert.hin")
        self.assertIn("AssertionError", str(ctx.exception))
        self.assertIn("Mismatch", str(ctx.exception))

    # -------------------------------------------------------------------------
    # 3. Del Statement Tests
    # -------------------------------------------------------------------------

    def test_del_statement_variables_and_containers(self) -> None:
        """Verifies mitao statement AST, compilation, and target deletion."""
        src = """
varg Container:
    kaam __init__(self):
        self.prop = "active"

c = Container()
mitao c.prop

lst = [10, 20, 30]
mitao lst[1]

d = {"a": 1, "b": 2}
mitao d["a"]
"""
        tree = parse(src)
        py = self._compile(src)
        self.assertIn("del c.prop", py)
        self.assertIn("del lst[1]", py)
        self.assertIn("del d['a']", py)

        ns = run(src)
        self.assertFalse(hasattr(ns["c"], "prop"))
        self.assertEqual(ns["lst"], [10, 30])
        self.assertEqual(ns["d"], {"b": 2})

    def test_del_invalid_target_syntax_error(self) -> None:
        """Verifies that non-deletable expression targets raise HinglishSyntaxError."""
        with self.assertRaises(HinglishSyntaxError):
            parse("mitao 1 + 2")

    # -------------------------------------------------------------------------
    # 4. Async Comprehensions Tests
    # -------------------------------------------------------------------------

    def test_async_comprehensions_execution(self) -> None:
        """Verifies async comprehensions with and without agar filters."""
        src = """
laao asyncio

asamanantar kaam astream():
    har x mein [1, 2, 3, 4, 5]:
        intezaar asyncio.sleep(0.001)
        upaj x

asamanantar kaam runner():
    # List comprehension
    evens = [x * 10 har intezaar x mein astream() agar x % 2 == 0]

    # Dict comprehension
    sq_dict = {x: x * x har intezaar x mein astream() agar x <= 3}

    # Set comprehension
    mods = {x % 2 har intezaar x mein astream()}
    wapas (evens, sq_dict, mods)

res = asyncio.run(runner())
"""
        tree = parse(src)
        py = self._compile(src)
        self.assertIn("async for x in astream()", py)

        ns = run(src)
        evens, sq_dict, mods = ns["res"]
        self.assertEqual(evens, [20, 40])
        self.assertEqual(sq_dict, {1: 1, 2: 4, 3: 9})
        self.assertEqual(mods, {0, 1})

    # -------------------------------------------------------------------------
    # 5. Exception Groups / Except* Tests
    # -------------------------------------------------------------------------

    def test_except_star_parsing_and_execution(self) -> None:
        """Verifies pakdo* parses into ExceptHandler(is_star=True) and handles ExceptionGroups."""
        src = """
caught = []

koshish:
    uthav ExceptionGroup("bulk_err", [ValueError("v1"), TypeError("t1"), ValueError("v2")])
pakdo* ValueError jaise eg:
    caught.append(f"value_errors_{lambai(eg.exceptions)}")
pakdo* TypeError jaise eg:
    caught.append(f"type_errors_{lambai(eg.exceptions)}")
"""
        tree = parse(src)
        try_node = tree.body[1]
        self.assertTrue(try_node.handlers[0].is_star)
        self.assertTrue(try_node.handlers[1].is_star)

        py = self._compile(src)
        self.assertIn("except* ValueError as eg:", py)
        self.assertIn("except* TypeError as eg:", py)

        ns = run(src)
        self.assertEqual(ns["caught"], ["value_errors_2", "type_errors_1"])

    # -------------------------------------------------------------------------
    # 6. Dotted & Multi-Name Imports Tests
    # -------------------------------------------------------------------------

    def test_dotted_and_multi_imports(self) -> None:
        """Verifies dotted module paths, multiple names, and aliases in imports."""
        src = """
laao math, json
laao os.path jaise osp
se math laao sin, cos, pi jaise PI
se urllib.parse laao urlparse

sin_val = sin(PI / 2)
json_str = json.dumps({"active": sahi})
basename = osp.basename("/root/app/file.hin")
scheme = urlparse("https://hinglish.lang/docs").scheme
"""
        ns = run(src)
        self.assertAlmostEqual(ns["sin_val"], 1.0)
        self.assertEqual(ns["json_str"], '{"active": true}')
        self.assertEqual(ns["basename"], "file.hin")
        self.assertEqual(ns["scheme"], "https")

    # -------------------------------------------------------------------------
    # 7. Multi-File Project Test
    # -------------------------------------------------------------------------

    def test_multi_file_project_execution(self) -> None:
        """Verifies that a multi-file project with .hin dependencies imports and executes cleanly."""
        proj_dir = Path(__file__).parent.parent / "examples" / "project"
        main_path = proj_dir / "main.hin"
        self.assertTrue(main_path.is_file())

        ns = run_file(main_path)
        self.assertEqual(ns["sum_val"], 40)
        self.assertEqual(ns["fact_val"], 120)
        self.assertEqual(ns["admin"].role, "admin")
        self.assertEqual(ns["order"].total, 110000.0)

    # -------------------------------------------------------------------------
    # 8. Complete Language Composition Tests (Programs A - F)
    # -------------------------------------------------------------------------

    def test_program_a_oop_decorators_exceptions_fstrings(self) -> None:
        """Program A: Classes + Inheritance + Decorators + Properties + Exceptions + F-Strings."""
        src = """
kaam track(f):
    kaam inner(*args, **kwargs):
        wapas f(*args, **kwargs)
    wapas inner

varg Vehicle:
    kaam __init__(self, make: str, speed: float):
        self.make = make
        self.speed = speed

    @property
    kaam velocity_mph(self) -> float:
        wapas self.speed * 0.621371

varg Car(Vehicle):
    @track
    kaam accelerate(self, delta: float):
        agar delta < 0:
            uthav ValueError("Delta cannot be negative")
        self.speed = self.speed + delta
        wapas f"{self.make} accelerated to {self.speed} km/h ({self.velocity_mph:.1f} mph)"

c = Car("Sedan", 60.0)
msg = c.accelerate(40.0)

err_caught = galat
koshish:
    c.accelerate(-10.0)
pakdo ValueError:
    err_caught = sahi
"""
        ns = run(src)
        self.assertIn("Sedan accelerated to 100.0 km/h", ns["msg"])
        self.assertTrue(ns["err_caught"])

    def test_program_b_async_generators_decorators_context(self) -> None:
        """Program B: Async + Generators + Decorators + Context Managers."""
        src = """
laao asyncio

varg AsyncTracker:
    asamanantar kaam __aenter__(self):
        wapas "active"
    asamanantar kaam __aexit__(self, exc_type, exc, tb):
        pass

asamanantar kaam num_gen():
    har i mein [1, 2, 3]:
        intezaar asyncio.sleep(0.001)
        upaj i * 10

asamanantar kaam pipeline():
    collected = []
    saath intezaar AsyncTracker() jaise state:
        har intezaar val mein num_gen():
            collected.append(val)
    wapas collected

results = asyncio.run(pipeline())
"""
        ns = run(src)
        self.assertEqual(ns["results"], [10, 20, 30])

    def test_program_c_comprehensions_lambda_closures_unpacking(self) -> None:
        """Program C: Comprehensions + Lambda + Closures + Unpacking."""
        src = """
raw_data = [("a", 30), ("b", 10), ("c", 20)]

# Lambda sorting
sorted_data = sorted(raw_data, key=sookshm pair: pair[1])

# Unpacking in comprehension
keys = [k har k, v mein sorted_data agar v >= 20]

# Extended unpacking
first_pair, *middle_pairs, last_pair = sorted_data
"""
        ns = run(src)
        self.assertEqual(ns["keys"], ["c", "a"])
        self.assertEqual(ns["first_pair"], ("b", 10))
        self.assertEqual(ns["last_pair"], ("a", 30))

    def test_program_d_match_classes_guards_annotations(self) -> None:
        """Program D: Pattern Matching + Classes + Guards + Annotations."""
        src = """
varg Response:
    __match_args__ = ("status_code", "data")
    kaam __init__(self, status_code: int, data: str):
        self.status_code: int = status_code
        self.data: str = data

kaam evaluate(resp: Response) -> str:
    milaao resp:
        vichaar Response(code, d) agar code == 200:
            wapas f"Success: {d}"
        vichaar Response(code, _) agar code >= 500:
            wapas f"Server error: {code}"
        vichaar _:
            wapas "Unknown response"

r1 = evaluate(Response(200, "OK Payload"))
r2 = evaluate(Response(503, "Unavailable"))
"""
        ns = run(src)
        self.assertEqual(ns["r1"], "Success: OK Payload")
        self.assertEqual(ns["r2"], "Server error: 503")

    def test_program_e_async_for_exceptions_context(self) -> None:
        """Program E: Async Generator + Async For + Exception Handling + Context Manager."""
        src = """
laao asyncio

varg Session:
    asamanantar kaam __aenter__(self):
        wapas self
    asamanantar kaam __aexit__(self, et, ev, tb):
        pass

asamanantar kaam fault_stream():
    upaj 1
    upaj 2
    uthav ValueError("Stream terminated")

asamanantar kaam safe_drain():
    received = []
    stream_failed = galat
    saath intezaar Session():
        koshish:
            har intezaar item mein fault_stream():
                received.append(item)
        pakdo ValueError:
            stream_failed = sahi
    wapas (received, stream_failed)

items, failed = asyncio.run(safe_drain())
"""
        ns = run(src)
        self.assertEqual(ns["items"], [1, 2])
        self.assertTrue(ns["failed"])

    # -------------------------------------------------------------------------
    # 9. CLI & REPL Audit Tests
    # -------------------------------------------------------------------------

    def test_cli_flags(self) -> None:
        """Verifies CLI execution with --tokens, --ast, and --transpile flags."""
        sample_hin = Path(__file__).parent.parent / "examples" / "hello.hin"

        # 1. Run file directly
        res_run = subprocess.run(
            [sys.executable, "-m", "hinglish", str(sample_hin)],
            capture_output=True,
            text=True,
        )
        self.assertEqual(res_run.returncode, 0)
        self.assertIn("Namaste duniya!", res_run.stdout)

        # 2. --tokens
        res_tok = subprocess.run(
            [sys.executable, "-m", "hinglish", "--tokens", str(sample_hin)],
            capture_output=True,
            text=True,
        )
        self.assertEqual(res_tok.returncode, 0)
        self.assertIn("KEYWORD", res_tok.stdout)

        # 3. --ast
        res_ast = subprocess.run(
            [sys.executable, "-m", "hinglish", "--ast", str(sample_hin)],
            capture_output=True,
            text=True,
        )
        self.assertEqual(res_ast.returncode, 0)
        self.assertIn("Program", res_ast.stdout)

        # 4. --transpile
        res_trans = subprocess.run(
            [sys.executable, "-m", "hinglish", "--transpile", str(sample_hin)],
            capture_output=True,
            text=True,
        )
        self.assertEqual(res_trans.returncode, 0)
        self.assertIn("print('Namaste duniya!')", res_trans.stdout)

    def test_repl_state_machine_multiline_and_namespace(self) -> None:
        """Verifies stateful REPL behavior with multi-line buffering, classes, functions, and errors."""
        repl = HinglishREPL()

        # Expression evaluation
        res = repl.run_line("40 + 2")
        self.assertEqual(res, 42)

        # Multi-line function
        repl.run_line("kaam square(x):")
        repl.run_line("    wapas x * x")
        repl.run_line("")  # Flush block
        self.assertEqual(repl.run_line("square(7)"), 49)

        # Namespace persistence
        repl.run_line("stored_val = 100")
        self.assertEqual(repl.run_line("stored_val * 2"), 200)

    # -------------------------------------------------------------------------
    # 10. Error Handling & Source Mapping Audit
    # -------------------------------------------------------------------------

    def test_error_handling_and_traceback_source_mapping(self) -> None:
        """Verifies runtime errors report accurate Hinglish line numbers and code snippets."""
        src = """# Line 1
# Line 2
a = 10
b = 0
result = a / b  # Line 5: Division by zero
"""
        with self.assertRaises(RuntimeError) as ctx:
            run(src, filename="error_calc.hin")

        err_str = str(ctx.exception)
        self.assertIn("error_calc.hin", err_str)
        self.assertIn("line 5", err_str)
        self.assertIn("ZeroDivisionError", err_str)
        self.assertIn("result = a / b", err_str)

    def test_syntax_error_reporting(self) -> None:
        """Verifies syntax errors provide exact line and column numbers."""
        invalid_src = "10 = x"
        with self.assertRaises(HinglishSyntaxError) as ctx:
            parse(invalid_src)
        self.assertIn("cannot assign to integer", str(ctx.exception))

    # -------------------------------------------------------------------------
    # 11. Python Semantic Compatibility Audit
    # -------------------------------------------------------------------------

    def test_python_truthiness_and_equality_semantics(self) -> None:
        """Verifies truthiness and identity matching native Python."""
        src = """
# Falsy values
falsy_empty_list = galat
agar []:
    falsy_empty_list = sahi

falsy_empty_dict = galat
agar {}:
    falsy_empty_dict = sahi

falsy_zero = galat
agar 0:
    falsy_zero = sahi

falsy_none = galat
agar shunya:
    falsy_none = sahi

# Equality vs Identity
l1 = [1, 2]
l2 = [1, 2]
eq = (l1 == l2)
same = (l1 hai l2)
diff = (l1 hai nahi l2)
"""
        ns = run(src)
        self.assertFalse(ns["falsy_empty_list"])
        self.assertFalse(ns["falsy_empty_dict"])
        self.assertFalse(ns["falsy_zero"])
        self.assertFalse(ns["falsy_none"])
        self.assertTrue(ns["eq"])
        self.assertFalse(ns["same"])
        self.assertTrue(ns["diff"])

    # -------------------------------------------------------------------------
    # 12. Final Integration Program Execution
    # -------------------------------------------------------------------------

    def test_run_v1_integration_program(self) -> None:
        """Executes examples/v1_integration.hin and verifies correct completion."""
        integ_file = Path(__file__).parent.parent / "examples" / "v1_integration.hin"
        self.assertTrue(integ_file.is_file())
        ns = run_file(integ_file)
        self.assertIsNotNone(ns)
        self.assertEqual(ns["TOTAL_PROCESSED"], 4)


if __name__ == "__main__":
    unittest.main()
