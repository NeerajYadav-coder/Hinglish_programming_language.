"""Execution Engine for the Hinglish programming language.

Handles end-to-end execution of Hinglish source code and files with namespace management,
code object compilation, and source-mapped traceback translation.
"""

import sys
import traceback
from pathlib import Path
from typing import Any, Dict, Optional, Tuple, Union

from ..compiler import HinglishCompiler
from ..exceptions import HinglishError
from ..parser import parse
from .context import get_default_globals


def format_runtime_exception(
    exc: Exception,
    filename: str,
    source_code: str,
    line_map: Dict[int, int],
) -> str:
    """Translates a Python runtime exception traceback back to Hinglish line numbers."""
    tb = exc.__traceback__
    hin_line: Optional[int] = None

    # Walk traceback frames in reverse to find the innermost frame in our file
    current = tb
    while current is not None:
        frame_filename = current.tb_frame.f_code.co_filename
        if frame_filename == filename:
            py_line = current.tb_lineno
            hin_line = line_map.get(py_line, py_line)
        current = current.tb_next

    # Extract source line snippet if line is known
    source_snippet = ""
    lines = source_code.splitlines()
    if hin_line is not None and 1 <= hin_line <= len(lines):
        source_snippet = f"\n  {lines[hin_line - 1].strip()}"

    loc_str = f"line {hin_line}" if hin_line is not None else "unknown location"
    exc_name = type(exc).__name__
    exc_msg = str(exc)

    return (
        f"Hinglish Runtime Error in '{filename}' ({loc_str}):"
        f"{source_snippet}\n"
        f"{exc_name}: {exc_msg}"
    )


def run(
    source_code: str,
    filename: str = "<string>",
    globals_dict: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """Compiles and executes Hinglish source code, returning the execution namespace."""
    if globals_dict is None:
        globals_dict = get_default_globals()
        globals_dict["__file__"] = filename

    # 1. Parse into Hinglish AST
    program_ast = parse(source_code)

    # 2. Compile into Python source with line map
    compiler = HinglishCompiler()
    py_source, line_map = compiler.compile_with_map(program_ast)

    # 3. Compile Python source into bytecode
    code_obj = compile(py_source, filename, "exec")

    # 4. Execute in namespace
    try:
        exec(code_obj, globals_dict)
    except Exception as exc:
        formatted = format_runtime_exception(exc, filename, source_code, line_map)
        raise RuntimeError(formatted) from exc

    return globals_dict


def run_file(
    path: Union[str, Path],
    globals_dict: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """Reads, compiles, and executes a .hin script file."""
    file_path = Path(path)
    if not file_path.is_file():
        raise FileNotFoundError(f"Hinglish file not found: {path}")

    source_code = file_path.read_text(encoding="utf-8")
    return run(source_code, filename=str(file_path), globals_dict=globals_dict)


__all__ = ["run", "run_file", "format_runtime_exception"]
