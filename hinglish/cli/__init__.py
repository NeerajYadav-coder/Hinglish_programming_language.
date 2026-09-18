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
        help="Path to the Hinglish script to run (.hin)",
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

    if not args.file:
        parser.print_help()
        return 0

    target_path = Path(args.file)
    if not target_path.is_file():
        print(f"Error: File not found: {args.file}", file=sys.stderr)
        return 1

    try:
        source_code = target_path.read_text(encoding="utf-8")
    except Exception as exc:
        print(f"Error reading {args.file}: {exc}", file=sys.stderr)
        return 1

    # 1. Inspect Token Stream
    if args.tokens:
        try:
            tokens = tokenize(source_code)
            print(f"Tokens for '{args.file}':\n")
            print(format_tokens(tokens))
            return 0
        except HinglishError as err:
            print(f"Lexer error in {args.file}:\n{err}", file=sys.stderr)
            return 1

    # 2. Inspect AST
    if args.ast:
        try:
            program_ast = parse(source_code)
            print(f"Hinglish AST for '{args.file}':\n")
            print(format_ast(program_ast))
            return 0
        except HinglishError as err:
            print(f"Syntax error in {args.file}:\n{err}", file=sys.stderr)
            return 1

    # 3. Transpile to Python Source
    if args.transpile:
        try:
            py_code = compile_hinglish(source_code)
            sys.stdout.write(py_code)
            return 0
        except HinglishError as err:
            print(f"Compilation error in {args.file}:\n{err}", file=sys.stderr)
            return 1

    print(
        f"[Hinglish v{__version__}] Compiler (Step 4) active.\n"
        f"File '{args.file}' is syntactically valid.\n"
        f"Tip: Use 'hinglish --tokens {args.file}' to inspect tokens.\n"
        f"Tip: Use 'hinglish --ast {args.file}' to inspect the AST.\n"
        f"Tip: Use 'hinglish --transpile {args.file}' to view generated Python code.",
        file=sys.stderr,
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
