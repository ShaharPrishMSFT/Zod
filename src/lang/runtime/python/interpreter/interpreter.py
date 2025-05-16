from FormalAiSdk.core.litellm_executor import LiteLLMExecutor
from FormalAiSdk.core.openai_executor import OpenAIExecutor
from FormalAiSdk.sdk.session import ModelSession
from FormalAiSdk.models.llm_models import LlmModels
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
from FormalAiSdk.sdk.fork import ModelFork
from FormalAiSdk.sdk.types import Message

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

    def run_llm(self, prompt=None, model_name="ollama", model_variant="phi3:mini"):
        """
        Executes an LLM call using the FormalAI SDK3
        Uses the current context as the initial message.
        Args:
            prompt (str, optional): The prompt to send to the LLM. If None, uses self.context_content.
            model_name (str): The backend to use (default: "ollama").
            model_variant (str): The model to use (default: "phi3:mini").
        Returns:
            list: List of message dicts from the session.
        """
        if not hasattr(self, "context_content") or self.context_content is None:
            raise ValueError("No context content available for LLM execution.")

        # Use the correct LlmModels static methods for config
        if model_name == "openai":
            model_config = LlmModels.FromOpenAi()
        elif model_name == "ollama":
            # For Ollama, model string must be "ollama/modelname"
            model_str = f"ollama/{model_variant}"
            model_config = LlmModels.From({"provider": "ollama", "model": model_str})
        else:
            model_config = LlmModels.From({"provider": model_name, "model": model_variant})

        # TODO: Bug - this will always use litellm
        executor = LiteLLMExecutor(model_config)
        self.session = ModelSession("user", model_config, executor)
        # Add context as the first message
        self.session.add_response("user", self.context_content)
        # Use provided prompt or context as the fork message
        fork_message = prompt if prompt is not None else self.context_content
        fork = self.session.Fork("fork1", "user", fork_message)
        fork.Answer(self.session)
        return [ {"actor": msg.actor, "content": msg.content} for msg in self.session.messages ]

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
        # If content is a Tree or has children, interpret it
        if hasattr(content, 'children') or hasattr(content, 'data'):
            result = self.transform(content)
            # If the result is None, set to empty string
            self.context_content = result if result is not None else ""
        elif isinstance(content, list):
            text_tokens = [c.value for c in content if isinstance(c, Token) and c.type == "__ANON_1"]
            self.context_content = "\n".join(text_tokens)
        else:
            if isinstance(content, Token):
                self.context_content = content.value
            else:
                self.context_content = str(content)


    def if_statement(self, children):
        """
        Lark transformer method for if_statement.
        Uses LLM to evaluate the condition and executes the block if LLM returns "yes".
        Raises error if LLM does not return "yes" or "no".
        """
        # children: [condition, block]
        condition = children[0]
        block = children[1]
        instruction = (
            "IMPORTANT: Answer with exactly one word, either 'yes' or 'no', and nothing else. "
            "Your answer must reflect the truth of the following statement to the best of your knowledge."
        )
        prompt = f"{instruction}\n\n{str(condition)}"
        llm_result = self.run_llm(prompt=prompt)
        answer = llm_result[-1]["content"].strip().lower() if llm_result else ""
        if answer == "yes":
            return self.transform(block)
        elif answer == "no":
            return None
        else:
            raise ValueError(f"LLM response must be 'yes' or 'no', got: '{answer}'")

    def if_else_statement(self, children):
        """
        Lark transformer method for if_else_statement.
        Uses LLM to evaluate the condition and executes the correct block.
        Raises error if LLM does not return "yes" or "no".
        """
        # children: [condition, if_block, else_clause]
        condition = children[0]
        if_block = children[1]
        else_clause = children[2]
        instruction = (
            "IMPORTANT: Answer with exactly one word, either 'yes' or 'no', and nothing else. "
            "Your answer must reflect the truth of the following statement to the best of your knowledge."
        )
        prompt = f"{instruction}\n\n{str(condition)}"
        llm_result = self.run_llm(prompt=prompt)
        answer = llm_result[-1]["content"].strip().lower() if llm_result else ""
        if answer == "yes":
            return self.transform(if_block)
        elif answer == "no":
            return self.transform(else_clause)
        else:
            raise ValueError(f"LLM response must be 'yes' or 'no', got: '{answer}'")

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
