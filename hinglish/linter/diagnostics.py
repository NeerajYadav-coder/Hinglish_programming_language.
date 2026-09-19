"""Diagnostic data structures and severity levels for Hinglish Static Analysis."""

from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, Optional


class Severity(str, Enum):
    """Diagnostic severity levels matching standard editor and compiler conventions."""

    ERROR = "error"
    WARNING = "warning"
    INFO = "info"

    def __str__(self) -> str:
        return self.value


@dataclass
class Diagnostic:
    """Represents a single static analysis finding in a Hinglish source file."""

    rule_id: str
    message: str
    severity: str
    line: int
    column: int
    end_line: Optional[int] = None
    end_column: Optional[int] = None
    filename: Optional[str] = None

    def __post_init__(self) -> None:
        if isinstance(self.severity, Severity):
            self.severity = self.severity.value

    def format_cli(self) -> str:
        """Formats the diagnostic for human-readable command-line output.
        
        Example:
            main.hin:7:5: warning H002: variable 'age' is assigned but never used
        """
        fn = self.filename or "<source>"
        return f"{fn}:{self.line}:{self.column}: {self.severity} {self.rule_id}: {self.message}"

    def to_dict(self) -> Dict[str, Any]:
        """Serializes the diagnostic to a machine-readable dictionary."""
        return {
            "rule_id": self.rule_id,
            "message": self.message,
            "severity": self.severity,
            "line": self.line,
            "column": self.column,
            "end_line": self.end_line or self.line,
            "end_column": self.end_column or self.column,
            "filename": self.filename,
        }

    def __lt__(self, other: "Diagnostic") -> bool:
        """Deterministic ordering for sorting diagnostics by file, location, and rule."""
        if not isinstance(other, Diagnostic):
            return NotImplemented
        return (
            self.filename or "",
            self.line,
            self.column,
            self.rule_id,
            self.message,
        ) < (
            other.filename or "",
            other.line,
            other.column,
            other.rule_id,
            other.message,
        )
