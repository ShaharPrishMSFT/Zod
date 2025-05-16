# Simple .ai Interpreter Design (Live Prompt)
## Current Status

| Layer    | Status        | Notes                        |
|----------|--------------|------------------------------|
| Layer 1  | Complete     | Parser connected, stubs done |
| Layer 2  | Complete     | Context processing implemented and tested |
| Layer 3  | Not Started  |                              |
| Layer 4  | Not Started  |                              |

This design describes a layered interpreter for `.ai` files, leveraging the FormalAI SDK infrastructure in [`src/client/python/FormalAiSdk/sdk/`](../client/python/FormalAiSdk/sdk/).

## High-Level Rules for the Agent

The bot must strictly maintain the structure, instructions, and formatting of the file at all times.

1. **One File, Markdown Only** – Write or update exactly one `.md` file.
2. **Immutable Sections** – Anything *outside* the explicitly editable fields is *frozen*; never alter wording, order, or formatting elsewhere.
3. **Editable Fields** – The agent may update **only**:

   * `Current Status` section (every field inside it).
   * Each step’s `Progress` sub-field.
4. **Protected Blocks** – Text wrapped in:

   ```
   <!-- protected -->
   ...content...
   <!-- end protected -->
   ```

   is absolutely read-only. Do **not** add, delete, or change anything inside those markers.
5. **Persistence** – Always load the existing file (do *not* start over), then save edits in place.

<!-- protected -->
...content...
<!-- end protected -->

is absolutely read-only. Do not add, delete, or change anything inside those markers.

Persistence – Always load the existing file (do not start over), then save edits in place.

---

## Layered Implementation Plan

This interpreter should be built in seven steps, each corresponding to a development milestone:

- **Step 1:** Connect to the base parser, but do nothing else. Provide stub methods for LLM and all other logic so the code compiles, even if tests fail.
- **Step 2:** Implement context processing.
- **Step 3:** Integrate LLM calls.
- **Step 4:** Connect context and LLM calls. At this point, context tests should pass.

---

## Step 5: Implement if statements

- Implement support for the if statements. 
- This includes conditonals
- Ensure each statement type is parsed, represented in the interpreter, and executed according to its semantics.
- Add/adjust tests to verify correct handling and execution of each statement type.

## Step 6: Implement Runtime Contract

- Define a contract (interface or abstract base class) for runtimes that the interpreter can use.
- The contract should specify the methods and behaviors required for any runtime implementation (e.g., execute, handle input/output, manage state).
- Refactor the interpreter to interact with runtimes only through this contract, allowing for pluggable runtime implementations.
- Document the contract and provide example usage.

## Step 7: Implement Terminal Runtime

- Implement a terminal runtime that executes when the interpreter is run in a console environment.
- This runtime should handle user input/output via the terminal, display results, and support interactive execution.
- Ensure the terminal runtime adheres to the runtime contract/interface.
- Add tests or manual usage examples to verify terminal execution works as intended.

---

## Layered Architecture

```mermaid
flowchart TD
    A[Parse .ai File] --> B[Create ModelSession]
    B --> C[Add Initial Messages]
    C --> D[Create Fork(s) for Execution]
    D --> E[ModelExecutor Runs]
    E --> F[Collect & Output Results]
```

---

## How to Use the Live Prompt

This section explains how to use the live prompt interpreter to execute `.ai` files using the FormalAI SDK.

### Basic Usage Example

```python
from FormalAiSdk.models.litellm_executor import LiteLLMExecutor
from FormalAiSdk.sdk.session import ModelSession

# Initialize with Ollama
executor = LiteLLMExecutor("ollama", "llama2")
session = ModelSession("user", executor)

# Add user message
session.add_response("user", "What is Python?")

# Get AI response through a fork
fork = session.Fork("fork1", "user", "Explain Python programming language")
fork.Answer(session)

# View conversation
for msg in session.messages:
    print(f"{msg.actor}: {msg.content}")
```

- Replace the message content and fork logic as needed for your `.ai` file.
- For advanced usage (parallel forks, multi-actor, integration), see [SDK Usage Examples](../../docs/python/sdk/examples.md).

---


## Layer 3: LLM Integration

- Implement the LLM execution logic, replacing the stub with real calls to the FormalAI SDK (e.g., using `ModelSession`, `ModelFork`).
- Ensure LLM calls can be made with the current context and input.
- Add/adjust tests to verify LLM call integration.

## Layer 4: Context + LLM Integration

- Connect context processing and LLM execution so that context is used in LLM calls.
- Ensure the interpreter produces correct results using both context and LLM.
- At this stage, context-related tests should pass.

---

## Example Flow

1. **Parse**: Load `.ai` file, extract messages.
2. **Session**: `session = ModelSession(actor, executor)`
3. **Add Messages**: `session.add_response(actor, content)` for each message.
4. **Fork**: `fork = session.Fork(fork_id, from_actor, message)`
5. **Execute**: `fork.Answer(session)`
6. **Output**: Iterate over `session.messages` for results.

---

## References

- [SDK Usage Examples](../../docs/python/sdk/examples.md)
- [`ModelSession`](../client/python/FormalAiSdk/sdk/session.py)
- [`ModelFork`](../client/python/FormalAiSdk/sdk/fork.py)
- [`Message`](../client/python/FormalAiSdk/sdk/types.py)

---

## Notes

- Each layer is independent and testable.
- Forks allow for parallel or isolated execution paths.
- The interpreter can be extended for advanced features (e.g., multi-actor, branching).