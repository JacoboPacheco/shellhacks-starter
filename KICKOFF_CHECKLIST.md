# Kickoff day runbook

## First 15 minutes
- [ ] Clone this repo fresh from GitHub into a folder **outside OneDrive** (e.g. `C:\dev\`) — OneDrive syncing `node_modules`/`venv` is slow and locks files mid-build. Don't copy the practice folder either; it drags along your real `.env` secret and test data.
- [ ] Note down the sponsor challenge list from the opening ceremony/event site before you forget it
- [ ] Do the one-time setup in README.md (venv, `pip install`, `npm install`, `backend\.env` with a new `JWT_SECRET`)
- [ ] `.\check.ps1` → must say `ALL CHECKS PASSED` before you write a single feature
- [ ] Start Claude Code in the repo and **accept the "trust this folder" prompt** — until you do, the permission allowlist and edit hook in `.claude/settings.json` are silently ignored
- [ ] Run `/hooks` once to confirm the "Checking edited file" PostToolUse hook is listed
- [ ] Run `/spec <your idea in a sentence>`, answer its questions — it writes SPEC.md and fills in CLAUDE.md
- [ ] Commit SPEC.md + CLAUDE.md as "Start ShellHacks project" — a clear line between the pre-event template and event work in the history
- [ ] `/clear`, then tell Claude Code to build from SPEC.md

## Building
- [ ] `.\dev.ps1` to run both servers (backend auto-reloads)
- [ ] Keep CLAUDE.md's "Current status" updated — this is what keeps Claude Code oriented across a long session
- [ ] Deploy early (see DEPLOY.md), not at hour 30 — a broken deploy found early is a non-event; found late is a crisis
- [ ] `git push` every few hours — backup if the gaming PC dies, and it keeps the timestamped history safe
- [ ] Re-check Scope every few hours — cut "nice to have" the moment you're behind

## Last 3 hours — stop building new features
- [ ] Freeze features, fix only what's broken
- [ ] `/ship-check` — runs every readiness check, including the rules disclosure line
- [ ] Full run-through of the demo path on the deployed URL, not localhost
- [ ] Record the 2-minute demo video (your backup if wifi dies)
- [ ] Write/rehearse the pitch: problem, demo, what's technically interesting, done

## Before you sleep / leave
- [ ] Confirm the deployed URL still works from a phone on cellular data (not the venue wifi)
- [ ] Charge everything
