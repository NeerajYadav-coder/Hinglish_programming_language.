"""Parser package for the Hinglish programming language."""

from abc import ABC, abstractmethod
from typing import List, Optional, Union

from ..ast.nodes import Program
from ..keywords import KeywordRegistry
from ..lexer import tokenize
from ..lexer.tokens import Token
from .parser import HinglishParser


class BaseParser(ABC):
    """Abstract interface for Hinglish syntax parsers."""

    @abstractmethod
    def parse(self, tokens: List[Token]) -> Program:
        """Parse a sequence of tokens into a Hinglish AST Program node."""
        pass


def parse(
    source_or_tokens: Union[str, List[Token]],
    registry: Optional[KeywordRegistry] = None,
) -> Program:
    """Convenience helper to parse Hinglish source code or token list into an AST Program."""
    if isinstance(source_or_tokens, str):
        source_code = source_or_tokens
        tokens = tokenize(source_code, registry=registry)
    else:
        source_code = None
        tokens = source_or_tokens

    parser = HinglishParser(tokens=tokens, registry=registry, source_code=source_code)
    return parser.parse()


__all__ = ["BaseParser", "HinglishParser", "parse"]
