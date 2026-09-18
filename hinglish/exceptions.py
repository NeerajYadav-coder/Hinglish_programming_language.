"""Exception classes for the Hinglish language pipeline."""

from typing import Optional


class HinglishError(Exception):
    """Base exception for all Hinglish language pipeline errors."""

    def __init__(
        self,
        message: str,
        line: Optional[int] = None,
        column: Optional[int] = None,
        source_line: Optional[str] = None,
    ) -> None:
        self.message = message
        self.line = line
        self.column = column
        self.source_line = source_line
        super().__init__(self._format_message())

    def _format_message(self) -> str:
        loc = ""
        if self.line is not None:
            col_str = f":{self.column}" if self.column is not None else ""
            loc = f" (line {self.line}{col_str})"
        msg = f"{self.__class__.__name__}{loc}: {self.message}"
        if self.source_line:
            msg += f"\n  {self.source_line.strip()}"
            if self.column is not None and self.column > 0:
                msg += f"\n  {' ' * (self.column - 1)}^"
        return msg


class HinglishLexerError(HinglishError):
    """Raised when the lexer encounters invalid syntax or malformed tokens."""
    pass


class HinglishIndentationError(HinglishLexerError):
    """Raised when an indentation inconsistency or invalid dedent occurs."""
    pass


class HinglishSyntaxError(HinglishError):
    """Raised when the parser encounters a grammatical syntax error."""
    pass
