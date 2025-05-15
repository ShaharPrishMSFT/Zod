# Project TODOs

This file tracks outstanding tasks and feature ideas for the FormalAI project.  
Each item includes a brief description and the date it was added.

---

## Active TODOs

- **JIT model compiler using metadata hints**  
  Implement a just-in-time model compiler that leverages metadata hints to dynamically select and match the most appropriate model for a given task or expression.  
  _Date Added: 2025-05-14_

- **Convert to a real schema instead of lark**  
  Replace the current lark-based parsing with a formal schema for better maintainability and validation.  
  _Date Added: 2025-05-13_

- **Spec out the ability to specify a set of models to run an expression in AL on, until one responds correctly**  
  Allow users to define multiple models for AL expressions, executing them sequentially until a correct response is received.  
  _Date Added: 2025-05-13_

- **Add live debugging capabilities**  
  Implement tools for real-time inspection and debugging of AL expressions and model outputs.  
  _Date Added: 2025-05-13_

- **Implement a "time machine" feature to review previous states and executions**  
  Enable users to view and step through historical states and execution logs for better traceability.  
  _Date Added: 2025-05-13_

- **Provide a way to see all context and what each LLM returned for a given expression**  
  Display the full context and all model responses for transparency and analysis.  
  _Date Added: 2025-05-13_

- **Add live prompts having a cleanup area at the bottom that gets added to**  
  Introduce a UI/UX feature where live prompts accumulate in a dedicated cleanup area at the bottom of the interface.  
  _Date Added: 2025-05-13_

- **AgentLingua Playground: Build a testable playground for AL**  
  Create an environment where users can execute, test, and iterate on `.al` code, supporting agent-friendly features and rich program metadata.  
  _Date Added: 2025-05-13_

- **Mocking the new AI language**  
  Allow the playground to mock agents and AI function calls, simulate responses for tests and debugging, and capture input/output flow for visual validation.  
  _Date Added: 2025-05-13_

- **Audit interactions in playground**  
  Capture all execution traces, track agent involvement and decisions, log inputs/outputs/errors/side effects, and support trace-based debugging and optimization.  
  _Date Added: 2025-05-13_

- **Utility wrapper for functions**  
  Provide a language primitive for wrapping user- or agent-defined methods, handling exception logging, retry suggestions, and proposing alternative implementations for self-healing/self-improving patterns.  
  _Date Added: 2025-05-13_

- **AI functions and agents as first-class language entities**  
  Support constructs like `agent my.agent`, `function suggest_alternatives`, and `contract {...}`; make agents and AI-backed functions discoverable and introspectable.  
  _Date Added: 2025-05-13_

- **Autogenerate function shells**  
  When an agent encounters a missing function or capability, propose a new function stub, fill in contract metadata, and register with context, similar to IDE "create method" features.  
  _Date Added: 2025-05-13_

- **Namespace hierarchy matches folder layout**  
  Ensure every namespace is derived from folder.folder.file.element for traceability and intuitive refactoring.  
  _Date Added: 2025-05-13_

- **Contract format spec**  
  Decide on contract format (inline or YAML-style) for AgentLingua.  
  _Date Added: 2025-05-13_

- **Multiple agent interop model**  
  Design composability and message passing for multiple agent interoperability.  
  _Date Added: 2025-05-13_

- **Error propagation and fallback logic**  
  Specify error propagation and fallback logic for robust agent execution.  
  _Date Added: 2025-05-13_

- **Test approval mechanism**  
  Define a mechanism for test approval in the playground.  
  _Date Added: 2025-05-13_

- **Self-hosting interpreter needs**  
  Identify requirements for a self-hosting interpreter for AgentLingua.  
  _Date Added: 2025-05-13_

- **Example: Using API shape for Session object with model and location resolution**  
  Create an example demonstrating how to use the API shape to pass model, location, etc., to the Session object. The example should use English to explain the desired model, and the system should resolve the most likely intended model.  
  _Date Added: 2025-05-14_

- **Make session options more expressive**  
  Modify the way options are passed into the session to allow for greater expressiveness and flexibility in configuration.  
  _Date Added: 2025-05-14_

- **Proxy LLM server protocol for direct optimization**  
  Design and implement a proxy LLM server protocol that uses LLMs to answer user questions, enabling direct optimization of responses.  
  _Date Added: 2025-05-14_

- **Mock server: embed conversation ID and support transient memory**  
  For the mock server, embed an ID at the start of each conversation and implement transient memory that is scoped to the given conversation.  
  _Date Added: 2025-05-14_

- **Pooled executors for AI usage control**  
  Implement pooled executors to manage and control the amount of AI resources being used concurrently.  
  _Date Added: 2025-05-14_

- **Hide keys and sensitive strings from LLMs using tokens**  
  Implement a mechanism to hide keys and sensitive strings from LLMs by replacing them with tokens before sending to the model. The tokens will appear in the LLM's output and can be swapped back to the correct values after processing.  
  _Date Added: 2025-05-14_

- **Pass "known" tokens to LLMs to hide actual data**  
  When communicating with an LLM, allow passing "known" tokens that mask actual data. The tokens will be returned in the LLM's output and can be replaced with the original values after processing.  
  _Date Added: 2025-05-14_
