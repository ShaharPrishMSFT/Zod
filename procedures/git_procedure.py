"""
git_procedure.py - LLM-powered English-to-git CLI agent

USAGE:
    python procedures/git_procedure.py "Delete the branch 'feature-x'"
    python procedures/git_procedure.py --smart "Show me all commits made by Alice in the last 2 weeks."
    python procedures/git_procedure.py --no-local "Create a new branch called hotfix and push it to origin"
    python procedures/git_procedure.py --log-stages --smart "Find all files changed in the last 3 commits"

OPTIONS:
    --smart         Retry with OpenAI GPT-4.1-nano if the first model fails
    --no-local      Only print the mapped git command, do not execute it
    --log-stages    Enable detailed stage logging and run the mapped command

NOTES:
- The tool assumes the current working directory is a git repository unless otherwise specified in the instruction.
- All answers are generated by the LLM; no hardcoded mappings or fallbacks are used.

EXAMPLES:
    python procedures/git_procedure.py "git status"
    python procedures/git_procedure.py --smart "Delete the branch 'feature-x'"
    python procedures/git_procedure.py --no-local "Create a new branch called hotfix and push it to origin"
    python procedures/git_procedure.py --log-stages --smart "Find all files changed in the last 3 commits"
"""

import sys
import subprocess
import time
from pathlib import Path

# Import FormalAI SDK
SDK_PATH = (Path(__file__).parent / "../src/client/python").resolve()
sys.path.insert(0, str(SDK_PATH))
from FormalAiSdk.core.litellm_executor import LiteLLMExecutor
from FormalAiSdk.core.openai_executor import OpenAIExecutor
from FormalAiSdk.sdk.session import ModelSession
from FormalAiSdk.models.llm_models import LlmModels

import argparse
import os

# Load environment variables from .env if present
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

def stage_log(stage, message, enabled):
    if enabled:
        print(f"[STAGE: {stage}] {message}", file=sys.stderr)

# --- BEGIN KNOWLEDGE BASES ---

# Basic Git knowledge base for small model
BASIC_GIT_KB = """
Git Command-Line Quick Reference

Setup:
  git config --global user.name "Your Name"
  git config --global user.email "your@email.com"
  git init
  git clone <url>

Working with Changes:
  git status
  git add <file>
  git commit -m "message"
  git diff

Branching:
  git branch
  git checkout <branch>
  git checkout -b <new-branch>
  git merge <branch>

Remotes:
  git remote add origin <url>
  git fetch origin
  git pull origin main
  git push origin main

History:
  git log --oneline --graph
  git show HEAD~1

Undo:
  git reset --soft HEAD~1
  git revert <commit>
  git commit --amend
  git checkout -- <file>
"""

# Full Git cheat sheet for smart model (from deletethis.md)
FULL_GIT_KB = """
Git Cheat Sheet (Command-Line Only)

Setup and Configuration:
  git config --global user.name "Alice"
  git config --global user.email "alice@example.com"
  git config --global color.ui auto
  git init my-repo
  cd my-repo
  git clone https://github.com/user/repo.git

Working with Changes:
  git status
  git add file1.txt file2.txt
  git diff
  git diff --staged
  git commit -m "Implement new feature"

Branching and Merging:
  git branch -a
  git branch feature-x
  git checkout feature-x
  git checkout -b hotfix
  git merge main

Remote Repositories:
  git remote add origin https://github.com/user/repo.git
  git fetch origin
  git pull origin main
  git push origin main
  git push --tags

Inspecting History:
  git log --oneline --graph
  git log -p
  git reflog
  git show HEAD~1

Undoing and Rewriting History:
  git reset --soft HEAD~1
  git reset --hard HEAD~1
  git revert abc123
  git commit --amend
  git checkout -- file.txt

Stashing Changes:
  git stash
  git stash list
  git stash apply stash@{0}
  git stash pop
  git stash drop stash@{0}

Conflict Resolution:
  git merge feature-branch
  # resolve conflicts, edit files, git add, git commit
  git merge --abort
  git rebase --abort
"""

# --- END KNOWLEDGE BASES ---

def call_llm_model(model_type, model_name, system_prompt, instruction, log_stages, stage_prefix):
    stage_log(f"before_llm_{stage_prefix}", f"Preparing system prompt for {stage_prefix} model:\n{system_prompt}", log_stages)
    if model_type == "openai":
        llm_model = LlmModels.FromOpenAi()
        executor = OpenAIExecutor()
    else:
        llm_model = LlmModels.From()
        executor = LiteLLMExecutor(llm_model)
    session = ModelSession("user", executor)
    session.add_response("system", system_prompt)
    session.add_response("user", instruction)
    stage_log(f"after_llm_{stage_prefix}", f"Prompt sent to {stage_prefix} model. Awaiting response...", log_stages)
    fork = session.Fork("git_cmd_fork", "user", instruction)
    fork.Answer(session)
    for msg in reversed(session.messages):
        if msg.actor == "git_cmd_fork":
            lines = msg.content.strip().splitlines()
            for line in lines:
                line = line.strip()
                if line and "git " in line:
                    line = line.lstrip("0123456789. )-")
                    line = line.split(";")[0].strip()
                    stage_log(f"after_llm_{stage_prefix}", f"{stage_prefix.capitalize()} model returned: {line}", log_stages)
                    return line
            stage_log(f"after_llm_{stage_prefix}", f"{stage_prefix.capitalize()} model returned: {msg.content.strip()}", log_stages)
            return msg.content.strip()
    return None

def get_git_command_from_llm(english_instruction, smart_mode=False, log_stages=False, no_local=False):
    """
    Returns the git command string mapped from the English instruction using the LLM.
    If --no-local is set, only the smart model is called.
    If --smart is set (without --no-local), local is tried first, then smart as fallback.
    Otherwise, only the local model is called.
    """
    if no_local:
        # Only call the smart model
        system_prompt_smart = (
            FULL_GIT_KB
            + "\n\nYou are a CLI assistant and a git expert. Given an English instruction, output the corresponding git command only. "
            "Do not explain. Do not add extra text. Output only the git command. Do not number your response. Do not repeat the command."
        )
        return call_llm_model("openai", "gpt-4.1-nano", system_prompt_smart, english_instruction, log_stages, "smart")
    if smart_mode:
        # Try local, then smart if local fails
        system_prompt_small = (
            BASIC_GIT_KB
            + "\n\nYou are a CLI assistant. Given an English instruction, output the corresponding git command only. "
            "Do not explain. Do not add extra text. Output only the git command. Do not number your response. Do not repeat the command."
        )
        result = call_llm_model("ollama", os.environ.get("OPENAI_MODEL", "phi3"), system_prompt_small, english_instruction, log_stages, "small")
        if result:
            return result
        system_prompt_smart = (
            FULL_GIT_KB
            + "\n\nYou are a CLI assistant and a git expert. Given an English instruction, output the corresponding git command only. "
            "Do not explain. Do not add extra text. Output only the git command. Do not number your response. Do not repeat the command."
        )
        return call_llm_model("openai", "gpt-4.1-nano", system_prompt_smart, english_instruction, log_stages, "smart")
    # Only local model
    system_prompt_small = (
        BASIC_GIT_KB
        + "\n\nYou are a CLI assistant. Given an English instruction, output the corresponding git command only. "
        "Do not explain. Do not add extra text. Output only the git command. Do not number your response. Do not repeat the command."
    )
    return call_llm_model("ollama", os.environ.get("OPENAI_MODEL", "phi3"), system_prompt_small, english_instruction, log_stages, "small")

def main():
    parser = argparse.ArgumentParser(description="LLM-powered English-to-git CLI agent")
    parser.add_argument("--smart", action="store_true", help="Retry with OpenAI GPT-4.1-nano if the first model fails")
    parser.add_argument("--no-local", action="store_true", help="Only call the smart model and print the mapped git command")
    parser.add_argument("--log-stages", action="store_true", help="Enable detailed stage logging")
    # Added for test harness compatibility; ignored by script logic
    parser.add_argument("--capture-output", action="store_true", help="(Test harness) Ignored")
    parser.add_argument("--repo", type=str, default=None, help="(Test harness) Ignored")
    parser.add_argument("instruction", nargs="+", help="English instruction to map to git command")
    args = parser.parse_args()

    english_instruction = " ".join(args.instruction).strip()
    git_cmd_str = get_git_command_from_llm(
        english_instruction,
        smart_mode=args.smart,
        log_stages=args.log_stages,
        no_local=args.no_local
    )
    if not git_cmd_str:
        stage_log("error", "LLM did not return a command.", args.log_stages)
        if args.smart or args.no_local:
            stage_log("error", "Tried both ollama/mistral and OpenAI GPT-4.1-nano, but no command was returned.", args.log_stages)
        sys.exit(1)

    # Always print the mapped command to stdout
    print(git_cmd_str)

    # No git execution code remains in the script

if __name__ == "__main__":
    main()
