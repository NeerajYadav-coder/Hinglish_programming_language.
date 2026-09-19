"""Deterministic, AST-based Formatter for Hinglish source code.

Adheres to canonical Hinglish style:
- 4 spaces indentation
- Deterministic blank line rules (2 blank lines around top-level defs, 1 between methods, at most 1 between statements)
- Canonical whitespace around operators and punctuation
- Operator precedence and parenthesization
- String literal byte-for-byte preservation (quotes, prefixes, escape sequences)
- Comment preservation (standalone comments aligned to block indentation, inline comments with 2 spaces)
- 100% idempotent: format(format(source)) == format(source)
"""

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
from ..lexer.lexer import HinglishLexer
from ..lexer.tokens import Token, TokenType
from ..parser.parser import HinglishParser


# Operator Precedence Levels (lowest 1 to highest 15)
PREC_LAMBDA = 1
PREC_ASSIGN = 2     # Walrus :=
PREC_OR = 3         # ya
PREC_AND = 4        # aur
PREC_NOT = 5        # nahi
PREC_COMPARE = 6    # ==, !=, <, <=, >, >=, mein, hai, etc.
PREC_BOR = 7        # |
PREC_BXOR = 8       # ^
PREC_BAND = 9       # &
PREC_SHIFT = 10     # <<, >>
PREC_ADD = 11       # +, -
PREC_MUL = 12       # *, /, //, %, @
PREC_UNARY = 13     # +, -, ~
PREC_POW = 14       # **
PREC_PRIMARY = 15   # Calls, Indexing, Attributes, Literals, Parens


def get_precedence(expr: Expression) -> int:
    """Returns the operator precedence level of an expression node."""
    if isinstance(expr, LambdaExpression):
        return PREC_LAMBDA
    if isinstance(expr, AssignmentExpression):
        return PREC_ASSIGN
    if isinstance(expr, BooleanOperation):
        if expr.op in ("ya", "or"):
            return PREC_OR
        if expr.op in ("aur", "and"):
            return PREC_AND
        return PREC_OR
    if isinstance(expr, UnaryOperation) and expr.op in ("nahi", "not"):
        return PREC_NOT
    if isinstance(expr, Comparison):
        return PREC_COMPARE
    if isinstance(expr, BinaryOperation):
        op = expr.op
        if op == "|":
            return PREC_BOR
        if op == "^":
            return PREC_BXOR
        if op == "&":
            return PREC_BAND
        if op in ("<<", ">>"):
            return PREC_SHIFT
        if op in ("+", "-"):
            return PREC_ADD
        if op in ("*", "/", "//", "%", "@"):
            return PREC_MUL
        if op == "**":
            return PREC_POW
        return PREC_COMPARE
    if isinstance(expr, UnaryOperation):
        return PREC_UNARY
    if isinstance(expr, (Yield, YieldFrom, Await)):
        return PREC_LAMBDA
    return PREC_PRIMARY


class HinglishFormatter:
    """Canonical pretty-printer and code formatter for Hinglish AST."""

    def __init__(self, source_code: str, indent_size: int = 4) -> None:
        self.source = source_code
        self.indent_size = indent_size
        self.source_lines = source_code.splitlines()

        # Tokenize with comments
        lexer = HinglishLexer(include_comments=True)
        tokens = lexer.tokenize(source_code)

        self.comment_tokens: List[Token] = [t for t in tokens if t.type == TokenType.COMMENT]
        code_tokens = [t for t in tokens if t.type != TokenType.COMMENT]

        # Classify comments into standalone vs inline
        self.inline_comments: Dict[int, str] = {}
        self.standalone_comments: List[Tuple[int, str]] = []

        for ct in self.comment_tokens:
            line_idx = ct.start_pos.line - 1
            if line_idx < len(self.source_lines):
                line_str = self.source_lines[line_idx]
                prefix = line_str[: ct.start_pos.column - 1]
                if prefix.strip() == "":
                    self.standalone_comments.append((ct.start_pos.line, ct.value))
                else:
                    # Inline comment attached to the line
                    self.inline_comments[ct.start_pos.line] = ct.value
            else:
                self.standalone_comments.append((ct.start_pos.line, ct.value))

        self.standalone_comments.sort(key=lambda x: x[0])

        # Parse code into AST
        parser = HinglishParser(code_tokens, source_code=source_code)
        self.ast: Program = parser.parse()

    def format(self) -> str:
        """Executes formatting pass and returns canonical formatted source."""
        if not self.ast.body and not self.comment_tokens:
            return ""

        output_lines: List[str] = []
        self._format_statement_list(self.ast.body, output_lines, indent_level=0, is_module=True)

        # Emit any remaining standalone comments
        if self.standalone_comments and output_lines and output_lines[-1] != "":
            output_lines.append("")
        self._emit_standalone_comments_before(999999999, output_lines, indent_level=0)

        # Normalize blank lines: trim leading/trailing empty lines, ensure exactly one newline
        res = "\n".join(output_lines).rstrip()
        if res:
            res += "\n"
        return res

    # -------------------------------------------------------------------------
    # Comments & Blank Lines Management
    # -------------------------------------------------------------------------

    def _emit_standalone_comments_before(
        self, target_line: int, output_lines: List[str], indent_level: int
    ) -> None:
        """Emits all standalone comments that appear before target_line."""
        indent_str = " " * (indent_level * self.indent_size)
        last_comment_line = -1

        while self.standalone_comments and self.standalone_comments[0][0] <= target_line:
            orig_line, comment_text = self.standalone_comments.pop(0)

            # Check if there was an intentional blank line in original source
            if last_comment_line != -1 and (orig_line - last_comment_line > 1):
                if output_lines and output_lines[-1] != "":
                    output_lines.append("")

            output_lines.append(f"{indent_str}{comment_text.strip()}")
            last_comment_line = orig_line

    def _get_inline_comment(self, line: int) -> str:
        """Retrieves and clears inline comment for a given line, if any."""
        if line in self.inline_comments:
            comment_text = self.inline_comments.pop(line).strip()
            return f"  {comment_text}"
        return ""

    # -------------------------------------------------------------------------
    # Statement List Formatting
    # -------------------------------------------------------------------------

    def _format_statement_list(
        self,
        statements: List[Statement],
        output_lines: List[str],
        indent_level: int,
        is_module: bool = False,
        is_class: bool = False,
    ) -> None:
        """Formats a block of statements with proper indentation and blank lines."""
        prev_stmt: Optional[Statement] = None

        for idx, stmt in enumerate(statements):
            stmt_start_line = stmt.start_pos.line if stmt.start_pos else 0
            is_top_def = is_module and isinstance(stmt, (FunctionDefinition, ClassDefinition))
            prev_was_top_def = is_module and isinstance(prev_stmt, (FunctionDefinition, ClassDefinition))

            # 1. Blank lines between statements
            if prev_stmt is not None:
                if is_top_def or prev_was_top_def:
                    # 2 blank lines around top-level definitions
                    while len(output_lines) < 2 or output_lines[-1] != "" or output_lines[-2] != "":
                        output_lines.append("")
                elif is_class and isinstance(stmt, FunctionDefinition):
                    # 1 blank line before methods in a class
                    if output_lines and output_lines[-1] != "":
                        output_lines.append("")
                else:
                    # Regular statements: preserve single blank line if separated in original source
                    if (
                        prev_stmt.end_pos
                        and stmt.start_pos
                        and (stmt.start_pos.line - prev_stmt.end_pos.line > 1)
                    ):
                        if output_lines and output_lines[-1] != "":
                            output_lines.append("")

            # 2. Emit any standalone comments before this statement
            self._emit_standalone_comments_before(stmt_start_line, output_lines, indent_level)

            # 3. Format the statement itself
            self._format_statement(stmt, output_lines, indent_level)
            prev_stmt = stmt

    def _format_statement(
        self, stmt: Statement, output_lines: List[str], indent_level: int
    ) -> None:
        """Formats a single statement node."""
        indent_str = " " * (indent_level * self.indent_size)
        stmt_line = stmt.start_pos.line if stmt.start_pos else 0
        end_line = stmt.end_pos.line if stmt.end_pos else stmt_line

        # ExpressionStatement
        if isinstance(stmt, ExpressionStatement):
            text = self._format_expr(stmt.expr)
            inline = self._get_inline_comment(end_line) or self._get_inline_comment(stmt_line)
            output_lines.append(f"{indent_str}{text}{inline}")

        # Assignment
        elif isinstance(stmt, Assignment):
            target_str = self._format_expr(stmt.target)
            val_str = self._format_expr(stmt.value)
            inline = self._get_inline_comment(end_line) or self._get_inline_comment(stmt_line)
            output_lines.append(f"{indent_str}{target_str} {stmt.op} {val_str}{inline}")

        # Annotated Assignment
        elif isinstance(stmt, AnnAssign):
            target_str = self._format_expr(stmt.target)
            ann_str = self._format_expr(stmt.annotation)
            val_part = f" = {self._format_expr(stmt.value)}" if stmt.value is not None else ""
            inline = self._get_inline_comment(end_line) or self._get_inline_comment(stmt_line)
            output_lines.append(f"{indent_str}{target_str}: {ann_str}{val_part}{inline}")

        # If Statement
        elif isinstance(stmt, If):
            cond_str = self._format_expr(stmt.condition)
            inline = self._get_inline_comment(stmt_line)
            output_lines.append(f"{indent_str}agar {cond_str}:{inline}")
            self._format_statement_list(stmt.body, output_lines, indent_level + 1)

            for elif_clause in stmt.elif_clauses:
                elif_line = elif_clause.start_pos.line if elif_clause.start_pos else stmt_line
                self._emit_standalone_comments_before(elif_line, output_lines, indent_level)
                elif_cond = self._format_expr(elif_clause.condition)
                elif_inline = self._get_inline_comment(elif_line)
                output_lines.append(f"{indent_str}warna_agar {elif_cond}:{elif_inline}")
                self._format_statement_list(elif_clause.body, output_lines, indent_level + 1)

            if stmt.else_body is not None:
                else_start = stmt.elif_clauses[-1].end_pos.line if stmt.elif_clauses else (stmt.body[-1].end_pos.line if stmt.body else stmt_line)
                self._emit_standalone_comments_before(else_start + 1, output_lines, indent_level)
                else_inline = self._get_inline_comment(else_start + 1) or self._get_inline_comment(end_line)
                output_lines.append(f"{indent_str}warna:{else_inline}")
                self._format_statement_list(stmt.else_body, output_lines, indent_level + 1)

        # While Loop
        elif isinstance(stmt, While):
            cond_str = self._format_expr(stmt.condition)
            inline = self._get_inline_comment(stmt_line)
            output_lines.append(f"{indent_str}jabtak {cond_str}:{inline}")
            self._format_statement_list(stmt.body, output_lines, indent_level + 1)

        # For Loop
        elif isinstance(stmt, For):
            if isinstance(stmt.target, TupleLiteral) and stmt.target.elements:
                target_str = ", ".join(self._format_expr(e) for e in stmt.target.elements)
            else:
                target_str = self._format_expr(stmt.target)
            iter_str = self._format_expr(stmt.iterable)
            async_prefix = "asamanantar " if stmt.is_async else ""
            inline = self._get_inline_comment(stmt_line)
            output_lines.append(f"{indent_str}{async_prefix}har {target_str} mein {iter_str}:{inline}")
            self._format_statement_list(stmt.body, output_lines, indent_level + 1)

        # Function Definition
        elif isinstance(stmt, FunctionDefinition):
            # Decorators
            for deco in stmt.decorators:
                deco_line = deco.start_pos.line if deco.start_pos else stmt_line
                self._emit_standalone_comments_before(deco_line, output_lines, indent_level)
                deco_inline = self._get_inline_comment(deco_line)
                output_lines.append(f"{indent_str}@{self._format_expr(deco)}{deco_inline}")

            self._emit_standalone_comments_before(stmt_line, output_lines, indent_level)
            async_prefix = "asamanantar " if stmt.is_async else ""
            params_str = self._format_parameters(stmt.parameters)
            ret_str = f" -> {self._format_expr(stmt.returns)}" if stmt.returns else ""
            inline = self._get_inline_comment(stmt_line)
            output_lines.append(f"{indent_str}{async_prefix}kaam {stmt.name}({params_str}){ret_str}:{inline}")
            self._format_statement_list(stmt.body, output_lines, indent_level + 1)

        # Class Definition
        elif isinstance(stmt, ClassDefinition):
            # Decorators
            for deco in stmt.decorators:
                deco_line = deco.start_pos.line if deco.start_pos else stmt_line
                self._emit_standalone_comments_before(deco_line, output_lines, indent_level)
                deco_inline = self._get_inline_comment(deco_line)
                output_lines.append(f"{indent_str}@{self._format_expr(deco)}{deco_inline}")

            self._emit_standalone_comments_before(stmt_line, output_lines, indent_level)
            bases_str = f"({', '.join(self._format_expr(b) for b in stmt.bases)})" if stmt.bases else ""
            inline = self._get_inline_comment(stmt_line)
            output_lines.append(f"{indent_str}varg {stmt.name}{bases_str}:{inline}")
            self._format_statement_list(stmt.body, output_lines, indent_level + 1, is_class=True)

        # Return Statement
        elif isinstance(stmt, Return):
            val_str = f" {self._format_expr(stmt.value)}" if stmt.value is not None else ""
            inline = self._get_inline_comment(end_line) or self._get_inline_comment(stmt_line)
            output_lines.append(f"{indent_str}wapas{val_str}{inline}")

        # Pass / Break / Continue
        elif isinstance(stmt, Pass):
            inline = self._get_inline_comment(end_line) or self._get_inline_comment(stmt_line)
            output_lines.append(f"{indent_str}chhod_do{inline}")
        elif isinstance(stmt, Break):
            inline = self._get_inline_comment(end_line) or self._get_inline_comment(stmt_line)
            output_lines.append(f"{indent_str}ruko{inline}")
        elif isinstance(stmt, Continue):
            inline = self._get_inline_comment(end_line) or self._get_inline_comment(stmt_line)
            output_lines.append(f"{indent_str}aage_bado{inline}")

        # Global & Nonlocal
        elif isinstance(stmt, Global):
            inline = self._get_inline_comment(end_line) or self._get_inline_comment(stmt_line)
            output_lines.append(f"{indent_str}sarvavyapi {', '.join(stmt.names)}{inline}")
        elif isinstance(stmt, Nonlocal):
            inline = self._get_inline_comment(end_line) or self._get_inline_comment(stmt_line)
            output_lines.append(f"{indent_str}asthanik {', '.join(stmt.names)}{inline}")

        # Assert
        elif isinstance(stmt, Assert):
            test_str = self._format_expr(stmt.test)
            msg_str = f", {self._format_expr(stmt.msg)}" if stmt.msg is not None else ""
            inline = self._get_inline_comment(end_line) or self._get_inline_comment(stmt_line)
            output_lines.append(f"{indent_str}daawa {test_str}{msg_str}{inline}")

        # Delete
        elif isinstance(stmt, Delete):
            targets_str = ", ".join(self._format_expr(t) for t in stmt.targets)
            inline = self._get_inline_comment(end_line) or self._get_inline_comment(stmt_line)
            output_lines.append(f"{indent_str}hatao {targets_str}{inline}")

        # Import
        elif isinstance(stmt, Import):
            items = [name + (f" jaise {alias}" if alias else "") for name, alias in stmt.names]
            inline = self._get_inline_comment(end_line) or self._get_inline_comment(stmt_line)
            output_lines.append(f"{indent_str}laao {', '.join(items)}{inline}")

        # FromImport
        elif isinstance(stmt, FromImport):
            items = [name + (f" jaise {alias}" if alias else "") for name, alias in stmt.names]
            inline = self._get_inline_comment(end_line) or self._get_inline_comment(stmt_line)
            output_lines.append(f"{indent_str}se {stmt.module} laao {', '.join(items)}{inline}")

        # Try-Except-Finally Block
        elif isinstance(stmt, Try):
            inline = self._get_inline_comment(stmt_line)
            output_lines.append(f"{indent_str}koshish:{inline}")
            self._format_statement_list(stmt.body, output_lines, indent_level + 1)

            for handler in stmt.handlers:
                h_line = handler.start_pos.line if handler.start_pos else stmt_line
                self._emit_standalone_comments_before(h_line, output_lines, indent_level)
                star = " *" if handler.is_star else ""
                type_str = f" {self._format_expr(handler.type)}" if handler.type is not None else ""
                name_str = f" jaise {handler.name}" if handler.name else ""
                h_inline = self._get_inline_comment(h_line)
                output_lines.append(f"{indent_str}pakdo{star}{type_str}{name_str}:{h_inline}")
                self._format_statement_list(handler.body, output_lines, indent_level + 1)

            if stmt.else_body is not None:
                else_line = stmt.else_body[0].start_pos.line - 1 if stmt.else_body and stmt.else_body[0].start_pos else stmt_line
                self._emit_standalone_comments_before(else_line, output_lines, indent_level)
                else_inline = self._get_inline_comment(else_line)
                output_lines.append(f"{indent_str}warna:{else_inline}")
                self._format_statement_list(stmt.else_body, output_lines, indent_level + 1)

            if stmt.finally_body is not None:
                fin_line = stmt.finally_body[0].start_pos.line - 1 if stmt.finally_body and stmt.finally_body[0].start_pos else stmt_line
                self._emit_standalone_comments_before(fin_line, output_lines, indent_level)
                fin_inline = self._get_inline_comment(fin_line)
                output_lines.append(f"{indent_str}antatah:{fin_inline}")
                self._format_statement_list(stmt.finally_body, output_lines, indent_level + 1)

        # Raise
        elif isinstance(stmt, Raise):
            exc_str = f" {self._format_expr(stmt.exc)}" if stmt.exc is not None else ""
            inline = self._get_inline_comment(end_line) or self._get_inline_comment(stmt_line)
            output_lines.append(f"{indent_str}uthav{exc_str}{inline}")

        # With Context Manager
        elif isinstance(stmt, With):
            items_str = []
            for item in stmt.items:
                ctx_str = self._format_expr(item.context_expr)
                var_str = f" jaise {self._format_expr(item.optional_vars)}" if item.optional_vars else ""
                items_str.append(f"{ctx_str}{var_str}")

            async_prefix = "asamanantar " if stmt.is_async else ""
            inline = self._get_inline_comment(stmt_line)
            output_lines.append(f"{indent_str}{async_prefix}saath {', '.join(items_str)}:{inline}")
            self._format_statement_list(stmt.body, output_lines, indent_level + 1)

        # Pattern Match
        elif isinstance(stmt, Match):
            subject_str = self._format_expr(stmt.subject)
            inline = self._get_inline_comment(stmt_line)
            output_lines.append(f"{indent_str}milao {subject_str}:{inline}")

            for case in stmt.cases:
                case_line = case.start_pos.line if case.start_pos else stmt_line
                self._emit_standalone_comments_before(case_line, output_lines, indent_level + 1)
                pat_str = self._format_pattern(case.pattern)
                guard_str = f" agar {self._format_expr(case.guard)}" if case.guard else ""
                case_inline = self._get_inline_comment(case_line)
                case_indent = " " * ((indent_level + 1) * self.indent_size)
                output_lines.append(f"{case_indent}vichaar {pat_str}{guard_str}:{case_inline}")
                self._format_statement_list(case.body, output_lines, indent_level + 2)

    # -------------------------------------------------------------------------
    # Function Parameters Formatting
    # -------------------------------------------------------------------------

    def _format_parameters(self, parameters: List[Parameter]) -> str:
        """Formats function parameters including /, *, *args, **kwargs, defaults and annotations."""
        if not parameters:
            return ""

        parts: List[str] = []
        had_pos_only = False
        seen_star = False

        for idx, param in enumerate(parameters):
            if param.kind == "POSITIONAL_ONLY":
                had_pos_only = True
                p_str = param.name
                if param.annotation is not None:
                    p_str += f": {self._format_expr(param.annotation)}"
                if param.default is not None:
                    eq_space = " = " if param.annotation is not None else "="
                    p_str += f"{eq_space}{self._format_expr(param.default)}"
                parts.append(p_str)
                continue

            if had_pos_only:
                parts.append("/")
                had_pos_only = False

            if param.kind == "KEYWORD_ONLY" and not seen_star:
                parts.append("*")
                seen_star = True

            if param.kind == "VAR_POSITIONAL":
                seen_star = True
                p_str = f"*{param.name}"
                if param.annotation is not None:
                    p_str += f": {self._format_expr(param.annotation)}"
                parts.append(p_str)
                continue

            if param.kind == "VAR_KEYWORD":
                p_str = f"**{param.name}"
                if param.annotation is not None:
                    p_str += f": {self._format_expr(param.annotation)}"
                parts.append(p_str)
                continue

            # Standard parameter
            p_str = param.name
            if param.annotation is not None:
                p_str += f": {self._format_expr(param.annotation)}"
            if param.default is not None:
                eq_space = " = " if param.annotation is not None else "="
                p_str += f"{eq_space}{self._format_expr(param.default)}"
            parts.append(p_str)

        if had_pos_only:
            parts.append("/")

        return ", ".join(parts)

    # -------------------------------------------------------------------------
    # Expression Formatting with Precedence & Parenthesization
    # -------------------------------------------------------------------------

    def _format_expr(self, expr: Expression, parent_prec: int = 0, is_right: bool = False) -> str:
        """Formats an expression, wrapping in parentheses if required by precedence."""
        my_prec = get_precedence(expr)
        text = self._format_expr_inner(expr)

        # Check if parentheses are needed
        needs_parens = False
        if my_prec < parent_prec:
            needs_parens = True
        elif my_prec == parent_prec and parent_prec not in (PREC_PRIMARY, 0):
            # Same precedence: left-associative operators need parens for right child
            if is_right and parent_prec not in (PREC_POW,):
                needs_parens = True
            elif not is_right and parent_prec == PREC_POW:
                needs_parens = True

        if needs_parens:
            return f"({text})"
        return text

    def _format_expr_inner(self, expr: Expression) -> str:
        """Formats the core representation of an expression node."""
        # Literals
        if isinstance(expr, Identifier):
            return expr.name
        if isinstance(expr, Integer):
            return expr.raw_text if expr.raw_text is not None else str(expr.value)
        if isinstance(expr, Float):
            return expr.raw_text if expr.raw_text is not None else str(expr.value)
        if isinstance(expr, Complex):
            return expr.raw_text if expr.raw_text is not None else str(expr.value)
        if isinstance(expr, Boolean):
            return "sahi" if expr.value else "galat"
        if isinstance(expr, NoneLiteral):
            return "kuch_nahi"

        # String literals (raw_text byte-for-byte exact preservation)
        if isinstance(expr, String):
            if expr.raw_text is not None:
                return expr.raw_text
            prefix = expr.prefix or ""
            return f"{prefix}{repr(expr.value)}"

        # F-Strings
        if isinstance(expr, JoinedStr):
            if expr.raw_text is not None:
                return expr.raw_text
            # Reconstruct if raw_text missing
            parts_str = []
            for part in expr.parts:
                if isinstance(part, String):
                    parts_str.append(part.value)
                elif isinstance(part, FormattedValue):
                    val_str = self._format_expr(part.value)
                    conv_str = f"!{part.conversion}" if part.conversion else ""
                    spec_str = f":{part.format_spec}" if part.format_spec else ""
                    parts_str.append(f"{{{val_str}{conv_str}{spec_str}}}")
                else:
                    parts_str.append(self._format_expr(part))
            return f'f"{"".join(parts_str)}"'

        if isinstance(expr, FormattedValue):
            val_str = self._format_expr(expr.value)
            conv_str = f"!{expr.conversion}" if expr.conversion else ""
            spec_str = f":{expr.format_spec}" if expr.format_spec else ""
            return f"{{{val_str}{conv_str}{spec_str}}}"

        # Collections
        if isinstance(expr, ListLiteral):
            return f"[{', '.join(self._format_expr(e) for e in expr.elements)}]"
        if isinstance(expr, TupleLiteral):
            if not expr.elements:
                return "()"
            if len(expr.elements) == 1:
                return f"({self._format_expr(expr.elements[0])},)"
            return f"({', '.join(self._format_expr(e) for e in expr.elements)})"
        if isinstance(expr, DictLiteral):
            pairs = [f"{self._format_expr(k)}: {self._format_expr(v)}" for k, v in zip(expr.keys, expr.values)]
            return f"{{{', '.join(pairs)}}}"
        if isinstance(expr, SetLiteral):
            if not expr.elements:
                return "set()"
            return f"{{{', '.join(self._format_expr(e) for e in expr.elements)}}}"

        # Comprehensions
        if isinstance(expr, ListComprehension):
            return f"[{self._format_expr(expr.element)} {self._format_clauses(expr.clauses)}]"
        if isinstance(expr, DictComprehension):
            return f"{{{self._format_expr(expr.key)}: {self._format_expr(expr.value)} {self._format_clauses(expr.clauses)}}}"
        if isinstance(expr, SetComprehension):
            return f"{{{self._format_expr(expr.element)} {self._format_clauses(expr.clauses)}}}"
        if isinstance(expr, GeneratorExpression):
            return f"({self._format_expr(expr.element)} {self._format_clauses(expr.clauses)})"

        # Operators
        if isinstance(expr, BinaryOperation):
            prec = get_precedence(expr)
            left_str = self._format_expr(expr.left, parent_prec=prec, is_right=False)
            right_str = self._format_expr(expr.right, parent_prec=prec, is_right=True)
            return f"{left_str} {expr.op} {right_str}"

        if isinstance(expr, UnaryOperation):
            prec = get_precedence(expr)
            operand_str = self._format_expr(expr.operand, parent_prec=prec)
            if expr.op in ("nahi", "not"):
                return f"nahi {operand_str}"
            return f"{expr.op}{operand_str}"

        if isinstance(expr, Comparison):
            prec = get_precedence(expr)
            left_str = self._format_expr(expr.left, parent_prec=prec, is_right=False)
            right_str = self._format_expr(expr.right, parent_prec=prec, is_right=True)
            return f"{left_str} {expr.op} {right_str}"

        if isinstance(expr, BooleanOperation):
            prec = get_precedence(expr)
            op_name = "aur" if expr.op in ("aur", "and") else "ya"
            parts = [self._format_expr(v, parent_prec=prec) for v in expr.values]
            return f" {op_name} ".join(parts)

        # Walrus
        if isinstance(expr, AssignmentExpression):
            t_str = self._format_expr(expr.target)
            v_str = self._format_expr(expr.value)
            return f"({t_str} := {v_str})"

        # Starred & DoubleStarred
        if isinstance(expr, Starred):
            return f"*{self._format_expr(expr.value)}"
        if isinstance(expr, DoubleStarred):
            return f"**{self._format_expr(expr.value)}"

        # Function Calls
        if isinstance(expr, FunctionCall):
            func_str = self._format_expr(expr.func, parent_prec=PREC_PRIMARY)
            call_args = [self._format_expr(a) for a in expr.args]
            for k, v in expr.keywords.items():
                call_args.append(f"{k}={self._format_expr(v)}")
            return f"{func_str}({', '.join(call_args)})"

        # Indexing & Slicing
        if isinstance(expr, Indexing):
            val_str = self._format_expr(expr.value, parent_prec=PREC_PRIMARY)
            idx_str = self._format_expr(expr.index)
            return f"{val_str}[{idx_str}]"
        if isinstance(expr, Slice):
            low = self._format_expr(expr.lower) if expr.lower is not None else ""
            upp = self._format_expr(expr.upper) if expr.upper is not None else ""
            step = f":{self._format_expr(expr.step)}" if expr.step is not None else ""
            return f"{low}:{upp}{step}"

        # Attribute Access
        if isinstance(expr, AttributeAccess):
            val_str = self._format_expr(expr.value, parent_prec=PREC_PRIMARY)
            return f"{val_str}.{expr.attr}"

        # Lambda
        if isinstance(expr, LambdaExpression):
            params_part = f" {', '.join(expr.params)}" if expr.params else ""
            body_str = self._format_expr(expr.body)
            return f"sookshm{params_part}: {body_str}"

        # Yield & Yield From
        if isinstance(expr, Yield):
            if expr.value is None:
                return "upaj"
            return f"upaj {self._format_expr(expr.value)}"
        if isinstance(expr, YieldFrom):
            return f"upaj se {self._format_expr(expr.value)}"

        # Await
        if isinstance(expr, Await):
            return f"intezaar {self._format_expr(expr.value, parent_prec=PREC_PRIMARY)}"

        return str(expr)

    def _format_clauses(self, clauses: List[ComprehensionClause]) -> str:
        """Formats comprehension 'har ... mein ... [agar ...]*' clauses."""
        parts = []
        for c in clauses:
            async_prefix = "intezaar " if c.is_async else ""
            if isinstance(c.target, TupleLiteral) and c.target.elements:
                t_str = ", ".join(self._format_expr(e) for e in c.target.elements)
            else:
                t_str = self._format_expr(c.target)
            it_str = self._format_expr(c.iterable)
            clause_str = f"{async_prefix}har {t_str} mein {it_str}"
            for cond in c.conditions:
                clause_str += f" agar {self._format_expr(cond)}"
            parts.append(clause_str)
        return " ".join(parts)

    # -------------------------------------------------------------------------
    # Pattern Matching Formatting
    # -------------------------------------------------------------------------

    def _format_pattern(self, pat: MatchPattern) -> str:
        """Formats structural pattern matching patterns."""
        if isinstance(pat, MatchValue):
            return self._format_expr(pat.value)
        if isinstance(pat, MatchSingleton):
            if pat.value is True:
                return "sahi"
            if pat.value is False:
                return "galat"
            return "kuch_nahi"
        if isinstance(pat, MatchAs):
            if pat.pattern is None:
                return pat.name or "_"
            return f"{self._format_pattern(pat.pattern)} jaise {pat.name}"
        if isinstance(pat, MatchOr):
            return " | ".join(self._format_pattern(p) for p in pat.patterns)
        if isinstance(pat, MatchSequence):
            return f"[{', '.join(self._format_pattern(p) for p in pat.patterns)}]"
        if isinstance(pat, MatchStar):
            return f"*{pat.name}" if pat.name else "*_"
        if isinstance(pat, MatchMapping):
            items = [f"{self._format_expr(k)}: {self._format_pattern(p)}" for k, p in zip(pat.keys, pat.patterns)]
            if pat.rest:
                items.append(f"**{pat.rest}")
            return f"{{{', '.join(items)}}}"
        if isinstance(pat, MatchClass):
            cls_str = self._format_expr(pat.cls)
            args = [self._format_pattern(p) for p in pat.patterns]
            for k, p in zip(pat.kwd_attrs, pat.kwd_patterns):
                args.append(f"{k}={self._format_pattern(p)}")
            return f"{cls_str}({', '.join(args)})"
        return str(pat)


def format_source(source: str, indent_size: int = 4) -> str:
    """Formats Hinglish source code into canonical Hinglish.

    Args:
        source: Hinglish source code string.
        indent_size: Number of spaces for indentation (default: 4).

    Returns:
        Canonical formatted Hinglish source code.

    Raises:
        HinglishError: If source contains lexical or syntax errors.
    """
    formatter = HinglishFormatter(source, indent_size=indent_size)
    return formatter.format()


def format_file(
    path: Union[str, Path],
    check: bool = False,
    output: Optional[Union[str, Path]] = None,
    indent_size: int = 4,
) -> bool:
    """Formats a Hinglish file on disk.

    Args:
        path: Path to .hin file.
        check: If True, do not write changes; return True if already formatted, False if changes needed.
        output: Optional destination path to write formatted output.
        indent_size: Indentation size (default: 4).

    Returns:
        True if formatted / clean, False if --check failed (changes needed).
    """
    file_path = Path(path)
    source = file_path.read_text(encoding="utf-8")
    formatted = format_source(source, indent_size=indent_size)

    if check:
        return source == formatted

    if output is not None:
        out_path = Path(output)
        out_path.write_text(formatted, encoding="utf-8")
    else:
        file_path.write_text(formatted, encoding="utf-8")
    return True
