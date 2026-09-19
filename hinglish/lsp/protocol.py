"""Language Server Protocol (LSP) types, enums, and JSON-RPC 2.0 framing.

Provides standard definitions for:
- JSON-RPC 2.0 message framing over stdio
- LSP Positions, Ranges, Locations, and TextEdits
- Enums for DiagnosticSeverity, CompletionItemKind, SymbolKind
"""

import json
import sys
from dataclasses import asdict, dataclass, field
from enum import IntEnum
from typing import Any, BinaryIO, Dict, List, Optional, Union


# -----------------------------------------------------------------------------
# LSP Enums
# -----------------------------------------------------------------------------


class DiagnosticSeverity(IntEnum):
    """LSP Diagnostic Severities."""
    Error = 1
    Warning = 2
    Information = 3
    Hint = 4


class CompletionItemKind(IntEnum):
    """LSP Completion Item Kinds."""
    Text = 1
    Method = 2
    Function = 3
    Constructor = 4
    Field = 5
    Variable = 6
    Class = 7
    Interface = 8
    Module = 9
    Property = 10
    Unit = 11
    Value = 12
    Enum = 13
    Keyword = 14
    Snippet = 15
    Color = 16
    File = 17
    Reference = 18
    Folder = 19
    EnumMember = 20
    Constant = 21
    Struct = 22
    Event = 23
    Operator = 24
    TypeParameter = 25


class SymbolKind(IntEnum):
    """LSP Symbol Kinds."""
    File = 1
    Module = 2
    Namespace = 3
    Package = 4
    Class = 5
    Method = 6
    Property = 7
    Field = 8
    Constructor = 9
    Enum = 10
    Interface = 11
    Function = 12
    Variable = 13
    Constant = 14
    String = 15
    Number = 16
    Boolean = 17
    Array = 18
    Object = 19
    Key = 20
    Null = 21
    EnumMember = 22
    Struct = 23
    Event = 24
    Operator = 25
    TypeParameter = 26


# -----------------------------------------------------------------------------
# LSP Data Structures
# -----------------------------------------------------------------------------


@dataclass
class Position:
    """LSP 0-indexed Position (line, character)."""
    line: int
    character: int

    def to_dict(self) -> Dict[str, int]:
        return {"line": self.line, "character": self.character}


@dataclass
class Range:
    """LSP Range representing start and end positions."""
    start: Position
    end: Position

    def to_dict(self) -> Dict[str, Any]:
        return {"start": self.start.to_dict(), "end": self.end.to_dict()}


@dataclass
class Location:
    """LSP Location representing a URI and Range."""
    uri: str
    range: Range

    def to_dict(self) -> Dict[str, Any]:
        return {"uri": self.uri, "range": self.range.to_dict()}


@dataclass
class Diagnostic:
    """LSP Diagnostic representation."""
    range: Range
    message: str
    severity: int = DiagnosticSeverity.Error
    source: str = "hinglish"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "range": self.range.to_dict(),
            "message": self.message,
            "severity": self.severity,
            "source": self.source,
        }


@dataclass
class CompletionItem:
    """LSP Completion Item."""
    label: str
    kind: int
    detail: Optional[str] = None
    documentation: Optional[str] = None
    insert_text: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        d: Dict[str, Any] = {"label": self.label, "kind": self.kind}
        if self.detail:
            d["detail"] = self.detail
        if self.documentation:
            d["documentation"] = self.documentation
        if self.insert_text:
            d["insertText"] = self.insert_text
        return d


@dataclass
class DocumentSymbol:
    """LSP Hierarchical Document Symbol."""
    name: str
    kind: int
    range: Range
    selection_range: Range
    detail: Optional[str] = None
    children: List["DocumentSymbol"] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        d: Dict[str, Any] = {
            "name": self.name,
            "kind": self.kind,
            "range": self.range.to_dict(),
            "selectionRange": self.selection_range.to_dict(),
        }
        if self.detail:
            d["detail"] = self.detail
        if self.children:
            d["children"] = [child.to_dict() for child in self.children]
        return d


@dataclass
class TextEdit:
    """LSP Text Edit."""
    range: Range
    new_text: str

    def to_dict(self) -> Dict[str, Any]:
        return {"range": self.range.to_dict(), "newText": self.new_text}


@dataclass
class WorkspaceEdit:
    """LSP Workspace Edit."""
    changes: Dict[str, List[TextEdit]] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "changes": {
                uri: [edit.to_dict() for edit in edits]
                for uri, edits in self.changes.items()
            }
        }


# -----------------------------------------------------------------------------
# JSON-RPC 2.0 Framing
# -----------------------------------------------------------------------------


def read_message(stream: BinaryIO) -> Optional[Dict[str, Any]]:
    """Reads a single JSON-RPC 2.0 message with Content-Length header from a binary stream."""
    content_length: Optional[int] = None

    # Read headers
    while True:
        line_bytes = stream.readline()
        if not line_bytes:
            return None  # Stream closed
        line = line_bytes.decode("latin1")
        if line in ("\r\n", "\n"):
            break  # End of headers
        if ":" in line:
            header_name, header_value = line.split(":", 1)
            if header_name.strip().lower() == "content-length":
                try:
                    content_length = int(header_value.strip())
                except ValueError:
                    pass

    if content_length is None:
        return None

    # Read body
    body_bytes = stream.read(content_length)
    if not body_bytes:
        return None

    try:
        return json.loads(body_bytes.decode("utf-8"))
    except json.JSONDecodeError:
        return None


def write_message(stream: BinaryIO, payload: Dict[str, Any]) -> None:
    """Encodes and writes a JSON-RPC 2.0 message with Content-Length header to a binary stream."""
    body_bytes = json.dumps(payload, separators=(",", ":")).encode("utf-8")
    header = f"Content-Length: {len(body_bytes)}\r\n\r\n".encode("latin1")
    stream.write(header)
    stream.write(body_bytes)
    stream.flush()
