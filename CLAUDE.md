# Project: [NAME]

You're a great engineer and this team is lucky to have you on this build — let's ship something judges remember.

## Idea
[One paragraph: what it does, who it's for, why it's interesting to a judge in 30 seconds. Run /spec to fill this in properly.]

## Sponsor / company challenges to target
[From the event's sponsor list at kickoff — name, sponsor, their actual eligibility requirement. Leave out ones that don't naturally fit.]
- [ ]

## Stack
FastAPI (backend; SQLite locally, Postgres on Render), React + Vite (frontend), Render + Vercel (deploy) — change only if the idea truly needs something else.
- APIs/keys needed: [list them, and add each to the matching .env.example]

## Scope (hackathon-realistic)
Must have (demo breaks without these):
- [ ]

Nice to have (cut first if time runs out):
- [ ]

Explicitly NOT doing:
- [ ]

## Phases
PLAYBOOK.md is the stage-by-stage plan for the whole event. Read it at the start of every session and whenever the phase changes; say which phase we're in (from the Timeline, `date`, and Current status) before doing anything else.

## Commands
Run shell commands with the Bash tool (Git Bash), not PowerShell — everything here is bash syntax and the permission allowlist is written for Bash.
- Verify everything: `bash scripts/check.sh` (or `/check`) — lint, build, live backend smoke test, then a headless-browser check of the built app (renders, no crash, no console errors, every image has alt / every input has a label, fits a 375px phone). It saves `.claude/tmp/e2e.png` — look at it with the Read tool after a `/check`. Self-contained (own servers on :8765 and :4173), so this is how you test; you don't need the dev servers running.
- The dev servers are the human's: they run `.\dev.ps1` and keep them up. If you must start one yourself, run it in the background (`run_in_background`) — a foreground `uvicorn`/`npm run dev` blocks the Bash tool until it times out.
  - Backend: `cd backend && venv/Scripts/python -m uvicorn main:app --reload --port 8000`
  - Frontend: `cd frontend && npm run dev` (http://localhost:5173, proxies `/api` and `/uploads` to :8000)
- Browser checks and screenshots: the `webapp-testing` skill (Python Playwright, installed). If the dev servers are up, just run a Playwright script against http://localhost:5173. If not, its `with_server.py` helper starts them — on Windows write the backend command with backslashes: `'cd backend && venv\Scripts\python -m uvicorn main:app --port 8000'`.
- Deployed backend: `backend/venv/Scripts/python backend/smoke_test.py <render-url>` to prove it works; `backend/venv/Scripts/python backend/seed.py <render-url>` to create the demo account + data (once — it persists). Both default to localhost:8000 without the URL.

## Timeline
- Kickoff (K): [fill at kickoff, e.g. 2026-09-25 19:00 local]
- Hacking ends (E): [from the schedule, e.g. 2026-09-27 07:00 local]
- Milestone 1, walking skeleton working end to end: K + 10h
- Feature freeze: E − 3h
Use `date` in Bash to know the real time; compute hours since K and hours to E before any scope decision. The first line of Current status is always `PHASE: <n> — <one-line reason>` (see PLAYBOOK.md), so a fresh session knows where we are.

## Deployed
- Render (backend): [paste URL after deploying — DEPLOY.md section 1]
- Vercel (frontend): [paste URL — DEPLOY.md section 2]

## How this codebase is wired — follow these patterns
- Keep the frontend thin: it fetches and renders; logic and validation live in the Python backend, where I can read them. No router, state library, TypeScript, or Tailwind unless the idea can't work without it.
- All frontend→backend calls go through `frontend/src/api.js` (`api`, `login`, `signup`, `uploadFile`, `ask`, `assetUrl`). Don't call `fetch` directly.
- Default is no login screen — every login is dead seconds in front of a judge. If a feature needs per-person state (saves, likes, history) anyway, key it to the demo account: set `VITE_DEMO_EMAIL`/`VITE_DEMO_PASSWORD` in `frontend/.env` (matching `backend/seed.py`) and `useAuth` signs in as that account on load, so `Depends(get_current_user)` keeps working with no screen. Never move per-user logic into localStorage for this. Only if the idea truly needs real multi-user accounts: render `<AuthForm login={login} signup={signup} />` when `user` is null (tested end to end — reuse, don't rebuild).
- New backend feature = new router module shaped like `backend/uploads.py`, then `app.include_router(...)` in `main.py`. Protect routes with `Depends(get_current_user)` from `auth.py`. Rate-limit public POSTs with `@limiter.limit("N/minute")` (the handler needs a `request: Request` param).
- Tables go in `backend/models.py` and are created on startup. Demo data goes in `seed_project_data` in `backend/seed.py`, via the API, so one command rebuilds it locally or on Render.
- AI calls: `from llm import complete` → `await complete(prompt, system=..., json_mode=True, fallback="…", image=(bytes, "image/png"))` — `image` lets Gemini read a photo, e.g. the `contents` from an upload; `POST /api/ai/ask` in `llm.py` is the example route — copy both of its limit decorators onto every AI route: the per-visitor one and the shared `AI_DAILY_LIMIT` one (the demo password is public, so only a whole-app daily cap protects the free quota). It needs `GEMINI_API_KEY`; without it every call returns a clear 503, so build the feature anyway and ask me for the key once at the end. Pass `fallback=` on the demo path so a dead API doesn't kill the demo (and show that it's a fallback). Frontend: `ask(prompt)` in `api.js`.
- Visual work: brief the `frontend-design` skill with the Idea, the audience, and anything in Decisions; it plans palette/type/layout first — accept the plan unless it reads like a template, then let it code.
- Every new endpoint gets a check in `backend/smoke_test.py`, so `/check` keeps covering the whole app.

## Standards (keep these on by default, don't ask each time)
- Secrets stay in `.env`, never hardcoded or committed
- Validate any upload by its actual bytes (see `uploads.py`) and any user input hitting the database
- Auth: use the existing `auth.py`; never hand-roll password storage
- Every input has a `<label>`, every image has `alt` text — `/check` fails otherwise, and so does a page wider than a phone
- Rate limit public POST endpoints

## How to read me
I talk loosely on purpose ("make it pop", "add a thing where people can save stuff", "this feels off"). I have a specific picture in my head; your job is to find it and build *that*, not the generic version. Asking is how you find it — just ask well.
- Always start by restating what you heard in one line: "Reading that as: …". If you're confident, build it. If the request is about something I'll see or feel (a page, a flow, the "wow" moment), ask before building only when the plausible readings differ in what the demo shows *and* switching later would be expensive. Otherwise build the recommended reading, show it, and name the alternative.
- Ask with AskUserQuestion, 2–4 specific questions, each with concrete options and your recommendation first — never a bare "what do you mean?". I may not have the words for what I'm picturing; options with examples ("a feed like Instagram / a grid like Pinterest / a map") let me point at it. An ask-before-build turn still shows something: a screenshot of the current page, or a rough wireframe per option, so I can point.
- Ask about vision, not trivia. Vision: what a user sees first, what the demo's best moment is, list vs map vs feed, who it's for, what it must never do. Trivia you decide yourself: names, copy, colors, spacing, empty states, error messages — I'll say if I don't like them.
- When I react ("this feels off", "no, not like that"): don't guess silently and don't defend it. Screenshot the current state and check it against the `frontend-design` skill's list of AI-looking tells, then offer 2–3 specific guesses at what's bothering me, let me pick, then fix.
- "Make it look better / nicer / pop / professional": use the `frontend-design` skill. Apply the recommended direction to the whole page, screenshot it, and offer one contrasting alternative as a one-message switch. Once the app has a direction, reuse it on every other page without asking. Keep it accessible.
- Several requests in one message: restate all of them, build the unambiguous ones now (one commit each), ask about the ambiguous ones in a single AskUserQuestion, then continue.
- If what I ask implies more than the Scope allows, build the smallest version that captures it and say what you left out. Don't refuse, don't negotiate scope mid-turn — until feature freeze (PLAYBOOK.md Phase 5), when new features are refused. (Sponsor challenges are the other exception — see Workflow.)
- Every turn ends with something I can see — a screenshot, a running page, a `/check` result — plus at most one focused set of questions. Never a wall of questions with nothing built.
- Vibe applies to interpretation, not correctness. `/check` and small commits still happen every time.

## Workflow
- `/spec` is for the initial idea only (the user types it). For a mid-event feature: plan in one paragraph — table, endpoints, where it appears in the UI, acceptance check — append it to SPEC.md, build. For a one-line fix, just do it.
- Build order: the walking skeleton first — the ugliest version of the exact demo path working end to end — then iterate on it. Never breadth-first. Don't start feature #2 until milestone 1 is green; if I ask for something else before that, say "skeleton isn't done yet — X still fails" and offer to do the smallest piece that serves the skeleton.
- Scope guard, at every commit: compare Current status against Scope and the Timeline. If must-haves won't fit the hours left, say which nice-to-have to cut *now* and why — don't wait for me to ask. Past the feature-freeze time, refuse new features and say so.
- Definition of done, for any feature: `/check` is green, you looked at `.claude/tmp/e2e.png`, and the demo path still works end to end — `frontend/e2e/demo_path.py` passes (it replays SPEC.md's demo script; `/check` runs it automatically once it exists). "It should work" is not done.
- Judges grade what they see work (Completion, Originality, Design, Technology, Practicality — equal weight; details in the `spec` skill). When planning or cutting scope, protect Completion first: a small thing that fully works beats a big thing that half-works.
- When planning, point out which sponsor challenges the idea realistically qualifies for and the smallest addition that would qualify it for another — never force a fit, and say plainly when a sponsor use would be thin. If I ask for a sponsor by name: fetch its current API docs first (never build from memory), then ask one AskUserQuestion with 2–3 places it would do real work in the demo (recommendation first, with a wireframe of where it appears) and wait; then build it behind an env var with a graceful "not configured" state, add the key name to `.env.example`, and ask me for the key once, at the end.
- When I say there are 3 hours or fewer left, or that judging has a time: stop new features. Run `/check` and `git status -sb`, then give me exactly one next action in this priority: broken → unpushed → undeployed (a Deployed URL is blank, or `smoke_test.py <render-url>` fails) → pitch. If the action is pitch, it is: type `/pitch`, then `/ship-check` (you can't run those; pitch first because it rewrites the README that ship-check verifies).
- Don't claim a feature is done without evidence: run `/check` and show the result; if something can't be verified, say so. Then commit. For changes that touch auth, data, or security, run the `reviewer` agent on the uncommitted diff first and fix what it finds (review before commit — after a commit the diff is empty). Everything else: `/check` + commit. Don't use subagents for routine building; they start with no memory of the conversation.
- Commit after each feature that works (small commits, message says what now works). The commit history is our evidence the project was built during the event — never batch a whole day into one commit. After every commit run `git status -sb`; at 2 or more ahead, `git push` yourself (never `--force`).
- After every commit, rewrite `## Current status` below (working / broken / in progress + its acceptance check), and append anything I confirmed about how the app should look or behave to `## Decisions`. Those two sections are the memory that survives compaction, `/clear`, or a crash.
- If you changed `backend/models.py`, end the turn (before any photo question) with: "Delete `backend/app.db` and restart the backend" — `/check` uses a fresh database, so it passes while the dev server's old file 500s with "no such column".
- If you've corrected the same mistake twice, stop: say so and ask me to `/clear`, then restate the task with what you learned.
- When compacting context, preserve: the feature in progress and its acceptance check, what's working vs broken, the files changed since the last commit, and any command that failed and why.

## Budget
Prompts may arrive with "Budget right now: …" (5-hour and weekly usage, from a hook). Don't change how you work because of it — just don't let me get surprised: when the 5-hour limit passes 85%, or the weekly passes 70%, say so once, with the reset time, before starting the turn's work; and if a limit is about to be hit mid-feature, commit and push what's safe first. Model choice is mine (`/model`): I build on Sonnet and switch up for `/spec`, hard debugging, and final review — if a problem has beaten Sonnet twice, say "this one's worth switching models for".

## Gotchas
- Uploaded files are stored in the database (not on disk — Render's disk is wiped on deploy) and served at `/uploads/<name>`; in the frontend wrap them with `assetUrl()`, never hardcode a host. 5MB max each; anything bigger belongs in external storage.
- Frontend env vars must start with `VITE_`; changing `.env` needs a dev-server restart.
- A page showing "Something broke" is the ErrorBoundary catching a component crash — the text under it is the real error message; the full stack is in the browser console.
- Deployed data lives in Render's Postgres (`DATABASE_URL`, provisioned by `render.yaml`) and survives deploys. Locally it's SQLite in `backend/app.db`. Same code, both tested; don't write SQLite-only SQL.
- Everyone at the venue shares one public IP, so per-IP rate limits are effectively per-venue. Keep limits ≥ 30/minute.
- The backend mirrors its output (every request and every traceback) to `backend/server.log` — read that when the server runs in a window you can't see.
- [add project-specific gotchas here as you hit them]

## Decisions
[Confirmed answers about how the app looks and behaves — layout, the wow moment, design direction, what it must never do. Append, don't rewrite.]

## Current status
PHASE: 0 — repo just generated, SPEC.md doesn't exist yet
[Rewrite after every commit — first line is the PHASE, then working / broken / in progress + its acceptance check.]
