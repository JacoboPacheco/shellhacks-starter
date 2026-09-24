---
name: debug
description: Structured debugging when something is broken — reproduce it, read the real error, fix the root cause, add a check so it stays fixed. Use whenever a feature doesn't work, a request fails, or the page breaks.
---

Problem as reported: $ARGUMENTS
If no target was given ("it's broken"), assume the last thing you changed or the last page you showed.

Rules: no code changes until step 3. Guessing costs more time than looking.

1. **Reproduce it and capture the real error, in this order:**
   - Backend: the terminal running uvicorn (or `backend/server.log`) — the traceback names the file and line. If the backend isn't running, that's the bug: tell the user (the dev servers are theirs), or start it with `run_in_background` if they say it's down.
   - Browser: open the page in the browser tool, read the console (`read_console_messages`) and the failed request (`read_network_requests`) — the response body has FastAPI's `detail`.
   - Still nothing? `bash scripts/check.sh` — it exercises every endpoint and says which one fails.
   Quote the exact error message in your reply. If you can't reproduce it, say so and ask one AskUserQuestion with options: the page just shown (recommended) / the backend won't start / something else — paste what you see. Don't fix something you can't see.
2. **Name the cause in one sentence** before touching code. If the error mentions CORS, the `.env`, a port, or "unreachable", check the Gotchas section of CLAUDE.md first — it's usually one of those.
3. **Fix the root cause**, not the symptom. Never suppress an error, widen a `try/except`, or loosen validation to make a message go away.
4. **Prove it:** reproduce the original steps and show they pass. If the bug was in an endpoint, add a check to `backend/smoke_test.py` so `/check` catches it next time.
5. If the fix is more than a few lines, commit it per CLAUDE.md → Workflow (that rule says when the reviewer runs first), with a message saying what was broken.
