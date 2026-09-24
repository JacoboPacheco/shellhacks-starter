# Kickoff day runbook

**ShellHacks 2026: Sept 25–27, FIU Graham Center (Modesto Maidique Campus), 36 hours of hacking.** Judging criteria, equally weighted: Completion, Originality, Design, Technology, Practicality. Submission is on Devpost with your GitHub repo attached — check the Hacker Guide / Discord on day 1 for the exact deadline and whether a video is required. Everything runs on the laptop; git push is the backup.

## Before the event (tonight, in this order — then sleep)
- [ ] **Pick your idea.** Two candidates, one sentence each, plus the one moment that makes a judge react. Decide. The sponsor list at kickoff only adjusts it.
- [ ] Put the starter on GitHub: `gh auth login`, then `gh repo create shellhacks-starter --public --source . --push`
- [ ] On github.com → the repo → Settings → tick **Template repository**
- [ ] Dry-run the kickoff command so it's not new on the day: in `C:\dev`, `gh repo create kickoff-test --public --clone --template <your-github-user>/shellhacks-starter`, confirm `backend\.env` and `app.db` are NOT in it, then delete the test repo (`gh repo delete kickoff-test --yes`) and the folder
- [ ] Free API keys, saved where you can paste from: Gemini (aistudio.google.com/apikey — `llm.py` is wired for it; the default model is a Flash-Lite because that's the one with a usable free quota, confirm at aistudio.google.com/rate-limit), Unsplash (photos). A sponsor track you care about with an API → that key too
- [ ] 15 minutes: learn to open the browser console (F12 → Console and Network tabs) and paste the red text to Claude. This is the one skill that unblocks a stuck AI on a frontend bug.
- [ ] 60-minute timed mini-build from the template: `/spec` a throwaway idea, build one feature end to end (table → endpoint → page), `/check`, commit. This tests your loop, not the code. Write down where you got stuck.
- [ ] Practice deploy per DEPLOY.md, timeboxed to 45 minutes. If Render/Vercel fight you, stop and do it at hour 4 of the event instead. Delete the practice services afterwards (DEPLOY.md top note).
- [ ] Sleep 6+ hours. Pack: laptop, charger, power strip, phone + charger, battery bank, headphones.

## First 15 minutes
- [ ] In `C:\dev` (outside OneDrive — it's slow and locks files mid-build):
  `gh repo create <project-name> --public --clone --template <your-github-user>/shellhacks-starter`
  The project gets its own GitHub repo with event-time history only, and a "generated from" badge that discloses the template.
- [ ] Paste the sponsor challenge list (from the opening ceremony / event site) into CLAUDE.md under "Sponsor / company challenges" — `/spec` reads it from there
- [ ] Do the one-time setup in README.md (venv, `pip install`, `npm install`, `backend\.env` with a new `JWT_SECRET` and your `GEMINI_API_KEY`)
- [ ] `.\check.ps1` → must say `ALL CHECKS PASSED` before you write a single feature
- [ ] Start Claude Code in the repo and **accept the "trust this folder" prompt** — until you do, the permission allowlist and hooks in `.claude/settings.json` are silently ignored. Also accept the prompt to install the repo's plugins (`frontend-design`, `example-skills`). If no prompt appears, `/plugin` and check they're listed.
- [ ] `/model` → pick the bigger model for the spec; run `/spec <your idea in a sentence>`, answer its questions — it writes SPEC.md, fills in CLAUDE.md, and commits "Start ShellHacks project". Timebox: 20 minutes; you already chose the idea.
- [ ] `/clear`, `/model` → Sonnet, then "build from SPEC.md, walking skeleton first"

## Building
- [ ] `.\dev.ps1` from a standalone PowerShell window keeps both servers up (backend auto-reloads)
- [ ] Model plan: build on Sonnet. Switch up (`/model`) for hard debugging when Sonnet has failed twice, and for the final review. Switch back after.
- [ ] Walking skeleton by hour 10: the ugliest version of the exact demo path working end to end. Then iterate. Never breadth-first.
- [ ] Claude keeps CLAUDE.md's "Current status" and "Decisions" updated after each commit — glance at them when you come back from a break; they're the session's memory
- [ ] Three Claude Code moves worth knowing: a change made things worse → press **Esc twice** and rewind to before it; a side question you don't want cluttering the session → start it with `/btw`; the session feels confused after many corrections → `/clear` and restate the task (Claude re-reads CLAUDE.md, SPEC.md, and Current status)
- [ ] Watch the status line at the bottom: `ctx` is how full Claude's memory is (it compacts itself near the top — fine), `5h` is your usage limit, `↑N` is unpushed commits
- [ ] Deploy early (see DEPLOY.md), once, by hour 4 — then turn Auto-Deploy off and redeploy manually a few times a day. A broken deploy found early is a non-event; found late is a crisis.
- [ ] `git push` every couple of hours — backup if the laptop dies, and it keeps the timestamped history safe (Claude nags at 2 unpushed commits)
- [ ] Re-check Scope every few hours — cut "nice to have" the moment you're behind
- [ ] Sleep night one. Solo with no sleep produces garbage on day two.

## Last 3 hours — stop building new features
- [ ] Freeze features, fix only what's broken
- [ ] Judging is table-to-table: **demo from your laptop's localhost** (`.\dev.ps1`, `seed.py` for fresh demo data). The deployed URL is for Devpost and for judges who click later.
- [ ] Final manual deploy on Render + Vercel, then `backend\venv\Scripts\python backend\seed.py <render-url>` — every deploy erases the demo account and data. Write the demo login on paper.
- [ ] `/pitch` — 30-second and 2-minute versions, Devpost writeup, screenshots, project README. Read the 2-minute one out loud with a timer; memorize the 30-second one.
- [ ] `/ship-check` — every readiness check, including the rules disclosure line and a secrets scan
- [ ] Full run-through of the demo path on both localhost and the deployed URL
- [ ] Record the 2-minute demo video (your backup if the laptop dies at the table)

## Before you sleep / leave
- [ ] Confirm the deployed URL works from a phone on cellular data (not the venue wifi)
- [ ] Charge everything
