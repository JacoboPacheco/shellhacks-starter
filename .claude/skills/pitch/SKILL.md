---
name: pitch
description: Draft the 2-minute demo script and the Devpost writeup from what was actually built. Only runs when the user types /pitch.
disable-model-invocation: true
---

Write the pitch for what exists, not what was planned. Extra notes from the user: $ARGUMENTS

1. Gather facts, don't invent them: read SPEC.md and CLAUDE.md (Idea, Sponsor challenges, Current status), skim `git log --oneline`, and run `bash scripts/check.sh`. Anything that's broken or unfinished is left out of the demo path or named honestly as "next".
2. Write `PITCH.md` with:
   - **30-second version first:** three sentences — who it's for and the problem, what it does, the one impressive thing — for the hallway, the table before the judge sits down, and the Devpost tagline. The user memorizes this one.
   - **Demo script (≤ 2 minutes, spoken):** the problem in one sentence, then the exact clicks a judge sees in order, then the one technically interesting thing under the hood, then what's next. Mark each step with what to say and what to click. Put the most impressive moment in the first 30 seconds. Make sure the script visibly hits all five judging criteria: Completion (show it working end to end, no "imagine this part"), Design (let the UI breathe for a beat), Technology (name the hard part in one sentence), Originality (the twist), Practicality (who uses it and how, in one line).
   - **Devpost writeup:** Inspiration, What it does, How we built it (stack + the interesting technical piece), Challenges, Accomplishments, What's next. Plain language, no hype words. Include the sponsor challenges it qualifies for and why, one line each.
   - **Disclosure line** (rules require it): "Auth, upload, deploy, and CI scaffolding came from a starter template I built before the event; the [project name] itself and all its features were built during ShellHacks." Adapt the wording to what's true.
   - **Judge Q&A:** 5 likely questions with one-sentence answers (e.g. "what happens with bad input?", "how would this scale?", "what did the AI tools do vs. you?"). Answer the AI one honestly.
3. Keep it tight: the whole file under 120 lines. The user will read it out loud, so short sentences.
   Also rewrite the top of `README.md` for the project (judges click the repo link): name, one-paragraph description, the live URL, a screenshot placeholder, how to run it locally, and the disclosure line. Move the starter-kit notes below it under "Development".
4. Screenshots for Devpost and the README: with the app running, use the `webapp-testing` skill (Python Playwright; running `python` scripts may trigger a permission prompt — that's expected) to save `docs/screenshots/01-<screen>.png` … for the 3–4 screens in the demo script, at 1280×800 with real demo data on screen (run `backend/seed.py` first if the data is missing). Reference them from README.md.
5. Tell the user to time themselves reading the script once — if it's over 2 minutes, cut the "what's next" section first.
