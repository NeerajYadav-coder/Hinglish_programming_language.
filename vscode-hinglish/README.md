# Hinglish Language Support for Visual Studio Code

This extension provides comprehensive language support and Language Server Protocol (LSP) integration for the **Hinglish** programming language (`.hin`).

---

## Features

### 1. Real-Time Language Server (LSP)
- **Live Diagnostics**: Immediate lexical and syntax error checking as you type, with exact line and column indicators.
- **Contextual Autocompletion**:
  - Full keyword registry (`agar`, `kaam`, `har`, `shreni`, etc.) with Python target information.
  - Built-in functions (`dikhao`, `pucho`, `lambai`, `prakar`, etc.).
  - Code snippets for functions, classes, conditionals, loops, and exception handling.
  - Local variables, parameters, and function/class symbols.
- **Hover Documentation**:
  - Inspect keywords and built-in functions with explanation and Python target equivalent.
  - Function and class signatures with parameter lists.
- **Go to Definition**:
  - Jump to definitions for local functions, classes, variables, and parameters.
  - Cross-file navigation across sibling `.hin` files and imported modules (`laao utils`, `se models laao User`).
- **Document Outline & Breadcrumbs**: Hierarchical symbol tree of classes, methods, functions, and variables.
- **Find References**: Locate all usages of any identifier across the document.
- **Safe Rename Symbol**: Rename identifiers safely across the document.

### 2. Syntax Highlighting & Language Configuration
- **Automatic File Association**: Recognizes `.hin` files automatically.
- **Rich Syntax Highlighting**: Declarations, control flow, pattern matching, async constructs, exceptions, literals, and f-strings.
- **Smart Indentation & Brackets**: Auto-closing pairs and Pythonic block indentation rules.

---

## Configuration Settings

| Setting | Type | Default | Description |
|---|---|---|---|
| `hinglish.lsp.enabled` | `boolean` | `true` | Enable Hinglish Language Server for intelligent editing features. |
| `hinglish.lsp.path` | `string` | `"hinglish-lsp"` | Path to the `hinglish-lsp` command. |
| `hinglish.lsp.pythonPath` | `string` | `"python3"` | Python interpreter used for fallback (`python3 -m hinglish.lsp`). |
| `hinglish.lsp.trace.server` | `string` | `"off"` | Traces communication between VS Code and the server (`off`, `messages`, `verbose`). |

---

## Installation

### Prerequisites
Make sure Hinglish is installed in your Python environment:
```bash
pip install hinglish
# or install from source
pip install -e .
```

### Install Extension in VS Code
```bash
code --install-extension vscode-hinglish/hinglish-1.0.0.vsix
```
Or in VS Code:
1. Press `Ctrl+Shift+X` (or `Cmd+Shift+X` on macOS) to open the Extensions view.
2. Click the `...` menu in the top-right of the Extensions panel.
3. Select **Install from VSIX...** and choose `hinglish-1.0.0.vsix`.
