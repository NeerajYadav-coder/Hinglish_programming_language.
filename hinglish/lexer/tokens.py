"""Token definitions and data structures for the Hinglish Lexer."""

from dataclasses import dataclass
from enum import Enum, auto
from typing import Any, Optional


class TokenType(Enum):
    """Complete enumeration of token types for Hinglish and Python compatibility."""

    # Keywords & Identifiers
    KEYWORD = auto()
    IDENTIFIER = auto()

    # Literals
    INTEGER = auto()
    FLOAT = auto()
    COMPLEX = auto()
    STRING = auto()
    BOOLEAN = auto()
    NONE = auto()

    # Arithmetic Operators
    PLUS = auto()               # +
    MINUS = auto()              # -
    STAR = auto()               # *
    SLASH = auto()              # /
    DOUBLE_SLASH = auto()       # //
    PERCENT = auto()            # %
    STAR_STAR = auto()          # **
    AT = auto()                 # @

    # Bitwise Operators
    AMPERSAND = auto()          # &
    PIPE = auto()               # |
    CARET = auto()              # ^
    TILDE = auto()              # ~
    LSHIFT = auto()             # <<
    RSHIFT = auto()             # >>

    # Comparison Operators
    EQ = auto()                 # ==
    NE = auto()                 # !=
    LT = auto()                 # <
    GT = auto()                 # >
    LE = auto()                 # <=
    GE = auto()                 # >=

    # Assignment & Augmented Assignments
    ASSIGN = auto()             # =
    PLUS_ASSIGN = auto()        # +=
    MINUS_ASSIGN = auto()       # -=
    STAR_ASSIGN = auto()        # *=
    SLASH_ASSIGN = auto()       # /=
    DOUBLE_SLASH_ASSIGN = auto()# //=
    PERCENT_ASSIGN = auto()     # %=
    STAR_STAR_ASSIGN = auto()   # **=
    AT_ASSIGN = auto()          # @=
    AMPERSAND_ASSIGN = auto()   # &=
    PIPE_ASSIGN = auto()        # |=
    CARET_ASSIGN = auto()       # ^=
    LSHIFT_ASSIGN = auto()      # <<=
    RSHIFT_ASSIGN = auto()      # >>=
    WALRUS = auto()             # :=

    # Delimiters & Punctuation
    COLON = auto()              # :
    COMMA = auto()              # ,
    SEMICOLON = auto()          # ;
    DOT = auto()                # .
    ARROW = auto()              # ->
    ELLIPSIS = auto()           # ...
    LPAREN = auto()             # (
    RPAREN = auto()             # )
    LBRACKET = auto()           # [
    RBRACKET = auto()           # ]
    LBRACE = auto()             # {
    RBRACE = auto()             # }

    # Layout & Indentation
    NEWLINE = auto()
    INDENT = auto()
    DEDENT = auto()

    # Special
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
