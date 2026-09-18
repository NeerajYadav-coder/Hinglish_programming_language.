"""Lexer package for the Hinglish programming language."""

from abc import ABC, abstractmethod
from typing import List

from .tokens import Position, Token, TokenType


class BaseLexer(ABC):
    """Abstract interface for Hinglish lexers."""

    @abstractmethod
    def tokenize(self, source_code: str) -> List[Token]:
        """Tokenize Hinglish source code into a list of Tokens."""
        pass


__all__ = ["TokenType", "Token", "Position", "BaseLexer"]
