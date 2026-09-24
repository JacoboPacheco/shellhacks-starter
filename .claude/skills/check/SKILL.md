---
name: check
description: Run every project check (frontend lint + build, backend smoke test against a live server, headless-browser check of the built app) and report pass/fail with evidence. Use before calling any feature done, and whenever the user asks if things work.
---

Run from the repo root:

```
bash scripts/check.sh
```

- Show the user the final PASSED/FAILED line and the names of anything that failed. That output is the evidence — don't summarize it as "looks good".
- Then look at `.claude/tmp/e2e.png` (Read tool) — it's the built app as a judge would see it. If it looks wrong even though the checks passed, say so.
- If something failed, fix the root cause and rerun. Never weaken a check, skip it, or edit smoke_test.py to make a failure go away unless the test itself is wrong — and say so explicitly if you believe it is.
- If you added a new backend endpoint, add a check for it to `backend/smoke_test.py` so this command keeps covering the whole app.
