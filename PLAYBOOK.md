# Playbook — what shcht does at each stage of the event

For the Claude Code session building this project. Read this at the start of every session and whenever the phase changes; work out which phase we're in from the Timeline in CLAUDE.md, `date`, and Current status, and say it in one line ("Phase 3, hour 14, milestone 1 done, 2 of 4 must-haves green"). Times are relative to kickoff (K) and hacking end (E).

## The loop every turn runs, in every phase

1. Restate what the human asked in one line. If it's about something they'll see and the readings differ in what the demo shows, ask 2–4 option-based questions (recommendation first) — otherwise build the recommended reading.
2. Build the smallest thing that makes the request true. New backend feature = router module like `uploads.py` + `include_router` + `models.py` + a `smoke_test.py` check; frontend = thin component using `api.js`.
3. `/check`. Look at `.claude/tmp/e2e.png`. If `demo_path.py` exists, it ran too.
4. Auth/data/security touched → `reviewer` agent on the diff, fix what it finds.
5. Commit with a message that says what now works.
6. Rewrite `## Current status`; append confirmed taste/behavior answers to `## Decisions`.
7. End with something visible (screenshot, `/check` output, a URL) and at most one focused set of questions.

Never: claim done without step 3, batch a day into one commit, start feature #2 before milestone 1, add a login screen, hand-roll auth, call `fetch` outside `api.js`, or build a sponsor integration from memory instead of its docs.

## Phase 0 — Sanity (first 15 minutes)

Entry: the repo was just generated from the template on the laptop, in `C:\dev\<project>`.
- Confirm the setup happened: `backend/venv`, `backend/.env` with `JWT_SECRET` (and `GEMINI_API_KEY` if AI), `frontend/node_modules`. If not, walk the human through README's one-time setup — don't run installs they haven't asked for.
- `/check` must be `ALL CHECKS PASSED` and the browser section must not say SKIPPED. If it does, Playwright is missing: `python -m pip install playwright && playwright install chromium`.
- Confirm `/hooks` lists the edit hook and the status line is showing (the human checks; you can't see the UI).
- Ask for the sponsor challenge list and paste it into CLAUDE.md → Sponsor / company challenges.
Exit: check green, sponsors in CLAUDE.md. Tell the human to switch to the bigger model and type `/spec <idea>`.

## Phase 1 — Spec (K+0:15 → K+0:45)

Runs as the `/spec` skill. Entry: the human typed `/spec`.
- Interview against the judging lens (Completion, Originality, Design, Technology, Practicality) and what past winners share; ~two rounds; "you pick" answers get folded into the read-back, not another round.
- Sponsor rule: every theme track that fits; the one API that is the heart of the idea; at most one extra API, behind an env var with a fallback.
- Write SPEC.md with the demo script click by click, must-haves with acceptance checks, cut order, out of scope, starter pieces reused vs extended, which smoke checks and sample files get added.
- Fill CLAUDE.md: Idea, Sponsors, Scope, and **Timeline** (hacking end from the schedule; milestone 1 = K+10h; feature freeze = E−3h).
- Commit "Start ShellHacks project".
Exit: SPEC.md committed. Tell the human: `/clear`, `/model` → Sonnet, then "build from SPEC.md, walking skeleton first". Timebox 20 minutes total — if the interview is running long, write the spec with what you have and mark open questions in it.

## Phase 2 — Walking skeleton (K+0:45 → K+10)

Entry: a fresh session, SPEC.md exists, milestone 1 not done.
- Build only the demo path, ugliest possible version, in this order: tables → endpoints → smoke checks → frontend calls → the screens a judge sees. No styling, no nice-to-haves, no photos, no error-message polish beyond what stops a crash.
- If the idea uses a photo or file: `uploads.py` as-is; AI on it: `complete(prompt, image=(bytes, mime), json_mode=True, fallback=...)`. The fallback is not optional on the demo path.
- Write `frontend/e2e/demo_path.py` as soon as the path works once — it replays SPEC.md's demo script and asserts what a judge sees at each step. From now on `/check` runs it.
- Fill `seed_project_data` in `backend/seed.py` so `seed.py` creates the demo data the script needs.
- **K+4: deploy.** Tell the human it's time (DEPLOY.md), and once both URLs are in CLAUDE.md → Deployed run `SMOKE_ORIGIN=<vercel> smoke_test.py <render>` and `seed.py <render>`. A broken deploy found now is a non-event.
- If the human asks for anything outside the demo path: "skeleton isn't done yet — X still fails; the smallest piece that serves it is Y" and offer Y.
Exit (milestone 1): `/check` green including `demo_path.py`; the demo script can be clicked through on localhost by the human; deployed and smoke-tested. Say so explicitly: "Milestone 1 done at hour N." If it's past K+10 and not done: cut must-haves until it is — tell the human which and why, then do it.

## Phase 3 — Build-out (milestone 1 → K+24)

Entry: milestone 1 announced.
- Take must-haves in SPEC.md order, one at a time, one commit each, each ending with `demo_path.py` extended to cover it if it's on the demo path.
- Scope guard at every commit: hours left vs must-haves left. If they don't fit, name the cut *now*: "At this pace feature 4 won't make it; I recommend dropping it to nice-to-have. Say no to keep it." Then proceed with the recommendation unless told otherwise.
- Sponsor integration (the one extra allowed): only after all must-haves; docs fetched first; behind an env var; `demo_path.py` must pass with it disabled.
- Photos: only when a page is done and `/check` passed, as the last step of a turn, via the `images` skill; never in a turn that changed the design direction.
- Push reminders: the Stop hook nags at 2 unpushed commits; when it does, say "push now" in your last line.
- If the human says "keep going while I'm away": work down the must-haves list in order, one commit each; stop at the first taste question and leave it in Current status as "WAITING ON YOU: …"; never do a design direction, photo pass, or sponsor integration alone.
Exit: every must-have green in `/check` and in `demo_path.py`, deployed. Say "All must-haves done at hour N — polish phase."

## Phase 4 — Polish (K+24 → E−3)

Entry: must-haves done, or the clock hit K+24 (then cut to what's done and polish that).
- One `frontend-design` pass on the whole demo path: brief it with Idea + audience + Decisions; apply one direction consistently; screenshot; offer one alternative. Then the photo pass.
- Empty states, error messages, loading states on the demo path — in the interface's voice, no apologies.
- Mobile: the browser check already fails on horizontal overflow; also check the demo path at 375px with a screenshot.
- Nice-to-haves only if they're in cut order, each behind the same loop, each removable in one commit. Stop the moment a nice-to-have breaks `demo_path.py`.
- Redeploy after each polish commit that changes the demo path; rerun `smoke_test.py <render>` with `SMOKE_ORIGIN`.
Exit: feature-freeze time from the Timeline. Announce it: "Feature freeze — from here I only fix."

## Phase 5 — Freeze and ship (E−3 → E)

Entry: the Timeline's freeze time, or the human mentions time left / judging / demo.
- Refuse new features, politely and without negotiation: "Frozen — I'll note it under What's next."
- `/check` + `git status -sb`, then exactly one next action in priority: broken → unpushed → undeployed → pitch.
- When the human types `/pitch`: 30-second and 2-minute scripts with backup lines for every live API step, Devpost writeup, disclosure line, Q&A, screenshots via `webapp-testing`, README rewrite, page title. Then `/ship-check`.
- Final push by E−1h. Then `smoke_test.py <render>` with `SMOKE_ORIGIN`, `python frontend/e2e/smoke.py <vercel-url>`, and a full `demo_path.py` run against the deployed frontend if the script takes a URL. Confirm the demo login works on both localhost and deployed.
- E−0:30: stop touching the code. Say so. Anything found now goes in Q&A as "known issue", not a fix.
Exit: `/ship-check` all green, PITCH.md exists, human has rehearsed once with a timer.

## Recovery workflows (any phase)

- **Something's broken:** `/debug` — reproduce, read `backend/server.log` and the browser console/network, name the cause, fix the root cause, add a smoke check. No code until the error is quoted.
- **Same fix failed twice:** stop; say so; ask the human to `/clear`; restate the task with what was learned. Suggest switching models once if it's beaten Sonnet twice.
- **Session lost / laptop restarted:** on resume: `git status`, `git diff --stat`, read Current status and Decisions, say where we were, restart nothing the human didn't ask for.
- **`/check` red after a merge or a big change:** fix in this order — lint → build → backend smoke → browser check → demo path. Never edit a check to make it pass; say if a check is wrong.
- **Deployed app misbehaves:** `smoke_test.py <render>` with `SMOKE_ORIGIN` tells you which of CORS / wrong build URL / backend is at fault; `db-error` from health means the Postgres link is wrong; "Incorrect email or password" for the demo account means the database is new — `seed.py <render>`.
- **Usage limit warning in the prompt (5-hour > 85%, weekly > 70%):** say it once with the reset time before starting; if a limit will hit mid-feature, commit and push what's safe first.
- **AI quota / Gemini down:** the `fallback=` path must keep the demo alive; if it doesn't, that's a must-fix, not a note.
- **Laptop dead:** the human clones the repo on another machine (`setup-machine.ps1`), re-enters `.env` keys, runs README setup; you resume from the repo + CLAUDE.md. Only unpushed work is lost — which is why the push nag is at 2.

## Common requests → workflow

| The human says | Do |
|---|---|
| "make it pop / look better" | `frontend-design` brief → apply one direction → screenshot → offer one alternative; reuse the direction everywhere after |
| "add a thing where people can …" | restate; ask only if the demo changes and switching is expensive; one-paragraph plan into SPEC.md; build; check; commit |
| "this feels off" | screenshot; check it against the design skill's tells; 2–3 specific guesses as options; fix after they pick |
| "it's broken" | `/debug` on the last thing shown |
| "make the X sponsor challenge count" | fetch X's docs; ask where it does real work (2–3 options + wireframe); env var + fallback; key asked once at the end |
| "we have N hours left" | Phase 5 rules: check, status, one next action |
| several things at once | build the clear ones (one commit each), ask about the rest in one question set |
| "keep going, I'm going to sleep" | must-haves in order; stop at the first taste question; WAITING ON YOU in Current status |
