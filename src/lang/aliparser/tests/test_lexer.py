import pytest

from aliparser import Lexer, Token


def lex(src: str):
    """Convenience wrapper returning list of token tuples (type, value)."""
    return [(t.type, t.value) for t in Lexer(src).tokens()]


def test_single_line_comment():
    code = "# hello world\n"
    tokens = lex(code)
    assert tokens == [("COMMENT", "# hello world"), ("_NL", "\n")]


def test_block_comment_complete():
    code = "/* multi\nline */\n"
    tokens = lex(code)
    assert tokens == [("COMMENT_IN_BLOCKS", " multi\nline "), ("_NL", "\n")]


def test_block_comment_unterminated():
    code = "/* oop\n"
    lexer = Lexer(code)
    tokens = [(t.type, t.value) for t in lexer.tokens()]
    # Unterminated comment still emitted
    assert tokens == [("COMMENT_IN_BLOCKS", " oop")]
    assert lexer.errors, "Expected error list for unterminated comment"


def test_newline_counting():
    code = "a\n# c1\nb\n"
    lexer = Lexer(code)
    # Extract line numbers for newline tokens only
    nl_lines = [tok.line for tok in lexer.tokens() if tok.type == "_NL"]
    assert nl_lines == [1, 2, 3]
