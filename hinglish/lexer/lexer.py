"""Production-grade Lexer implementation for the Hinglish programming language.

Provides deterministic tokenization, robust Python-compliant indentation tracking
(with INDENT, DEDENT, NEWLINE emission), implicit line continuation within
parentheses/brackets/braces, explicit line continuation with backslashes,
rich numeric, string literal, and Unicode identifier support, and configurable keyword recognition.
"""

from typing import List, Optional

from ..exceptions import HinglishIndentationError, HinglishLexerError
from ..keywords import DEFAULT_KEYWORD_REGISTRY, KeywordRegistry
from .tokens import Position, Token, TokenType


def is_ident_start(ch: str) -> bool:
    """Checks if a character is valid as the first character of an identifier (Unicode-aware)."""
    return (ch == "_") or (ch.isidentifier() and not ch.isdigit())


def is_ident_part(ch: str) -> bool:
    """Checks if a character is valid as a subsequent character in an identifier (Unicode-aware)."""
    return ("a" + ch).isidentifier()


class HinglishLexer:
    """Deterministic lexical scanner for Hinglish source code."""

    # Multi-character operator mappings (ordered by decreasing length)
    MULTI_CHAR_OPS = [
        # 3 characters
        ("**=", TokenType.STAR_STAR_ASSIGN),
        ("//=", TokenType.DOUBLE_SLASH_ASSIGN),
        ("<<=", TokenType.LSHIFT_ASSIGN),
        (">>=", TokenType.RSHIFT_ASSIGN),
        ("...", TokenType.ELLIPSIS),
        # 2 characters
        ("+=", TokenType.PLUS_ASSIGN),
        ("-=", TokenType.MINUS_ASSIGN),
        ("*=", TokenType.STAR_ASSIGN),
        ("/=", TokenType.SLASH_ASSIGN),
        ("%=", TokenType.PERCENT_ASSIGN),
        ("&=", TokenType.AMPERSAND_ASSIGN),
        ("|=", TokenType.PIPE_ASSIGN),
        ("^=", TokenType.CARET_ASSIGN),
        ("@=", TokenType.AT_ASSIGN),
        ("**", TokenType.STAR_STAR),
        ("//", TokenType.DOUBLE_SLASH),
        ("<<", TokenType.LSHIFT),
        (">>", TokenType.RSHIFT),
        ("==", TokenType.EQ),
        ("!=", TokenType.NE),
        ("<=", TokenType.LE),
        (">=", TokenType.GE),
        (":=", TokenType.WALRUS),
        ("->", TokenType.ARROW),
    ]

    SINGLE_CHAR_OPS = {
        "+": TokenType.PLUS,
        "-": TokenType.MINUS,
        "*": TokenType.STAR,
        "/": TokenType.SLASH,
        "%": TokenType.PERCENT,
        "&": TokenType.AMPERSAND,
        "|": TokenType.PIPE,
        "^": TokenType.CARET,
        "~": TokenType.TILDE,
        "<": TokenType.LT,
        ">": TokenType.GT,
        "=": TokenType.ASSIGN,
        ":": TokenType.COLON,
        ",": TokenType.COMMA,
        ";": TokenType.SEMICOLON,
        ".": TokenType.DOT,
        "(": TokenType.LPAREN,
        ")": TokenType.RPAREN,
        "[": TokenType.LBRACKET,
        "]": TokenType.RBRACKET,
        "{": TokenType.LBRACE,
        "}": TokenType.RBRACE,
    }

    def __init__(
        self,
        registry: Optional[KeywordRegistry] = None,
        include_comments: bool = False,
    ) -> None:
        self.registry = registry or DEFAULT_KEYWORD_REGISTRY
        self.include_comments = include_comments

    def tokenize(self, source_code: str) -> List[Token]:
        """Tokenizes the given Hinglish source code into a list of Tokens."""
        self._source = source_code
        self._length = len(source_code)
        self._cursor = 0
        self._line = 1
        self._col = 1

        self._indent_stack: List[int] = [0]
        self._nesting_level = 0
        self._at_line_start = True

        self._tokens: List[Token] = []

        while self._cursor < self._length:
            # 1. Line start & Indentation handling
            if self._at_line_start:
                if not self._handle_line_start():
                    # Line was empty, comment-only, or had an explicit newline
                    continue

            ch = self._source[self._cursor]

            # 2. Skip horizontal whitespace inside a line
            if ch in (" ", "\t", "\f"):
                self._advance()
                continue

            # 3. Explicit line continuation (\ followed by newline)
            if ch == "\\" and self._cursor + 1 < self._length and self._source[self._cursor + 1] in ("\r", "\n"):
                self._advance()  # Skip '\'
                if self._cursor < self._length and self._source[self._cursor] == "\r":
                    self._advance()
                if self._cursor < self._length and self._source[self._cursor] == "\n":
                    self._advance()
                self._line += 1
                self._col = 1
                continue

            # 4. Newline handling
            if ch in ("\r", "\n"):
                start_pos = Position(self._line, self._col)
                if ch == "\r" and self._cursor + 1 < self._length and self._source[self._cursor + 1] == "\n":
                    self._advance()
                self._advance()
                end_pos = Position(self._line, self._col)

                self._line += 1
                self._col = 1

                if self._nesting_level > 0:
                    # Inside brackets/parens, newlines are ignored
                    continue

                # Avoid emitting consecutive NEWLINE tokens
                if self._tokens and self._tokens[-1].type not in (
                    TokenType.NEWLINE,
                    TokenType.INDENT,
                ):
                    self._tokens.append(
                        Token(TokenType.NEWLINE, "\n", start_pos, end_pos, "\n")
                    )
                self._at_line_start = True
                continue

            # 5. Comments
            if ch == "#":
                start_pos = Position(self._line, self._col)
                comment_start = self._cursor
                while self._cursor < self._length and self._source[self._cursor] not in ("\r", "\n"):
                    self._advance()
                comment_text = self._source[comment_start:self._cursor]
                if self.include_comments:
                    self._tokens.append(
                        Token(
                            TokenType.COMMENT,
                            comment_text,
                            start_pos,
                            Position(self._line, self._col),
                            comment_text,
                        )
                    )
                continue

            # 6. Check for invalid repeated '@' (e.g. naam = @@@)
            if ch == "@":
                p1 = self._peek(1)
                if p1 == "@":
                    # Repeated '@' is an invalid token sequence
                    current_line_text = self._get_current_line_text()
                    raise HinglishLexerError(
                        "Unexpected character '@'",
                        line=self._line,
                        column=self._col,
                        source_line=current_line_text,
                    )
                # Single @ or @=
                if p1 == "=":
                    start_pos = Position(self._line, self._col)
                    self._advance()
                    self._advance()
                    end_pos = Position(self._line, self._col)
                    self._tokens.append(
                        Token(TokenType.AT_ASSIGN, "@=", start_pos, end_pos, "@=")
                    )
                    continue
                # Single @ (decorator or matrix op)
                start_pos = Position(self._line, self._col)
                self._advance()
                end_pos = Position(self._line, self._col)
                self._tokens.append(
                    Token(TokenType.AT, "@", start_pos, end_pos, "@")
                )
                continue

            # 7. String Literals (including prefixes: r, f, b, etc.)
            if self._is_string_start():
                self._scan_string()
                continue

            # 8. Numeric Literals (decimal, hex, octal, binary, float, complex)
            if ch.isdigit() or (ch == "." and self._cursor + 1 < self._length and self._source[self._cursor + 1].isdigit()):
                self._scan_number()
                continue

            # 9. Multi-character Operators
            matched_op = False
            for op_str, token_type in self.MULTI_CHAR_OPS:
                if self._source.startswith(op_str, self._cursor):
                    start_pos = Position(self._line, self._col)
                    for _ in range(len(op_str)):
                        self._advance()
                    end_pos = Position(self._line, self._col)
                    self._tokens.append(
                        Token(token_type, op_str, start_pos, end_pos, op_str)
                    )
                    matched_op = True
                    break
            if matched_op:
                continue

            # 10. Single-character Operators & Delimiters
            if ch in self.SINGLE_CHAR_OPS:
                token_type = self.SINGLE_CHAR_OPS[ch]
                start_pos = Position(self._line, self._col)
                self._advance()
                end_pos = Position(self._line, self._col)

                # Track bracket nesting depth
                if token_type in (TokenType.LPAREN, TokenType.LBRACKET, TokenType.LBRACE):
                    self._nesting_level += 1
                elif token_type in (TokenType.RPAREN, TokenType.RBRACKET, TokenType.RBRACE):
                    self._nesting_level = max(0, self._nesting_level - 1)

                self._tokens.append(Token(token_type, ch, start_pos, end_pos, ch))
                continue

            # 11. Identifiers & Keywords (Supports Unicode / Devanagari)
            if is_ident_start(ch):
                self._scan_identifier_or_keyword()
                continue

            # Unrecognized character error (e.g. $, ?, `, etc.)
            current_line_text = self._get_current_line_text()
            raise HinglishLexerError(
                f"Unexpected character '{ch}'",
                line=self._line,
                column=self._col,
                source_line=current_line_text,
            )

        # 12. End-of-File processing
        self._finalize_tokens()
        return self._tokens

    def _advance(self) -> str:
        """Advance the cursor by one character."""
        ch = self._source[self._cursor]
        self._cursor += 1
        self._col += 1
        return ch

    def _peek(self, offset: int = 0) -> Optional[str]:
        """Look ahead by offset characters without advancing cursor."""
        pos = self._cursor + offset
        if pos < self._length:
            return self._source[pos]
        return None

    def _get_current_line_text(self) -> str:
        """Retrieves the full line of text containing the current cursor."""
        line_start = self._source.rfind("\n", 0, self._cursor)
        if line_start == -1:
            line_start = 0
        else:
            line_start += 1
        line_end = self._source.find("\n", self._cursor)
        if line_end == -1:
            line_end = self._length
        return self._source[line_start:line_end]

    def _handle_line_start(self) -> bool:
        """Processes leading whitespace, calculates indentation, and emits INDENT/DEDENT."""
        start_col = self._col
        indent_chars = 0
        indent_str = []

        while self._cursor < self._length:
            ch = self._source[self._cursor]
            if ch == " ":
                indent_chars += 1
                indent_str.append(" ")
                self._advance()
            elif ch == "\t":
                indent_chars += 8
                indent_str.append("\t")
                self._advance()
            else:
                break

        # Check if line is empty or comment-only
        if self._cursor >= self._length:
            return False

        next_ch = self._source[self._cursor]

        if next_ch in ("\r", "\n"):
            # Empty line, ignore indentation
            if next_ch == "\r" and self._peek(1) == "\n":
                self._advance()
            self._advance()
            self._line += 1
            self._col = 1
            return False

        if next_ch == "#":
            # Comment-only line, do not emit INDENT/DEDENT
            return True

        if self._nesting_level > 0:
            # Inside brackets, indentation is ignored
            self._at_line_start = False
            return True

        # Validate consistent indentation mixing
        if " " in indent_str and "\t" in indent_str:
            raise HinglishIndentationError(
                "Inconsistent use of tabs and spaces in indentation",
                line=self._line,
                column=start_col,
                source_line=self._get_current_line_text(),
            )

        current_level = indent_chars
        last_level = self._indent_stack[-1]

        if current_level > last_level:
            self._indent_stack.append(current_level)
            self._tokens.append(
                Token(
                    TokenType.INDENT,
                    current_level,
                    Position(self._line, 1),
                    Position(self._line, self._col),
                    "".join(indent_str),
                )
            )
        elif current_level < last_level:
            while self._indent_stack and self._indent_stack[-1] > current_level:
                popped = self._indent_stack.pop()
                self._tokens.append(
                    Token(
                        TokenType.DEDENT,
                        popped,
                        Position(self._line, 1),
                        Position(self._line, self._col),
                        "",
                    )
                )

            if not self._indent_stack or self._indent_stack[-1] != current_level:
                raise HinglishIndentationError(
                    f"Unindent does not match any outer indentation level (level {current_level})",
                    line=self._line,
                    column=1,
                    source_line=self._get_current_line_text(),
                )

        self._at_line_start = False
        return True

    def _is_string_start(self) -> bool:
        """Determines if the cursor is at the beginning of a string literal."""
        ch = self._source[self._cursor]
        if ch in ("'", '"'):
            return True

        # Check for string prefixes: r, u, b, f, rf, fr, rb, br
        if ch.lower() in ("r", "u", "b", "f"):
            p1 = self._peek(1)
            if p1 in ("'", '"'):
                return True
            if p1 and p1.lower() in ("r", "b"):
                p2 = self._peek(2)
                if p2 in ("'", '"'):
                    return True
        return False

    def _scan_string(self) -> None:
        """Scans single, double, or triple-quoted string literals with optional prefixes."""
        start_line = self._line
        start_col = self._col
        start_pos = Position(start_line, start_col)
        start_idx = self._cursor

        # 1. Scan prefix (if any)
        prefix = ""
        while self._cursor < self._length and self._source[self._cursor].lower() in ("r", "u", "b", "f"):
            prefix += self._advance()

        quote_char = self._advance()
        is_triple = False

        if (
            self._cursor + 1 < self._length
            and self._source[self._cursor] == quote_char
            and self._source[self._cursor + 1] == quote_char
        ):
            is_triple = True
            self._advance()
            self._advance()
            quote_str = quote_char * 3
        else:
            quote_str = quote_char

        chars = []
        is_raw = "r" in prefix.lower()

        while self._cursor < self._length:
            if is_triple:
                if self._source.startswith(quote_str, self._cursor):
                    for _ in range(3):
                        self._advance()
                    break
            else:
                if self._source[self._cursor] == quote_char:
                    self._advance()
                    break
                if self._source[self._cursor] in ("\r", "\n"):
                    raise HinglishLexerError(
                        "EOL while scanning single-line string literal",
                        line=start_line,
                        column=start_col,
                        source_line=self._get_current_line_text(),
                    )

            ch = self._source[self._cursor]

            if ch == "\\" and not is_raw and self._cursor + 1 < self._length:
                self._advance()
                esc = self._source[self._cursor]
                self._advance()
                if esc == "n":
                    chars.append("\n")
                elif esc == "t":
                    chars.append("\t")
                elif esc == "r":
                    chars.append("\r")
                elif esc == "\\":
                    chars.append("\\")
                elif esc == "'":
                    chars.append("'")
                elif esc == '"':
                    chars.append('"')
                elif esc in ("\r", "\n"):
                    if esc == "\r" and self._cursor < self._length and self._source[self._cursor] == "\n":
                        self._advance()
                    self._line += 1
                    self._col = 1
                else:
                    chars.append("\\" + esc)
                continue

            if ch in ("\r", "\n"):
                if ch == "\r" and self._cursor + 1 < self._length and self._source[self._cursor + 1] == "\n":
                    self._advance()
                self._advance()
                chars.append("\n")
                self._line += 1
                self._col = 1
                continue

            chars.append(self._advance())
        else:
            raise HinglishLexerError(
                f"Unterminated string literal starting at {start_pos}",
                line=start_line,
                column=start_col,
                source_line=self._get_current_line_text(),
            )

        end_pos = Position(self._line, self._col)
        raw_text = self._source[start_idx:self._cursor]
        val = "".join(chars)
        self._tokens.append(
            Token(TokenType.STRING, val, start_pos, end_pos, raw_text)
        )

    def _scan_number(self) -> None:
        """Scans numeric literals: integers, floats, complex, hex, binary, octal."""
        start_pos = Position(self._line, self._col)
        start_idx = self._cursor

        # Hex, Octal, Binary
        if self._source[self._cursor] == "0" and self._cursor + 1 < self._length:
            base_char = self._source[self._cursor + 1].lower()
            if base_char in ("x", "o", "b"):
                self._advance()  # '0'
                self._advance()  # 'x', 'o', 'b'
                valid_chars = {
                    "x": "0123456789abcdefABCDEF_",
                    "o": "01234567_",
                    "b": "01_",
                }[base_char]

                digits = []
                while self._cursor < self._length and self._source[self._cursor] in valid_chars:
                    digits.append(self._advance())

                if not digits or digits == ["_"]:
                    raise HinglishLexerError(
                        f"Invalid numeric literal with base '{base_char}'",
                        line=self._line,
                        column=start_pos.column,
                        source_line=self._get_current_line_text(),
                    )

                raw_text = self._source[start_idx:self._cursor]
                clean = raw_text.replace("_", "")
                base = {"x": 16, "o": 8, "b": 2}[base_char]
                val = int(clean, base)
                self._tokens.append(
                    Token(
                        TokenType.INTEGER,
                        val,
                        start_pos,
                        Position(self._line, self._col),
                        raw_text,
                    )
                )
                return

        # Decimal, Float, or Complex
        is_float = False
        is_complex = False

        while self._cursor < self._length and (self._source[self._cursor].isdigit() or self._source[self._cursor] == "_"):
            self._advance()

        # Check for fractional part
        if self._cursor < self._length and self._source[self._cursor] == ".":
            # Avoid confusing dot operator or ellipsis with float
            if self._peek(1) != ".":
                is_float = True
                self._advance()  # '.'
                while self._cursor < self._length and (self._source[self._cursor].isdigit() or self._source[self._cursor] == "_"):
                    self._advance()

        # Check for exponent
        if self._cursor < self._length and self._source[self._cursor].lower() == "e":
            is_float = True
            self._advance()  # 'e'
            if self._cursor < self._length and self._source[self._cursor] in ("+", "-"):
                self._advance()
            while self._cursor < self._length and (self._source[self._cursor].isdigit() or self._source[self._cursor] == "_"):
                self._advance()

        # Check for imaginary unit 'j'
        if self._cursor < self._length and self._source[self._cursor].lower() == "j":
            is_complex = True
            self._advance()

        raw_text = self._source[start_idx:self._cursor]
        clean = raw_text.replace("_", "")

        try:
            if is_complex:
                val = complex(clean)
                token_type = TokenType.COMPLEX
            elif is_float:
                val = float(clean)
                token_type = TokenType.FLOAT
            else:
                val = int(clean)
                token_type = TokenType.INTEGER
        except ValueError as exc:
            raise HinglishLexerError(
                f"Invalid number literal '{raw_text}': {exc}",
                line=start_pos.line,
                column=start_pos.column,
                source_line=self._get_current_line_text(),
            )

        self._tokens.append(
            Token(
                token_type,
                val,
                start_pos,
                Position(self._line, self._col),
                raw_text,
            )
        )

    def _scan_identifier_or_keyword(self) -> None:
        """Scans words (supporting Unicode/Devanagari) and resolves keywords, literals, or identifiers."""
        start_pos = Position(self._line, self._col)
        start_idx = self._cursor

        while self._cursor < self._length and is_ident_part(self._source[self._cursor]):
            self._advance()

        word = self._source[start_idx:self._cursor]
        end_pos = Position(self._line, self._col)

        # 1. Check if word is a literal keyword (sahi, galat, kuch_nahi)
        if self.registry.is_literal_keyword(word):
            py_lit = self.registry.get_python_equivalent(word)
            if py_lit == "True":
                self._tokens.append(Token(TokenType.BOOLEAN, True, start_pos, end_pos, word))
            elif py_lit == "False":
                self._tokens.append(Token(TokenType.BOOLEAN, False, start_pos, end_pos, word))
            elif py_lit == "None":
                self._tokens.append(Token(TokenType.NONE, None, start_pos, end_pos, word))
            return

        # 2. Check if word is a statement/operator/soft keyword
        if (
            self.registry.is_statement_keyword(word)
            or self.registry.is_operator_keyword(word)
            or self.registry.is_soft_keyword(word)
        ):
            self._tokens.append(Token(TokenType.KEYWORD, word, start_pos, end_pos, word))
            return

        # 3. Otherwise it is an IDENTIFIER
        self._tokens.append(Token(TokenType.IDENTIFIER, word, start_pos, end_pos, word))

    def _finalize_tokens(self) -> None:
        """Handles trailing NEWLINE, flushes any remaining indentation DEDENTs, and adds EOF."""
        end_pos = Position(self._line, self._col)

        # Ensure source ends with a NEWLINE token if not already empty or ending in newline
        if self._tokens:
            last_type = self._tokens[-1].type
            if last_type not in (TokenType.NEWLINE, TokenType.INDENT, TokenType.DEDENT):
                self._tokens.append(Token(TokenType.NEWLINE, "\n", end_pos, end_pos, "\n"))

        # Flush all remaining indentations
        while len(self._indent_stack) > 1:
            popped = self._indent_stack.pop()
            self._tokens.append(Token(TokenType.DEDENT, popped, end_pos, end_pos, ""))

        # Emit EOF
        self._tokens.append(Token(TokenType.EOF, None, end_pos, end_pos, ""))
