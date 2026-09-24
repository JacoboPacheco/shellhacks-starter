# Playbook — what shcht does at each phase of the event

For the Claude Code session building this project. CLAUDE.md holds the rules for every turn (reading the human, build → `/check` → commit → status, standards, budget); this file holds what changes by phase. Times are relative to kickoff (K) and hacking end (E), from CLAUDE.md → Timeline.

## Knowing where we are (first thing, every session)

1. `date`. Read CLAUDE.md → Timeline and the first two lines of Current status (`PHASE: n — reason`, `deployed: yes/no`).
2. Timeline still has placeholders: K = the timestamp of the `Start ShellHacks project` commit (`git log --format=%ci --grep="Start ShellHacks"`), or now if there is none; ask E in one AskUserQuestion (ShellHacks 2026 hacks Sept 25–27 — offer the likely end times); write both lines before anything else.
3. Say it in one line: "Phase 3 — hour 14 of 36, milestone 1 done, 2 of 4 must-haves ticked, deployed: yes."
4. When a phase's exit condition is met, write the new `PHASE:` line into Current status and announce it. A phase is only real once it's written.

## Phase 0 — Sanity (K+0:00 → K+0:15)

Entry: SPEC.md does not exist.
- Confirm setup: `backend/venv`, `backend/.env` with `JWT_SECRET` (and `GEMINI_API_KEY` if the idea uses AI), `frontend/node_modules`. Missing pieces: offer to run the README setup commands (allowlisted); the human creates `.env` and pastes keys.
- `/check` must end `ALL CHECKS PASSED` with no `SKIPPED` browser section. If SKIPPED: `python -m pip install playwright && python -m playwright install chromium`; if the download fails on venue wifi, proceed and retry on the phone hotspot before K+4.
- Ask the human for the sponsor challenge list and paste it into CLAUDE.md → "Sponsor / company challenges to target".
Exit: check green, sponsors written. Say: switch `/model` to the bigger model and type `/spec <idea>`.

## Phase 1 — Spec (K+0:15 → K+0:35)

The `/spec` skill, typed by the human; everything it does is in the skill. Exit: SPEC.md and the Timeline committed as "Start ShellHacks project", `PHASE: 2` written, and the skill's hand-off (`/clear`, Sonnet, "build from SPEC.md, walking skeleton first").

## Phase 2 — Walking skeleton (K+0:35 → K+10)

Entry: `PHASE: 2`.
- Build only the demo path, ugliest possible version: tables → endpoints → smoke checks → `api.js` calls → the screens a judge sees. No styling, no nice-to-haves, no photos.
- Photo/file on the demo path: `uploads.py` as-is. AI on it: `complete(..., image=..., json_mode=True, fallback=...)` per CLAUDE.md.
- As soon as the path works once, write `frontend/e2e/demo_path.py`: same shape as `frontend/e2e/smoke.py`, URL as `sys.argv[1]`, exits non-zero on any failed step; it replays SPEC.md's demo script and asserts what a judge sees at each step. It must also be safe to run against the deployed app: create nothing a judge would see, or clean up after itself. `/check` runs it from then on against a throwaway backend seeded only by `seed_project_data`.
- **Deploy is the human's task (DEPLOY.md), never a gate.** First turn after K+4 with `deployed: no`: say "time to deploy — DEPLOY.md" once. At K+10 still `no`: make it the turn's one ask ("deploy now per DEPLOY.md — I keep building meanwhile") and repeat that ask at most once an hour. You build; they deploy. When they paste both URLs into CLAUDE.md → Deployed: flip `deployed: yes`, then `smoke_test.py <render-url> <vercel-url>` and `seed.py <render-url>` (the human confirms Render shows green first, or you're testing the old build).
- Request outside the demo path: "skeleton isn't done yet — X still fails; the smallest piece that serves it is Y" and offer Y.
Exit (milestone 1): `/check` green including `demo_path.py`, and the human clicked through the demo on localhost. Write `PHASE: 3 — milestone 1 done at hour N`.
Cut rule, past K+10 and not there: cut the must-have whose demo step is last in the script and furthest from the wow moment — shorten SPEC.md's demo script and `demo_path.py` to match, move it to nice-to-haves, say "Cutting X: it's step 5 of 5, the wow moment is step 3" — repeat until green.

## Phase 3 — Build-out (milestone 1 → K+24)

Entry: `PHASE: 3`.
- Must-haves in SPEC.md order, one commit each; tick its `- [ ]` in CLAUDE.md → Scope in that commit; extend `demo_path.py` when the must-have is on the demo path.
- When CLAUDE.md's scope guard says they don't fit: "At this pace feature 4 won't make it; dropping it to nice-to-have — say no to keep it," then proceed with the recommendation unless told otherwise.
- The one extra sponsor integration (SPEC.md names it): only after every must-have is ticked, built per CLAUDE.md → Workflow; `demo_path.py` must pass with it disabled.
- Photos: the `images` skill (it owns when).
Exit: every must-have ticked and green in `/check`. Write `PHASE: 4 — all must-haves done at hour N`. If K+24 arrives first: freeze the must-have list to what's green, demote the rest with Phase 2's cut rule (shorten the demo script and `demo_path.py` to what's green), write `PHASE: 4` anyway.

## Away mode (the human says "keep going, I'm going to sleep")

Any phase. Before they leave: run `git push` once so you know it works without a prompt. Then, turn after turn:
- Must-haves in SPEC.md order, one commit each, `git push` after each.
- A taste question where switching later is cheap: build the recommendation, log `ASSUMED: …` in Decisions. Expensive: write `WAITING ON YOU: …` in Current status, move to the next must-have.
- A fix that fails twice: `git add` its files, `git commit -m "WIP (blocked): X"`, `git revert --no-edit HEAD`, then `BLOCKED: X — attempt in commit <sha>` in Current status, move on. Never loop on it, never leave a red diff in the tree.
- `models.py` changed: `DO FIRST: delete backend/app.db and restart the backend` in Current status.
- Must-haves exhausted: `/check`, update status, stop. No nice-to-haves, no design direction, no photos, no sponsor integration alone.

## Phase 4 — Polish (K+24 → E−3)

Entry: `PHASE: 4`.
- One `frontend-design` pass over the demo path (CLAUDE.md → How to read me says how), then the photo pass.
- Empty, loading, and error states on the demo path, in the interface's voice.
- Mobile: the browser check already fails on overflow; also screenshot the demo path at 375px.
- Nice-to-haves only in SPEC.md's cut order, one commit each. If the demo path goes red while building one: one fix attempt, then `git diff > .claude/tmp/dropped-<name>.patch` and ask the human to rewind (Esc Esc) to before it started — don't debug a nice-to-have.
- After each push that touches the demo path, once the human says Render is green: `smoke_test.py <render-url> <vercel-url>`.
Exit: E−3 by the Timeline. Write `PHASE: 5 — feature freeze`, then announce it.

## Phase 5 — Freeze and ship (E−3 → E)

Entry: `PHASE: 5`, or the human says 3 hours or fewer are left, or that judging has a time — write `PHASE: 5` first.
- Feature = new endpoint, table, screen, or `demo_path.py` step. Copy, CSS, empty/error states on existing screens are fixes. Features are refused without negotiation: "Frozen — added as `NEXT: …` in Current status" (`/pitch` reads those into What's next).
- Every turn: `/check` + `git status -sb`, then exactly one next action, in this priority: broken → unpushed → undeployed (`deployed: no`, or `smoke_test.py <render-url> <vercel-url>` fails) → pitch. If the action is pitch: the human types `/pitch`, then `/ship-check` (pitch first — it rewrites the README that ship-check verifies; you can't run either).
- Final push by E−1:30 (venue wifi is slow; the phone hotspot is the fallback). You can't see Render's dashboard — the human reads it. When they say green: `smoke_test.py <render-url> <vercel-url>`, `python frontend/e2e/smoke.py <vercel-url>`, `python frontend/e2e/demo_path.py <vercel-url>`. Not green by E−0:45: stop pushing — Render keeps serving the last successful deploy; demo that or localhost, and write it as the Backup in PITCH.md.
- E−0:30: stop touching code and say so. A demo-path bug found after that is routed around in PITCH.md (a seeded record to open instead; a Backup line), not fixed.
Exit: `/ship-check` green, PITCH.md exists, the human rehearsed once with a timer.

## Recovery (any phase)

- **Broken:** `/debug`. **Same fix failed twice:** CLAUDE.md → Workflow (human present) or Away mode (alone).
- **Uncommitted breakage:** you can't `git restore .` (CLAUDE.md → Gotchas) — ask the human to rewind (Esc Esc). **Committed breakage:** `git revert --no-edit <sha>`.
- **`/check` red after a big change:** fix in order lint → build → backend smoke → browser check → demo path.
- **Session lost / reboot:** the human runs `claude --continue`; your first turn: `git status`, `git diff --stat`, Current status + Decisions, say where we were; the dev servers are dead — tell them `.\dev.ps1`.
- **Deployed app misbehaves:** `smoke_test.py <render-url> <vercel-url>` names the culprit (CORS / wrong build URL / backend); `db-error` from `/api/health` = the Postgres link; demo login rejected = new database → `seed.py <render-url>`.
- **AI answers wearing the fallback badge, or 429s in `backend/server.log`:** two different 429s. Body says `AI quota for today is used up` → our own `AI_DAILY_LIMIT` (in-memory: restarting the backend resets it, or raise it — `backend/.env` locally, Render's env tab deployed; both are the human's). 429 from `generativelanguage.googleapis.com` → Google's free quota: say the reset time (midnight Pacific), stop exercising AI routes on the dev server, lower `AI_DAILY_LIMIT`; a second key is the human's call. Demoing on the fallback is fine if the badge is visible.
- **Usage limit warning:** CLAUDE.md → Budget. **Laptop dead:** the human clones onto another machine (`setup-machine.ps1`), re-enters `.env` keys, runs README setup; you resume from the repo — only unpushed work is lost.
