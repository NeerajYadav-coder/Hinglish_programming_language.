# Hinglish Programming Language

> **Hinglish** is a Python-compatible programming language interface that uses familiar Hinglish (Hindi + English) keywords and syntax, targeting Python execution under the hood.

---

## What is Hinglish?

Hinglish is an intuitive, approachable programming language interface designed for Hindi and Hinglish speakers. It allows developers and students to express algorithms, logic, and data flows using natural Hinglish vocabulary (such as `agar`, `warna`, `jabtak`, `kaam`, and `dikhao`), while retaining the simplicity, semantics, and standard library power of Python.

---

## Why Hinglish?

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
# From local repository source
pip install .

# Or from pre-built wheel
pip install dist/hinglish-1.0.0-py3-none-any.whl
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

### 2. Interactive REPL

Start the interactive Hinglish REPL by running `hinglish` with no arguments:

```bash
hinglish
```

Example session:
```hinglish
Hinglish 1.0.0 Interactive REPL
Type "exit()", "quit()", or Ctrl-D to exit.

>>> x = 10
>>> agar x > 5:
...     dikhao(f"Value is {x}")
...
Value is 10
>>>
```

### 3. CLI Commands & Flags

The `hinglish` CLI supports execution, debugging, and transpilation:

```bash
# Run a Hinglish script
hinglish script.hin

# Inspect token stream
hinglish --tokens script.hin

# Inspect Abstract Syntax Tree (AST)
hinglish --ast script.hin

# Transpile to Python source without executing
hinglish --transpile script.hin

# Check version
hinglish --version
```

