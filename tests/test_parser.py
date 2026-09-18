"""Comprehensive unit tests for the Hinglish Parser and AST generation."""

import unittest
from pathlib import Path

from hinglish.ast import (
    Assignment,
    AttributeAccess,
    BinaryOperation,
    Boolean,
    BooleanOperation,
    Break,
    Comparison,
    Complex,
    Continue,
    DictLiteral,
    ExpressionStatement,
    Float,
    For,
    FromImport,
    FunctionCall,
    FunctionDefinition,
    Identifier,
    If,
    Import,
    Indexing,
    Integer,
    ListLiteral,
    NoneLiteral,
    Pass,
    Program,
    Return,
    Slice,
    String,
    TupleLiteral,
    UnaryOperation,
    While,
    format_ast,
)
from hinglish.exceptions import HinglishSyntaxError
from hinglish.parser import parse


class TestHinglishParser(unittest.TestCase):
    """Test suite covering AST nodes, statement and expression grammar, precedence, and syntax diagnostics."""

    def test_variable_assignment(self) -> None:
        source = 'naam = "Neeraj"\numar = 25\nx += 1\n'
        prog = parse(source)
        self.assertEqual(len(prog.body), 3)

        stmt1 = prog.body[0]
        self.assertIsInstance(stmt1, Assignment)
        self.assertIsInstance(stmt1.target, Identifier)
        self.assertEqual(stmt1.target.name, "naam")
        self.assertEqual(stmt1.op, "=")
        self.assertIsInstance(stmt1.value, String)
        self.assertEqual(stmt1.value.value, "Neeraj")

        stmt2 = prog.body[1]
        self.assertIsInstance(stmt2, Assignment)
        self.assertEqual(stmt2.target.name, "umar")
        self.assertIsInstance(stmt2.value, Integer)
        self.assertEqual(stmt2.value.value, 25)

        stmt3 = prog.body[2]
        self.assertIsInstance(stmt3, Assignment)
        self.assertEqual(stmt3.op, "+=")
        self.assertEqual(stmt3.value.value, 1)

    def test_literals_ast(self) -> None:
        source = "10\n3.14\n3j\n'namaste'\nsahi\ngalat\nkuch_nahi\n"
        prog = parse(source)
        exprs = [stmt.expr for stmt in prog.body if isinstance(stmt, ExpressionStatement)]

        self.assertIsInstance(exprs[0], Integer)
        self.assertEqual(exprs[0].value, 10)

        self.assertIsInstance(exprs[1], Float)
        self.assertEqual(exprs[1].value, 3.14)

        self.assertIsInstance(exprs[2], Complex)
        self.assertEqual(exprs[2].value, 3j)

        self.assertIsInstance(exprs[3], String)
        self.assertEqual(exprs[3].value, "namaste")

        self.assertIsInstance(exprs[4], Boolean)
        self.assertEqual(exprs[4].value, True)

        self.assertIsInstance(exprs[5], Boolean)
        self.assertEqual(exprs[5].value, False)

        self.assertIsInstance(exprs[6], NoneLiteral)
        self.assertIsNone(exprs[6].value)

    def test_operator_precedence(self) -> None:
        # x + 2 * 3 => x + (2 * 3)
        prog = parse("natija = x + 2 * 3\n")
        assign = prog.body[0]
        self.assertIsInstance(assign.value, BinaryOperation)
        self.assertEqual(assign.value.op, "+")
        self.assertIsInstance(assign.value.left, Identifier)
        self.assertIsInstance(assign.value.right, BinaryOperation)
        self.assertEqual(assign.value.right.op, "*")

        # 2 * 3 + x => (2 * 3) + x
        prog2 = parse("natija = 2 * 3 + x\n")
        assign2 = prog2.body[0]
        self.assertIsInstance(assign2.value, BinaryOperation)
        self.assertEqual(assign2.value.op, "+")
        self.assertIsInstance(assign2.value.left, BinaryOperation)
        self.assertEqual(assign2.value.left.op, "*")
        self.assertIsInstance(assign2.value.right, Identifier)

        # 2 ** 3 ** 2 => 2 ** (3 ** 2) (Right-associative)
        prog3 = parse("natija = 2 ** 3 ** 2\n")
        assign3 = prog3.body[0]
        self.assertIsInstance(assign3.value, BinaryOperation)
        self.assertEqual(assign3.value.op, "**")
        self.assertEqual(assign3.value.left.value, 2)
        self.assertIsInstance(assign3.value.right, BinaryOperation)
        self.assertEqual(assign3.value.right.left.value, 3)
        self.assertEqual(assign3.value.right.right.value, 2)

    def test_comparison_and_boolean_precedence(self) -> None:
        # x > 5 aur y < 10 => (x > 5) and (y < 10)
        prog = parse("shart = x > 5 aur y < 10\n")
        assign = prog.body[0]
        self.assertIsInstance(assign.value, BooleanOperation)
        self.assertEqual(assign.value.op, "and")
        self.assertEqual(len(assign.value.values), 2)
        self.assertIsInstance(assign.value.values[0], Comparison)
        self.assertIsInstance(assign.value.values[1], Comparison)

        # a ya b aur c => a or (b and c) (and has higher precedence than or)
        prog2 = parse("ans = a ya b aur c\n")
        assign2 = prog2.body[0]
        self.assertIsInstance(assign2.value, BooleanOperation)
        self.assertEqual(assign2.value.op, "or")
        self.assertIsInstance(assign2.value.values[0], Identifier)
        self.assertIsInstance(assign2.value.values[1], BooleanOperation)
        self.assertEqual(assign2.value.values[1].op, "and")

    def test_unary_and_boolean_not(self) -> None:
        prog = parse("val = -x + ~y\nshart = nahi sahi\n")
        assign1 = prog.body[0]
        self.assertIsInstance(assign1.value.left, UnaryOperation)
        self.assertEqual(assign1.value.left.op, "-")
        self.assertIsInstance(assign1.value.right, UnaryOperation)
        self.assertEqual(assign1.value.right.op, "~")

        assign2 = prog.body[1]
        self.assertIsInstance(assign2.value, UnaryOperation)
        self.assertEqual(assign2.value.op, "not")
        self.assertIsInstance(assign2.value.operand, Boolean)

    def test_function_call(self) -> None:
        source = 'dikhao("Namaste", naam, end="\\n")\n'
        prog = parse(source)
        stmt = prog.body[0]
        self.assertIsInstance(stmt, ExpressionStatement)
        call = stmt.expr
        self.assertIsInstance(call, FunctionCall)
        self.assertEqual(call.func.name, "dikhao")
        self.assertEqual(len(call.args), 2)
        self.assertIn("end", call.keywords)
        self.assertEqual(call.keywords["end"].value, "\n")

    def test_subscript_indexing_and_slices(self) -> None:
        source = "a = shehar[0]\nb = shehar[1:5]\nc = shehar[::2]\n"
        prog = parse(source)

        idx1 = prog.body[0].value
        self.assertIsInstance(idx1, Indexing)
        self.assertIsInstance(idx1.index, Integer)
        self.assertEqual(idx1.index.value, 0)

        idx2 = prog.body[1].value
        self.assertIsInstance(idx2, Indexing)
        self.assertIsInstance(idx2.index, Slice)
        self.assertEqual(idx2.index.lower.value, 1)
        self.assertEqual(idx2.index.upper.value, 5)
        self.assertIsNone(idx2.index.step)

        idx3 = prog.body[2].value
        self.assertIsInstance(idx3, Indexing)
        self.assertIsInstance(idx3.index, Slice)
        self.assertIsNone(idx3.index.lower)
        self.assertIsNone(idx3.index.upper)
        self.assertEqual(idx3.index.step.value, 2)

    def test_attribute_access(self) -> None:
        source = "naam = vyakti.pata.shehar\nvyakti.dikhao()\n"
        prog = parse(source)

        attr1 = prog.body[0].value
        self.assertIsInstance(attr1, AttributeAccess)
        self.assertEqual(attr1.attr, "shehar")
        self.assertIsInstance(attr1.value, AttributeAccess)
        self.assertEqual(attr1.value.attr, "pata")

        call = prog.body[1].expr
        self.assertIsInstance(call, FunctionCall)
        self.assertIsInstance(call.func, AttributeAccess)
        self.assertEqual(call.func.attr, "dikhao")

    def test_lists_dicts_tuples(self) -> None:
        source = "soochi = [1, 2, 'teen']\nkosh = {'a': 1, 'b': 2}\ntup = (10, 20)\n"
        prog = parse(source)

        lst = prog.body[0].value
        self.assertIsInstance(lst, ListLiteral)
        self.assertEqual(len(lst.elements), 3)

        d = prog.body[1].value
        self.assertIsInstance(d, DictLiteral)
        self.assertEqual(len(d.keys), 2)
        self.assertEqual(len(d.values), 2)

        tup = prog.body[2].value
        self.assertIsInstance(tup, TupleLiteral)
        self.assertEqual(len(tup.elements), 2)

    def test_if_elif_else_statement(self) -> None:
        source = (
            'agar umar >= 18:\n'
            '    dikhao("bada")\n'
            'warna_agar umar >= 16:\n'
            '    dikhao("learner")\n'
            'warna:\n'
            '    dikhao("chhota")\n'
        )
        prog = parse(source)
        stmt = prog.body[0]
        self.assertIsInstance(stmt, If)
        self.assertIsInstance(stmt.condition, Comparison)
        self.assertEqual(len(stmt.body), 1)

        self.assertEqual(len(stmt.elif_clauses), 1)
        self.assertIsInstance(stmt.elif_clauses[0].condition, Comparison)
        self.assertEqual(len(stmt.elif_clauses[0].body), 1)

        self.assertIsNotNone(stmt.else_body)
        self.assertEqual(len(stmt.else_body), 1)

    def test_while_loop(self) -> None:
        source = "jabtak ginti <= 5:\n    dikhao(ginti)\n    ginti += 1\n"
        prog = parse(source)
        stmt = prog.body[0]
        self.assertIsInstance(stmt, While)
        self.assertIsInstance(stmt.condition, Comparison)
        self.assertEqual(len(stmt.body), 2)

    def test_for_loop(self) -> None:
        source = 'har x mein [1, 2, 3]:\n    dikhao(x)\n'
        prog = parse(source)
        stmt = prog.body[0]
        self.assertIsInstance(stmt, For)
        self.assertIsInstance(stmt.target, Identifier)
        self.assertEqual(stmt.target.name, "x")
        self.assertIsInstance(stmt.iterable, ListLiteral)
        self.assertEqual(len(stmt.body), 1)

    def test_for_loop_with_andar_alias(self) -> None:
        source = 'har x andar soochi:\n    dikhao(x)\n'
        prog = parse(source)
        stmt = prog.body[0]
        self.assertIsInstance(stmt, For)
        self.assertEqual(stmt.target.name, "x")

    def test_function_definition_and_return(self) -> None:
        source = (
            'kaam jod(a, b):\n'
            '    natija = a + b\n'
            '    wapas natija\n'
        )
        prog = parse(source)
        stmt = prog.body[0]
        self.assertIsInstance(stmt, FunctionDefinition)
        self.assertEqual(stmt.name, "jod")
        self.assertEqual(stmt.params, ["a", "b"])
        self.assertEqual(len(stmt.body), 2)
        self.assertIsInstance(stmt.body[1], Return)
        self.assertIsInstance(stmt.body[1].value, Identifier)

    def test_pass_break_continue(self) -> None:
        source = "chhod_do\nruko\naage_bado\n"
        prog = parse(source)
        self.assertIsInstance(prog.body[0], Pass)
        self.assertIsInstance(prog.body[1], Break)
        self.assertIsInstance(prog.body[2], Continue)

    def test_import_statements(self) -> None:
        source = "laao math\nlaao math jaise m\nse math laao sqrt jaise s\n"
        prog = parse(source)
        self.assertIsInstance(prog.body[0], Import)
        self.assertEqual(prog.body[0].names, [("math", None)])

        self.assertIsInstance(prog.body[1], Import)
        self.assertEqual(prog.body[1].names, [("math", "m")])

        self.assertIsInstance(prog.body[2], FromImport)
        self.assertEqual(prog.body[2].module, "math")
        self.assertEqual(prog.body[2].names, [("sqrt", "s")])

    def test_nested_blocks(self) -> None:
        source = (
            'agar a:\n'
            '    agar b:\n'
            '        dikhao("nested")\n'
            '    warna:\n'
            '        dikhao("else nested")\n'
        )
        prog = parse(source)
        outer_if = prog.body[0]
        self.assertIsInstance(outer_if, If)
        inner_if = outer_if.body[0]
        self.assertIsInstance(inner_if, If)
        self.assertIsNotNone(inner_if.else_body)

    def test_syntax_error_missing_colon_if(self) -> None:
        source = "agar x > 5\n    dikhao(x)\n"
        with self.assertRaises(HinglishSyntaxError) as ctx:
            parse(source)
        err = ctx.exception
        self.assertIn("Expected ':' after agar", str(err))
        self.assertEqual(err.line, 1)

    def test_syntax_error_missing_condition_if(self) -> None:
        source = "agar:\n    dikhao(x)\n"
        with self.assertRaises(HinglishSyntaxError) as ctx:
            parse(source)
        err = ctx.exception
        self.assertIn("Expected condition expression after 'agar'", str(err))

    def test_syntax_error_missing_condition_while(self) -> None:
        source = "jabtak:\n    dikhao(x)\n"
        with self.assertRaises(HinglishSyntaxError) as ctx:
            parse(source)
        err = ctx.exception
        self.assertIn("Expected condition expression after 'jabtak'", str(err))

    def test_syntax_error_missing_indent(self) -> None:
        source = "agar x > 5:\ndikhao(x)\n"
        with self.assertRaises(HinglishSyntaxError) as ctx:
            parse(source)
        err = ctx.exception
        self.assertIn("Expected an indented block after ':'", str(err))

    def test_ast_dump_format(self) -> None:
        source = 'agar x == 10:\n    dikhao("Namaste")\n'
        prog = parse(source)
        dump = format_ast(prog)
        self.assertIn("Program(", dump)
        self.assertIn("If(", dump)
        self.assertIn("Comparison(", dump)
        self.assertIn("FunctionCall(", dump)

    def test_parse_all_example_files(self) -> None:
        example_dir = Path(__file__).parent.parent / "examples"
        hin_files = list(example_dir.glob("*.hin"))
        self.assertTrue(len(hin_files) >= 3)

        for hin_file in hin_files:
            content = hin_file.read_text(encoding="utf-8")
            prog = parse(content)
            self.assertIsInstance(prog, Program)
            self.assertTrue(len(prog.body) > 0)


if __name__ == "__main__":
    unittest.main()
