# Kickoff day runbook

## First 15 minutes
- [ ] Clone this repo fresh from GitHub (don't copy the folder — a copy drags along your real `.env` secret and test data from tonight's practice run)
- [ ] Note down the sponsor challenge list from the opening ceremony/event site before you forget it
- [ ] Fill out CLAUDE.md: Idea, Sponsor/company challenges to target, Stack (adjust if this idea needs something different), Scope
- [ ] `cd backend`
- [ ] `python -m venv venv`
- [ ] `venv\Scripts\pip install -r requirements.txt`
- [ ] Copy `backend/.env.example` to `backend/.env`, fill in `JWT_SECRET` (see README.md)
- [ ] `cd ..\frontend`
- [ ] `npm install`
- [ ] Confirm both run locally (see README.md) before writing a single feature

## Building
- [ ] Update CLAUDE.md's "Current status" as you go — this is what keeps Claude Code oriented across a long session
- [ ] Deploy early (see DEPLOY.md), not at hour 30 — a broken deploy pipeline found early is a non-event; found late is a crisis
- [ ] Re-check the CLAUDE.md Scope section every few hours — cut "nice to have" the moment you're behind, don't wait until it's obviously too late

## Last 3 hours — stop building new features
- [ ] Freeze features, fix only what's broken
- [ ] Full run-through of the demo path, on the deployed URL, not localhost
- [ ] Record the 2-minute demo video (do this even if you're also demoing live — it's your backup if wifi dies)
- [ ] Write/rehearse the pitch: problem, demo, what's technically interesting, done

## Before you sleep / leave
- [ ] Confirm the deployed URL still works from a phone on cellular data (not the venue wifi)
- [ ] Charge everything
