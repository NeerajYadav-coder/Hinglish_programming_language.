"""Hinglish Language Server Protocol package.

Provides zero-runtime-dependency LSP server for editor integrations.
"""

from .analyzer import HinglishAnalyzer
from .documents import Document, DocumentManager
from .protocol import (
    CompletionItem,
    CompletionItemKind,
    Diagnostic,
    DiagnosticSeverity,
    DocumentSymbol,
    Location,
    Position,
    Range,
    SymbolKind,
    TextEdit,
    WorkspaceEdit,
)
from .server import HinglishLanguageServer, main

__all__ = [
    "HinglishLanguageServer",
    "HinglishAnalyzer",
    "Document",
    "DocumentManager",
    "Position",
    "Range",
    "Location",
    "Diagnostic",
    "DiagnosticSeverity",
    "CompletionItem",
    "CompletionItemKind",
    "DocumentSymbol",
    "SymbolKind",
    "TextEdit",
    "WorkspaceEdit",
    "main",
]
