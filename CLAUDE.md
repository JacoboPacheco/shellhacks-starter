# Project: [NAME]

You're a great engineer and this team is lucky to have you on this build — let's ship something judges remember.

## Idea
[One paragraph: what it does, who it's for, why it's interesting to a judge in 30 seconds.]

## Sponsor / company challenges to target
[Pasted at Phase 0 — name, sponsor, their actual eligibility requirement; `/spec` trims it to what the idea fits.]
- [ ]

## Stack
FastAPI (backend; SQLite locally, Postgres on Render), React + Vite (frontend), Render + Vercel (deploy) — change only if the idea truly needs something else.
- APIs/keys needed: [list them]

## Scope (hackathon-realistic)
Must have (demo breaks without these — tick each in the commit that finishes it):
- [ ]

Nice to have (in cut order):
- [ ]

Explicitly NOT doing:
- [ ]

## Phases
Every session starts with PLAYBOOK.md → "Knowing where we are", before anything else. When I say I'm leaving or going to sleep, reread PLAYBOOK → Away mode and follow it instead of asking.

## Commands
Shell commands go through the Bash tool (Git Bash); the permission allowlist is written for it.
- Verify everything: `bash scripts/check.sh` (or `/check`) — lint, build, backend smoke test, headless-browser check, and `demo_path.py` once it exists. Self-contained on :8765/:4173; the dev servers needn't be running. Give it a 600000 ms Bash timeout.
- The dev servers are the human's (`.\dev.ps1`). If you must start one, use `run_in_background` — a foreground server blocks the Bash tool. Backend: `cd backend && venv/Scripts/python -m uvicorn main:app --reload --port 8000`. Frontend: `cd frontend && npm run dev` (:5173, proxies `/api` and `/uploads` to :8000).
- New dependency: `cd frontend && npm install <pkg>` / `cd backend && venv/Scripts/pip install <pkg>` (both allowlisted), then add the Python one to `requirements.txt` yourself — pip doesn't.
- Browser checks and screenshots: the `webapp-testing` skill (Python Playwright, installed). Write scripts to `.claude/tmp/` and run them as `python .claude/tmp/<name>.py` (allowlisted) against http://localhost:5173 when the dev servers are up; when they're down, its `with_server.py` starts them — write the backend command with backslashes: `'cd backend && venv\Scripts\python -m uvicorn main:app --port 8000'` (cmd.exe). Live debugging of a page: the browser tool if this session has one, else a Playwright script that prints console messages and failed responses.
- Deployed: `backend/venv/Scripts/python backend/smoke_test.py <render-url> <vercel-url>` tests the deployed pair (CORS, build URL, every endpoint); `backend/venv/Scripts/python backend/seed.py <render-url>` creates the demo account + data there.

## Timeline
- Kickoff (K): [fill at kickoff, e.g. 2026-09-25 19:00 local]
- Hacking ends (E): [from the schedule, e.g. 2026-09-27 07:00 local]
- Milestone 1, walking skeleton working end to end: K + 10h
- Feature freeze: E − 3h
`date` in Bash gives the real time.

## Deployed
- Render (backend): [paste URL after deploying — DEPLOY.md section 1]
- Vercel (frontend): [paste URL — DEPLOY.md section 2]

## How this codebase is wired — follow these patterns
- Keep the frontend thin: it fetches and renders; logic and validation live in the Python backend. No router, state library, TypeScript, or Tailwind unless the idea can't work without it.
- All frontend→backend calls go through `frontend/src/api.js` (`api`, `login`, `signup`, `uploadFile`, `ask`, `assetUrl`). Never call `fetch` directly.
- No login screen by default. Per-person state (saves, likes, history) is keyed to the demo account: `VITE_DEMO_EMAIL`/`VITE_DEMO_PASSWORD` in `frontend/.env` (matching `backend/seed.py`) make `useAuth` sign in on load, so `Depends(get_current_user)` keeps working with no screen — never move per-user logic into localStorage. Only a true multi-user idea renders `<AuthForm login={login} signup={signup} />` when `user` is null (tested; reuse, don't rebuild).
- New backend feature = new router module shaped like `backend/uploads.py`, then `app.include_router(...)` in `main.py`. Protect routes with `Depends(get_current_user)` from `auth.py`; rate-limit public POSTs with `@limiter.limit("N/minute")` (the handler needs a `request: Request` param). Every new endpoint gets a check in `backend/smoke_test.py`.
- Tables go in `backend/models.py`, created on startup. If you changed it, the dev server's old `backend/app.db` will 500 with "no such column" — the last non-question line of the turn is "Delete `backend/app.db` and restart the backend".
- Demo data goes in `seed_project_data` in `backend/seed.py`, via the API. It runs on every `/check` and every `seed.py <render-url>`, so it must be idempotent: check before creating.
- AI calls: `from llm import complete` → `await complete(prompt, system=..., json_mode=True, fallback=FALLBACK, image=(bytes, "image/png"))`. `POST /api/ai/ask` in `llm.py` is the example route: copy both of its limit decorators onto every AI route — the per-visitor one and the shared `AI_DAILY_LIMIT` one, which is the only thing protecting the free quota. `fallback=` is mandatory on the demo path; the route returns `"fallback": text == FALLBACK` (pattern in `complete`'s docstring) and the UI badges it. Without `GEMINI_API_KEY` every call returns a clear 503 — build the feature anyway.
- A new API key: name it in the matching `.env.example`, build the feature anyway, and at the end of the turn that builds it ask me to paste the key into `backend/.env` (if I paste it in chat, write it there yourself, nowhere else); then tell me to restart the backend (`.env` isn't hot-reloaded) and, if deployed, to add it in Render → Environment.

## Standards (on by default, don't ask each time)
- Secrets stay in `.env`, never hardcoded or committed
- Validate any upload by its actual bytes (see `uploads.py`) and any user input hitting the database
- Every input has a `<label>`, every image has `alt` text, no page wider than a phone

## How to read me
I talk loosely on purpose. I have a specific picture in my head; your job is to find it and build *that*, not the generic version — and asking well is how you find it.
- Start every request by restating it in one line: "Reading that as: …". Confident → build. Something I'll see or feel (a page, a flow, the wow moment) → ask first only when the plausible readings differ in what the demo shows *and* switching later would be expensive; otherwise build the recommended reading, show it, name the alternative.
- Ask with AskUserQuestion: 2–4 specific questions, concrete options, your recommendation first — never a bare "what do you mean?". I may not have words for what I'm picturing; options with examples ("a feed / a grid / a map") let me point. An ask-first turn still shows something — a screenshot of the current page or a rough wireframe per option.
- Ask about vision, not trivia. Vision: what a user sees first, the demo's best moment, list vs map vs feed, who it's for, what it must never do. Trivia you decide: names, copy, colors, spacing, empty states, error messages — I'll say if I don't like them.
- When I react ("this feels off", "no, not like that"): screenshot the current state, check it against the `frontend-design` skill's list of AI-looking tells, offer 2–3 specific guesses at what's bothering me, let me pick, fix.
- "Make it look better / nicer / pop / professional": the `frontend-design` skill, briefed with the Idea, the audience, and Decisions. Apply the direction to the whole page, screenshot, offer one contrasting alternative as a one-message switch. Once the app has a direction, reuse it everywhere without asking.
- Several requests in one message: restate all, build the unambiguous ones now, ask about the ambiguous ones in a single AskUserQuestion, continue.
- A feature request, or one bigger than Scope: build the smallest version that captures it and say what you left out. The exceptions are PLAYBOOK's: before milestone 1 (Phase 2) and after feature freeze (Phase 5).
- Every turn ends with something I can see — a screenshot, a running page, a `/check` result — plus at most one AskUserQuestion call.

## Workflow
- Mid-event feature: plan in one paragraph — table, endpoints, where it appears in the UI, acceptance check — append it to SPEC.md, build.
- Build order: walking skeleton first (PLAYBOOK Phase 2), then iterate — never breadth-first.
- Done means evidence: `/check` green and you looked at `.claude/tmp/e2e.png`; if something can't be verified, say so.
- Scope guard at every commit: Current status vs Scope vs the hours left. If the must-haves won't fit, say so now and demote per PLAYBOOK's rule for the current phase (in Phase 2, only past K+10) — don't wait to be asked.
- A sponsor I name: fetch its current API docs first (never build from memory), ask one AskUserQuestion with 2–3 places it would do real work in the demo, and wait; then build it behind an env var with a graceful "not configured" state (PLAYBOOK Phase 3 says when).
- Changes touching auth, data, or security: run the `reviewer` agent on the uncommitted diff before committing and fix what it finds. Don't use subagents for routine building.
- Commit after each feature that works, one commit per feature. Before each commit, rewrite `## Current status` and append new confirmed answers to `## Decisions`, so they land in that commit. After each commit, `git status -sb`; at `ahead 2` or more, `git push` (until PLAYBOOK Phase 5 says stop).
- 3 hours or fewer left until E, or I say judging starts within 3 hours: PLAYBOOK Phase 5.
- The same fix has failed twice: stop, say so, write what you tried and learned into `## Current status`, commit it, then ask me to `/clear` — and say if a bigger `/model` is worth it. (Alone: PLAYBOOK → Away mode.)
- When compacting context, preserve: the feature in progress and its acceptance check, working vs broken, files changed since the last commit, and any command that failed and why.

## Budget
Prompts may arrive with "Budget right now: …". Don't change how you work because of it: 5-hour past 85% or weekly past 70% → say so once, with the reset time when the hook gives one, before the turn's work; a limit about to hit mid-feature → commit and push what's safe first.

## Gotchas
- Uploaded files are stored in the database and served at `/uploads/<name>`; wrap them with `assetUrl()` in the frontend, never hardcode a host. 5MB max each.
- Frontend env vars must start with `VITE_`; changing `.env` needs a dev-server restart.
- "Something broke" on a page is the ErrorBoundary catching a component crash — the text under it is the real error.
- Render runs Postgres, local is SQLite: don't write SQLite-only SQL.
- Per-IP rate limits are per-venue. Keep limits ≥ 30/minute.
- The backend mirrors every request and traceback to `backend/server.log` — read it for server errors.
- `git restore .` / `git checkout .` / `git reset --hard` are denied. To drop uncommitted work, ask me to rewind (Esc Esc) or run it myself.
- [add project-specific gotchas here as you hit them]

## Decisions
[Confirmed answers about how the app looks and behaves — layout, the wow moment, design direction, what it must never do. Append, don't rewrite.]

## Current status
PHASE: 0 — repo just generated, SPEC.md doesn't exist yet
deployed: no
[Line 1 is always `PHASE: n — reason`, line 2 `deployed: yes/no`; then, when they apply, one per line: `DO FIRST: …`, `BLOCKED: …`, `WAITING ON YOU: …`, `LATER: …` (PLAYBOOK says when); then working / broken / in progress + its acceptance check.]
