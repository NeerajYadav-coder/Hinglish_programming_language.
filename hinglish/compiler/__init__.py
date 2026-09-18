"""Compiler and lowering package for the Hinglish programming language."""

from abc import ABC, abstractmethod
from typing import Any

from ..ast import Program


class BaseCompiler(ABC):
    """Abstract interface for compiling Hinglish AST into Python targets."""

    @abstractmethod
    def compile(self, program: Program) -> Any:
        """Compile a Hinglish AST into a target representation (Python AST or source string)."""
        pass


__all__ = ["BaseCompiler"]
