"""Lexer package for the Hinglish programming language."""

from typing import List, Optional

from ..keywords import KeywordRegistry
from .lexer import HinglishLexer
from .tokens import Position, Token, TokenType


class BaseLexer:
    """Abstract interface for Hinglish lexers."""

    def tokenize(self, source_code: str) -> List[Token]:
        """Tokenize Hinglish source code into a list of Tokens."""
        raise NotImplementedError


def tokenize(
    source_code: str,
    registry: Optional[KeywordRegistry] = None,
    include_comments: bool = False,
) -> List[Token]:
    """Convenience helper to tokenize Hinglish source code."""
    lexer = HinglishLexer(registry=registry, include_comments=include_comments)
    return lexer.tokenize(source_code)


__all__ = [
    "TokenType",
    "Token",
    "Position",
    "BaseLexer",
    "HinglishLexer",
    "tokenize",
]
