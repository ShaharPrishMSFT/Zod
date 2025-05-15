# Process: Archiving Completed Steps

When a step is completed:
1. **Delete the full content of the completed step from `playground/viewer/liveprompt.md`, leaving only a summary line in its place.**
2. Move the full content (including heading and details) to the top of `playground/viewer/liveprompt.archive.md`.
3. Mark the step as completed in the steps list, with the completion date.
4. Commit both file changes to the current working branch.

# Steps & Completion Log

- [x] **Step 1: Problem Statement** — *Completed: 2025-05-13*
- [x] **Step 2: User Stories / Use Cases** — *Completed: 2025-05-13*
- [x] **Step 3: Requirements & Constraints** — *Completed: 2025-05-13*
- [ ] **Step 4: Initial Design / Wireframe**
- [ ] **Step 5: Implementation Plan**

**Instructions:**  
When a step is completed, move its full content (including heading and details) to `playground/viewer/liveprompt.archive.md` to keep this file focused on active work. Don't forget to delete it from this doc once moved.

---

# Live Prompt: Build a Local Graphical Flow Diagram Viewer for `.al` Files

> **Objective:**  
> Design and plan a developer-friendly HTML tool that visually represents AgentLingua (`.al`) files as interactive flow diagrams, running easily and locally in the browser.

---

## Step 2: User Stories / Use Cases
*See archive for full details. Step completed 2025-05-13.*

---

## Step 3: Requirements & Constraints
*See archive for full details. Step completed 2025-05-13.*

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
