"""
Example chat application using LiteLLMExecutor with Azure OpenAI.
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
from FormalAiSdk.core.litellm_executor import LiteLLMExecutor
from FormalAiSdk.exceptions.base import ModelError, InvalidConversationError

from FormalAiSdk.models.llm_models import LlmModels

def main():
    # Build Azure config using the unified entry point (env-based by default)
    azure_config = LlmModels.From({
        "provider": "azure"
        # Optionally override with explicit values here
        # "model": "azure/my-deployment",
        # "api_key": "...",
        # "api_base": "...",
        # "api_version": "2025-01-01-preview"
    })
    print(f"DEBUG: Azure config: {azure_config}")
    executor = LiteLLMExecutor(azure_config)
    
    # Create a conversation
    conversation = Conversation()
    
    print("Chat with Azure OpenAI (type 'exit' to quit)")
    print("---------------------------------------------")
    
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
