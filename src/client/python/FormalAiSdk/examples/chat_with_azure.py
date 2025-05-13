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
from FormalAiSdk.models.litellm_executor import LiteLLMExecutor
from FormalAiSdk.exceptions import ModelError, InvalidConversationError

def main():
    # Initialize the executor with Azure OpenAI
    deployment = os.environ.get("AZURE_DEPLOYMENT_NAME", "gpt-4.1")
    api_key = os.environ.get("AZURE_API_KEY")
    api_base = os.environ.get("AZURE_API_BASE")
    api_version = os.environ.get("AZURE_API_VERSION", "2025-01-01-preview")
    print(f"DEBUG: AZURE_DEPLOYMENT_NAME={deployment}")
    print(f"DEBUG: AZURE_API_KEY={'set' if api_key else 'MISSING'}")
    print(f"DEBUG: AZURE_API_BASE={api_base}")
    print(f"DEBUG: AZURE_API_VERSION={api_version}")
    executor = LiteLLMExecutor("azure", deployment)
    
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
