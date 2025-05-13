# Self-Evolving Agentic Prompt — OpenAI Model Support via LiteLLM

<!--- COMPLETED-STEP SUMMARIES (append most salient take-aways, pitfalls, key decisions) --->
<!-- Example: 1. OpenAI model support is best handled through LiteLLM; avoid redundant direct integration. -->
1. LiteLLMExecutor supports OpenAI models; dependencies are up to date; all required OpenAI features are accessible via LiteLLM.
2. OpenAI-related tests are opt-in only (require RUN_OPENAI_TESTS=1), expanded to cover both basic and error scenarios, ensuring robust and safe test coverage.
---

## Progress Tracker

* 1. Review LiteLLMExecutor OpenAI support and dependencies ... [[STEP-1 STATUS: DONE (2025-05-13)]]
* 2. Ensure OpenAI model configuration and credentials are handled via LiteLLM ... [[STEP-2 STATUS: DONE (2025-05-13)]]
* 3. Create unified model configuration entry points (`LlmModels.FromOpenAi`, `LlmModels.From`) with env-based defaults and tests ... [[STEP-3 STATUS: PENDING]]
* 4. Update and expand tests for OpenAI usage through LiteLLM ... [[STEP-4 STATUS: DONE (2025-05-13)]]
* 5. Document OpenAI model usage via LiteLLM in SDK docs and examples ... [[STEP-5 STATUS: PENDING]]
* 6. Review CI pipeline for OpenAI/LiteLLM coverage ... [[STEP-6 STATUS: PENDING]]

When a step is finished, replace its `PENDING` with `DONE (yyyy-mm-dd)` and copy the full step block to `prompt.archive.md`.

---

## How the Agent Evolves

1. Read this prompt top-to-bottom.
2. Execute the next `PENDING` step; edit code in review-sized chunks (complex code => smaller diffs).
3. Update this file:
   * Move finished step(s) to archive, keep only their key take-aways above.
   * Mark step status.
   * Maintain the Technical Index at exactly 10 high-value items (drop the least useful).
4. If execution restarts, resume from the first `PENDING` step.
5. Repeat until all steps are `DONE`.

---

### Technical Index (max 10 items)

1. [LiteLLM Documentation](https://github.com/BerriAI/litellm)
2. [Executor Interface Spec](../core/executor.py)
3. [ModelSession Usage](../sdk/session.py)
4. [Security: Handling API Keys](https://platform.openai.com/docs/guides/authentication)
5. [Test Suite Example](../tests/test_litellm_executor.py)
6. [CI Pipeline Config](../../../../.github/workflows/)
7. [Error Handling Patterns](../exceptions/)
8. [SDK Example Usage](../examples/chat_with_ollama.py)
9. [FormalAI Trunk/Fork Architecture](../core/types.py)
10. [OpenAI Model List](https://platform.openai.com/docs/models)

---

### Important Paths / Files

* LiteLLM executor implementation   -> src/client/python/FormalAiSdk/models/litellm_executor.py
* Executor interface               -> src/client/python/FormalAiSdk/core/executor.py
* Model session                    -> src/client/python/FormalAiSdk/sdk/session.py
* Tests                            -> src/client/python/FormalAiSdk/tests/
* CI pipeline                      -> .github/workflows/
* Documentation                    -> docs/python/
* Usage examples                   -> src/client/python/FormalAiSdk/examples/

---

### Current Step Bodies

#### 3. Create unified model configuration entry points (`LlmModels.FromOpenAi`, `LlmModels.From`) with env-based defaults and tests

* Implement `LlmModels.FromOpenAi(openai_config)` to create model configs for OpenAI, with defaults that pull from environment variables (e.g., `OPENAI_API_KEY`, `OPENAI_MODEL`, etc.).
* Implement `LlmModels.From(litellm_config)` for generic LiteLLM config, also with sensible env-based defaults.
* Ensure both methods provide a clear, documented interface for model configuration.
* Add/expand tests to verify correct config loading, env fallback, and error handling for both entry points.

#### 4. Update and expand tests for OpenAI usage through LiteLLM

* Add/expand unit tests for OpenAI model usage via LiteLLMExecutor.
* Ensure test coverage for key OpenAI features.
* Replace obvious `TODO:`s; log remaining ones in `issues.md`.

#### 5. Document OpenAI model usage via LiteLLM in SDK docs and examples

* Update SDK documentation to show OpenAI usage through LiteLLM.
* Add or update example scripts.
* Update technical index and project snapshot.

#### 6. Review CI pipeline for OpenAI/LiteLLM coverage

* Ensure CI runs all relevant tests for OpenAI via LiteLLM.
* Document any CI-specific configuration for OpenAI credentials.

---

```mermaid
flowchart TD
    A[Start / Restart] --> B{Next pending step?}
    B -- no --> Z[All steps DONE]
    B -- yes --> C[Execute step N]
    C --> D[Commit & PR (review-sized)]
    D --> E[Update prompt: status, summary, tech index]
    E --> B
```

---

## Project Snapshot (terse)

> OpenAI model support is provided via LiteLLMExecutor, ensuring unified configuration, robust test coverage, and clear documentation. No redundant direct OpenAI integration is maintained.

---

Follow the process, keep diffs tidy, value practicality over dogma.
