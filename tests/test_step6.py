"""Comprehensive Test Suite for Step 6: OOP, Exception Handling, Context Managers, and F-Strings."""

import io
import math
import sys
import tempfile
import unittest
from pathlib import Path

from hinglish.ast import (
    ClassDefinition,
    ExceptHandler,
    FormattedValue,
    FunctionCall,
    FunctionDefinition,
    Identifier,
    JoinedStr,
    Raise,
    String,
    Try,
    With,
    WithItem,
)
from hinglish.compiler import HinglishCompiler
from hinglish.exceptions import HinglishSyntaxError
from hinglish.parser import parse
from hinglish.runtime import run, run_file


class TestStep6LanguageFeatures(unittest.TestCase):
    """Verifies end-to-end lexer, parser, compiler, and runtime for Step 6 additions."""

    def setUp(self) -> None:
        self.compiler = HinglishCompiler()

    def _compile(self, source: str) -> str:
        """Helper to parse and compile Hinglish source to Python."""
        ast_tree = parse(source)
        return self.compiler.compile(ast_tree)

    # -------------------------------------------------------------------------
    # A. Object-Oriented Programming (OOP) Tests
    # -------------------------------------------------------------------------

    def test_oop_simple_class(self) -> None:
        """1. Simple class definition without constructor."""
        src = """
varg Counter:
    count = 100
"""
        ast_tree = parse(src)
        self.assertIsInstance(ast_tree.body[0], ClassDefinition)
        self.assertEqual(ast_tree.body[0].name, "Counter")

        py_code = self.compiler.compile(ast_tree)
        self.assertIn("class Counter:", py_code)

        ns = run(src)
        self.assertEqual(ns["Counter"].count, 100)

    def test_oop_constructor_and_instance_attributes(self) -> None:
        """2 & 3. Class constructor __init__ and instance attributes."""
        src = """
varg Point:
    kaam __init__(self, x, y):
        self.x = x
        self.y = y

p = Point(10, 20)
res_x = p.x
res_y = p.y
"""
        ns = run(src)
        self.assertEqual(ns["res_x"], 10)
        self.assertEqual(ns["res_y"], 20)

    def test_oop_instance_methods(self) -> None:
        """4. Class instance methods calling other methods and accessing self."""
        src = """
varg Calculator:
    kaam __init__(self, base):
        self.base = base

    kaam add(self, n):
        wapas self.base + n

    kaam multiply(self, n):
        wapas self.base * n

calc = Calculator(5)
sum_val = calc.add(10)
prod_val = calc.multiply(4)
"""
        ns = run(src)
        self.assertEqual(ns["sum_val"], 15)
        self.assertEqual(ns["prod_val"], 20)

    def test_oop_inheritance_and_method_override(self) -> None:
        """5 & 6. Inheritance, subclassing, and method overriding."""
        src = """
varg Animal:
    kaam speak(self):
        wapas "Generic sound"

varg Dog(Animal):
    kaam speak(self):
        wapas "Bark"

varg Cat(Animal):
    chhod_do

d = Dog()
c = Cat()
dog_sound = d.speak()
cat_sound = c.speak()
is_dog_animal = isinstance(d, Animal)
is_cat_animal = isinstance(c, Animal)
"""
        ns = run(src)
        self.assertEqual(ns["dog_sound"], "Bark")
        self.assertEqual(ns["cat_sound"], "Generic sound")
        self.assertTrue(ns["is_dog_animal"])
        self.assertTrue(ns["is_cat_animal"])

    def test_oop_multiple_inheritance(self) -> None:
        """Structural support for multiple inheritance."""
        src = """
varg A:
    kaam f_a(self):
        wapas "A"

varg B:
    kaam f_b(self):
        wapas "B"

varg C(A, B):
    chhod_do

obj = C()
res_a = obj.f_a()
res_b = obj.f_b()
"""
        ns = run(src)
        self.assertEqual(ns["res_a"], "A")
        self.assertEqual(ns["res_b"], "B")

    def test_oop_multiple_instances(self) -> None:
        """7. Multiple distinct instances with independent attribute state."""
        src = """
varg Person:
    kaam __init__(self, name):
        self.name = name

p1 = Person("Alice")
p2 = Person("Bob")
name1 = p1.name
name2 = p2.name
"""
        ns = run(src)
        self.assertEqual(ns["name1"], "Alice")
        self.assertEqual(ns["name2"], "Bob")

    def test_oop_interaction_with_python_objects(self) -> None:
        """8. Class interaction with standard Python objects and modules."""
        src = """
laao math

varg Circle:
    kaam __init__(self, r):
        self.r = r

    kaam area(self):
        wapas math.pi * (self.r ** 2)

c = Circle(7)
area_val = c.area()
"""
        ns = run(src)
        self.assertAlmostEqual(ns["area_val"], math.pi * 49, places=5)

    # -------------------------------------------------------------------------
    # B. Exception Handling Tests
    # -------------------------------------------------------------------------

    def test_exception_try_except_bare(self) -> None:
        """1. Bare try/except block (koshish / pakdo)."""
        src = """
caught = galat
koshish:
    x = 1 / 0
pakdo:
    caught = sahi
"""
        ns = run(src)
        self.assertTrue(ns["caught"])

    def test_exception_specific_and_as_variable(self) -> None:
        """2 & 4. Specific exception class and jaise variable binding."""
        src = """
error_msg = ""
koshish:
    s = purnank("not_a_number")
pakdo ValueError jaise err:
    error_msg = str(err)
"""
        ns = run(src)
        self.assertIn("invalid literal for int", ns["error_msg"])

    def test_exception_multiple_clauses(self) -> None:
        """3. Multiple pakdo clauses."""
        src = """
caught_clause = ""
koshish:
    x = 1 / 0
pakdo ValueError:
    caught_clause = "value"
pakdo ZeroDivisionError:
    caught_clause = "zero"
pakdo:
    caught_clause = "other"
"""
        ns = run(src)
        self.assertEqual(ns["caught_clause"], "zero")

    def test_exception_finally_block(self) -> None:
        """5. Finally block (antatah) executed whether exception occurs or not."""
        src = """
fin_ran1 = galat
koshish:
    x = 10
antatah:
    fin_ran1 = sahi

fin_ran2 = galat
koshish:
    y = 1 / 0
pakdo ZeroDivisionError:
    chhod_do
antatah:
    fin_ran2 = sahi
"""
        ns = run(src)
        self.assertTrue(ns["fin_ran1"])
        self.assertTrue(ns["fin_ran2"])

    def test_exception_raise_and_bare_raise(self) -> None:
        """6. Raise with exception expression (uthav) and bare raise in except."""
        src = """
caught_custom = ""
koshish:
    uthav RuntimeError("Mera error")
pakdo RuntimeError jaise e:
    caught_custom = str(e)
"""
        ns = run(src)
        self.assertEqual(ns["caught_custom"], "Mera error")

        # Bare raise test inside try/except
        src_bare = """
re_caught = galat
koshish:
    koshish:
        uthav KeyError("k")
    pakdo KeyError:
        uthav
pakdo KeyError:
    re_caught = sahi
"""
        ns2 = run(src_bare)
        self.assertTrue(ns2["re_caught"])

    def test_exception_nested_blocks(self) -> None:
        """7. Nested try/except blocks."""
        src = """
outer_caught = galat
inner_caught = galat

koshish:
    koshish:
        uthav ValueError("inner")
    pakdo ValueError:
        inner_caught = sahi
        uthav TypeError("outer")
pakdo TypeError:
    outer_caught = sahi
"""
        ns = run(src)
        self.assertTrue(ns["inner_caught"])
        self.assertTrue(ns["outer_caught"])

    def test_exception_traceback_source_mapping_in_class(self) -> None:
        """8. Runtime traceback mapping reporting exact .hin line inside class method."""
        src = """varg Test:
    kaam run(self):
        x = 10 / 0

t = Test()
t.run()
"""
        with self.assertRaises(RuntimeError) as ctx:
            run(src, filename="my_class.hin")

        err_text = str(ctx.exception)
        self.assertIn("my_class.hin", err_text)
        self.assertIn("line 3", err_text)
        self.assertIn("x = 10 / 0", err_text)
        self.assertIn("ZeroDivisionError", err_text)

    # -------------------------------------------------------------------------
    # C. Context Managers Tests
    # -------------------------------------------------------------------------

    def test_context_manager_basic_with(self) -> None:
        """1. Basic with statement without variable binding."""
        src = """
varg CustomManager:
    kaam __init__(self):
        self.entered = galat
        self.exited = galat

    kaam __enter__(self):
        self.entered = sahi
        wapas self

    kaam __exit__(self, exc_type, exc_val, exc_tb):
        self.exited = sahi
        wapas galat

cm = CustomManager()
saath cm:
    in_block = cm.entered
"""
        ns = run(src)
        self.assertTrue(ns["in_block"])
        self.assertTrue(ns["cm"].entered)
        self.assertTrue(ns["cm"].exited)

    def test_context_manager_with_as(self) -> None:
        """2. With statement with jaise target variable binding."""
        src = """
varg Resource:
    kaam __enter__(self):
        wapas "ActiveResource"

    kaam __exit__(self, exc_type, exc_val, exc_tb):
        wapas galat

captured = ""
saath Resource() jaise r:
    captured = r
"""
        ns = run(src)
        self.assertEqual(ns["captured"], "ActiveResource")

    def test_context_manager_multiple_managers_and_khol(self) -> None:
        """3. Multiple context managers with khol builtin."""
        with tempfile.NamedTemporaryFile("w+", delete=False) as f1, tempfile.NamedTemporaryFile("w+", delete=False) as f2:
            f1.write("Alpha")
            f2.write("Beta")
            p1, p2 = f1.name, f2.name

        try:
            src = f"""
c1 = ""
c2 = ""
saath khol("{p1}", "r") jaise file1, khol("{p2}", "r") jaise file2:
    c1 = file1.read()
    c2 = file2.read()
"""
            ns = run(src)
            self.assertEqual(ns["c1"], "Alpha")
            self.assertEqual(ns["c2"], "Beta")
        finally:
            Path(p1).unlink(missing_ok=True)
            Path(p2).unlink(missing_ok=True)

    # -------------------------------------------------------------------------
    # D. F-Strings & String Interpolation Tests
    # -------------------------------------------------------------------------

    def test_fstring_ast_structure(self) -> None:
        """F-string AST is parsed into JoinedStr and FormattedValue nodes."""
        src = 'dikhao(f"Naam: {naam}, Umr: {umr}")'
        ast_tree = parse(src)
        call_node = ast_tree.body[0].expr
        self.assertIsInstance(call_node, FunctionCall)
        fstring_node = call_node.args[0]
        self.assertIsInstance(fstring_node, JoinedStr)
        self.assertEqual(len(fstring_node.parts), 4)
        self.assertIsInstance(fstring_node.parts[0], String)
        self.assertEqual(fstring_node.parts[0].value, "Naam: ")
        self.assertIsInstance(fstring_node.parts[1], FormattedValue)
        self.assertEqual(fstring_node.parts[1].value.name, "naam")
        self.assertIsInstance(fstring_node.parts[2], String)
        self.assertEqual(fstring_node.parts[2].value, ", Umr: ")
        self.assertIsInstance(fstring_node.parts[3], FormattedValue)
        self.assertEqual(fstring_node.parts[3].value.name, "umr")

    def test_fstring_single_and_multiple_interpolation(self) -> None:
        """1 & 2. Single and multiple interpolations."""
        src = """
a = "Hello"
b = "World"
res1 = f"{a}"
res2 = f"{a} {b}!"
"""
        ns = run(src)
        self.assertEqual(ns["res1"], "Hello")
        self.assertEqual(ns["res2"], "Hello World!")

    def test_fstring_expression_interpolation(self) -> None:
        """3. Arithmetic and complex expression evaluation inside f-string."""
        src = """
x = 10
y = 20
res = f"Total: {x + y * 2}"
"""
        ns = run(src)
        self.assertEqual(ns["res"], "Total: 50")

    def test_fstring_escaped_braces(self) -> None:
        """4. Escaped curly braces {{ and }} produce literal { and }."""
        src = """
name = "Hinglish"
res = f"Escaped {{braces}} with {name}"
"""
        ns = run(src)
        self.assertEqual(ns["res"], "Escaped {braces} with Hinglish")

    def test_fstring_formatting_and_conversion_features(self) -> None:
        """5. Format specifiers (:.2f) and conversions (!r)."""
        src = """
val = 3.14159
tag = "test"
res_spec = f"Val: {val:.2f}"
res_conv = f"Tag: {tag!r}"
"""
        ns = run(src)
        self.assertEqual(ns["res_spec"], "Val: 3.14")
        self.assertEqual(ns["res_conv"], "Tag: 'test'")

    def test_fstring_syntax_errors(self) -> None:
        """Invalid f-strings raise HinglishSyntaxError."""
        with self.assertRaises(HinglishSyntaxError):
            parse('f"unclosed {x"')

        with self.assertRaises(HinglishSyntaxError):
            parse('f"single } closing"')

        with self.assertRaises(HinglishSyntaxError):
            parse('f"empty {}"')

    # -------------------------------------------------------------------------
    # E. Canonical Example Files Execution
    # -------------------------------------------------------------------------

    def test_run_canonical_examples(self) -> None:
        """Executes all 4 Step 6 canonical example files from disk."""
        examples_dir = Path(__file__).resolve().parent.parent / "examples"

        for hin_file in ["classes.hin", "exceptions.hin", "context_managers.hin", "fstrings.hin"]:
            path = examples_dir / hin_file
            self.assertTrue(path.exists(), f"Example file missing: {path}")

            old_stdout = sys.stdout
            sys.stdout = io.StringIO()
            try:
                ns = run_file(path)
                output = sys.stdout.getvalue()
                self.assertIsNotNone(ns)
                self.assertGreater(len(output), 0)
            finally:
                sys.stdout = old_stdout

        # Clean up any file created by context_managers.hin
        sample_path = Path("sample_output.txt")
        if sample_path.exists():
            sample_path.unlink()


if __name__ == "__main__":
    unittest.main()
