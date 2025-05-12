import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "../src/client/python"))
from FormalAiSdk.models.litellm_executor import LiteLLMExecutor
from FormalAiSdk.sdk.session import ModelSession

def discovery(input_text: str) -> str:
    """
    Discovery procedure that interacts with the Ollama LLM to process input text
    and includes the procedures.json file content as context.

    Args:
        input_text (str): The plain text input to process.

    Returns:
        str: The response from the LLM.
    """
    # Initialize the executor and session
    executor = LiteLLMExecutor("ollama", "tinyllama")
    session = ModelSession("user", executor)

    # Read the procedures.json file
    import os
    procedures_path = os.path.join(os.path.dirname(__file__), "procedures.json")
    with open(procedures_path, "r") as file:
        procedures_content = file.read()

    # Add the input text and procedures content to the session

    combined_prompt = f"You will be provided with a json formatted list of procedures, you need to use the user input provided to respond with a natural english answer. Procedures:\n{procedures_content}\n\nUser Input:\n{input_text}"

    print("****************")
    print(combined_prompt)
    print("****************")


    session.add_response("user", combined_prompt)

    # Create a fork and get the response
    fork = session.Fork("discovery_fork", "user", combined_prompt)
    fork.Answer(session)

    # Retrieve and return the response
    for msg in session.messages:
        if msg.actor == "discovery_fork":
            return msg.content

    return "No response received from the LLM."

if __name__ == "__main__":
    import sys
    input_text = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else "tell me what procedures you have"
    result = discovery(input_text)
    print(result)
