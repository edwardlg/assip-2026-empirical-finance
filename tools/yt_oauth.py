#!/usr/bin/env python3
"""
yt_oauth.py -- minimal, dependency-free OAuth (device flow) for reading a
channel owner's OWN uploads, INCLUDING unlisted/private videos, via the YouTube
Data API. A plain API key only sees PUBLIC videos; owner OAuth sees everything,
which is what build_video_map.py needs when the lessons are uploaded Unlisted.

Read-only scope. No third-party libraries (urllib only). Uses the OAuth 2.0
"device" flow: you open a URL on any device and type a short code -- no localhost
redirect, so it works cleanly over SSH/WSL.

ONE-TIME SETUP (channel owner):
  1. Google Cloud Console -> APIs & Services -> Library -> enable
     "YouTube Data API v3".
  2. APIs & Services -> OAuth consent screen:
       - User type: External
       - Add your own Google account under "Test users"
       - (Sensitive scope youtube.readonly + "Testing" status is fine for personal
          use. Note: in Testing, refresh tokens expire after ~7 days -- if a run
          says it must re-authorize, just approve the code again.)
  3. APIs & Services -> Credentials -> Create credentials -> OAuth client ID ->
     Application type: "TVs and Limited Input devices". Download the JSON.
  4. Save that JSON as:  ~/.config/leigao-video/client_secrets.json
     (or pass --client-secrets PATH, or set GOOGLE_CLIENT_SECRETS=PATH)

The access/refresh token is cached at ~/.config/leigao-video/yt_token.json
(mode 0600). Never commit client_secrets.json or yt_token.json.
"""
from __future__ import annotations
import json, os, time, urllib.error, urllib.parse, urllib.request
from pathlib import Path

SCOPE = "https://www.googleapis.com/auth/youtube.readonly"
DEVICE_CODE_URL = "https://oauth2.googleapis.com/device/code"
TOKEN_URL = "https://oauth2.googleapis.com/token"
DEVICE_GRANT = "urn:ietf:params:oauth:grant-type:device_code"

CONF_DIR = Path(os.environ.get("LEIGAO_VIDEO_CONF", Path.home() / ".config" / "leigao-video"))
DEFAULT_SECRETS = CONF_DIR / "client_secrets.json"
DEFAULT_TOKEN = CONF_DIR / "yt_token.json"


def _post(url: str, **params) -> dict:
    """POST form-urlencoded; return parsed JSON even for 4xx (OAuth error bodies)."""
    data = urllib.parse.urlencode(params).encode()
    req = urllib.request.Request(
        url, data=data, method="POST",
        headers={"Content-Type": "application/x-www-form-urlencoded"})
    try:
        with urllib.request.urlopen(req) as r:
            return json.load(r)
    except urllib.error.HTTPError as e:
        try:
            return json.load(e)
        except Exception:
            raise SystemExit(f"OAuth POST {url} failed: HTTP {e.code}")


def load_client_secrets(path: str | None) -> tuple[str, str]:
    p = Path(path) if path else Path(os.environ.get("GOOGLE_CLIENT_SECRETS", DEFAULT_SECRETS))
    if not p.exists():
        raise SystemExit(
            f"OAuth client secrets not found at {p}\n"
            "Create an OAuth client (type: 'TVs and Limited Input devices') in the\n"
            "Google Cloud Console, download the JSON, and save it there.\n"
            "See the setup notes at the top of tools/yt_oauth.py.")
    block = json.loads(p.read_text())
    block = block.get("installed") or block.get("web") or block
    if "client_id" not in block or "client_secret" not in block:
        raise SystemExit(f"{p} is not a valid OAuth client_secrets file.")
    return block["client_id"], block["client_secret"]


def _save_token(cache: Path, tok: dict) -> None:
    cache.parent.mkdir(parents=True, exist_ok=True)
    cache.write_text(json.dumps(tok))
    os.chmod(cache, 0o600)


def _device_login(client_id: str, client_secret: str, cache: Path) -> dict:
    d = _post(DEVICE_CODE_URL, client_id=client_id, scope=SCOPE)
    if "device_code" not in d:
        raise SystemExit(f"device-code request failed: {d.get('error', d)}")
    url = d.get("verification_url") or d.get("verification_uri")
    print("\n=== Authorize read-only access to your YouTube channel ===")
    print(f"  1. On any device, open:  {url}")
    print(f"  2. Enter this code:      {d['user_code']}")
    print("  (waiting for approval...)", flush=True)
    interval = int(d.get("interval", 5))
    deadline = time.time() + int(d.get("expires_in", 1800))
    while time.time() < deadline:
        time.sleep(interval)
        t = _post(TOKEN_URL, client_id=client_id, client_secret=client_secret,
                  device_code=d["device_code"], grant_type=DEVICE_GRANT)
        err = t.get("error")
        if not err:
            t["_obtained"] = int(time.time())
            _save_token(cache, t)
            print("authorized ✓\n", flush=True)
            return t
        if err == "authorization_pending":
            continue
        if err == "slow_down":
            interval += 5
            continue
        raise SystemExit(f"authorization failed: {err} ({t.get('error_description', '')})")
    raise SystemExit("authorization timed out — re-run and approve the code sooner.")


def get_access_token(client_secrets: str | None = None,
                     cache_path: str | os.PathLike = DEFAULT_TOKEN,
                     force_login: bool = False) -> str:
    """Return a usable access token: refresh the cached one, else device-login."""
    client_id, client_secret = load_client_secrets(client_secrets)
    cache = Path(cache_path)
    if not force_login and cache.exists():
        rt = json.loads(cache.read_text()).get("refresh_token")
        if rt:
            t = _post(TOKEN_URL, client_id=client_id, client_secret=client_secret,
                      refresh_token=rt, grant_type="refresh_token")
            if "access_token" in t:
                return t["access_token"]
            print(f"(cached token refresh failed: {t.get('error', '?')} — re-authorizing)")
    return _device_login(client_id, client_secret, cache)["access_token"]


def authorized_get(path: str, access_token: str,
                   api: str = "https://www.googleapis.com/youtube/v3", **params) -> dict:
    url = f"{api}/{path}?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={"Authorization": f"Bearer {access_token}"})
    with urllib.request.urlopen(req) as r:
        return json.load(r)
