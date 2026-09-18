"""Unit tests for Step 10C: VS Code Developer Tooling (Syntax Highlighting)."""

import json
import re
import subprocess
import sys
import unittest
import zipfile
from pathlib import Path

from hinglish.keywords import DEFAULT_KEYWORD_REGISTRY
from hinglish.runtime import run_file


class TestStep10cVscode(unittest.TestCase):
    """Verifies VS Code extension manifest, grammar, language configuration, and editor demo."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.repo_root = Path(__file__).parent.parent.resolve()
        cls.ext_dir = cls.repo_root / "vscode-hinglish"
        cls.package_json_path = cls.ext_dir / "package.json"
        cls.lang_config_path = cls.ext_dir / "language-configuration.json"
        cls.grammar_path = cls.ext_dir / "syntaxes" / "hinglish.tmLanguage.json"
        cls.demo_file = cls.repo_root / "examples" / "editor_demo.hin"

    # -------------------------------------------------------------------------
    # 1. Extension Manifest & Metadata
    # -------------------------------------------------------------------------

    def test_package_json_structure(self) -> None:
        """Verifies package.json exists, is valid JSON, and has all required extension keys."""
        self.assertTrue(self.package_json_path.is_file())
        with open(self.package_json_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        self.assertEqual(data.get("name"), "hinglish")
        self.assertEqual(data.get("version"), "1.0.0")
        self.assertIn("engines", data)
        self.assertIn("vscode", data["engines"])

        # Language contribution
        languages = data.get("contributes", {}).get("languages", [])
        self.assertEqual(len(languages), 1)
        lang = languages[0]
        self.assertEqual(lang.get("id"), "hinglish")
        self.assertIn(".hin", lang.get("extensions", []))
        self.assertEqual(lang.get("configuration"), "./language-configuration.json")

        # Grammar contribution
        grammars = data.get("contributes", {}).get("grammars", [])
        self.assertEqual(len(grammars), 1)
        grammar = grammars[0]
        self.assertEqual(grammar.get("language"), "hinglish")
        self.assertEqual(grammar.get("scopeName"), "source.hinglish")
        self.assertEqual(grammar.get("path"), "./syntaxes/hinglish.tmLanguage.json")

    # -------------------------------------------------------------------------
    # 2. Language Configuration
    # -------------------------------------------------------------------------

    def test_language_configuration(self) -> None:
        """Verifies language-configuration.json comments, brackets, and indentation regexes."""
        self.assertTrue(self.lang_config_path.is_file())
        with open(self.lang_config_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        self.assertEqual(data.get("comments", {}).get("lineComment"), "#")
        self.assertIn("brackets", data)
        self.assertIn("autoClosingPairs", data)
        self.assertIn("surroundingPairs", data)

        # Validate indentation regexes compile
        indent_rules = data.get("indentationRules", {})
        increase_pat = indent_rules.get("increaseIndentPattern")
        decrease_pat = indent_rules.get("decreaseIndentPattern")
        self.assertIsNotNone(increase_pat)
        self.assertIsNotNone(decrease_pat)

        re_increase = re.compile(increase_pat)
        re_decrease = re.compile(decrease_pat)

        # Test positive match on statements
        self.assertTrue(re_increase.search("agar x > 5:"))
        self.assertTrue(re_increase.search("kaam greet(naam):"))
        self.assertTrue(re_decrease.search("warna:"))
        self.assertTrue(re_decrease.search("pakdo Exception:"))

    # -------------------------------------------------------------------------
    # 3. TextMate Grammar
    # -------------------------------------------------------------------------

    def test_textmate_grammar_validity_and_regexes(self) -> None:
        """Verifies TextMate grammar is valid JSON and all regular expressions compile."""
        self.assertTrue(self.grammar_path.is_file())
        with open(self.grammar_path, "r", encoding="utf-8") as f:
            grammar = json.load(f)

        self.assertEqual(grammar.get("name"), "Hinglish")
        self.assertEqual(grammar.get("scopeName"), "source.hinglish")
        self.assertIn("repository", grammar)
        self.assertIn("patterns", grammar)

        # Walk through grammar and compile all regexes
        def check_patterns(obj: object) -> None:
            if isinstance(obj, dict):
                for key, val in obj.items():
                    if key in ("match", "begin", "end") and isinstance(val, str):
                        try:
                            re.compile(val)
                        except re.error as e:
                            self.fail(f"Invalid regex '{val}' in grammar: {e}")
                    else:
                        check_patterns(val)
            elif isinstance(obj, list):
                for item in obj:
                    check_patterns(item)

        check_patterns(grammar)

    def test_grammar_covers_all_keyword_registry_entries(self) -> None:
        """Ensures that every keyword, literal, and builtin from DEFAULT_KEYWORD_REGISTRY is in grammar."""
        grammar_text = self.grammar_path.read_text(encoding="utf-8")

        # Statement keywords
        for kw in DEFAULT_KEYWORD_REGISTRY._statement_keywords:
            self.assertIn(
                kw,
                grammar_text,
                f"Statement keyword '{kw}' missing from TextMate grammar",
            )

        # Operator keywords
        for op in DEFAULT_KEYWORD_REGISTRY._operator_keywords:
            self.assertIn(
                op,
                grammar_text,
                f"Operator keyword '{op}' missing from TextMate grammar",
            )

        # Literal keywords
        for lit in DEFAULT_KEYWORD_REGISTRY._literal_keywords:
            self.assertIn(
                lit,
                grammar_text,
                f"Literal keyword '{lit}' missing from TextMate grammar",
            )

        # Builtin functions
        for fn in DEFAULT_KEYWORD_REGISTRY._builtin_functions:
            self.assertIn(
                fn,
                grammar_text,
                f"Built-in function '{fn}' missing from TextMate grammar",
            )

    # -------------------------------------------------------------------------
    # 4. Showcase Editor Demo File Execution
    # -------------------------------------------------------------------------

    def test_editor_demo_hin_compiles_and_runs(self) -> None:
        """Verifies examples/editor_demo.hin executes cleanly without errors."""
        self.assertTrue(self.demo_file.is_file())
        ns = run_file(self.demo_file)
        self.assertEqual(ns.get("hyp"), 5.0)
        self.assertEqual(ns.get("rect").area(), 50)
        self.assertEqual(ns.get("even_squares"), [4, 16, 36])
        self.assertEqual(ns.get("stream_result"), [1, 2, 3])
        self.assertEqual(ns.get("sarvavyapi_counter"), 1)

    # -------------------------------------------------------------------------
    # 5. VSIX Package Verification
    # -------------------------------------------------------------------------

    def test_vsix_package_contents(self) -> None:
        """Verifies that hinglish-1.0.0.vsix exists and contains valid extension payload."""
        vsix_file = self.ext_dir / "hinglish-1.0.0.vsix"
        self.assertTrue(vsix_file.is_file(), "VSIX package was not generated")
        with zipfile.ZipFile(vsix_file, "r") as zf:
            file_names = zf.namelist()
            self.assertIn("extension/package.json", file_names)
            self.assertIn("extension/language-configuration.json", file_names)
            self.assertIn("extension/syntaxes/hinglish.tmLanguage.json", file_names)
            self.assertIn("extension/readme.md", file_names)
            self.assertIn("extension/LICENSE.md", file_names)


if __name__ == "__main__":
    unittest.main()
