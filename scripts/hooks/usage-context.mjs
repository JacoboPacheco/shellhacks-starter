// UserPromptSubmit hook: tell Claude, on every prompt, how much of the usage
// limits are left (from the snapshot the status line writes), so it can follow
// the Budget rules in CLAUDE.md. Silent if there's no fresh snapshot.
import { readFileSync } from 'node:fs'
import { join } from 'node:path'

const MAX_AGE_MS = 20 * 60 * 1000

function relative(epochSeconds) {
  const ms = epochSeconds * 1000 - Date.now()
  if (ms <= 0) return 'now'
  const h = Math.floor(ms / 3_600_000)
  const m = Math.round((ms % 3_600_000) / 60_000)
  const at = new Date(epochSeconds * 1000).toLocaleTimeString([], { hour: 'numeric', minute: '2-digit' })
  return `${h ? `${h}h ` : ''}${m}m (at ${at})`
}

try {
  let cwd = process.env.CLAUDE_PROJECT_DIR
  if (!cwd) {
    try {
      cwd = JSON.parse(readFileSync(0, 'utf8') || '{}').cwd
    } catch {}
  }
  const snap = JSON.parse(readFileSync(join(cwd || process.cwd(), '.claude', 'tmp', 'usage.json'), 'utf8'))
  if (Date.now() - snap.ts > MAX_AGE_MS) process.exit(0)

  const parts = []
  if (snap.five_hour?.used_percentage != null) {
    parts.push(`5-hour limit ${Math.round(snap.five_hour.used_percentage)}% used, resets in ${relative(snap.five_hour.resets_at)}`)
  }
  if (snap.seven_day?.used_percentage != null) {
    parts.push(`weekly limit ${Math.round(snap.seven_day.used_percentage)}% used`)
  }
  if (snap.context_pct != null) parts.push(`context ${Math.round(snap.context_pct)}% full`)
  if (!parts.length) process.exit(0)

  process.stdout.write(
    JSON.stringify({
      hookSpecificOutput: {
        hookEventName: 'UserPromptSubmit',
        additionalContext: `Budget right now: ${parts.join('; ')}. Apply the Budget section of CLAUDE.md.`,
      },
    })
  )
} catch {
  // no snapshot yet, or unreadable — say nothing
}
process.exit(0)
