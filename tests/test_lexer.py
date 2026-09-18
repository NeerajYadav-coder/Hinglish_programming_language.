"""Comprehensive tests for the Hinglish Lexer implementation."""

import unittest
from pathlib import Path

from hinglish.exceptions import (
    HinglishIndentationError,
    HinglishLexerError,
)
from hinglish.keywords import DEFAULT_KEYWORD_REGISTRY, KeywordRegistry
from hinglish.lexer import (
    HinglishLexer,
    TokenType,
    format_tokens,
    tokenize,
)


class TestHinglishLexer(unittest.TestCase):
    """Test suite covering tokenization, operators, literals, indentation, and error diagnostics."""

    def test_basic_assignment(self) -> None:
        source = 'naam = "Neeraj"'
        tokens = tokenize(source)
        types = [t.type for t in tokens]
        values = [t.value for t in tokens]

        self.assertEqual(
            types,
            [
                TokenType.IDENTIFIER,
                TokenType.ASSIGN,
                TokenType.STRING,
                TokenType.NEWLINE,
                TokenType.EOF,
            ],
        )
        self.assertEqual(values, ["naam", "=", "Neeraj", "\n", None])

    def test_unicode_and_devanagari_identifiers(self) -> None:
        source = 'नाम = "नीरज"\nउम्र = 25\n'
        tokens = tokenize(source)
        ident_tokens = [t for t in tokens if t.type == TokenType.IDENTIFIER]
        self.assertEqual([t.value for t in ident_tokens], ["नाम", "उम्र"])

    def test_numeric_literals(self) -> None:
        source = "10 42 1_000_000 0xff 0b1011 0o77 3.14 .5 1e-4 2.5E+3 3j 4.5J"
        tokens = tokenize(source)

        int_tokens = [t for t in tokens if t.type == TokenType.INTEGER]
        float_tokens = [t for t in tokens if t.type == TokenType.FLOAT]
        complex_tokens = [t for t in tokens if t.type == TokenType.COMPLEX]

        self.assertEqual([t.value for t in int_tokens], [10, 42, 1000000, 255, 11, 63])
        self.assertEqual([t.value for t in float_tokens], [3.14, 0.5, 0.0001, 2500.0])
        self.assertEqual([t.value for t in complex_tokens], [3j, 4.5j])

    def test_strings_and_prefixes(self) -> None:
        source = (
            '\'single\' "double" """triple double""" \'\'\'triple single\'\'\' '
            'r"raw\\nstring" f"hello {x}"'
        )
        tokens = tokenize(source)
        str_tokens = [t for t in tokens if t.type == TokenType.STRING]

        self.assertEqual(len(str_tokens), 6)
        self.assertEqual(str_tokens[0].value, "single")
        self.assertEqual(str_tokens[1].value, "double")
        self.assertEqual(str_tokens[2].value, "triple double")
        self.assertEqual(str_tokens[3].value, "triple single")
        self.assertEqual(str_tokens[4].value, "raw\\nstring")

    def test_operators_maximal_munch(self) -> None:
        source = "+= -= *= /= //= %= **= &= |= ^= @= <<= >>= := -> ... == != <= >= ** // << >>"
        tokens = tokenize(source)
        types = [t.type for t in tokens if t.type not in (TokenType.NEWLINE, TokenType.EOF)]

        expected = [
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
            TokenType.AT_ASSIGN,
            TokenType.LSHIFT_ASSIGN,
            TokenType.RSHIFT_ASSIGN,
            TokenType.WALRUS,
            TokenType.ARROW,
            TokenType.ELLIPSIS,
            TokenType.EQ,
            TokenType.NE,
            TokenType.LE,
            TokenType.GE,
            TokenType.STAR_STAR,
            TokenType.DOUBLE_SLASH,
            TokenType.LSHIFT,
            TokenType.RSHIFT,
        ]
        self.assertEqual(types, expected)

    def test_keywords_and_literals(self) -> None:
        source = (
            "agar warna warna_agar jabtak har kaam wapas varg koshish pakdo "
            "antatah uthav daawa saath jaise laao se asamanantar intezaar upaj "
            "milao sthiti sahi galat kuch_nahi shunya aur ya nahi hai"
        )
        tokens = tokenize(source)

        bool_tokens = [t for t in tokens if t.type == TokenType.BOOLEAN]
        none_tokens = [t for t in tokens if t.type == TokenType.NONE]
        kw_tokens = [t for t in tokens if t.type == TokenType.KEYWORD]

        self.assertEqual([t.value for t in bool_tokens], [True, False])
        self.assertEqual([t.value for t in none_tokens], [None, None])
        self.assertIn("agar", [t.value for t in kw_tokens])
        self.assertIn("varg", [t.value for t in kw_tokens])
        self.assertIn("koshish", [t.value for t in kw_tokens])
        self.assertIn("aur", [t.value for t in kw_tokens])

    def test_single_block_indentation(self) -> None:
        source = "agar x == 10:\n    y = 20\n"
        tokens = tokenize(source)
        types = [t.type for t in tokens]

        self.assertEqual(
            types,
            [
                TokenType.KEYWORD,      # agar
                TokenType.IDENTIFIER,   # x
                TokenType.EQ,           # ==
                TokenType.INTEGER,      # 10
                TokenType.COLON,        # :
                TokenType.NEWLINE,      # \n
                TokenType.INDENT,       # indent 4
                TokenType.IDENTIFIER,   # y
                TokenType.ASSIGN,       # =
                TokenType.INTEGER,      # 20
                TokenType.NEWLINE,      # \n
                TokenType.DEDENT,       # dedent to 0
                TokenType.EOF,
            ],
        )

    def test_nested_blocks_and_multiple_dedents(self) -> None:
        source = (
            "agar a:\n"
            "    agar b:\n"
            "        x = 1\n"
            "y = 2"
        )
        tokens = tokenize(source)
        types = [t.type for t in tokens]

        dedents = [t for t in tokens if t.type == TokenType.DEDENT]
        indents = [t for t in tokens if t.type == TokenType.INDENT]

        self.assertEqual(len(indents), 2)
        self.assertEqual(len(dedents), 2)

    def test_bracket_nesting_ignores_newlines_and_indentation(self) -> None:
        source = (
            "soochi = [\n"
            "    1,\n"
            "    2,\n"
            "    3\n"
            "]\n"
        )
        tokens = tokenize(source)
        types = [t.type for t in tokens]

        # No INDENT or DEDENT should be emitted inside brackets
        self.assertNotIn(TokenType.INDENT, types)
        self.assertNotIn(TokenType.DEDENT, types)

    def test_comments_with_hindi(self) -> None:
        source = (
            "# यह एक comment है\n"
            "x = 10 # Inline comment\n"
            "       # Indented comment on empty block line\n"
            "y = 20\n"
        )
        # Default: comments discarded
        tokens = tokenize(source)
        types = [t.type for t in tokens]
        self.assertNotIn(TokenType.COMMENT, types)

        # Optional: include comments
        tokens_with_comments = tokenize(source, include_comments=True)
        types_with_comments = [t.type for t in tokens_with_comments]
        self.assertIn(TokenType.COMMENT, types_with_comments)

    def test_explicit_line_continuation(self) -> None:
        source = "x = 10 + \\\n    20"
        tokens = tokenize(source)
        types = [t.type for t in tokens]

        self.assertNotIn(TokenType.INDENT, types)
        values = [t.value for t in tokens if t.type in (TokenType.IDENTIFIER, TokenType.ASSIGN, TokenType.PLUS, TokenType.INTEGER)]
        self.assertEqual(values, ["x", "=", 10, "+", 20])

    def test_source_locations(self) -> None:
        source = "x = 42"
        tokens = tokenize(source)
        self.assertEqual(tokens[0].line, 1)
        self.assertEqual(tokens[0].column, 1)
        self.assertEqual(tokens[0].location, "Line 1, Column 1")
        self.assertEqual(tokens[1].column, 3)
        self.assertEqual(tokens[2].column, 5)

    def test_invalid_input_error_at_at_at(self) -> None:
        source = "naam = @@@"
        with self.assertRaises(HinglishLexerError) as ctx:
            tokenize(source)
        err = ctx.exception
        self.assertEqual(err.line, 1)
        self.assertEqual(err.column, 8)
        self.assertIn("Unexpected character '@'", str(err))
        self.assertIn("naam = @@@", str(err))

    def test_invalid_character_error_dollar(self) -> None:
        source = "x = $$$"
        with self.assertRaises(HinglishLexerError) as ctx:
            tokenize(source)
        err = ctx.exception
        self.assertEqual(err.line, 1)
        self.assertEqual(err.column, 5)
        self.assertIn("Unexpected character '$'", str(err))

    def test_indentation_error_unmatched(self) -> None:
        source = (
            "agar x:\n"
            "    a = 1\n"
            "  b = 2\n"  # 2 spaces does not match 4 or 0
        )
        with self.assertRaises(HinglishIndentationError):
            tokenize(source)

    def test_indentation_error_mixed_tabs_spaces(self) -> None:
        source = (
            "agar x:\n"
            " \t a = 1\n"
        )
        with self.assertRaises(HinglishIndentationError):
            tokenize(source)

    def test_unterminated_string_error(self) -> None:
        source = 'naam = "Neeraj'
        with self.assertRaises(HinglishLexerError):
            tokenize(source)

    def test_debug_format_tokens(self) -> None:
        source = 'agar naam == "Neeraj":\n    dikhao("Namaste")'
        tokens = tokenize(source)
        table = format_tokens(tokens)
        self.assertIn("KEYWORD", table)
        self.assertIn("→ if", table)
        self.assertIn("builtin (print)", table)

    def test_tokenize_all_example_files(self) -> None:
        example_dir = Path(__file__).parent.parent / "examples"
        hin_files = list(example_dir.glob("*.hin"))
        self.assertTrue(len(hin_files) >= 3)

        for hin_file in hin_files:
            content = hin_file.read_text(encoding="utf-8")
            tokens = tokenize(content)
            self.assertTrue(len(tokens) > 0)
            self.assertEqual(tokens[-1].type, TokenType.EOF)


if __name__ == "__main__":
    unittest.main()
