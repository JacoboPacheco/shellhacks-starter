# Run this on the gaming PC once you're home (item 4 prep).
# Installs everything needed to build + run this repo and to reach the PC remotely.
# Run from a normal PowerShell window — no Administrator needed for winget or the Claude installer.

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
Write-Host ""
Write-Host "Then open Tailscale from the Start menu and sign in with the SAME account you used on the laptop." -ForegroundColor Yellow
