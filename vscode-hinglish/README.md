# Hinglish Language Support for Visual Studio Code

This extension provides comprehensive language support, Language Server Protocol (LSP), and Debug Adapter Protocol (DAP) integration for the **Hinglish** programming language (`.hin`).

---

## Features

### 1. Source-Level Debugging (DAP)
- **Breakpoints**: Click the margin next to any line in a `.hin` file to set a breakpoint.
- **F5 Zero-Config Launch**: Press `F5` on any active `.hin` file to start debugging immediately.
- **Debug Controls**: Continue (`F5`), Step Over (`F10`), Step Into (`F11`), Step Out (`Shift+F11`), Pause (`F6`), and Stop (`Shift+F5`).
- **Variable Inspection**: Inspect local variables, function parameters, and globals in the Run & Debug panel.
- **Call Stack Navigation**: View active stack frames mapped directly to `.hin` files and line numbers.
- **Runtime Exceptions**: Execution pauses automatically on uncaught runtime errors at the exact Hinglish source line.
- **Multi-File Debugging**: Step seamlessly between imported `.hin` files (`se utils laao add`).

### 2. Real-Time Language Server (LSP)
- **Live Diagnostics**: Immediate lexical and syntax error checking with line and column indicators.
- **Contextual Autocompletion**: Hinglish keywords, builtins, code snippets, local functions, and variables.
- **Hover Documentation**: Detailed documentation and Python target equivalents for keywords and functions.
- **Go to Definition**: Jump to local definitions and cross-file imported symbols (`F12`).
- **Document Outline**: Hierarchical tree of classes, methods, and functions in the Outline panel.
- **Find References & Rename**: Find all usages (`Shift+F12`) and safely rename identifiers (`F2`).

### 3. Syntax Highlighting & Language Configuration
- Automatic recognition of `.hin` files.
- Highlighting for keywords, operators, strings, f-strings, decorators, and comments.
- Smart auto-closing pairs and indentation rules.

---

## Debugger Configuration (`launch.json`)

To customize your debug session, create a `.vscode/launch.json` file in your workspace:

```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "type": "hinglish",
      "request": "launch",
      "name": "Debug Hinglish (${fileBasename})",
      "program": "${file}",
      "stopOnEntry": false,
      "args": []
    }
  ]
}
```

---

## Configuration Settings

| Setting | Type | Default | Description |
|---|---|---|---|
| `hinglish.lsp.enabled` | `boolean` | `true` | Enable Language Server for autocompletion, diagnostics, and hover. |
| `hinglish.lsp.path` | `string` | `"hinglish-lsp"` | Path to the language server executable. |
| `hinglish.lsp.pythonPath` | `string` | `"python3"` | Fallback Python interpreter for LSP. |
| `hinglish.dap.path` | `string` | `"hinglish-dap"` | Path to the Debug Adapter executable. |
| `hinglish.dap.pythonPath` | `string` | `"python3"` | Fallback Python interpreter for DAP. |

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
code --install-extension vscode-hinglish/hinglish-1.1.0.vsix
```
Or in VS Code:
1. Open the Extensions view (`Ctrl+Shift+X` or `Cmd+Shift+X`).
2. Click the `...` menu in the top-right.
3. Select **Install from VSIX...** and choose `hinglish-1.1.0.vsix`.
