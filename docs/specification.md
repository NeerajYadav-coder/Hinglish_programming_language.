# Hinglish Language Specification (v0.1)

This document defines the formal specification for **Hinglish v0.1**, an experimental, Python-compatible programming language interface.

---

## 1. Design Principles

1. **Separation of Syntax and Semantics**: Hinglish provides a localized, natural syntax layer while relying on Python's mature execution semantics.
2. **Indentation as Syntax**: Hinglish retains Python's whitespace-sensitive block indentation.
3. **Transparent Expressions**: Standard Python mathematical and logical expressions remain valid without artificial translation.
4. **Configurable Vocabulary**: Keywords are treated as a pluggable dictionary rather than rigid, hardcoded lexer rules.
5. **Deterministic Execution**: Parsing and translation are strictly deterministic—no heuristic or LLM-based guessing.

---

## 2. Lexical Structure

### 2.1 Character Set & Encoding
- Source files are encoded in standard UTF-8.
- The canonical file extension is `.hin` (e.g., `program.hin`).

### 2.2 Whitespace & Indentation
- Blocks are delimited by indentation, identical to Python.
- A block begins with a colon `:` at the end of a header statement, followed by an increased indentation level.
- Indentation increases emit an `INDENT` token.
- Indentation decreases emit one or more `DEDENT` tokens.
- Recommended indentation is 4 spaces. Consistent use of spaces or tabs is enforced per file.

### 2.3 Comments
Single-line comments begin with `#` and extend to the end of the line:
```hinglish
# Yeh ek comment hai (This is a comment)
naam = "Neeraj" # Inline comment
```

---

## 3. Initial Supported Constructs (v0.1)

Hinglish v0.1 focuses strictly on foundational programming constructs:

### 3.1 Literals & Values
| Type | Example | Python Equivalent |
|------|---------|-------------------|
| **String** | `"Namaste"`, `'Duniya'` | `"Namaste"`, `'Duniya'` |
| **Integer** | `10`, `-42` | `10`, `-42` |
| **Float** | `3.14`, `-0.001` | `3.14`, `-0.001` |
| **Boolean True** | `sahi` (or `True`) | `True` |
| **Boolean False** | `galat` (or `False`) | `False` |
| **None / Null** | `kuch_nahi` or `shunya` (or `None`) | `None` |

### 3.2 Variables & Assignment
Variables are declared and assigned using the standard assignment operator `=`:
```hinglish
naam = "Neeraj"
umar = 25
bhaarat_se = sahi
```

### 3.3 Output / Print (`dikhao`)
The standard output construct is `dikhao(...)`:
```hinglish
dikhao("Namaste Duniya!")
dikhao("Mera naam hai:", naam)
```

### 3.4 Conditionals (`agar`, `warna_agar`, `warna`)
Conditional branching mirrors Python's `if`, `elif`, and `else`:
```hinglish
agar umar >= 18:
    dikhao("Aap vote de sakte hain")
warna_agar umar >= 16:
    dikhao("Aap driving license learner le sakte hain")
warna:
    dikhao("Abhi aap chhote hain")
```

### 3.5 Loops (`jabtak`, `har`)
#### While Loop (`jabtak`):
```hinglish
ginti = 1
jabtak ginti <= 5:
    dikhao("Ginti hai:", ginti)
    ginti = ginti + 1
```

#### For Loop (`har` ... `mein` / `andar`):
```hinglish
phal = ["aam", "kela", "seb"]
har ek_phal mein phal:
    dikhao("Mujhe pasand hai:", ek_phal)
```

#### Loop Control:
- `ruko` (`break`): Terminates loop execution immediately.
- `aage_bado` (`continue`): Skips to the next loop iteration.

### 3.6 Functions (`kaam`, `wapas`)
Functions are declared using `kaam` and return values using `wapas`:
```hinglish
kaam jod(pehla, doosra):
    natija = pehla + doosra
    wapas natija

kul = jod(10, 20)
dikhao("Kul jod:", kul)
```

### 3.7 Data Structures: Lists & Dictionaries
Lists and dictionaries follow standard Python syntax with full expression nesting:
```hinglish
# List
shehar = ["Delhi", "Mumbai", "Bengaluru"]
dikhao(shehar[0])

# Dictionary
pata = {
    "shehar": "Delhi",
    "pin": 110001,
    "mukhya": sahi
}
dikhao(pata["shehar"])
```

### 3.8 Logical Operators
Hinglish introduces intuitive logical keywords:
- `aur` → `and`
- `ya` → `or`
- `nahi` → `not`

Example:
```hinglish
agar umar >= 18 aur bhaarat_se == sahi:
    dikhao("Yogya hain")
```

---

## 4. Initial Keyword Mapping Table

The vocabulary is centrally defined and configurable (see [`hinglish/keywords.py`](../hinglish/keywords.py)):

| Hinglish Keyword | Python Keyword / Builtin | Purpose | Notes / Synonyms |
|------------------|--------------------------|---------|------------------|
| `agar` | `if` | Conditional branch | Primary |
| `warna` | `else` | Alternative branch | Primary |
| `warna_agar` | `elif` | Secondary condition | Primary (`warna agar` conceptually) |
| `jabtak` | `while` | Indefinite loop | Primary |
| `har` | `for` | Iterative loop | Primary |
| `mein` | `in` | Membership / iteration | Alias: `andar` |
| `kaam` | `def` | Function definition | Primary |
| `wapas` | `return` | Return statement | Primary |
| `dikhao` | `print` | Standard output | Primary (Alias: `chapo`, `batao`) |
| `sahi` | `True` | Boolean true | Primary |
| `galat` | `False` | Boolean false | Primary |
| `kuch_nahi` | `None` | Null object | Primary (Alias: `shunya`) |
| `aur` | `and` | Conjunction | Primary |
| `ya` | `or` | Disjunction | Primary |
| `nahi` | `not` | Negation | Primary |
| `ruko` | `break` | Loop exit | Primary |
| `aage_bado` | `continue` | Loop continue | Primary |
| `chhod_do` | `pass` | No-op statement | Primary |

---

## 5. Expression Transparency Rules

To avoid redundant translation and maintain compatibility with the rich Python ecosystem:
1. **Mathematical Operators**: `+`, `-`, `*`, `/`, `//`, `%`, `**` remain identical.
2. **Comparison Operators**: `==`, `!=`, `<`, `<=`, `>`, `>=` remain identical.
3. **Collection Access**: Indexing `obj[0]`, slicing `obj[1:5]`, and key lookup `dict["key"]` remain standard.
4. **Member / Method Calls**: `obj.method(...)` and function calls `func(arg1, arg2)` remain standard.

---

## 6. Execution Model & `.hin` Files

Programs are written in files with the `.hin` extension:
```bash
# Example invocation
hinglish program.hin
```

### Execution Lifecycle:
1. **Source Ingestion**: Read UTF-8 encoded text from `program.hin`.
2. **Lexical Analysis**: Produce tokens (`KEYWORD`, `IDENTIFIER`, `NUMBER`, `STRING`, `INDENT`, `DEDENT`, `NEWLINE`).
3. **Syntax Analysis**: Build an abstract syntax tree representing statements and expressions.
4. **Compilation**: Lower the Hinglish AST into a Python AST or canonical Python source code.
5. **Execution**: Execute the generated Python program using Python's standard `compile()` and `exec()`, maintaining an environment with any Hinglish runtime helpers (e.g., `dikhao`).
