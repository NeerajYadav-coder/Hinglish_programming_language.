"""Deterministic Recursive-Descent Parser for Hinglish.

Consumes a token stream from HinglishLexer and produces a strongly-typed
Hinglish Abstract Syntax Tree (AST).
"""

from typing import Any, Dict, List, Optional, Tuple

from ..ast.nodes import (
    AnnAssign,
    Assignment,
    AssignmentExpression,
    ASTNode,
    AsyncFor,
    AsyncFunctionDefinition,
    AsyncWith,
    AttributeAccess,
    Await,
    BinaryOperation,
    Boolean,
    BooleanOperation,
    Break,
    ClassDefinition,
    Comparison,
    Complex,
    ComprehensionClause,
    Continue,
    DictComprehension,
    DictLiteral,
    DoubleStarred,
    ElifClause,
    ExceptHandler,
    Expression,
    ExpressionStatement,
    Float,
    For,
    FormattedValue,
    FromImport,
    FunctionCall,
    FunctionDefinition,
    GeneratorExpression,
    Identifier,
    If,
    Import,
    Indexing,
    Integer,
    JoinedStr,
    LambdaExpression,
    ListComprehension,
    ListLiteral,
    Match,
    MatchAs,
    MatchCase,
    MatchClass,
    MatchMapping,
    MatchOr,
    MatchPattern,
    MatchSequence,
    MatchSingleton,
    MatchStar,
    MatchValue,
    NoneLiteral,
    Parameter,
    Pass,
    Program,
    Raise,
    Return,
    SetComprehension,
    SetLiteral,
    Slice,
    Starred,
    Statement,
    String,
    Try,
    TupleLiteral,
    UnaryOperation,
    While,
    With,
    WithItem,
    Yield,
    YieldFrom,
)
from ..exceptions import HinglishSyntaxError
from ..keywords import DEFAULT_KEYWORD_REGISTRY, KeywordRegistry
from ..lexer.tokens import Position, Token, TokenType


class HinglishParser:
    """Hand-written recursive-descent parser for Hinglish programs."""

    def __init__(
        self,
        tokens: List[Token],
        registry: Optional[KeywordRegistry] = None,
        source_code: Optional[str] = None,
    ) -> None:
        self.tokens = tokens
        self.registry = registry or DEFAULT_KEYWORD_REGISTRY
        self.source_code = source_code
        self.cursor = 0
        self.length = len(tokens)

    # -------------------------------------------------------------------------
    # Helper & Navigation Methods
    # -------------------------------------------------------------------------

    def is_at_end(self) -> bool:
        """Returns True if the parser has reached EOF."""
        if self.cursor >= self.length:
            return True
        return self.tokens[self.cursor].type == TokenType.EOF

    def peek(self, offset: int = 0) -> Token:
        """Returns the token at cursor + offset without consuming it."""
        pos = self.cursor + offset
        if pos < self.length:
            return self.tokens[pos]
        return self.tokens[-1]  # Return last token (usually EOF)

    def advance(self) -> Token:
        """Consumes and returns the current token."""
        tok = self.peek()
        if not self.is_at_end():
            self.cursor += 1
        return tok

    def check(self, token_type: TokenType) -> bool:
        """Checks if current token matches the given token type."""
        if self.is_at_end():
            return False
        return self.peek().type == token_type

    def match(self, *token_types: TokenType) -> Optional[Token]:
        """Consumes current token if its type matches any of token_types."""
        if self.is_at_end():
            return None
        if self.peek().type in token_types:
            return self.advance()
        return None

    def get_py_keyword(self, tok: Token) -> Optional[str]:
        """Returns target Python keyword if token is a KEYWORD or IDENTIFIER matching registry."""
        if tok.type == TokenType.KEYWORD:
            return self.registry.get_python_equivalent(str(tok.value))
        if tok.type == TokenType.IDENTIFIER:
            if self.registry.is_statement_keyword(str(tok.value)) or self.registry.is_operator_keyword(str(tok.value)):
                return self.registry.get_python_equivalent(str(tok.value))
        return None

    def check_py_keyword(self, *py_keywords: str) -> bool:
        """Checks if current token maps to any of the target Python keywords."""
        if self.is_at_end():
            return False
        py_kw = self.get_py_keyword(self.peek())
        return py_kw in py_keywords

    def match_py_keyword(self, *py_keywords: str) -> Optional[Token]:
        """Consumes current token if it maps to any of the target Python keywords."""
        if self.check_py_keyword(*py_keywords):
            return self.advance()
        return None

    def expect(self, token_type: TokenType, message: str) -> Token:
        """Asserts current token matches token_type, otherwise raises HinglishSyntaxError."""
        if self.check(token_type):
            return self.advance()
        current = self.peek()
        raise self._syntax_error(message, current)

    def skip_newlines(self) -> None:
        """Consumes any consecutive NEWLINE tokens."""
        while not self.is_at_end() and self.check(TokenType.NEWLINE):
            self.advance()

    def _syntax_error(self, message: str, token: Token) -> HinglishSyntaxError:
        """Constructs a HinglishSyntaxError with line, column, and source snippet."""
        source_line = None
        if self.source_code and token.start_pos:
            lines = self.source_code.splitlines()
            if 0 <= token.start_pos.line - 1 < len(lines):
                source_line = lines[token.start_pos.line - 1]

        line = token.start_pos.line if token.start_pos else None
        col = token.start_pos.column if token.start_pos else None
        return HinglishSyntaxError(
            message,
            line=line,
            column=col,
            source_line=source_line,
        )

    # -------------------------------------------------------------------------
    # Program & Statement Parsing
    # -------------------------------------------------------------------------

    def parse(self) -> Program:
        """Parses the entire token stream into a Program AST node."""
        statements: List[Statement] = []
        start_pos = self.peek().start_pos

        self.skip_newlines()
        while not self.is_at_end():
            stmt = self.parse_statement()
            if stmt is not None:
                statements.append(stmt)
            self.skip_newlines()

        end_pos = self.peek().end_pos
        return Program(body=statements, start_pos=start_pos, end_pos=end_pos)

    def parse_statement(self) -> Statement:
        """Parses a single statement based on keyword or expression dispatch."""
        self.skip_newlines()
        tok = self.peek()
        py_kw = self.get_py_keyword(tok)

        if py_kw == "if":
            return self.parse_if()
        if py_kw == "while":
            return self.parse_while()
        if py_kw == "for":
            return self.parse_for()
        if py_kw == "def":
            return self.parse_function_definition()
        if py_kw == "return":
            return self.parse_return()
        if py_kw == "break":
            return self.parse_break()
        if py_kw == "continue":
            return self.parse_continue()
        if py_kw == "pass":
            return self.parse_pass()
        if py_kw == "import":
            return self.parse_import()
        if py_kw == "from":
            return self.parse_from_import()
        if py_kw == "class":
            return self.parse_class_definition()
        if py_kw == "try":
            return self.parse_try()
        if py_kw == "raise":
            return self.parse_raise()
        if py_kw == "with":
            return self.parse_with()
        if py_kw == "async":
            return self.parse_async_statement()
        if py_kw == "match":
            return self.parse_match()
        if tok.type == TokenType.AT:
            return self.parse_decorated_definition()
        if py_kw == "yield":
            return self.parse_yield_statement()

        # Expression or Assignment
        return self.parse_assignment_or_expression_statement()

    def parse_block(self, context_name: str = "statement") -> List[Statement]:
        """Parses a colon followed by an indented block of statements."""
        if not self.check(TokenType.COLON):
            tok = self.peek()
            raise self._syntax_error(f"Expected ':' after {context_name}", tok)
        self.advance()  # Consume ':'

        # Must have a NEWLINE followed by INDENT
        if not self.check(TokenType.NEWLINE):
            tok = self.peek()
            raise self._syntax_error(f"Expected newline after ':' in {context_name}", tok)
        self.advance()  # Consume NEWLINE

        self.skip_newlines()

        if not self.check(TokenType.INDENT):
            tok = self.peek()
            raise self._syntax_error(f"Expected an indented block after ':' in {context_name}", tok)
        self.advance()  # Consume INDENT

        body: List[Statement] = []
        self.skip_newlines()

        while not self.is_at_end() and not self.check(TokenType.DEDENT):
            stmt = self.parse_statement()
            if stmt is not None:
                body.append(stmt)
            self.skip_newlines()

        self.expect(TokenType.DEDENT, f"Expected dedent to close {context_name} block")
        return body

    def parse_if(self) -> If:
        """Parses an if statement with optional elif and else branches."""
        start_tok = self.advance()  # Consume 'agar'
        start_pos = start_tok.start_pos

        if self.check(TokenType.COLON):
            raise self._syntax_error("Expected condition expression after 'agar'", self.peek())

        condition = self.parse_expression()
        body = self.parse_block("agar")

        elif_clauses: List[ElifClause] = []
        else_body: Optional[List[Statement]] = None

        while not self.is_at_end():
            self.skip_newlines()
            if self.check_py_keyword("elif"):
                elif_tok = self.advance()  # Consume 'warna_agar'
                if self.check(TokenType.COLON):
                    raise self._syntax_error("Expected condition expression after 'warna_agar'", self.peek())
                elif_cond = self.parse_expression()
                elif_body = self.parse_block("warna_agar")
                elif_clauses.append(
                    ElifClause(
                        condition=elif_cond,
                        body=elif_body,
                        start_pos=elif_tok.start_pos,
                    )
                )
            else:
                break

        self.skip_newlines()
        if self.check_py_keyword("else"):
            self.advance()  # Consume 'warna'
            else_body = self.parse_block("warna")

        end_pos = (else_body[-1].end_pos if else_body else body[-1].end_pos) if body else start_pos
        return If(
            condition=condition,
            body=body,
            elif_clauses=elif_clauses,
            else_body=else_body,
            start_pos=start_pos,
            end_pos=end_pos,
        )

    def parse_while(self) -> While:
        """Parses a while loop: jabtak <cond>: <body>."""
        start_tok = self.advance()  # Consume 'jabtak'
        start_pos = start_tok.start_pos

        if self.check(TokenType.COLON):
            raise self._syntax_error("Expected condition expression after 'jabtak'", self.peek())

        condition = self.parse_expression()
        body = self.parse_block("jabtak")

        end_pos = body[-1].end_pos if body else start_pos
        return While(
            condition=condition,
            body=body,
            start_pos=start_pos,
            end_pos=end_pos,
        )

    def parse_for(self) -> For:
        """Parses a for loop: har [intezaar] <target> mein <iterable>: <body>."""
        start_tok = self.advance()  # Consume 'har'
        start_pos = start_tok.start_pos
        is_async = False

        if self.check_py_keyword("await"):
            self.advance()  # Consume 'intezaar'
            is_async = True

        if self.check(TokenType.COLON):
            raise self._syntax_error("Expected loop variable after 'har'", self.peek())

        target = self.parse_primary()

        # Expect 'mein' or 'andar' (Python target 'in')
        if not self.check_py_keyword("in"):
            tok = self.peek()
            raise self._syntax_error("Expected 'mein' or 'andar' in for loop", tok)
        self.advance()  # Consume 'mein' / 'andar'

        iterable = self.parse_expression()
        body = self.parse_block("har")

        end_pos = body[-1].end_pos if body else start_pos
        return For(
            target=target,
            iterable=iterable,
            body=body,
            is_async=is_async,
            start_pos=start_pos,
            end_pos=end_pos,
        )

    def parse_parameters(self) -> Tuple[List[str], List[Parameter]]:
        """Parses modern Python-compatible function parameter signatures.

        Supports positional-only ('/'), annotations (': type'), defaults ('= val'),
        var-positional ('*args'), bare ('*'), keyword-only, and var-keyword ('**kwargs').
        """
        params_str_list: List[str] = []
        parameters: List[Parameter] = []
        seen_slash = False
        seen_star = False
        seen_kwarg = False
        seen_default = False

        while not self.check(TokenType.RPAREN) and not self.is_at_end():
            # 1. Positional-only separator: '/'
            if self.match(TokenType.SLASH):
                if seen_slash:
                    raise self._syntax_error("'/' may only appear once in parameter list", self.peek())
                if seen_star:
                    raise self._syntax_error("'/' must be ahead of '*' in parameter list", self.peek())
                if not parameters:
                    raise self._syntax_error("'/' must follow at least one parameter", self.peek())
                seen_slash = True
                for p in parameters:
                    if p.kind == "POSITIONAL_OR_KEYWORD":
                        p.kind = "POSITIONAL_ONLY"

                self.match(TokenType.COMMA)
                continue

            # 2. Var-positional '*args' or bare '*'
            if self.match(TokenType.STAR):
                if seen_star:
                    raise self._syntax_error("Multiple '*' not allowed in parameter list", self.peek())
                seen_star = True

                # Bare '*'
                if self.check(TokenType.COMMA) or self.check(TokenType.RPAREN):
                    self.match(TokenType.COMMA)
                    continue

                arg_tok = self.expect(TokenType.IDENTIFIER, "Expected parameter name after '*'")
                arg_name = str(arg_tok.value)
                params_str_list.append(arg_name)

                annotation = None
                if self.match(TokenType.COLON):
                    annotation = self.parse_expression()

                parameters.append(
                    Parameter(
                        name=arg_name,
                        annotation=annotation,
                        kind="VAR_POSITIONAL",
                        start_pos=arg_tok.start_pos,
                        end_pos=annotation.end_pos if annotation else arg_tok.end_pos,
                    )
                )
                self.match(TokenType.COMMA)
                continue

            # 3. Var-keyword '**kwargs'
            if self.match(TokenType.STAR_STAR):
                if seen_kwarg:
                    raise self._syntax_error("Multiple '**' not allowed in parameter list", self.peek())
                seen_kwarg = True

                kw_tok = self.expect(TokenType.IDENTIFIER, "Expected parameter name after '**'")
                kw_name = str(kw_tok.value)
                params_str_list.append(kw_name)

                annotation = None
                if self.match(TokenType.COLON):
                    annotation = self.parse_expression()

                parameters.append(
                    Parameter(
                        name=kw_name,
                        annotation=annotation,
                        kind="VAR_KEYWORD",
                        start_pos=kw_tok.start_pos,
                        end_pos=annotation.end_pos if annotation else kw_tok.end_pos,
                    )
                )

                if self.match(TokenType.COMMA):
                    if not self.check(TokenType.RPAREN):
                        raise self._syntax_error("No parameters may follow '**kwargs'", self.peek())
                continue

            # 4. Standard parameter
            if seen_kwarg:
                raise self._syntax_error("No parameters may follow '**kwargs'", self.peek())

            name_tok = self.expect(TokenType.IDENTIFIER, "Expected parameter name")
            name = str(name_tok.value)
            params_str_list.append(name)

            annotation = None
            if self.match(TokenType.COLON):
                annotation = self.parse_expression()

            default = None
            if self.match(TokenType.ASSIGN):
                default = self.parse_expression()

            if default is not None:
                seen_default = True
            elif not seen_star and seen_default:
                raise self._syntax_error(
                    f"Non-default argument '{name}' follows default argument", name_tok
                )

            kind = "KEYWORD_ONLY" if seen_star else "POSITIONAL_OR_KEYWORD"
            parameters.append(
                Parameter(
                    name=name,
                    annotation=annotation,
                    default=default,
                    kind=kind,
                    start_pos=name_tok.start_pos,
                    end_pos=default.end_pos if default else (annotation.end_pos if annotation else name_tok.end_pos),
                )
            )

            if not self.match(TokenType.COMMA):
                break

        return params_str_list, parameters

    def parse_function_definition(self) -> FunctionDefinition:
        """Parses a function definition: kaam <name>(<params>) [-> <ret>]: <body>."""
        start_tok = self.advance()  # Consume 'kaam'
        start_pos = start_tok.start_pos

        name_tok = self.expect(TokenType.IDENTIFIER, "Expected function name after 'kaam'")
        self.expect(TokenType.LPAREN, "Expected '(' after function name")

        params, parameters = self.parse_parameters()
        self.expect(TokenType.RPAREN, "Expected ')' after parameter list")

        returns: Optional[Expression] = None
        if self.match(TokenType.ARROW):
            returns = self.parse_expression()

        body = self.parse_block(f"function '{name_tok.value}'")

        end_pos = body[-1].end_pos if body else start_pos
        return FunctionDefinition(
            name=str(name_tok.value),
            params=params,
            parameters=parameters,
            returns=returns,
            body=body,
            start_pos=start_pos,
            end_pos=end_pos,
        )

    def parse_return(self) -> Return:
        """Parses return statement: wapas [<value>]."""
        start_tok = self.advance()  # Consume 'wapas'
        start_pos = start_tok.start_pos

        val: Optional[Expression] = None
        if not self.is_at_end() and not self.check(TokenType.NEWLINE):
            val = self.parse_expression()

        self.expect_statement_terminator()
        end_pos = val.end_pos if val else start_tok.end_pos
        return Return(value=val, start_pos=start_pos, end_pos=end_pos)

    def parse_break(self) -> Break:
        """Parses break statement: ruko."""
        start_tok = self.advance()
        self.expect_statement_terminator()
        return Break(start_pos=start_tok.start_pos, end_pos=start_tok.end_pos)

    def parse_continue(self) -> Continue:
        """Parses continue statement: aage_bado."""
        start_tok = self.advance()
        self.expect_statement_terminator()
        return Continue(start_pos=start_tok.start_pos, end_pos=start_tok.end_pos)

    def parse_pass(self) -> Pass:
        """Parses pass statement: chhod_do."""
        start_tok = self.advance()
        self.expect_statement_terminator()
        return Pass(start_pos=start_tok.start_pos, end_pos=start_tok.end_pos)

    def parse_import(self) -> Import:
        """Parses import statement: laao <module> [jaise <alias>]."""
        start_tok = self.advance()
        start_pos = start_tok.start_pos

        module_tok = self.expect(TokenType.IDENTIFIER, "Expected module name after 'laao'")
        alias: Optional[str] = None
        if self.check_py_keyword("as"):
            self.advance()  # Consume 'jaise'
            alias_tok = self.expect(TokenType.IDENTIFIER, "Expected alias name after 'jaise'")
            alias = str(alias_tok.value)

        self.expect_statement_terminator()
        return Import(
            names=[(str(module_tok.value), alias)],
            start_pos=start_pos,
            end_pos=self.peek().end_pos,
        )

    def parse_from_import(self) -> FromImport:
        """Parses from-import statement: se <module> laao <name> [jaise <alias>]."""
        start_tok = self.advance()
        start_pos = start_tok.start_pos

        module_tok = self.expect(TokenType.IDENTIFIER, "Expected module name after 'se'")
        if not self.check_py_keyword("import"):
            raise self._syntax_error("Expected 'laao' after module name in from-import", self.peek())
        self.advance()  # Consume 'laao'

        name_tok = self.expect(TokenType.IDENTIFIER, "Expected imported name after 'laao'")
        alias: Optional[str] = None
        if self.check_py_keyword("as"):
            self.advance()  # Consume 'jaise'
            alias_tok = self.expect(TokenType.IDENTIFIER, "Expected alias name after 'jaise'")
            alias = str(alias_tok.value)

        self.expect_statement_terminator()
        return FromImport(
            module=str(module_tok.value),
            names=[(str(name_tok.value), alias)],
            start_pos=start_pos,
            end_pos=self.peek().end_pos,
        )

    def parse_class_definition(self) -> ClassDefinition:
        """Parses a class definition: varg <name>[(<bases>)]: <body>"""
        start_tok = self.advance()  # Consume 'varg' (or alias)
        start_pos = start_tok.start_pos

        name_tok = self.expect(TokenType.IDENTIFIER, "Expected class name after 'varg'")
        class_name = str(name_tok.value)

        bases: List[Expression] = []
        if self.match(TokenType.LPAREN):
            if not self.check(TokenType.RPAREN):
                bases.append(self.parse_expression())
                while self.match(TokenType.COMMA):
                    if self.check(TokenType.RPAREN):
                        break
                    bases.append(self.parse_expression())
            self.expect(TokenType.RPAREN, "Expected ')' after base classes")

        body = self.parse_block("varg")
        end_pos = body[-1].end_pos if body else name_tok.end_pos
        return ClassDefinition(
            name=class_name,
            bases=bases,
            body=body,
            start_pos=start_pos,
            end_pos=end_pos,
        )

    def parse_try(self) -> Try:
        """Parses a try statement: koshish: <body> [pakdo ...]* [warna: ...] [antatah: ...]"""
        start_tok = self.advance()  # Consume 'koshish'
        start_pos = start_tok.start_pos

        body = self.parse_block("koshish")

        handlers: List[ExceptHandler] = []
        self.skip_newlines()
        while not self.is_at_end() and self.check_py_keyword("except"):
            handler_tok = self.advance()  # Consume 'pakdo'
            h_start_pos = handler_tok.start_pos

            exc_type: Optional[Expression] = None
            exc_name: Optional[str] = None

            if not self.check(TokenType.COLON):
                exc_type = self.parse_expression()
                if self.check_py_keyword("as"):
                    self.advance()  # Consume 'jaise'
                    name_tok = self.expect(TokenType.IDENTIFIER, "Expected identifier after 'jaise'")
                    exc_name = str(name_tok.value)

            handler_body = self.parse_block("pakdo")
            h_end_pos = handler_body[-1].end_pos if handler_body else h_start_pos
            handlers.append(
                ExceptHandler(
                    type=exc_type,
                    name=exc_name,
                    body=handler_body,
                    start_pos=h_start_pos,
                    end_pos=h_end_pos,
                )
            )
            self.skip_newlines()

        else_body: Optional[List[Statement]] = None
        self.skip_newlines()
        if not self.is_at_end() and self.check_py_keyword("else"):
            self.advance()  # Consume 'warna'
            else_body = self.parse_block("warna")
            self.skip_newlines()

        finally_body: Optional[List[Statement]] = None
        self.skip_newlines()
        if not self.is_at_end() and self.check_py_keyword("finally"):
            self.advance()  # Consume 'antatah'
            finally_body = self.parse_block("antatah")

        if not handlers and finally_body is None:
            raise self._syntax_error("Expected 'pakdo' or 'antatah' after 'koshish' block", start_tok)

        end_pos = (
            finally_body[-1].end_pos
            if finally_body
            else (
                else_body[-1].end_pos
                if else_body
                else (handlers[-1].end_pos if handlers else body[-1].end_pos if body else start_pos)
            )
        )

        return Try(
            body=body,
            handlers=handlers,
            else_body=else_body,
            finally_body=finally_body,
            start_pos=start_pos,
            end_pos=end_pos,
        )

    def parse_raise(self) -> Raise:
        """Parses a raise statement: uthav [<exc>]"""
        start_tok = self.advance()  # Consume 'uthav'
        start_pos = start_tok.start_pos

        exc: Optional[Expression] = None
        if not self.is_at_end() and self.peek().type not in (TokenType.NEWLINE, TokenType.EOF, TokenType.SEMICOLON, TokenType.DEDENT):
            exc = self.parse_expression()

        self.expect_statement_terminator()
        end_pos = exc.end_pos if exc and exc.end_pos else start_pos
        return Raise(exc=exc, start_pos=start_pos, end_pos=end_pos)

    def parse_with(self) -> With:
        """Parses a context manager statement: saath [intezaar] <item1>, <item2>: <body>"""
        start_tok = self.advance()  # Consume 'saath'
        start_pos = start_tok.start_pos
        is_async = False

        if self.check_py_keyword("await"):
            self.advance()  # Consume 'intezaar'
            is_async = True

        items: List[WithItem] = []
        while True:
            item_start = self.peek().start_pos
            context_expr = self.parse_expression()
            optional_vars: Optional[Expression] = None

            if self.check_py_keyword("as"):
                self.advance()  # Consume 'jaise'
                optional_vars = self.parse_primary()

            item_end = optional_vars.end_pos if optional_vars and optional_vars.end_pos else context_expr.end_pos
            items.append(
                WithItem(
                    context_expr=context_expr,
                    optional_vars=optional_vars,
                    start_pos=item_start,
                    end_pos=item_end,
                )
            )

            if not self.match(TokenType.COMMA):
                break

        body = self.parse_block("saath")
        end_pos = body[-1].end_pos if body else start_pos
        return With(items=items, body=body, is_async=is_async, start_pos=start_pos, end_pos=end_pos)

    def parse_async_statement(self) -> Statement:
        """Parses an async definition: asamanantar kaam <name>(<params>): <body>."""
        start_tok = self.advance()  # Consume 'asamanantar'
        start_pos = start_tok.start_pos

        if not self.check_py_keyword("def"):
            tok = self.peek()
            raise self._syntax_error("Expected 'kaam' after 'asamanantar'", tok)

        func = self.parse_function_definition()
        func.is_async = True
        func.start_pos = start_pos
        return func

    def parse_decorated_definition(self) -> Statement:
        """Parses @decorator lines followed by a function or class definition."""
        decorators: List[Expression] = []
        start_pos = self.peek().start_pos

        while not self.is_at_end() and self.check(TokenType.AT):
            self.advance()  # Consume '@'
            dec_expr = self.parse_call_subscript_attribute()
            self.skip_newlines()
            decorators.append(dec_expr)

        self.skip_newlines()
        next_tok = self.peek()
        py_kw = self.get_py_keyword(next_tok)

        if py_kw == "def":
            func = self.parse_function_definition()
            func.decorators = decorators
            func.start_pos = start_pos
            return func

        if py_kw == "async":
            func = self.parse_async_statement()
            if isinstance(func, FunctionDefinition):
                func.decorators = decorators
                func.start_pos = start_pos
            return func

        if py_kw == "class":
            cls = self.parse_class_definition()
            cls.decorators = decorators
            cls.start_pos = start_pos
            return cls

        raise self._syntax_error("Expected function ('kaam') or class ('varg') definition after decorator", next_tok)

    def parse_yield_statement(self) -> ExpressionStatement:
        """Parses a yield statement: upaj [<value>] or upaj se <value>."""
        start_tok = self.advance()  # Consume 'upaj'
        start_pos = start_tok.start_pos

        if self.check_py_keyword("from"):
            self.advance()  # Consume 'se'
            val = self.parse_expression()
            self.expect_statement_terminator()
            node = YieldFrom(value=val, start_pos=start_pos, end_pos=val.end_pos)
            return ExpressionStatement(expr=node, start_pos=start_pos, end_pos=node.end_pos)

        val = None
        if not self.is_at_end() and self.peek().type not in (
            TokenType.NEWLINE, TokenType.EOF, TokenType.SEMICOLON, TokenType.DEDENT
        ):
            val = self.parse_expression()

        self.expect_statement_terminator()
        end_pos = val.end_pos if val and val.end_pos else start_pos
        node = Yield(value=val, start_pos=start_pos, end_pos=end_pos)
        return ExpressionStatement(expr=node, start_pos=start_pos, end_pos=end_pos)

    def parse_comprehension_clauses(self) -> List[ComprehensionClause]:
        """Parses one or more 'har <target> mein <iterable> [agar <condition>]*' clauses."""
        clauses: List[ComprehensionClause] = []

        while not self.is_at_end() and self.check_py_keyword("for"):
            for_tok = self.advance()  # Consume 'har'
            clause_start = for_tok.start_pos

            target = self.parse_primary()
            if not self.check_py_keyword("in"):
                raise self._syntax_error("Expected 'mein' or 'andar' after comprehension variable", self.peek())
            self.advance()  # Consume 'mein' / 'andar'

            iterable = self.parse_boolean_or()

            conditions: List[Expression] = []
            while not self.is_at_end() and self.check_py_keyword("if"):
                self.advance()  # Consume 'agar'
                cond = self.parse_boolean_or()
                conditions.append(cond)

            clause_end = conditions[-1].end_pos if conditions else iterable.end_pos
            clauses.append(
                ComprehensionClause(
                    target=target,
                    iterable=iterable,
                    conditions=conditions,
                    start_pos=clause_start,
                    end_pos=clause_end,
                )
            )

        return clauses

    def parse_lambda(self) -> LambdaExpression:
        """Parses an anonymous lambda function: sookshm [<params>]: <body>"""
        start_tok = self.advance()  # Consume 'sookshm'
        params: List[str] = []

        if not self.check(TokenType.COLON):
            param_tok = self.expect(TokenType.IDENTIFIER, "Expected parameter name in lambda")
            params.append(str(param_tok.value))
            while self.match(TokenType.COMMA):
                if self.check(TokenType.COLON):
                    break
                param_tok = self.expect(TokenType.IDENTIFIER, "Expected parameter name in lambda")
                params.append(str(param_tok.value))

        self.expect(TokenType.COLON, "Expected ':' after lambda parameters")
        body = self.parse_expression()
        return LambdaExpression(
            params=params,
            body=body,
            start_pos=start_tok.start_pos,
            end_pos=body.end_pos,
        )

    def parse_starred_or_expression(self) -> Expression:
        """Parses *expr (Starred) or a regular expression."""
        if self.match(TokenType.STAR):
            star_pos = self.tokens[self.cursor - 1].start_pos
            val = self.parse_expression()
            return Starred(value=val, start_pos=star_pos, end_pos=val.end_pos)
        return self.parse_expression()

    def parse_expression_or_tuple(self, allow_starred: bool = False) -> Expression:
        """Parses an expression or a comma-separated tuple of expressions."""
        first = self.parse_starred_or_expression() if allow_starred else self.parse_expression()
        if not self.match(TokenType.COMMA):
            return first

        elements = [first]
        while not self.is_at_end():
            if self.peek().type in (
                TokenType.ASSIGN,
                TokenType.PLUS_ASSIGN,
                TokenType.MINUS_ASSIGN,
                TokenType.STAR_ASSIGN,
                TokenType.SLASH_ASSIGN,
                TokenType.DOUBLE_SLASH_ASSIGN,
                TokenType.PERCENT_ASSIGN,
                TokenType.STAR_STAR_ASSIGN,
                TokenType.AMPERSAND_ASSIGN,
                TokenType.PIPE_ASSIGN,
                TokenType.CARET_ASSIGN,
                TokenType.LSHIFT_ASSIGN,
                TokenType.RSHIFT_ASSIGN,
                TokenType.NEWLINE,
                TokenType.EOF,
                TokenType.SEMICOLON,
                TokenType.DEDENT,
            ):
                break
            elt = self.parse_starred_or_expression() if allow_starred else self.parse_expression()
            elements.append(elt)
            if not self.match(TokenType.COMMA):
                break

        end_pos = elements[-1].end_pos if elements else first.end_pos
        return TupleLiteral(elements=elements, start_pos=first.start_pos, end_pos=end_pos)

    def parse_assignment_or_expression_statement(self) -> Statement:
        """Parses an assignment statement, annotated assignment, or expression statement."""
        expr = self.parse_expression_or_tuple(allow_starred=True)

        # 1. Annotated assignment: target: annotation [= value]
        if self.match(TokenType.COLON):
            annotation = self.parse_expression()
            value = None
            if self.match(TokenType.ASSIGN):
                value = self.parse_expression_or_tuple()
            self.expect_statement_terminator()
            end_pos = value.end_pos if value else annotation.end_pos
            return AnnAssign(
                target=expr,
                annotation=annotation,
                value=value,
                start_pos=expr.start_pos,
                end_pos=end_pos,
            )

        # 2. Assignment operators
        assign_tokens = {
            TokenType.ASSIGN: "=",
            TokenType.PLUS_ASSIGN: "+=",
            TokenType.MINUS_ASSIGN: "-=",
            TokenType.STAR_ASSIGN: "*=",
            TokenType.SLASH_ASSIGN: "/=",
            TokenType.DOUBLE_SLASH_ASSIGN: "//=",
            TokenType.PERCENT_ASSIGN: "%=",
            TokenType.STAR_STAR_ASSIGN: "**=",
            TokenType.AMPERSAND_ASSIGN: "&=",
            TokenType.PIPE_ASSIGN: "|=",
            TokenType.CARET_ASSIGN: "^=",
            TokenType.LSHIFT_ASSIGN: "<<=",
            TokenType.RSHIFT_ASSIGN: ">>=",
        }

        if self.peek().type in assign_tokens:
            op_tok = self.advance()
            op_str = assign_tokens[op_tok.type]
            value = self.parse_expression_or_tuple()
            self.expect_statement_terminator()
            return Assignment(
                target=expr,
                op=op_str,
                value=value,
                start_pos=expr.start_pos,
                end_pos=value.end_pos,
            )

        self.expect_statement_terminator()
        return ExpressionStatement(
            expr=expr,
            start_pos=expr.start_pos,
            end_pos=expr.end_pos,
        )

    def expect_statement_terminator(self) -> None:
        """Expects a NEWLINE or EOF to terminate a statement."""
        if self.is_at_end():
            return
        if self.check(TokenType.NEWLINE):
            self.advance()
            return
        tok = self.peek()
        raise self._syntax_error(f"Unexpected token '{tok.raw_text or tok.value}' after statement", tok)

    # -------------------------------------------------------------------------
    # Expression Parsing with Precedence Climbing
    # -------------------------------------------------------------------------

    def parse_expression(self) -> Expression:
        """Top-level entry for parsing expressions."""
        if self.check_py_keyword("lambda"):
            return self.parse_lambda()
        expr = self.parse_boolean_or()
        if self.match(TokenType.WALRUS):
            value = self.parse_expression()
            return AssignmentExpression(
                target=expr,
                value=value,
                start_pos=expr.start_pos,
                end_pos=value.end_pos,
            )
        return expr

    def parse_boolean_or(self) -> Expression:
        """Parses boolean OR: expr ('ya' / 'or' expr)*."""
        left = self.parse_boolean_and()
        values = [left]

        while self.check_py_keyword("or"):
            op_tok = self.advance()
            right = self.parse_boolean_and()
            values.append(right)

        if len(values) > 1:
            return BooleanOperation(
                op="or",
                values=values,
                start_pos=left.start_pos,
                end_pos=values[-1].end_pos,
            )
        return left

    def parse_boolean_and(self) -> Expression:
        """Parses boolean AND: expr ('aur' / 'and' expr)*."""
        left = self.parse_boolean_not()
        values = [left]

        while self.check_py_keyword("and"):
            op_tok = self.advance()
            right = self.parse_boolean_not()
            values.append(right)

        if len(values) > 1:
            return BooleanOperation(
                op="and",
                values=values,
                start_pos=left.start_pos,
                end_pos=values[-1].end_pos,
            )
        return left

    def parse_boolean_not(self) -> Expression:
        """Parses boolean NOT: 'nahi' / 'not' expr."""
        if self.check_py_keyword("not"):
            op_tok = self.advance()
            operand = self.parse_boolean_not()
            return UnaryOperation(
                op="not",
                operand=operand,
                start_pos=op_tok.start_pos,
                end_pos=operand.end_pos,
            )
        return self.parse_comparison()

    def parse_comparison(self) -> Expression:
        """Parses comparison operators: ==, !=, <, <=, >, >=, hai (is), mein (in)."""
        left = self.parse_bitwise_or()

        cmp_tokens = {
            TokenType.EQ: "==",
            TokenType.NE: "!=",
            TokenType.LT: "<",
            TokenType.LE: "<=",
            TokenType.GT: ">",
            TokenType.GE: ">=",
        }

        # Handle operators like ==, !=, etc.
        if self.peek().type in cmp_tokens:
            op_tok = self.advance()
            op_str = cmp_tokens[op_tok.type]
            right = self.parse_bitwise_or()
            return Comparison(
                left=left,
                op=op_str,
                right=right,
                start_pos=left.start_pos,
                end_pos=right.end_pos,
            )

        # Handle 'hai' (is) or 'mein' (in)
        if self.check_py_keyword("is"):
            op_tok = self.advance()
            op_str = "is"
            if self.check_py_keyword("not"):
                self.advance()
                op_str = "is not"
            right = self.parse_bitwise_or()
            return Comparison(
                left=left,
                op=op_str,
                right=right,
                start_pos=left.start_pos,
                end_pos=right.end_pos,
            )

        if self.check_py_keyword("in"):
            op_tok = self.advance()
            right = self.parse_bitwise_or()
            return Comparison(
                left=left,
                op="in",
                right=right,
                start_pos=left.start_pos,
                end_pos=right.end_pos,
            )

        return left

    def parse_bitwise_or(self) -> Expression:
        """Parses bitwise OR: left | right."""
        left = self.parse_bitwise_xor()
        while self.match(TokenType.PIPE):
            right = self.parse_bitwise_xor()
            left = BinaryOperation(left=left, op="|", right=right, start_pos=left.start_pos, end_pos=right.end_pos)
        return left

    def parse_bitwise_xor(self) -> Expression:
        """Parses bitwise XOR: left ^ right."""
        left = self.parse_bitwise_and()
        while self.match(TokenType.CARET):
            right = self.parse_bitwise_and()
            left = BinaryOperation(left=left, op="^", right=right, start_pos=left.start_pos, end_pos=right.end_pos)
        return left

    def parse_bitwise_and(self) -> Expression:
        """Parses bitwise AND: left & right."""
        left = self.parse_shift()
        while self.match(TokenType.AMPERSAND):
            right = self.parse_shift()
            left = BinaryOperation(left=left, op="&", right=right, start_pos=left.start_pos, end_pos=right.end_pos)
        return left

    def parse_shift(self) -> Expression:
        """Parses shift operators: <<, >>."""
        left = self.parse_term()
        while True:
            if self.match(TokenType.LSHIFT):
                right = self.parse_term()
                left = BinaryOperation(left=left, op="<<", right=right, start_pos=left.start_pos, end_pos=right.end_pos)
            elif self.match(TokenType.RSHIFT):
                right = self.parse_term()
                left = BinaryOperation(left=left, op=">>", right=right, start_pos=left.start_pos, end_pos=right.end_pos)
            else:
                break
        return left

    def parse_term(self) -> Expression:
        """Parses addition and subtraction: +, -."""
        left = self.parse_factor()
        while True:
            if self.match(TokenType.PLUS):
                right = self.parse_factor()
                left = BinaryOperation(left=left, op="+", right=right, start_pos=left.start_pos, end_pos=right.end_pos)
            elif self.match(TokenType.MINUS):
                right = self.parse_factor()
                left = BinaryOperation(left=left, op="-", right=right, start_pos=left.start_pos, end_pos=right.end_pos)
            else:
                break
        return left

    def parse_factor(self) -> Expression:
        """Parses multiplication, division, modulo: *, /, //, %, @."""
        left = self.parse_unary()
        while True:
            if self.match(TokenType.STAR):
                right = self.parse_unary()
                left = BinaryOperation(left=left, op="*", right=right, start_pos=left.start_pos, end_pos=right.end_pos)
            elif self.match(TokenType.SLASH):
                right = self.parse_unary()
                left = BinaryOperation(left=left, op="/", right=right, start_pos=left.start_pos, end_pos=right.end_pos)
            elif self.match(TokenType.DOUBLE_SLASH):
                right = self.parse_unary()
                left = BinaryOperation(left=left, op="//", right=right, start_pos=left.start_pos, end_pos=right.end_pos)
            elif self.match(TokenType.PERCENT):
                right = self.parse_unary()
                left = BinaryOperation(left=left, op="%", right=right, start_pos=left.start_pos, end_pos=right.end_pos)
            elif self.match(TokenType.AT):
                right = self.parse_unary()
                left = BinaryOperation(left=left, op="@", right=right, start_pos=left.start_pos, end_pos=right.end_pos)
            else:
                break
        return left

    def parse_unary(self) -> Expression:
        """Parses unary operators: +, -, ~, await (intezaar)."""
        if self.check_py_keyword("await"):
            tok = self.advance()
            operand = self.parse_unary()
            return Await(value=operand, start_pos=tok.start_pos, end_pos=operand.end_pos)
        if self.match(TokenType.PLUS):
            tok = self.tokens[self.cursor - 1]
            operand = self.parse_unary()
            return UnaryOperation(op="+", operand=operand, start_pos=tok.start_pos, end_pos=operand.end_pos)
        if self.match(TokenType.MINUS):
            tok = self.tokens[self.cursor - 1]
            operand = self.parse_unary()
            return UnaryOperation(op="-", operand=operand, start_pos=tok.start_pos, end_pos=operand.end_pos)
        if self.match(TokenType.TILDE):
            tok = self.tokens[self.cursor - 1]
            operand = self.parse_unary()
            return UnaryOperation(op="~", operand=operand, start_pos=tok.start_pos, end_pos=operand.end_pos)
        return self.parse_power()

    def parse_power(self) -> Expression:
        """Parses exponentiation: ** (right-associative)."""
        left = self.parse_call_subscript_attribute()
        if self.match(TokenType.STAR_STAR):
            right = self.parse_unary()  # Right-associative calls parse_unary
            return BinaryOperation(left=left, op="**", right=right, start_pos=left.start_pos, end_pos=right.end_pos)
        return left

    def parse_call_subscript_attribute(self) -> Expression:
        """Parses primary followed by calls (), subscripts [], or attribute accesses ."""
        expr = self.parse_primary()

        while True:
            # 1. Function call: expr(...)
            if self.match(TokenType.LPAREN):
                args: List[Expression] = []
                keywords: Dict[str, Expression] = {}

                if not self.check(TokenType.RPAREN):
                    while True:
                        if self.check(TokenType.RPAREN):
                            break
                        # Check keyword arg: name = expr
                        if (
                            self.check(TokenType.IDENTIFIER)
                            and self.peek(1).type == TokenType.ASSIGN
                        ):
                            k_tok = self.advance()  # name
                            self.advance()          # '='
                            v_expr = self.parse_expression()
                            keywords[str(k_tok.value)] = v_expr
                        elif self.match(TokenType.STAR):
                            # *args
                            star_pos = self.tokens[self.cursor - 1].start_pos
                            val = self.parse_expression()
                            args.append(Starred(value=val, start_pos=star_pos, end_pos=val.end_pos))
                        elif self.match(TokenType.STAR_STAR):
                            # **kwargs
                            star_pos = self.tokens[self.cursor - 1].start_pos
                            val = self.parse_expression()
                            args.append(DoubleStarred(value=val, start_pos=star_pos, end_pos=val.end_pos))
                        else:
                            args.append(self.parse_expression())

                        if not self.match(TokenType.COMMA):
                            break

                rparen = self.expect(TokenType.RPAREN, "Expected ')' after function arguments")
                expr = FunctionCall(
                    func=expr,
                    args=args,
                    keywords=keywords,
                    start_pos=expr.start_pos,
                    end_pos=rparen.end_pos,
                )
                continue

            # 2. Subscript / Slicing: expr[...]
            if self.match(TokenType.LBRACKET):
                subscript_expr = self.parse_subscript_or_slice()
                rbracket = self.expect(TokenType.RBRACKET, "Expected ']' after index")
                expr = Indexing(
                    value=expr,
                    index=subscript_expr,
                    start_pos=expr.start_pos,
                    end_pos=rbracket.end_pos,
                )
                continue

            # 3. Attribute access: expr.attr
            if self.match(TokenType.DOT):
                attr_tok = self.expect(TokenType.IDENTIFIER, "Expected attribute name after '.'")
                expr = AttributeAccess(
                    value=expr,
                    attr=str(attr_tok.value),
                    start_pos=expr.start_pos,
                    end_pos=attr_tok.end_pos,
                )
                continue

            break

        return expr

    def parse_subscript_or_slice(self) -> Expression:
        """Parses an index expression or a slice lower:upper:step."""
        # Check for slice starting with ':' e.g. [:5]
        if self.match(TokenType.COLON):
            upper = None
            step = None
            if not self.check(TokenType.RBRACKET) and not self.check(TokenType.COLON):
                upper = self.parse_expression()
            if self.match(TokenType.COLON):
                if not self.check(TokenType.RBRACKET):
                    step = self.parse_expression()
            return Slice(lower=None, upper=upper, step=step)

        first_expr = self.parse_expression()

        # If followed by ':', it is a slice
        if self.match(TokenType.COLON):
            upper = None
            step = None
            if not self.check(TokenType.RBRACKET) and not self.check(TokenType.COLON):
                upper = self.parse_expression()
            if self.match(TokenType.COLON):
                if not self.check(TokenType.RBRACKET):
                    step = self.parse_expression()
            return Slice(lower=first_expr, upper=upper, step=step)

        return first_expr

    def parse_primary(self) -> Expression:
        """Parses atomic primary expressions: literals, identifiers, lists, dicts, grouped exprs."""
        tok = self.peek()

        # 1. Literals
        if tok.type == TokenType.INTEGER:
            self.advance()
            return Integer(value=int(tok.value), start_pos=tok.start_pos, end_pos=tok.end_pos)

        if tok.type == TokenType.FLOAT:
            self.advance()
            return Float(value=float(tok.value), start_pos=tok.start_pos, end_pos=tok.end_pos)

        if tok.type == TokenType.COMPLEX:
            self.advance()
            return Complex(value=complex(tok.value), start_pos=tok.start_pos, end_pos=tok.end_pos)

        if tok.type == TokenType.STRING:
            self.advance()
            if tok.prefix and "f" in tok.prefix.lower():
                return self.parse_fstring(tok)
            return String(value=str(tok.value), prefix=tok.prefix, start_pos=tok.start_pos, end_pos=tok.end_pos)

        if tok.type == TokenType.BOOLEAN:
            self.advance()
            return Boolean(value=bool(tok.value), start_pos=tok.start_pos, end_pos=tok.end_pos)

        if tok.type == TokenType.NONE:
            self.advance()
            return NoneLiteral(value=None, start_pos=tok.start_pos, end_pos=tok.end_pos)

        # 2. Identifiers
        if tok.type == TokenType.IDENTIFIER:
            self.advance()
            return Identifier(name=str(tok.value), start_pos=tok.start_pos, end_pos=tok.end_pos)

        # 3. Parentheses: (expr) or tuple (x, y) or () or generator expression (elt har ...)
        if self.match(TokenType.LPAREN):
            start_pos = tok.start_pos
            if self.match(TokenType.RPAREN):
                # Empty tuple ()
                return TupleLiteral(elements=[], start_pos=start_pos, end_pos=self.tokens[self.cursor - 1].end_pos)

            first = self.parse_expression()

            # Generator expression: (elt har x mein iter [agar cond]*)
            if self.check_py_keyword("for"):
                clauses = self.parse_comprehension_clauses()
                rparen = self.expect(TokenType.RPAREN, "Expected ')' after generator expression")
                return GeneratorExpression(
                    element=first,
                    clauses=clauses,
                    start_pos=start_pos,
                    end_pos=rparen.end_pos,
                )

            if self.match(TokenType.COMMA):
                # Tuple literal (first, ...)
                elements = [first]
                while not self.check(TokenType.RPAREN) and not self.is_at_end():
                    elements.append(self.parse_expression())
                    if not self.match(TokenType.COMMA):
                        break
                rparen = self.expect(TokenType.RPAREN, "Expected ')' after tuple elements")
                return TupleLiteral(elements=elements, start_pos=start_pos, end_pos=rparen.end_pos)

            rparen = self.expect(TokenType.RPAREN, "Expected ')' after expression")
            return first

        # 4. Lists: [elem1, elem2, ...] or [elt har x mein iter [agar cond]*]
        if self.match(TokenType.LBRACKET):
            start_pos = tok.start_pos
            if self.match(TokenType.RBRACKET):
                return ListLiteral(elements=[], start_pos=start_pos, end_pos=self.tokens[self.cursor - 1].end_pos)

            first = self.parse_starred_or_expression()

            # List comprehension: [elt har x mein iter [agar cond]*]
            if self.check_py_keyword("for"):
                clauses = self.parse_comprehension_clauses()
                rbracket = self.expect(TokenType.RBRACKET, "Expected ']' after list comprehension")
                return ListComprehension(
                    element=first,
                    clauses=clauses,
                    start_pos=start_pos,
                    end_pos=rbracket.end_pos,
                )

            elements = [first]
            while self.match(TokenType.COMMA):
                if self.check(TokenType.RBRACKET):
                    break
                elements.append(self.parse_starred_or_expression())

            rbracket = self.expect(TokenType.RBRACKET, "Expected ']' after list elements")
            return ListLiteral(elements=elements, start_pos=start_pos, end_pos=rbracket.end_pos)

        # 5. Dictionaries / Sets / Comprehensions: { ... }
        if self.match(TokenType.LBRACE):
            start_pos = tok.start_pos
            if self.match(TokenType.RBRACE):
                # Empty dict {}
                return DictLiteral(keys=[], values=[], start_pos=start_pos, end_pos=self.tokens[self.cursor - 1].end_pos)

            # Check for dict unpacking as first element: {**dict_a, ...}
            if self.match(TokenType.STAR_STAR):
                first_val = self.parse_expression()
                keys = [NoneLiteral(start_pos=start_pos, end_pos=first_val.end_pos)]
                values = [DoubleStarred(value=first_val, start_pos=start_pos, end_pos=first_val.end_pos)]
                while self.match(TokenType.COMMA):
                    if self.check(TokenType.RBRACE):
                        break
                    if self.match(TokenType.STAR_STAR):
                        ds_pos = self.tokens[self.cursor - 1].start_pos
                        v = self.parse_expression()
                        keys.append(NoneLiteral(start_pos=ds_pos, end_pos=v.end_pos))
                        values.append(DoubleStarred(value=v, start_pos=ds_pos, end_pos=v.end_pos))
                    else:
                        k = self.parse_expression()
                        self.expect(TokenType.COLON, "Expected ':' after dictionary key")
                        v = self.parse_expression()
                        keys.append(k)
                        values.append(v)
                rbrace = self.expect(TokenType.RBRACE, "Expected '}' after dictionary elements")
                return DictLiteral(keys=keys, values=values, start_pos=start_pos, end_pos=rbrace.end_pos)

            first = self.parse_starred_or_expression()

            # Case A: Dictionary or Dict Comprehension
            if self.match(TokenType.COLON):
                first_val = self.parse_expression()
                if self.check_py_keyword("for"):
                    clauses = self.parse_comprehension_clauses()
                    rbrace = self.expect(TokenType.RBRACE, "Expected '}' after dict comprehension")
                    return DictComprehension(
                        key=first,
                        value=first_val,
                        clauses=clauses,
                        start_pos=start_pos,
                        end_pos=rbrace.end_pos,
                    )
                keys = [first]
                values = [first_val]
                while self.match(TokenType.COMMA):
                    if self.check(TokenType.RBRACE):
                        break
                    if self.match(TokenType.STAR_STAR):
                        ds_pos = self.tokens[self.cursor - 1].start_pos
                        v = self.parse_expression()
                        keys.append(NoneLiteral(start_pos=ds_pos, end_pos=v.end_pos))
                        values.append(DoubleStarred(value=v, start_pos=ds_pos, end_pos=v.end_pos))
                    else:
                        k = self.parse_expression()
                        self.expect(TokenType.COLON, "Expected ':' after dictionary key")
                        v = self.parse_expression()
                        keys.append(k)
                        values.append(v)
                rbrace = self.expect(TokenType.RBRACE, "Expected '}' after dictionary elements")
                return DictLiteral(keys=keys, values=values, start_pos=start_pos, end_pos=rbrace.end_pos)

            # Case B: Set Comprehension: {elt har x mein iter [agar cond]*}
            if self.check_py_keyword("for"):
                clauses = self.parse_comprehension_clauses()
                rbrace = self.expect(TokenType.RBRACE, "Expected '}' after set comprehension")
                return SetComprehension(
                    element=first,
                    clauses=clauses,
                    start_pos=start_pos,
                    end_pos=rbrace.end_pos,
                )

            # Case C: Set Literal: {elem1, elem2, ...}
            set_elements = [first]
            while self.match(TokenType.COMMA):
                if self.check(TokenType.RBRACE):
                    break
                set_elements.append(self.parse_starred_or_expression())
            rbrace = self.expect(TokenType.RBRACE, "Expected '}' after set elements")
            return SetLiteral(elements=set_elements, start_pos=start_pos, end_pos=rbrace.end_pos)

        # 6. Yield expression: upaj [<value>] or upaj se <value>
        if self.check_py_keyword("yield"):
            start_tok = self.advance()
            if self.check_py_keyword("from"):
                self.advance()  # Consume 'se'
                val = self.parse_expression()
                return YieldFrom(value=val, start_pos=start_tok.start_pos, end_pos=val.end_pos)

            val = None
            if not self.is_at_end() and self.peek().type not in (
                TokenType.RPAREN,
                TokenType.RBRACKET,
                TokenType.RBRACE,
                TokenType.COMMA,
                TokenType.COLON,
                TokenType.NEWLINE,
                TokenType.EOF,
                TokenType.SEMICOLON,
                TokenType.DEDENT,
            ):
                val = self.parse_expression()
            end_pos = val.end_pos if val and val.end_pos else start_tok.start_pos
            return Yield(value=val, start_pos=start_tok.start_pos, end_pos=end_pos)

        # Unexpected token
        raise self._syntax_error(f"Unexpected token '{tok.raw_text or tok.value}'", tok)

    def parse_fstring(self, tok: Token) -> Expression:
        """Parses an f-string into a JoinedStr AST node containing String and FormattedValue parts."""
        from ..lexer.lexer import HinglishLexer

        val = str(tok.value)
        parts: List[Expression] = []
        current_literal: List[str] = []
        i = 0
        n = len(val)

        while i < n:
            # Escaped opening brace {{ -> literal {
            if val[i : i + 2] == "{{":
                current_literal.append("{")
                i += 2
                continue

            # Escaped closing brace }} -> literal }
            if val[i : i + 2] == "}}":
                current_literal.append("}")
                i += 2
                continue

            # Unescaped closing brace
            if val[i] == "}":
                raise self._syntax_error("f-string: single '}' is not allowed", tok)

            # Opening brace { -> interpolation
            if val[i] == "{":
                if current_literal:
                    parts.append(
                        String(
                            value="".join(current_literal),
                            start_pos=tok.start_pos,
                            end_pos=tok.end_pos,
                        )
                    )
                    current_literal = []

                i += 1  # Skip '{'
                brace_depth = 1
                paren_depth = 0
                bracket_depth = 0
                in_str: Optional[str] = None
                escaped = False
                expr_chars: List[str] = []

                while i < n:
                    c = val[i]
                    if in_str:
                        expr_chars.append(c)
                        if escaped:
                            escaped = False
                        elif c == "\\":
                            escaped = True
                        elif c == in_str:
                            in_str = None
                        i += 1
                        continue

                    if c in ('"', "'"):
                        in_str = c
                        expr_chars.append(c)
                        i += 1
                        continue

                    if c == "(":
                        paren_depth += 1
                    elif c == ")":
                        if paren_depth > 0:
                            paren_depth -= 1
                    elif c == "[":
                        bracket_depth += 1
                    elif c == "]":
                        if bracket_depth > 0:
                            bracket_depth -= 1
                    elif c == "{":
                        brace_depth += 1
                    elif c == "}":
                        if brace_depth == 1 and paren_depth == 0 and bracket_depth == 0:
                            i += 1
                            break
                        brace_depth -= 1

                    expr_chars.append(c)
                    i += 1
                else:
                    raise self._syntax_error("f-string: expecting '}'", tok)

                expr_content = "".join(expr_chars)
                if not expr_content.strip():
                    raise self._syntax_error("f-string: empty expression not allowed", tok)

                # Scan top-level ':' for format_spec
                spec_idx: Optional[int] = None
                sub_brace = 0
                sub_paren = 0
                sub_bracket = 0
                sub_str = None
                sub_esc = False

                for idx, ch in enumerate(expr_content):
                    if sub_str:
                        if sub_esc:
                            sub_esc = False
                        elif ch == "\\":
                            sub_esc = True
                        elif ch == sub_str:
                            sub_str = None
                        continue
                    if ch in ('"', "'"):
                        sub_str = ch
                        continue
                    if ch == "(":
                        sub_paren += 1
                    elif ch == ")":
                        if sub_paren > 0:
                            sub_paren -= 1
                    elif ch == "[":
                        sub_bracket += 1
                    elif ch == "]":
                        if sub_bracket > 0:
                            sub_bracket -= 1
                    elif ch == "{":
                        sub_brace += 1
                    elif ch == "}":
                        if sub_brace > 0:
                            sub_brace -= 1
                    elif ch == ":" and sub_brace == 0 and sub_paren == 0 and sub_bracket == 0:
                        spec_idx = idx
                        break

                format_spec: Optional[str] = None
                if spec_idx is not None:
                    format_spec = expr_content[spec_idx + 1 :]
                    code_part = expr_content[:spec_idx]
                else:
                    code_part = expr_content

                conversion: Optional[str] = None
                code_part_stripped = code_part.rstrip()
                if len(code_part_stripped) >= 2 and code_part_stripped[-2] == "!" and code_part_stripped[-1] in ("r", "s", "a"):
                    conversion = code_part_stripped[-1]
                    code_part = code_part_stripped[:-2]

                code_to_parse = code_part.strip()
                if not code_to_parse:
                    raise self._syntax_error("f-string: empty expression not allowed", tok)

                sub_tokens = HinglishLexer(registry=self.registry).tokenize(code_to_parse)
                sub_parser = HinglishParser(sub_tokens, source_code=code_to_parse, registry=self.registry)
                parsed_expr = sub_parser.parse_expression()

                parts.append(
                    FormattedValue(
                        value=parsed_expr,
                        conversion=conversion,
                        format_spec=format_spec,
                        start_pos=tok.start_pos,
                        end_pos=tok.end_pos,
                    )
                )
                continue

            current_literal.append(val[i])
            i += 1

        if current_literal:
            parts.append(
                String(
                    value="".join(current_literal),
                    start_pos=tok.start_pos,
                    end_pos=tok.end_pos,
                )
            )

        return JoinedStr(parts=parts, start_pos=tok.start_pos, end_pos=tok.end_pos)

    # -------------------------------------------------------------------------
    # Pattern Matching (match / case) Parsing
    # -------------------------------------------------------------------------

    def parse_match(self) -> Match:
        """Parses a pattern matching statement: milaao <subject>: <cases>"""
        start_tok = self.advance()  # Consume 'milaao' / 'milao'
        start_pos = start_tok.start_pos

        subject = self.parse_expression()
        self.expect(TokenType.COLON, "Expected ':' after match subject")
        self.expect(TokenType.NEWLINE, "Expected newline after ':' in match")
        self.skip_newlines()
        self.expect(TokenType.INDENT, "Expected indented block of cases for match")
        self.skip_newlines()

        cases: List[MatchCase] = []
        while not self.is_at_end() and not self.check(TokenType.DEDENT):
            case_node = self.parse_match_case()
            cases.append(case_node)
            self.skip_newlines()

        self.expect(TokenType.DEDENT, "Expected dedent after match block")
        end_pos = cases[-1].end_pos if cases else start_pos
        return Match(subject=subject, cases=cases, start_pos=start_pos, end_pos=end_pos)

    def parse_match_case(self) -> MatchCase:
        """Parses a single case branch: vichaar <pattern> [agar <guard>]: <body>"""
        self.skip_newlines()
        tok = self.peek()
        if not self.check_py_keyword("case"):
            raise self._syntax_error("Expected 'vichaar' or 'sthiti' to start case branch", tok)
        case_tok = self.advance()  # Consume 'vichaar'
        start_pos = case_tok.start_pos

        pattern = self.parse_pattern()

        guard: Optional[Expression] = None
        if self.check_py_keyword("if"):
            self.advance()  # Consume 'agar'
            guard = self.parse_expression()

        body = self.parse_block("case")
        end_pos = body[-1].end_pos if body else start_pos
        return MatchCase(
            pattern=pattern,
            guard=guard,
            body=body,
            start_pos=start_pos,
            end_pos=end_pos,
        )

    def parse_pattern(self) -> MatchPattern:
        """Parses a pattern, supporting OR ('|') combinations."""
        first = self.parse_pattern_as()
        if not self.match(TokenType.PIPE):
            return first

        patterns = [first]
        while True:
            patterns.append(self.parse_pattern_as())
            if not self.match(TokenType.PIPE):
                break

        return MatchOr(
            patterns=patterns,
            start_pos=first.start_pos,
            end_pos=patterns[-1].end_pos,
        )

    def parse_pattern_as(self) -> MatchPattern:
        """Parses a pattern with optional 'jaise <name>' capture."""
        pat = self.parse_pattern_atom()
        if self.check_py_keyword("as"):
            self.advance()  # Consume 'jaise'
            name_tok = self.expect(TokenType.IDENTIFIER, "Expected identifier after 'jaise' in pattern")
            return MatchAs(
                pattern=pat,
                name=str(name_tok.value),
                start_pos=pat.start_pos,
                end_pos=name_tok.end_pos,
            )
        return pat

    def parse_pattern_atom(self) -> MatchPattern:
        """Parses atomic patterns: wildcard, literals, sequences, mappings, classes, captures."""
        tok = self.peek()
        start_pos = tok.start_pos

        # 1. Negative numbers: -1, -3.14
        if self.match(TokenType.MINUS):
            num_tok = self.peek()
            if num_tok.type == TokenType.INTEGER:
                self.advance()
                return MatchValue(
                    value=UnaryOperation(
                        op="-",
                        operand=Integer(value=int(num_tok.value), start_pos=num_tok.start_pos, end_pos=num_tok.end_pos),
                        start_pos=start_pos,
                        end_pos=num_tok.end_pos,
                    ),
                    start_pos=start_pos,
                    end_pos=num_tok.end_pos,
                )
            if num_tok.type == TokenType.FLOAT:
                self.advance()
                return MatchValue(
                    value=UnaryOperation(
                        op="-",
                        operand=Float(value=float(num_tok.value), start_pos=num_tok.start_pos, end_pos=num_tok.end_pos),
                        start_pos=start_pos,
                        end_pos=num_tok.end_pos,
                    ),
                    start_pos=start_pos,
                    end_pos=num_tok.end_pos,
                )

        # 2. Literals: Integer, Float, Complex, String
        if tok.type == TokenType.INTEGER:
            self.advance()
            return MatchValue(
                value=Integer(value=int(tok.value), start_pos=start_pos, end_pos=tok.end_pos),
                start_pos=start_pos,
                end_pos=tok.end_pos,
            )
        if tok.type == TokenType.FLOAT:
            self.advance()
            return MatchValue(
                value=Float(value=float(tok.value), start_pos=start_pos, end_pos=tok.end_pos),
                start_pos=start_pos,
                end_pos=tok.end_pos,
            )
        if tok.type == TokenType.COMPLEX:
            self.advance()
            return MatchValue(
                value=Complex(value=complex(tok.value), start_pos=start_pos, end_pos=tok.end_pos),
                start_pos=start_pos,
                end_pos=tok.end_pos,
            )
        if tok.type == TokenType.STRING:
            self.advance()
            return MatchValue(
                value=String(value=str(tok.value), start_pos=start_pos, end_pos=tok.end_pos),
                start_pos=start_pos,
                end_pos=tok.end_pos,
            )

        # 3. Singletons: sahi, galat, kuch_nahi / shunya
        if tok.type == TokenType.BOOLEAN:
            self.advance()
            return MatchSingleton(value=bool(tok.value), start_pos=start_pos, end_pos=tok.end_pos)

        if tok.type == TokenType.NONE:
            self.advance()
            return MatchSingleton(value=None, start_pos=start_pos, end_pos=tok.end_pos)

        if self.registry.is_literal_keyword(str(tok.raw_text or tok.value)):
            py_lit = self.registry.get_python_equivalent(str(tok.raw_text or tok.value))
            self.advance()
            val: Any = None
            if py_lit == "True":
                val = True
            elif py_lit == "False":
                val = False
            return MatchSingleton(value=val, start_pos=start_pos, end_pos=tok.end_pos)

        # 4. Sequence patterns: [ ... ] or ( ... )
        if self.match(TokenType.LBRACKET):
            elements: List[MatchPattern] = []
            while not self.check(TokenType.RBRACKET) and not self.is_at_end():
                if self.match(TokenType.STAR):
                    star_tok = self.tokens[self.cursor - 1]
                    if self.check(TokenType.IDENTIFIER):
                        id_tok = self.advance()
                        star_name = str(id_tok.value)
                        elements.append(MatchStar(name=star_name, start_pos=star_tok.start_pos, end_pos=id_tok.end_pos))
                    else:
                        elements.append(MatchStar(name=None, start_pos=star_tok.start_pos, end_pos=star_tok.end_pos))
                else:
                    elements.append(self.parse_pattern())

                if not self.match(TokenType.COMMA):
                    break

            rbracket = self.expect(TokenType.RBRACKET, "Expected ']' after sequence pattern")
            return MatchSequence(patterns=elements, start_pos=start_pos, end_pos=rbracket.end_pos)

        if self.match(TokenType.LPAREN):
            elements = []
            while not self.check(TokenType.RPAREN) and not self.is_at_end():
                if self.match(TokenType.STAR):
                    star_tok = self.tokens[self.cursor - 1]
                    if self.check(TokenType.IDENTIFIER):
                        id_tok = self.advance()
                        star_name = str(id_tok.value)
                        elements.append(MatchStar(name=star_name, start_pos=star_tok.start_pos, end_pos=id_tok.end_pos))
                    else:
                        elements.append(MatchStar(name=None, start_pos=star_tok.start_pos, end_pos=star_tok.end_pos))
                else:
                    elements.append(self.parse_pattern())

                if not self.match(TokenType.COMMA):
                    break

            rparen = self.expect(TokenType.RPAREN, "Expected ')' after sequence pattern")
            return MatchSequence(patterns=elements, start_pos=start_pos, end_pos=rparen.end_pos)

        # 5. Mapping patterns: { ... }
        if self.match(TokenType.LBRACE):
            keys: List[Expression] = []
            patterns: List[MatchPattern] = []
            rest: Optional[str] = None

            while not self.check(TokenType.RBRACE) and not self.is_at_end():
                if self.match(TokenType.STAR_STAR):
                    rest_tok = self.expect(TokenType.IDENTIFIER, "Expected identifier after '**' in mapping pattern")
                    rest = str(rest_tok.value)
                    self.match(TokenType.COMMA)
                    break

                k = self.parse_expression()
                self.expect(TokenType.COLON, "Expected ':' in mapping pattern")
                p = self.parse_pattern()
                keys.append(k)
                patterns.append(p)

                if not self.match(TokenType.COMMA):
                    break

            rbrace = self.expect(TokenType.RBRACE, "Expected '}' after mapping pattern")
            return MatchMapping(keys=keys, patterns=patterns, rest=rest, start_pos=start_pos, end_pos=rbrace.end_pos)

        # 6. Identifier-based patterns: wildcard '_', class 'Point(...)', value 'Color.RED', or capture 'x'
        if tok.type == TokenType.IDENTIFIER:
            id_name = str(tok.value)
            # Wildcard
            if id_name == "_":
                self.advance()
                return MatchAs(pattern=None, name="_", start_pos=start_pos, end_pos=tok.end_pos)

            # Class pattern: Name(...)
            if self.peek(1).type == TokenType.LPAREN:
                self.advance()  # Consume name
                self.expect(TokenType.LPAREN, "Expected '(' in class pattern")
                pos_patterns: List[MatchPattern] = []
                kwd_attrs: List[str] = []
                kwd_patterns: List[MatchPattern] = []

                while not self.check(TokenType.RPAREN) and not self.is_at_end():
                    if self.check(TokenType.IDENTIFIER) and self.peek(1).type == TokenType.ASSIGN:
                        k_tok = self.advance()
                        self.advance()  # '='
                        p = self.parse_pattern()
                        kwd_attrs.append(str(k_tok.value))
                        kwd_patterns.append(p)
                    else:
                        p = self.parse_pattern()
                        pos_patterns.append(p)

                    if not self.match(TokenType.COMMA):
                        break

                rparen = self.expect(TokenType.RPAREN, "Expected ')' after class pattern")
                cls_node = Identifier(name=id_name, start_pos=start_pos, end_pos=tok.end_pos)
                return MatchClass(
                    cls=cls_node,
                    patterns=pos_patterns,
                    kwd_attrs=kwd_attrs,
                    kwd_patterns=kwd_patterns,
                    start_pos=start_pos,
                    end_pos=rparen.end_pos,
                )

            # Value pattern with attribute access: Color.RED
            if self.peek(1).type == TokenType.DOT:
                expr = self.parse_call_subscript_attribute()
                return MatchValue(value=expr, start_pos=start_pos, end_pos=expr.end_pos)

            # Standard variable capture: x
            self.advance()
            return MatchAs(pattern=None, name=id_name, start_pos=start_pos, end_pos=tok.end_pos)

        raise self._syntax_error(f"Unexpected token in pattern: '{tok.raw_text or tok.value}'", tok)
