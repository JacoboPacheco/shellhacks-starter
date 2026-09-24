# Playbook — what shcht does at each phase of the event

For the Claude Code session building this project. CLAUDE.md holds the rules for every turn; this file holds what changes by phase. Times are relative to kickoff (K) and hacking end (E), from CLAUDE.md → Timeline.

## Knowing where we are (first thing, every session)

1. `date`. Read CLAUDE.md → Timeline and Current status (`PHASE`, `deployed`, and any `DO FIRST` / `BLOCKED` / `WAITING ON YOU` lines).
2. Timeline still has placeholders: ask K and E in one AskUserQuestion (K = the kickoff time the human gives, else now; ShellHacks 2026 hacks Sept 25–27 — offer the likely end times); write both lines before anything else.
3. Say it in one line: "Phase 3 — hour 14 of 36, milestone 1 done, 2 of 4 must-haves ticked, deployed: yes" — then repeat any `DO FIRST` / `WAITING ON YOU` lines verbatim.
4. When a phase's exit condition is met, write the new `PHASE:` line into Current status and announce it. A phase is only real once it's written.

## Phase 0 — Sanity (K+0:00 → K+0:15)

Entry: SPEC.md does not exist.
- Confirm setup: `backend/venv`, `backend/.env` with `JWT_SECRET` (and `GEMINI_API_KEY` if the idea uses AI), `frontend/node_modules`. Missing pieces: run the bash equivalents of the README setup (`cd backend && python -m venv venv && venv/Scripts/pip install -r requirements.txt`; `cd frontend && npm install`); the human creates `.env` and pastes keys.
- `/check` must end `ALL CHECKS PASSED` with no `SKIPPED` browser section. If SKIPPED: `python -m pip install playwright && python -m playwright install chromium`; if the download fails on venue wifi, proceed and retry on the phone hotspot before K+4.
- Ask the human for the sponsor challenge list and paste it into CLAUDE.md → "Sponsor / company challenges to target".
Exit: check green, sponsors written. Say: switch `/model` to the bigger model and type `/spec <idea>`.

## Phase 1 — Spec (K+0:15 → K+0:35)

The `/spec` skill, typed by the human; everything it does is in the skill. Exit: the skill's commit and hand-off are done.

## Phase 2 — Walking skeleton (K+0:35 → K+10)

Entry: `PHASE: 2`.
- The walking skeleton is the ugliest possible version of the exact demo path working end to end: tables → endpoints → smoke checks → `api.js` calls → the screens a judge sees. Nothing else — no styling, no nice-to-haves. AI on the path: CLAUDE.md → How this codebase is wired.
- As soon as the path works once, write `frontend/e2e/demo_path.py`: same shape as `frontend/e2e/smoke.py`, URL as `sys.argv[1]`, exits non-zero on any failed step; it replays SPEC.md's demo script and asserts what a judge sees at each step. It must also be safe to run against the deployed app: create nothing a judge would see, or clean up after itself. `/check` runs it from then on against a throwaway backend seeded only by `seed_project_data`.
- Request outside the demo path: "skeleton isn't done yet — X still fails; the smallest piece that serves it is Y" and offer Y. If they insist: push back once, never twice. Build the smallest version as its own commit after the current skeleton step is committed, add it to SPEC.md nice-to-haves (must-haves if they say so), log it in Decisions.
Exit (milestone 1): `/check` green including `demo_path.py`, and the human clicked through the demo on localhost. Write `PHASE: 3 — milestone 1 done at hour N`.
Cut rule, past K+10 and not there: cut the must-have whose demo step is last in the script and furthest from the wow moment — shorten SPEC.md's demo script and `demo_path.py` to match, move it to nice-to-haves, say "Cutting X: it's step 5 of 5, the wow moment is step 3" — repeat until green.

## Deploy (Phases 2–4)

Deploy is the human's task (DEPLOY.md), never a gate: you build, they deploy. First turn after K+4 with `deployed: no`: write `WAITING ON YOU: deploy per DEPLOY.md (asked HH:MM)` in Current status and say it once. From K+10, put it first in the turn's ask whenever that timestamp is an hour or more old, and update the timestamp. When they paste both URLs into CLAUDE.md → Deployed: flip `deployed: yes`, drop the line. The deployed checks — `smoke_test.py <render-url> <vercel-url>`, then `seed.py <render-url>` the first time — run only after the human says Render shows green: you can't see Render's dashboard, and before green you're testing the old build.

## Phase 3 — Build-out (milestone 1 → K+24)

Entry: `PHASE: 3`.
- Must-haves in SPEC.md order; extend `demo_path.py` when the must-have is on the demo path.
- When CLAUDE.md's scope guard says they don't fit: "At this pace feature 4 won't make it; dropping it to nice-to-have — say no to keep it," then proceed with the recommendation unless told otherwise.
- The one extra sponsor integration (SPEC.md names it): only after every must-have is ticked; `demo_path.py` must pass with it disabled.
Exit: every must-have ticked and green in `/check`. Write `PHASE: 4 — all must-haves done at hour N`. If K+24 arrives first: freeze the must-have list to what's green, demote the rest with Phase 2's cut rule (shorten the demo script and `demo_path.py` to what's green), write `PHASE: 4` anyway.

## Away mode (the human says "keep going, I'm going to sleep")

Any phase. Before they leave: run `git push` once so you know it works without a prompt, and finish-and-commit or WIP-and-revert (below) anything uncommitted. Then, turn after turn:
- Must-haves in SPEC.md order, `git push` after each commit.
- A taste question where switching later is cheap: build the recommendation, log `ASSUMED: …` in Decisions. Expensive: write `WAITING ON YOU: …` in Current status, move to the next must-have.
- A fix that fails twice: `git add` its files — not CLAUDE.md — then `git commit -m "WIP (blocked): X"` and `git revert --no-edit HEAD`. Then write `BLOCKED: X — attempt in commit <WIP sha>` in Current status, `git commit -m "Status: X blocked" CLAUDE.md`, `git push`, move on. Never loop on it, never leave a red diff in the tree.
- `models.py` changed: `DO FIRST: delete backend/app.db and restart the backend` in Current status.
- Must-haves exhausted: `/check`, update status, commit CLAUDE.md, `git push`, stop. No nice-to-haves, no design direction, no sponsor integration alone.

## Phase 4 — Polish (K+24 → E−3)

Entry: `PHASE: 4`.
- One `frontend-design` pass over the demo path (CLAUDE.md → How to read me says how) — if Decisions already records a design direction, apply it instead of planning a new one. The photo pass (`images` skill) comes the following turn.
- Empty, loading, and error states on the demo path, in the interface's voice.
- Mobile: screenshot the demo path at 375px.
- Nice-to-haves only in SPEC.md's cut order. If the demo path goes red while building one: one fix attempt, then `git add` its files (not CLAUDE.md), `git commit -m "WIP (dropped): <name>"`, `git revert --no-edit HEAD`, note `BLOCKED: <name> (nice-to-have) — attempt in <sha>` — don't debug a nice-to-have.
- After each push that touches the demo path: the deployed checks (Deploy section).
Exit: E−3 by the Timeline. Write `PHASE: 5 — feature freeze`, then announce it.

## Phase 5 — Freeze and ship (E−3 → E)

Entry: `PHASE: 5` (CLAUDE.md → Workflow can trigger it early — write it first).
- Feature = new endpoint, table, screen, or `demo_path.py` step. Copy, CSS, empty/error states on existing screens are fixes. Features are refused without negotiation: "Frozen — added as `LATER: …` in Current status."
- Every turn: `/check` + `git status -sb`, then exactly one next action, in this priority: broken → unpushed → undeployed (`deployed: no`, or the deployed checks fail after the human said Render is green) → pitch; while Render is still building, pitch is next. If the action is pitch: the human types `/pitch`, then `/ship-check` (pitch first — it rewrites the README that ship-check verifies; you can't run either).
- Final push by E−1:30 (venue wifi is slow; the phone hotspot is the fallback). When the human says green: the deployed checks, then `python frontend/e2e/smoke.py <vercel-url>` and `python frontend/e2e/demo_path.py <vercel-url>`. Not green by E−0:45: stop pushing; run `python frontend/e2e/demo_path.py <vercel-url>` — passes → the deployed app is demoable, fails → demo localhost, and tell the human to run `/pitch Backup: Render not green — demo localhost`.
- E−0:30: stop touching code and say so. A demo-path bug found after that is routed around, not fixed: the human reruns `/pitch` with a note naming the seeded record to open instead.
Exit: `/ship-check` green, PITCH.md exists, the human rehearsed once with a timer.

## Recovery (any phase)

- **Broken:** `/debug`. **Same fix failed twice:** CLAUDE.md → Workflow (human present) or Away mode (alone).
- **Uncommitted breakage:** CLAUDE.md → Gotchas. **Committed breakage:** `git revert --no-edit <sha>`.
- **`/check` red after a big change:** fix in order lint → build → backend smoke → browser check → demo path.
- **Session lost / reboot:** the human runs `claude --continue`; your first turn: `git status`, `git diff --stat`, Current status + Decisions, say where we were; the dev servers are dead — tell them `.\dev.ps1`.
- **Deployed app misbehaves:** `smoke_test.py <render-url> <vercel-url>` names the culprit (CORS / wrong build URL / backend); `db-error` from `/api/health` = the Postgres link; demo login rejected = new database → `seed.py <render-url>`.
- **AI answers wearing the fallback badge:** `backend/server.log` tells the two 429s apart. A `429` on the AI route's request line → our own `AI_DAILY_LIMIT` (in-memory: restarting the backend resets it, or raise it — `backend/.env` locally, Render's env tab deployed; both are the human's). A `WARNING … AI fallback used: AI request failed (429)` line → Google's free quota: say the reset time (midnight Pacific), stop exercising AI routes on the dev server, lower `AI_DAILY_LIMIT`; a second key is the human's call. Demoing on the fallback is fine if the badge is visible.
- **Usage limit warning:** CLAUDE.md → Budget. **Laptop dead:** the human clones onto another machine (`setup-machine.ps1`), re-enters `.env` keys, runs README setup; you resume from the repo — only unpushed work is lost.
