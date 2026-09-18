"""Compiler and lowering package for the Hinglish programming language."""

from abc import ABC, abstractmethod
from typing import Any, Optional, Union

from ..ast.nodes import Program
from ..keywords import KeywordRegistry
from ..parser import parse
from .compiler import HinglishCompiler


class BaseCompiler(ABC):
    """Abstract interface for compiling Hinglish AST into Python targets."""

    @abstractmethod
    def compile(self, program: Program) -> Any:
        """Compile a Hinglish AST into a target representation (Python AST or source string)."""
        pass


def compile(
    source_or_ast: Union[str, Program],
    registry: Optional[KeywordRegistry] = None,
) -> str:
    """Convenience helper to compile Hinglish source code or AST Program into validated Python 3 source."""
    if isinstance(source_or_ast, str):
        program_ast = parse(source_or_ast, registry=registry)
    else:
        program_ast = source_or_ast

    compiler = HinglishCompiler(registry=registry)
    return compiler.compile(program_ast)


__all__ = ["BaseCompiler", "HinglishCompiler", "compile"]
