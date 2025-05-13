# Playground UI Manual Test Checklist

This checklist covers all core UI features for the playground app. For each test, perform the action in the browser and verify the expected result. Record pass/fail and any notes.

---

## 1. Editor Initialization

- [ ] **Test:** Load the playground app in the browser.
  - **Expected Result:** Editor is visible and initialized with a minimal `.al` example.
  - **Notes:** Editor supports multi-line editing, indentation, undo/redo, and find/replace.

---

## 2. Open File

- [ ] **Test:** Click "Open" and select a valid `.al` file.
  - **Expected Result:** Editor loads the file content. Status message confirms successful load.

- [ ] **Test:** Click "Open" and select a non-`.al` file (e.g., `.txt`).
  - **Expected Result:** Error message or warning is shown. Editor content is unchanged.

- [ ] **Test:** Click "Open" and select an empty `.al` file.
  - **Expected Result:** Editor is cleared. Status message indicates empty file loaded.

---

## 3. Save File

- [ ] **Test:** Edit the code, then click "Save".
  - **Expected Result:** Download of a `.al` file with current editor content. Status message confirms save.

- [ ] **Test:** Click "Save" with an empty editor.
  - **Expected Result:** Download of an empty `.al` file or warning message.

---

## 4. Copy to Clipboard

- [ ] **Test:** Click "Copy" with non-empty editor content.
  - **Expected Result:** Editor content is copied to clipboard. Status message confirms copy.

- [ ] **Test:** Click "Copy" with empty editor.
  - **Expected Result:** Clipboard is cleared or warning message shown.

---

## 5. Status Messages

- [ ] **Test:** Perform Open, Save, and Copy actions.
  - **Expected Result:** Appropriate status messages appear for each action (success, error, warning).

---

## 6. Responsive Layout

- [ ] **Test:** Resize browser window to small and large sizes.
  - **Expected Result:** Editor and output panels adjust layout (horizontal split on large screens, tabbed panels on small screens).

---

## 7. Error Handling

- [ ] **Test:** Attempt to open a corrupted or very large `.al` file.
  - **Expected Result:** Error message is shown. App remains responsive.

---

## 8. Undo/Redo

- [ ] **Test:** Make changes in the editor, use undo/redo shortcuts or buttons.
  - **Expected Result:** Editor correctly undoes/redoes changes.

---

## 9. Find/Replace

- [ ] **Test:** Use find/replace functionality in the editor.
  - **Expected Result:** Can search and replace text within the editor.

---

## 10. Edge Cases

- [ ] **Test:** Rapidly perform Open/Save/Copy actions in succession.
  - **Expected Result:** App remains stable, no crashes or unexpected behavior.

---

**Instructions:**  
- For each test, mark as Pass/Fail and add notes as needed.
- If a test fails, document the issue for follow-up.
