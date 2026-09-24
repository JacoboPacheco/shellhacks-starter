---
name: spec
description: Interview the user about THEIR hackathon idea and write a buildable SPEC.md. Only runs when the user types /spec.
disable-model-invocation: true
---

The user has an idea: $ARGUMENTS

Do not propose ideas of your own. Your job is to pressure-test theirs and turn it into a spec that can be built in the time left.

**The lens for every question — what wins here.** ShellHacks judges on five equally weighted criteria: Completion (does it work), Originality (is it new or a twist), Design (how it looks and feels), Technology (what's under the hood and how well it's used), Practicality (could a real person use it). Judges grade what they see work in a few minutes — not code quality, not pitch polish. The last two years of winners share: a real problem a judge recognizes in one sentence; a live demo with one moment that makes a judge react; one genuinely technical piece (vision, AI, real-time, hardware) doing real work, not bolted on; polish on a small scope over breadth; a clear audience, often an underserved one; when going for a sponsor prize, the sponsor's tech used meaningfully. Push the spec toward one wow moment that works end to end, and cut whatever doesn't serve it.

1. Read CLAUDE.md first, especially the sponsor/company challenges list and the stack.
2. Interview the user with the AskUserQuestion tool, a few questions per round, each with concrete options and your recommended answer first. Skip anything obvious or already implied. If an answer is loose ("whatever works", "you pick"), propose a concrete interpretation and fold it into the next thing you show — the demo-script read-back is the confirmation; don't spend a round on it. Keep going until you can describe the demo screen by screen, usually two rounds; the whole skill is timeboxed to 20 minutes — if it's running long, write the spec with what you have and mark open questions in it. In round one also ask when hacking ends (for the Timeline). Dig into:
   - The one thing a judge must see in the demo for this to land
   - What data exists, where it comes from, and what happens with bad or missing input
   - Which sponsor challenges it realistically qualifies for. Rule: enter every *theme* track the idea already fits; for *API* tracks, the one whose tech is the heart of the idea plus at most ONE extra integration (built per CLAUDE.md → Workflow, after the must-haves, so it can never break the demo). A bolted-on API loses "best use of" to a project where it's central, and every extra one costs hours and Completion. Never force a fit.
   - What gets cut first if time runs short
3. Write `SPEC.md`: problem (2 sentences), demo script (the exact clicks a judge sees), must-have features with an acceptance check for each, nice-to-haves in cut order, explicitly out of scope, sponsor challenges targeted and why, new endpoints and tables, **starter pieces touched** (for each of `uploads.py`, `llm.py`, `seed.py`, `smoke_test.py`: reused as-is or needs extending — e.g. `complete(image=...)` for photos — and any extension goes in milestone 1), and the verification: which `smoke_test.py` checks get added and which committed sample file (e.g. `backend/demo/sample.jpg`) they use. Any latency or accuracy number in the spec is *measured after the skeleton*, never promised up front. Two defaults unless the idea truly needs otherwise: **no login screen** (the demo auto-login in CLAUDE.md → How this codebase is wired; only a true multi-user idea gets `<AuthForm>`) and **milestone 1 = the walking skeleton**: the ugliest possible version of the exact demo path working end to end, before any second feature or any polish, including `frontend/e2e/demo_path.py` as PLAYBOOK.md Phase 2 specifies it.
4. Fill CLAUDE.md's **Timeline** section — kickoff time (K, now if the user doesn't say) and hacking end (E, from the schedule; ask) — and set Current status's first line to `PHASE: 2 — spec done, skeleton not started` (keep `deployed: no` as line 2).
5. Update the Idea, Sponsor challenges, and Scope sections of CLAUDE.md to match. Keep them short — SPEC.md holds the detail.
6. Commit SPEC.md and CLAUDE.md with the message `Start ShellHacks project` — this is the line in the history between the pre-event template and event work.
7. Tell the user to run `/clear`, switch `/model` back to Sonnet, then say "build from SPEC.md, walking skeleton first" — so the build starts with clean context on the cheaper model.
