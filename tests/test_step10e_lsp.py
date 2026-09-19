"""Tests for Step 10E — Hinglish Language Server Protocol (LSP) and Tooling.

Verifies:
- JSON-RPC 2.0 stdio message framing and parsing
- Document tracking, coordinates, and word extraction
- Live syntax and lexical diagnostics
- Contextual completions (keywords, builtins, snippets, local symbols)
- Hover documentation
- Go-to-Definition (local definitions and cross-file resolution)
- Hierarchical Document Symbols (Outline view)
- Find References and safe identifier Rename
- Server JSON-RPC request/notification dispatch and lifecycle
"""

import io
import json
import shutil
import tempfile
import unittest
from pathlib import Path

from hinglish.lsp.analyzer import HinglishAnalyzer
from hinglish.lsp.documents import Document, DocumentManager
from hinglish.lsp.protocol import (
    CompletionItemKind,
    DiagnosticSeverity,
    Position,
    Range,
    SymbolKind,
    read_message,
    write_message,
)
from hinglish.lsp.server import HinglishLanguageServer


class TestLspProtocol(unittest.TestCase):
    """Test JSON-RPC 2.0 framing and LSP data structures."""

    def test_message_roundtrip(self):
        stream = io.BytesIO()
        payload = {"jsonrpc": "2.0", "id": 42, "method": "ping", "params": {"key": "value"}}
        write_message(stream, payload)

        stream.seek(0)
        decoded = read_message(stream)
        self.assertEqual(decoded, payload)

    def test_read_empty_stream(self):
        stream = io.BytesIO()
        self.assertIsNone(read_message(stream))

    def test_read_malformed_stream(self):
        stream = io.BytesIO(b"Not-A-Header\r\n\r\n")
        self.assertIsNone(read_message(stream))


class TestDocumentManager(unittest.TestCase):
    """Test Document model and DocumentManager store."""

    def test_document_lines_and_words(self):
        doc = Document("file:///test.hin", "kaam greet(naam):\n    dikhao(naam)\n")
        self.assertEqual(len(doc.lines), 2)
        self.assertEqual(doc.get_line(0), "kaam greet(naam):\n")
        self.assertEqual(doc.get_line(1), "    dikhao(naam)\n")
        self.assertEqual(doc.get_line(99), "")

        # Word at position
        word_kaam = doc.get_word_at_position(Position(line=0, character=2))
        self.assertEqual(word_kaam, "kaam")

        word_greet = doc.get_word_at_position(Position(line=0, character=7))
        self.assertEqual(word_greet, "greet")

        word_dikhao = doc.get_word_at_position(Position(line=1, character=6))
        self.assertEqual(word_dikhao, "dikhao")

        # Word range
        rng = doc.get_word_range_at_position(Position(line=0, character=7))
        self.assertIsNotNone(rng)
        self.assertEqual(rng.start.character, 5)
        self.assertEqual(rng.end.character, 10)

    def test_document_full_and_incremental_updates(self):
        mgr = DocumentManager()
        doc = mgr.open_document("file:///app.hin", "x = 10\n", version=1)
        self.assertEqual(doc.version, 1)

        # Full change
        mgr.change_document("file:///app.hin", [{"text": "x = 20\ny = 30\n"}], version=2)
        self.assertEqual(doc.version, 2)
        self.assertEqual(doc.text, "x = 20\ny = 30\n")

        # Close document
        mgr.close_document("file:///app.hin")
        self.assertIsNone(mgr.get_document("file:///app.hin"))


class TestHinglishAnalyzer(unittest.TestCase):
    """Test analyzer capabilities: diagnostics, completions, hover, definition, symbols, references, rename."""

    def setUp(self):
        self.analyzer = HinglishAnalyzer()
        self.temp_dir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    # 1. Diagnostics
    def test_diagnostics_valid_code(self):
        doc = Document("file:///valid.hin", "kaam add(a, b):\n    wapas a + b\n")
        diags = self.analyzer.get_diagnostics(doc)
        self.assertEqual(len(diags), 0)

    def test_diagnostics_syntax_error(self):
        doc = Document("file:///error.hin", "kaam (\n")
        diags = self.analyzer.get_diagnostics(doc)
        self.assertEqual(len(diags), 1)
        self.assertEqual(diags[0].severity, DiagnosticSeverity.Error)
        self.assertEqual(diags[0].source, "hinglish")
        self.assertIn("Expected function name", diags[0].message)

    def test_diagnostics_lexer_error(self):
        doc = Document("file:///error.hin", "x = @@@\n")
        diags = self.analyzer.get_diagnostics(doc)
        self.assertEqual(len(diags), 1)
        self.assertEqual(diags[0].severity, DiagnosticSeverity.Error)
        self.assertIn("Unexpected character", diags[0].message)

    def test_diagnostics_fault_tolerance(self):
        # Server should never crash on empty, partial, or malformed input
        doc = Document("file:///empty.hin", "")
        self.assertEqual(self.analyzer.get_diagnostics(doc), [])

    # 2. Completions
    def test_completions_keywords_and_builtins(self):
        doc = Document("file:///comp.hin", "k")
        comps = self.analyzer.get_completions(doc, Position(0, 1))
        labels = {c.label for c in comps}

        # Statement keywords
        self.assertIn("agar", labels)
        self.assertIn("kaam", labels)
        self.assertIn("har", labels)
        self.assertIn("varg", labels)
        self.assertIn("shreni", labels)

        # Builtins
        self.assertIn("dikhao", labels)
        self.assertIn("lambai", labels)
        self.assertIn("pucho", labels)

        # Snippets
        snippets = [c for c in comps if c.kind == CompletionItemKind.Snippet]
        self.assertTrue(len(snippets) >= 5)

    def test_completions_local_symbols(self):
        source = (
            "kaam calculate(base, factor):\n"
            "    result = base * factor\n"
            "    wapas result\n"
        )
        doc = Document("file:///comp.hin", source)
        comps = self.analyzer.get_completions(doc, Position(1, 4))
        labels = {c.label: c for c in comps}

        self.assertIn("calculate", labels)
        self.assertEqual(labels["calculate"].kind, CompletionItemKind.Function)

        self.assertIn("base", labels)
        self.assertEqual(labels["base"].kind, CompletionItemKind.Variable)

        self.assertIn("result", labels)
        self.assertEqual(labels["result"].kind, CompletionItemKind.Variable)

    # 3. Hover
    def test_hover_keyword(self):
        doc = Document("file:///hover.hin", "agar sahi:\n    chhod_do\n")
        hover_agar = self.analyzer.get_hover(doc, Position(0, 2))
        self.assertIsNotNone(hover_agar)
        self.assertIn("Python equivalent", hover_agar["contents"]["value"])
        self.assertIn("`if`", hover_agar["contents"]["value"])

        hover_sahi = self.analyzer.get_hover(doc, Position(0, 6))
        self.assertIsNotNone(hover_sahi)
        self.assertIn("`True`", hover_sahi["contents"]["value"])

    def test_hover_builtin(self):
        doc = Document("file:///hover.hin", "dikhao('Namaste')\n")
        hover = self.analyzer.get_hover(doc, Position(0, 3))
        self.assertIsNotNone(hover)
        self.assertIn("dikhao", hover["contents"]["value"])
        self.assertIn("print", hover["contents"]["value"])

    def test_hover_local_function(self):
        doc = Document("file:///hover.hin", "kaam greet(naam):\n    wapas naam\n")
        hover = self.analyzer.get_hover(doc, Position(0, 7))
        self.assertIsNotNone(hover)
        self.assertIn("kaam greet(naam)", hover["contents"]["value"])

    # 4. Go to Definition (Local & Cross-file)
    def test_local_definition(self):
        source = (
            "kaam multiply(x, y):\n"
            "    wapas x * y\n\n"
            "ans = multiply(4, 5)\n"
        )
        doc = Document("file:///local.hin", source)
        defn = self.analyzer.get_definition(doc, Position(3, 8))
        self.assertIsNotNone(defn)
        self.assertEqual(defn.uri, "file:///local.hin")
        self.assertEqual(defn.range.start.line, 0)
        self.assertEqual(defn.range.start.character, 5)

    def test_cross_file_definition(self):
        # Create helper.hin and main.hin in temp directory
        helper_path = Path(self.temp_dir) / "helper.hin"
        helper_path.write_text("kaam compute(val):\n    wapas val * 2\n", encoding="utf-8")

        main_path = Path(self.temp_dir) / "main.hin"
        main_source = "se helper laao compute\nres = compute(10)\n"
        main_path.write_text(main_source, encoding="utf-8")

        doc = Document(main_path.as_uri(), main_source)
        defn = self.analyzer.get_definition(doc, Position(1, 8))
        self.assertIsNotNone(defn)
        self.assertEqual(defn.uri, helper_path.as_uri())
        self.assertEqual(defn.range.start.line, 0)
        self.assertEqual(defn.range.start.character, 5)

    # 5. Document Symbols (Outline View)
    def test_document_symbols_hierarchy(self):
        source = (
            "varg Greeter:\n"
            "    kaam __init__(khud, naam):\n"
            "        khud.naam = naam\n"
            "    kaam say_hi(khud):\n"
            "        dikhao(khud.naam)\n\n"
            "kaam standalone():\n"
            "    chhod_do\n\n"
            "total = 100\n"
        )
        doc = Document("file:///symbols.hin", source)
        symbols = self.analyzer.get_document_symbols(doc)
        self.assertEqual(len(symbols), 3)

        cls_sym = symbols[0]
        self.assertEqual(cls_sym.name, "Greeter")
        self.assertEqual(cls_sym.kind, SymbolKind.Class)
        self.assertEqual(len(cls_sym.children), 2)
        self.assertEqual(cls_sym.children[0].name, "__init__")
        self.assertEqual(cls_sym.children[0].kind, SymbolKind.Method)
        self.assertEqual(cls_sym.children[1].name, "say_hi")
        self.assertEqual(cls_sym.children[1].kind, SymbolKind.Method)

        fn_sym = symbols[1]
        self.assertEqual(fn_sym.name, "standalone")
        self.assertEqual(fn_sym.kind, SymbolKind.Function)

        var_sym = symbols[2]
        self.assertEqual(var_sym.name, "total")
        self.assertEqual(var_sym.kind, SymbolKind.Variable)

    # 6. References & Rename
    def test_references(self):
        source = "count = 0\ncount = count + 1\ndikhao(count)\n"
        doc = Document("file:///refs.hin", source)
        refs = self.analyzer.get_references(doc, Position(0, 2))
        self.assertEqual(len(refs), 4)

    def test_rename_valid(self):
        source = "count = 0\ncount = count + 1\ndikhao(count)\n"
        doc = Document("file:///rename.hin", source)
        edit = self.analyzer.rename_symbol(doc, Position(0, 0), "counter")
        self.assertIsNotNone(edit)
        edits = edit.changes[doc.uri]
        self.assertEqual(len(edits), 4)
        for e in edits:
            self.assertEqual(e.new_text, "counter")

    def test_rename_invalid_rejected(self):
        doc = Document("file:///rename.hin", "x = 10\n")
        # Cannot rename to keyword
        self.assertIsNone(self.analyzer.rename_symbol(doc, Position(0, 0), "agar"))
        # Cannot rename to invalid identifier
        self.assertIsNone(self.analyzer.rename_symbol(doc, Position(0, 0), "123bad"))


class TestHinglishLanguageServer(unittest.TestCase):
    """Test full JSON-RPC server request/response protocol loop."""

    def setUp(self):
        self.in_stream = io.BytesIO()
        self.out_stream = io.BytesIO()
        self.server = HinglishLanguageServer(
            in_stream=self.in_stream, out_stream=self.out_stream
        )

    def _send_and_get_response(self, message):
        self.out_stream.seek(0)
        self.out_stream.truncate(0)
        self.server.handle_message(message)
        self.out_stream.seek(0)
        return read_message(self.out_stream)

    def test_initialize_and_capabilities(self):
        req = {"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {}}
        res = self._send_and_get_response(req)
        self.assertEqual(res["id"], 1)
        caps = res["result"]["capabilities"]
        self.assertTrue(caps["hoverProvider"])
        self.assertTrue(caps["definitionProvider"])
        self.assertTrue(caps["documentSymbolProvider"])
        self.assertTrue(caps["referencesProvider"])
        self.assertTrue(caps["renameProvider"])
        self.assertEqual(caps["textDocumentSync"], 1)

    def test_did_open_and_publish_diagnostics(self):
        # Open invalid file -> triggers diagnostic notification
        notif = {
            "jsonrpc": "2.0",
            "method": "textDocument/didOpen",
            "params": {
                "textDocument": {
                    "uri": "file:///test.hin",
                    "version": 1,
                    "text": "kaam invalid(\n",
                }
            },
        }
        res = self._send_and_get_response(notif)
        self.assertEqual(res["method"], "textDocument/publishDiagnostics")
        self.assertEqual(res["params"]["uri"], "file:///test.hin")
        self.assertEqual(len(res["params"]["diagnostics"]), 1)

    def test_did_change_and_clear_diagnostics(self):
        # First open invalid file
        self.server.handle_message({
            "jsonrpc": "2.0",
            "method": "textDocument/didOpen",
            "params": {
                "textDocument": {
                    "uri": "file:///test.hin",
                    "version": 1,
                    "text": "kaam invalid(\n",
                }
            },
        })
        # Next fix it via didChange
        change_notif = {
            "jsonrpc": "2.0",
            "method": "textDocument/didChange",
            "params": {
                "textDocument": {"uri": "file:///test.hin", "version": 2},
                "contentChanges": [{"text": "kaam valid():\n    chhod_do\n"}],
            },
        }
        res = self._send_and_get_response(change_notif)
        self.assertEqual(res["method"], "textDocument/publishDiagnostics")
        self.assertEqual(res["params"]["diagnostics"], [])

    def test_completion_request(self):
        self.server.handle_message({
            "jsonrpc": "2.0",
            "method": "textDocument/didOpen",
            "params": {
                "textDocument": {
                    "uri": "file:///app.hin",
                    "version": 1,
                    "text": "kaam main():\n    chhod_do\n",
                }
            },
        })
        req = {
            "jsonrpc": "2.0",
            "id": 10,
            "method": "textDocument/completion",
            "params": {
                "textDocument": {"uri": "file:///app.hin"},
                "position": {"line": 0, "character": 0},
            },
        }
        res = self._send_and_get_response(req)
        self.assertEqual(res["id"], 10)
        labels = [item["label"] for item in res["result"]]
        self.assertIn("main", labels)
        self.assertIn("agar", labels)

    def test_hover_request(self):
        self.server.handle_message({
            "jsonrpc": "2.0",
            "method": "textDocument/didOpen",
            "params": {
                "textDocument": {
                    "uri": "file:///app.hin",
                    "version": 1,
                    "text": "agar sahi:\n    chhod_do\n",
                }
            },
        })
        req = {
            "jsonrpc": "2.0",
            "id": 11,
            "method": "textDocument/hover",
            "params": {
                "textDocument": {"uri": "file:///app.hin"},
                "position": {"line": 0, "character": 2},
            },
        }
        res = self._send_and_get_response(req)
        self.assertEqual(res["id"], 11)
        self.assertIn("`if`", res["result"]["contents"]["value"])

    def test_shutdown_and_exit(self):
        req = {"jsonrpc": "2.0", "id": 99, "method": "shutdown", "params": {}}
        res = self._send_and_get_response(req)
        self.assertEqual(res["id"], 99)
        self.assertIsNone(res["result"])
        self.assertTrue(self.server.shutdown_received)

    def test_unsupported_method(self):
        req = {"jsonrpc": "2.0", "id": 12, "method": "custom/unknownMethod", "params": {}}
        res = self._send_and_get_response(req)
        self.assertEqual(res["id"], 12)
        self.assertEqual(res["error"]["code"], -32601)


if __name__ == "__main__":
    unittest.main()
