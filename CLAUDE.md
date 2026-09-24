# Project: [NAME]

You're a great engineer and this team is lucky to have you on this build — let's ship something judges remember.

## Idea
[One paragraph: what it does, who it's for, why it's interesting to a judge in 30 seconds.]

## Stack
- Frontend: [e.g. React + Vite]
- Backend: [e.g. Node/Express, FastAPI]
- Database: [e.g. SQLite, Postgres, Supabase]
- Deploy target: [e.g. Vercel + Railway]
- APIs/keys needed: [list them — fill in .env.example too]

## Scope (hackathon-realistic)
Must have (demo breaks without these):
- [ ]
- [ ]

Nice to have (cut first if time runs out):
- [ ]

Explicitly NOT doing:
- [ ]

## Standards (keep these on by default, don't ask each time)
- Secrets stay in `.env`, never hardcoded or committed
- Validate/sanitize any file upload (type + size check) and any user input hitting the database
- Auth: use a library (FastAPI OAuth2/passlib, Clerk, Auth0) — don't hand-roll password storage
- Forms: every input has a `<label>`, every image has `alt` text
- Basic rate limit on public POST endpoints

## Current status
[Update this as you go — what's working, what's broken, what you're mid-way through.]

## Known issues / gotchas
[Anything Claude should know before touching the code — flaky endpoint, env var quirks, etc.]
