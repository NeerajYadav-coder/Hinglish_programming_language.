"""Concrete Abstract Syntax Tree (AST) node definitions for Hinglish."""

from abc import ABC
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple

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


# -----------------------------------------------------------------------------
# Program / Module
# -----------------------------------------------------------------------------


@dataclass
class Program(ASTNode):
    """Root node representing an entire Hinglish program / module."""

    body: List[Statement] = field(default_factory=list)


# -----------------------------------------------------------------------------
# Statements
# -----------------------------------------------------------------------------


@dataclass
class ExpressionStatement(Statement):
    """A statement consisting of a single expression (e.g. function call)."""

    expr: Expression = field(default_factory=Expression)


@dataclass
class Assignment(Statement):
    """Assignment statement (e.g. x = 10, x += 5)."""

    target: Expression = field(default_factory=Expression)
    op: str = "="
    value: Expression = field(default_factory=Expression)


@dataclass
class ElifClause(ASTNode):
    """An elif branch in an if statement."""

    condition: Expression = field(default_factory=Expression)
    body: List[Statement] = field(default_factory=list)


@dataclass
class If(Statement):
    """Conditional statement: agar <cond>: <body> [warna_agar ...]* [warna: ...]"""

    condition: Expression = field(default_factory=Expression)
    body: List[Statement] = field(default_factory=list)
    elif_clauses: List[ElifClause] = field(default_factory=list)
    else_body: Optional[List[Statement]] = None


@dataclass
class While(Statement):
    """While loop: jabtak <cond>: <body>"""

    condition: Expression = field(default_factory=Expression)
    body: List[Statement] = field(default_factory=list)


@dataclass
class For(Statement):
    """For loop: har <target> mein <iterable>: <body>"""

    target: Expression = field(default_factory=Expression)
    iterable: Expression = field(default_factory=Expression)
    body: List[Statement] = field(default_factory=list)


@dataclass
class FunctionDefinition(Statement):
    """Function definition: kaam <name>(<params>): <body>"""

    name: str = ""
    params: List[str] = field(default_factory=list)
    body: List[Statement] = field(default_factory=list)


@dataclass
class Return(Statement):
    """Return statement: wapas [<value>]"""

    value: Optional[Expression] = None


@dataclass
class Pass(Statement):
    """No-op statement: chhod_do"""
    pass


@dataclass
class Break(Statement):
    """Break loop statement: ruko"""
    pass


@dataclass
class Continue(Statement):
    """Continue loop statement: aage_bado"""
    pass


@dataclass
class Import(Statement):
    """Import statement: laao <module> [jaise <alias>]"""

    names: List[Tuple[str, Optional[str]]] = field(default_factory=list)


@dataclass
class FromImport(Statement):
    """From import statement: se <module> laao <name> [jaise <alias>]"""

    module: str = ""
    names: List[Tuple[str, Optional[str]]] = field(default_factory=list)


# -----------------------------------------------------------------------------
# Expressions
# -----------------------------------------------------------------------------


@dataclass
class Identifier(Expression):
    """Variable or symbol name."""

    name: str = ""


@dataclass
class Integer(Expression):
    """Integer literal value."""

    value: int = 0


@dataclass
class Float(Expression):
    """Floating point literal value."""

    value: float = 0.0


@dataclass
class Complex(Expression):
    """Complex number literal value."""

    value: complex = 0j


@dataclass
class String(Expression):
    """String literal value."""

    value: str = ""
    prefix: Optional[str] = None


@dataclass
class Boolean(Expression):
    """Boolean literal value (sahi -> True, galat -> False)."""

    value: bool = False


@dataclass
class NoneLiteral(Expression):
    """None / Null literal value (kuch_nahi / shunya)."""

    value: Any = None


@dataclass
class ListLiteral(Expression):
    """List literal [elem1, elem2, ...]."""

    elements: List[Expression] = field(default_factory=list)


@dataclass
class DictLiteral(Expression):
    """Dictionary literal {key1: val1, key2: val2}."""

    keys: List[Expression] = field(default_factory=list)
    values: List[Expression] = field(default_factory=list)


@dataclass
class TupleLiteral(Expression):
    """Tuple literal (elem1, elem2, ...)."""

    elements: List[Expression] = field(default_factory=list)


@dataclass
class BinaryOperation(Expression):
    """Binary operation: left op right (e.g. x + y, a * b)."""

    left: Expression = field(default_factory=Expression)
    op: str = ""
    right: Expression = field(default_factory=Expression)


@dataclass
class UnaryOperation(Expression):
    """Unary operation: op operand (e.g. -x, +y, ~z)."""

    op: str = ""
    operand: Expression = field(default_factory=Expression)


@dataclass
class Comparison(Expression):
    """Comparison expression: left op right (e.g. x == y, a > b)."""

    left: Expression = field(default_factory=Expression)
    op: str = ""
    right: Expression = field(default_factory=Expression)


@dataclass
class BooleanOperation(Expression):
    """Logical boolean operation: left 'aur'/'ya' right."""

    op: str = ""
    values: List[Expression] = field(default_factory=list)


@dataclass
class FunctionCall(Expression):
    """Function call expression: func(arg1, arg2, kw=val)."""

    func: Expression = field(default_factory=Expression)
    args: List[Expression] = field(default_factory=list)
    keywords: Dict[str, Expression] = field(default_factory=dict)


@dataclass
class AttributeAccess(Expression):
    """Attribute access: value.attr (e.g. obj.method)."""

    value: Expression = field(default_factory=Expression)
    attr: str = ""


@dataclass
class Indexing(Expression):
    """Indexing or subscript: value[index]."""

    value: Expression = field(default_factory=Expression)
    index: Expression = field(default_factory=Expression)


@dataclass
class Slice(Expression):
    """Slice expression inside subscript: [lower:upper:step]."""

    lower: Optional[Expression] = None
    upper: Optional[Expression] = None
    step: Optional[Expression] = None
