"""Configurable Keyword Registry for Hinglish.

This module defines the vocabulary mapping between Hinglish keywords/builtins
and their Python target equivalents. The registry is designed to be configurable
and extensible so vocabulary can easily scale to full Python language coverage
without requiring changes to the core lexer or parser mechanics.
"""

from typing import Dict, List, Optional, Set


class KeywordRegistry:
    """Registry maintaining bidirectional mapping, categorization, and aliases for Hinglish vocabulary."""

    def __init__(self) -> None:
        # Maps Hinglish token string -> Python equivalent
        self._hinglish_to_python: Dict[str, str] = {}

        # Maps Python target keyword -> Primary canonical Hinglish keyword
        self._python_to_hinglish: Dict[str, str] = {}

        # Maps alias -> Canonical Hinglish keyword
        self._alias_to_canonical: Dict[str, str] = {}

        # Categorized sets
        self._statement_keywords: Set[str] = set()
        self._operator_keywords: Set[str] = set()
        self._literal_keywords: Set[str] = set()
        self._builtin_functions: Set[str] = set()
        self._soft_keywords: Set[str] = set()

        self._load_defaults()

    def _load_defaults(self) -> None:
        """Loads default keyword specifications across major Python capabilities."""
        # 1. Control Flow & Loops
        control_flow = [
            ("agar", "if"),
            ("warna", "else"),
            ("warna_agar", "elif"),
            ("jabtak", "while"),
            ("har", "for"),
            ("mein", "in"),
            ("ruko", "break"),
            ("aage_bado", "continue"),
            ("chhod_do", "pass"),
        ]
        for hin_kw, py_kw in control_flow:
            self.register_statement_keyword(hin_kw, py_kw)

        # 2. Functions, Classes & OOP
        oop_and_functions = [
            ("kaam", "def"),
            ("varg", "class"),
            ("wapas", "return"),
            ("upaj", "yield"),
            ("sookshm", "lambda"),
        ]
        for hin_kw, py_kw in oop_and_functions:
            self.register_statement_keyword(hin_kw, py_kw)

        # 3. Exception Handling
        exceptions = [
            ("koshish", "try"),
            ("pakdo", "except"),
            ("antatah", "finally"),
            ("uthav", "raise"),
            ("daawa", "assert"),
        ]
        for hin_kw, py_kw in exceptions:
            self.register_statement_keyword(hin_kw, py_kw)

        # 4. Context Managers & Scope
        context_and_scope = [
            ("saath", "with"),
            ("jaise", "as"),
            ("sarvavyapi", "global"),
            ("asthanik", "nonlocal"),
            ("hatao", "del"),
        ]
        for hin_kw, py_kw in context_and_scope:
            self.register_statement_keyword(hin_kw, py_kw)

        # 5. Modules & Imports
        imports = [
            ("laao", "import"),
            ("se", "from"),
        ]
        for hin_kw, py_kw in imports:
            self.register_statement_keyword(hin_kw, py_kw)

        # 6. Asynchronous Programming
        async_keywords = [
            ("asamanantar", "async"),
            ("intezaar", "await"),
        ]
        for hin_kw, py_kw in async_keywords:
            self.register_statement_keyword(hin_kw, py_kw)

        # 7. Pattern Matching (Soft keywords)
        soft_keywords = [
            ("milao", "match"),
            ("sthiti", "case"),
        ]
        for hin_kw, py_kw in soft_keywords:
            self.register_soft_keyword(hin_kw, py_kw)

        # 8. Logical & Identity Operators
        logical_ops = [
            ("aur", "and"),
            ("ya", "or"),
            ("nahi", "not"),
            ("hai", "is"),
        ]
        for hin_op, py_op in logical_ops:
            self.register_operator_keyword(hin_op, py_op)

        # 9. Literal Values
        literals = [
            ("sahi", "True"),
            ("galat", "False"),
            ("kuch_nahi", "None"),
        ]
        for hin_lit, py_lit in literals:
            self.register_literal_keyword(hin_lit, py_lit)

        # 10. Built-in Core Functions
        builtins = [
            ("dikhao", "print"),
            ("pucho", "input"),
            ("lambai", "len"),
            ("prakar", "type"),
            ("kram", "range"),
            ("purnank", "int"),
            ("dashamlav", "float"),
            ("akshar", "str"),
            ("kul_jod", "sum"),
            ("adhiktam", "max"),
            ("nyuntam", "min"),
            ("khol", "open"),
        ]
        for hin_fn, py_fn in builtins:
            self.register_builtin_function(hin_fn, py_fn)

        # 11. Aliases & Synonyms
        self.register_alias("andar", "mein")          # 'har x andar y'
        self.register_alias("shunya", "kuch_nahi")    # 'shunya' -> None
        self.register_alias("chapo", "dikhao")        # 'chapo' -> print
        self.register_alias("batao", "dikhao")        # 'batao' -> print
        self.register_alias("shreni", "varg")         # 'shreni' -> class
        self.register_alias("sambhalo", "pakdo")      # 'sambhalo' -> except
        self.register_alias("aakhir_mein", "antatah") # 'aakhir_mein' -> finally
        self.register_alias("fenko", "uthav")         # 'fenko' -> raise
        self.register_alias("lekar", "saath")         # 'lekar' -> with
        self.register_alias("roop_mein", "jaise")     # 'roop_mein' -> as
        self.register_alias("aayat", "laao")          # 'aayat' -> import
        self.register_alias("mitao", "hatao")         # 'mitao' -> del
        self.register_alias("milaao", "milao")        # 'milaao' -> match
        self.register_alias("vichaar", "sthiti")      # 'vichaar' -> case

    def register_statement_keyword(
        self, hinglish_kw: str, python_kw: str, aliases: Optional[List[str]] = None
    ) -> None:
        """Register a statement keyword."""
        self._hinglish_to_python[hinglish_kw] = python_kw
        self._statement_keywords.add(hinglish_kw)
        if python_kw not in self._python_to_hinglish:
            self._python_to_hinglish[python_kw] = hinglish_kw
        if aliases:
            for alias in aliases:
                self.register_alias(alias, hinglish_kw)

    def register_operator_keyword(
        self, hinglish_op: str, python_op: str, aliases: Optional[List[str]] = None
    ) -> None:
        """Register an operator keyword (e.g. aur -> and)."""
        self._hinglish_to_python[hinglish_op] = python_op
        self._operator_keywords.add(hinglish_op)
        if python_op not in self._python_to_hinglish:
            self._python_to_hinglish[python_op] = hinglish_op
        if aliases:
            for alias in aliases:
                self.register_alias(alias, hinglish_op)

    def register_literal_keyword(
        self, hinglish_kw: str, python_kw: str, aliases: Optional[List[str]] = None
    ) -> None:
        """Register a literal keyword (e.g. sahi -> True)."""
        self._hinglish_to_python[hinglish_kw] = python_kw
        self._literal_keywords.add(hinglish_kw)
        if python_kw not in self._python_to_hinglish:
            self._python_to_hinglish[python_kw] = hinglish_kw
        if aliases:
            for alias in aliases:
                self.register_alias(alias, hinglish_kw)

    def register_soft_keyword(
        self, hinglish_kw: str, python_kw: str, aliases: Optional[List[str]] = None
    ) -> None:
        """Register a soft keyword (e.g. milao -> match, sthiti -> case)."""
        self._hinglish_to_python[hinglish_kw] = python_kw
        self._soft_keywords.add(hinglish_kw)
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
        elif canonical_hinglish in self._operator_keywords:
            self._operator_keywords.add(alias)
        elif canonical_hinglish in self._literal_keywords:
            self._literal_keywords.add(alias)
        elif canonical_hinglish in self._soft_keywords:
            self._soft_keywords.add(alias)
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
        """Checks if a word is any recognized Hinglish keyword, literal, operator, or builtin."""
        return word in self._hinglish_to_python

    def is_statement_keyword(self, word: str) -> bool:
        """Checks if a word is a statement/control-flow keyword."""
        return word in self._statement_keywords

    def is_operator_keyword(self, word: str) -> bool:
        """Checks if a word is an operator keyword (aur, ya, nahi, hai)."""
        return word in self._operator_keywords

    def is_literal_keyword(self, word: str) -> bool:
        """Checks if a word is a literal keyword (sahi, galat, kuch_nahi)."""
        return word in self._literal_keywords

    def is_soft_keyword(self, word: str) -> bool:
        """Checks if a word is a soft keyword (milao, sthiti)."""
        return word in self._soft_keywords

    def is_builtin_function(self, word: str) -> bool:
        """Checks if a word is a built-in function name (e.g., dikhao)."""
        return word in self._builtin_functions

    def all_hinglish_words(self) -> Set[str]:
        """Returns all recognized Hinglish words in the registry."""
        return set(self._hinglish_to_python.keys())


# Default globally accessible registry
DEFAULT_KEYWORD_REGISTRY = KeywordRegistry()
