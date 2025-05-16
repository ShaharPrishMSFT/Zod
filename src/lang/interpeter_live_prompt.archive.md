# ARCHIVED: Simple .ai Interpreter Design (Live Prompt)

This file is an archive of the live prompt before moving to Layer 2. And it mostly just needs to include the step. No need for other info.

---


## Layer 1: Parser Connection & Stubs

- Connect to the base parser (import and instantiate, but do not process input yet).
- Implement stub methods for all major interpreter components:
  - LLM execution (e.g., `run_llm_stub`)
  - Context processing (e.g., `process_context_stub`)
  - Output handling (e.g., `output_results_stub`)
- All stubs should have correct signatures and docstrings, but raise `NotImplementedError` or return dummy values.
- Ensure the code compiles and can be imported, even if tests fail.

