#!/usr/bin/env python3
"""
set_playlist_public.py -- flip every video in one or more YouTube playlists to a
target visibility (default: public), authorized as the channel OWNER.

Why owner OAuth with WRITE scope: changing a video's privacy is videos.update,
which needs the `youtube` (manage-your-account) scope -- see tools/yt_oauth.py
for the one-time Cloud Console setup. An API key or the read-only token cannot.

Careful by design:
  * READ-MODIFY-WRITE per video. videos.update REPLACES the whole `status` part,
    so we fetch the current status and change privacyStatus while round-tripping
    the other mutable fields -- `embeddable` (our lessons are embedded on the
    site!), `license`, and the made-for-kids self-declaration. Blindly sending
    {privacyStatus} would reset the rest. (A scheduled `publishAt` is not carried
    over -- making a video public/unlisted takes effect now, not on a schedule.)
  * --dry-run prints what WOULD change and writes nothing.
  * Without --yes you get a confirmation prompt before anything is modified.
  * Videos already at the target visibility are skipped (no wasted quota).

Usage:
  python tools/set_playlist_public.py PLGUlAx2L0tq4                 # -> public (asks first)
  python tools/set_playlist_public.py PLxxxx PLyyyy --dry-run       # preview only
  python tools/set_playlist_public.py PLxxxx --visibility unlisted --yes

Quota note: videos.update costs 50 units each (list calls cost 1); the default
daily quota is 10,000 units, so ~180-190 visibility changes/day.
"""
from __future__ import annotations
import argparse, json, sys, urllib.error

from yt_oauth import (get_access_token, authorized_get, authorized_request,
                      SCOPE_WRITE, DEFAULT_TOKEN_WRITE)

VISIBILITIES = ("public", "unlisted", "private")
# Mutable status fields we round-trip so videos.update doesn't reset them.
WRITABLE_STATUS = ("license", "embeddable", "publicStatsViewable")


def playlist_items(fetch, playlist_id):
    """All (videoId, title, privacyStatus) in a playlist, following pagination."""
    out, token = [], None
    while True:
        d = fetch("playlistItems", part="snippet,status", playlistId=playlist_id,
                  maxResults=50, **({"pageToken": token} if token else {}))
        for it in d.get("items", []):
            vid = it.get("snippet", {}).get("resourceId", {}).get("videoId")
            title = it.get("snippet", {}).get("title", "(untitled)")
            privacy = it.get("status", {}).get("privacyStatus")
            if vid:
                out.append((vid, title, privacy))
        token = d.get("nextPageToken")
        if not token:
            return out


def current_status(fetch, video_id):
    d = fetch("videos", part="status", id=video_id)
    items = d.get("items", [])
    return items[0]["status"] if items else None


def new_status(cur, visibility):
    """Preserve mutable status fields; change only privacyStatus.

    videos.update on the status part requires the made-for-kids self-declaration,
    so always send it -- preserving the current designation, defaulting to False
    (correct for lecture content) when the channel never set one."""
    ns = {k: cur[k] for k in WRITABLE_STATUS if k in cur}
    ns["privacyStatus"] = visibility
    ns["selfDeclaredMadeForKids"] = bool(cur.get("selfDeclaredMadeForKids",
                                                 cur.get("madeForKids", False)))
    return ns


def _err(e: urllib.error.HTTPError) -> tuple[str, str]:
    """Return (human message, primary reason) from a YouTube API error body."""
    try:
        er = json.loads(e.read()).get("error", {})
        reason = (er.get("errors") or [{}])[0].get("reason", "")
        return er.get("message", str(e.code)), reason
    except Exception:
        return getattr(e, "reason", str(e)), ""


def main():
    ap = argparse.ArgumentParser(description="Set every video in a playlist to a visibility.")
    ap.add_argument("playlists", nargs="+", metavar="PLAYLIST_ID",
                    help="one or more playlist IDs (e.g. PLGUlAx2L0tq4)")
    ap.add_argument("--visibility", choices=VISIBILITIES, default="public")
    ap.add_argument("--client-secrets", metavar="PATH",
                    help="OAuth client_secrets.json (default ~/.config/leigao-video/ or $GOOGLE_CLIENT_SECRETS)")
    ap.add_argument("--reauth", action="store_true", help="force a fresh OAuth login")
    ap.add_argument("--dry-run", action="store_true", help="show what would change; write nothing")
    ap.add_argument("--yes", action="store_true", help="skip the confirmation prompt")
    a = ap.parse_args()

    token = get_access_token(a.client_secrets, cache_path=DEFAULT_TOKEN_WRITE,
                             force_login=a.reauth, scope=SCOPE_WRITE)
    def fetch(path, **p):
        return authorized_get(path, token, **p)

    # Gather targets across all playlists, de-duped by video id (a clip may recur).
    seen, targets = set(), []
    for pl in a.playlists:
        try:
            vids = playlist_items(fetch, pl)
        except urllib.error.HTTPError as e:
            msg, _ = _err(e)
            print(f"{pl}: cannot read playlist (HTTP {e.code}: {msg}) — skipping.")
            continue
        already = sum(1 for _, _, pv in vids if pv == a.visibility)
        print(f"{pl}: {len(vids)} videos ({already} already {a.visibility})")
        for vid, title, privacy in vids:
            if vid in seen:
                continue
            seen.add(vid)
            targets.append((vid, title, privacy))

    todo = [(v, t) for (v, t, pv) in targets if pv != a.visibility]
    print(f"\n{len(targets)} unique video(s); {len(todo)} to change to '{a.visibility}'.")
    if not todo:
        print("nothing to do — all already at target visibility." if targets
              else "no videos found (check the playlist IDs and that you own them).")
        return

    if a.dry_run:
        for vid, title in todo:
            print(f"  [dry] {vid}  {title[:64]}")
        print("\n(dry run — nothing changed)")
        return

    if not a.yes:
        if not sys.stdin.isatty():
            raise SystemExit("refusing to modify videos non-interactively; re-run with --yes (after a --dry-run).")
        if input(f"Change {len(todo)} video(s) to {a.visibility}? type 'yes': ").strip().lower() != "yes":
            raise SystemExit("aborted.")

    changed = skipped = failed = 0
    for vid, title in todo:
        try:
            st = current_status(fetch, vid)
            if st is None:
                print(f"  ? {vid} not accessible: {title[:48]}"); failed += 1; continue
            if st.get("privacyStatus") == a.visibility:      # changed since we listed
                skipped += 1; continue
            authorized_request("PUT", "videos", token,
                               body={"id": vid, "status": new_status(st, a.visibility)},
                               part="status")
            changed += 1
            print(f"  ✓ {a.visibility}: {title[:64]}")
        except urllib.error.HTTPError as e:
            msg, reason = _err(e)
            failed += 1
            print(f"  ✗ {vid} HTTP {e.code} {reason or ''}: {msg[:70]} ({title[:32]})")
            if reason in ("quotaExceeded", "dailyLimitExceeded"):
                print("  ! daily API quota exhausted — re-run tomorrow or raise the quota; "
                      "already-changed videos stay changed.")
                break

    print(f"\ndone: {changed} changed, {skipped} already {a.visibility}, {failed} failed")


if __name__ == "__main__":
    main()
