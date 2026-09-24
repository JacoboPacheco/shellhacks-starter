# Remote path (item 4)

## Current state (verified during practice)
- Laptop: Tailscale installed, signed in, connected. Tailscale hostname `raccoonlaptop`, Tailscale IP `100.104.202.72`.
- Gaming PC: not set up yet — do this once you're home, via `setup-gaming-pc.ps1`.
- VS Code: Remote-SSH extension installed on the laptop.
- Parsec: installed on the laptop (as a fallback if SSH/Remote-SSH has issues).

## Once you're home, in order

1. Run `setup-gaming-pc.ps1` on the gaming PC (installs git/node/python/Tailscale).
2. Sign into Tailscale on the gaming PC with the **same account** as the laptop.
3. In an admin PowerShell on the gaming PC, enable OpenSSH Server (commands are printed at the end of the setup script).
4. Back on the laptop, run `tailscale status` — you should now see both `raccoonlaptop` and the gaming PC's Tailscale hostname listed.
5. Test the connection: `ssh <your-windows-username>@<gaming-pc-tailscale-hostname>` — if this logs you in, SSH works.
6. In VS Code on the laptop: Command Palette → "Remote-SSH: Connect to Host..." → enter `<username>@<gaming-pc-tailscale-hostname>`.
7. **The real test, off your home network**: tether the laptop to your phone hotspot (not home wifi) and repeat steps 4-6. This is the actual practice — confirming it works from an arbitrary network, since that's the condition at the venue.
8. If SSH/Remote-SSH gives you trouble, Parsec is the fallback — open the Parsec app on both machines, sign into the same account, and connect for full remote desktop instead of a terminal.

## Why this matters

Not being able to reach the gaming PC from an unfamiliar network is the single most likely way this whole plan falls apart at the venue. Test it now, while a fix is a Google search away, not at 11pm mid-build.
