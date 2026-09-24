# Playbook — what shcht does at each phase of the event

For the Claude Code session building this project. The rules for every turn (how to read the human, the build → `/check` → commit → status loop, standards, budget) live in CLAUDE.md and apply in every phase; this file adds what changes by phase. Times are relative to kickoff (K) and hacking end (E), from CLAUDE.md → Timeline.

## Knowing where we are (first thing, every session)

1. `date`. Read CLAUDE.md → Timeline and the first line of Current status (`PHASE: n — reason`).
2. If the Timeline still holds placeholders: K = the timestamp of the `Start ShellHacks project` commit (`git log --format=%ci --grep="Start ShellHacks"`), or now if there is none; ask E in one AskUserQuestion (ShellHacks 2026 hacks Sept 25–27 — offer the likely end times); write both lines before anything else.
3. Say it in one line: "Phase 3 — hour 14 of 36, milestone 1 done, 2 of 4 must-haves green, deployed: yes."
4. Whenever a phase's exit condition is met, announce it and write the new `PHASE:` line into Current status. Phases are only real once they're written there.

## Phase 0 — Sanity (K+0:00 → K+0:15)

Entry: SPEC.md does not exist.
- Confirm setup: `backend/venv`, `backend/.env` with `JWT_SECRET` (and `GEMINI_API_KEY` if the idea uses AI), `frontend/node_modules`. Missing pieces: offer to run the README setup commands (they're allowlisted); the human creates `.env` and pastes keys.
- `/check` must end `ALL CHECKS PASSED` with no `SKIPPED` browser section. If SKIPPED: `python -m pip install playwright && python -m playwright install chromium`; if that download fails on venue wifi, proceed and retry on the phone hotspot before K+4.
- Ask the human for the sponsor challenge list and paste it into CLAUDE.md → "Sponsor / company challenges to target".
Exit: check green, sponsors written. Say: switch `/model` to the bigger model and type `/spec <idea>`.

## Phase 1 — Spec (K+0:15 → K+0:35)

Runs as the `/spec` skill (the human types it); everything it must do is in that skill. Exit: SPEC.md and the Timeline committed as "Start ShellHacks project", `PHASE: 2` written. Then: `/clear`, `/model` → Sonnet, "build from SPEC.md, walking skeleton first".

## Phase 2 — Walking skeleton (K+0:35 → K+10)

Entry: `PHASE: 2`.
- Build only the demo path, ugliest possible version: tables → endpoints → smoke checks → `api.js` calls → the screens a judge sees. No styling, no nice-to-haves, no photos.
- Photo/file on the demo path: `uploads.py` as-is; AI on it: `complete(prompt, image=(bytes, mime), json_mode=True, fallback=...)` — the fallback is mandatory on the demo path.
- `seed_project_data` in `backend/seed.py` creates the demo data the script needs. It runs on every `/check` and every `seed.py <render-url>`, so it must be idempotent (check before creating).
- As soon as the path works once, write `frontend/e2e/demo_path.py`: same shape as `frontend/e2e/smoke.py`, URL as `sys.argv[1]`, exits non-zero on any failed step, replays SPEC.md's demo script and asserts what a judge sees. `/check` runs it from then on against the throwaway backend seeded only by `seed_project_data`.
- If `models.py` changed, end the turn with "Delete `backend/app.db` and restart the backend".
- **Deploy is the human's task (DEPLOY.md), not a gate.** First turn after K+4 with CLAUDE.md → Deployed blank: say "time to deploy" once; if declined, mention it at most once an hour. At K+10 an empty Deployed becomes the next action before any feature. Track it as `deployed: yes/no` in Current status. Once both URLs exist: `backend/venv/Scripts/python backend/smoke_test.py <render-url> <vercel-url>` (wait for Render's deploy to show green first, or you're testing the old build) and `backend/venv/Scripts/python backend/seed.py <render-url>`.
- Request outside the demo path: "skeleton isn't done yet — X still fails; the smallest piece that serves it is Y" and offer Y.
Exit (milestone 1): `/check` green including `demo_path.py`, and the human clicked through the demo on localhost. Write `PHASE: 3 — milestone 1 done at hour N`. Past K+10 and not there: cut the must-have whose demo step is last in the script and furthest from the wow moment — shorten the script and `demo_path.py` to match, move it to nice-to-haves, say "Cutting X: it's step 5 of 5, the wow moment is step 3" — until it's green.

## Phase 3 — Build-out (milestone 1 → K+24)

Entry: `PHASE: 3`.
- Must-haves in SPEC.md order, one commit each; extend `demo_path.py` when a must-have is on the demo path.
- Scope guard at every commit (hours left vs must-haves left, per CLAUDE.md). When they don't fit: "At this pace feature 4 won't make it; dropping it to nice-to-have — say no to keep it," then proceed with the recommendation unless told otherwise.
- After every commit: `git status -sb`; at `ahead 2` or more, `git push` (allowlisted; it's the backup and the timestamped evidence).
- The one extra sponsor integration (SPEC.md names it): only after all must-haves; docs fetched first; env var + fallback; `demo_path.py` must pass with it disabled.
- Photos: `images` skill, only on a finished page, last step of the turn, never in a turn that changed the design direction.
Exit: every must-have green in `/check` and `demo_path.py`. Write `PHASE: 4 — all must-haves done at hour N`. If K+24 arrives first: freeze the must-have list to what's green, demote the rest, write `PHASE: 4` anyway.

## Away mode (the human says "keep going, I'm going to sleep")

Any phase. Before they leave: confirm `git push` works (run it). Then, turn after turn:
- Must-haves in SPEC.md order, one commit each, `git push` after each.
- A taste question where switching later is cheap: build the recommendation, log `ASSUMED: …` in Decisions. Expensive: stop, write `WAITING ON YOU: …` as the second line of Current status, move to the next must-have.
- A fix that fails twice: `BLOCKED: …` in Current status, move on. Never loop on it.
- `models.py` changed: Current status starts with "Delete `backend/app.db` and restart the backend".
- Must-haves exhausted: `/check`, update status, stop. No nice-to-haves, no design direction, no photos, no sponsor integration alone.

## Phase 4 — Polish (K+24 → E−3)

Entry: `PHASE: 4`.
- One `frontend-design` pass over the demo path: brief it with Idea + audience + Decisions; one direction applied consistently; screenshot; one alternative offered. Then the photo pass.
- Empty, loading, and error states on the demo path, in the interface's voice.
- Mobile: the browser check already fails on overflow; also screenshot the demo path at 375px.
- Nice-to-haves only in SPEC.md's cut order, each removable in one commit; if one breaks `demo_path.py`, `git revert` that commit rather than debugging it.
- Push after each polish commit that touches the demo path; when Render shows green, rerun `smoke_test.py <render-url> <vercel-url>`.
Exit: E−3 from the Timeline. Write `PHASE: 5 — feature freeze`. Announce it.

## Phase 5 — Freeze and ship (E−3 → E)

Entry: `PHASE: 5`, or the human states ≤ 3 hours left, or says judging has a time.
- Feature = new endpoint, table, screen, or `demo_path.py` step. Copy, CSS, empty/error states on existing screens are fixes. Features are refused without negotiation: "Frozen — noted under What's next."
- `/check` + `git status -sb`, then exactly one next action: broken → unpushed → undeployed → pitch (per CLAUDE.md).
- The human types `/pitch` (backup lines for every live-API step, screenshots, README, title), then `/ship-check`. Both are theirs to type.
- Final push by E−1:30 (venue wifi is slow; the phone hotspot is the fallback). Wait for Render green, then `smoke_test.py <render-url> <vercel-url>`, `python frontend/e2e/smoke.py <vercel-url>`, `python frontend/e2e/demo_path.py <vercel-url>`. Demo login works on localhost and deployed.
- E−0:30: stop touching code and say so. A demo-path bug found after that is routed around in PITCH.md (open a seeded record instead; a Backup line), not fixed.
Exit: `/ship-check` green, PITCH.md exists, the human rehearsed once with a timer.

## Recovery (any phase)

- **Broken:** `/debug` (CLAUDE.md). **Same fix failed twice:** stop, say so, ask for `/clear`, restate with what was learned; suggest switching models once.
- **Uncommitted breakage:** you can't `git restore .` (denied on purpose) — ask the human to press Esc twice and rewind, or run it themselves. **Committed breakage:** `git revert <sha>`.
- **`/check` red after a big change:** fix in order lint → build → backend smoke → browser check → demo path; never edit a check to pass.
- **Session lost / reboot:** the human runs `claude --continue`; your first turn: `git status`, `git diff --stat`, read Current status + Decisions, say where we were; dev servers are dead — tell them `.\dev.ps1`.
- **Deployed app misbehaves:** `smoke_test.py <render-url> <vercel-url>` names the culprit (CORS / wrong build URL / backend); `db-error` from `/api/health` = the Postgres link; demo login rejected = new database → `seed.py <render-url>`.
- **Gemini quota or outage:** symptom is 429 in `backend/server.log` or every AI answer wearing the fallback badge. Say the reset time (daily quota resets at midnight Pacific), stop exercising AI routes on the dev server, lower `AI_DAILY_LIMIT`; a second key is the human's call. Demoing on the fallback is fine if the badge is visible.
- **Usage limit warning in the prompt:** per CLAUDE.md → Budget. **Laptop dead:** the human clones onto another machine (`setup-machine.ps1`), re-enters `.env` keys, runs README setup; you resume from the repo — only unpushed work is lost.
