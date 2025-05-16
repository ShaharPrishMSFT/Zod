import sys
import os

# Add the same sys.path modification as interpreter.py
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../../client/python")))
print("DEBUG sys.path[0]:", sys.path[0])

try:
    from FormalAiSdk.models.llm_models import LlmModels
    print("SUCCESS: Imported LlmModels from FormalAiSdk.models.llm_models")
except Exception as e:
    print("FAILURE:", type(e).__name__, e)
    raise