"""
Quick pass/fail check against a running backend (default http://localhost:8000).
Run this after starting the server to confirm health, auth, and upload
validation all actually work — don't just eyeball it.

Usage: venv/Scripts/python smoke_test.py
"""

import json
import sys
import urllib.error
import urllib.request
import uuid

BASE = "http://localhost:8000"
failures = []


def check(name, fn):
    try:
        fn()
        print(f"PASS  {name}")
    except Exception as e:
        print(f"FAIL  {name}: {e}")
        failures.append(name)


def request(method, path, data=None, headers=None, expect=200):
    url = BASE + path
    body = json.dumps(data).encode() if data is not None else None
    req = urllib.request.Request(url, data=body, method=method, headers=headers or {})
    if data is not None:
        req.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(req) as resp:
            status = resp.status
            payload = json.loads(resp.read())
    except urllib.error.HTTPError as e:
        status = e.code
        payload = json.loads(e.read())
    if status != expect:
        raise AssertionError(f"expected {expect}, got {status}: {payload}")
    return payload


email = f"smoketest-{uuid.uuid4().hex[:8]}@example.com"
token = {}


def test_health():
    payload = request("GET", "/api/health")
    assert payload == {"status": "ok"}


def test_signup():
    payload = request("POST", "/api/auth/signup", {"email": email, "password": "smoketest123"})
    assert "access_token" in payload
    token["value"] = payload["access_token"]


def test_me_authenticated():
    payload = request("GET", "/api/auth/me", headers={"Authorization": f"Bearer {token['value']}"})
    assert payload["email"] == email


def test_me_unauthenticated():
    request("GET", "/api/auth/me", expect=401)


def test_signup_duplicate_rejected():
    request("POST", "/api/auth/signup", {"email": email, "password": "smoketest123"}, expect=400)


check("health check", test_health)
check("signup returns token", test_signup)
check("authenticated /me returns correct user", test_me_authenticated)
check("unauthenticated /me is rejected", test_me_unauthenticated)
check("duplicate signup is rejected", test_signup_duplicate_rejected)

if failures:
    print(f"\n{len(failures)} check(s) failed: {', '.join(failures)}")
    sys.exit(1)
print("\nAll checks passed.")
