# Hinglish Architecture & Pipeline Design

This document details the architectural boundaries, system modules, and execution pipeline for the Hinglish programming language interface.

---

## 1. Architectural Overview

The Hinglish system is divided into modular, decoupled layers. Each module has a single, well-defined responsibility:

```
                  +-------------------------+
                  | Hinglish Source (.hin)  |
                  +-------------------------+
                               |
                               v
                     [ hinglish.lexer ]
             (Lexer, Tokenizer, Indentation Tracker)
                               |
                               v
                     Token Stream (Tokens)
                               |
                               v
                     [ hinglish.parser ]
                      (Syntax Analyzer)
                               |
                               v
                      [ hinglish.ast ]
                 (Hinglish AST Node Hierarchy)
                               |
                               v
                    [ hinglish.compiler ]
               (Lowering / Python AST Generator)
                               |
                               v
                     Python Code / AST
                               |
                               v
                    [ hinglish.runtime ]
               (Execution Environment & Builtins)
                               |
                               v
                     [ hinglish.cli ]
             (User Interface, CLI & Entrypoint)
```

---

## 2. Component Boundaries & Responsibilities

### 2.1 `hinglish.keywords`
- **Responsibility**: Single source of truth for all language vocabulary.
- **Key Characteristics**:
  - Configurable vocabulary mapping (Hinglish ↔ Python).
  - Alias registry (allowing synonyms like `shunya` alongside `kuch_nahi`).
  - Separation from parser and lexer mechanics, allowing vocabulary evolution without rewriting compiler logic.

### 2.2 `hinglish.lexer`
- **Responsibility**: Converts raw Hinglish UTF-8 text into a linear stream of strongly typed tokens.
- **Key Responsibilities**:
  - Keyword identification using `hinglish.keywords`.
  - Whitespace and indentation processing (generating `INDENT`, `DEDENT`, `NEWLINE` tokens).
  - String and numeric literal tokenization.
  - Tracking accurate source positions (line number, column offset) for error reporting.

### 2.3 `hinglish.ast`
- **Responsibility**: Represents the syntactic structure of Hinglish programs as an immutable, typed node tree.
- **Key Categories**:
  - `Statement`: Assignment, IfStatement, WhileLoop, ForLoop, FunctionDef, ReturnStatement, ExprStatement.
  - `Expression`: BinaryOp, UnaryOp, Literal, Identifier, FunctionCall, ListLiteral, DictLiteral.
  - Position metadata (`lineno`, `col_offset`) preserved on every node.

### 2.4 `hinglish.parser`
- **Responsibility**: Consumes the token stream and constructs the corresponding Hinglish AST.
- **Key Characteristics**:
  - Deterministic parsing (e.g. recursive descent / operator-precedence parsing).
  - Clear, descriptive syntax error messages with source coordinates.
  - Validates block structures (ensuring `:` precedes indented blocks).

### 2.5 `hinglish.compiler`
- **Responsibility**: Lowers Hinglish AST nodes into Python representations.
- **Design Options**:
  - **Option A (Direct Python AST)**: Build `ast.Module` directly using Python's standard `ast` module. Advantage: Faster compilation, direct bytecode compilation.
  - **Option B (Python Source Transpilation)**: Emit formatted Python code. Advantage: Simpler inspection, easy debugging, transparent source maps.
- *Recommended Strategy*: Emit Python source or standard Python `ast` nodes with source mapping so tracebacks map back to the original `.hin` line numbers.

### 2.6 `hinglish.runtime`
- **Responsibility**: Provides execution environment and runtime helpers.
- **Key Components**:
  - Built-in functions: `dikhao` mapped to `print`, Hindi aliases for basic functions.
  - Exception handler that intercepts Python tracebacks and translates file/line numbers back to original Hinglish source locations.

### 2.7 `hinglish.cli`
- **Responsibility**: User-facing command line interface.
- **Key Functions**:
  - `hinglish <file.hin>`: Read, compile, and execute file.
  - `hinglish --transpile <file.hin>`: Output generated Python code for inspection.
  - `hinglish`: Start interactive REPL session (in future steps).

---

## 3. Structural Decisions & Rationale

1. **Standard Library First**:
   - Zero hard external dependencies for core operation.
   - Uses standard Python `unittest`, `dataclasses`, and `typing`.
2. **Explicit AST**:
   - Avoids simplistic regex or string substitution. A proper lexer and parser ensure grammatical correctness and robustness against edge cases (such as keywords inside strings or comments).
3. **Pluggable Keywords**:
   - Centralizing keywords in a data-driven registry ensures that dialect variations or community vocabulary preferences can be accommodated without modifying lexing or parsing algorithms.
