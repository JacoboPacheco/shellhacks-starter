# Shellhacks starter

FastAPI backend + React (Vite) frontend, wired together and verified working end to end.
Clone this at kickoff, fill out [CLAUDE.md](./CLAUDE.md) with the actual idea, and start building features instead of plumbing.

## Run it locally

**Backend:**
```
cd backend
python -m venv venv
venv\Scripts\pip install -r requirements.txt
venv\Scripts\python -m uvicorn main:app --port 8000
```

**Frontend** (separate terminal):
```
cd frontend
npm install
npm run dev
```

Open http://localhost:5173 — it should show "Backend status: ok". If it says "backend unreachable", the backend isn't running or isn't on port 8000.

## Deploying

See [DEPLOY.md](./DEPLOY.md).

## First-time gaming PC setup

Run [setup-gaming-pc.ps1](./setup-gaming-pc.ps1) once, from a normal PowerShell window.
