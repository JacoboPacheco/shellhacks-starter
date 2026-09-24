#!/usr/bin/env bash
# One command that proves the app works: frontend lint + build, then the
# backend smoke test against a real running server. Exits non-zero on any
# failure. Used by Claude Code (/check), by CI, and by you.
#
# Usage (from repo root, Git Bash or any bash): bash scripts/check.sh

set -uo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
PORT=8765
failed=()

if [ -x "$ROOT/backend/venv/Scripts/python.exe" ]; then
  PY="$ROOT/backend/venv/Scripts/python.exe"
elif [ -x "$ROOT/backend/venv/bin/python" ]; then
  PY="$ROOT/backend/venv/bin/python"
else
  PY="python"
fi

stop_server() {
  if command -v taskkill >/dev/null 2>&1; then
    for pid in $(netstat -ano 2>/dev/null | grep LISTENING | grep ":$PORT " | awk '{print $5}' | sort -u); do
      taskkill //F //PID "$pid" >/dev/null 2>&1
    done
  elif [ -n "${SERVER_PID:-}" ]; then
    kill "$SERVER_PID" 2>/dev/null
  fi
  rm -f "$ROOT/backend/check.db"
}
trap stop_server EXIT

echo "== frontend lint =="
(cd "$ROOT/frontend" && npm run lint --silent) || failed+=("frontend lint")

echo "== frontend build =="
(cd "$ROOT/frontend" && npm run build --silent >/dev/null) && echo "build ok" || failed+=("frontend build")

echo "== backend smoke test (live server on :$PORT) =="
# a server left over from a crashed run would answer the health check with stale code
stop_server
if curl -sf "http://localhost:$PORT/api/health" >/dev/null 2>&1; then
  echo "port $PORT is already serving something else — stop it and rerun"
  exit 1
fi
rm -f "$ROOT/backend/check.db"
# exec so SERVER_PID is the server itself, not a wrapper subshell
(cd "$ROOT/backend" && JWT_SECRET="${JWT_SECRET:-check-only-secret}" DATABASE_URL="sqlite:///./check.db" \
  exec "$PY" -m uvicorn main:app --port "$PORT" > "$ROOT/backend/check-server.log" 2>&1) &
SERVER_PID=$!

up=0
for _ in $(seq 1 20); do
  if curl -sf "http://localhost:$PORT/api/health" >/dev/null 2>&1; then up=1; break; fi
  sleep 0.5
done

if [ "$up" -eq 1 ]; then
  (cd "$ROOT/backend" && SMOKE_BASE_URL="http://localhost:$PORT" "$PY" smoke_test.py) || failed+=("backend smoke test")
else
  echo "backend never came up — last server output:"
  tail -20 "$ROOT/backend/check-server.log"
  failed+=("backend startup")
fi

echo
if [ ${#failed[@]} -eq 0 ]; then
  echo "ALL CHECKS PASSED"
  exit 0
fi
echo "FAILED: ${failed[*]}"
exit 1
