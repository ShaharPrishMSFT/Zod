const { test, expect } = require('@playwright/test');

test.describe('Playground UI', () => {
  test('Editor initializes with minimal .al example', async ({ page }) => {
    // Capture browser console output
    page.on('console', msg => {
      console.log('BROWSER CONSOLE:', msg.type(), msg.text());
    });

    // Open the app via local HTTP server (root URL)
    await page.goto('http://localhost:4173/');

    // Log the page HTML for debugging
    const html = await page.content();
    console.log('DEBUG PAGE HTML:', html);

    // Check if CodeMirror is loaded in the browser context
    const codeMirrorType = await page.evaluate(() => typeof window.CodeMirror);
    console.log('DEBUG typeof CodeMirror:', codeMirrorType);

    // Wait for the CodeMirror editor to appear (up to 10 seconds)
    await page.waitForSelector('.CodeMirror', { timeout: 10000 });

    // Check that the editor is visible
    const editor = await page.locator('.CodeMirror');
    await expect(editor).toBeVisible();

    // Check that the editor contains the minimal .al example
    const editorText = await editor.textContent();
    expect(editorText).toContain('context');
  });
});
