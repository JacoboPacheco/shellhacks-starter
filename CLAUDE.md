# Project: [NAME]

You're a great engineer and this team is lucky to have you on this build — let's ship something judges remember.

## Idea
[One paragraph: what it does, who it's for, why it's interesting to a judge in 30 seconds. Run /spec to fill this in properly.]

## Sponsor / company challenges to target
[From the event's sponsor list at kickoff — name, sponsor, their actual eligibility requirement. Leave out ones that don't naturally fit.]
- [ ]

## Stack
FastAPI + SQLite (backend), React + Vite (frontend), Render + Vercel (deploy) — change only if the idea truly needs something else.
- APIs/keys needed: [list them, and add each to the matching .env.example]

## Scope (hackathon-realistic)
Must have (demo breaks without these):
- [ ]

Nice to have (cut first if time runs out):
- [ ]

Explicitly NOT doing:
- [ ]

## Commands
Run shell commands with the Bash tool (Git Bash), not PowerShell — everything here is bash syntax and the permission allowlist is written for Bash.
- Verify everything: `bash scripts/check.sh` (or `/check`) — lint, build, live backend smoke test. Self-contained (own server on :8765), so this is how you test; you don't need the dev servers running.
- The dev servers are the human's: they run `.\dev.ps1` (or two VS Code terminals) and keep them up. If you must start one yourself, run it in the background (`run_in_background`) — a foreground `uvicorn`/`npm run dev` blocks the Bash tool until it times out.
  - Backend: `cd backend && venv/Scripts/python -m uvicorn main:app --reload --port 8000`
  - Frontend: `cd frontend && npm run dev` (http://localhost:5173, proxies `/api` and `/uploads` to :8000)
- Check the deployed backend: `SMOKE_BASE_URL=<render-url> backend/venv/Scripts/python backend/smoke_test.py`

## Deployed
- Render (backend): [paste URL after deploying — DEPLOY.md section 1]
- Vercel (frontend): [paste URL — DEPLOY.md section 2]

## How this codebase is wired — follow these patterns
- All frontend→backend calls go through `frontend/src/api.js` (`api`, `login`, `signup`, `uploadFile`, `assetUrl`). Don't call `fetch` directly.
- If the idea needs accounts: `const { user, loading, login, signup, logout } = useAuth()` from `frontend/src/useAuth.js`, and render `<AuthForm login={login} signup={signup} />` when `user` is null. Already tested end to end — reuse it, don't rebuild auth UI.
- New backend feature = new router module shaped like `backend/uploads.py`, then `app.include_router(...)` in `main.py`. Protect routes with `Depends(get_current_user)` from `auth.py`. Rate-limit public POSTs with `@limiter.limit("N/minute")` (the handler needs a `request: Request` param).
- Tables go in `backend/models.py` and are created on startup.
- Every new endpoint gets a check in `backend/smoke_test.py`, so `/check` keeps covering the whole app.

## Standards (keep these on by default, don't ask each time)
- Secrets stay in `.env`, never hardcoded or committed
- Validate any upload by its actual bytes (see `uploads.py`) and any user input hitting the database
- Auth: use the existing `auth.py`; never hand-roll password storage
- Every input has a `<label>`, every image has `alt` text
- Rate limit public POST endpoints

## Workflow
- For a new idea or big feature: `/spec` first. For anything touching more than one file: plan briefly. For a one-line fix, just do it.
- When planning, point out which sponsor challenges the idea realistically qualifies for and the smallest addition that would qualify it for another — never force a fit.
- Don't claim a feature is done without evidence: run `/check` and show the result. If something can't be verified, say so.
- Before calling a nontrivial feature done: `/check`, then the `reviewer` agent on the uncommitted diff, fix what it finds, **then** commit. (Review before commit — after a commit the diff is empty.) Don't use subagents for routine building; they start with no memory of the conversation.
- Commit after each feature that works (small commits, message says what now works). The commit history is our evidence the project was built during the event — never batch a whole day into one commit. Remind me to push every few hours.
- If you've corrected the same mistake twice, stop — `/clear` and restate the task with what you learned.
- When something's broken, use `/debug`: reproduce and read the actual error (server log, browser console) before changing code.
- When compacting context, preserve: the feature in progress and its acceptance check, what's working vs broken, the files changed since the last commit, and any command that failed and why.
- Photos: as the last step of a turn where pages got finished and `/check` passed, run the `images` skill — place your best picks, then ask me once to confirm or swap. Never mid-feature, and never block on my answer.

## Gotchas
- SQLite `create_all` never alters existing tables: after changing a model's columns, stop the backend and delete `backend/app.db` (dev data is disposable).
- Uploaded files are served at `/uploads/<name>`; in the frontend wrap them with `assetUrl()`, never hardcode a host.
- Frontend env vars must start with `VITE_`; changing `.env` needs a dev-server restart.
- Windows venv python is `venv/Scripts/python`, not `venv/bin/python`.
- A page showing "Something broke" is the ErrorBoundary catching a component crash — the text under it is the real error message; the full stack is in the browser console.
- Render free tier wipes the disk on redeploy/restart — SQLite data and uploads don't survive. Fine for a demo.
- [add project-specific gotchas here as you hit them]

## Current status
[Update as you go — what's working, what's broken, what you're mid-way through.]
