"""Command Line Interface (CLI) entrypoint for Hinglish."""

import argparse
import sys
from pathlib import Path
from typing import List, Optional

from .. import __version__
from ..ast import format_ast
from ..compiler import compile as compile_hinglish
from ..exceptions import HinglishError
from ..lexer import format_tokens, tokenize
from ..parser import parse
from ..runtime import run_file, start_repl


def create_parser() -> argparse.ArgumentParser:
    """Creates the command line argument parser for hinglish."""
    parser = argparse.ArgumentParser(
        prog="hinglish",
        description="Hinglish — A Python-compatible programming language interface using Hinglish syntax.",
    )
    parser.add_argument(
        "-v", "--version",
        action="version",
        version=f"hinglish {__version__}",
    )
    parser.add_argument(
        "file",
        nargs="?",
        help="Path to the Hinglish script to execute (.hin). If omitted, starts interactive REPL.",
    )
    parser.add_argument(
        "--tokens",
        action="store_true",
        help="Tokenize the file and print a readable token table for debugging.",
    )
    parser.add_argument(
        "--ast",
        action="store_true",
        help="Parse the file and print the formatted Abstract Syntax Tree (AST).",
    )
    parser.add_argument(
        "--transpile",
        action="store_true",
        help="Transpile to valid Python source code and print to stdout.",
    )
    return parser


def main(argv: Optional[List[str]] = None) -> int:
    """CLI main entrypoint."""
    parser = create_parser()
    args = parser.parse_args(argv)

    # 1. Interactive REPL if no file provided
    if not args.file:
        try:
            start_repl()
            return 0
        except Exception as exc:
            print(f"REPL Error: {exc}", file=sys.stderr)
            return 1

    target_path = Path(args.file)
    if not target_path.is_file():
        print(f"Error: File not found: {args.file}", file=sys.stderr)
        return 1

    try:
        source_code = target_path.read_text(encoding="utf-8")
    except Exception as exc:
        print(f"Error reading {args.file}: {exc}", file=sys.stderr)
        return 1

    # 2. Inspect Token Stream
    if args.tokens:
        try:
            tokens = tokenize(source_code)
            print(f"Tokens for '{args.file}':\n")
            print(format_tokens(tokens))
            return 0
        except HinglishError as err:
            print(f"Lexer error in {args.file}:\n{err}", file=sys.stderr)
            return 1

    # 3. Inspect AST
    if args.ast:
        try:
            program_ast = parse(source_code)
            print(f"Hinglish AST for '{args.file}':\n")
            print(format_ast(program_ast))
            return 0
        except HinglishError as err:
            print(f"Syntax error in {args.file}:\n{err}", file=sys.stderr)
            return 1

    # 4. Transpile to Python Source
    if args.transpile:
        try:
            py_code = compile_hinglish(source_code)
            sys.stdout.write(py_code)
            return 0
        except HinglishError as err:
            print(f"Compilation error in {args.file}:\n{err}", file=sys.stderr)
            return 1

    # 5. Direct Execution
    try:
        run_file(target_path)
        return 0
    except HinglishError as err:
        print(f"Hinglish Error in {args.file}:\n{err}", file=sys.stderr)
        return 1
    except RuntimeError as r_err:
        print(f"{r_err}", file=sys.stderr)
        return 1
    except Exception as exc:
        print(f"Error executing {args.file}: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
