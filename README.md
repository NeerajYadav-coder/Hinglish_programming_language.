# Hinglish Programming Language

> **Hinglish** is a Python-compatible programming language interface that uses familiar Hinglish (Hindi + English) keywords and syntax, targeting Python execution under the hood.

*Created by **NJ 5.0***

[![PyPI version](https://img.shields.io/pypi/v/hinglish-lang.svg)](https://pypi.org/project/hinglish-lang/)
[![Documentation](https://img.shields.io/badge/docs-live%20website-0071e3.svg)](https://hinglish-programming-language.neerajbhaiya1508.workers.dev/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)

📖 **Official Documentation Website**: [https://hinglish-programming-language.neerajbhaiya1508.workers.dev/](https://hinglish-programming-language.neerajbhaiya1508.workers.dev/)

---

## What is Hinglish?

Hinglish is an intuitive, approachable programming language interface designed for Hindi and Hinglish speakers. It allows developers and students to express algorithms, logic, and data flows using natural Hinglish vocabulary (such as `agar`, `warna`, `jabtak`, `kaam`, and `dikhao`), while retaining the simplicity, semantics, and standard library power of Python.

---

## Why Hinglish?

Hinglish began as a **curiosity-driven project**. It started with a simple spark of thought: *"Could a practical programming language actually be built around the natural cadence of everyday Hinglish without sacrificing Python's power?"* It was never conceived as a commercial product, a final career milestone, or a grand statement—the idea felt genuinely interesting, so it was simply explored and built.

Looking back, it stands as one small step in an ongoing rhythm of **observation → curiosity → creation → learning**.

Beyond that original spark of curiosity, Hinglish serves several concrete ergonomic and educational purposes:

1. **Accessibility**: For millions of aspiring developers in India and South Asia, syntax barriers in English can add unnecessary cognitive friction when learning computational logic.
2. **Cognitive Ease**: Reading `agar umar >= 18:` feels immediately intuitive and lowers the barrier to entry for beginners.
3. **Bridge, Not Island**: Rather than creating an isolated language with no ecosystem, Hinglish seamlessly maps to Python. Code written in Hinglish preserves Python's block structure and expression semantics, acting as an educational and practical bridge to full Python mastery.

---

## The Core Idea

Hinglish separates **syntax representation** from **computational semantics**:

- **Syntax Layer**: Natural Hinglish keywords (`agar`, `warna`, `dikhao`, `kaam`, `har`, `jabtak`) and idiomatic constructs.
- **Structural Model**: Strict preservation of Python-style indentation (`INDENT`, `DEDENT`, and colons `:`).
- **Expression Compatibility**: Mathematical operations, indexing, slicing, function calls, and object attribute access remain standard Python expressions wherever practical.
- **Execution Target**: Hinglish compiles deterministically into clean Python AST or Python source code for execution via standard Python runtimes.

### Example

```hinglish
# Hinglish Source Code
naam = "Neeraj"

agar naam == "Neeraj":
    dikhao("Namaste duniya!")
warna:
    dikhao("Hello!")
```

Translates under the hood to:

```python
# Generated Python
naam = "Neeraj"

if naam == "Neeraj":
    print("Namaste duniya!")
else:
    print("Hello!")
```

---

## Long-Term Compiler Pipeline

The complete end-to-end architectural pipeline is designed as follows:

```
Hinglish Source Code (.hin)
            ↓
    Tokenizer / Lexer       (converts Hinglish characters into token stream; tracks INDENT / DEDENT)
            ↓
          Parser            (constructs Hinglish Abstract Syntax Tree from tokens)
            ↓
       Hinglish AST         (semantic node graph representing Hinglish program logic)
            ↓
     Semantic Analysis      (validates scopes, names, and grammar rules)
            ↓
      Compiler / Lowering   (transforms Hinglish AST to Python AST or Python source code)
            ↓
      Python Execution      (executes directly via Python runtime)
```

---

## Installation

Install Hinglish directly using `pip`:

```bash
# From PyPI
pip install hinglish-lang

# Or from local repository source
pip install .
```

Requires **Python 3.10+** (tested on Python 3.10 through 3.14). Zero third-party runtime dependencies required!

---

## Quickstart

### 1. Minimal Hello World

Create a file named `hello.hin`:

```hinglish
naam = "Neeraj"

agar naam == "Neeraj":
    dikhao("Namaste")
warna:
    dikhao("Hello")
```

Run it using the `hinglish` command:

```bash
hinglish hello.hin
```

Output:
```text
Namaste
```

You can also run it via standard Python module invocation:
```bash
python3 -m hinglish hello.hin
```

### 2. Basic Syntax at a Glance

```hinglish
# Variables and Printing
naam = "Aarav"
dikhao(f"Namaste, {naam}!")

# Conditionals (agar, warna_agar, warna)
agar naam == "Aarav":
    dikhao("User verified")
warna_agar naam == "Neeraj":
    dikhao("Creator verified")
warna:
    dikhao("Guest verified")

# Loops (har ... mein ...)
har i mein ginti(1, 4):
    dikhao(f"Step {i}")

# Inline Conditional Expression (ternary)
status = "Admin" agar naam == "Neeraj" warna "Member"

# Bilingual Built-in Aliases
items = [10, 20, 30]
n = lambai(items)       # len -> 3
total = jod(items)      # sum -> 60
valid = sab([sahi, sahi]) # all -> True
exists = koi([galat, sahi]) # any -> True

# Functions (kaam, wapas)
kaam jodo(a: int, b: int) -> int:
    wapas a + b
```

### 3. Interactive REPL

Start the interactive Hinglish REPL by running `hinglish` with no arguments:

```bash
hinglish
```

Example session:
```hinglish
Hinglish 1.1.0 Interactive REPL
Type "exit()", "quit()", or Ctrl-D to exit.

>>> x = 10
>>> agar x > 5:
...     dikhao(f"Value is {x}")
...
Value is 10
>>>
```

### 4. CLI Commands & Subcommands

The `hinglish` CLI supports both explicit subcommands and backward-compatible flags:

```bash
# Subcommand Syntax
hinglish run script.hin              # Execute a Hinglish script
hinglish tokens script.hin           # Inspect token stream
hinglish ast script.hin              # Inspect Abstract Syntax Tree
hinglish transpile script.hin        # Transpile to Python source
hinglish transpile script.hin -o out.py  # Save Python output to file
hinglish format script.hin           # Format Hinglish source in-place
hinglish format src/ tests/          # Recursively format all *.hin in directories
hinglish format script.hin --check   # Check if formatted without modifying (exit code 0/1)
hinglish format script.hin -o out.hin # Save formatted source to another file (single input only)
hinglish lint script.hin [files...]  # Static analysis and lint diagnostics
hinglish lint src/ tests/            # Recursively discover and lint all *.hin in directories
hinglish lint script.hin --check     # Lint check (exits 1 if warnings/errors found)
hinglish repl                        # Start interactive REPL

# Shorthand Syntax (100% Backward Compatible)
hinglish script.hin                  # Execute script directly
hinglish --tokens script.hin         # Inspect tokens
hinglish --ast script.hin            # Inspect AST
hinglish --transpile script.hin      # Transpile to stdout
hinglish --format src/               # Format directory in-place
hinglish --lint src/                 # Run linter across directory
hinglish --version                   # Show version
```

### 5. Standard Input (Stdin / Pipelines)

Hinglish can read and execute source code directly from pipelines:

```bash
# Pipe code into hinglish
cat script.hin | hinglish

# Explicit stdin execution
echo 'dikhao("Namaste")' | hinglish -
```

---

## Developer Tooling & Ecosystem

Hinglish provides a complete developer ecosystem:

- **VS Code Extension (`vscode-hinglish`)**:
  - Full TextMate syntax highlighting for all 64 Hinglish keywords, strings, decorators, and builtins.
  - **Language Server Protocol (LSP)**: `hinglish-lsp` entrypoint providing hover documentation, real-time diagnostics, document symbols, and auto-completion.
  - **Debug Adapter Protocol (DAP)**: `hinglish-dap` entrypoint with breakpoints, variable inspection, call stack navigation, and step debugging.
  - **Document Formatter & Linter**: Integrated source formatting and static analysis directly within VS Code.
- **Official Documentation Website**: [https://hinglish-programming-language.neerajbhaiya1508.workers.dev/](https://hinglish-programming-language.neerajbhaiya1508.workers.dev/)
  - Full modern interactive Apple-style documentation, comprehensive language guide, comparison tables, 30+ keyword glossary, CLI reference, and real-world examples.


---

## Real Multi-File Projects

Hinglish provides first-class support for multi-file modular architectures:

```text
my_project/
├── config.hin       # App constants and configuration
├── utils.hin        # Helper functions and formatting
├── models.hin       # Data classes and models
├── services.hin     # Business logic & async operations
└── main.hin         # Project entrypoint
```

### Module Resolution Semantics
- **Executing Projects**: Run `hinglish /path/to/project/main.hin` from **any** working directory.
- **Working Directory Independence**: Hinglish automatically sets `sys.path[0]` to the directory of the executed script, so relative `.hin` imports (`laao utils`, `se models laao Product`) resolve cleanly regardless of your current working directory.
- **Nested & Inter-Module Imports**: A module (`models.hin`) can import another sibling module (`utils.hin`) without needing complex packaging configuration.
- **Source-Mapped Multi-File Tracebacks**: When an exception occurs inside an imported `.hin` module, Hinglish renders a full traceback showing every `.hin` file name, exact line number, and original code snippet.
- **Python Interoperability**: Hinglish seamlessly imports Python standard library modules (`se datetime laao datetime`, `se json laao dumps`), and Python scripts can import `.hin` files via `hinglish.runtime.install_import_hook()`.

### Exit Codes
- `0`: Successful execution, version display, help display, or clean REPL exit.
- `1`: Program execution error (syntax errors, compiler errors, runtime exceptions, missing file, or source overwrite safety violation).
- `2`: CLI argument usage error (unrecognized flags, missing file argument for subcommands).


