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


# Cache mapping normalized file paths to (source_code, line_map)
_MODULE_SOURCE_CACHE: Dict[str, Tuple[str, Dict[int, int]]] = {}


def register_source(filename: str, source_code: str, line_map: Dict[int, int]) -> None:
    """Registers source code and line map for a compiled Hinglish file."""
    _MODULE_SOURCE_CACHE[filename] = (source_code, line_map)
    try:
        resolved = str(Path(filename).resolve())
        _MODULE_SOURCE_CACHE[resolved] = (source_code, line_map)
    except Exception:
        pass


def format_runtime_exception(
    exc: Exception,
    filename: str,
    source_code: str,
    line_map: Dict[int, int],
) -> str:
    """Translates a Python runtime exception traceback back to Hinglish line numbers."""
    register_source(filename, source_code, line_map)

    tb = exc.__traceback__
    hin_frames: List[Dict[str, Any]] = []

    current = tb
    while current is not None:
        frame_filename = current.tb_frame.f_code.co_filename
        py_line = current.tb_lineno
        func_name = current.tb_frame.f_code.co_name

        # Lookup in cache
        cached = _MODULE_SOURCE_CACHE.get(frame_filename)
        if not cached:
            try:
                resolved = str(Path(frame_filename).resolve())
                cached = _MODULE_SOURCE_CACHE.get(resolved)
            except Exception:
                pass

        if cached:
            src, lmap = cached
            h_line = lmap.get(py_line, py_line)
            src_lines = src.splitlines()
            snippet = src_lines[h_line - 1].strip() if 1 <= h_line <= len(src_lines) else ""
            hin_frames.append({
                "filename": frame_filename,
                "line": h_line,
                "func": func_name,
                "snippet": snippet,
            })
        elif frame_filename == filename:
            h_line = line_map.get(py_line, py_line)
            src_lines = source_code.splitlines()
            snippet = src_lines[h_line - 1].strip() if 1 <= h_line <= len(src_lines) else ""
            hin_frames.append({
                "filename": filename,
                "line": h_line,
                "func": func_name,
                "snippet": snippet,
            })

        current = current.tb_next

    exc_name = type(exc).__name__
    exc_msg = str(exc)

    if not hin_frames:
        return f"Hinglish Runtime Error in '{filename}':\n{exc_name}: {exc_msg}"

    # Innermost frame
    innermost = hin_frames[-1]
    err_file = innermost["filename"]
    err_line = innermost["line"]
    source_snippet = f"\n  {innermost['snippet']}" if innermost["snippet"] else ""

    if len(hin_frames) > 1:
        # Multi-frame traceback representation
        tb_lines = ["Traceback (most recent call last):"]
        for f in hin_frames:
            tb_lines.append(f'  File "{f["filename"]}", line {f["line"]}, in {f["func"]}')
            if f["snippet"]:
                tb_lines.append(f'    {f["snippet"]}')
        tb_str = "\n".join(tb_lines) + "\n"
        return (
            f"{tb_str}"
            f"Hinglish Runtime Error in '{err_file}' (line {err_line}):"
            f"{source_snippet}\n"
            f"{exc_name}: {exc_msg}"
        )

    return (
        f"Hinglish Runtime Error in '{err_file}' (line {err_line}):"
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
    file_path = Path(path).resolve()
    if not file_path.is_file():
        raise FileNotFoundError(f"Hinglish file not found: {path}")

    from .importer import install_import_hook
    install_import_hook()

    file_dir = str(file_path.parent)
    if file_dir not in sys.path:
        sys.path.insert(0, file_dir)

    source_code = file_path.read_text(encoding="utf-8")
    return run(source_code, filename=str(file_path), globals_dict=globals_dict)


__all__ = ["run", "run_file", "format_runtime_exception", "register_source", "_MODULE_SOURCE_CACHE"]
