"""Standard JSON-RPC 2.0 Language Server implementation for Hinglish.

Communicates over stdio or any binary streams, supporting:
- Document synchronization (open, change, close)
- Live diagnostics publication (textDocument/publishDiagnostics)
- Code completion (textDocument/completion)
- Hover information (textDocument/hover)
- Go-to-Definition (textDocument/definition)
- Hierarchical Document Symbols (textDocument/documentSymbol)
- Find References (textDocument/references)
- Safe Rename (textDocument/rename)
"""

import sys
from typing import Any, BinaryIO, Dict, Optional

from .analyzer import HinglishAnalyzer
from .documents import DocumentManager
from .protocol import (
    Position,
    read_message,
    write_message,
)


class HinglishLanguageServer:
    """Hinglish Language Server protocol handler."""

    def __init__(
        self,
        in_stream: Optional[BinaryIO] = None,
        out_stream: Optional[BinaryIO] = None,
    ) -> None:
        self.in_stream: BinaryIO = in_stream or sys.stdin.buffer
        self.out_stream: BinaryIO = out_stream or sys.stdout.buffer
        self.documents = DocumentManager()
        self.analyzer = HinglishAnalyzer()
        self.is_running = False
        self.shutdown_received = False

    def send_response(
        self,
        request_id: Any,
        result: Any = None,
        error: Optional[Dict[str, Any]] = None,
    ) -> None:
        """Sends a JSON-RPC response."""
        payload: Dict[str, Any] = {"jsonrpc": "2.0", "id": request_id}
        if error is not None:
            payload["error"] = error
        else:
            payload["result"] = result
        write_message(self.out_stream, payload)

    def send_notification(self, method: str, params: Any = None) -> None:
        """Sends a JSON-RPC notification."""
        payload: Dict[str, Any] = {"jsonrpc": "2.0", "method": method}
        if params is not None:
            payload["params"] = params
        write_message(self.out_stream, payload)

    def publish_diagnostics(self, uri: str) -> None:
        """Runs diagnostics on the document and publishes results to the client."""
        doc = self.documents.get_document(uri)
        if doc is None:
            diagnostics = []
        else:
            diagnostics = self.analyzer.get_diagnostics(doc)

        self.send_notification(
            "textDocument/publishDiagnostics",
            {
                "uri": uri,
                "diagnostics": [diag.to_dict() for diag in diagnostics],
            },
        )

    def handle_message(self, message: Dict[str, Any]) -> None:
        """Dispatches an incoming JSON-RPC message to the appropriate handler."""
        method = message.get("method")
        msg_id = message.get("id")
        params = message.get("params", {})

        # Requests (have msg_id)
        if msg_id is not None:
            self._handle_request(method, msg_id, params)
        # Notifications (no msg_id)
        elif method is not None:
            self._handle_notification(method, params)

    def _handle_request(self, method: Optional[str], msg_id: Any, params: Dict[str, Any]) -> None:
        """Handles JSON-RPC request methods."""
        if method == "initialize":
            server_capabilities = {
                "capabilities": {
                    "textDocumentSync": 1,  # 1 = Full sync
                    "completionProvider": {
                        "resolveProvider": False,
                        "triggerCharacters": [".", " ", "(", ":"],
                    },
                    "hoverProvider": True,
                    "definitionProvider": True,
                    "documentSymbolProvider": True,
                    "referencesProvider": True,
                    "renameProvider": True,
                },
                "serverInfo": {
                    "name": "hinglish-lsp",
                    "version": "1.0.0",
                },
            }
            self.send_response(msg_id, result=server_capabilities)

        elif method == "shutdown":
            self.shutdown_received = True
            self.send_response(msg_id, result=None)

        elif method == "textDocument/completion":
            uri = params.get("textDocument", {}).get("uri", "")
            pos_dict = params.get("position", {})
            position = Position(
                line=pos_dict.get("line", 0),
                character=pos_dict.get("character", 0),
            )
            doc = self.documents.get_document(uri)
            if doc is None:
                self.send_response(msg_id, result=[])
            else:
                completions = self.analyzer.get_completions(doc, position)
                self.send_response(
                    msg_id, result=[item.to_dict() for item in completions]
                )

        elif method == "textDocument/hover":
            uri = params.get("textDocument", {}).get("uri", "")
            pos_dict = params.get("position", {})
            position = Position(
                line=pos_dict.get("line", 0),
                character=pos_dict.get("character", 0),
            )
            doc = self.documents.get_document(uri)
            if doc is None:
                self.send_response(msg_id, result=None)
            else:
                hover = self.analyzer.get_hover(doc, position)
                self.send_response(msg_id, result=hover)

        elif method == "textDocument/definition":
            uri = params.get("textDocument", {}).get("uri", "")
            pos_dict = params.get("position", {})
            position = Position(
                line=pos_dict.get("line", 0),
                character=pos_dict.get("character", 0),
            )
            doc = self.documents.get_document(uri)
            if doc is None:
                self.send_response(msg_id, result=None)
            else:
                defn = self.analyzer.get_definition(doc, position)
                if defn is None:
                    self.send_response(msg_id, result=None)
                elif isinstance(defn, list):
                    self.send_response(
                        msg_id, result=[loc.to_dict() for loc in defn]
                    )
                else:
                    self.send_response(msg_id, result=defn.to_dict())

        elif method == "textDocument/documentSymbol":
            uri = params.get("textDocument", {}).get("uri", "")
            doc = self.documents.get_document(uri)
            if doc is None:
                self.send_response(msg_id, result=[])
            else:
                symbols = self.analyzer.get_document_symbols(doc)
                self.send_response(
                    msg_id, result=[s.to_dict() for s in symbols]
                )

        elif method == "textDocument/references":
            uri = params.get("textDocument", {}).get("uri", "")
            pos_dict = params.get("position", {})
            position = Position(
                line=pos_dict.get("line", 0),
                character=pos_dict.get("character", 0),
            )
            context = params.get("context", {})
            include_decl = context.get("includeDeclaration", True)
            doc = self.documents.get_document(uri)
            if doc is None:
                self.send_response(msg_id, result=[])
            else:
                refs = self.analyzer.get_references(
                    doc, position, include_declaration=include_decl
                )
                self.send_response(
                    msg_id, result=[loc.to_dict() for loc in refs]
                )

        elif method == "textDocument/rename":
            uri = params.get("textDocument", {}).get("uri", "")
            pos_dict = params.get("position", {})
            position = Position(
                line=pos_dict.get("line", 0),
                character=pos_dict.get("character", 0),
            )
            new_name = params.get("newName", "")
            doc = self.documents.get_document(uri)
            if doc is None:
                self.send_response(msg_id, result=None)
            else:
                edit = self.analyzer.rename_symbol(doc, position, new_name)
                self.send_response(
                    msg_id, result=edit.to_dict() if edit else None
                )

        else:
            # Unhandled request
            self.send_response(
                msg_id,
                error={
                    "code": -32601,
                    "message": f"Method '{method}' not supported.",
                },
            )

    def _handle_notification(self, method: str, params: Dict[str, Any]) -> None:
        """Handles JSON-RPC notifications."""
        if method == "initialized":
            pass

        elif method == "exit":
            self.is_running = False

        elif method == "textDocument/didOpen":
            text_doc = params.get("textDocument", {})
            uri = text_doc.get("uri", "")
            text = text_doc.get("text", "")
            version = text_doc.get("version", 1)
            self.documents.open_document(uri, text, version)
            self.publish_diagnostics(uri)

        elif method == "textDocument/didChange":
            text_doc = params.get("textDocument", {})
            uri = text_doc.get("uri", "")
            version = text_doc.get("version", 1)
            changes = params.get("contentChanges", [])
            self.documents.change_document(uri, changes, version)
            self.publish_diagnostics(uri)

        elif method == "textDocument/didClose":
            text_doc = params.get("textDocument", {})
            uri = text_doc.get("uri", "")
            self.documents.close_document(uri)
            # Clear diagnostics
            self.send_notification(
                "textDocument/publishDiagnostics",
                {"uri": uri, "diagnostics": []},
            )

    def run(self) -> None:
        """Starts the main stdio event loop."""
        self.is_running = True
        try:
            while self.is_running:
                message = read_message(self.in_stream)
                if message is None:
                    break
                self.handle_message(message)
        except (KeyboardInterrupt, SystemExit):
            pass
        finally:
            self.is_running = False


def main() -> None:
    """Entry point for hinglish-lsp console command."""
    server = HinglishLanguageServer()
    server.run()


if __name__ == "__main__":
    main()
