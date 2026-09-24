# Deploy path

Do this once, early (Day 1 practice), so kickoff-day deploy is just "repeat these steps."
Order matters: backend first (Vercel needs its URL), then frontend, then close the loop.

After the practice run, delete the practice services (Render: service → Settings → Delete; Vercel: project → Settings → Delete). Otherwise on kickoff day the Blueprint's service name `shellhacks-backend` is already taken and Vercel's project name collides — a confusing 10 minutes you don't need. (Or just rename the service in `render.yaml` to your project's name at kickoff.)

## 1. Backend → Render (about 5 clicks — `render.yaml` does the rest)

1. Push this repo to GitHub.
2. render.com → New → **Blueprint** → connect the repo. Render reads `render.yaml` and shows one service, `shellhacks-backend`.
3. It asks for `ALLOWED_ORIGINS` — put `http://localhost:5173` for now (you'll change it in section 3). `JWT_SECRET` is generated for you.
4. Apply. Wait for the deploy to go green. Copy the URL (e.g. `https://shellhacks-backend.onrender.com`) into CLAUDE.md under **Deployed**.
5. Confirm: `https://<your-render-url>/api/health` shows `{"status":"ok"}`.

## 2. Frontend → Vercel

1. vercel.com → New Project → import the same repo.
2. Root directory: `frontend` (Vite is auto-detected; `frontend/vercel.json` handles page routing).
3. Environment variable `VITE_API_URL` = your Render URL from above, **no trailing slash**.
4. Deploy. Get the URL from **Project → Settings → Domains** (the stable `yourapp.vercel.app` one), not the "Visit" button — that often opens a per-deployment URL like `yourapp-abc123.vercel.app`, which won't match the CORS setting below. Copy it into CLAUDE.md under **Deployed**.

## 3. Close the loop

Render → your service → Environment → set `ALLOWED_ORIGINS` to your Vercel URL (no trailing slash; several origins are comma-separated) → save, it redeploys. Then open the Vercel URL: "Backend status: ok" with no CORS errors in the browser console. If it says "backend unreachable", the origin doesn't match — compare the browser's address bar to `ALLOWED_ORIGINS` character by character (https, no trailing slash, the Domains URL not a deployment URL).

Prove the deployed backend works, not just that it's up:

```
SMOKE_BASE_URL=https://<your-render-url> backend/venv/Scripts/python backend/smoke_test.py
```

(Git Bash / Claude Code. From PowerShell: `$env:SMOKE_BASE_URL='https://<your-render-url>'; backend\venv\Scripts\python backend\smoke_test.py`.)

## 4. Keep the backend awake (2 minutes, do it right after deploying)

Render's free tier spins down after ~15 min idle, and the next request waits ~30s — that would be a judge's first click. The repo includes a GitHub Action that pings the backend every 10 minutes. Turn it on: GitHub → your repo → Settings → Secrets and variables → Actions → **Variables** → New repository variable → name `RENDER_URL`, value your Render URL. Confirm under the Actions tab that "Keep backend warm" runs green. (GitHub may delay scheduled runs by a few minutes; that's fine.) Still open the site yourself a minute before demoing.

## Redeploying during the hackathon

Both services redeploy automatically on every `git push` — expect about a minute for Render, less for Vercel. Don't push an untested change in the last 15 minutes before a demo.

## Important: Render's free tier disk is not persistent

This starter uses SQLite (`backend/app.db`) and saves uploads to local disk (`backend/uploads/`). On Render's free tier, the filesystem resets on every redeploy and on every restart after the service spins down from inactivity — meaning **all signups and all uploaded files can vanish without warning**, possibly mid-demo. For a 36-hour hackathon this is usually fine to accept as-is (judges see a fresh demo anyway), but know it going in. If it becomes a problem: switch to Render's free Postgres for the database (`DATABASE_URL` is already read from the environment), and either accept uploads are ephemeral or move them to an external store (S3-compatible bucket) if the idea depends on files surviving.

## Why Render + Vercel

Both have free tiers, both deploy straight from a GitHub push (no CLI setup needed mid-hackathon), and this combo is battle-tested for FastAPI + Vite.
