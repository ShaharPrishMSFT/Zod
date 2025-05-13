import sys
import subprocess
from pathlib import Path

# Import GitSandbox from the correct path
sys.path.append(str(Path(__file__).parent / "../client/python/FormalAiSdk/tests/_util"))
from git_sandbox import GitSandbox

# Import FormalAI SDK
sys.path.append(str(Path(__file__).parent / "../client/python"))
from FormalAiSdk.models.litellm_executor import LiteLLMExecutor
from FormalAiSdk.sdk.session import ModelSession

def get_git_command_from_llm(english_instruction):
    # Initialize LLM executor and session
    executor = LiteLLMExecutor("ollama", "llama2")
    session = ModelSession("user", executor)
    # Add system prompt for CLI mapping
    session.add_response("system", (
        "You are a CLI assistant. Given an English instruction, output the corresponding git command only. "
        "Do not explain. Do not add extra text. Output only the git command."
    ))
    # Add user instruction
    session.add_response("user", english_instruction)
    # Use a fork to get the LLM's response
    fork = session.Fork("git_cmd_fork", "user", english_instruction)
    fork.Answer(session)
    # Find the latest message from the fork
    for msg in reversed(session.messages):
        if msg.actor == "git_cmd_fork":
            return msg.content.strip()
    return None

def main():
    if len(sys.argv) < 2:
        print("Usage: python git_procedure.py <english command>")
        sys.exit(1)

    english_instruction = " ".join(sys.argv[1:]).strip()
    git_cmd_str = get_git_command_from_llm(english_instruction)
    if not git_cmd_str:
        print("LLM did not return a command.")
        sys.exit(1)

    print(f"LLM mapped command: {git_cmd_str}")

    # Parse the git command string into a list for subprocess
    import shlex
    git_cmd = shlex.split(git_cmd_str)

    # Set up or use existing sandbox
    sandbox = GitSandbox().setup()
    # Ensure at least one commit exists for git status to work
    sandbox.add_sample_code().commit()

    # Run the git command in the sandbox repo, streaming output live
    proc = subprocess.Popen(
        git_cmd,
        cwd=sandbox.repo_dir,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1,
    )
    for line in proc.stdout:
        print(line, end="")
    proc.wait()

if __name__ == "__main__":
    main()
