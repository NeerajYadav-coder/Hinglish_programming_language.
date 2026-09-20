"""AST-based static analyzer and scope engine for Hinglish."""

import builtins
from enum import Enum, auto
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple, Union

from ..ast.nodes import (
    AnnAssign,
    Assert,
    Assignment,
    AssignmentExpression,
    ASTNode,
    AsyncFor,
    AsyncFunctionDefinition,
    AsyncWith,
    AttributeAccess,
    Await,
    BinaryOperation,
    Boolean,
    BooleanOperation,
    Break,
    ClassDefinition,
    Comparison,
    Complex,
    ComprehensionClause,
    Continue,
    Delete,
    DictComprehension,
    DictLiteral,
    DoubleStarred,
    ElifClause,
    ExceptHandler,
    Expression,
    ExpressionStatement,
    Float,
    For,
    FormattedValue,
    FromImport,
    FunctionCall,
    FunctionDefinition,
    GeneratorExpression,
    Global,
    Identifier,
    If,
    IfExp,
    Import,
    Indexing,
    Integer,
    JoinedStr,
    LambdaExpression,
    ListComprehension,
    ListLiteral,
    Match,
    MatchAs,
    MatchCase,
    MatchClass,
    MatchMapping,
    MatchOr,
    MatchPattern,
    MatchSequence,
    MatchSingleton,
    MatchStar,
    MatchValue,
    NoneLiteral,
    Nonlocal,
    Parameter,
    Pass,
    Program,
    Raise,
    Return,
    SetComprehension,
    SetLiteral,
    Slice,
    Starred,
    Statement,
    String,
    Try,
    TupleLiteral,
    UnaryOperation,
    While,
    With,
    WithItem,
    Yield,
    YieldFrom,
)
from ..exceptions import HinglishError
from ..keywords import DEFAULT_KEYWORD_REGISTRY, KeywordRegistry
from ..lexer import tokenize
from ..lexer.tokens import Position
from ..parser import parse
from .diagnostics import Diagnostic, Severity
from .rules import get_rule


# -----------------------------------------------------------------------------
# Builtin Vocabulary Registry
# -----------------------------------------------------------------------------

# Standard Python builtins
_PYTHON_BUILTINS: Set[str] = set(dir(builtins))

# Hinglish keyword registry built-in functions and aliases
_HINGLISH_BUILTINS: Set[str] = {
    "dikhao",
    "pucho",
    "lambai",
    "ginti",
    "jod",
    "sab",
    "koi",
    "prakar",
    "kram",
    "purnank",
    "dashamlav",
    "akshar",
    "kul_jod",
    "adhiktam",
    "nyuntam",
    "khol",
    "chapo",
    "batao",
    "sahi",
    "galat",
    "kuch_nahi",
    "shunya",
}

# Special variables and decorators
_SPECIAL_NAMES: Set[str] = {
    "__name__",
    "__doc__",
    "__file__",
    "__package__",
    "__path__",
    "__annotations__",
    "__builtins__",
    "__spec__",
    "__loader__",
    "__class__",
    "self",
    "cls",
    # Decorators
    "property",
    "staticmethod",
    "classmethod",
    "gunadharma",
    "sthiravidhi",
    "shrenividhi",
}

ALL_BUILTINS: Set[str] = _PYTHON_BUILTINS | _HINGLISH_BUILTINS | _SPECIAL_NAMES

# Subset of built-in functions considered high-risk for shadowing (Rule H007)
BUILTIN_FUNCTIONS_FOR_SHADOWING: Set[str] = {
    "dikhao",
    "pucho",
    "lambai",
    "prakar",
    "kram",
    "purnank",
    "dashamlav",
    "akshar",
    "kul_jod",
    "adhiktam",
    "nyuntam",
    "khol",
    "chapo",
    "batao",
    "print",
    "len",
    "range",
    "input",
    "int",
    "str",
    "float",
    "list",
    "dict",
    "set",
    "tuple",
    "bool",
    "type",
    "open",
    "sum",
    "max",
    "min",
    "abs",
    "round",
    "all",
    "any",
    "enumerate",
    "zip",
    "filter",
    "map",
    "id",
    "dir",
    "repr",
}


# -----------------------------------------------------------------------------
# Scope & Symbol Model
# -----------------------------------------------------------------------------


class ScopeKind(Enum):
    """Classification of lexical scope boundaries."""

    MODULE = auto()
    FUNCTION = auto()
    CLASS = auto()
    COMPREHENSION = auto()
    LAMBDA = auto()


class SymbolKind(Enum):
    """Classification of symbols within a scope."""

    VARIABLE = auto()
    PARAMETER = auto()
    FUNCTION = auto()
    CLASS = auto()
    IMPORT = auto()


class Symbol:
    """Represents a declared symbol and tracks its definitions and usages."""

    def __init__(
        self,
        name: str,
        kind: SymbolKind,
        scope: "Scope",
        def_node: Optional[ASTNode] = None,
        def_pos: Optional[Position] = None,
    ) -> None:
        self.name: str = name
        self.kind: SymbolKind = kind
        self.scope: "Scope" = scope
        self.def_node: Optional[ASTNode] = def_node
        self.def_pos: Optional[Position] = def_pos
        self.reads: List[Tuple[ASTNode, Optional[Position]]] = []
        self.writes: List[Tuple[ASTNode, Optional[Position]]] = []


class Scope:
    """Represents a lexical scope container."""

    def __init__(
        self,
        kind: ScopeKind,
        name: str = "<anonymous>",
        parent: Optional["Scope"] = None,
    ) -> None:
        self.kind: ScopeKind = kind
        self.name: str = name
        self.parent: Optional["Scope"] = parent
        self.children: List["Scope"] = []
        self.symbols: Dict[str, Symbol] = {}
        self.explicit_globals: Set[str] = set()
        self.explicit_nonlocals: Set[str] = set()
        self.defined_callables: Dict[str, Tuple[ASTNode, Optional[Position], str]] = {}

        if parent:
            parent.children.append(self)

    def get_module_scope(self) -> "Scope":
        """Walks up the parent chain to the root Module scope."""
        curr = self
        while curr.parent is not None:
            curr = curr.parent
        return curr

    def define_symbol(
        self,
        name: str,
        kind: SymbolKind,
        node: Optional[ASTNode] = None,
        pos: Optional[Position] = None,
    ) -> Symbol:
        """Registers or writes to a symbol in this scope, respecting global and nonlocal directives."""
        if name in self.explicit_globals:
            return self.get_module_scope().define_symbol(name, kind, node, pos)

        if name in self.explicit_nonlocals:
            curr = self.parent
            while curr and curr.kind != ScopeKind.MODULE:
                if name in curr.symbols:
                    sym = curr.symbols[name]
                    sym.writes.append((node, pos))
                    return sym
                curr = curr.parent

        if name in self.symbols:
            sym = self.symbols[name]
            sym.writes.append((node, pos))
            return sym

        sym = Symbol(name=name, kind=kind, scope=self, def_node=node, def_pos=pos)
        sym.writes.append((node, pos))
        self.symbols[name] = sym
        return sym


# -----------------------------------------------------------------------------
# Static Analyzer
# -----------------------------------------------------------------------------


class HinglishLinter:
    """Traverses a Hinglish AST, tracks scopes, and generates static analysis diagnostics."""

    def __init__(self, registry: Optional[KeywordRegistry] = None) -> None:
        self.registry: KeywordRegistry = registry or DEFAULT_KEYWORD_REGISTRY
        self.diagnostics: List[Diagnostic] = []
        self.all_scopes: List[Scope] = []
        self.all_reads: List[Tuple[str, ASTNode, Optional[Position], Scope]] = []
        self.filename: Optional[str] = None

    def lint(self, tree: Program, filename: Optional[str] = None) -> List[Diagnostic]:
        """Runs static analysis on a parsed Hinglish Program AST."""
        self.diagnostics = []
        self.all_scopes = []
        self.all_reads = []
        self.filename = filename

        # Pass 1: Scope construction, declaration collection, and local rule checks
        module_scope = Scope(ScopeKind.MODULE, name="<module>")
        self.all_scopes.append(module_scope)
        self._visit_statements(tree.body, module_scope)

        # Pass 2: Identifier resolution (H001 Undefined Name)
        self._resolve_reads()

        # Pass 3: Unused variable and import analysis (H002, H003)
        self._check_unused_symbols()

        # Sort diagnostics deterministically
        self.diagnostics.sort()
        return self.diagnostics

    # -------------------------------------------------------------------------
    # Pass 1: AST Traversal & Local Rule Evaluation
    # -------------------------------------------------------------------------

    def _visit_statements(self, statements: List[Statement], scope: Scope) -> None:
        """Visits a block of statements within a lexical scope."""
        terminator_seen = False
        terminator_keyword = ""

        for stmt in statements:
            # Rule H005: Unreachable code
            if terminator_seen:
                pos = stmt.start_pos
                self.diagnostics.append(
                    Diagnostic(
                        rule_id="H005",
                        message=f"unreachable code after '{terminator_keyword}'",
                        severity=Severity.WARNING,
                        line=pos.line if pos else 1,
                        column=pos.column if pos else 1,
                        filename=self.filename,
                    )
                )

            # Check if this statement is an unconditional terminator
            if isinstance(stmt, Return):
                terminator_seen = True
                terminator_keyword = "wapas"
            elif isinstance(stmt, Raise):
                terminator_seen = True
                terminator_keyword = "uthav"
            elif isinstance(stmt, Break):
                terminator_seen = True
                terminator_keyword = "ruko"
            elif isinstance(stmt, Continue):
                terminator_seen = True
                terminator_keyword = "aage_bado"

            self._visit_statement(stmt, scope)

    def _visit_statement(self, stmt: Statement, scope: Scope) -> None:
        """Dispatches statement visitors."""
        if isinstance(stmt, ExpressionStatement):
            self._visit_expression(stmt.expr, scope)

        elif isinstance(stmt, Assignment):
            self._handle_assignment(stmt, scope)

        elif isinstance(stmt, AnnAssign):
            self._handle_ann_assign(stmt, scope)

        elif isinstance(stmt, FunctionDefinition):
            self._handle_function_def(stmt, scope)

        elif isinstance(stmt, ClassDefinition):
            self._handle_class_def(stmt, scope)

        elif isinstance(stmt, If):
            self._handle_if(stmt, scope)

        elif isinstance(stmt, While):
            self._handle_while(stmt, scope)

        elif isinstance(stmt, For):
            self._handle_for(stmt, scope)

        elif isinstance(stmt, With):
            self._handle_with(stmt, scope)

        elif isinstance(stmt, Try):
            self._handle_try(stmt, scope)

        elif isinstance(stmt, Return):
            if stmt.value:
                self._visit_expression(stmt.value, scope)

        elif isinstance(stmt, Raise):
            if stmt.exc:
                self._visit_expression(stmt.exc, scope)

        elif isinstance(stmt, Assert):
            self._visit_expression(stmt.test, scope)
            if stmt.msg:
                self._visit_expression(stmt.msg, scope)

        elif isinstance(stmt, Delete):
            for tgt in stmt.targets:
                self._visit_expression(tgt, scope)

        elif isinstance(stmt, Global):
            for name in stmt.names:
                scope.explicit_globals.add(name)

        elif isinstance(stmt, Nonlocal):
            for name in stmt.names:
                scope.explicit_nonlocals.add(name)

        elif isinstance(stmt, Import):
            for mod_name, alias in stmt.names:
                bound_name = alias if alias else mod_name.split(".")[0]
                scope.define_symbol(bound_name, SymbolKind.IMPORT, node=stmt, pos=stmt.start_pos)

        elif isinstance(stmt, FromImport):
            for name, alias in stmt.names:
                if name == "*":
                    continue
                bound_name = alias if alias else name
                scope.define_symbol(bound_name, SymbolKind.IMPORT, node=stmt, pos=stmt.start_pos)

        elif isinstance(stmt, Match):
            self._handle_match(stmt, scope)

        elif isinstance(stmt, Pass):
            pass

    # -------------------------------------------------------------------------
    # Statement Handlers
    # -------------------------------------------------------------------------

    def _handle_assignment(self, stmt: Assignment, scope: Scope) -> None:
        """Handles variable assignment, augmented assignment, and unpacking."""
        # 1. Evaluate RHS value expressions
        self._visit_expression(stmt.value, scope)

        # 2. If augmented assignment (e.g. x += 1), target is also read
        if stmt.op != "=":
            self._visit_expression(stmt.target, scope)

        # 3. Extract targets and define in scope
        targets = self._extract_lvalue_targets(stmt.target, scope)
        for name, node, pos in targets:
            # Check Rule H007: Shadowing built-in functions
            if name in BUILTIN_FUNCTIONS_FOR_SHADOWING and scope.kind != ScopeKind.MODULE:
                self.diagnostics.append(
                    Diagnostic(
                        rule_id="H007",
                        message=f"variable '{name}' shadows built-in function",
                        severity=Severity.WARNING,
                        line=pos.line if pos else 1,
                        column=pos.column if pos else 1,
                        filename=self.filename,
                    )
                )

            scope.define_symbol(name, SymbolKind.VARIABLE, node=node, pos=pos)

    def _handle_ann_assign(self, stmt: AnnAssign, scope: Scope) -> None:
        """Handles annotated variable assignment: x: int [= 10]."""
        self._visit_expression(stmt.annotation, scope)
        if stmt.value:
            self._visit_expression(stmt.value, scope)

        targets = self._extract_lvalue_targets(stmt.target, scope)
        for name, node, pos in targets:
            scope.define_symbol(name, SymbolKind.VARIABLE, node=node, pos=pos)

    def _handle_function_def(self, stmt: FunctionDefinition, scope: Scope) -> None:
        """Handles function definition, parameter binding, decorators, and body."""
        # Check Rule H004: Duplicate function definition in same scope
        if stmt.name in scope.defined_callables:
            prev_node, prev_pos, prev_type = scope.defined_callables[stmt.name]
            pos = stmt.start_pos
            self.diagnostics.append(
                Diagnostic(
                    rule_id="H004",
                    message=f"duplicate {prev_type} definition '{stmt.name}'",
                    severity=Severity.WARNING,
                    line=pos.line if pos else 1,
                    column=pos.column if pos else 1,
                    filename=self.filename,
                )
            )
        scope.defined_callables[stmt.name] = (stmt, stmt.start_pos, "function")

        # Check Rule H007: Shadowing built-in functions or outer functions
        if stmt.name in BUILTIN_FUNCTIONS_FOR_SHADOWING:
            pos = stmt.start_pos
            self.diagnostics.append(
                Diagnostic(
                    rule_id="H007",
                    message=f"function '{stmt.name}' shadows built-in function",
                    severity=Severity.WARNING,
                    line=pos.line if pos else 1,
                    column=pos.column if pos else 1,
                    filename=self.filename,
                )
            )
        else:
            # Check outer function shadowing
            outer = scope
            while outer is not None:
                if outer.name == stmt.name:
                    pos = stmt.start_pos
                    self.diagnostics.append(
                        Diagnostic(
                            rule_id="H007",
                            message=f"function '{stmt.name}' shadows outer function '{stmt.name}'",
                            severity=Severity.WARNING,
                            line=pos.line if pos else 1,
                            column=pos.column if pos else 1,
                            filename=self.filename,
                        )
                    )
                    break
                outer = outer.parent

        # Define function in enclosing scope
        scope.define_symbol(stmt.name, SymbolKind.FUNCTION, node=stmt, pos=stmt.start_pos)

        # Decorators, parameter annotations, defaults, and return annotations evaluate in ENCLOSING scope
        for dec in stmt.decorators:
            self._visit_expression(dec, scope)
        if stmt.returns:
            self._visit_expression(stmt.returns, scope)
        for param in stmt.parameters:
            if param.annotation:
                self._visit_expression(param.annotation, scope)
            if param.default:
                self._visit_expression(param.default, scope)

        # Create Function Scope
        func_scope = Scope(ScopeKind.FUNCTION, name=stmt.name, parent=scope)
        self.all_scopes.append(func_scope)

        # Bind parameters in function scope
        param_names = stmt.params or [p.name for p in stmt.parameters]
        for p_name in param_names:
            if not p_name:
                continue
            # Rule H007: Parameter shadowing builtins
            if p_name in BUILTIN_FUNCTIONS_FOR_SHADOWING and p_name not in {"self", "cls"}:
                pos = stmt.start_pos
                self.diagnostics.append(
                    Diagnostic(
                        rule_id="H007",
                        message=f"parameter '{p_name}' shadows built-in function",
                        severity=Severity.WARNING,
                        line=pos.line if pos else 1,
                        column=pos.column if pos else 1,
                        filename=self.filename,
                    )
                )

            func_scope.define_symbol(p_name, SymbolKind.PARAMETER, node=stmt, pos=stmt.start_pos)

        # Traverse function body
        self._visit_statements(stmt.body, func_scope)

    def _handle_class_def(self, stmt: ClassDefinition, scope: Scope) -> None:
        """Handles class definition, inheritance bases, and methods."""
        # Check Rule H004: Duplicate class definition
        if stmt.name in scope.defined_callables:
            prev_node, prev_pos, prev_type = scope.defined_callables[stmt.name]
            pos = stmt.start_pos
            self.diagnostics.append(
                Diagnostic(
                    rule_id="H004",
                    message=f"duplicate {prev_type} definition '{stmt.name}'",
                    severity=Severity.WARNING,
                    line=pos.line if pos else 1,
                    column=pos.column if pos else 1,
                    filename=self.filename,
                )
            )
        scope.defined_callables[stmt.name] = (stmt, stmt.start_pos, "class")

        # Check Rule H007: Shadowing built-in functions
        if stmt.name in BUILTIN_FUNCTIONS_FOR_SHADOWING:
            pos = stmt.start_pos
            self.diagnostics.append(
                Diagnostic(
                    rule_id="H007",
                    message=f"class '{stmt.name}' shadows built-in function",
                    severity=Severity.WARNING,
                    line=pos.line if pos else 1,
                    column=pos.column if pos else 1,
                    filename=self.filename,
                )
            )

        # Define class in enclosing scope
        scope.define_symbol(stmt.name, SymbolKind.CLASS, node=stmt, pos=stmt.start_pos)

        # Bases & decorators evaluate in enclosing scope
        for base in stmt.bases:
            self._visit_expression(base, scope)
        for dec in stmt.decorators:
            self._visit_expression(dec, scope)

        # Create Class Scope
        class_scope = Scope(ScopeKind.CLASS, name=stmt.name, parent=scope)
        self.all_scopes.append(class_scope)

        self._visit_statements(stmt.body, class_scope)

    def _handle_if(self, stmt: If, scope: Scope) -> None:
        """Handles if statement and elif/else clauses, checking constant conditions (H006)."""
        # Rule H006: Constant condition on 'agar'
        if self._is_constant_condition(stmt.condition):
            pos = stmt.condition.start_pos or stmt.start_pos
            self.diagnostics.append(
                Diagnostic(
                    rule_id="H006",
                    message="constant condition in 'agar' statement",
                    severity=Severity.WARNING,
                    line=pos.line if pos else 1,
                    column=pos.column if pos else 1,
                    filename=self.filename,
                )
            )

        self._visit_expression(stmt.condition, scope)
        self._visit_statements(stmt.body, scope)

        for clause in stmt.elif_clauses:
            if self._is_constant_condition(clause.condition):
                pos = clause.condition.start_pos or clause.start_pos
                self.diagnostics.append(
                    Diagnostic(
                        rule_id="H006",
                        message="constant condition in 'warna_agar' clause",
                        severity=Severity.WARNING,
                        line=pos.line if pos else 1,
                        column=pos.column if pos else 1,
                        filename=self.filename,
                    )
                )
            self._visit_expression(clause.condition, scope)
            self._visit_statements(clause.body, scope)

        if stmt.else_body:
            self._visit_statements(stmt.else_body, scope)

    def _handle_while(self, stmt: While, scope: Scope) -> None:
        """Handles while loops, detecting trivially constant conditions (H006)."""
        if self._is_constant_false_condition(stmt.condition):
            pos = stmt.condition.start_pos or stmt.start_pos
            self.diagnostics.append(
                Diagnostic(
                    rule_id="H006",
                    message="constant false condition in 'jabtak' loop (loop will never run)",
                    severity=Severity.WARNING,
                    line=pos.line if pos else 1,
                    column=pos.column if pos else 1,
                    filename=self.filename,
                )
            )

        self._visit_expression(stmt.condition, scope)
        self._visit_statements(stmt.body, scope)

    def _handle_for(self, stmt: For, scope: Scope) -> None:
        """Handles for and async for loops, binding loop targets."""
        self._visit_expression(stmt.iterable, scope)

        targets = self._extract_lvalue_targets(stmt.target, scope)
        for name, node, pos in targets:
            scope.define_symbol(name, SymbolKind.VARIABLE, node=node, pos=pos)

        self._visit_statements(stmt.body, scope)

    def _handle_with(self, stmt: With, scope: Scope) -> None:
        """Handles with and async with statements."""
        for item in stmt.items:
            self._visit_expression(item.context_expr, scope)
            if item.optional_vars:
                targets = self._extract_lvalue_targets(item.optional_vars, scope)
                for name, node, pos in targets:
                    scope.define_symbol(name, SymbolKind.VARIABLE, node=node, pos=pos)

        self._visit_statements(stmt.body, scope)

    def _handle_try(self, stmt: Try, scope: Scope) -> None:
        """Handles try/except/else/finally blocks."""
        self._visit_statements(stmt.body, scope)

        for handler in stmt.handlers:
            if handler.type:
                self._visit_expression(handler.type, scope)
            if handler.name:
                scope.define_symbol(handler.name, SymbolKind.VARIABLE, node=handler, pos=handler.start_pos)
            self._visit_statements(handler.body, scope)

        if stmt.else_body:
            self._visit_statements(stmt.else_body, scope)

        if stmt.finally_body:
            self._visit_statements(stmt.finally_body, scope)

    def _handle_match(self, stmt: Match, scope: Scope) -> None:
        """Handles structural pattern matching."""
        self._visit_expression(stmt.subject, scope)

        for case in stmt.cases:
            self._bind_pattern_targets(case.pattern, scope)
            if case.guard:
                self._visit_expression(case.guard, scope)
            self._visit_statements(case.body, scope)

    # -------------------------------------------------------------------------
    # Expression Visitors
    # -------------------------------------------------------------------------

    def _visit_expression(self, expr: Expression, scope: Scope) -> None:
        """Traverses expressions and records variable reads."""
        if isinstance(expr, Identifier):
            self.all_reads.append((expr.name, expr, expr.start_pos, scope))

        elif isinstance(expr, IfExp):
            self._visit_expression(expr.condition, scope)
            self._visit_expression(expr.body, scope)
            self._visit_expression(expr.orelse, scope)

        elif isinstance(expr, AssignmentExpression):
            # Walrus operator: (x := 10)
            self._visit_expression(expr.value, scope)
            # Walrus binds outside comprehensions if inside one
            target_scope = scope
            while target_scope.kind == ScopeKind.COMPREHENSION and target_scope.parent is not None:
                target_scope = target_scope.parent

            targets = self._extract_lvalue_targets(expr.target, target_scope)
            for name, node, pos in targets:
                target_scope.define_symbol(name, SymbolKind.VARIABLE, node=node, pos=pos)

        elif isinstance(expr, FunctionCall):
            self._visit_expression(expr.func, scope)
            for arg in expr.args:
                self._visit_expression(arg, scope)
            for val in expr.keywords.values():
                self._visit_expression(val, scope)

        elif isinstance(expr, AttributeAccess):
            # In obj.attr, obj is read; attr is an attribute name, not a variable read
            self._visit_expression(expr.value, scope)

        elif isinstance(expr, Indexing):
            self._visit_expression(expr.value, scope)
            self._visit_expression(expr.index, scope)

        elif isinstance(expr, Slice):
            if expr.lower:
                self._visit_expression(expr.lower, scope)
            if expr.upper:
                self._visit_expression(expr.upper, scope)
            if expr.step:
                self._visit_expression(expr.step, scope)

        elif isinstance(expr, BinaryOperation):
            self._visit_expression(expr.left, scope)
            self._visit_expression(expr.right, scope)

        elif isinstance(expr, UnaryOperation):
            self._visit_expression(expr.operand, scope)

        elif isinstance(expr, Comparison):
            self._visit_expression(expr.left, scope)
            self._visit_expression(expr.right, scope)

        elif isinstance(expr, BooleanOperation):
            for val in expr.values:
                self._visit_expression(val, scope)

        elif isinstance(expr, (ListLiteral, TupleLiteral, SetLiteral)):
            for elem in expr.elements:
                self._visit_expression(elem, scope)

        elif isinstance(expr, DictLiteral):
            for k in expr.keys:
                self._visit_expression(k, scope)
            for v in expr.values:
                self._visit_expression(v, scope)

        elif isinstance(expr, JoinedStr):
            for part in expr.parts:
                self._visit_expression(part, scope)

        elif isinstance(expr, FormattedValue):
            self._visit_expression(expr.value, scope)

        elif isinstance(expr, (ListComprehension, SetComprehension, GeneratorExpression)):
            comp_scope = Scope(ScopeKind.COMPREHENSION, name="<comprehension>", parent=scope)
            self.all_scopes.append(comp_scope)
            for clause in expr.clauses:
                self._visit_expression(clause.iterable, scope)
                targets = self._extract_lvalue_targets(clause.target, comp_scope)
                for name, node, pos in targets:
                    comp_scope.define_symbol(name, SymbolKind.VARIABLE, node=node, pos=pos)
                for cond in clause.conditions:
                    self._visit_expression(cond, comp_scope)
            self._visit_expression(expr.element, comp_scope)

        elif isinstance(expr, DictComprehension):
            comp_scope = Scope(ScopeKind.COMPREHENSION, name="<dict_comprehension>", parent=scope)
            self.all_scopes.append(comp_scope)
            for clause in expr.clauses:
                self._visit_expression(clause.iterable, scope)
                targets = self._extract_lvalue_targets(clause.target, comp_scope)
                for name, node, pos in targets:
                    comp_scope.define_symbol(name, SymbolKind.VARIABLE, node=node, pos=pos)
                for cond in clause.conditions:
                    self._visit_expression(cond, comp_scope)
            self._visit_expression(expr.key, comp_scope)
            self._visit_expression(expr.value, comp_scope)

        elif isinstance(expr, LambdaExpression):
            lambda_scope = Scope(ScopeKind.LAMBDA, name="<lambda>", parent=scope)
            self.all_scopes.append(lambda_scope)
            for p in expr.params:
                lambda_scope.define_symbol(p, SymbolKind.PARAMETER, node=expr, pos=expr.start_pos)
            self._visit_expression(expr.body, lambda_scope)

        elif isinstance(expr, Yield):
            if expr.value:
                self._visit_expression(expr.value, scope)

        elif isinstance(expr, YieldFrom):
            self._visit_expression(expr.value, scope)

        elif isinstance(expr, Await):
            self._visit_expression(expr.value, scope)

        elif isinstance(expr, (Starred, DoubleStarred)):
            self._visit_expression(expr.value, scope)

    # -------------------------------------------------------------------------
    # Target Extraction Helpers
    # -------------------------------------------------------------------------

    def _extract_lvalue_targets(
        self, expr: Expression, scope: Scope
    ) -> List[Tuple[str, ASTNode, Optional[Position]]]:
        """Extracts variable names and positions from assignment lvalue targets."""
        targets: List[Tuple[str, ASTNode, Optional[Position]]] = []

        if isinstance(expr, Identifier):
            targets.append((expr.name, expr, expr.start_pos))

        elif isinstance(expr, (TupleLiteral, ListLiteral)):
            for elem in expr.elements:
                targets.extend(self._extract_lvalue_targets(elem, scope))

        elif isinstance(expr, Starred):
            targets.extend(self._extract_lvalue_targets(expr.value, scope))

        elif isinstance(expr, AttributeAccess):
            # self.x = 10 -> self is read; x is an attribute
            self._visit_expression(expr.value, scope)

        elif isinstance(expr, Indexing):
            # arr[0] = 10 -> both arr and 0 are read
            self._visit_expression(expr.value, scope)
            self._visit_expression(expr.index, scope)

        return targets

    def _bind_pattern_targets(self, pattern: MatchPattern, scope: Scope) -> None:
        """Extracts and binds variable captures in structural pattern matching."""
        if isinstance(pattern, MatchAs):
            if pattern.name and pattern.name != "_":
                scope.define_symbol(pattern.name, SymbolKind.VARIABLE, node=pattern, pos=pattern.start_pos)
            if pattern.pattern:
                self._bind_pattern_targets(pattern.pattern, scope)

        elif isinstance(pattern, MatchStar):
            if pattern.name and pattern.name != "_":
                scope.define_symbol(pattern.name, SymbolKind.VARIABLE, node=pattern, pos=pattern.start_pos)

        elif isinstance(pattern, MatchSequence):
            for subpat in pattern.patterns:
                self._bind_pattern_targets(subpat, scope)

        elif isinstance(pattern, MatchMapping):
            for key_expr in pattern.keys:
                self._visit_expression(key_expr, scope)
            for pat in pattern.patterns:
                self._bind_pattern_targets(pat, scope)
            if pattern.rest and pattern.rest != "_":
                scope.define_symbol(pattern.rest, SymbolKind.VARIABLE, node=pattern, pos=pattern.start_pos)

        elif isinstance(pattern, MatchClass):
            self._visit_expression(pattern.cls, scope)
            for subpat in pattern.patterns:
                self._bind_pattern_targets(subpat, scope)
            for kw_pat in pattern.kwd_patterns:
                self._bind_pattern_targets(kw_pat, scope)

        elif isinstance(pattern, MatchOr):
            for subpat in pattern.patterns:
                self._bind_pattern_targets(subpat, scope)

        elif isinstance(pattern, MatchValue):
            self._visit_expression(pattern.value, scope)

    # -------------------------------------------------------------------------
    # Pass 2: Identifier Resolution (Rule H001 Undefined Name)
    # -------------------------------------------------------------------------

    def _resolve_reads(self) -> None:
        """Resolves all identifier reads against the scope hierarchy and builtins."""
        for name, node, pos, read_scope in self.all_reads:
            resolved_symbol = self._lookup_symbol(name, read_scope)

            if resolved_symbol is not None:
                resolved_symbol.reads.append((node, pos))
            else:
                # Check builtins
                if name in ALL_BUILTINS:
                    continue

                # Unresolved identifier -> Rule H001: Undefined Name
                self.diagnostics.append(
                    Diagnostic(
                        rule_id="H001",
                        message=f"undefined name '{name}'",
                        severity=Severity.ERROR,
                        line=pos.line if pos else 1,
                        column=pos.column if pos else 1,
                        filename=self.filename,
                    )
                )

    def _lookup_symbol(self, name: str, start_scope: Scope) -> Optional[Symbol]:
        """Resolves an identifier starting from a given scope up to module scope."""
        # 1. If explicit global, look directly in module scope
        if name in start_scope.explicit_globals:
            mod_scope = start_scope.get_module_scope()
            return mod_scope.symbols.get(name)

        # 2. If explicit nonlocal, climb parent scopes skipping class scopes
        if name in start_scope.explicit_nonlocals:
            curr = start_scope.parent
            while curr is not None and curr.kind != ScopeKind.MODULE:
                if curr.kind != ScopeKind.CLASS and name in curr.symbols:
                    return curr.symbols[name]
                curr = curr.parent
            return None

        # 3. Lexical scope chain lookup
        curr: Optional[Scope] = start_scope
        while curr is not None:
            # In Python, inner functions/methods do NOT inherit class body namespace
            if curr.kind == ScopeKind.CLASS and curr != start_scope:
                curr = curr.parent
                continue

            if name in curr.symbols:
                return curr.symbols[name]

            curr = curr.parent

        return None

    # -------------------------------------------------------------------------
    # Pass 3: Unused Definitions (Rules H002 and H003)
    # -------------------------------------------------------------------------

    def _check_unused_symbols(self) -> None:
        """Checks for unused local variables (H002) and unused imports (H003)."""
        for scope in self.all_scopes:
            # Rule H003: Unused imports (check at module and local levels)
            for sym in scope.symbols.values():
                if sym.kind == SymbolKind.IMPORT:
                    if len(sym.reads) == 0 and not sym.name.startswith("_"):
                        pos = sym.def_pos
                        self.diagnostics.append(
                            Diagnostic(
                                rule_id="H003",
                                message=f"imported name '{sym.name}' is never used",
                                severity=Severity.WARNING,
                                line=pos.line if pos else 1,
                                column=pos.column if pos else 1,
                                filename=self.filename,
                            )
                        )

            # Rule H002: Unused local variables (in functions and lambdas only)
            if scope.kind in (ScopeKind.FUNCTION, ScopeKind.LAMBDA):
                for sym in scope.symbols.values():
                    if sym.kind == SymbolKind.VARIABLE:
                        if len(sym.reads) == 0:
                            if not sym.name.startswith("_") and sym.name not in {"self", "cls"}:
                                pos = sym.def_pos
                                self.diagnostics.append(
                                    Diagnostic(
                                        rule_id="H002",
                                        message=f"variable '{sym.name}' is assigned but never used",
                                        severity=Severity.WARNING,
                                        line=pos.line if pos else 1,
                                        column=pos.column if pos else 1,
                                        filename=self.filename,
                                    )
                                )

    # -------------------------------------------------------------------------
    # Constant Condition Helpers (Rule H006)
    # -------------------------------------------------------------------------

    def _is_constant_condition(self, expr: Expression) -> bool:
        """Returns True if the expression is trivially constant (e.g. sahi, galat, literals)."""
        if isinstance(expr, (Boolean, Integer, Float, NoneLiteral, String)):
            return True
        return False

    def _is_constant_false_condition(self, expr: Expression) -> bool:
        """Returns True if the expression is trivially false/zero/none."""
        if isinstance(expr, Boolean) and expr.value is False:
            return True
        if isinstance(expr, Integer) and expr.value == 0:
            return True
        if isinstance(expr, Float) and expr.value == 0.0:
            return True
        if isinstance(expr, NoneLiteral):
            return True
        return False


# -----------------------------------------------------------------------------
# Public API Functions
# -----------------------------------------------------------------------------


def lint_source(source: str, filename: Optional[str] = "<source>") -> List[Diagnostic]:
    """Analyzes Hinglish source code and returns a deterministic list of static diagnostics."""
    try:
        tokens = tokenize(source, include_comments=False)
        tree = parse(tokens)
        linter = HinglishLinter()
        return linter.lint(tree, filename=filename)
    except HinglishError as err:
        return [
            Diagnostic(
                rule_id="syntax-error",
                message=err.message or str(err),
                severity=Severity.ERROR,
                line=err.line or 1,
                column=err.column or 1,
                filename=filename,
            )
        ]
    except Exception as exc:
        return [
            Diagnostic(
                rule_id="syntax-error",
                message=str(exc),
                severity=Severity.ERROR,
                line=1,
                column=1,
                filename=filename,
            )
        ]


def lint_file(filepath: Union[str, Path]) -> List[Diagnostic]:
    """Reads a .hin file from disk and performs static analysis."""
    path = Path(filepath)
    if not path.is_file():
        raise FileNotFoundError(f"File not found: {filepath}")
    source = path.read_text(encoding="utf-8")
    return lint_source(source, filename=str(path))
