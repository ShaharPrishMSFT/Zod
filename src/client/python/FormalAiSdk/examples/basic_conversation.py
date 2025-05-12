"""
Example showing basic usage of the FormalAI SDK.
"""

from ..models.litellm_executor import LiteLLMExecutor
from ..sdk.session import ModelSession

def main():
    # Initialize the executor (using Ollama for this example)
    executor = LiteLLMExecutor("ollama", "llama2")
    
    # Create a session for our conversation
    session = ModelSession("user", executor)
    
    # Add a user message
    session.add_response("user", "Hello! Can you help me with Python programming?")
    
    # Create a fork to get model response
    fork = session.Fork("fork1", "user", "Your message will be handled by an AI assistant.")
    fork.Answer(session)
    
    # Add another user message
    session.add_response("user", "Great! How do I use a list comprehension?")
    
    # Create another fork for the response
    fork = session.Fork("fork2", "user", "I will explain list comprehensions.")
    fork.Answer(session)
    
    # Print the conversation
    print("\nConversation History:")
    print("--------------------")
    for msg in session.messages:
        print(f"{msg.actor}: {msg.content}")
        print("--------------------")

if __name__ == "__main__":
    main()
