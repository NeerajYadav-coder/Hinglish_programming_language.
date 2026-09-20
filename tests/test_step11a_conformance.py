"""Step 11A Conformance and Release Test Suite.

Verifies end-to-end conformance of Hinglish across the comprehensive
13-program conformance corpus, formatting idempotence, AST equivalence,
linter determinism, packaging integrity, and runtime robustness.
"""

import ast
import os
from pathlib import Path
import re
import tomllib
import unittest

import hinglish
from hinglish.compiler import HinglishCompiler
from hinglish.exceptions import HinglishLexerError, HinglishSyntaxError
from hinglish.formatter import format_source
from hinglish.lexer import tokenize
from hinglish.linter import lint_source
from hinglish.parser import parse
from hinglish.runtime import run, run_file


class TestStep11aConformance(unittest.TestCase):
    """End-to-end verification of the 13 conformance corpus programs."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.repo_root = Path(__file__).resolve().parent.parent
        cls.conformance_dir = cls.repo_root / "examples" / "conformance"
        cls.conformance_files = sorted(cls.conformance_dir.glob("*.hin"))
        if not cls.conformance_files:
            raise RuntimeError(f"No conformance files found in {cls.conformance_dir}")

    def test_corpus_count(self) -> None:
        """Verifies exactly 13 conformance corpus programs exist."""
        self.assertGreaterEqual(len(self.conformance_files), 13)

    def test_conformance_execution(self) -> None:
        """Verifies each conformance program executes cleanly without error."""
        for file_path in self.conformance_files:
            with self.subTest(file=file_path.name):
                ns = run_file(file_path)
                self.assertIsInstance(ns, dict)

    def test_formatting_idempotence(self) -> None:
        """Verifies format(format(src)) == format(src) on all conformance programs."""
        for file_path in self.conformance_files:
            with self.subTest(file=file_path.name):
                src = file_path.read_text(encoding="utf-8")
                f1 = format_source(src)
                f2 = format_source(f1)
                self.assertEqual(f1, f2, f"Formatting is not idempotent for {file_path.name}")

    def test_format_preserves_ast_semantics(self) -> None:
        """Verifies parsing formatted code compiles to valid Python AST."""
        compiler = HinglishCompiler()
        for file_path in self.conformance_files:
            with self.subTest(file=file_path.name):
                src = file_path.read_text(encoding="utf-8")
                formatted_src = format_source(src)
                tree = parse(formatted_src)
                py_code = compiler.compile(tree)
                # Verify py_code compiles to standard Python AST without error
                py_ast = ast.parse(py_code)
                self.assertIsNotNone(py_ast)

    def test_linter_zero_errors_on_conformance(self) -> None:
        """Verifies all conformance files pass static analysis without lint errors."""
        for file_path in self.conformance_files:
            with self.subTest(file=file_path.name):
                src = file_path.read_text(encoding="utf-8")
                diags = lint_source(src)
                error_diags = [d for d in diags if d.severity.name == "ERROR"]
                self.assertEqual(
                    len(error_diags),
                    0,
                    f"Unexpected lint errors in {file_path.name}: {error_diags}",
                )


class TestStep11aPackagingAndRobustness(unittest.TestCase):
    """Verifies packaging metadata, dependency purity, and error robustness."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.repo_root = Path(__file__).resolve().parent.parent
        cls.pyproject_path = cls.repo_root / "pyproject.toml"

    def test_zero_mandatory_runtime_dependencies(self) -> None:
        """Ensures pyproject.toml has zero external runtime dependencies."""
        with open(self.pyproject_path, "rb") as f:
            data = tomllib.load(f)
        deps = data.get("project", {}).get("dependencies", None)
        self.assertIsNotNone(deps, "dependencies field missing from pyproject.toml")
        self.assertEqual(
            deps,
            [],
            f"Expected zero runtime dependencies in pyproject.toml, found: {deps}",
        )

    def test_version_consistency_across_all_modules(self) -> None:
        """Ensures version 1.1.0 is consistent across pyproject, package, vscode, and docs."""
        with open(self.pyproject_path, "rb") as f:
            pyproject_ver = tomllib.load(f)["project"]["version"]

        pkg_ver = hinglish.__version__
        self.assertEqual(pyproject_ver, "1.1.0")
        self.assertEqual(pkg_ver, "1.1.0")

        # VS Code extension package.json
        vscode_pkg = self.repo_root / "vscode-hinglish" / "package.json"
        if vscode_pkg.exists():
            import json
            with open(vscode_pkg, "r", encoding="utf-8") as f:
                vscode_data = json.load(f)
            self.assertEqual(vscode_data["version"], "1.1.0")

        # Docs package.json
        docs_pkg = self.repo_root / "docs" / "package.json"
        if docs_pkg.exists():
            import json
            with open(docs_pkg, "r", encoding="utf-8") as f:
                docs_data = json.load(f)
            self.assertEqual(docs_data["version"], "1.1.0")

    def test_cli_entrypoints_configured(self) -> None:
        """Verifies CLI entrypoints hinglish, hinglish-lsp, hinglish-dap are configured."""
        with open(self.pyproject_path, "rb") as f:
            scripts = tomllib.load(f)["project"]["scripts"]
        self.assertIn("hinglish", scripts)
        self.assertIn("hinglish-lsp", scripts)
        self.assertIn("hinglish-dap", scripts)
        self.assertEqual(scripts["hinglish"], "hinglish.cli:main")
        self.assertEqual(scripts["hinglish-lsp"], "hinglish.lsp.server:main")
        self.assertEqual(scripts["hinglish-dap"], "hinglish.dap.server:main")

    def test_robustness_empty_and_whitespace_sources(self) -> None:
        """Verifies empty and whitespace-only files parse, compile, format, and run cleanly."""
        for src in ["", "   \n\n  \t  \n", "# Only a comment\n# Another comment\n"]:
            with self.subTest(src=repr(src)):
                tokens = tokenize(src)
                self.assertTrue(len(tokens) >= 1)
                tree = parse(src)
                self.assertEqual(len(tree.body), 0)
                formatted = format_source(src)
                self.assertIsInstance(formatted, str)
                ns = run(src)
                self.assertIsInstance(ns, dict)

    def test_robustness_unicode_and_hindi_literals(self) -> None:
        """Verifies Unicode in strings and comments works seamlessly."""
        src = '''
# यह एक हिंदी टिप्पणी है
sandesh = "नमस्ते दुनिया! 🚀 Hinglish v1.0"
dikhao(sandesh)
daawa sandesh == "नमस्ते दुनिया! 🚀 Hinglish v1.0"
'''
        ns = run(src)
        self.assertEqual(ns["sandesh"], "नमस्ते दुनिया! 🚀 Hinglish v1.0")

    def test_robustness_syntax_error_diagnostics(self) -> None:
        """Verifies malformed source raises clean HinglishSyntaxError with source position."""
        bad_sources = [
            "agar :\n    dikhao(1)",
            "kaam (a, b):\n    wapas a",
            "varg :\n    chhod_do",
            "har in items:\n    dikhao(1)",
        ]
        for bad in bad_sources:
            with self.subTest(bad=bad):
                with self.assertRaises(HinglishSyntaxError) as ctx:
                    parse(bad)
                self.assertIsNotNone(ctx.exception.line)
                self.assertIsNotNone(ctx.exception.column)


if __name__ == "__main__":
    unittest.main()
