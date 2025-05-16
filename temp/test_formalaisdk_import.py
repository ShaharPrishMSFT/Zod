# Verifies that FormalAiSdk is installed and importable as a package

try:
    from FormalAiSdk.models.llm_models import LlmModels
    print("Import successful: LlmModels found in FormalAiSdk.models.llm_models")
except ImportError as e:
    print("Import failed:", e)