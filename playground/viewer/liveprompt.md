# Steps & Completion Log

- [x] **Step 1: Problem Statement** — *Completed: 2025-05-13*
- [ ] **Step 2: User Stories / Use Cases**
- [ ] **Step 3: Requirements & Constraints**
- [ ] **Step 4: Initial Design / Wireframe**
- [ ] **Step 5: Implementation Plan**

**Instructions:**  
When a step is completed, move its full content (including heading and details) to `playground/viewer/liveprompt.archive.md` to keep this file focused on active work.

---

# Live Prompt: Build a Local Graphical Flow Diagram Viewer for `.al` Files

> **Objective:**  
> Design and plan a developer-friendly HTML tool that visually represents AgentLingua (`.al`) files as interactive flow diagrams, running easily and locally in the browser.

---

## Step 1: Problem Statement

**Problem Statement:**  
AgentLingua (`.al`) source files define agent logic and structure, but are currently only accessible as code—making it difficult for developers and users to quickly grasp their flow, relationships, and logic at a glance.

To address this, we will build a local, graphical flow diagram viewer that:
- Allows developers and users to visually inspect `.al` files, seeing contexts, functions, rules, and their relationships as an interactive flow diagram.
- Runs as a single HTML file, easily opened in any browser with no server or build step required.
- Helps users move from code-centric to visual understanding, supporting exploration, learning, and debugging of AgentLingua programs.

This tool will emphasize rapid prototyping and experimentation, with clear documentation of objectives and lessons learned as we iterate.
---

## Step 2: User Stories / Use Cases

**List the main user stories or use cases.**  
- As a developer, I want to open an `.al` file in my browser and see its structure as a flow diagram.
- As a user, I want to drag-and-drop or select an `.al` file to visualize it.
- As a developer, I want to see nodes for contexts, functions, rules, and their relationships (edges).
- As a user, I want to interact with the diagram (e.g., zoom, pan, click nodes for details).
- (Optional/future) As a user, I want to export the diagram or share a snapshot.

---

## Step 3: Requirements & Constraints

**Define the requirements and constraints for the viewer.**  
- Must be a single HTML file (with embedded JS/CSS) for easy local use.
- No server or build step required; should work by double-clicking or opening in browser.
- Support for loading `.al` files via file picker and/or drag-and-drop.
- Parse `.al` files according to AgentLingua grammar (see `src/lang/grammar/grammar.peg`).
- Render a flow diagram showing contexts, functions, rules, and their relationships.
- Interactive UI: zoom, pan, and node selection.
- No code editing features.
- No external dependencies unless loaded via CDN (e.g., D3.js, Mermaid, or similar for diagrams).

---

## Step 4: Initial Design / Wireframe

**Sketch or describe the initial UI and component structure.**  
- **Header:** Title and brief instructions.
- **File Input:** Button or drag-and-drop area to load `.al` files.
- **Diagram Area:**  
  - Displays the parsed `.al` file as an interactive flow diagram.
  - Nodes represent contexts, functions, rules; edges show relationships.
  - Support for zooming, panning, and clicking nodes for more info.
- **Footer:** Credits, links, or additional instructions.

```
+------------------------------------------------------+
| AgentLingua .al Flow Diagram Viewer                  |
| [Select File]  or  [Drag & Drop Area]                |
+------------------------------------------------------+
| [ Interactive flow diagram appears here ]            |
|   (nodes: context, function, rule, etc.)             |
|   (edges: relationships, calls, dependencies)        |
+------------------------------------------------------+
| [Zoom] [Pan] [About]                                 |
+------------------------------------------------------+
```

---

*Continue to Step 5: Implementation Plan once the above steps are reviewed and refined.*
