"""In-memory Document Store and text management for Hinglish LSP."""

import re
from typing import Any, Dict, List, Optional
from urllib.parse import unquote, urlparse
from pathlib import Path

from .protocol import Position, Range


class Document:
    """Represents an open text document in the editor."""

    def __init__(self, uri: str, text: str, version: int = 1) -> None:
        self.uri = uri
        self.text = text
        self.version = version
        self.lines: List[str] = text.splitlines(keepends=True)
        self.file_path: Optional[Path] = self._uri_to_path(uri)

    @property
    def source(self) -> str:
        """Alias for text property."""
        return self.text

    def _uri_to_path(self, uri: str) -> Optional[Path]:
        """Converts file:// URI to a local Path object."""
        if uri.startswith("file://"):
            parsed = urlparse(uri)
            return Path(unquote(parsed.path))
        return None

    def update_text(self, text: str, version: int) -> None:
        """Updates full document text and lines."""
        self.text = text
        self.version = version
        self.lines = text.splitlines(keepends=True)

    def apply_change(self, change: Dict[str, Any], version: int) -> None:
        """Applies a text change (full sync or incremental)."""
        if "range" not in change:
            # Full content sync
            self.update_text(change.get("text", ""), version)
        else:
            # Incremental sync (if provided)
            # For robustness, if full text is not provided, we replace range
            range_info = change["range"]
            start_line = range_info["start"]["line"]
            start_char = range_info["start"]["character"]
            end_line = range_info["end"]["line"]
            end_char = range_info["end"]["character"]
            new_text = change.get("text", "")

            lines = self.lines[:]
            # Convert to flat text with replacement
            before = "".join(lines[:start_line])
            if start_line < len(lines):
                before += lines[start_line][:start_char]
            after = ""
            if end_line < len(lines):
                after += lines[end_line][end_char:]
            after += "".join(lines[end_line + 1:])
            self.update_text(before + new_text + after, version)

    def get_line(self, line_number: int) -> str:
        """Returns the content of a line (0-indexed)."""
        if 0 <= line_number < len(self.lines):
            return self.lines[line_number]
        return ""

    def get_word_at_position(self, position: Position) -> Optional[str]:
        """Extracts the identifier or keyword word at the given 0-indexed position."""
        line = self.get_line(position.line)
        if not line or position.character >= len(line):
            return None

        # Regex for valid Hinglish identifiers / keywords (letters, digits, underscores)
        pattern = re.compile(r"[a-zA-Z_][a-zA-Z0-9_]*")
        for match in pattern.finditer(line):
            start, end = match.span()
            if start <= position.character <= end:
                return match.group(0)
        return None

    def get_word_range_at_position(self, position: Position) -> Optional[Range]:
        """Returns the LSP Range for the word at the given 0-indexed position."""
        line = self.get_line(position.line)
        if not line:
            return None

        pattern = re.compile(r"[a-zA-Z_][a-zA-Z0-9_]*")
        for match in pattern.finditer(line):
            start, end = match.span()
            if start <= position.character <= end:
                return Range(
                    start=Position(line=position.line, character=start),
                    end=Position(line=position.line, character=end),
                )
        return None


class DocumentManager:
    """Manages all open documents within the language server."""

    def __init__(self) -> None:
        self._documents: Dict[str, Document] = {}

    def open_document(self, uri: str, text: str, version: int = 1) -> Document:
        doc = Document(uri=uri, text=text, version=version)
        self._documents[uri] = doc
        return doc

    def change_document(
        self, uri: str, changes: List[Dict[str, Any]], version: int
    ) -> Optional[Document]:
        doc = self._documents.get(uri)
        if doc is not None:
            for change in changes:
                doc.apply_change(change, version)
        return doc

    def close_document(self, uri: str) -> None:
        self._documents.pop(uri, None)

    def get_document(self, uri: str) -> Optional[Document]:
        return self._documents.get(uri)

    def all_documents(self) -> List[Document]:
        return list(self._documents.values())
