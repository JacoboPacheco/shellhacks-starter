# Project: [NAME]

You're a great engineer and this team is lucky to have you on this build — let's ship something judges remember.

## Idea
[One paragraph: what it does, who it's for, why it's interesting to a judge in 30 seconds. /spec fills this in.]

## Sponsor / company challenges to target
[From the event's sponsor list at kickoff — name, sponsor, their actual eligibility requirement. Leave out ones that don't naturally fit.]
- [ ]

## Stack
FastAPI (backend; SQLite locally, Postgres on Render), React + Vite (frontend), Render + Vercel (deploy) — change only if the idea truly needs something else.
- APIs/keys needed: [list them, and add each to the matching .env.example]

## Scope (hackathon-realistic)
Must have (demo breaks without these — tick each in the commit that finishes it):
- [ ]

Nice to have (in cut order):
- [ ]

Explicitly NOT doing:
- [ ]

## Phases
PLAYBOOK.md is the stage-by-stage plan for the event. Every session starts with its "Knowing where we are" section, before anything else. It owns what to build, cut, and refuse in each phase; this file owns the rules for every turn.

## Commands
Shell commands go through the Bash tool (Git Bash) — everything here is bash syntax and the permission allowlist is written for it.
- Verify everything: `bash scripts/check.sh` (or `/check`): lint, build, live backend smoke test, then a headless-browser check of the built app (renders, no console errors, alt text and labels, fits a 375px phone) and `frontend/e2e/demo_path.py` once it exists. Self-contained on :8765/:4173 — the dev servers don't need to be running. It saves `.claude/tmp/e2e.png`; look at it.
- The dev servers are the human's (`.\dev.ps1`). If you must start one, use `run_in_background` — a foreground server blocks the Bash tool until it times out. Backend: `cd backend && venv/Scripts/python -m uvicorn main:app --reload --port 8000`. Frontend: `cd frontend && npm run dev` (:5173, proxies `/api` and `/uploads` to :8000).
- Browser checks and screenshots: the `webapp-testing` skill (Python Playwright, installed). Dev servers up → run a Playwright script against http://localhost:5173. Down → its `with_server.py` starts them; on Windows write the backend command with backslashes: `'cd backend && venv\Scripts\python -m uvicorn main:app --port 8000'` (it runs through cmd.exe, where the forward-slash form fails).
- Deployed: `backend/venv/Scripts/python backend/smoke_test.py <render-url> <vercel-url>` proves the pair works together (CORS, build URL, every endpoint); `backend/venv/Scripts/python backend/seed.py <render-url>` creates the demo account + data there. Both default to localhost:8000 without a URL.

## Timeline
- Kickoff (K): [fill at kickoff, e.g. 2026-09-25 19:00 local]
- Hacking ends (E): [from the schedule, e.g. 2026-09-27 07:00 local]
- Milestone 1, walking skeleton working end to end: K + 10h
- Feature freeze: E − 3h
`date` in Bash gives the real time; compute hours since K and hours to E before any scope decision.

## Deployed
- Render (backend): [paste URL after deploying — DEPLOY.md section 1]
- Vercel (frontend): [paste URL — DEPLOY.md section 2]

## How this codebase is wired — follow these patterns
- Keep the frontend thin: it fetches and renders; logic and validation live in the Python backend, where I can read them. No router, state library, TypeScript, or Tailwind unless the idea can't work without it.
- All frontend→backend calls go through `frontend/src/api.js` (`api`, `login`, `signup`, `uploadFile`, `ask`, `assetUrl`). Never call `fetch` directly.
- No login screen by default. Per-person state (saves, likes, history) is keyed to the demo account: `VITE_DEMO_EMAIL`/`VITE_DEMO_PASSWORD` in `frontend/.env` (matching `backend/seed.py`) make `useAuth` sign in on load, so `Depends(get_current_user)` keeps working with no screen — never move per-user logic into localStorage. Only a true multi-user idea renders `<AuthForm login={login} signup={signup} />` when `user` is null (tested; reuse, don't rebuild).
- New backend feature = new router module shaped like `backend/uploads.py`, then `app.include_router(...)` in `main.py`. Protect routes with `Depends(get_current_user)` from `auth.py`; rate-limit public POSTs with `@limiter.limit("N/minute")` (the handler needs a `request: Request` param). Every new endpoint gets a check in `backend/smoke_test.py`, so `/check` keeps covering the whole app.
- Tables go in `backend/models.py`, created on startup. If you changed it: `/check` uses a fresh database, but the dev server's old `backend/app.db` will 500 with "no such column" — so the last non-question line of the turn is "Delete `backend/app.db` and restart the backend".
- Demo data goes in `seed_project_data` in `backend/seed.py`, via the API, so one command rebuilds it locally or on Render. It runs on every `/check` and every `seed.py <render-url>`, so it must be idempotent: check before creating.
- AI calls: `from llm import complete` → `await complete(prompt, system=..., json_mode=True, fallback="…", image=(bytes, "image/png"))` — `image` lets Gemini read a photo (e.g. an upload's `contents`). `POST /api/ai/ask` in `llm.py` is the example route: copy both of its limit decorators onto every AI route — the per-visitor one and the shared `AI_DAILY_LIMIT` one, which is the only thing protecting the free quota. Without `GEMINI_API_KEY` every call returns a clear 503, so build the feature anyway and ask for the key at the end of the turn that builds it. `fallback=` is mandatory on the demo path, and the UI shows when it fired. Frontend: `ask(prompt)` in `api.js`.

## Standards (on by default, don't ask each time)
- Secrets stay in `.env`, never hardcoded or committed
- Validate any upload by its actual bytes (see `uploads.py`) and any user input hitting the database
- Auth: the existing `auth.py`; never hand-roll password storage
- Every input has a `<label>`, every image has `alt` text, no page wider than a phone — `/check` fails otherwise
- Rate limit public POST endpoints

## How to read me
I talk loosely on purpose ("make it pop", "add a thing where people can save stuff", "this feels off"). I have a specific picture in my head; your job is to find it and build *that*, not the generic version — and asking well is how you find it.
- Start every request by restating it in one line: "Reading that as: …". Confident → build. Something I'll see or feel (a page, a flow, the wow moment) → ask first only when the plausible readings differ in what the demo shows *and* switching later would be expensive; otherwise build the recommended reading, show it, name the alternative.
- Ask with AskUserQuestion: 2–4 specific questions, concrete options, your recommendation first — never a bare "what do you mean?". I may not have words for what I'm picturing; options with examples ("a feed / a grid / a map") let me point. An ask-first turn still shows something — a screenshot of the current page or a rough wireframe per option.
- Ask about vision, not trivia. Vision: what a user sees first, the demo's best moment, list vs map vs feed, who it's for, what it must never do. Trivia you decide: names, copy, colors, spacing, empty states, error messages — I'll say if I don't like them.
- When I react ("this feels off", "no, not like that"): don't guess silently, don't defend. Screenshot the current state, check it against the `frontend-design` skill's list of AI-looking tells, offer 2–3 specific guesses at what's bothering me, let me pick, fix.
- "Make it look better / nicer / pop / professional": the `frontend-design` skill. Brief it with the Idea, the audience, and Decisions; it plans palette/type/layout first — accept the plan unless it reads like a template. Apply the direction to the whole page, screenshot, offer one contrasting alternative as a one-message switch. Once the app has a direction, reuse it everywhere without asking. Keep it accessible.
- Several requests in one message: restate all, build the unambiguous ones now (one commit each), ask about the ambiguous ones in a single AskUserQuestion, continue.
- A request bigger than Scope: build the smallest version that captures it and say what you left out — don't refuse or negotiate mid-turn. The exceptions are PLAYBOOK's: before milestone 1 (Phase 2) and after feature freeze (Phase 5).
- Every turn ends with something I can see — a screenshot, a running page, a `/check` result — plus at most one focused set of questions. Never a wall of questions with nothing built.

## Workflow
- `/spec` is for the initial idea only (I type it). Mid-event feature: plan in one paragraph — table, endpoints, where it appears in the UI, acceptance check — append it to SPEC.md, build. One-line fix: just do it.
- Build order: the walking skeleton — the ugliest version of the exact demo path working end to end — then iterate on it. Never breadth-first.
- Done means evidence: `/check` green, you looked at `.claude/tmp/e2e.png`, and the demo path still passes (`demo_path.py`). Show the result; if something can't be verified, say so. "It should work" is not done.
- Scope guard at every commit: Current status vs Scope vs the hours left. If the must-haves won't fit, say so now and demote per PLAYBOOK's rule for the current phase — don't wait to be asked. Protect Completion first: a small thing that fully works beats a big thing that half-works (the five criteria are in the `spec` skill).
- Sponsor challenges: when planning, say which ones the idea realistically qualifies for and the smallest addition that would qualify it for another — never force a fit, and say plainly when a use would be thin. If I name a sponsor: fetch its current API docs first (never build from memory), ask one AskUserQuestion with 2–3 places it would do real work in the demo (recommendation first, with a wireframe) and wait; then build it behind an env var with a graceful "not configured" state, add the key name to `.env.example`, and ask for the key at the end of the turn that builds it.
- Changes touching auth, data, or security: run the `reviewer` agent on the uncommitted diff before committing (after a commit the diff is empty) and fix what it finds. Don't use subagents for routine building — they start with no memory of the conversation.
- Commit after each feature that works (small commits, message says what now works). Before each commit, rewrite `## Current status` and append anything I confirmed about how the app looks or behaves to `## Decisions`, so they land in that commit — those two sections are the memory that survives compaction, `/clear`, or a crash. After each commit, `git status -sb`; at `ahead 2` or more, `git push` (never `--force`).
- 3 hours or fewer left until E, or I say judging has a time: PLAYBOOK Phase 5.
- The same fix has failed twice: stop, say so, say "this one's worth switching models for", and ask me to `/clear`; then restate the task with what you learned. (Alone: PLAYBOOK → Away mode.)
- When compacting context, preserve: the feature in progress and its acceptance check, working vs broken, files changed since the last commit, and any command that failed and why.

## Budget
Prompts may arrive with "Budget right now: …" (5-hour and weekly usage, from a hook). Don't change how you work because of it; just don't let me get surprised: 5-hour past 85% or weekly past 70% → say so once, with the reset time, before the turn's work; a limit about to hit mid-feature → commit and push what's safe first. Model choice is mine (`/model`).

## Gotchas
- Uploaded files are stored in the database (not on disk — Render's disk is wiped on deploy) and served at `/uploads/<name>`; wrap them with `assetUrl()` in the frontend, never hardcode a host. 5MB max each.
- Frontend env vars must start with `VITE_`; changing `.env` needs a dev-server restart.
- "Something broke" on a page is the ErrorBoundary catching a component crash — the text under it is the real error; the full stack is in the browser console.
- Deployed data lives in Render's Postgres (`DATABASE_URL` from `render.yaml`) and survives deploys; locally it's SQLite in `backend/app.db`. Don't write SQLite-only SQL.
- Per-IP rate limits are per-venue (one shared public IP). Keep limits ≥ 30/minute.
- The backend mirrors every request and traceback to `backend/server.log` — read that when the server runs in a window you can't see.
- `git restore .` / `git checkout .` / `git reset --hard` are denied on purpose. To drop uncommitted work, ask me to rewind (Esc Esc) or run it myself.
- [add project-specific gotchas here as you hit them]

## Decisions
[Confirmed answers about how the app looks and behaves — layout, the wow moment, design direction, what it must never do. Append, don't rewrite.]

## Current status
PHASE: 0 — repo just generated, SPEC.md doesn't exist yet
deployed: no
[Rewrite before every commit. Line 1 is always `PHASE: n — reason`, line 2 `deployed: yes/no`; then, when they apply, one per line: `DO FIRST: …`, `BLOCKED: …`, `WAITING ON YOU: …`, `NEXT: …` (PLAYBOOK says when); then working / broken / in progress + its acceptance check.]
