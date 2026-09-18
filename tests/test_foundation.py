"""Tests for the Hinglish package foundation, imports, and module structure."""

import unittest
from hinglish import __version__
from hinglish.cli import create_parser
from hinglish.runtime import get_default_globals, dikhao
from hinglish.lexer import TokenType, Position, Token, BaseLexer
from hinglish.parser import BaseParser
from hinglish.ast import ASTNode, Program, Statement, Expression
from hinglish.compiler import BaseCompiler


class TestFoundation(unittest.TestCase):
    """Verifies that all architectural modules and interfaces exist and load cleanly."""

    def test_version_format(self) -> None:
        self.assertIsInstance(__version__, str)
        self.assertTrue(len(__version__.split(".")) >= 2)

    def test_cli_parser_setup(self) -> None:
        parser = create_parser()
        self.assertEqual(parser.prog, "hinglish")
        parsed = parser.parse_args(["test.hin"])
        self.assertEqual(parsed.file, "test.hin")

    def test_runtime_defaults(self) -> None:
        context = get_default_globals()
        self.assertIn("dikhao", context)
        self.assertIs(context["dikhao"], dikhao)
        self.assertIs(context["sahi"], True)
        self.assertIs(context["galat"], False)
        self.assertIsNone(context["kuch_nahi"])
        self.assertIsNone(context["shunya"])

    def test_lexer_token_structure(self) -> None:
        pos_start = Position(line=1, column=0)
        pos_end = Position(line=1, column=4)
        tok = Token(
            type=TokenType.KEYWORD,
            value="agar",
            start_pos=pos_start,
            end_pos=pos_end,
            raw_text="agar",
        )
        self.assertEqual(tok.type, TokenType.KEYWORD)
        self.assertEqual(tok.value, "agar")
        self.assertEqual(str(pos_start), "1:0")

    def test_ast_hierarchy(self) -> None:
        prog = Program()
        self.assertIsInstance(prog, ASTNode)
        self.assertEqual(prog.body, [])


if __name__ == "__main__":
    unittest.main()
