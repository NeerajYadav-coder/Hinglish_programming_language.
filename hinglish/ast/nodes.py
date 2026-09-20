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
    """For loop: har [intezaar] <target> mein <iterable>: <body>"""

    target: Expression = field(default_factory=Expression)
    iterable: Expression = field(default_factory=Expression)
    body: List[Statement] = field(default_factory=list)
    is_async: bool = False


@dataclass
class Parameter(ASTNode):
    """Function parameter metadata."""

    name: str = ""
    annotation: Optional[Expression] = None
    default: Optional[Expression] = None
    kind: str = "POSITIONAL_OR_KEYWORD"


@dataclass
class FunctionDefinition(Statement):
    """Function definition: [asamanantar] kaam <name>(<params>) [-> <ret>]: <body>"""

    name: str = ""
    params: List[str] = field(default_factory=list)
    body: List[Statement] = field(default_factory=list)
    decorators: List[Expression] = field(default_factory=list)
    is_async: bool = False
    parameters: List[Parameter] = field(default_factory=list)
    returns: Optional[Expression] = None


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
class Global(Statement):
    """Global statement: sarvavyapi <name1> [, <name2>]*"""

    names: List[str] = field(default_factory=list)


@dataclass
class Nonlocal(Statement):
    """Nonlocal statement: asthaniya <name1> [, <name2>]*"""

    names: List[str] = field(default_factory=list)


@dataclass
class Assert(Statement):
    """Assert statement: dawa <test> [, <msg>]"""

    test: Expression = field(default_factory=Expression)
    msg: Optional[Expression] = None


@dataclass
class Delete(Statement):
    """Delete statement: mitao <target1> [, <target2>]*"""

    targets: List[Expression] = field(default_factory=list)


@dataclass
class Import(Statement):
    """Import statement: laao <module> [jaise <alias>]"""

    names: List[Tuple[str, Optional[str]]] = field(default_factory=list)


@dataclass
class FromImport(Statement):
    """From import statement: se <module> laao <name> [jaise <alias>]"""

    module: str = ""
    names: List[Tuple[str, Optional[str]]] = field(default_factory=list)


@dataclass
class ClassDefinition(Statement):
    """Class definition: varg <name>[(<bases>)]: <body>"""

    name: str = ""
    bases: List[Expression] = field(default_factory=list)
    body: List[Statement] = field(default_factory=list)
    decorators: List[Expression] = field(default_factory=list)


@dataclass
class ExceptHandler(ASTNode):
    """Exception handler clause: pakdo [*] [<type>] [jaise <name>]: <body>"""

    type: Optional[Expression] = None
    name: Optional[str] = None
    body: List[Statement] = field(default_factory=list)
    is_star: bool = False


@dataclass
class Try(Statement):
    """Try block: koshish: <body> [pakdo ...]* [warna: ...] [antatah: ...]"""

    body: List[Statement] = field(default_factory=list)
    handlers: List[ExceptHandler] = field(default_factory=list)
    else_body: Optional[List[Statement]] = None
    finally_body: Optional[List[Statement]] = None


@dataclass
class Raise(Statement):
    """Raise exception statement: uthav [<exc>]"""

    exc: Optional[Expression] = None


@dataclass
class WithItem(ASTNode):
    """Single context manager item: <context_expr> [jaise <optional_vars>]"""

    context_expr: Expression = field(default_factory=Expression)
    optional_vars: Optional[Expression] = None


@dataclass
class With(Statement):
    """Context manager statement: saath [intezaar] <item1>, <item2>: <body>"""

    items: List[WithItem] = field(default_factory=list)
    body: List[Statement] = field(default_factory=list)
    is_async: bool = False


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
    raw_text: Optional[str] = None


@dataclass
class Float(Expression):
    """Floating point literal value."""

    value: float = 0.0
    raw_text: Optional[str] = None


@dataclass
class Complex(Expression):
    """Complex number literal value."""

    value: complex = 0j
    raw_text: Optional[str] = None


@dataclass
class String(Expression):
    """String literal value."""

    value: str = ""
    prefix: Optional[str] = None
    raw_text: Optional[str] = None


@dataclass
class FormattedValue(Expression):
    """Formatted value within an f-string: {value[!conversion][:format_spec]}."""

    value: Expression = field(default_factory=Expression)
    conversion: Optional[str] = None
    format_spec: Optional[str] = None


@dataclass
class JoinedStr(Expression):
    """F-string consisting of string literals and formatted values: f"..."."""

    parts: List[Expression] = field(default_factory=list)
    raw_text: Optional[str] = None


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
class IfExp(Expression):
    """Inline conditional expression: body 'agar' condition 'warna' orelse (e.g. x agar cond warna y)."""

    body: Expression = field(default_factory=Expression)
    condition: Expression = field(default_factory=Expression)
    orelse: Expression = field(default_factory=Expression)

    @property
    def test(self) -> Expression:
        return self.condition

    @property
    def true_expression(self) -> Expression:
        return self.body

    @property
    def false_expression(self) -> Expression:
        return self.orelse


ConditionalExpression = IfExp


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


# -----------------------------------------------------------------------------
# Comprehensions, Lambda & Generator AST Nodes (Step 7)
# -----------------------------------------------------------------------------


@dataclass
class ComprehensionClause(ASTNode):
    """A 'for ... in ... [if ...]*' or 'async for ... in ... [if ...]*' clause in a comprehension."""

    target: Expression = field(default_factory=Expression)
    iterable: Expression = field(default_factory=Expression)
    conditions: List[Expression] = field(default_factory=list)
    is_async: bool = False


@dataclass
class ListComprehension(Expression):
    """List comprehension: [elt for ... in ... if ...]"""

    element: Expression = field(default_factory=Expression)
    clauses: List[ComprehensionClause] = field(default_factory=list)


@dataclass
class DictComprehension(Expression):
    """Dict comprehension: {key: value for ... in ... if ...]"""

    key: Expression = field(default_factory=Expression)
    value: Expression = field(default_factory=Expression)
    clauses: List[ComprehensionClause] = field(default_factory=list)


@dataclass
class SetComprehension(Expression):
    """Set comprehension: {elt for ... in ... if ...]"""

    element: Expression = field(default_factory=Expression)
    clauses: List[ComprehensionClause] = field(default_factory=list)


@dataclass
class GeneratorExpression(Expression):
    """Generator expression: (elt for ... in ... if ...)"""

    element: Expression = field(default_factory=Expression)
    clauses: List[ComprehensionClause] = field(default_factory=list)


@dataclass
class SetLiteral(Expression):
    """Set literal {elem1, elem2, ...}."""

    elements: List[Expression] = field(default_factory=list)


@dataclass
class LambdaExpression(Expression):
    """Anonymous lambda function: sookshm [<params>]: <body>"""

    params: List[str] = field(default_factory=list)
    body: Expression = field(default_factory=Expression)


@dataclass
class Yield(Expression):
    """Yield expression or statement: upaj [<value>]"""

    value: Optional[Expression] = None


@dataclass
class YieldFrom(Expression):
    """Yield from expression or statement: upaj se <value>"""

    value: Expression = field(default_factory=Expression)


# -----------------------------------------------------------------------------
# Step 8: Async, Advanced Syntax, Annotations & Pattern Matching AST Nodes
# -----------------------------------------------------------------------------


@dataclass
class AnnAssign(Statement):
    """Annotated variable assignment: <target>: <annotation> [= <value>]"""

    target: Expression = field(default_factory=Expression)
    annotation: Expression = field(default_factory=Expression)
    value: Optional[Expression] = None


@dataclass
class Await(Expression):
    """Await expression: intezaar <value>"""

    value: Expression = field(default_factory=Expression)


@dataclass
class AssignmentExpression(Expression):
    """Walrus assignment expression: (<target> := <value>)"""

    target: Expression = field(default_factory=Expression)
    value: Expression = field(default_factory=Expression)


@dataclass
class Starred(Expression):
    """Starred expression: *<value>"""

    value: Expression = field(default_factory=Expression)


@dataclass
class DoubleStarred(Expression):
    """Double-starred mapping unpack expression: **<value>"""

    value: Expression = field(default_factory=Expression)


@dataclass
class MatchPattern(ASTNode):
    """Base class for structural pattern matching patterns."""
    pass


@dataclass
class MatchValue(MatchPattern):
    """Literal or value pattern in match-case."""

    value: Expression = field(default_factory=Expression)


@dataclass
class MatchSingleton(MatchPattern):
    """Singleton pattern (sahi, galat, shunya / None)."""

    value: Any = None


@dataclass
class MatchAs(MatchPattern):
    """Capture pattern (x), wildcard (_), or 'pat jaise x' pattern."""

    pattern: Optional[MatchPattern] = None
    name: Optional[str] = None


@dataclass
class MatchOr(MatchPattern):
    """OR pattern: pat1 | pat2 | pat3"""

    patterns: List[MatchPattern] = field(default_factory=list)


@dataclass
class MatchSequence(MatchPattern):
    """Sequence pattern: [pat1, pat2] or (pat1, pat2)"""

    patterns: List[MatchPattern] = field(default_factory=list)


@dataclass
class MatchStar(MatchPattern):
    """Starred capture pattern in sequence: *rest or *_"""

    name: Optional[str] = None


@dataclass
class MatchMapping(MatchPattern):
    """Mapping pattern: {key1: pat1, **rest}"""

    keys: List[Expression] = field(default_factory=list)
    patterns: List[MatchPattern] = field(default_factory=list)
    rest: Optional[str] = None


@dataclass
class MatchClass(MatchPattern):
    """Class pattern: Cls(p1, p2, attr=pat)"""

    cls: Expression = field(default_factory=Expression)
    patterns: List[MatchPattern] = field(default_factory=list)
    kwd_attrs: List[str] = field(default_factory=list)
    kwd_patterns: List[MatchPattern] = field(default_factory=list)


@dataclass
class MatchCase(ASTNode):
    """Case branch in match statement: vichaar <pattern> [agar <guard>]: <body>"""

    pattern: MatchPattern = field(default_factory=MatchPattern)
    guard: Optional[Expression] = None
    body: List[Statement] = field(default_factory=list)


@dataclass
class Match(Statement):
    """Pattern matching statement: milaao <subject>: <cases>"""

    subject: Expression = field(default_factory=Expression)
    cases: List[MatchCase] = field(default_factory=list)


# Type Aliases for convenient semantic identification
AsyncFunctionDefinition = FunctionDefinition
AsyncFor = For
AsyncWith = With


