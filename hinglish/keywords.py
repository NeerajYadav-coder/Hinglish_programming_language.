"""Configurable Keyword Registry for Hinglish.

This module defines the vocabulary mapping between Hinglish keywords/builtins
and their Python target equivalents. The registry is designed to be configurable
and extensible so vocabulary can be easily altered or extended with synonyms.
"""

from typing import Dict, List, Optional, Set


class KeywordRegistry:
    """Registry maintaining bidirectional mapping and aliases for Hinglish vocabulary."""

    def __init__(self) -> None:
        # Maps Hinglish token string -> Python equivalent
        self._hinglish_to_python: Dict[str, str] = {}

        # Maps Python target keyword -> Primary canonical Hinglish keyword
        self._python_to_hinglish: Dict[str, str] = {}

        # Maps alias -> Canonical Hinglish keyword
        self._alias_to_canonical: Dict[str, str] = {}

        # Set of reserved keywords (excluding functions like 'dikhao')
        self._statement_keywords: Set[str] = set()

        # Set of literal keywords (e.g. sahi, galat, kuch_nahi)
        self._literal_keywords: Set[str] = set()

        # Set of built-in function names (e.g. dikhao)
        self._builtin_functions: Set[str] = set()

        self._load_defaults()

    def _load_defaults(self) -> None:
        """Loads default initial keyword specifications."""
        # Core control flow and statement keywords
        statements = [
            ("agar", "if"),
            ("warna", "else"),
            ("warna_agar", "elif"),
            ("jabtak", "while"),
            ("har", "for"),
            ("mein", "in"),
            ("kaam", "def"),
            ("wapas", "return"),
            ("ruko", "break"),
            ("aage_bado", "continue"),
            ("chhod_do", "pass"),
        ]

        for hin_kw, py_kw in statements:
            self.register_statement_keyword(hin_kw, py_kw)

        # Logical operators
        logical_ops = [
            ("aur", "and"),
            ("ya", "or"),
            ("nahi", "not"),
        ]
        for hin_op, py_op in logical_ops:
            self.register_statement_keyword(hin_op, py_op)

        # Literal value keywords
        literals = [
            ("sahi", "True"),
            ("galat", "False"),
            ("kuch_nahi", "None"),
        ]
        for hin_lit, py_lit in literals:
            self.register_literal_keyword(hin_lit, py_lit)

        # Built-in functions
        self.register_builtin_function("dikhao", "print")

        # Aliases / Synonyms
        self.register_alias("andar", "mein")          # 'har x andar y' alternative
        self.register_alias("shunya", "kuch_nahi")    # 'shunya' alternative for None
        self.register_alias("chapo", "dikhao")        # 'chapo' alternative for print
        self.register_alias("batao", "dikhao")        # 'batao' alternative for print

    def register_statement_keyword(
        self, hinglish_kw: str, python_kw: str, aliases: Optional[List[str]] = None
    ) -> None:
        """Register a statement or operator keyword."""
        self._hinglish_to_python[hinglish_kw] = python_kw
        self._statement_keywords.add(hinglish_kw)
        if python_kw not in self._python_to_hinglish:
            self._python_to_hinglish[python_kw] = hinglish_kw

        if aliases:
            for alias in aliases:
                self.register_alias(alias, hinglish_kw)

    def register_literal_keyword(
        self, hinglish_kw: str, python_kw: str, aliases: Optional[List[str]] = None
    ) -> None:
        """Register a literal keyword (e.g., sahi -> True)."""
        self._hinglish_to_python[hinglish_kw] = python_kw
        self._literal_keywords.add(hinglish_kw)
        if python_kw not in self._python_to_hinglish:
            self._python_to_hinglish[python_kw] = hinglish_kw

        if aliases:
            for alias in aliases:
                self.register_alias(alias, hinglish_kw)

    def register_builtin_function(
        self, hinglish_fn: str, python_fn: str, aliases: Optional[List[str]] = None
    ) -> None:
        """Register a built-in function (e.g. dikhao -> print)."""
        self._hinglish_to_python[hinglish_fn] = python_fn
        self._builtin_functions.add(hinglish_fn)
        if python_fn not in self._python_to_hinglish:
            self._python_to_hinglish[python_fn] = hinglish_fn

        if aliases:
            for alias in aliases:
                self.register_alias(alias, hinglish_fn)

    def register_alias(self, alias: str, canonical_hinglish: str) -> None:
        """Register an alias pointing to a canonical Hinglish word."""
        if canonical_hinglish not in self._hinglish_to_python:
            raise ValueError(
                f"Cannot register alias '{alias}' for unknown keyword '{canonical_hinglish}'"
            )
        py_target = self._hinglish_to_python[canonical_hinglish]
        self._hinglish_to_python[alias] = py_target
        self._alias_to_canonical[alias] = canonical_hinglish

        if canonical_hinglish in self._statement_keywords:
            self._statement_keywords.add(alias)
        elif canonical_hinglish in self._literal_keywords:
            self._literal_keywords.add(alias)
        elif canonical_hinglish in self._builtin_functions:
            self._builtin_functions.add(alias)

    def get_python_equivalent(self, word: str) -> Optional[str]:
        """Returns the Python keyword/name for a given Hinglish word, or None."""
        return self._hinglish_to_python.get(word)

    def get_canonical_hinglish(self, word: str) -> str:
        """Returns the canonical Hinglish keyword, resolving any aliases."""
        return self._alias_to_canonical.get(word, word)

    def get_primary_hinglish(self, python_kw: str) -> Optional[str]:
        """Returns the primary canonical Hinglish keyword for a Python keyword."""
        return self._python_to_hinglish.get(python_kw)

    def is_keyword(self, word: str) -> bool:
        """Checks if a word is any recognized Hinglish keyword, literal, or builtin."""
        return word in self._hinglish_to_python

    def is_statement_keyword(self, word: str) -> bool:
        """Checks if a word is a statement/control-flow keyword."""
        return word in self._statement_keywords

    def is_literal_keyword(self, word: str) -> bool:
        """Checks if a word is a literal keyword (sahi, galat, kuch_nahi)."""
        return word in self._literal_keywords

    def is_builtin_function(self, word: str) -> bool:
        """Checks if a word is a built-in function name (e.g., dikhao)."""
        return word in self._builtin_functions

    def all_hinglish_words(self) -> Set[str]:
        """Returns all recognized Hinglish words in the registry."""
        return set(self._hinglish_to_python.keys())


# Default globally accessible registry
DEFAULT_KEYWORD_REGISTRY = KeywordRegistry()
