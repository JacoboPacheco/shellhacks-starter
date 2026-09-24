"""
Browser-level smoke check, run by scripts/check.sh after the backend smoke test.
Loads the built frontend in headless Chromium and fails on the things lint and
build can't see: a blank page, a component crash, console errors, images with no
alt text, inputs with no label, horizontal overflow on a phone.

    python frontend/e2e/smoke.py [frontend-url]     (default http://localhost:4173)

Saves a screenshot to .claude/tmp/e2e.png (gitignored) so Claude can look at it.
"""

import os
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

URL = (sys.argv[1] if len(sys.argv) > 1 else os.getenv("E2E_URL", "http://localhost:4173")).rstrip("/")
ROOT = Path(__file__).resolve().parents[2]
SHOT = ROOT / ".claude" / "tmp" / "e2e.png"

A11Y_JS = """
() => {
  const problems = [];
  document.querySelectorAll('img').forEach((img, i) => {
    if (!img.hasAttribute('alt')) problems.push(`img #${i + 1} (${img.getAttribute('src') || 'no src'}) has no alt attribute`);
  });
  document.querySelectorAll('input, textarea, select').forEach((el) => {
    if (['hidden', 'submit', 'button'].includes(el.type)) return;
    const labelled = el.labels?.length || el.getAttribute('aria-label') || el.getAttribute('aria-labelledby');
    if (!labelled) problems.push(`${el.tagName.toLowerCase()} ${el.id ? '#' + el.id : '(no id)'} has no label`);
  });
  return problems;
}
"""

failures = []


def check(name, ok, detail=""):
    print(f"{'PASS' if ok else 'FAIL'}  {name}{'' if ok else ': ' + detail}")
    if not ok:
        failures.append(name)


with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={"width": 1280, "height": 800})
    console_errors, page_errors = [], []
    page.on("console", lambda m: console_errors.append(m.text) if m.type == "error" else None)
    page.on("pageerror", lambda e: page_errors.append(str(e)))

    page.goto(URL, wait_until="networkidle", timeout=30000)
    page.wait_for_timeout(500)

    root_text = page.inner_text("#root").strip()
    check("page rendered something", bool(root_text), "#root is empty — the app didn't mount")
    check("no component crash", "Something broke" not in root_text, "ErrorBoundary is showing: " + root_text[:200])
    check("no uncaught exceptions", not page_errors, "; ".join(page_errors)[:300])
    check("no console errors", not console_errors, "; ".join(console_errors)[:300])

    problems = page.evaluate(A11Y_JS)
    check("every image has alt text and every input has a label", not problems, "; ".join(problems)[:300])

    page.set_viewport_size({"width": 375, "height": 812})
    page.wait_for_timeout(300)
    overflow = page.evaluate("() => document.documentElement.scrollWidth - document.documentElement.clientWidth")
    check("no horizontal overflow at phone width", overflow <= 0, f"page is {overflow}px wider than a 375px screen")

    page.set_viewport_size({"width": 1280, "height": 800})
    SHOT.parent.mkdir(parents=True, exist_ok=True)
    page.screenshot(path=str(SHOT))
    browser.close()

print(f"\nscreenshot: {SHOT}")
if failures:
    print(f"{len(failures)} browser check(s) failed: {', '.join(failures)}")
    sys.exit(1)
print("All browser checks passed.")
