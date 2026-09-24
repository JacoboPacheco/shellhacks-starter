"""
Quick pass/fail check against a running backend (default http://localhost:8000).
Run this after starting the server to confirm health, auth, and upload
validation all actually work — don't just eyeball it.

Usage: venv/Scripts/python smoke_test.py
"""

import base64
import json
import sys
import urllib.error
import urllib.request
import uuid

# smallest possible valid PNG (1x1 transparent pixel)
TINY_PNG = base64.b64decode(
    "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNk+A8AAQUBAScY42YAAAAASUVORK5CYII="
)

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


def upload(filename, content_type, data_bytes, expect=200):
    boundary = uuid.uuid4().hex
    body = (
        f"--{boundary}\r\n"
        f'Content-Disposition: form-data; name="file"; filename="{filename}"\r\n'
        f"Content-Type: {content_type}\r\n\r\n"
    ).encode() + data_bytes + f"\r\n--{boundary}--\r\n".encode()
    req = urllib.request.Request(
        BASE + "/api/upload",
        data=body,
        method="POST",
        headers={"Content-Type": f"multipart/form-data; boundary={boundary}"},
    )
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


def test_upload_valid_image():
    payload = upload("test.png", "image/png", TINY_PNG)
    assert payload["filename"].endswith(".png")


def test_upload_wrong_type_rejected():
    upload("test.txt", "text/plain", b"hello world", expect=400)


check("health check", test_health)
check("signup returns token", test_signup)
check("authenticated /me returns correct user", test_me_authenticated)
check("unauthenticated /me is rejected", test_me_unauthenticated)
check("duplicate signup is rejected", test_signup_duplicate_rejected)
check("valid image upload accepted", test_upload_valid_image)
check("non-image upload rejected", test_upload_wrong_type_rejected)

if failures:
    print(f"\n{len(failures)} check(s) failed: {', '.join(failures)}")
    sys.exit(1)
print("\nAll checks passed.")
