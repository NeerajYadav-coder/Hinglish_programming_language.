"""Interactive REPL (Read-Eval-Print Loop) for the Hinglish programming language."""

import sys
from typing import Any, Dict, List, Optional

from .. import __version__
from ..ast.nodes import ExpressionStatement
from ..compiler import HinglishCompiler
from ..exceptions import HinglishError
from ..parser import parse
from .context import get_default_globals


class HinglishREPL:
    """Interactive stateful REPL for Hinglish sessions."""

    def __init__(self, globals_dict: Optional[Dict[str, Any]] = None) -> None:
        self.namespace: Dict[str, Any] = (
            globals_dict if globals_dict is not None else get_default_globals()
        )
        self.namespace["__name__"] = "__repl__"
        self.namespace["madad"] = self._help
        self.buffer: List[str] = []
        self.in_block: bool = False

    def _help(self) -> None:
        """Built-in help command for the REPL."""
        print(
            "Hinglish REPL Quick Reference:\n"
            "  dikhao(...)     - Print output\n"
            "  agar / warna    - If / Else conditional\n"
            "  jabtak / har    - While / For loops\n"
            "  kaam / wapas    - Function definition & return\n"
            "  sahi / galat    - True / False\n"
            "  kuch_nahi       - None\n"
            "  laao <mod>      - Import Python module\n"
            "  Press Ctrl+C or Ctrl+D to exit.\n"
        )

    def run_line(self, line: str) -> Optional[Any]:
        """Feeds a single line of input to the REPL state machine.

        Returns the evaluated result (for expressions) or None.
        """
        # Block buffer handling
        if self.in_block:
            if not line.strip():
                # Empty line signals the end of the multi-line block
                full_source = "\n".join(self.buffer)
                self.buffer = []
                self.in_block = False
                return self._execute_chunk(full_source)
            self.buffer.append(line)
            return None

        # Check if line initiates a block (ends with ':')
        stripped = line.strip()
        if stripped.endswith(":"):
            self.in_block = True
            self.buffer.append(line)
            return None

        if not stripped:
            return None

        return self._execute_chunk(line)

    def _execute_chunk(self, source_code: str) -> Optional[Any]:
        """Parses, compiles, and evaluates or executes a chunk of Hinglish code."""
        # 1. Parse into AST
        prog = parse(source_code)
        if not prog.body:
            return None

        compiler = HinglishCompiler()

        # 2. Check if the chunk is a standalone expression (for REPL auto-print)
        if len(prog.body) == 1 and isinstance(prog.body[0], ExpressionStatement):
            expr_node = prog.body[0].expr
            py_expr = compiler.compile_expression(expr_node)
            code_obj = compile(py_expr, "<repl>", "eval")
            res = eval(code_obj, self.namespace)
            if res is not None:
                print(repr(res))
            return res

        # 3. Statement or multi-statement block
        py_source = compiler.compile(prog)
        code_obj = compile(py_source, "<repl>", "exec")
        exec(code_obj, self.namespace)
        return None

    def start(self) -> None:
        """Starts the interactive REPL terminal loop."""
        print(f"Hinglish {__version__} Interactive REPL")
        print("Type 'madad()' for quick help. Press Ctrl+C or Ctrl+D to exit.\n")

        while True:
            prompt = "... " if self.in_block else ">>> "
            try:
                line = input(prompt)
                self.run_line(line)
            except KeyboardInterrupt:
                print("\n[Operation cancelled]")
                self.buffer = []
                self.in_block = False
            except EOFError:
                print("\nAlvida! (Goodbye)")
                break
            except HinglishError as err:
                print(f"Hinglish Error:\n{err}", file=sys.stderr)
                self.buffer = []
                self.in_block = False
            except Exception as exc:
                print(f"{type(exc).__name__}: {exc}", file=sys.stderr)
                self.buffer = []
                self.in_block = False


def start_repl() -> None:
    """Convenience helper to launch the REPL."""
    repl = HinglishREPL()
    repl.start()


__all__ = ["HinglishREPL", "start_repl"]
