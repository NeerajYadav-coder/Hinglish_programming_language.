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
from ..runtime import run, run_file, start_repl


def create_parser() -> argparse.ArgumentParser:
    """Creates the command line argument parser for hinglish."""
    parser = argparse.ArgumentParser(
        prog="hinglish",
        description="Hinglish — A Python-compatible programming language interface using Hinglish syntax.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Commands:
  run <file>              Execute a Hinglish script (.hin)
  tokens <file>           Tokenize and print token table
  ast <file>              Parse and print Abstract Syntax Tree
  transpile <file> [-o]   Transpile to Python source code
  repl                    Start interactive REPL

Shorthand Usage:
  hinglish <file>            Run script directly
  hinglish --tokens <file>   Inspect tokens
  hinglish --ast <file>      Inspect AST
  hinglish --transpile <file> Transpile to Python
  hinglish                   Start interactive REPL (or execute stdin if piped)
""",
    )
    parser.add_argument(
        "-v", "--version",
        action="version",
        version=f"hinglish {__version__}",
    )
    parser.add_argument(
        "file",
        nargs="?",
        metavar="command|file",
        help="Subcommand (run, tokens, ast, transpile, repl) or path to .hin script.",
    )
    parser.add_argument(
        "sub_file",
        nargs="?",
        metavar="file",
        help="Path to the Hinglish script when using a subcommand.",
    )
    parser.add_argument(
        "-o", "--output",
        help="Write transpiled Python code to specified file instead of stdout.",
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
    """CLI main entrypoint with predictable exit codes:

    0: Success
    1: Execution / Syntax / Runtime / File error
    2: CLI argument usage error
    """
    parser = create_parser()
    args = parser.parse_args(argv)

    raw_cmd = args.file
    sub_file = args.sub_file

    # 1. Determine resolved command and target file
    subcommands = {"run", "tokens", "ast", "transpile", "repl"}
    if raw_cmd in subcommands:
        command = raw_cmd
        file_arg = sub_file
    else:
        if args.tokens:
            command = "tokens"
        elif args.ast:
            command = "ast"
        elif args.transpile:
            command = "transpile"
        elif raw_cmd:
            command = "run"
        else:
            # If no file provided, check if stdin is being piped into hinglish
            if not sys.stdin.isatty():
                command = "run"
                file_arg = "-"
            else:
                command = "repl"
                file_arg = None

        if raw_cmd and not (raw_cmd in subcommands):
            file_arg = raw_cmd

    # 2. Handle REPL command
    if command == "repl":
        try:
            from ..runtime import install_import_hook
            install_import_hook()
            start_repl()
            return 0
        except Exception as exc:
            print(f"REPL Error: {exc}", file=sys.stderr)
            return 1

    # 3. Validate file argument for file-based commands
    if command in {"run", "tokens", "ast", "transpile"} and not file_arg:
        print(f"Error: Subcommand '{command}' requires a script file argument.", file=sys.stderr)
        return 2

    # 4. Handle reading source code (either from stdin '-' or from disk)
    if file_arg == "-":
        filename = "<stdin>"
        try:
            source_code = sys.stdin.read()
        except Exception as exc:
            print(f"Error reading standard input: {exc}", file=sys.stderr)
            return 1
        target_path = None
    else:
        target_path = Path(file_arg)
        if not target_path.is_file():
            print(f"Error: File not found: {file_arg}", file=sys.stderr)
            return 1
        filename = str(target_path)
        try:
            source_code = target_path.read_text(encoding="utf-8")
        except Exception as exc:
            print(f"Error reading {file_arg}: {exc}", file=sys.stderr)
            return 1

    # 5. Inspect Token Stream
    if command == "tokens":
        try:
            tokens = tokenize(source_code)
            print(f"Tokens for '{file_arg}':\n")
            print(format_tokens(tokens))
            return 0
        except HinglishError as err:
            print(f"Lexer error in {file_arg}:\n{err}", file=sys.stderr)
            return 1

    # 6. Inspect AST
    if command == "ast":
        try:
            program_ast = parse(source_code)
            print(f"Hinglish AST for '{file_arg}':\n")
            print(format_ast(program_ast))
            return 0
        except HinglishError as err:
            print(f"Syntax error in {file_arg}:\n{err}", file=sys.stderr)
            return 1

    # 7. Transpile to Python Source
    if command == "transpile":
        try:
            py_code = compile_hinglish(source_code)
            if args.output:
                out_path = Path(args.output)
                if target_path and out_path.resolve() == target_path.resolve():
                    print("Error: Output path cannot overwrite the source file.", file=sys.stderr)
                    return 1
                out_path.write_text(py_code, encoding="utf-8")
            else:
                sys.stdout.write(py_code)
            return 0
        except HinglishError as err:
            print(f"Compilation error in {file_arg}:\n{err}", file=sys.stderr)
            return 1

    # 8. Direct Execution (File or Stdin)
    try:
        if target_path is not None:
            run_file(target_path)
        else:
            from ..runtime import install_import_hook
            install_import_hook()
            run(source_code, filename=filename)
        return 0
    except HinglishError as err:
        print(f"Hinglish Error in {file_arg}:\n{err}", file=sys.stderr)
        return 1
    except RuntimeError as r_err:
        print(f"{r_err}", file=sys.stderr)
        return 1
    except Exception as exc:
        print(f"Error executing {file_arg}: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
