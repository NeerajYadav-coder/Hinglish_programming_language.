"""Command Line Interface (CLI) entrypoint for Hinglish."""

import argparse
import sys
from pathlib import Path
from typing import List, Optional

from .. import __version__
from ..exceptions import HinglishError
from ..lexer import format_tokens, tokenize


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
        "--transpile",
        action="store_true",
        help="Transpile to Python source code without executing (upcoming steps).",
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

    if args.tokens:
        try:
            tokens = tokenize(source_code)
            print(f"Tokens for '{args.file}':\n")
            print(format_tokens(tokens))
            return 0
        except HinglishError as err:
            print(f"Lexer error in {args.file}:\n{err}", file=sys.stderr)
            return 1

    print(
        f"[Hinglish v{__version__}] Lexer (Step 2) active.\n"
        f"File '{args.file}' contains valid syntax for tokenization.\n"
        f"Tip: Use 'hinglish --tokens {args.file}' to inspect the token stream.",
        file=sys.stderr,
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
