import pytest
from .parser import AgentLinguaParser, ParserError
from lark import Tree

def test_parse_simple_context_block():
    source = (
        "# Comment\n"
        "context my.agent\n"
        "--begin\n"
        "Hello world\n"
        "--end\n"
    )
    parser = AgentLinguaParser()
    tree = parser.parse(source)
    assert isinstance(tree, Tree)
    # Accept either 'start' or 'formal_decl_block' as the root, depending on grammar flattening
    assert tree.data in ("start", "formal_decl_block")
