import os
from pathlib import Path

def load_project_env():
    """
    Loads the .env file from the project root, regardless of the current working directory.
    Searches upwards from this file's location for a .env file.
    """
    current = Path(__file__).resolve()
    for parent in [current] + list(current.parents):
        env_path = parent / ".env"
        if env_path.exists():
            try:
                from dotenv import load_dotenv
                load_dotenv(dotenv_path=env_path, override=True)
                print(f"[env.py] Loaded .env from: {env_path}")
            except ImportError:
                print("[env.py] python-dotenv is not installed.")
            return
    print("[env.py] WARNING: .env file not found in any parent directory.")
