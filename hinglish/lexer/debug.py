"""Debugging utilities for inspecting Hinglish lexer token streams."""

from typing import List, Optional

from ..keywords import DEFAULT_KEYWORD_REGISTRY, KeywordRegistry
from .tokens import Token, TokenType


def format_tokens(
    tokens: List[Token],
    registry: Optional[KeywordRegistry] = None,
) -> str:
    """Formats a list of tokens into a human-readable tabular debug view.

    Example output:
    Line:Col   Type            Value                  Target (Python)
    ----------------------------------------------------------------------
    4:1        IDENTIFIER      'naam'                 -
    4:6        ASSIGN          '='                    -
    4:8        STRING          'Neeraj'               -
    4:16       NEWLINE         '\\n'                  -
    6:1        KEYWORD         'agar'                 if
    """
    reg = registry or DEFAULT_KEYWORD_REGISTRY
    lines = []
    header = f"{'Pos':<10} {'Type':<18} {'Value':<24} {'Python Target'}"
    lines.append(header)
    lines.append("-" * 65)

    for tok in tokens:
        pos_str = f"{tok.line}:{tok.column}"
        type_str = tok.type.name
        val_repr = repr(tok.value)
        if len(val_repr) > 22:
            val_repr = val_repr[:19] + "..."

        py_target = "-"
        if tok.type == TokenType.KEYWORD:
            target = reg.get_python_equivalent(str(tok.value))
            if target:
                py_target = f"→ {target}"
        elif tok.type == TokenType.BOOLEAN:
            py_target = f"→ {tok.value}"
        elif tok.type == TokenType.NONE:
            py_target = "→ None"
        elif tok.type == TokenType.IDENTIFIER:
            if reg.is_builtin_function(str(tok.value)):
                py_target = f"builtin ({reg.get_python_equivalent(str(tok.value))})"

        lines.append(f"{pos_str:<10} {type_str:<18} {val_repr:<24} {py_target}")

    return "\n".join(lines)


def print_tokens(
    tokens: List[Token],
    registry: Optional[KeywordRegistry] = None,
) -> None:
    """Prints a list of tokens in a readable table for development/debugging."""
    print(format_tokens(tokens, registry=registry))
