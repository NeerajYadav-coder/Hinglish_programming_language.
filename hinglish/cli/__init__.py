"""Command Line Interface (CLI) entrypoint for Hinglish."""

import argparse
import sys
from typing import List, Optional

from .. import __version__


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
        "--transpile",
        action="store_true",
        help="Transpile to Python source code without executing.",
    )
    return parser


def main(argv: Optional[List[str]] = None) -> int:
    """CLI main entrypoint."""
    parser = create_parser()
    args = parser.parse_args(argv)

    if not args.file:
        parser.print_help()
        return 0

    print(
        f"[Hinglish v{__version__}] Step 1 Foundation active.\n"
        f"Target file: {args.file}\n"
        f"Execution engine will be activated in upcoming steps.",
        file=sys.stderr,
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
