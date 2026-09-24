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

## Why Render + Vercel

Both have free tiers, both deploy straight from a GitHub push (no CLI setup needed mid-hackathon), and this combo is battle-tested for FastAPI + Vite. Render free tier spins down after inactivity and takes ~30s to wake up on the first request after idling — mention this if a judge's first click is slow.
