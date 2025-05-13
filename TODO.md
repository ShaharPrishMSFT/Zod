# Project TODOs

This file tracks outstanding tasks and feature ideas for the FormalAI project.  
Each item includes a brief description and the date it was added.

---

## Active TODOs

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
