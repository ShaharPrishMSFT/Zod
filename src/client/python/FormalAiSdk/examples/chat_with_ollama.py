"""
Example chat application using LiteLLMExecutor with Ollama.
"""

from ..core.types import Conversation, Role
from ..models.litellm_executor import LiteLLMExecutor
from ..exceptions import ModelError, InvalidConversationError

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
            # Add user message to conversation
            conversation.add_message(Role.CLIENT, user_input)
            
            # Get model response
            response = executor.execute(conversation)
            
            # Add response to conversation history
            conversation.messages.append(response)
            
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
