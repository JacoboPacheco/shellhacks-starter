# Working on the gaming PC from the laptop

The plan: the laptop is a thin client; Claude Code, the servers, and the repo all run on the gaming PC. The laptop reaches it over Tailscale + VS Code Remote-SSH, with Parsec as a fallback.

## Setup checklist
- [x] Laptop: Tailscale installed and signed in (`tailscale status` shows it)
- [x] Laptop: VS Code Remote-SSH extension installed
- [x] Laptop: Parsec installed
- [ ] Gaming PC: everything below

## Gaming PC, in order

1. Get `setup-gaming-pc.ps1` onto the gaming PC. The PC has no git yet, so you can't clone first:
   - If the PC is signed into the same OneDrive, it's already at `Documents\Projects\shellhacks-starter\setup-gaming-pc.ps1`.
   - Otherwise, copy just that file over with a USB stick or email it to yourself.

   Then, in PowerShell in that folder: `powershell -ExecutionPolicy Bypass -File .\setup-gaming-pc.ps1` (it installs git/node/python/Tailscale).
2. Sign into Tailscale on the gaming PC with the **same account** as the laptop.
   - **Pause Windows Update for the week:** Settings → Windows Update → Pause updates. An overnight reboot brings Tailscale and SSH back, but not your Claude session or dev servers.
   - **Stop the gaming PC from ever sleeping:** Settings → System → Power → Screen and sleep → "When plugged in, put my device to sleep after" → **Never**. A sleeping PC drops off Tailscale and nothing can wake it remotely — this is the easiest way to get locked out mid-hackathon. (Turning the screen off is fine.)
   - Also worth setting: BIOS "Restore on AC power loss" → **Power On**, so a power blip at home doesn't leave it off for the rest of the event.
3. In an admin PowerShell on the gaming PC, enable OpenSSH Server (commands are printed at the end of the setup script).
4. Back on the laptop, run `tailscale status` — you should now see both the laptop and the gaming PC listed.
5. Test the connection: `ssh <your-windows-username>@<gaming-pc-tailscale-hostname>` — if this logs you in, SSH works.
6. In VS Code on the laptop: Command Palette → "Remote-SSH: Connect to Host..." → enter `<username>@<gaming-pc-tailscale-hostname>`. Open a terminal there and run `git --version` — you're now working on the PC.
7. **The real test, off your home network**: tether the laptop to your phone hotspot (not home wifi) and repeat steps 4-6. This is the actual practice — confirming it works from an arbitrary network, since that's the condition at the venue.
8. If SSH/Remote-SSH gives you trouble, Parsec is the fallback — open the Parsec app on both machines, sign into the same account, and connect for full remote desktop instead of a terminal.

## Day-to-day over Remote-SSH

- Everything happens in VS Code's remote window: its terminal, its file explorer, and Claude Code all run on the PC.
- Dev servers: open two VS Code terminals — one for the backend command, one for the frontend command (both in CLAUDE.md → Commands). **Don't use `dev.ps1` over SSH**; it opens windows on the PC's own screen where you can't see them.
- Seeing the app: when Vite prints `http://localhost:5173`, VS Code forwards the port and the link works in the laptop's browser. If not, Ports panel → Forward a Port → 5173. Only 5173 is needed; the frontend proxies `/api` to the backend on the PC.
- Claude's browser checks run on the PC too. When you want to look yourself, use the forwarded 5173 in your laptop browser.

## If the connection drops, the PC rebooted, or the PC is gone

Your work is safe if it's committed (and safer if pushed — Claude nags at 2 unpushed commits for this reason). In order:

1. **Connection dropped:** VS Code → Remote-SSH reconnect. The terminal usually comes back with Claude still running mid-turn. Say "continue" and it does.
2. **Session gone (PC rebooted, terminal closed):** open a VS Code terminal on the PC, `cd C:\dev\<project>`, then `claude --continue`. First message: "run git status and git diff --stat, read Current status and Decisions in CLAUDE.md, and tell me where we were." Then restart the two dev servers.
3. **PC unreachable at the venue:** work on the laptop. `gh repo clone <you>/<project>` into `C:\dev`, do the README one-time setup (new `JWT_SECRET`), `claude`. You lose only whatever wasn't pushed. Claude sessions don't move between machines — the repo, CLAUDE.md's Current status / Decisions, and SPEC.md are the memory.

## Why this matters

Not being able to reach the gaming PC from an unfamiliar network is the single most likely way this whole plan falls apart at the venue. Test it now, while a fix is a Google search away, not at 11pm mid-build.
