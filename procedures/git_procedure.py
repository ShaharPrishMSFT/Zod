import sys
import subprocess
import time
from pathlib import Path

# Import GitSandbox from the correct path
GIT_SANDBOX_PATH = (Path(__file__).parent / "../src/client/python/FormalAiSdk/tests/_util").resolve()
sys.path.insert(0, str(GIT_SANDBOX_PATH))
import tempfile
from git_sandbox import GitSandbox

# Import FormalAI SDK
SDK_PATH = (Path(__file__).parent / "../src/client/python").resolve()
sys.path.insert(0, str(SDK_PATH))
from FormalAiSdk.models.litellm_executor import LiteLLMExecutor
from FormalAiSdk.sdk.session import ModelSession

import argparse

def get_git_command_from_llm(english_instruction):
    # Initialize LLM executor and session
    executor = LiteLLMExecutor("ollama", "mistral")
    session = ModelSession("user", executor)
    # Add system prompt for CLI mapping
    session.add_response("system", (
        "You are a CLI assistant. Given an English instruction, output the corresponding git command only. "
        "Do not explain. Do not add extra text. Output only the git command. Do not number your response. Do not repeat the command."
    ))
    # Add user instruction
    session.add_response("user", english_instruction)
    # Use a fork to get the LLM's response
    fork = session.Fork("git_cmd_fork", "user", english_instruction)
    fork.Answer(session)
    # Find the latest message from the fork
    for msg in reversed(session.messages):
        if msg.actor == "git_cmd_fork":
            # Extract only the first line, strip numbering and extra text
            lines = msg.content.strip().splitlines()
            for line in lines:
                # Remove leading numbering (e.g., "1. git status")
                line = line.strip()
                if line and "git " in line:
                    # Remove any leading numbering or punctuation
                    line = line.lstrip("0123456789. )-")
                    # Only take up to the first semicolon or newline
                    line = line.split(";")[0].strip()
                    return line
            # Fallback: return the whole content
            return msg.content.strip()
    return None

def main():
    overall_start = time.time()
    parser = argparse.ArgumentParser(description="LLM-powered English-to-git CLI agent")
    parser.add_argument("--print-only", action="store_true", help="Only print the mapped git command, do not execute it")
    parser.add_argument("--repo", type=str, help="Path to an existing git repo to use (for testing)")
    parser.add_argument("--capture-output", action="store_true", help="Print only the output of the git command (for test harnesses)")
    parser.add_argument("instruction", nargs="+", help="English instruction to map to git command")
    args = parser.parse_args()

    english_instruction = " ".join(args.instruction).strip()
    git_cmd_str = get_git_command_from_llm(english_instruction)
    if not git_cmd_str:
        print("LLM did not return a command.", file=sys.stderr)
        # Debug: print session messages if available
        try:
            from FormalAiSdk.sdk.session import ModelSession
            print("Debug: LLM session messages:", file=sys.stderr)
            print(getattr(ModelSession, "messages", "No session messages attribute"), file=sys.stderr)
        except Exception as e:
            print(f"Debug: Could not print session messages: {e}", file=sys.stderr)
        sys.exit(1)

    if args.print_only:
        print(git_cmd_str)
        sys.exit(0)

    print(f"LLM mapped command: {git_cmd_str}", file=sys.stderr)

    # Parse the git command string into a list for subprocess
    import shlex
    git_cmd = shlex.split(git_cmd_str)

    def run_and_time_git_command(cmd, cwd, capture_output=False):
        import sys
        print(f"[Timing] Running: {' '.join(cmd)}", file=sys.stderr)
        start = time.time()
        if capture_output:
            proc = subprocess.run(
                cmd,
                cwd=cwd,
                capture_output=True,
                text=True,
                check=False,
            )
            print(proc.stdout, end="")
            end = time.time()
            print(f"[Timing] Command took {end - start:.3f} seconds", file=sys.stderr)
            return proc.returncode
        else:
            proc = subprocess.Popen(
                cmd,
                cwd=cwd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1,
            )
            for line in proc.stdout:
                print(line, end="")
            proc.wait()
            end = time.time()
            print(f"[Timing] Command took {end - start:.3f} seconds", file=sys.stderr)
            return proc.returncode

    if args.repo:
        repo_dir = Path(args.repo)
        if not (repo_dir / ".git").exists():
            print(f"Provided repo path {repo_dir} is not a git repository.")
            sys.exit(1)
        run_and_time_git_command(git_cmd, repo_dir, capture_output=args.capture_output)
    else:
        # Set up or use existing sandbox in a temp directory
        with tempfile.TemporaryDirectory() as tmpdir:
            sandbox = GitSandbox(root_dir=tmpdir).setup()
            # Ensure at least one commit exists for git status to work
            sandbox.add_sample_code().commit()

            # Run the git command in the sandbox repo, streaming output live
            run_and_time_git_command(git_cmd, sandbox.repo_dir, capture_output=args.capture_output)

    overall_end = time.time()
    print(f"[Timing] Total playground session took {overall_end - overall_start:.3f} seconds", file=sys.stderr)

if __name__ == "__main__":
    main()
