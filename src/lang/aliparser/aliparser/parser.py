from pathlib import Path
from lark import Lark, Tree, UnexpectedInput, UnexpectedToken
from typing import Optional, Union

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
