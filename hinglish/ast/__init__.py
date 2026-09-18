"""Hinglish Abstract Syntax Tree (AST) node definitions.

Defines the base classes for syntactic statements and expressions in Hinglish.
"""

from abc import ABC
from dataclasses import dataclass, field
from typing import List, Optional

from ..lexer.tokens import Position


@dataclass
class ASTNode(ABC):
    """Base class for all Hinglish AST nodes."""

    start_pos: Optional[Position] = None
    end_pos: Optional[Position] = None


@dataclass
class Statement(ASTNode):
    """Base class for statement nodes."""
    pass


@dataclass
class Expression(ASTNode):
    """Base class for expression nodes."""
    pass


@dataclass
class Program(ASTNode):
    """Root node of a Hinglish program."""

    body: List[Statement] = field(default_factory=list)


__all__ = ["ASTNode", "Statement", "Expression", "Program"]
