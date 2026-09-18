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

## Status: What is Implemented Now (Step 1)

Step 1 establishes the **architectural foundation, specification, and project baseline**:

- [x] **Project Architecture**: Clean, modular Python package structure (`hinglish/lexer`, `hinglish/parser`, `hinglish/ast`, `hinglish/compiler`, `hinglish/runtime`, `hinglish/cli`).
- [x] **Formal Specification**: Detailed language specification covering initial constructs, indentation rules, and expression rules in [`docs/specification.md`](docs/specification.md).
- [x] **Keyword Registry**: Centralized, configurable dictionary of keywords and aliases (`hinglish/keywords.py`) designed for easy expansion and customization.
- [x] **Architecture Blueprint**: Detailed module boundaries and data flow in [`docs/architecture.md`](docs/architecture.md).
- [x] **Example `.hin` Programs**: Canonical source examples in [`examples/`](examples/).
- [x] **Test Strategy**: Foundation test suite running with Python's standard `unittest` framework (`tests/`).

---

## Roadmap: What Will Be Implemented Later

Future steps will incrementally build out the language pipeline without skipping stages:

- **Step 2: Lexer & Tokenizer**:
  - Deterministic lexical analysis
  - Proper handling of indentation (`INDENT`, `DEDENT`, `NEWLINE`)
  - String, number, and comment tokenization
- **Step 3: Abstract Syntax Tree (AST) & Parser**:
  - Grammar specification
  - Deterministic parser translating tokens into Hinglish AST nodes
- **Step 4: Compiler / Code Generation**:
  - Transpilation of Hinglish AST into Python AST / Python source
  - Source-map tracking for accurate error reporting
- **Step 5: Runtime & CLI**:
  - `hinglish <file>.hin` command-line runner
  - Interactive REPL (`hinglish`)
  - Execution sandbox and error tracebacks translated back to Hinglish line numbers
