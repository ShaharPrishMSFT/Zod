import pytest
from .parser import AgentLinguaParser, ParserError, ContextNode, NaturalBlockNode, TextNode
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

def test_parse_ast_context_block():
    source = (
        "# Comment\n"
        "context my.agent\n"
        "--begin\n"
        "Hello world\n"
        "--end\n"
    )
    parser = AgentLinguaParser()
    # Print the Lark parse tree for debugging
    tree = parser.parse(source)
    print(tree.pretty())
    ast_nodes = parser.parse_ast(source)
    # Should return a list with one ContextNode
    assert isinstance(ast_nodes, list)
    assert len(ast_nodes) == 1
    ctx = ast_nodes[0]
    assert isinstance(ctx, ContextNode)
    assert ctx.name == "my.agent"
    assert isinstance(ctx.body, NaturalBlockNode)
    # The natural block should contain a list of TextNode(s)
    content = ctx.body.content
    print("AST content nodes:", [n.text for n in content if isinstance(n, TextNode)])
    # Print the repr of the natural_content node's children for debugging
    tree = parser.parse(source)
    for node in tree.iter_subtrees():
        if node.data == "natural_content":
            print("natural_content children repr:", [repr(child) for child in node.children])
    assert any(isinstance(n, TextNode) and "Hello world" in n.text for n in content)
