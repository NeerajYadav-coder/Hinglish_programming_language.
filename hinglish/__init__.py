"""Hinglish Programming Language Package.

A Python-compatible programming language interface using Hinglish/Hindi-style syntax.
"""

__version__ = "0.1.0"
__author__ = "Hinglish Language Contributors"

from .keywords import DEFAULT_KEYWORD_REGISTRY, KeywordRegistry

__all__ = ["DEFAULT_KEYWORD_REGISTRY", "KeywordRegistry", "__version__"]
