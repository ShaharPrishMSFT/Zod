from pathlib import Path
from typing import Dict, List, Generator
import pytest
from lark import Lark, Tree, UnexpectedInput, Token

class TestAgentLinguaExamples:
    def test_grammar_loads(self, grammar_content: str):
        """Test that the grammar can be loaded and parsed by Lark."""
        parser = Lark(grammar_content, start="start", parser="earley")
        assert isinstance(parser, Lark), "Failed to create Lark parser"

    def test_all_examples_exist(self, example_files: List[Path]):
        """Test that we have the expected example files."""
        file_names = [f.name for f in example_files]
        assert file_names, "No example files found"
        for i in range(len(file_names)):
            expected = f"{i:02d}_"
            assert any(name.startswith(expected) for name in file_names), \
                f"Missing example file with prefix {expected}"

    @pytest.mark.parametrize("example_file", [
        "00_super_simple.al",
        "01_simple_function.al",
        "02_rule_with_else.al",
        "03_rule_branches.al",
        "04_context_natural.al",
        "05_combined_module.al",
    ])
    def test_individual_examples(
        self, 
        parser: Lark,
        example_contents: Dict[str, str],
        example_file: str
    ):
        """Test each example file individually."""
        content = example_contents[example_file]
        
        try:
            tree = parser.parse(content)
            assert isinstance(tree, Tree), f"Failed to generate parse tree for {example_file}"
        except UnexpectedInput as e:
            pytest.fail(
                f"Failed to parse {example_file} at line {e.line}, col {e.column}:\n"
                f"{e.get_context(content)}"
            )
        except Exception as e:
            pytest.fail(f"Unexpected error parsing {example_file}: {str(e)}")

    def find_nodes_by_type(self, tree: Tree, node_type: str) -> Generator[Tree, None, None]:
        """Find all nodes of a specific type in the parse tree."""
        if isinstance(tree, Tree):
            if tree.data == node_type:
                yield tree
            for child in tree.children:
                if isinstance(child, Tree):
                    yield from self.find_nodes_by_type(child, node_type)

    def find_token_in_tree(self, tree: Tree, token_value: str) -> bool:
        """Search for a token with specific value in the tree."""
        if isinstance(tree, Token):
            return tree.value == token_value
        if isinstance(tree, Tree):
            return any(self.find_token_in_tree(child, token_value) for child in tree.children)
        if isinstance(tree, str):
            return tree == token_value
        return False

    def test_parse_tree_validation(
        self,
        parser: Lark,
        example_contents: Dict[str, str]
    ):
        """Test the structure of parse trees for successfully parsed examples."""
        for file_name, content in example_contents.items():
            try:
                tree = parser.parse(content)
                
                # Verify basic tree structure
                assert hasattr(tree, 'data'), f"Parse tree for {file_name} has no data attribute"
                
                # Basic validation based on file type
                if "context" in file_name:
                    assert any(
                        self.find_token_in_tree(node, "context")
                        for node in self.find_nodes_by_type(tree, "block")
                    ), f"Context file {file_name} should have a block with 'context' token"
                    
                elif "function" in file_name:
                    function_blocks = list(self.find_nodes_by_type(tree, "block"))
                    assert any(
                        self.find_token_in_tree(node, "function")
                        for node in function_blocks
                    ), f"Function file {file_name} should have a block with 'function' token"
                    
                elif "rule" in file_name:
                    assert any(
                        self.find_token_in_tree(node, "rule")
                        for node in self.find_nodes_by_type(tree, "block")
                    ), f"Rule file {file_name} should have a block with 'rule' token"
                
            except UnexpectedInput:
                # Skip validation for files that don't parse
                continue

    def test_error_reporting(self, parser: Lark, example_contents: Dict[str, str]):
        """Test that error reporting provides useful information."""
        for file_name, content in example_contents.items():
            try:
                parser.parse(content)
            except UnexpectedInput as e:
                # Verify error contains useful information
                error_context = e.get_context(content)
                assert error_context, f"No error context provided for {file_name}"
                assert e.line > 0, f"No line number in error for {file_name}"
                assert e.column >= 0, f"No column number in error for {file_name}"
                assert "^" in error_context, f"No error pointer in context for {file_name}"
