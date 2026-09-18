"""Tests for Hinglish keyword registry, mappings, and vocabulary configurability."""

import unittest
from hinglish.keywords import DEFAULT_KEYWORD_REGISTRY, KeywordRegistry


class TestKeywordRegistry(unittest.TestCase):
    """Verifies keyword mappings, alias resolution, and custom vocabulary extension."""

    def setUp(self) -> None:
        self.registry = DEFAULT_KEYWORD_REGISTRY

    def test_core_statement_keywords(self) -> None:
        expected = {
            "agar": "if",
            "warna": "else",
            "warna_agar": "elif",
            "jabtak": "while",
            "har": "for",
            "mein": "in",
            "kaam": "def",
            "wapas": "return",
            "ruko": "break",
            "aage_bado": "continue",
            "chhod_do": "pass",
        }
        for hin_kw, py_kw in expected.items():
            self.assertTrue(
                self.registry.is_keyword(hin_kw),
                f"Expected '{hin_kw}' to be recognized as keyword",
            )
            self.assertEqual(
                self.registry.get_python_equivalent(hin_kw),
                py_kw,
                f"Expected '{hin_kw}' to map to '{py_kw}'",
            )
            self.assertTrue(self.registry.is_statement_keyword(hin_kw))

    def test_logical_operators(self) -> None:
        logical_ops = {
            "aur": "and",
            "ya": "or",
            "nahi": "not",
        }
        for hin_op, py_op in logical_ops.items():
            self.assertEqual(self.registry.get_python_equivalent(hin_op), py_op)

    def test_literal_values(self) -> None:
        literals = {
            "sahi": "True",
            "galat": "False",
            "kuch_nahi": "None",
        }
        for hin_lit, py_lit in literals.items():
            self.assertTrue(self.registry.is_literal_keyword(hin_lit))
            self.assertEqual(self.registry.get_python_equivalent(hin_lit), py_lit)

    def test_builtin_functions(self) -> None:
        self.assertTrue(self.registry.is_builtin_function("dikhao"))
        self.assertEqual(self.registry.get_python_equivalent("dikhao"), "print")

    def test_aliases(self) -> None:
        self.assertEqual(self.registry.get_python_equivalent("andar"), "in")
        self.assertEqual(self.registry.get_canonical_hinglish("andar"), "mein")

        self.assertEqual(self.registry.get_python_equivalent("shunya"), "None")
        self.assertEqual(self.registry.get_canonical_hinglish("shunya"), "kuch_nahi")

        self.assertEqual(self.registry.get_python_equivalent("chapo"), "print")
        self.assertEqual(self.registry.get_canonical_hinglish("chapo"), "dikhao")

    def test_reverse_lookup(self) -> None:
        self.assertEqual(self.registry.get_primary_hinglish("if"), "agar")
        self.assertEqual(self.registry.get_primary_hinglish("else"), "warna")
        self.assertEqual(self.registry.get_primary_hinglish("def"), "kaam")
        self.assertEqual(self.registry.get_primary_hinglish("return"), "wapas")

    def test_custom_registry_extensibility(self) -> None:
        custom = KeywordRegistry()
        custom.register_statement_keyword("yadi", "if")
        custom.register_alias("maan_lo", "yadi")

        self.assertTrue(custom.is_keyword("yadi"))
        self.assertEqual(custom.get_python_equivalent("yadi"), "if")
        self.assertTrue(custom.is_keyword("maan_lo"))
        self.assertEqual(custom.get_python_equivalent("maan_lo"), "if")
        self.assertEqual(custom.get_canonical_hinglish("maan_lo"), "yadi")


if __name__ == "__main__":
    unittest.main()
