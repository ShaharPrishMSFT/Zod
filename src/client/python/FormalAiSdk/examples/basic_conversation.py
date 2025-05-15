"""
Example showing basic usage of the FormalAI SDK with unified model configuration.

Demonstrates both OpenAI and Ollama config entry points via LlmModels.
"""

from ..models.llm_models import LlmModels
from ..sdk.session import ModelSession

def main():
    # --- Example 1: Using OpenAI with env-based defaults ---
    # (Requires OPENAI_API_KEY and optionally OPENAI_MODEL in your .env)
    openai_config = LlmModels.FromOpenAi()
    openai_session = ModelSession("user", model_config=openai_config)
    openai_session.add_response("user", "Hello! Can you help me with Python programming?")
    fork = openai_session.Fork("fork1", "user", "Your message will be handled by an AI assistant.")
    fork.Answer(openai_session)
    print("\n[OpenAI] Conversation History:")
    print("--------------------")
    for msg in openai_session.messages:
        print(f"{msg.actor}: {msg.content}")
        print("--------------------")

    # --- Example 2: Using Ollama (local) ---
    ollama_config = LlmModels.From({"provider": "ollama", "model": "llama2"})
    ollama_session = ModelSession("user", model_config=ollama_config)
    ollama_session.add_response("user", "Great! How do I use a list comprehension?")
    fork = ollama_session.Fork("fork2", "user", "I will explain list comprehensions.")
    fork.Answer(ollama_session)
    print("\n[Ollama] Conversation History:")
    print("--------------------")
    for msg in ollama_session.messages:
        print(f"{msg.actor}: {msg.content}")
        print("--------------------")

if __name__ == "__main__":
    main()
