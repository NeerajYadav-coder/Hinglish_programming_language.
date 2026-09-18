"""Hinglish to Python Compiler and Code Generator.

Consumes a Hinglish Program AST and generates clean, valid, and verified Python 3 source code
along with source mapping for runtime traceback translation.
"""

import ast
from typing import Any, Dict, List, Optional, Tuple

from ..ast.nodes import (
    AnnAssign,
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
from ..exceptions import HinglishCompilerError
from ..keywords import DEFAULT_KEYWORD_REGISTRY, KeywordRegistry


class HinglishCompiler:
    """AST-driven code generator producing validated Python 3 source code."""

    PRECEDENCE = {
        "or": 1,
        "and": 2,
        "not": 3,
        "==": 4,
        "!=": 4,
        "<": 4,
        "<=": 4,
        ">": 4,
        ">=": 4,
        "is": 4,
        "is not": 4,
        "in": 4,
        "not in": 4,
        "|": 5,
        "^": 6,
        "&": 7,
        "<<": 8,
        ">>": 8,
        "+": 9,
        "-": 9,
        "*": 10,
        "/": 10,
        "//": 10,
        "%": 10,
        "@": 10,
        "unary": 11,
        "**": 12,
        "call": 13,
        "atom": 14,
    }

    def __init__(self, registry: Optional[KeywordRegistry] = None) -> None:
        self.registry = registry or DEFAULT_KEYWORD_REGISTRY
        self.line_map: Dict[int, int] = {}  # py_line (1-based) -> hin_line (1-based)

    def compile(self, program: Program) -> str:
        """Compiles a Hinglish Program AST into validated Python 3 source code."""
        py_source, _ = self.compile_with_map(program)
        return py_source

    def compile_with_map(self, program: Program) -> Tuple[str, Dict[int, int]]:
        """Compiles a Program AST and returns (py_source, line_map)."""
        if not isinstance(program, Program):
            raise HinglishCompilerError(f"Expected Program AST node, got {type(program).__name__}")

        self.line_map = {}
        py_lines: List[str] = []
        current_py_line = 1

        for stmt in program.body:
            stmt_lines = self.compile_statement_lines(stmt, indent_level=0)
            for py_str, hin_line in stmt_lines:
                self.line_map[current_py_line] = hin_line
                py_lines.append(py_str)
                current_py_line += 1

        py_source = "\n".join(py_lines)
        if py_source and not py_source.endswith("\n"):
            py_source += "\n"

        # Validate syntax using Python's standard ast module
        self._validate_python_syntax(py_source)
        return py_source, self.line_map

    def _validate_python_syntax(self, py_source: str) -> None:
        """Validates that the generated Python source is parseable by Python's ast parser."""
        if not py_source.strip():
            return
        try:
            ast.parse(py_source)
        except SyntaxError as err:
            raise HinglishCompilerError(
                f"Generated Python code contains syntax error: {err.msg}",
                line=err.lineno,
                column=err.offset,
                source_line=err.text,
            ) from err

    # -------------------------------------------------------------------------
    # Statement Compilation
    # -------------------------------------------------------------------------

    def compile_statement(self, stmt: Statement, indent_level: int = 0) -> str:
        """Compiles a single statement with proper indentation."""
        lines = [line_str for line_str, _ in self.compile_statement_lines(stmt, indent_level)]
        return "\n".join(lines)

    def compile_statement_lines(self, stmt: Statement, indent_level: int = 0) -> List[Tuple[str, int]]:
        """Compiles a statement into a list of (python_line, hinglish_line) pairs."""
        indent = "    " * indent_level
        hin_line = stmt.start_pos.line if stmt.start_pos else 1

        if isinstance(stmt, ExpressionStatement):
            expr_code = self.compile_expression(stmt.expr)
            return [(f"{indent}{expr_code}", hin_line)]

        if isinstance(stmt, Assignment):
            target_code = self.compile_expression(stmt.target)
            value_code = self.compile_expression(stmt.value)
            return [(f"{indent}{target_code} {stmt.op} {value_code}", hin_line)]

        if isinstance(stmt, If):
            return self._compile_if_lines(stmt, indent_level)

        if isinstance(stmt, While):
            cond_code = self.compile_expression(stmt.condition)
            lines = [(f"{indent}while {cond_code}:", hin_line)]
            lines.extend(self._compile_body_lines(stmt.body, indent_level + 1, hin_line))
            return lines

        if isinstance(stmt, For):
            target_code = self.compile_expression(stmt.target)
            iter_code = self.compile_expression(stmt.iterable)
            for_kw = "async for" if getattr(stmt, "is_async", False) else "for"
            lines = [(f"{indent}{for_kw} {target_code} in {iter_code}:", hin_line)]
            lines.extend(self._compile_body_lines(stmt.body, indent_level + 1, hin_line))
            return lines

        if isinstance(stmt, FunctionDefinition):
            lines = []
            if stmt.decorators:
                for dec in stmt.decorators:
                    dec_hin = dec.start_pos.line if dec.start_pos else hin_line
                    lines.append((f"{indent}@{self.compile_expression(dec)}", dec_hin))
            def_kw = "async def" if getattr(stmt, "is_async", False) else "def"
            if stmt.parameters:
                params_str = self._compile_parameters(stmt.parameters)
            else:
                params_str = ", ".join(stmt.params)
            ret_str = f" -> {self.compile_expression(stmt.returns)}" if stmt.returns else ""
            lines.append((f"{indent}{def_kw} {stmt.name}({params_str}){ret_str}:", hin_line))
            lines.extend(self._compile_body_lines(stmt.body, indent_level + 1, hin_line))
            return lines

        if isinstance(stmt, ClassDefinition):
            lines = []
            if stmt.decorators:
                for dec in stmt.decorators:
                    dec_hin = dec.start_pos.line if dec.start_pos else hin_line
                    lines.append((f"{indent}@{self.compile_expression(dec)}", dec_hin))
            bases_str = ""
            if stmt.bases:
                bases_compiled = [self.compile_expression(b) for b in stmt.bases]
                bases_str = f"({', '.join(bases_compiled)})"
            lines.append((f"{indent}class {stmt.name}{bases_str}:", hin_line))
            lines.extend(self._compile_body_lines(stmt.body, indent_level + 1, hin_line))
            return lines

        if isinstance(stmt, Try):
            lines = [(f"{indent}try:", hin_line)]
            lines.extend(self._compile_body_lines(stmt.body, indent_level + 1, hin_line))
            for h in stmt.handlers:
                h_hin = h.start_pos.line if h.start_pos else hin_line
                clause = f"{indent}except"
                if h.type is not None:
                    clause += f" {self.compile_expression(h.type)}"
                    if h.name:
                        clause += f" as {h.name}"
                clause += ":"
                lines.append((clause, h_hin))
                lines.extend(self._compile_body_lines(h.body, indent_level + 1, h_hin))
            if stmt.else_body is not None:
                else_hin = stmt.else_body[0].start_pos.line if stmt.else_body and stmt.else_body[0].start_pos else hin_line
                lines.append((f"{indent}else:", else_hin))
                lines.extend(self._compile_body_lines(stmt.else_body, indent_level + 1, else_hin))
            if stmt.finally_body is not None:
                fin_hin = stmt.finally_body[0].start_pos.line if stmt.finally_body and stmt.finally_body[0].start_pos else hin_line
                lines.append((f"{indent}finally:", fin_hin))
                lines.extend(self._compile_body_lines(stmt.finally_body, indent_level + 1, fin_hin))
            return lines

        if isinstance(stmt, Raise):
            if stmt.exc is not None:
                exc_code = self.compile_expression(stmt.exc)
                return [(f"{indent}raise {exc_code}", hin_line)]
            return [(f"{indent}raise", hin_line)]

        if isinstance(stmt, With):
            items_parts = []
            for item in stmt.items:
                c_code = self.compile_expression(item.context_expr)
                if item.optional_vars is not None:
                    v_code = self.compile_expression(item.optional_vars)
                    items_parts.append(f"{c_code} as {v_code}")
                else:
                    items_parts.append(c_code)
            with_kw = "async with" if getattr(stmt, "is_async", False) else "with"
            lines = [(f"{indent}{with_kw} {', '.join(items_parts)}:", hin_line)]
            lines.extend(self._compile_body_lines(stmt.body, indent_level + 1, hin_line))
            return lines

        if isinstance(stmt, AnnAssign):
            target_code = self.compile_expression(stmt.target)
            ann_code = self.compile_expression(stmt.annotation)
            if stmt.value is not None:
                val_code = self.compile_expression(stmt.value)
                return [(f"{indent}{target_code}: {ann_code} = {val_code}", hin_line)]
            return [(f"{indent}{target_code}: {ann_code}", hin_line)]

        if isinstance(stmt, Match):
            subj_code = self.compile_expression(stmt.subject)
            lines = [(f"{indent}match {subj_code}:", hin_line)]
            for case in stmt.cases:
                c_hin = case.start_pos.line if case.start_pos else hin_line
                pat_code = self.compile_pattern(case.pattern)
                guard_code = f" if {self.compile_expression(case.guard)}" if case.guard is not None else ""
                lines.append((f"{indent}    case {pat_code}{guard_code}:", c_hin))
                lines.extend(self._compile_body_lines(case.body, indent_level + 2, c_hin))
            return lines

        if isinstance(stmt, Return):
            if stmt.value is not None:
                val_code = self.compile_expression(stmt.value)
                return [(f"{indent}return {val_code}", hin_line)]
            return [(f"{indent}return", hin_line)]

        if isinstance(stmt, Pass):
            return [(f"{indent}pass", hin_line)]

        if isinstance(stmt, Break):
            return [(f"{indent}break", hin_line)]

        if isinstance(stmt, Continue):
            return [(f"{indent}continue", hin_line)]

        if isinstance(stmt, Import):
            names_parts = []
            for name, alias in stmt.names:
                if alias:
                    names_parts.append(f"{name} as {alias}")
                else:
                    names_parts.append(name)
            return [(f"{indent}import {', '.join(names_parts)}", hin_line)]

        if isinstance(stmt, FromImport):
            names_parts = []
            for name, alias in stmt.names:
                if alias:
                    names_parts.append(f"{name} as {alias}")
                else:
                    names_parts.append(name)
            return [(f"{indent}from {stmt.module} import {', '.join(names_parts)}", hin_line)]

        if isinstance(stmt, Yield):
            if stmt.value is not None:
                val_code = self.compile_expression(stmt.value)
                return [(f"{indent}yield {val_code}", hin_line)]
            return [(f"{indent}yield", hin_line)]

        if isinstance(stmt, YieldFrom):
            val_code = self.compile_expression(stmt.value)
            return [(f"{indent}yield from {val_code}", hin_line)]

        line = stmt.start_pos.line if stmt.start_pos else None
        col = stmt.start_pos.column if stmt.start_pos else None
        raise HinglishCompilerError(
            f"Unsupported statement node '{type(stmt).__name__}'",
            line=line,
            column=col,
        )

    def _compile_if_lines(self, stmt: If, indent_level: int) -> List[Tuple[str, int]]:
        """Compiles an If statement into (python_line, hinglish_line) pairs."""
        indent = "    " * indent_level
        hin_line = stmt.start_pos.line if stmt.start_pos else 1
        cond_code = self.compile_expression(stmt.condition)

        lines: List[Tuple[str, int]] = [(f"{indent}if {cond_code}:", hin_line)]
        lines.extend(self._compile_body_lines(stmt.body, indent_level + 1, hin_line))

        for elif_clause in stmt.elif_clauses:
            elif_hin = elif_clause.start_pos.line if elif_clause.start_pos else hin_line
            elif_cond = self.compile_expression(elif_clause.condition)
            lines.append((f"{indent}elif {elif_cond}:", elif_hin))
            lines.extend(self._compile_body_lines(elif_clause.body, indent_level + 1, elif_hin))

        if stmt.else_body is not None:
            else_hin = stmt.else_body[0].start_pos.line if stmt.else_body and stmt.else_body[0].start_pos else hin_line
            lines.append((f"{indent}else:", else_hin))
            lines.extend(self._compile_body_lines(stmt.else_body, indent_level + 1, else_hin))

        return lines

    def _compile_body_lines(
        self, body: List[Statement], indent_level: int, fallback_hin_line: int
    ) -> List[Tuple[str, int]]:
        """Compiles block statements into a list of (python_line, hinglish_line) pairs."""
        if not body:
            indent = "    " * indent_level
            return [(f"{indent}pass", fallback_hin_line)]

        lines: List[Tuple[str, int]] = []
        for s in body:
            lines.extend(self.compile_statement_lines(s, indent_level=indent_level))
        return lines

    def _compile_body(self, body: List[Statement], indent_level: int) -> str:
        """Compiles a list of statements forming a block body."""
        lines = [line_str for line_str, _ in self._compile_body_lines(body, indent_level, 1)]
        return "\n".join(lines)

    def _compile_comprehension_clauses(self, clauses: List[ComprehensionClause]) -> str:
        """Compiles comprehension clauses ('for ... in ... if ...')."""
        parts: List[str] = []
        for clause in clauses:
            target_str = self.compile_expression(clause.target)
            iter_str = self.compile_expression(clause.iterable)
            parts.append(f"for {target_str} in {iter_str}")
            for cond in clause.conditions:
                cond_str = self.compile_expression(cond)
                parts.append(f"if {cond_str}")
        return " ".join(parts)

    def _compile_parameters(self, parameters: List[Parameter]) -> str:
        """Compiles a list of Parameter AST nodes into a Python parameter list."""
        parts: List[str] = []
        pos_only_count = sum(1 for p in parameters if p.kind == "POSITIONAL_ONLY")
        has_var_positional = any(p.kind == "VAR_POSITIONAL" for p in parameters)
        bare_star_emitted = False
        pos_only_seen = 0

        for p in parameters:
            if p.kind == "KEYWORD_ONLY" and not has_var_positional and not bare_star_emitted:
                parts.append("*")
                bare_star_emitted = True

            if p.kind == "VAR_POSITIONAL":
                p_str = f"*{p.name}"
                if p.annotation is not None:
                    p_str += f": {self.compile_expression(p.annotation)}"
            elif p.kind == "VAR_KEYWORD":
                p_str = f"**{p.name}"
                if p.annotation is not None:
                    p_str += f": {self.compile_expression(p.annotation)}"
            else:
                p_str = p.name
                if p.annotation is not None:
                    p_str += f": {self.compile_expression(p.annotation)}"
                if p.default is not None:
                    p_str += f"={self.compile_expression(p.default)}"

            parts.append(p_str)

            if p.kind == "POSITIONAL_ONLY":
                pos_only_seen += 1
                if pos_only_seen == pos_only_count:
                    parts.append("/")

        return ", ".join(parts)

    def compile_pattern(self, pattern: MatchPattern) -> str:
        """Compiles a MatchPattern AST node into valid Python 3.10+ match pattern syntax."""
        if isinstance(pattern, MatchValue):
            return self.compile_expression(pattern.value)

        if isinstance(pattern, MatchSingleton):
            return repr(pattern.value)

        if isinstance(pattern, MatchStar):
            if pattern.name:
                return f"*{pattern.name}"
            return "*_"

        if isinstance(pattern, MatchAs):
            if pattern.pattern is None:
                return pattern.name if pattern.name is not None else "_"
            pat_str = self.compile_pattern(pattern.pattern)
            if pattern.name is not None:
                return f"{pat_str} as {pattern.name}"
            return pat_str

        if isinstance(pattern, MatchOr):
            parts = [self.compile_pattern(p) for p in pattern.patterns]
            return " | ".join(parts)

        if isinstance(pattern, MatchSequence):
            parts = [self.compile_pattern(p) for p in pattern.patterns]
            return f"[{', '.join(parts)}]"

        if isinstance(pattern, MatchMapping):
            parts = []
            for k, p in zip(pattern.keys, pattern.patterns):
                k_str = self.compile_expression(k)
                p_str = self.compile_pattern(p)
                parts.append(f"{k_str}: {p_str}")
            if pattern.rest:
                parts.append(f"**{pattern.rest}")
            return f"{{{', '.join(parts)}}}"

        if isinstance(pattern, MatchClass):
            cls_str = self.compile_expression(pattern.cls)
            pos_args = [self.compile_pattern(p) for p in pattern.patterns]
            kwd_args = [
                f"{attr}={self.compile_pattern(p)}"
                for attr, p in zip(pattern.kwd_attrs, pattern.kwd_patterns)
            ]
            all_args = pos_args + kwd_args
            return f"{cls_str}({', '.join(all_args)})"

        raise HinglishCompilerError(f"Unsupported match pattern node '{type(pattern).__name__}'")

    # -------------------------------------------------------------------------
    # Expression Compilation with Precedence Handling
    # -------------------------------------------------------------------------

    def compile_expression(self, expr: Expression, parent_prec: int = 0) -> str:
        """Compiles an expression, wrapping in parentheses if required by precedence."""
        # 1. Literals & Identifiers
        if isinstance(expr, Identifier):
            if self.registry.is_builtin_function(expr.name):
                return self.registry.get_python_equivalent(expr.name) or expr.name
            return expr.name

        if isinstance(expr, Integer):
            return repr(expr.value)

        if isinstance(expr, Float):
            return repr(expr.value)

        if isinstance(expr, Complex):
            return repr(expr.value)

        if isinstance(expr, String):
            prefix = expr.prefix or ""
            return f"{prefix}{repr(expr.value)}"

        if isinstance(expr, FormattedValue):
            val_str = self.compile_expression(expr.value)
            conv_str = f"!{expr.conversion}" if expr.conversion else ""
            spec_str = f":{expr.format_spec}" if expr.format_spec else ""
            return f"{{{val_str}{conv_str}{spec_str}}}"

        if isinstance(expr, JoinedStr):
            pieces = []
            for part in expr.parts:
                if isinstance(part, String):
                    s = (
                        part.value.replace("\\", "\\\\")
                        .replace('"', '\\"')
                        .replace("\n", "\\n")
                        .replace("\r", "\\r")
                        .replace("\t", "\\t")
                        .replace("{", "{{")
                        .replace("}", "}}")
                    )
                    pieces.append(s)
                elif isinstance(part, FormattedValue):
                    val_str = self.compile_expression(part.value)
                    conv_str = f"!{part.conversion}" if part.conversion else ""
                    spec_str = f":{part.format_spec}" if part.format_spec else ""
                    pieces.append(f"{{{val_str}{conv_str}{spec_str}}}")
                else:
                    pieces.append(self.compile_expression(part))
            return f'f"{"".join(pieces)}"'

        if isinstance(expr, Boolean):
            return "True" if expr.value else "False"

        if isinstance(expr, NoneLiteral):
            return "None"

        # 2. Collections
        if isinstance(expr, ListLiteral):
            elements = [self.compile_expression(e) for e in expr.elements]
            return f"[{', '.join(elements)}]"

        if isinstance(expr, DictLiteral):
            items = []
            for k, v in zip(expr.keys, expr.values):
                if k is None or isinstance(k, NoneLiteral) or isinstance(v, DoubleStarred):
                    if isinstance(v, DoubleStarred):
                        items.append(f"**{self.compile_expression(v.value)}")
                    else:
                        items.append(f"**{self.compile_expression(v)}")
                else:
                    items.append(f"{self.compile_expression(k)}: {self.compile_expression(v)}")
            return f"{{{', '.join(items)}}}"

        if isinstance(expr, TupleLiteral):
            if not expr.elements:
                return "()"
            if len(expr.elements) == 1:
                return f"({self.compile_expression(expr.elements[0])},)"
            elements = [self.compile_expression(e) for e in expr.elements]
            return f"({', '.join(elements)})"

        if isinstance(expr, SetLiteral):
            elements = [self.compile_expression(e) for e in expr.elements]
            return f"{{{', '.join(elements)}}}"

        if isinstance(expr, ListComprehension):
            elt_str = self.compile_expression(expr.element)
            clauses_str = self._compile_comprehension_clauses(expr.clauses)
            return f"[{elt_str} {clauses_str}]"

        if isinstance(expr, DictComprehension):
            key_str = self.compile_expression(expr.key)
            val_str = self.compile_expression(expr.value)
            clauses_str = self._compile_comprehension_clauses(expr.clauses)
            return f"{{{key_str}: {val_str} {clauses_str}}}"

        if isinstance(expr, SetComprehension):
            elt_str = self.compile_expression(expr.element)
            clauses_str = self._compile_comprehension_clauses(expr.clauses)
            return f"{{{elt_str} {clauses_str}}}"

        if isinstance(expr, GeneratorExpression):
            elt_str = self.compile_expression(expr.element)
            clauses_str = self._compile_comprehension_clauses(expr.clauses)
            return f"({elt_str} {clauses_str})"

        if isinstance(expr, LambdaExpression):
            params_str = ", ".join(expr.params)
            body_str = self.compile_expression(expr.body)
            res = f"lambda {params_str}: {body_str}" if params_str else f"lambda: {body_str}"
            if parent_prec > 0:
                return f"({res})"
            return res

        if isinstance(expr, Yield):
            if expr.value is not None:
                val_str = self.compile_expression(expr.value)
                res = f"yield {val_str}"
            else:
                res = "yield"
            if parent_prec > 0:
                return f"({res})"
            return res

        if isinstance(expr, YieldFrom):
            val_str = self.compile_expression(expr.value)
            res = f"yield from {val_str}"
            if parent_prec > 0:
                return f"({res})"
            return res

        if isinstance(expr, Await):
            current_prec = self.PRECEDENCE.get("unary", 11)
            val_str = self.compile_expression(expr.value, parent_prec=current_prec)
            res = f"await {val_str}"
            if current_prec < parent_prec:
                return f"({res})"
            return res

        if isinstance(expr, AssignmentExpression):
            target_str = self.compile_expression(expr.target)
            val_str = self.compile_expression(expr.value)
            return f"({target_str} := {val_str})"

        if isinstance(expr, Starred):
            return f"*{self.compile_expression(expr.value)}"

        if isinstance(expr, DoubleStarred):
            return f"**{self.compile_expression(expr.value)}"

        # 3. Binary Operations
        if isinstance(expr, BinaryOperation):
            current_prec = self.PRECEDENCE.get(expr.op, 0)
            left_prec = current_prec if expr.op != "**" else current_prec + 1
            right_prec = current_prec + 1 if expr.op != "**" else current_prec

            left_str = self.compile_expression(expr.left, parent_prec=left_prec)
            right_str = self.compile_expression(expr.right, parent_prec=right_prec)
            res = f"{left_str} {expr.op} {right_str}"

            if current_prec < parent_prec:
                return f"({res})"
            return res

        # 4. Unary Operations
        if isinstance(expr, UnaryOperation):
            current_prec = self.PRECEDENCE.get("not" if expr.op == "not" else "unary", 11)
            op_str = f"{expr.op} " if expr.op == "not" else expr.op
            operand_str = self.compile_expression(expr.operand, parent_prec=current_prec)
            res = f"{op_str}{operand_str}"
            if current_prec < parent_prec:
                return f"({res})"
            return res

        # 5. Comparisons
        if isinstance(expr, Comparison):
            current_prec = self.PRECEDENCE.get(expr.op, 4)
            left_str = self.compile_expression(expr.left, parent_prec=current_prec + 1)
            right_str = self.compile_expression(expr.right, parent_prec=current_prec + 1)
            res = f"{left_str} {expr.op} {right_str}"
            if current_prec < parent_prec:
                return f"({res})"
            return res

        # 6. Boolean Operations (and, or)
        if isinstance(expr, BooleanOperation):
            current_prec = self.PRECEDENCE.get(expr.op, 1)
            parts = [
                self.compile_expression(val, parent_prec=current_prec + 1)
                for val in expr.values
            ]
            res = f" {expr.op} ".join(parts)
            if current_prec < parent_prec:
                return f"({res})"
            return res

        # 7. Function Call
        if isinstance(expr, FunctionCall):
            func_str = self.compile_expression(expr.func, parent_prec=self.PRECEDENCE["call"])
            pos_args = [self.compile_expression(a) for a in expr.args if not isinstance(a, DoubleStarred)]
            kw_args = [f"{k}={self.compile_expression(v)}" for k, v in expr.keywords.items()]
            star_star_args = [self.compile_expression(a) for a in expr.args if isinstance(a, DoubleStarred)]
            all_args = pos_args + kw_args + star_star_args
            return f"{func_str}({', '.join(all_args)})"

        # 8. Attribute Access
        if isinstance(expr, AttributeAccess):
            val_str = self.compile_expression(expr.value, parent_prec=self.PRECEDENCE["call"])
            return f"{val_str}.{expr.attr}"

        # 9. Indexing
        if isinstance(expr, Indexing):
            val_str = self.compile_expression(expr.value, parent_prec=self.PRECEDENCE["call"])
            idx_str = self.compile_expression(expr.index)
            return f"{val_str}[{idx_str}]"

        # 10. Slice
        if isinstance(expr, Slice):
            lower_str = self.compile_expression(expr.lower) if expr.lower else ""
            upper_str = self.compile_expression(expr.upper) if expr.upper else ""
            if expr.step:
                step_str = self.compile_expression(expr.step)
                return f"{lower_str}:{upper_str}:{step_str}"
            return f"{lower_str}:{upper_str}"

        line = expr.start_pos.line if expr.start_pos else None
        col = expr.start_pos.column if expr.start_pos else None
        raise HinglishCompilerError(
            f"Unsupported expression node '{type(expr).__name__}'",
            line=line,
            column=col,
        )
