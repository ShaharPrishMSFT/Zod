# Verifies that FormalAiSdk is installed and importable as a package
try:
    from FormalAiSdk.models.llm_models import LlmModels
    print("Import successful: LlmModels found in FormalAiSdk.models.llm_models")
    # Use a static method to verify functionality
    config = LlmModels.FromOpenAi()
    print("LlmModels.FromOpenAi() output:", config)
except ImportError as e:
    print("Import failed:", e)
except Exception as ex:
    print("SDK usage failed:", ex)