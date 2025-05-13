from pathlib import Path
from lark import Lark, Tree, UnexpectedInput, UnexpectedToken, Token
from typing import Optional, Union, List, Any

class ParserError(Exception):
    """Custom exception for parser errors with context."""
    def __init__(self, message: str, line: Optional[int] = None, column: Optional[int] = None, context: Optional[str] = None):
        super().__init__(message)
        self.line = line
        self.column = column
        self.context = context

    def __str__(self):
        base = super().__str__()
        if self.line is not None and self.column is not None:
            base += f" (line {self.line}, column {self.column})"
        if self.context:
            base += f"\nContext:\n{self.context}"
        return base

# AST Node Classes

class ASTNode:
    pass

class ContextNode(ASTNode):
    def __init__(self, name: Optional[str], body: Any):
        self.name = name
        self.body = body  # Usually a NaturalBlockNode or similar

class NaturalBlockNode(ASTNode):
    def __init__(self, content: List[Any]):
        self.content = content  # List of TextNode or embedded formal nodes

class TextNode(ASTNode):
    def __init__(self, text: str):
        self.text = text

class AgentLinguaParser:
    """
    Lark-based parser for AgentLingua using PEG grammar.
    Loads grammar from src/lang/grammar/grammar.peg.
    """

    def __init__(self, grammar_path: Optional[Union[str, Path]] = None):
        if grammar_path is None:
            # Default to grammar file relative to this file
            grammar_path = Path(__file__).parent.parent.parent / "grammar" / "grammar.peg"
        else:
            grammar_path = Path(grammar_path)
        with open(grammar_path, "r", encoding="utf-8") as f:
            grammar = f.read()
        self.lark = Lark(grammar, start="start", parser="earley")

    def parse(self, source: str) -> Tree:
        """
        Parse AgentLingua source code from a string.
        Returns a Lark parse tree.
        Raises ParserError on failure.
        """
        try:
            return self.lark.parse(source)
        except UnexpectedToken as e:
            raise ParserError(
                f"Unexpected token: {e.token}",
                line=e.line,
                column=e.column,
                context=e.get_context(source)
            ) from e
        except UnexpectedInput as e:
            raise ParserError(
                "Unexpected input",
                line=getattr(e, "line", None),
                column=getattr(e, "column", None),
                context=e.get_context(source) if hasattr(e, "get_context") else None
            ) from e
        except Exception as e:
            raise ParserError(f"Parser error: {str(e)}") from e

    def parse_file(self, file_path: Union[str, Path]) -> Tree:
        """
        Parse AgentLingua source code from a file.
        Returns a Lark parse tree.
        Raises ParserError on failure.
        """
        file_path = Path(file_path)
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
        return self.parse(content)

    def parse_ast(self, source: str) -> List[ASTNode]:
        """
        Parse AgentLingua source and return a list of top-level AST nodes.
        """
        tree = self.parse(source)
        result = self._tree_to_ast(tree)
        # Always return a list at the top level
        if isinstance(result, list):
            return result
        elif result is not None:
            return [result]
        else:
            return []

    def _tree_to_ast(self, tree) -> List[ASTNode]:
        """
        Convert Lark parse tree to a list of AST nodes.
        Only handles context blocks and natural blocks for now.
        """
        print("DEBUG _tree_to_ast visiting:", getattr(tree, "data", None))
        nodes = []
        if tree.data == "start":
            for child in tree.children:
                node = self._tree_to_ast(child)
                if node:
                    if isinstance(node, list):
                        nodes.extend(node)
                    else:
                        nodes.append(node)
        elif tree.data == "formal_decl_block":
            # Find context declaration
            for child in tree.children:
                if hasattr(child, "data") and child.data == "formal_decl_stripped":
                    # child: formal_decl_stripped
                    name = None
                    body = None
                    print("DEBUG formal_decl_stripped children:", [(type(sub), repr(sub)) for sub in child.children])
                    for sub in child.children:
                        if isinstance(sub, Token) and sub.type == "ID":
                            name = str(sub)
                        elif hasattr(sub, "data"):
                            print("DEBUG recursing into:", sub.data)
                            result = self._tree_to_ast(sub)
                            # If result is a list, search for a NaturalBlockNode
                            if isinstance(result, list):
                                def find_nb(lst):
                                    for n in lst:
                                        if isinstance(n, NaturalBlockNode):
                                            return n
                                        elif isinstance(n, list):
                                            found = find_nb(n)
                                            if found:
                                                return found
                                    return None
                                nb = find_nb(result)
                                if nb is not None:
                                    body = nb
                                else:
                                    body = result
                            elif isinstance(result, NaturalBlockNode):
                                body = result
                            else:
                                body = result
                    if body is None:
                        body = NaturalBlockNode([])
                    return ContextNode(name, body)
        elif tree.data == "any_expr_in_formal":
            # Recurse into all children and return the first non-None result
            for child in tree.children:
                result = self._tree_to_ast(child)
                if result:
                    return result
            return None
        elif tree.data == "any_block_body":
            # Descend into any_block_body_stripped
            for child in tree.children:
                if hasattr(child, "data") and child.data == "any_block_body_stripped":
                    result = self._tree_to_ast(child)
                    if isinstance(result, list):
                        nb = next((n for n in result if isinstance(n, NaturalBlockNode)), None)
                        if nb is not None:
                            return nb
                        # If all elements are TextNode or result is empty, wrap in NaturalBlockNode
                        if all(isinstance(n, TextNode) for n in result) or not result:
                            return NaturalBlockNode(result)
                    elif isinstance(result, NaturalBlockNode):
                        return result
            return NaturalBlockNode([]) if result is None else None
        elif tree.data == "any_block_body_stripped":
            # Descend into natural_block_stripped or formal_block_stripped
            for child in tree.children:
                if hasattr(child, "data") and child.data in ("natural_block_stripped", "formal_block_stripped"):
                    result = self._tree_to_ast(child)
                    if isinstance(result, list):
                        nb = next((n for n in result if isinstance(n, NaturalBlockNode)), None)
                        if nb is not None:
                            return nb
                        # If all elements are TextNode, wrap in NaturalBlockNode
                        if all(isinstance(n, TextNode) for n in result) and result:
                            return NaturalBlockNode(result)
                    elif isinstance(result, NaturalBlockNode):
                        return result
            return NaturalBlockNode([]) if result is None else None
        elif tree.data == "natural_block":
            # child: natural_block_stripped
            for child in tree.children:
                if hasattr(child, "data") and child.data == "natural_block_stripped":
                    return self._tree_to_ast(child)
        elif tree.data == "natural_block_stripped":
            # children: NAT_BEGIN, _NL, natural_content, _NL, NAT_END, _NL?
            found_content = False
            for sub in tree.children:
                if hasattr(sub, "data") and sub.data == "natural_content":
                    content = self._tree_to_ast(sub)
                    found_content = True
                    if content is None or content == []:
                        # If content is empty, join all Token values as text
                        text = "".join(s.value for s in sub.children if isinstance(s, Token))
                        if text:
                            return NaturalBlockNode([TextNode(text)])
                        else:
                            return NaturalBlockNode([])
                    if isinstance(content, list):
                        return NaturalBlockNode(content)
                    else:
                        return NaturalBlockNode([content])
            if not found_content:
                # Fallback: join all Token values as text
                text = "".join(sub.value for sub in tree.children if isinstance(sub, Token))
                if text:
                    return NaturalBlockNode([TextNode(text)])
                else:
                    return NaturalBlockNode([])
        elif tree.data == "natural_content":
            # children: TEXT_CHAR, _NL, WS, or formal_expr_in_natural
            text = ""
            for sub in tree.children:
                if isinstance(sub, Token):
                    text += sub.value  # Preserve all token values, including whitespace and newlines
                elif isinstance(sub, str):
                    text += sub
            print("DEBUG natural_content joined text:", repr(text))
            if text:
                return [TextNode(text)]
            else:
                return []
        return None
