# TEMPORARY: Utility for verifying OpenAI/LiteLLM config. Remove after step 2 is complete.
import os
import sys

# Load .env if present
try:
    from dotenv import load_dotenv
    load_dotenv(override=False)  # Do not override existing env vars
except ImportError:
    pass  # If python-dotenv is not installed, skip loading .env

try:
    import litellm
except ImportError:
    print("ERROR: 'litellm' package is not installed. Please install it to run this check.")
    sys.exit(3)

def main():
    api_key = os.environ.get("OPENAI_API_KEY")
    api_base = os.environ.get("OPENAI_API_BASE")
    model = os.environ.get("OPENAI_MODEL", "gpt-3.5-turbo")
    if not api_key:
        print("ERROR: OPENAI_API_KEY not set in environment.")
        sys.exit(1)
    print(f"Using model: {model}")
    if api_base:
        print(f"Using custom endpoint: {api_base}")
    else:
        print("Using default OpenAI endpoint.")
    try:
        # Enable LiteLLM debug mode for detailed output
        if hasattr(litellm, "_turn_on_debug"):
            litellm._turn_on_debug()
            print("LiteLLM debug mode enabled.")
        # Attempt a minimal OpenAI call via LiteLLM
        response = litellm.completion(
            model=model,
            messages=[{"role": "user", "content": "Hello"}]
        )
        print("SUCCESS: LiteLLM can access OpenAI model and credentials are valid.")
        sys.exit(0)
    except Exception as e:
        print(f"ERROR: LiteLLM/OpenAI check failed: {e}")
        print("If you see a NotFoundError, check that your API key is valid and has access to the requested model.")
        print("You can set a different model by setting the OPENAI_MODEL environment variable.")
        print("LiteLLM debug mode was enabled for detailed output above.")
        sys.exit(2)

if __name__ == "__main__":
    main()
