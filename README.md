# Shellhacks starter

FastAPI backend + React (Vite) frontend, wired together and verified working end to end, plus a `.claude/` setup that makes Claude Code faster and more reliable on this repo.
Clone this at kickoff, run `/spec` in Claude Code with your idea, and start building features instead of plumbing.

> **"Running scripts is disabled on this system"?** Fresh Windows blocks `.ps1` files. Run any of this repo's scripts as `powershell -ExecutionPolicy Bypass -File .\script.ps1`, or allow them for your account once with `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`.

## One-time setup (PowerShell, from the repo root)

```
cd backend
python -m venv venv
venv\Scripts\pip install -r requirements.txt
copy .env.example .env
cd ..\frontend
npm install
cd ..
```

Then open `backend\.env` and set `JWT_SECRET` (generate one with `python -c "import secrets; print(secrets.token_hex(32))"`).

Optional, for `/images`: copy `.env.example` (repo root) to `.env` and add a free Unsplash access key.

## Run it

```
.\dev.ps1
```

Opens the backend (auto-reloads when files change) and frontend in two windows. Open http://localhost:5173 — it should show "Backend status: ok". Working on the gaming PC over Remote-SSH? Use two VS Code terminals instead — see [REMOTE.md](./REMOTE.md).

## Check that it actually works

```
.\check.ps1
```

(From Git Bash or inside Claude Code: `bash scripts/check.sh` — same thing.) Lints and builds the frontend, starts a throwaway backend, and runs the smoke test (health, signup, auth, uploads, rejection paths). Prints `ALL CHECKS PASSED` or names what failed. CI runs the same script on every push.

## What's in `.claude/` (Claude Code picks this up automatically)

| | What it does |
|---|---|
| `CLAUDE.md` | Standing orders: commands, codebase patterns, standards, gotchas |
| `/spec <idea>` | Interviews you about your idea and writes SPEC.md (never suggests its own ideas) |
| `/check` | Runs `scripts/check.sh` and reports with evidence |
| `images` skill | When a page is done, Claude finds its photo spots, looks at Unsplash options, places its best picks with credit, then asks you once to confirm or swap. Also runs on `/images` |
| `/ship-check` | Pre-demo readiness check, including the ShellHacks disclosure rule |
| `/pitch` | Drafts the 2-minute demo script, Devpost writeup, disclosure line, and judge Q&A from what actually got built |
| `/debug` | Reproduce → read the real error (server log, browser console) → fix the root cause → add a check. No guessing first |
| `reviewer` agent | Fresh-eyes review of a finished feature's diff |
| Edit hook | After every edit, lint-checks JS/JSX and syntax-checks Python so broken code is caught immediately |
| Push reminder | When Claude finishes a turn with 4+ unpushed commits, it says so — pushes are your timestamped proof of event-time work and your backup |
| Permissions | Routine commands (npm scripts, checks, git status/diff/commit) run without asking; `git push --force` and `git reset --hard` are denied; any other push still asks |

## More

- Deploying: [DEPLOY.md](./DEPLOY.md)
- Reaching the gaming PC remotely: [REMOTE.md](./REMOTE.md)
- Kickoff-day runbook: [KICKOFF_CHECKLIST.md](./KICKOFF_CHECKLIST.md)
- First-time gaming PC setup: `powershell -ExecutionPolicy Bypass -File .\setup-gaming-pc.ps1` once
