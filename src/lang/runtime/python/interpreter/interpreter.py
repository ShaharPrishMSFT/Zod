"""
AI Interpreter (Layer 1 Stub)
-----------------------------

Implements Layer 1 of the .ai interpreter as described in the live prompt design.

Layer 1 Requirements:
- Subclass BaseInterpreter to walk the parse tree.
- Implement stub methods for all major interpreter components:
    - LLM execution (run_llm_stub)
    - Context processing (process_context_stub)
    - Output handling (output_results_stub)
- All stubs have correct signatures and docstrings, but raise NotImplementedError or return dummy values.
- Code must compile and be importable, even if tests fail.

References:
- src/lang/interpeter_live_prompt.md
- src/lang/runtime/base_interpreter.py
- ModelSession: src/client/python/FormalAiSdk/sdk/session.py
- ModelFork: src/client/python/FormalAiSdk/sdk/fork.py
- Message: src/client/python/FormalAiSdk/sdk/types.py
"""

from src.lang.runtime.base_interpreter import BaseInterpreter

# Placeholder imports for SDK (update as needed)
from src.client.python.FormalAiSdk.sdk.session import ModelSession
from src.client.python.FormalAiSdk.sdk.fork import ModelFork
from src.client.python.FormalAiSdk.sdk.types import Message

class AIInterpreter(BaseInterpreter):
    """
    Layer 1 AI Interpreter for .ai files.

    Inherits from BaseInterpreter to walk the parse tree.
    Provides stubs for LLM, context, and output logic.
    """

    def __init__(self, ai_file_path: str):
        """
        Initialize the interpreter with the path to a .ai file.
        """
        super().__init__()
        self.ai_file_path = ai_file_path
        self.parser = None  # Layer 1: placeholder for compatibility with tests
        self.session = None

    def connect_parser(self):
        """
        Connect to the base parser (stub).
        """
        # Inherits parse tree walking from BaseInterpreter
        pass

    def run_llm_stub(self, *args, **kwargs):
        """
        Stub for LLM execution logic.
        Raises:
            NotImplementedError: Always, as this is a stub.
        """
        raise NotImplementedError("LLM execution is not implemented in Layer 1.")

    def process_context(self, ai_file_content: str):
        """Extracts the context identifier and content from a .ai file string using the Lark parser and the interpreter."""
        from lark import Lark
        from lark.exceptions import UnexpectedToken, UnexpectedCharacters

        # Load the grammar
        with open("src/lang/grammar/grammar.lark", "r", encoding="utf-8") as f:
            grammar = f.read()

        parser = Lark(grammar, parser="lalr", start="start")
        try:
            tree = parser.parse(ai_file_content)
        except (UnexpectedToken, UnexpectedCharacters) as e:
            raise ValueError("No context block found in .ai file.") from e
        # Walk the tree with this interpreter instance
        self.context_id = None
        self.context_content = None
        self.transform(tree)
    def context_statement(self, children):
        """
        Lark transformer method for context_statement.
        Extracts context ID and content from the parse tree.
        """
        # children: [Token('ID', ...)? , natural_inline/natural_block]
        from lark import Token

        self.context_id = None
        self.context_content = None

        if len(children) == 2:
            # context ID? (inline or block)
            if isinstance(children[0], Token) and children[0].type == "ID":
                self.context_id = str(children[0])
                content = children[1]
            else:
                content = children[0]
        else:
            content = children[0]

        # content is either a string (from natural_inline/natural_block) or a Tree
        from lark import Token
        # Handle case where content is a list of tokens (block or inline)
        if isinstance(content, list):
            text_tokens = [c.value for c in content if isinstance(c, Token) and c.type == "__ANON_1"]
            self.context_content = "\n".join(text_tokens)
        elif hasattr(content, 'children'):
            text_tokens = [c.value for c in content.children if isinstance(c, Token) and c.type == "__ANON_1"]
            self.context_content = "\n".join(text_tokens)
        else:
            if isinstance(content, Token):
                self.context_content = content.value
            else:
                self.context_content = str(content)


    @classmethod
    def from_code(cls, code: str):
        """
        Create an AIInterpreter instance from a string of .ai code.
        """
        inst = cls("<from_code>")
        inst.process_context(code)
        return inst

    @classmethod
    def from_file(cls, file_path: str):
        """
        Create an AIInterpreter instance from a .ai file on disk.
        """
        with open(file_path, "r", encoding="utf-8") as f:
            code = f.read()
        inst = cls(file_path)
        inst.process_context(code)
        return inst

    def process_context_stub(self, *args, **kwargs):
        """
        Deprecated: Use process_context instead.
        """
        raise NotImplementedError("Use process_context for context extraction.")

    def output_results_stub(self, *args, **kwargs):
        """
        Stub for output handling logic.
        Raises:
            NotImplementedError: Always, as this is a stub.
        """
        raise NotImplementedError("Output handling is not implemented in Layer 1.")