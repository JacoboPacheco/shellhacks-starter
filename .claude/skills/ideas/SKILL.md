---
name: ideas
description: Generate and score candidate hackathon ideas from the sponsor challenge list and the user's answers, then help them pick one. Only runs when the user types /ideas, at kickoff, before /spec.
disable-model-invocation: true
---

The user wants ideas. Seeds they gave, if any: $ARGUMENTS

Your job is to generate real candidates, score them honestly, and kill the bad ones — including the user's own if they bring one. The user can come up with horrible plans and has asked to be told. This runs once, at kickoff: 15 minutes, two rounds at most.

0. If SPEC.md exists, or Current status's PHASE is 2 or higher: change nothing, say "/ideas is kickoff-only — the idea is already chosen (PHASE n)" and stop.
1. Read CLAUDE.md → "Sponsor / company challenges to target" and the Stack, the "what wins here" paragraph in `.claude/skills/spec/SKILL.md`, and the "Pick your idea" scoring rubric in `KICKOFF_CHECKLIST.md`. If the sponsor list is still a placeholder, ask the human to paste it (Phase 0) — ideas without it waste the sponsor prizes.
2. **Ask first, in one AskUserQuestion of 3–4 questions**, each with concrete options and your recommendation first, about the human, not trivia: which problem areas or audiences they know firsthand or care about; what they want the demo to feel like (a tool someone uses, something that reacts live, something visual, something that surprises); what they want to get better at or show off; anything they won't do. Solo, 36 hours, a walking skeleton in 10.5 — so it must be buildable by one person on this stack (FastAPI + React + Gemini for text and images) with no hardware, no scraping, no approvals from third parties.
3. **Generate 6 candidates** from their answers and the sponsor list. For each: a one-sentence pitch; who it's for; **the moment a judge watches happen** (not explains); the one technical piece doing real work; which sponsor challenges it honestly fits (theme tracks it fits; at most one API track that is central; never forced); whether the walking skeleton — the exact demo path, ugly — is buildable in 10 hours, and what could sink it. At least two must be strong sponsor fits, and at least one must be modest and certain to finish. Do not pad with near-duplicates.
4. **Check originality for the top 2** with a few web searches (Devpost galleries of past ShellHacks and similar hackathons, plus the obvious existing products); at most 5 minutes. Say plainly what already exists and what the twist is, or that there is none.
5. **Score all 6** with the KICKOFF rubric (five criteria, 1–5 each) in a table, then a blunt recommendation: the top pick, why, and its single biggest risk. Name any candidate that is a clone of a product, needs data you can't get in an hour, or has its wow moment in explanation rather than action, and say it's out.
6. **Ask which to build**, one AskUserQuestion: the recommended one first, the runner-up, "combine two" (say which), or "none — regenerate" with what to change. One regeneration round at most; then pick the best one.
7. Write the chosen idea into CLAUDE.md → Idea (one paragraph: what it does, who it's for, why a judge cares in 30 seconds) and the runner-up under Decisions as `RUNNER-UP: …` in case the first collapses. Don't commit — `/spec` commits. Then tell the human: type `/spec <the chosen idea in one sentence>` — the same bigger model, no `/clear` in between.
