# TEMPORARY: Minimal LiteLLM test for Azure OpenAI (correct Azure config).
import os
import sys

try:
    from dotenv import load_dotenv
    load_dotenv(override=False)
except ImportError:
    pass

try:
    import litellm
except ImportError:
    print("ERROR: 'litellm' package is not installed. Please install it to run this check.")
    sys.exit(3)

def main():
    api_key = os.environ.get("AZURE_API_KEY")
    api_base = os.environ.get("AZURE_API_BASE")
    api_version = os.environ.get("AZURE_API_VERSION", "2025-01-01-preview")
    deployment = os.environ.get("AZURE_DEPLOYMENT_NAME")
    if not api_key:
        print("ERROR: AZURE_API_KEY not set in environment.")
        sys.exit(1)
    if not api_base:
        print("ERROR: AZURE_API_BASE not set in environment.")
        sys.exit(1)
    if not deployment:
        print("ERROR: AZURE_DEPLOYMENT_NAME not set in environment.")
        sys.exit(1)
    print(f"Using endpoint: {api_base}")
    print(f"Using deployment: {deployment}")
    print(f"Using version: {api_version}")
    try:
        if hasattr(litellm, "_turn_on_debug"):
            litellm._turn_on_debug()
            print("LiteLLM debug mode enabled.")
        # Use Azure model prefix
        response = litellm.completion(
            model=f"azure/{deployment}",
            api_key=api_key,
            api_base=api_base,
            api_version=api_version,
            messages=[{"role": "user", "content": "Hello"}]
        )
        print("SUCCESS: LiteLLM Azure call succeeded.")
        print("Response:")
        print(response)
        sys.exit(0)
    except Exception as e:
        print(f"ERROR: LiteLLM Azure call failed: {e}")
        sys.exit(2)

if __name__ == "__main__":
    main()
