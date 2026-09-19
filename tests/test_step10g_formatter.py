"""Comprehensive Test Suite for Step 10G — Hinglish Formatter & Code Quality Tooling.

Verifies:
1. Basic formatting (assignments, arithmetic, calls, whitespace)
2. Indentation (nested blocks, loops, functions, classes)
3. Expressions (precedence, calls, indexing, attributes, comprehensions)
4. Functions (defaults, pos-only /, bare *, *args, **kwargs, decorators, lambda)
5. OOP (classes, inheritance, methods, class attributes)
6. Exceptions (try/except/finally, raise, assert)
7. Generators (yield, yield from)
8. Async (async functions, await, async for, async with)
9. Pattern matching (match, case, guards, captures)
10. Imports (laao, se ... laao, aliases, relative)
11. Strings (single, double, triple-quoted, f-strings, escapes)
12. Comments (inline comments, standalone comments, header/footer)
13. Idempotence (format(format(source)) == format(source))
14. Semantic preservation (parse(format(source)) is semantically equivalent to parse(source))
15. CLI formatting (in-place, --check, -o, stdin)
16. LSP (textDocument/formatting JSON-RPC request & response)
17. VS Code extension metadata (contributions and package.json)
"""

import io
import json
import subprocess
import tempfile
import unittest
from pathlib import Path

from hinglish.compiler import compile as compile_hinglish
from hinglish.formatter import HinglishFormatter, format_file, format_source
from hinglish.lsp.protocol import read_message, write_message
from hinglish.lsp.server import HinglishLanguageServer
from hinglish.parser import parse


class TestStep10GFormatter(unittest.TestCase):
    """Unit and integration tests for the Hinglish source formatter."""

    def _assert_idempotent_and_semantic(self, source: str) -> str:
        """Helper to format source, verify byte-for-byte idempotence, and verify semantic preservation."""
        formatted = format_source(source)
        formatted_again = format_source(formatted)
        self.assertEqual(
            formatted,
            formatted_again,
            f"Idempotence check failed!\nFirst:\n{formatted}\nSecond:\n{formatted_again}",
        )

        # Semantic preservation: both should compile to identical or semantically equivalent Python
        py_orig = compile_hinglish(source)
        py_formatted = compile_hinglish(formatted)
        # Strip trailing whitespaces and line markers for AST comparison
        self.assertEqual(
            [line.strip() for line in py_orig.splitlines() if line.strip()],
            [line.strip() for line in py_formatted.splitlines() if line.strip()],
            "Semantic preservation failed between original and formatted code!",
        )
        return formatted

    # -------------------------------------------------------------------------
    # 1. Basic Formatting & Whitespace
    # -------------------------------------------------------------------------

    def test_basic_assignments_and_arithmetic(self) -> None:
        src = "x=10+20*30\ny   =   40   -   5\nz+=1\n"
        expected = "x = 10 + 20 * 30\ny = 40 - 5\nz += 1\n"
        res = self._assert_idempotent_and_semantic(src)
        self.assertEqual(res, expected)

    def test_whitespace_normalization_around_operators(self) -> None:
        src = "a=b+c*d-e//f%g**h\nflag=x>10aur y<=20ya nahi z\n"
        res = self._assert_idempotent_and_semantic(src)
        self.assertIn("a = b + c * d - e // f % g ** h", res)
        self.assertIn("flag = x > 10 aur y <= 20 ya nahi z", res)

    # -------------------------------------------------------------------------
    # 2. Indentation & Nested Blocks
    # -------------------------------------------------------------------------

    def test_nested_blocks_and_control_flow(self) -> None:
        src = """
agar x > 10:
  agar y > 20:
      dikhao("high")
  warna:
    dikhao("mid")
warna:
        dikhao("low")
"""
        res = self._assert_idempotent_and_semantic(src)
        expected = (
            "agar x > 10:\n"
            "    agar y > 20:\n"
            '        dikhao("high")\n'
            "    warna:\n"
            '        dikhao("mid")\n'
            "warna:\n"
            '    dikhao("low")\n'
        )
        self.assertEqual(res, expected)

    def test_while_and_for_loops(self) -> None:
        src = """
count = 5
jabtak count > 0:
    count -= 1
    agar count == 2:
        aage_bado
    agar count == 0:
        ruko

har item mein [1, 2, 3]:
    dikhao(item)
"""
        res = self._assert_idempotent_and_semantic(src)
        self.assertIn("jabtak count > 0:\n    count -= 1", res)
        self.assertIn("har item mein [1, 2, 3]:\n    dikhao(item)", res)

    # -------------------------------------------------------------------------
    # 3. Expressions & Precedence
    # -------------------------------------------------------------------------

    def test_expression_precedence_and_parentheses(self) -> None:
        src = """
a = (1 + 2) * 3
b = 1 + (2 * 3)
c = (x ya y) aur z
d = x aur (y ya z)
walrus = (x := 10)
"""
        res = self._assert_idempotent_and_semantic(src)
        self.assertIn("a = (1 + 2) * 3", res)
        self.assertIn("b = 1 + 2 * 3", res)
        self.assertIn("c = (x ya y) aur z", res)
        self.assertIn("d = x aur (y ya z)", res)
        self.assertIn("walrus = (x := 10)", res)

    def test_collections_and_comprehensions(self) -> None:
        src = """
lst = [1, 2, 3]
tup = (1, 2)
single = (42,)
empty_tup = ()
dct = {"k1": 10, "k2": 20}
st = {1, 2, 3}

c_lst = [x * 2 har x mein lst agar x > 1]
c_dct = {k: v * 10 har k, v mein dct.items()}
c_gen = (x har x mein lst)
c_set = {x % 2 har x mein lst}
"""
        res = self._assert_idempotent_and_semantic(src)
        self.assertIn("single = (42,)", res)
        self.assertIn("empty_tup = ()", res)
        self.assertIn("c_lst = [x * 2 har x mein lst agar x > 1]", res)
        self.assertIn("c_dct = {k: v * 10 har k, v mein dct.items()}", res)
        self.assertIn("c_gen = (x har x mein lst)", res)
        self.assertIn("c_set = {x % 2 har x mein lst}", res)

    def test_indexing_and_slicing(self) -> None:
        src = """
elem = arr[0]
sub1 = arr[1:5]
sub2 = arr[:5]
sub3 = arr[2:]
sub4 = arr[::2]
sub5 = arr[1:10:2]
"""
        res = self._assert_idempotent_and_semantic(src)
        self.assertIn("elem = arr[0]", res)
        self.assertIn("sub1 = arr[1:5]", res)
        self.assertIn("sub2 = arr[:5]", res)
        self.assertIn("sub3 = arr[2:]", res)
        self.assertIn("sub4 = arr[::2]", res)
        self.assertIn("sub5 = arr[1:10:2]", res)

    # -------------------------------------------------------------------------
    # 4. Functions & Parameters
    # -------------------------------------------------------------------------

    def test_function_formatting_and_signatures(self) -> None:
        src = """
@first_deco
@second_deco(opt=sahi)
kaam process(p1, p2=10, /, normal=20, *, kw1: akshar, kw2: purnank = 5, **kwargs) -> sahi:
    wapas normal + kw2

lam = sookshm x, y: x * y
"""
        res = self._assert_idempotent_and_semantic(src)
        self.assertIn("@first_deco\n@second_deco(opt=sahi)", res)
        self.assertIn("kaam process(p1, p2=10, /, normal=20, *, kw1: akshar, kw2: purnank = 5, **kwargs) -> sahi:", res)
        self.assertIn("lam = sookshm x, y: x * y", res)

    # -------------------------------------------------------------------------
    # 5. OOP & Classes
    # -------------------------------------------------------------------------

    def test_class_formatting(self) -> None:
        src = """
@singleton
varg Animal(BaseModel, Serializable):
    species = "Canine"

    kaam __init__(khood, name: akshar):
        khood.name = name

    kaam speak(khood) -> akshar:
        wapas f"{khood.name} barks"
"""
        res = self._assert_idempotent_and_semantic(src)
        self.assertIn("varg Animal(BaseModel, Serializable):", res)
        self.assertIn('species = "Canine"', res)
        self.assertIn("kaam __init__(khood, name: akshar):", res)
        self.assertIn("kaam speak(khood) -> akshar:", res)

    # -------------------------------------------------------------------------
    # 6. Exceptions
    # -------------------------------------------------------------------------

    def test_exceptions_and_assertions(self) -> None:
        src = """
daawa score >= 0, "Score cannot be negative"

koshish:
    res = 10 / x
pakdo ZeroDivisionError jaise err:
    uthav ValueError("Divide by zero")
warna:
    dikhao("Success")
antatah:
    cleanup()
"""
        res = self._assert_idempotent_and_semantic(src)
        self.assertIn('daawa score >= 0, "Score cannot be negative"', res)
        self.assertIn("koshish:\n    res = 10 / x", res)
        self.assertIn("pakdo ZeroDivisionError jaise err:", res)
        self.assertIn('uthav ValueError("Divide by zero")', res)
        self.assertIn("warna:\n    dikhao(\"Success\")", res)
        self.assertIn("antatah:\n    cleanup()", res)

    # -------------------------------------------------------------------------
    # 7. Generators & Async
    # -------------------------------------------------------------------------

    def test_generators_and_async(self) -> None:
        src = """
kaam num_gen():
    upaj 1
    upaj se other_gen()
    upaj

asamanantar kaam fetch_all(urls):
    asamanantar saath open_session() jaise sess:
        asamanantar har url mein urls:
            data = intezaar sess.get(url)
"""
        res = self._assert_idempotent_and_semantic(src)
        self.assertIn("upaj 1", res)
        self.assertIn("upaj se other_gen()", res)
        self.assertIn("asamanantar kaam fetch_all(urls):", res)
        self.assertIn("asamanantar saath open_session() jaise sess:", res)
        self.assertIn("asamanantar har url mein urls:", res)
        self.assertIn("data = intezaar sess.get(url)", res)

    # -------------------------------------------------------------------------
    # 8. Pattern Matching
    # -------------------------------------------------------------------------

    def test_pattern_matching_formatting(self) -> None:
        src = """
milao command:
    vichaar "quit" | "exit":
        ruko
    vichaar [x, y]:
        handle_point(x, y)
    vichaar {"type": "event", **rest}:
        handle_event(rest)
    vichaar User(name=n, age=a) agar a > 18:
        handle_adult(n)
    vichaar _:
        default_handler()
"""
        res = self._assert_idempotent_and_semantic(src)
        self.assertIn("milao command:", res)
        self.assertIn('vichaar "quit" | "exit":', res)
        self.assertIn("vichaar [x, y]:", res)
        self.assertIn('vichaar {"type": "event", **rest}:', res)
        self.assertIn("vichaar User(name=n, age=a) agar a > 18:", res)
        self.assertIn("vichaar _:", res)

    # -------------------------------------------------------------------------
    # 9. Imports
    # -------------------------------------------------------------------------

    def test_import_forms(self) -> None:
        src = """
laao math
laao os, sys jaise system
se utils laao calculate, format_str jaise fmt
se .models laao User
"""
        res = self._assert_idempotent_and_semantic(src)
        self.assertIn("laao math", res)
        self.assertIn("laao os, sys jaise system", res)
        self.assertIn("se utils laao calculate, format_str jaise fmt", res)
        self.assertIn("se .models laao User", res)

    # -------------------------------------------------------------------------
    # 10. Strings (Preservation of Quotes, Escapes, Triple Quotes, F-Strings)
    # -------------------------------------------------------------------------

    def test_string_literal_preservation(self) -> None:
        src = """
s1 = 'single quoted with \"double\"'
s2 = "double quoted with 'single'"
s3 = '''triple
single'''
s4 = \"\"\"triple
double
multiline\"\"\"
s5 = r"raw \\n not escape"
s6 = f"hello {name!r:>10}"
"""
        formatted = format_source(src)
        formatted_again = format_source(formatted)
        self.assertEqual(formatted, formatted_again)

        # Quotes and escapes must match exactly
        self.assertIn("s1 = 'single quoted with \"double\"'", formatted)
        self.assertIn("s2 = \"double quoted with 'single'\"", formatted)
        self.assertIn("s3 = '''triple\nsingle'''", formatted)
        self.assertIn('s5 = r"raw \\n not escape"', formatted)
        self.assertIn('s6 = f"hello {name!r:>10}"', formatted)

    # -------------------------------------------------------------------------
    # 11. Comments (Standalone, Inline, Block)
    # -------------------------------------------------------------------------

    def test_comments_preservation(self) -> None:
        src = """# Module Header Comment

# Another Comment Line
x = 10  # Inline on x

# Explaining calculate
kaam calculate(a, b):
    # Inside calculate
    total = a + b  # compute sum
    wapas total  # return it

# Trailing footer comment
"""
        res = format_source(src)
        res_again = format_source(res)
        self.assertEqual(res, res_again)

        self.assertIn("# Module Header Comment", res)
        self.assertIn("x = 10  # Inline on x", res)
        self.assertIn("# Explaining calculate\nkaam calculate(a, b):", res)
        self.assertIn("    # Inside calculate\n    total = a + b  # compute sum", res)
        self.assertIn("# Trailing footer comment", res)

    # -------------------------------------------------------------------------
    # 12. CLI Integration
    # -------------------------------------------------------------------------

    def test_cli_format_stdin(self) -> None:
        proc = subprocess.run(
            ["python3", "-m", "hinglish.cli", "format", "-"],
            input="x=10+20\n",
            capture_output=True,
            text=True,
        )
        self.assertEqual(proc.returncode, 0)
        self.assertEqual(proc.stdout, "x = 10 + 20\n")

    def test_cli_format_check_flag(self) -> None:
        # Unformatted -> exit 1
        proc1 = subprocess.run(
            ["python3", "-m", "hinglish.cli", "format", "-", "--check"],
            input="x=10+20\n",
            capture_output=True,
            text=True,
        )
        self.assertEqual(proc1.returncode, 1)

        # Formatted -> exit 0
        proc2 = subprocess.run(
            ["python3", "-m", "hinglish.cli", "format", "-", "--check"],
            input="x = 10 + 20\n",
            capture_output=True,
            text=True,
        )
        self.assertEqual(proc2.returncode, 0)

    def test_cli_format_file_and_output(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            f = Path(tmpdir) / "prog.hin"
            f.write_text("a=1*2\n")

            # Check fails
            res = subprocess.run(
                ["python3", "-m", "hinglish.cli", "format", str(f), "--check"],
                capture_output=True,
            )
            self.assertEqual(res.returncode, 1)

            # Output to separate file
            out_file = Path(tmpdir) / "formatted.hin"
            res = subprocess.run(
                ["python3", "-m", "hinglish.cli", "format", str(f), "-o", str(out_file)],
                capture_output=True,
            )
            self.assertEqual(res.returncode, 0)
            self.assertEqual(out_file.read_text(), "a = 1 * 2\n")
            self.assertEqual(f.read_text(), "a=1*2\n")  # unchanged

            # In-place format
            res = subprocess.run(
                ["python3", "-m", "hinglish.cli", "format", str(f)],
                capture_output=True,
            )
            self.assertEqual(res.returncode, 0)
            self.assertEqual(f.read_text(), "a = 1 * 2\n")

    # -------------------------------------------------------------------------
    # 13. LSP Integration (textDocument/formatting)
    # -------------------------------------------------------------------------

    def test_lsp_formatting_request(self) -> None:
        in_stream = io.BytesIO()
        out_stream = io.BytesIO()
        server = HinglishLanguageServer(in_stream=in_stream, out_stream=out_stream)

        # 1. Initialize
        server.handle_message({
            "jsonrpc": "2.0",
            "id": 1,
            "method": "initialize",
            "params": {"capabilities": {}},
        })
        out_stream.seek(0)
        init_resp = read_message(out_stream)
        self.assertTrue(init_resp["result"]["capabilities"]["documentFormattingProvider"])

        # 2. Open document
        doc_uri = "file:///workspace/demo.hin"
        server.handle_message({
            "jsonrpc": "2.0",
            "method": "textDocument/didOpen",
            "params": {
                "textDocument": {
                    "uri": doc_uri,
                    "version": 1,
                    "text": "num=10+20\n",
                }
            },
        })

        # 3. Request formatting
        out_stream.seek(0)
        out_stream.truncate(0)
        server.handle_message({
            "jsonrpc": "2.0",
            "id": 2,
            "method": "textDocument/formatting",
            "params": {
                "textDocument": {"uri": doc_uri},
                "options": {"tabSize": 4, "insertSpaces": True},
            },
        })
        out_stream.seek(0)
        format_resp = read_message(out_stream)
        edits = format_resp["result"]
        self.assertEqual(len(edits), 1)
        self.assertEqual(edits[0]["newText"], "num = 10 + 20\n")

    def test_lsp_formatting_syntax_error_fails_safely(self) -> None:
        in_stream = io.BytesIO()
        out_stream = io.BytesIO()
        server = HinglishLanguageServer(in_stream=in_stream, out_stream=out_stream)

        doc_uri = "file:///workspace/broken.hin"
        server.handle_message({
            "jsonrpc": "2.0",
            "method": "textDocument/didOpen",
            "params": {
                "textDocument": {
                    "uri": doc_uri,
                    "version": 1,
                    "text": "agar x > :\n",
                }
            },
        })

        out_stream.seek(0)
        out_stream.truncate(0)
        server.handle_message({
            "jsonrpc": "2.0",
            "id": 3,
            "method": "textDocument/formatting",
            "params": {"textDocument": {"uri": doc_uri}},
        })
        out_stream.seek(0)
        resp = read_message(out_stream)
        self.assertEqual(resp["result"], [])

    # -------------------------------------------------------------------------
    # 14. VS Code Extension Metadata
    # -------------------------------------------------------------------------

    def test_vscode_extension_formatter_metadata(self) -> None:
        pkg_json_path = Path(__file__).parent.parent / "vscode-hinglish" / "package.json"
        pkg = json.loads(pkg_json_path.read_text(encoding="utf-8"))
        self.assertIn("Formatters", pkg["categories"])
        self.assertIn("formatter", pkg["keywords"])
        self.assertIn("formatter", pkg["description"].lower())


if __name__ == "__main__":
    unittest.main()
