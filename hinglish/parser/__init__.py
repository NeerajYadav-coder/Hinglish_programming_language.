"""Parser package for the Hinglish programming language."""

from abc import ABC, abstractmethod
from typing import List

from ..ast import Program
from ..lexer.tokens import Token


class BaseParser(ABC):
    """Abstract interface for Hinglish syntax parsers."""

    @abstractmethod
    def parse(self, tokens: List[Token]) -> Program:
        """Parse a sequence of tokens into a Hinglish AST Program node."""
        pass


__all__ = ["BaseParser"]
