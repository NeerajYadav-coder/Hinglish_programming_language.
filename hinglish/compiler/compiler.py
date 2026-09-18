"""Hinglish to Python Compiler and Code Generator.

Consumes a Hinglish Program AST and generates clean, valid, and verified Python 3 source code.
"""

import ast
from typing import Any, Dict, List, Optional, Tuple

from ..ast.nodes import (
    Assignment,
    ASTNode,
    AttributeAccess,
    BinaryOperation,
    Boolean,
    BooleanOperation,
    Break,
    Comparison,
    Complex,
    Continue,
    DictLiteral,
    ElifClause,
    Expression,
    ExpressionStatement,
    Float,
    For,
    FromImport,
    FunctionCall,
    FunctionDefinition,
    Identifier,
    If,
    Import,
    Indexing,
    Integer,
    ListLiteral,
    NoneLiteral,
    Pass,
    Program,
    Return,
    Slice,
    Statement,
    String,
    TupleLiteral,
    UnaryOperation,
    While,
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
        self.line_map: Dict[int, int] = {}  # py_line -> hin_line

    def compile(self, program: Program) -> str:
        """Compiles a Hinglish Program AST into validated Python 3 source code."""
        if not isinstance(program, Program):
            raise HinglishCompilerError(f"Expected Program AST node, got {type(program).__name__}")

        lines: List[str] = []
        for stmt in program.body:
            stmt_code = self.compile_statement(stmt, indent_level=0)
            if stmt_code:
                lines.append(stmt_code)

        py_source = "\n".join(lines)
        if py_source and not py_source.endswith("\n"):
            py_source += "\n"

        # Validate syntax using Python's standard ast module
        self._validate_python_syntax(py_source)
        return py_source

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
        indent = "    " * indent_level

        if isinstance(stmt, ExpressionStatement):
            expr_code = self.compile_expression(stmt.expr)
            return f"{indent}{expr_code}"

        if isinstance(stmt, Assignment):
            target_code = self.compile_expression(stmt.target)
            value_code = self.compile_expression(stmt.value)
            return f"{indent}{target_code} {stmt.op} {value_code}"

        if isinstance(stmt, If):
            return self._compile_if(stmt, indent_level)

        if isinstance(stmt, While):
            cond_code = self.compile_expression(stmt.condition)
            body_code = self._compile_body(stmt.body, indent_level + 1)
            return f"{indent}while {cond_code}:\n{body_code}"

        if isinstance(stmt, For):
            target_code = self.compile_expression(stmt.target)
            iter_code = self.compile_expression(stmt.iterable)
            body_code = self._compile_body(stmt.body, indent_level + 1)
            return f"{indent}for {target_code} in {iter_code}:\n{body_code}"

        if isinstance(stmt, FunctionDefinition):
            params_str = ", ".join(stmt.params)
            body_code = self._compile_body(stmt.body, indent_level + 1)
            return f"{indent}def {stmt.name}({params_str}):\n{body_code}"

        if isinstance(stmt, Return):
            if stmt.value is not None:
                val_code = self.compile_expression(stmt.value)
                return f"{indent}return {val_code}"
            return f"{indent}return"

        if isinstance(stmt, Pass):
            return f"{indent}pass"

        if isinstance(stmt, Break):
            return f"{indent}break"

        if isinstance(stmt, Continue):
            return f"{indent}continue"

        if isinstance(stmt, Import):
            names_parts = []
            for name, alias in stmt.names:
                if alias:
                    names_parts.append(f"{name} as {alias}")
                else:
                    names_parts.append(name)
            return f"{indent}import {', '.join(names_parts)}"

        if isinstance(stmt, FromImport):
            names_parts = []
            for name, alias in stmt.names:
                if alias:
                    names_parts.append(f"{name} as {alias}")
                else:
                    names_parts.append(name)
            return f"{indent}from {stmt.module} import {', '.join(names_parts)}"

        line = stmt.start_pos.line if stmt.start_pos else None
        col = stmt.start_pos.column if stmt.start_pos else None
        raise HinglishCompilerError(
            f"Unsupported statement node '{type(stmt).__name__}'",
            line=line,
            column=col,
        )

    def _compile_if(self, stmt: If, indent_level: int) -> str:
        """Compiles an If statement with elif and else branches."""
        indent = "    " * indent_level
        cond_code = self.compile_expression(stmt.condition)
        body_code = self._compile_body(stmt.body, indent_level + 1)

        result = [f"{indent}if {cond_code}:\n{body_code}"]

        for elif_clause in stmt.elif_clauses:
            elif_cond = self.compile_expression(elif_clause.condition)
            elif_body = self._compile_body(elif_clause.body, indent_level + 1)
            result.append(f"{indent}elif {elif_cond}:\n{elif_body}")

        if stmt.else_body is not None:
            else_body = self._compile_body(stmt.else_body, indent_level + 1)
            result.append(f"{indent}else:\n{else_body}")

        return "\n".join(result)

    def _compile_body(self, body: List[Statement], indent_level: int) -> str:
        """Compiles a list of statements forming a block body."""
        if not body:
            return f"{'    ' * indent_level}pass"

        lines: List[str] = []
        for s in body:
            compiled = self.compile_statement(s, indent_level=indent_level)
            if compiled:
                lines.append(compiled)
        return "\n".join(lines)

    # -------------------------------------------------------------------------
    # Expression Compilation with Precedence Handling
    # -------------------------------------------------------------------------

    def compile_expression(self, expr: Expression, parent_prec: int = 0) -> str:
        """Compiles an expression, wrapping in parentheses if required by precedence."""
        # 1. Literals & Identifiers
        if isinstance(expr, Identifier):
            # Check if identifier is a mapped builtin (e.g. dikhao -> print, lambai -> len)
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

        if isinstance(expr, Boolean):
            return "True" if expr.value else "False"

        if isinstance(expr, NoneLiteral):
            return "None"

        # 2. Collections
        if isinstance(expr, ListLiteral):
            elements = [self.compile_expression(e) for e in expr.elements]
            return f"[{', '.join(elements)}]"

        if isinstance(expr, DictLiteral):
            items = [
                f"{self.compile_expression(k)}: {self.compile_expression(v)}"
                for k, v in zip(expr.keys, expr.values)
            ]
            return f"{{{', '.join(items)}}}"

        if isinstance(expr, TupleLiteral):
            if not expr.elements:
                return "()"
            if len(expr.elements) == 1:
                return f"({self.compile_expression(expr.elements[0])},)"
            elements = [self.compile_expression(e) for e in expr.elements]
            return f"({', '.join(elements)})"

        # 3. Binary Operations
        if isinstance(expr, BinaryOperation):
            current_prec = self.PRECEDENCE.get(expr.op, 0)
            # For right-associative power (**), right child keeps same prec
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
            args_list = [self.compile_expression(a) for a in expr.args]
            for k, v in expr.keywords.items():
                args_list.append(f"{k}={self.compile_expression(v)}")
            return f"{func_str}({', '.join(args_list)})"

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
