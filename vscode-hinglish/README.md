# Hinglish Language Support for Visual Studio Code

This extension provides syntax highlighting, language identification, and editor configurations for the **Hinglish** programming language (`.hin`).

---

## Features

- **Automatic File Association**: Recognizes `.hin` files automatically and assigns the `hinglish` language mode.
- **Rich Syntax Highlighting**:
  - Declarations: `kaam` (functions), `varg` / `shreni` (classes), `sookshm` (lambda)
  - Control Flow: `agar`, `warna`, `warna_agar`, `jabtak`, `har`, `mein`, `ruko`, `aage_bado`, `chhod_do`
  - Pattern Matching: `milao` / `milaao`, `sthiti` / `vichaar`
  - Asynchronous: `asamanantar`, `intezaar`
  - Exception Handling: `koshish`, `pakdo`, `sambhalo`, `antatah`, `uthav`, `daawa`
  - Scoping & Imports: `sarvavyapi`, `asthanik`, `saath`, `hatao`, `laao`, `se`, `jaise`
  - Literals & Builtins: `sahi`, `galat`, `shunya`, `kuch_nahi`, `dikhao`, `lambai`, `kram`
  - Decorators: `@property` and custom decorators
  - String Interpolation: Formatted strings (`f"..."`, `f'...'`) with embedded expression highlighting
- **Smart Language Configuration**:
  - Line comments (`#`)
  - Auto-closing pairs for parentheses `()`, brackets `[]`, braces `{}`, and quotes
  - Pythonic block indentation rules for colons `:` and dedent keywords (`warna`, `pakdo`, etc.)

---

## Installation

### From VSIX Package

1. Package the extension:
   ```bash
   cd vscode-hinglish
   vsce package --no-dependencies
   ```
2. Install in VS Code:
   ```bash
   code --install-extension hinglish-1.0.0.vsix
   ```
   Or open VS Code, go to the Extensions view (`Ctrl+Shift+X`), select the `...` menu, and choose **Install from VSIX...**.

---

## Current Scope & Roadmap

- **Step 10C (Current)**: Declarative TextMate syntax highlighting and language configuration.
- **Future Phases**: Language Server Protocol (LSP) for autocompletion, hover documentation, semantic diagnostics, and go-to-definition.
