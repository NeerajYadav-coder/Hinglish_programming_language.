"""Command Line Interface (CLI) entrypoint for Hinglish."""

import argparse
import sys
from pathlib import Path
from typing import List, Optional, Tuple

from .. import __version__
from ..ast import format_ast
from ..compiler import compile as compile_hinglish
from ..exceptions import HinglishError
from ..formatter import format_source
from ..lexer import format_tokens, tokenize
from ..linter import lint_source
from ..parser import parse
from ..runtime import run, run_file, start_repl


def discover_hin_files(target_inputs: List[str]) -> Tuple[Optional[List[Path]], bool, Optional[str], int]:
    """Resolves target paths (files or directories) into a deterministic list of files.

    Returns:
        (files, has_directory, error_message, exit_code)
        If stdin mode ('-'), files is None, error_message is None, exit_code is 0.
    """
    if "-" in target_inputs:
        if len(target_inputs) > 1:
            return None, False, "Error: Standard input ('-') cannot be combined with other targets.", 2
        return None, False, None, 0

    has_directory = False
    discovered_files: List[Path] = []
    seen = set()

    for target in target_inputs:
        p = Path(target)
        if not p.exists():
            return None, False, f"Error: File not found: {target}", 2
        if p.is_dir():
            has_directory = True
            dir_hin_files = sorted(
                [f for f in p.rglob("*.hin") if f.is_file()],
                key=lambda x: x.as_posix(),
            )
            for f in dir_hin_files:
                resolved = f.resolve()
                if resolved not in seen:
                    seen.add(resolved)
                    discovered_files.append(f)
        elif p.is_file():
            resolved = p.resolve()
            if resolved not in seen:
                seen.add(resolved)
                discovered_files.append(p)
        else:
            return None, False, f"Error: File not found: {target}", 2

    return discovered_files, has_directory, None, 0


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
  format <file|dir>... [-o] [--check] Format Hinglish script(s) to canonical style
  lint <file|dir>... [--check] Run static analysis and lint diagnostics
  repl                    Start interactive REPL

Shorthand Usage:
  hinglish <file>            Run script directly
  hinglish --tokens <file>   Inspect tokens
  hinglish --ast <file>      Inspect AST
  hinglish --transpile <file> Transpile to Python
  hinglish --format <file|dir>... Format script(s) in-place
  hinglish --lint <file|dir>...   Lint script(s)
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
        help="Subcommand (run, tokens, ast, transpile, format, lint, repl) or path to .hin script.",
    )
    parser.add_argument(
        "sub_file",
        nargs="?",
        metavar="file",
        help="Path to the Hinglish script when using a subcommand.",
    )
    parser.add_argument(
        "extra_files",
        nargs="*",
        metavar="extra_files",
        help="Additional file or directory paths when using multi-target subcommands like lint and format.",
    )
    parser.add_argument(
        "-o", "--output",
        help="Write transpiled Python code or formatted Hinglish code to specified file instead of stdout / in-place.",
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
    parser.add_argument(
        "--format",
        action="store_true",
        help="Format the file to canonical Hinglish syntax.",
    )
    parser.add_argument(
        "--lint",
        action="store_true",
        help="Run static analysis and lint diagnostics on file.",
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Check if file is formatted or check if lint clean without writing changes. Exits with 0 if clean, 1 if changes/findings needed.",
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
    subcommands = {"run", "tokens", "ast", "transpile", "repl", "format", "lint"}
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
        elif args.format:
            command = "format"
        elif args.lint:
            command = "lint"
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

    # 2.5 Handle Lint command
    if command == "lint":
        target_inputs = []
        if raw_cmd in subcommands:
            if sub_file:
                target_inputs.append(sub_file)
            if getattr(args, "extra_files", None):
                target_inputs.extend(args.extra_files)
        else:
            if raw_cmd:
                target_inputs.append(raw_cmd)
            if sub_file:
                target_inputs.append(sub_file)
            if getattr(args, "extra_files", None):
                target_inputs.extend(args.extra_files)

        if not target_inputs:
            if not sys.stdin.isatty():
                target_inputs = ["-"]
            else:
                print("Error: Subcommand 'lint' requires a script file argument or standard input ('-').", file=sys.stderr)
                return 2

        discovered_files, has_directory, err_msg, exit_code = discover_hin_files(target_inputs)
        if err_msg:
            print(err_msg, file=sys.stderr)
            return exit_code

        if discovered_files is None:
            try:
                src = sys.stdin.read()
            except Exception as exc:
                print(f"Error reading standard input: {exc}", file=sys.stderr)
                return 2
            diags = lint_source(src, filename="<stdin>")
            total_findings = len(diags)
            error_findings = sum(1 for d in diags if d.severity == "error")
            for d in diags:
                print(d.format_cli())
            if args.check:
                return 1 if total_findings > 0 else 0
            return 1 if error_findings > 0 else 0

        total_findings = 0
        error_findings = 0

        for file_path in discovered_files:
            filename = str(file_path)
            try:
                src = file_path.read_text(encoding="utf-8")
            except Exception as exc:
                print(f"Error reading {file_path}: {exc}", file=sys.stderr)
                return 2

            diags = lint_source(src, filename=filename)
            for d in diags:
                total_findings += 1
                if d.severity == "error":
                    error_findings += 1
                print(d.format_cli())

        if args.check:
            return 1 if total_findings > 0 else 0
        return 1 if error_findings > 0 else 0

    # 2.6 Handle Format command
    if command == "format":
        target_inputs = []
        if raw_cmd in subcommands:
            if sub_file:
                target_inputs.append(sub_file)
            if getattr(args, "extra_files", None):
                target_inputs.extend(args.extra_files)
        else:
            if raw_cmd:
                target_inputs.append(raw_cmd)
            if sub_file:
                target_inputs.append(sub_file)
            if getattr(args, "extra_files", None):
                target_inputs.extend(args.extra_files)

        if not target_inputs:
            if not sys.stdin.isatty():
                target_inputs = ["-"]
            else:
                print("Error: Subcommand 'format' requires a script file argument.", file=sys.stderr)
                return 2

        discovered_files, has_directory, err_msg, exit_code = discover_hin_files(target_inputs)
        if err_msg:
            print(err_msg, file=sys.stderr)
            return exit_code

        # Safety check for -o / --output
        if args.output:
            if has_directory or len(target_inputs) > 1 or (discovered_files is not None and len(discovered_files) > 1):
                print("Error: -o/--output cannot be used with multiple files or directory targets.", file=sys.stderr)
                return 2

        # 1. Stdin mode
        if discovered_files is None:
            try:
                src = sys.stdin.read()
            except Exception as exc:
                print(f"Error reading standard input: {exc}", file=sys.stderr)
                return 1

            try:
                formatted = format_source(src)
            except HinglishError as err:
                print(f"Format error in <stdin>:\n{err}", file=sys.stderr)
                return 1
            except Exception as exc:
                print(f"Format error in <stdin>: {exc}", file=sys.stderr)
                return 1

            if args.check:
                if formatted == src:
                    return 0
                else:
                    print("File would be reformatted: <stdin>", file=sys.stderr)
                    return 1

            if args.output:
                out_path = Path(args.output)
                try:
                    out_path.write_text(formatted, encoding="utf-8")
                    return 0
                except Exception as exc:
                    print(f"Error writing to {args.output}: {exc}", file=sys.stderr)
                    return 1
            else:
                sys.stdout.write(formatted)
                return 0

        # 2. Check mode
        if args.check:
            would_reformat = False
            for file_path in discovered_files:
                try:
                    src = file_path.read_text(encoding="utf-8")
                    formatted = format_source(src)
                except HinglishError as err:
                    print(f"Format error in {file_path}:\n{err}", file=sys.stderr)
                    return 1
                except Exception as exc:
                    print(f"Format error in {file_path}: {exc}", file=sys.stderr)
                    return 1

                if formatted != src:
                    print(f"File would be reformatted: {file_path}", file=sys.stderr)
                    would_reformat = True
            return 1 if would_reformat else 0

        # 3. Output flag mode (single file)
        if args.output:
            if not discovered_files:
                return 0
            file_path = discovered_files[0]
            out_path = Path(args.output)
            if out_path.resolve() == file_path.resolve():
                print("Error: Output path cannot overwrite the source file.", file=sys.stderr)
                return 1
            try:
                src = file_path.read_text(encoding="utf-8")
                formatted = format_source(src)
                out_path.write_text(formatted, encoding="utf-8")
                return 0
            except HinglishError as err:
                print(f"Format error in {file_path}:\n{err}", file=sys.stderr)
                return 1
            except Exception as exc:
                print(f"Error writing to {args.output}: {exc}", file=sys.stderr)
                return 1

        # 4. In-place formatting mode
        for file_path in discovered_files:
            try:
                src = file_path.read_text(encoding="utf-8")
                formatted = format_source(src)
                file_path.write_text(formatted, encoding="utf-8")
            except HinglishError as err:
                print(f"Format error in {file_path}:\n{err}", file=sys.stderr)
                return 1
            except Exception as exc:
                print(f"Error writing to {file_path}: {exc}", file=sys.stderr)
                return 1
        return 0

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


__all__ = ["create_parser", "main", "discover_hin_files"]


if __name__ == "__main__":
    sys.exit(main())
