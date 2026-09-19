"""Hinglish Programming Language Package.

A Python-compatible programming language interface using Hinglish/Hindi-style syntax.
"""

__version__ = "1.0.0"
__author__ = "Neeraj Yadav"

from .compiler import compile
from .formatter import format_source
from .keywords import DEFAULT_KEYWORD_REGISTRY, KeywordRegistry
from .lexer import tokenize
from .parser import parse
from .runtime import HinglishREPL, run, run_file, start_repl

__all__ = [
    "DEFAULT_KEYWORD_REGISTRY",
    "KeywordRegistry",
    "HinglishREPL",
    "compile",
    "format_source",
    "parse",
    "run",
    "run_file",
    "start_repl",
    "tokenize",
    "__version__",
]
