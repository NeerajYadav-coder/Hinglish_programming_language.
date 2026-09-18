"""AST inspection and formatting utilities for Hinglish."""

from typing import Any

from .nodes import ASTNode


def format_ast(node: Any, indent: int = 0) -> str:
    """Recursively formats an AST node into a clean, human-readable indented string."""
    pad = "  " * indent

    if node is None:
        return "None"

    if isinstance(node, (int, float, complex, str, bool)):
        return repr(node)

    if isinstance(node, list):
        if not node:
            return "[]"
        items = ",\n".join(f"{pad}  {format_ast(x, indent + 1)}" for x in node)
        return f"[\n{items}\n{pad}]"

    if isinstance(node, dict):
        if not node:
            return "{}"
        items = ",\n".join(
            f"{pad}  {k!r}: {format_ast(v, indent + 1)}" for k, v in node.items()
        )
        return f"{{\n{items}\n{pad}}}"

    if isinstance(node, ASTNode):
        cls_name = node.__class__.__name__
        fields = []
        for k, v in node.__dict__.items():
            if k in ("start_pos", "end_pos"):
                continue
            fields.append((k, v))

        if not fields:
            return f"{cls_name}()"

        field_strs = []
        for k, v in fields:
            v_str = format_ast(v, indent + 1)
            field_strs.append(f"{pad}  {k}={v_str}")

        body_str = ",\n".join(field_strs)
        return f"{cls_name}(\n{body_str}\n{pad})"

    return repr(node)


def print_ast(node: Any) -> None:
    """Prints the formatted AST to standard output."""
    print(format_ast(node))
