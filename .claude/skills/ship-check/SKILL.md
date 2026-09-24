---
name: ship-check
description: Pre-demo and pre-submission readiness check. Only runs when the user types /ship-check.
disable-model-invocation: true
---

Go through each item, actually run the command where there is one, and report a short PASS/FAIL list. Fix only what's quick and safe; flag the rest.

1. `bash scripts/check.sh` passes locally.
2. The deployed pair works together: take both URLs from CLAUDE.md → Deployed (ask if not filled in), then run `SMOKE_ORIGIN=<vercel-url> backend/venv/Scripts/python backend/smoke_test.py <render-url>`. With SMOKE_ORIGIN set it also verifies CORS and that the deployed frontend was built with this backend's URL — the two most common "works locally, dead on Vercel" mistakes. A Render free-tier cold start can take 30s or more — a slow first request is not a failure. Then `backend/venv/Scripts/python backend/seed.py <render-url>` so the demo account exists on the deployed backend.
3. The deployed frontend actually works in a browser: `python frontend/e2e/smoke.py <vercel-url>` — renders, no crash, no console errors, alt text/labels, fits a phone — then look at `.claude/tmp/e2e.png`, which is now the live site. If Playwright isn't installed, open the Vercel URL in the browser tool instead.
4. `git status` is clean and the latest commit is pushed (`git status -sb` shows no "ahead").
5. README.md describes the actual project (what it is, how to run it) — not the starter template text.
6. Rules disclosure: README.md (and the Devpost writeup) states that auth/upload/deploy/CI scaffolding and the LLM helper (`llm.py`) came from a starter template the user built before the event, and names what was built during the hackathon. ShellHacks rules require documenting pre-existing and external code. If missing, draft the sentence and add it.
7. CREDITS.md lists every third-party asset (Unsplash photos, etc.), and each photo shows its credit in the UI.
8. No secrets in the repo. Both of these must print nothing:
   - `git ls-files | grep -E '(^|/)\.env$'` (a real .env file is tracked)
   - `git grep --untracked -nIE "((SECRET|KEY|TOKEN|PASSWORD)[A-Za-z_]*['\"]?[[:space:]]*[:=][[:space:]]*['\"][A-Za-z0-9_./+-]{20,}['\"]|sk-[A-Za-z0-9_-]{20,}|AIza[0-9A-Za-z_-]{30,}|gh[pous]_[A-Za-z0-9]{30,})" -- . ':!*.example' ':!scripts/' ':!**/package-lock.json'` (hardcoded key-looking values)
   If either finds something, move the value into the right `.env`, read it with `os.getenv` / `import.meta.env`, and tell the user to rotate that key since it may already be in git history.
