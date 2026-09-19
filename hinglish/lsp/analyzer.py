"""Semantic analyzer and LSP feature provider for Hinglish source files.

Leverages the official Hinglish Lexer, Parser, AST, and Keyword Registry to provide:
- Live syntax diagnostics with 0-indexed positions
- Contextual code completion (keywords, builtins, local symbols, snippets)
- Rich hover information with Python equivalents and documentation
- Go-to-Definition (local definitions and cross-file .hin resolution)
- Hierarchical Document Symbols (Outline view)
- Find references
- Safe identifier renaming
"""

import re
from pathlib import Path
from typing import Any, Dict, Generator, List, Optional, Set, Tuple, Union

from ..ast.nodes import (
    ASTNode,
    Assignment,
    ClassDefinition,
    FromImport,
    FunctionCall,
    FunctionDefinition,
    Identifier,
    Import,
    Parameter,
    Program,
)
from ..exceptions import HinglishError
from ..keywords import DEFAULT_KEYWORD_REGISTRY, KeywordRegistry
from ..lexer import tokenize
from ..lexer.tokens import Position as LexerPosition, Token, TokenType
from ..parser import parse
from .documents import Document
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


def _to_lsp_pos(pos: Optional[LexerPosition]) -> Position:
    """Converts 1-indexed LexerPosition to 0-indexed LSP Position."""
    if pos is None:
        return Position(line=0, character=0)
    return Position(line=max(0, pos.line - 1), character=max(0, pos.column - 1))


def _node_range(node: ASTNode, fallback_len: int = 1) -> Range:
    """Computes an LSP Range for an AST node."""
    start = _to_lsp_pos(node.start_pos)
    if node.end_pos and (
        node.end_pos.line > (node.start_pos.line if node.start_pos else 0)
        or node.end_pos.column > (node.start_pos.column if node.start_pos else 0)
    ):
        end = _to_lsp_pos(node.end_pos)
    else:
        end = Position(line=start.line, character=start.character + max(1, fallback_len))
    return Range(start=start, end=end)


def _token_range(tok: Token) -> Range:
    """Computes an LSP Range for a lexical Token."""
    return Range(start=_to_lsp_pos(tok.start_pos), end=_to_lsp_pos(tok.end_pos))


def walk_ast(node: ASTNode) -> Generator[ASTNode, None, None]:
    """Recursively yields all AST nodes in pre-order traversal."""
    yield node
    for val in vars(node).values():
        if isinstance(val, ASTNode):
            yield from walk_ast(val)
        elif isinstance(val, list):
            for item in val:
                if isinstance(item, ASTNode):
                    yield from walk_ast(item)
        elif isinstance(val, tuple):
            for item in val:
                if isinstance(item, ASTNode):
                    yield from walk_ast(item)
        elif isinstance(val, dict):
            for item in val.values():
                if isinstance(item, ASTNode):
                    yield from walk_ast(item)


class HinglishAnalyzer:
    """Analyzes Hinglish documents and computes LSP responses."""

    def __init__(self, registry: Optional[KeywordRegistry] = None) -> None:
        self.registry = registry or DEFAULT_KEYWORD_REGISTRY

    # -------------------------------------------------------------------------
    # Diagnostics
    # -------------------------------------------------------------------------

    def get_diagnostics(self, doc: Document) -> List[Diagnostic]:
        """Analyzes the document for lexical and grammatical errors."""
        try:
            # First pass: lexing
            tokens = tokenize(doc.text, registry=self.registry, include_comments=False)
            # Second pass: parsing
            parse(tokens, registry=self.registry)
            return []
        except HinglishError as err:
            line_idx = max(0, (err.line or 1) - 1)
            col_idx = max(0, (err.column or 1) - 1)
            line_content = doc.get_line(line_idx)
            end_char = len(line_content) if line_content else col_idx + 1
            if end_char <= col_idx:
                end_char = col_idx + 1

            rng = Range(
                start=Position(line=line_idx, character=col_idx),
                end=Position(line=line_idx, character=end_char),
            )
            return [
                Diagnostic(
                    range=rng,
                    message=err.message or str(err),
                    severity=DiagnosticSeverity.Error,
                    source="hinglish",
                )
            ]
        except Exception:
            # Fallback guard to ensure the language server never crashes
            return []

    # -------------------------------------------------------------------------
    # Completions
    # -------------------------------------------------------------------------

    def get_completions(self, doc: Document, position: Position) -> List[CompletionItem]:
        """Generates completion suggestions at the current cursor position."""
        completions: List[CompletionItem] = []
        seen_items: Set[Tuple[str, int]] = set()

        def add_item(item: CompletionItem) -> None:
            key = (item.label, item.kind)
            if key not in seen_items:
                seen_items.add(key)
                completions.append(item)

        # 1. Keywords & Builtins from the Registry
        for word in sorted(self.registry.all_hinglish_words()):
            py_eq = self.registry.get_python_equivalent(word)
            canonical = self.registry.get_canonical_hinglish(word)

            if self.registry.is_builtin_function(word):
                kind = CompletionItemKind.Function
                detail = f"Built-in function ({py_eq})"
                doc_text = f"**Hinglish Built-in**: `{word}`\n\nPython target: `{py_eq}`"
            else:
                kind = CompletionItemKind.Keyword
                detail = f"Hinglish keyword -> {py_eq}"
                alias_str = f" (alias for `{canonical}`)" if canonical != word else ""
                doc_text = f"**Hinglish Keyword**: `{word}`{alias_str}\n\nPython target: `{py_eq}`"

            add_item(
                CompletionItem(
                    label=word,
                    kind=kind,
                    detail=detail,
                    documentation=doc_text,
                )
            )

        # 2. Hinglish Snippets
        snippets = [
            ("kaam", CompletionItemKind.Snippet, "kaam ${1:naam}(${2:params}):\n    ${0:chhod_do}", "Function definition"),
            ("varg", CompletionItemKind.Snippet, "varg ${1:Naam}:\n    kaam __init__(khud):\n        ${0:chhod_do}", "Class definition"),
            ("shreni", CompletionItemKind.Snippet, "shreni ${1:Naam}:\n    kaam __init__(khud):\n        ${0:chhod_do}", "Class definition (alias)"),
            ("agar", CompletionItemKind.Snippet, "agar ${1:shart}:\n    ${0:chhod_do}", "If conditional"),
            ("agar_warna", CompletionItemKind.Snippet, "agar ${1:shart}:\n    ${2:chhod_do}\nwarna:\n    ${0:chhod_do}", "If-Else conditional"),
            ("har", CompletionItemKind.Snippet, "har ${1:item} mein ${2:items}:\n    ${0:chhod_do}", "For loop"),
            ("jabtak", CompletionItemKind.Snippet, "jabtak ${1:shart}:\n    ${0:chhod_do}", "While loop"),
            ("koshish", CompletionItemKind.Snippet, "koshish:\n    ${1:chhod_do}\npakdo ${2:Exception} jaise ${3:e}:\n    ${0:dikhao(e)}", "Try-Except block"),
        ]
        for label, kind, insert_text, doc_text in snippets:
            add_item(
                CompletionItem(
                    label=label,
                    kind=kind,
                    detail=f"Hinglish snippet: {label}",
                    documentation=doc_text,
                    insert_text=insert_text,
                )
            )

        # 3. Local Symbols from AST / Lexer
        ast = self._safe_parse(doc.text)
        if ast:
            for node in walk_ast(ast):
                if isinstance(node, FunctionDefinition) and node.name:
                    params_str = ", ".join(
                        p.name if hasattr(p, "name") else str(p)
                        for p in (node.parameters or node.params)
                    )
                    add_item(
                        CompletionItem(
                            label=node.name,
                            kind=CompletionItemKind.Function,
                            detail=f"kaam {node.name}({params_str})",
                            documentation="User-defined function",
                        )
                    )
                    # Add parameters
                    for p in node.parameters:
                        if p.name:
                            add_item(
                                CompletionItem(
                                    label=p.name,
                                    kind=CompletionItemKind.Variable,
                                    detail=f"parameter {p.name}",
                                )
                            )
                elif isinstance(node, ClassDefinition) and node.name:
                    add_item(
                        CompletionItem(
                            label=node.name,
                            kind=CompletionItemKind.Class,
                            detail=f"shreni {node.name}",
                            documentation="User-defined class",
                        )
                    )
                elif isinstance(node, Assignment) and isinstance(node.target, Identifier):
                    add_item(
                        CompletionItem(
                            label=node.target.name,
                            kind=CompletionItemKind.Variable,
                            detail=f"variable {node.target.name}",
                        )
                    )
                elif isinstance(node, Import):
                    for mod, alias in node.names:
                        target = alias or mod
                        add_item(
                            CompletionItem(
                                label=target,
                                kind=CompletionItemKind.Module,
                                detail=f"laao {mod}",
                            )
                        )
                elif isinstance(node, FromImport):
                    for name, alias in node.names:
                        target = alias or name
                        add_item(
                            CompletionItem(
                                label=target,
                                kind=CompletionItemKind.Variable,
                                detail=f"se {node.module} laao {name}",
                            )
                        )

        return completions

    # -------------------------------------------------------------------------
    # Hover
    # -------------------------------------------------------------------------

    def get_hover(self, doc: Document, position: Position) -> Optional[Dict[str, Any]]:
        """Provides rich markdown hover information for the symbol under the cursor."""
        word = doc.get_word_at_position(position)
        if not word:
            return None

        # 1. Keywords & Builtins
        if self.registry.is_keyword(word):
            py_eq = self.registry.get_python_equivalent(word)
            canonical = self.registry.get_canonical_hinglish(word)
            if self.registry.is_builtin_function(word):
                md = (
                    f"### `(builtin) {word}`\n\n"
                    f"**Python equivalent**: `{py_eq}`\n\n"
                    f"Standard built-in function in Hinglish runtime."
                )
            else:
                alias_str = f"\n\n*Canonical*: `{canonical}`" if canonical != word else ""
                md = (
                    f"### `(keyword) {word}`\n\n"
                    f"**Python equivalent**: `{py_eq}`{alias_str}\n\n"
                    f"Core Hinglish language keyword."
                )
            return {"contents": {"kind": "markdown", "value": md}}

        # 2. Local AST definitions
        ast = self._safe_parse(doc.text)
        if ast:
            for node in walk_ast(ast):
                if isinstance(node, FunctionDefinition) and node.name == word:
                    params_str = ", ".join(
                        p.name if hasattr(p, "name") else str(p)
                        for p in (node.parameters or node.params)
                    )
                    async_prefix = "asamanantar " if node.is_async else ""
                    md = (
                        f"### `(function) {async_prefix}kaam {node.name}({params_str})`\n\n"
                        f"User-defined Hinglish function."
                    )
                    return {"contents": {"kind": "markdown", "value": md}}
                elif isinstance(node, ClassDefinition) and node.name == word:
                    bases_str = ""
                    if node.bases:
                        bases_names = [getattr(b, "name", str(b)) for b in node.bases]
                        bases_str = f"({', '.join(bases_names)})"
                    md = (
                        f"### `(class) shreni {node.name}{bases_str}`\n\n"
                        f"User-defined Hinglish class."
                    )
                    return {"contents": {"kind": "markdown", "value": md}}
                elif isinstance(node, Assignment) and isinstance(node.target, Identifier) and node.target.name == word:
                    md = (
                        f"### `(variable) {word}`\n\n"
                        f"Variable defined in this module."
                    )
                    return {"contents": {"kind": "markdown", "value": md}}
                elif isinstance(node, Parameter) and node.name == word:
                    md = (
                        f"### `(parameter) {word}`\n\n"
                        f"Function parameter."
                    )
                    return {"contents": {"kind": "markdown", "value": md}}

        # 3. Cross-file definitions in sibling modules
        cross_loc = self._resolve_cross_file_symbol(doc, word)
        if cross_loc:
            md = (
                f"### `(imported symbol) {word}`\n\n"
                f"Defined in: `{Path(cross_loc.uri).name}`"
            )
            return {"contents": {"kind": "markdown", "value": md}}

        return None

    # -------------------------------------------------------------------------
    # Go to Definition
    # -------------------------------------------------------------------------

    def get_definition(self, doc: Document, position: Position) -> Union[Location, List[Location], None]:
        """Resolves the definition location for the symbol under the cursor."""
        word = doc.get_word_at_position(position)
        if not word:
            return None

        # 1. Search local AST
        ast = self._safe_parse(doc.text)
        if ast:
            # Check functions
            for node in walk_ast(ast):
                if isinstance(node, FunctionDefinition) and node.name == word:
                    line_idx = _to_lsp_pos(node.start_pos).line
                    return Location(uri=doc.uri, range=_name_range(node.name, node, doc.get_line(line_idx)))
                elif isinstance(node, ClassDefinition) and node.name == word:
                    line_idx = _to_lsp_pos(node.start_pos).line
                    return Location(uri=doc.uri, range=_name_range(node.name, node, doc.get_line(line_idx)))
                elif isinstance(node, Assignment) and isinstance(node.target, Identifier) and node.target.name == word:
                    return Location(uri=doc.uri, range=_node_range(node.target, len(word)))

            # Check parameters within current enclosing function
            func_node = self._find_enclosing_function(ast, position)
            if func_node:
                for param in func_node.parameters:
                    if param.name == word:
                        return Location(uri=doc.uri, range=_node_range(param, len(word)))

        # 2. Check imports / cross-file symbols
        cross_loc = self._resolve_cross_file_symbol(doc, word)
        if cross_loc:
            return cross_loc

        return None

    # -------------------------------------------------------------------------
    # Document Symbols (Outline View)
    # -------------------------------------------------------------------------

    def get_document_symbols(self, doc: Document) -> List[DocumentSymbol]:
        """Computes hierarchical document symbols for the editor outline view."""
        symbols: List[DocumentSymbol] = []
        ast = self._safe_parse(doc.text)
        if not ast:
            return symbols

        for stmt in ast.body:
            if isinstance(stmt, ClassDefinition) and stmt.name:
                cls_range = _node_range(stmt)
                cls_line = doc.get_line(_to_lsp_pos(stmt.start_pos).line)
                cls_sel = _name_range(stmt.name, stmt, cls_line)
                children: List[DocumentSymbol] = []
                for inner in stmt.body:
                    if isinstance(inner, FunctionDefinition) and inner.name:
                        m_range = _node_range(inner)
                        m_line = doc.get_line(_to_lsp_pos(inner.start_pos).line)
                        m_sel = _name_range(inner.name, inner, m_line)
                        children.append(
                            DocumentSymbol(
                                name=inner.name,
                                kind=SymbolKind.Method,
                                range=m_range,
                                selection_range=m_sel,
                                detail=f"kaam {inner.name}(...)",
                            )
                        )
                    elif isinstance(inner, Assignment) and isinstance(inner.target, Identifier):
                        f_range = _node_range(inner)
                        f_sel = _node_range(inner.target, len(inner.target.name))
                        children.append(
                            DocumentSymbol(
                                name=inner.target.name,
                                kind=SymbolKind.Field,
                                range=f_range,
                                selection_range=f_sel,
                            )
                        )
                symbols.append(
                    DocumentSymbol(
                        name=stmt.name,
                        kind=SymbolKind.Class,
                        range=cls_range,
                        selection_range=cls_sel,
                        detail=f"shreni {stmt.name}",
                        children=children,
                    )
                )
            elif isinstance(stmt, FunctionDefinition) and stmt.name:
                f_range = _node_range(stmt)
                f_line = doc.get_line(_to_lsp_pos(stmt.start_pos).line)
                f_sel = _name_range(stmt.name, stmt, f_line)
                symbols.append(
                    DocumentSymbol(
                        name=stmt.name,
                        kind=SymbolKind.Function,
                        range=f_range,
                        selection_range=f_sel,
                        detail=f"kaam {stmt.name}(...)",
                    )
                )
            elif isinstance(stmt, Assignment) and isinstance(stmt.target, Identifier):
                v_range = _node_range(stmt)
                v_sel = _node_range(stmt.target, len(stmt.target.name))
                symbols.append(
                    DocumentSymbol(
                        name=stmt.target.name,
                        kind=SymbolKind.Variable,
                        range=v_range,
                        selection_range=v_sel,
                    )
                )

        return symbols

    # -------------------------------------------------------------------------
    # References & Rename
    # -------------------------------------------------------------------------

    def get_references(
        self, doc: Document, position: Position, include_declaration: bool = True
    ) -> List[Location]:
        """Finds all references to the identifier under the cursor."""
        word = doc.get_word_at_position(position)
        if not word:
            return []

        locations: List[Location] = []
        try:
            tokens = tokenize(doc.text, registry=self.registry, include_comments=False)
            for tok in tokens:
                if tok.type == TokenType.IDENTIFIER and tok.value == word:
                    locations.append(Location(uri=doc.uri, range=_token_range(tok)))
        except Exception:
            # If tokenize fails, fall back to regex on lines
            pattern = re.compile(rf"\b{re.escape(word)}\b")
            for line_idx, line in enumerate(doc.lines):
                for match in pattern.finditer(line):
                    locations.append(
                        Location(
                            uri=doc.uri,
                            range=Range(
                                start=Position(line=line_idx, character=match.start()),
                                end=Position(line=line_idx, character=match.end()),
                            ),
                        )
                    )

        return locations

    def rename_symbol(
        self, doc: Document, position: Position, new_name: str
    ) -> Optional[WorkspaceEdit]:
        """Safely renames all occurrences of the symbol under the cursor."""
        # 1. Validate new name
        if not re.match(r"^[a-zA-Z_][a-zA-Z0-9_]*$", new_name):
            return None
        if self.registry.is_keyword(new_name):
            return None

        # 2. Collect references
        references = self.get_references(doc, position, include_declaration=True)
        if not references:
            return None

        # 3. Formulate text edits
        edits = [TextEdit(range=loc.range, new_text=new_name) for loc in references]
        return WorkspaceEdit(changes={doc.uri: edits})

    # -------------------------------------------------------------------------
    # Helpers
    # -------------------------------------------------------------------------

    def _safe_parse(self, text: str) -> Optional[Program]:
        """Attempts to parse text without throwing exceptions."""
        try:
            tokens = tokenize(text, registry=self.registry, include_comments=False)
            return parse(tokens, registry=self.registry)
        except Exception:
            return None

    def _find_enclosing_function(
        self, ast: Program, position: Position
    ) -> Optional[FunctionDefinition]:
        """Finds the function definition enclosing the specified position."""
        for node in walk_ast(ast):
            if isinstance(node, FunctionDefinition):
                rng = _node_range(node)
                if (
                    rng.start.line <= position.line <= rng.end.line
                ):
                    return node
        return None

    def _resolve_cross_file_symbol(self, doc: Document, word: str) -> Optional[Location]:
        """Resolves definitions located in sibling .hin files or imported modules."""
        if not doc.file_path:
            return None

        parent_dir = doc.file_path.parent
        if not parent_dir.is_dir():
            return None

        # Check if the word directly names a sibling .hin file
        sibling_file = parent_dir / f"{word}.hin"
        if sibling_file.is_file():
            return Location(
                uri=sibling_file.as_uri(),
                range=Range(start=Position(0, 0), end=Position(0, 0)),
            )

        # Inspect import statements in current document
        ast = self._safe_parse(doc.text)
        candidate_files: List[Path] = []
        if ast:
            for node in walk_ast(ast):
                if isinstance(node, FromImport):
                    mod_file = parent_dir / f"{node.module}.hin"
                    if mod_file.is_file() and any(
                        (name == word or alias == word) for name, alias in node.names
                    ):
                        candidate_files.append(mod_file)
                elif isinstance(node, Import):
                    for mod_name, alias in node.names:
                        mod_file = parent_dir / f"{mod_name}.hin"
                        if mod_file.is_file():
                            candidate_files.append(mod_file)

        # Also search other sibling .hin files
        for f in parent_dir.glob("*.hin"):
            if f != doc.file_path and f not in candidate_files:
                candidate_files.append(f)

        for f in candidate_files:
            try:
                content = f.read_text(encoding="utf-8")
                f_lines = content.splitlines()
                f_ast = self._safe_parse(content)
                if f_ast:
                    for node in walk_ast(f_ast):
                        if (
                            isinstance(node, FunctionDefinition)
                            and node.name == word
                        ):
                            line_idx = _to_lsp_pos(node.start_pos).line
                            line_str = f_lines[line_idx] if line_idx < len(f_lines) else None
                            return Location(
                                uri=f.as_uri(),
                                range=_name_range(node.name, node, line_str),
                            )
                        elif (
                            isinstance(node, ClassDefinition)
                            and node.name == word
                        ):
                            line_idx = _to_lsp_pos(node.start_pos).line
                            line_str = f_lines[line_idx] if line_idx < len(f_lines) else None
                            return Location(
                                uri=f.as_uri(),
                                range=_name_range(node.name, node, line_str),
                            )
                        elif (
                            isinstance(node, Assignment)
                            and isinstance(node.target, Identifier)
                            and node.target.name == word
                        ):
                            return Location(
                                uri=f.as_uri(),
                                range=_node_range(node.target, len(word)),
                            )
            except Exception:
                continue

        return None


def _name_range(name: str, node: ASTNode, line_content: Optional[str] = None) -> Range:
    """Helper to compute Range for a node's identifier name."""
    start = _to_lsp_pos(node.start_pos)
    if line_content:
        match = re.search(r"\b" + re.escape(name) + r"\b", line_content)
        if match:
            return Range(
                start=Position(line=start.line, character=match.start()),
                end=Position(line=start.line, character=match.end()),
            )
    return Range(
        start=start,
        end=Position(line=start.line, character=start.character + len(name)),
    )
