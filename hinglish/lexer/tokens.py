"""Token definitions and data structures for the Hinglish Lexer."""

from dataclasses import dataclass
from enum import Enum, auto
from typing import Any, Optional


class TokenType(Enum):
    """Enumeration of token types in Hinglish."""

    # Keywords & Literals
    KEYWORD = auto()
    IDENTIFIER = auto()
    NUMBER = auto()
    STRING = auto()
    BOOLEAN = auto()
    NONE = auto()

    # Operators & Delimiters
    OPERATOR = auto()
    ASSIGN = auto()         # =
    COLON = auto()          # :
    COMMA = auto()          # ,
    LPAREN = auto()         # (
    RPAREN = auto()         # )
    LBRACKET = auto()       # [
    RBRACKET = auto()       # ]
    LBRACE = auto()         # {
    RBRACE = auto()         # }
    DOT = auto()            # .

    # Layout & Indentation
    NEWLINE = auto()
    INDENT = auto()
    DEDENT = auto()

    # Special / End-of-Stream
    COMMENT = auto()
    EOF = auto()


@dataclass(frozen=True)
class Position:
    """Source position coordinates for error reporting."""

    line: int
    column: int

    def __str__(self) -> str:
        return f"{self.line}:{self.column}"


@dataclass(frozen=True)
class Token:
    """Represents a lexical token in a Hinglish source file."""

    type: TokenType
    value: Any
    start_pos: Position
    end_pos: Position
    raw_text: Optional[str] = None

    def __repr__(self) -> str:
        return (
            f"Token({self.type.name}, value={self.value!r}, "
            f"pos={self.start_pos})"
        )
