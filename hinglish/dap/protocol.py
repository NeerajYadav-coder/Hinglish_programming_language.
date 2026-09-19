"""Debug Adapter Protocol (DAP) types, data structures, and stdio framing.

Provides standard definitions for:
- DAP message framing over stdio (Content-Length header)
- Protocol requests, responses, and events
- Stack frames, scopes, variables, and breakpoints data structures
"""

import json
from dataclasses import dataclass, field
from typing import Any, BinaryIO, Dict, List, Optional


def read_dap_message(stream: BinaryIO) -> Optional[Dict[str, Any]]:
    """Reads a single DAP message with Content-Length header from a binary stream."""
    content_length: Optional[int] = None

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

    body_bytes = stream.read(content_length)
    if not body_bytes:
        return None

    try:
        return json.loads(body_bytes.decode("utf-8"))
    except json.JSONDecodeError:
        return None


def write_dap_message(stream: BinaryIO, payload: Dict[str, Any]) -> None:
    """Encodes and writes a DAP message with Content-Length header to a binary stream."""
    body_bytes = json.dumps(payload, separators=(",", ":")).encode("utf-8")
    header = f"Content-Length: {len(body_bytes)}\r\n\r\n".encode("latin1")
    stream.write(header)
    stream.write(body_bytes)
    stream.flush()


class DapMessageBuilder:
    """Helper to construct sequential DAP responses and events."""

    def __init__(self) -> None:
        self._seq = 1

    def next_seq(self) -> int:
        seq = self._seq
        self._seq += 1
        return seq

    def response(
        self,
        request: Dict[str, Any],
        body: Optional[Dict[str, Any]] = None,
        success: bool = True,
        message: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Builds a DAP response message for a request."""
        res: Dict[str, Any] = {
            "seq": self.next_seq(),
            "type": "response",
            "request_seq": request.get("seq", 0),
            "command": request.get("command", ""),
            "success": success,
        }
        if body is not None:
            res["body"] = body
        if message is not None:
            res["message"] = message
        return res

    def event(self, event_name: str, body: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Builds a DAP event message."""
        res: Dict[str, Any] = {
            "seq": self.next_seq(),
            "type": "event",
            "event": event_name,
        }
        if body is not None:
            res["body"] = body
        return res


@dataclass
class Source:
    """DAP Source representation."""
    path: str
    name: str

    def to_dict(self) -> Dict[str, Any]:
        return {"name": self.name, "path": self.path}


@dataclass
class Breakpoint:
    """DAP Breakpoint representation."""
    id: int
    verified: bool
    line: int
    source: Optional[Source] = None
    message: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        d: Dict[str, Any] = {
            "id": self.id,
            "verified": self.verified,
            "line": self.line,
        }
        if self.source:
            d["source"] = self.source.to_dict()
        if self.message:
            d["message"] = self.message
        return d


@dataclass
class StackFrame:
    """DAP StackFrame representation."""
    id: int
    name: str
    source: Source
    line: int
    column: int = 1

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "source": self.source.to_dict(),
            "line": self.line,
            "column": self.column,
        }


@dataclass
class Scope:
    """DAP Scope representation."""
    name: str
    variables_reference: int
    expensive: bool = False

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "variablesReference": self.variables_reference,
            "expensive": self.expensive,
        }


@dataclass
class Variable:
    """DAP Variable representation."""
    name: str
    value: str
    type: str
    variables_reference: int = 0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "value": self.value,
            "type": self.type,
            "variablesReference": self.variables_reference,
        }


@dataclass
class ThreadInfo:
    """DAP Thread representation."""
    id: int
    name: str

    def to_dict(self) -> Dict[str, Any]:
        return {"id": self.id, "name": self.name}
