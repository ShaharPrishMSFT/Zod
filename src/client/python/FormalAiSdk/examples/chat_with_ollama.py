"""
Example chat application using LiteLLMExecutor with Ollama.
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

# Load .env if present
try:
    from dotenv import load_dotenv
    load_dotenv(override=True)
except ImportError:
    pass

from FormalAiSdk.core.types import Conversation, Role
from FormalAiSdk.models.litellm_executor import LiteLLMExecutor
from FormalAiSdk.exceptions.base import ModelError, InvalidConversationError

def main():
    # Initialize the executor with Ollama
    # Note: Assumes Ollama is running locally with tinyllama model
    executor = LiteLLMExecutor("ollama", "tinyllama")

    # Create a conversation
    conversation = Conversation()

    print("Chat with Ollama (type 'exit' to quit)")
    print("--------------------------------------")

    while True:
        # Get user input
        user_input = input("\nYou: ").strip()

        # Check for exit
        if user_input.lower() == 'exit':
            break

        try:
            # Add user message to conversation (returns new Conversation)
            conversation = conversation.add_message(Role.CLIENT, user_input)

            # Get model response
            response = executor.execute(conversation)

            # Add response to conversation history (returns new Conversation)
            conversation = conversation.add_message(Role.AGENT, response.content)

            # Display response
            print(f"\nAssistant: {response.content}")

        except (ModelError, InvalidConversationError) as e:
            print(f"\nError: {str(e)}")
            continue
        except KeyboardInterrupt:
            print("\nExiting...")
            break

if __name__ == "__main__":
    main()
