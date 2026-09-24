# Deploy path

Do this once, early (Day 1 practice), so kickoff-day deploy is just "repeat these steps."

## Backend → Render

1. Push this repo to GitHub.
2. render.com → New → Web Service → connect the repo.
3. Root directory: `backend`
4. Build command: `pip install -r requirements.txt`
5. Start command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
6. Add env vars from `backend/.env.example` (set `ALLOWED_ORIGINS` to your Vercel URL once you have it — step 5 below).
7. Deploy. Note the URL, e.g. `https://yourapp.onrender.com`.
8. Confirm: visit `https://yourapp.onrender.com/api/health` — should show `{"status":"ok"}`.

## Frontend → Vercel

1. vercel.com → New Project → import the same repo.
2. Root directory: `frontend`
3. Framework preset: Vite (auto-detected)
4. Add env var `VITE_API_URL` = your Render backend URL from above (no trailing slash).
5. Deploy. Note the URL, e.g. `https://yourapp.vercel.app`.

## Close the loop

Go back to Render, set `ALLOWED_ORIGINS` to your Vercel URL, redeploy the backend. Reload the frontend — "Backend status: ok" should show with no CORS errors.

## Important: Render's free tier disk is not persistent

This starter uses SQLite (`backend/app.db`) and saves uploads to local disk (`backend/uploads/`). On Render's free tier, the filesystem resets on every redeploy and on every restart after the service spins down from inactivity — meaning **all signups and all uploaded files can vanish without warning**, possibly mid-demo. For a 36-hour hackathon this is usually fine to accept as-is (judges see a fresh demo anyway), but know it going in. If it becomes a problem: switch to Render's free Postgres for the database, and either accept uploads are ephemeral or move them to an external store (S3-compatible bucket) if the idea depends on files surviving.

## Why Render + Vercel

Both have free tiers, both deploy straight from a GitHub push (no CLI setup needed mid-hackathon), and this combo is battle-tested for FastAPI + Vite. Render free tier spins down after inactivity and takes ~30s to wake up on the first request after idling — mention this if a judge's first click is slow.
