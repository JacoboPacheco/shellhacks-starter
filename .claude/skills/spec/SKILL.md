---
name: spec
description: Interview the user about THEIR hackathon idea and write a buildable SPEC.md. Only runs when the user types /spec.
disable-model-invocation: true
---

The user has an idea: $ARGUMENTS

Do not propose ideas of your own. Your job is to pressure-test theirs and turn it into a spec that can be built in the time left.

**The lens for every question — what wins here.** ShellHacks judges on five equally weighted criteria: Completion (does it work), Originality (is it new or a twist), Design (how it looks and feels), Technology (what's under the hood and how well it's used), Practicality (could a real person use it). Judges grade what they see work in a few minutes — not code quality, not pitch polish. The last two years of winners share: a real problem a judge recognizes in one sentence; a live demo with one moment that makes a judge react; one genuinely technical piece (vision, AI, real-time, hardware) doing real work, not bolted on; polish on a small scope over breadth; a clear audience, often an underserved one; when going for a sponsor prize, the sponsor's tech used meaningfully. Push the spec toward one wow moment that works end to end, and cut whatever doesn't serve it.

1. Read CLAUDE.md first, especially the sponsor/company challenges list and the stack.
2. Interview the user with the AskUserQuestion tool, a few questions per round, each with concrete options and your recommended answer first. Skip anything obvious or already implied. If an answer is loose ("whatever works", "you pick"), propose a concrete interpretation and fold it into the next thing you show — the demo-script read-back is the confirmation; don't spend a round on it. Keep going until you can describe the demo screen by screen, usually two rounds. Dig into:
   - The one thing a judge must see in the demo for this to land
   - What data exists, where it comes from, and what happens with bad or missing input
   - Which sponsor challenges it realistically qualifies for, and the smallest addition that would qualify it for another (never force a fit)
   - What gets cut first if time runs short
3. Write `SPEC.md`: problem (2 sentences), demo script (the exact clicks a judge sees), must-have features with an acceptance check for each, nice-to-haves in cut order, explicitly out of scope, sponsor challenges targeted and why, new endpoints and tables, **starter pieces touched** (for each of `uploads.py`, `llm.py`, `seed.py`, `smoke_test.py`: reused as-is or needs extending — e.g. `complete(image=...)` for photos — and any extension goes in milestone 1), and the verification: which `smoke_test.py` checks get added and which committed sample file (e.g. `backend/demo/sample.jpg`) they use. Any latency or accuracy number in the spec is *measured after the skeleton*, never promised up front. Two defaults unless the idea truly needs otherwise: **no login screen** — existing routes stay behind `Depends(get_current_user)` and the frontend signs in as the `seed.py` demo account on load (`VITE_DEMO_EMAIL`, see CLAUDE.md); only a true multi-user idea gets `<AuthForm>` — and **milestone 1 = the walking skeleton**: the ugliest possible version of the exact demo path working end to end, before any second feature or any polish.
4. Update the Idea, Sponsor challenges, and Scope sections of CLAUDE.md to match. Keep them short — SPEC.md holds the detail.
5. Commit SPEC.md and CLAUDE.md with the message `Start ShellHacks project` — this is the line in the history between the pre-event template and event work.
6. Tell the user to run `/clear` and then say "build from SPEC.md", so the build starts with clean context.
