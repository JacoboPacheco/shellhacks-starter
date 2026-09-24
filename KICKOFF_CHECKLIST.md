# Kickoff day runbook

**ShellHacks 2026: Sept 25–27, FIU Graham Center (Modesto Maidique Campus), 36 hours of hacking.** Judging criteria, equally weighted: Completion, Originality, Design, Technology, Practicality. Submission is on Devpost and must have your GitHub repo attached — check the Hacker Guide / Discord on day 1 for the exact deadline and whether a video is required.

## Before the event (once, from this practice folder)
- [ ] Put the starter on GitHub: `gh auth login`, then `gh repo create shellhacks-starter --public --source . --push`
- [ ] On github.com → the repo → Settings → tick **Template repository**. Kickoff day then starts from a one-liner, and the new repo shows "generated from …/shellhacks-starter" — built-in disclosure of the pre-existing code.
- [ ] Gaming PC set up and reachable from the laptop over a phone hotspot (REMOTE.md)

## First 15 minutes
- [ ] On the gaming PC (over Remote-SSH from the laptop), in `C:\dev` — **outside OneDrive**, which is slow and locks files mid-build:
  `gh repo create <project-name> --public --clone --template <your-github-user>/shellhacks-starter`
  This creates the project's own GitHub repo, with event-time history only, and clones it. Don't copy the practice folder; it drags along your real `.env` and test data.
- [ ] Paste the sponsor challenge list (from the opening ceremony / event site) into CLAUDE.md under "Sponsor / company challenges" — `/spec` reads it from there
- [ ] Do the one-time setup in README.md (venv, `pip install`, `npm install`, `backend\.env` with a new `JWT_SECRET`)
- [ ] `.\check.ps1` → must say `ALL CHECKS PASSED` before you write a single feature
- [ ] Start Claude Code in the repo and **accept the "trust this folder" prompt** — until you do, the permission allowlist and hooks in `.claude/settings.json` are silently ignored. Also accept the prompt to install the repo's plugins (`frontend-design`, `example-skills`) — they're registered in the same file, so a fresh machine gets them automatically. If no prompt appears, run `/plugin` and check they're listed; otherwise install them from there.
- [ ] Run `/hooks` once to confirm the "Checking edited file" hook is listed
- [ ] Run `/spec <your idea in a sentence>`, answer its questions — it writes SPEC.md, fills in CLAUDE.md, and commits "Start ShellHacks project"
- [ ] `/clear`, then tell Claude Code to build from SPEC.md

## Building
- [ ] Dev servers over Remote-SSH: **don't use `dev.ps1`** (its windows open on the gaming PC's screen, not yours). In VS Code, open two terminals and run the backend and frontend commands from CLAUDE.md → Commands. VS Code forwards port 5173 automatically when Vite prints its URL; if the laptop browser shows nothing, add 5173 in the **Ports** panel. The backend needs no forward — Vite proxies `/api` to it.
- [ ] Keep CLAUDE.md's "Current status" updated — this is what keeps Claude Code oriented across a long session
- [ ] Deploy early (see DEPLOY.md), not at hour 30 — a broken deploy found early is a non-event; found late is a crisis
- [ ] `git push` every few hours — backup if the gaming PC dies, and it keeps the timestamped history safe (Claude reminds you at 4 unpushed commits)
- [ ] Re-check Scope every few hours — cut "nice to have" the moment you're behind

## Last 3 hours — stop building new features
- [ ] Freeze features, fix only what's broken
- [ ] Render → service → Settings → Build & Deploy → **Auto-Deploy: No**. From here on pushes are backups only; ship a chosen commit with "Manual Deploy" so a stray push can't wipe the demo data mid-judging
- [ ] **After the final deploy: create the demo account and demo data again — every deploy erases them** — and write the login on paper
- [ ] `/ship-check` — runs every readiness check, including the rules disclosure line
- [ ] `/pitch` — drafts the demo script, Devpost writeup, and judge Q&A from what actually got built; read it out loud once with a timer
- [ ] Full run-through of the demo path on the deployed URL, not localhost
- [ ] Record the 2-minute demo video (your backup if wifi dies)

## Before you sleep / leave
- [ ] Confirm the deployed URL still works from a phone on cellular data (not the venue wifi)
- [ ] Charge everything
