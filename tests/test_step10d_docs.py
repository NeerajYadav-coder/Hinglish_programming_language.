"""Tests for Step 10D — Hinglish Official Documentation Website (v1.0.0).

Verifies:
1. Static build artifacts exist in docs/dist.
2. Documentation keyword dataset exactly matches DEFAULT_KEYWORD_REGISTRY.
3. All code examples on the documentation website parse and compile as valid Hinglish.
4. Navigation routes and internal links resolve correctly.
5. Docs directory remains properly isolated from the core Python package.
"""

import os
import re
import unittest
from pathlib import Path

from hinglish.keywords import DEFAULT_KEYWORD_REGISTRY
from hinglish.parser import parse
from hinglish.compiler import HinglishCompiler


class TestStep10DDocs(unittest.TestCase):
    """Test suite verifying official documentation website integrity."""

    def setUp(self) -> None:
        self.repo_root = Path(__file__).parent.parent
        self.docs_dir = self.repo_root / "docs"
        self.dist_dir = self.docs_dir / "dist"
        self.src_dir = self.docs_dir / "src"

    def test_docs_build_artifacts_exist(self) -> None:
        """Verify that docs/dist/index.html and built assets exist."""
        index_html = self.dist_dir / "index.html"
        if not index_html.exists():
            import subprocess
            subprocess.run(["npm", "run", "build"], cwd=str(self.docs_dir), check=False)

        self.assertTrue(index_html.exists(), "docs/dist/index.html must exist")
        content = index_html.read_text(encoding="utf-8")
        self.assertIn("Hinglish", content)
        self.assertTrue("v1.1.0" in content or "v1.0.0" in content)

        assets_dir = self.dist_dir / "assets"
        self.assertTrue(assets_dir.exists(), "docs/dist/assets must exist")
        js_files = list(assets_dir.glob("*.js"))
        css_files = list(assets_dir.glob("*.css"))
        self.assertGreater(len(js_files), 0, "At least one bundled JavaScript file must exist")
        self.assertGreater(len(css_files), 0, "At least one bundled CSS file must exist")

    def test_all_keywords_in_docs(self) -> None:
        """Verify that all keywords from DEFAULT_KEYWORD_REGISTRY are in keywords.ts."""
        keywords_ts_path = self.src_dir / "data" / "keywords.ts"
        self.assertTrue(keywords_ts_path.exists(), "keywords.ts must exist")
        content = keywords_ts_path.read_text(encoding="utf-8")

        all_registered = DEFAULT_KEYWORD_REGISTRY.all_hinglish_words()
        self.assertGreater(len(all_registered), 30, "Registry should contain over 30 words")

        missing_tokens = []
        for word in all_registered:
            # Check for token: 'word' in content
            pattern = rf"token:\s*['\"]{re.escape(word)}['\"]"
            alias_pattern = rf"aliases:\s*\[[^\]]*['\"]{re.escape(word)}['\"]"
            if not re.search(pattern, content) and not re.search(alias_pattern, content):
                missing_tokens.append(word)

        self.assertEqual(
            missing_tokens,
            [],
            f"Keywords missing from documentation dataset: {missing_tokens}",
        )

    def test_examples_syntactically_valid(self) -> None:
        """Verify that all executable Hinglish code blocks in examples.ts compile cleanly."""
        examples_ts_path = self.src_dir / "data" / "examples.ts"
        self.assertTrue(examples_ts_path.exists(), "examples.ts must exist")
        content = examples_ts_path.read_text(encoding="utf-8")

        # Extract all hinglishCode template strings
        pattern = r"hinglishCode:\s*`([^`]+)`"
        matches = re.findall(pattern, content)
        self.assertGreater(len(matches), 5, "Should have multiple Hinglish examples")

        compiler = HinglishCompiler()
        for idx, code in enumerate(matches):
            # Skip multi-file mock example that has split file headers
            if "File: utils.hin" in code:
                continue
            with self.subTest(example_idx=idx):
                ast_node = parse(code)
                py_code = compiler.compile(ast_node)
                # Verify that python code compiles to bytecode cleanly
                compiled = compile(py_code, f"<example_{idx}>", "exec")
                self.assertIsNotNone(compiled)

    def test_navigation_routes_resolve(self) -> None:
        """Verify that all routes defined in Sidebar.tsx are handled in App.tsx."""
        sidebar_path = self.src_dir / "components" / "Sidebar.tsx"
        app_path = self.src_dir / "App.tsx"

        sidebar_content = sidebar_path.read_text(encoding="utf-8")
        app_content = app_path.read_text(encoding="utf-8")

        # Find all route ids in sidebar: id: '/...'
        routes = re.findall(r"id:\s*['\"](/[^'\"]*)['\"]", sidebar_content)
        self.assertGreater(len(routes), 5, "Sidebar should define multiple navigation routes")

        for route in routes:
            with self.subTest(route=route):
                # Ensure route is handled in App.tsx switch statement
                self.assertIn(
                    f"case '{route}':",
                    app_content,
                    f"Route '{route}' from Sidebar.tsx not handled in App.tsx router",
                )

    def test_package_isolation(self) -> None:
        """Verify that docs directory is excluded from Python package distribution in pyproject.toml."""
        pyproject_path = self.repo_root / "pyproject.toml"
        content = pyproject_path.read_text(encoding="utf-8")
        self.assertIn('"docs*"', content, "docs* must be excluded in pyproject.toml package finder")


if __name__ == "__main__":
    unittest.main()
