"""Hinglish Programming Language Package.

A Python-compatible programming language interface using Hinglish/Hindi-style syntax.
"""

__version__ = "0.1.0"
__author__ = "Hinglish Language Contributors"

from .compiler import compile
from .keywords import DEFAULT_KEYWORD_REGISTRY, KeywordRegistry
from .lexer import tokenize
from .parser import parse
from .runtime import HinglishREPL, run, run_file, start_repl

__all__ = [
    "DEFAULT_KEYWORD_REGISTRY",
    "KeywordRegistry",
    "HinglishREPL",
    "compile",
    "parse",
    "run",
    "run_file",
    "start_repl",
    "tokenize",
    "__version__",
]
