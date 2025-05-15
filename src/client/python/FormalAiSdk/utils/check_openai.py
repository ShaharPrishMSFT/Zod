import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

import os
from env import load_project_env

# Load environment variables from the project root .env
load_project_env()

import openai

def main():
    api_key = os.getenv("OPENAI_API_KEY")
    api_base = os.getenv("OPENAI_API_BASE")
    api_version = os.getenv("OPENAI_API_VERSION")
    deployment = os.getenv("OPENAI_MODEL")  # For Azure, this is the deployment name
    prompt = "Say hello from the minimal OpenAI check utility."

    if not api_key or not api_base or not deployment:
        print("Missing required environment variables. Please check your .env file.")
        print(f"OPENAI_API_KEY={api_key}")
        print(f"OPENAI_API_BASE={api_base}")
        print(f"OPENAI_MODEL={deployment}")
        return

    # Detect if this is an Azure endpoint
    is_azure = "azure" in api_base

    try:
        if is_azure:
            client = openai.AzureOpenAI(
                api_key=api_key,
                api_version=api_version,
                azure_endpoint=api_base
            )
            response = client.chat.completions.create(
                model=deployment,
                messages=[{"role": "user", "content": prompt}],
            )
        else:
            client = openai.OpenAI(api_key=api_key, base_url=api_base)
            response = client.chat.completions.create(
                model=deployment,
                messages=[{"role": "user", "content": prompt}],
            )
        print("OpenAI API response:")
        print(response)
    except Exception as e:
        print("Error communicating with OpenAI API:")
        print(e)

if __name__ == "__main__":
    main()
