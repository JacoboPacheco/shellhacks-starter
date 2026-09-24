# Run this on the gaming PC once you're home (item 4 prep).
# Installs everything needed to build + run this repo and to reach the PC remotely.
# Fresh Windows blocks .ps1 scripts by default, so run it like this from a normal PowerShell window
# (no Administrator needed):
#   powershell -ExecutionPolicy Bypass -File .\setup-gaming-pc.ps1

Write-Host "=== Installing Git ===" -ForegroundColor Cyan
winget install --id Git.Git -e --source winget

Write-Host "=== Installing Node.js LTS ===" -ForegroundColor Cyan
winget install --id OpenJS.NodeJS.LTS -e --source winget

Write-Host "=== Installing Python ===" -ForegroundColor Cyan
winget install --id Python.Python.3.13 -e --source winget

Write-Host "=== Installing Tailscale ===" -ForegroundColor Cyan
winget install --id Tailscale.Tailscale -e --source winget

Write-Host ""
Write-Host "winget installs done. Close this window and open a NEW PowerShell so PATH updates take effect." -ForegroundColor Yellow
Write-Host ""
Write-Host "Then, in the new window, run:" -ForegroundColor Yellow
Write-Host "  irm https://claude.ai/install.ps1 | iex        # installs Claude Code"
Write-Host "  git --version; node --version; python --version; claude --version"
Write-Host "  claude        # first run: pick your Claude subscription login and sign in in the browser"
Write-Host "  (the repo's .claude/settings.json installs the frontend-design and example-skills plugins when you first open it)"
Write-Host ""
Write-Host "Then open Tailscale from the Start menu and sign in with the SAME account you used on the laptop." -ForegroundColor Yellow
Write-Host ""
Write-Host "=== One more step, in an ADMIN PowerShell (right-click Start > Terminal (Admin)) ===" -ForegroundColor Yellow
Write-Host "VS Code Remote-SSH needs an SSH server running on this PC to connect into. Run these there:" -ForegroundColor Yellow
Write-Host '  Add-WindowsCapability -Online -Name OpenSSH.Server~~~~0.0.1.0'
Write-Host "  Start-Service sshd"
Write-Host "  Set-Service -Name sshd -StartupType Automatic"
Write-Host ""
Write-Host "Optional: let this repo's scripts (.\dev.ps1, .\check.ps1) run directly instead of needing" -ForegroundColor Yellow
Write-Host "'powershell -ExecutionPolicy Bypass -File ...' every time. This is your choice - it only affects your user account:" -ForegroundColor Yellow
Write-Host "  Set-ExecutionPolicy -Scope CurrentUser RemoteSigned"
Write-Host ""
Write-Host "Then from the LAPTOP, once both machines show up in 'tailscale status', connect with:" -ForegroundColor Yellow
Write-Host "  ssh <windows-username>@<gaming-pc-tailscale-ip-or-hostname>"
Write-Host "See REMOTE.md for this laptop's Tailscale identity and the exact commands to try first."
