# Remote path (item 4)

## Current state (verified during practice)
- Laptop: Tailscale installed, signed in, connected (run `tailscale status` to see its name and IP).
- Gaming PC: not set up yet — step 1 below.
- VS Code: Remote-SSH extension installed on the laptop.
- Parsec: installed on the laptop (as a fallback if SSH/Remote-SSH has issues).

## Once you're home, in order

1. Get `setup-gaming-pc.ps1` onto the gaming PC. The PC has no git yet, so you can't clone first:
   - If the PC is signed into the same OneDrive, it's already at `Documents\Projects\shellhacks-starter\setup-gaming-pc.ps1`.
   - Otherwise, copy just that file over with a USB stick or email it to yourself.

   Then, in PowerShell in that folder: `powershell -ExecutionPolicy Bypass -File .\setup-gaming-pc.ps1` (it installs git/node/python/Tailscale). Once git is installed, clone the repo into `C:\dev\` — outside OneDrive — and work from that copy.
2. Sign into Tailscale on the gaming PC with the **same account** as the laptop.
   - **Stop the gaming PC from ever sleeping:** Settings → System → Power → Screen and sleep → "When plugged in, put my device to sleep after" → **Never**. A sleeping PC drops off Tailscale and nothing can wake it remotely — this is the easiest way to get locked out mid-hackathon. (Turning the screen off is fine.)
   - Also worth setting: BIOS "Restore on AC power loss" → **Power On**, so a power blip at home doesn't leave it off for the rest of the event.
3. In an admin PowerShell on the gaming PC, enable OpenSSH Server (commands are printed at the end of the setup script).
4. Back on the laptop, run `tailscale status` — you should now see both the laptop and the gaming PC listed.
5. Test the connection: `ssh <your-windows-username>@<gaming-pc-tailscale-hostname>` — if this logs you in, SSH works.
6. In VS Code on the laptop: Command Palette → "Remote-SSH: Connect to Host..." → enter `<username>@<gaming-pc-tailscale-hostname>`.
7. **The real test, off your home network**: tether the laptop to your phone hotspot (not home wifi) and repeat steps 4-6. This is the actual practice — confirming it works from an arbitrary network, since that's the condition at the venue.
8. If SSH/Remote-SSH gives you trouble, Parsec is the fallback — open the Parsec app on both machines, sign into the same account, and connect for full remote desktop instead of a terminal.

## Why this matters

Not being able to reach the gaming PC from an unfamiliar network is the single most likely way this whole plan falls apart at the venue. Test it now, while a fix is a Google search away, not at 11pm mid-build.
