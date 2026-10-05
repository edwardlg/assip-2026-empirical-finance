#!/usr/bin/env python3
"""
set_playlist_order.py -- reorder a YouTube playlist into the camp's canonical
curriculum sequence, read from each clip's "NGN W<week> <chapter> P<part>" title
code. Chapters ascend by number, then Lab (L), then Mentor (M); within each, by
part. (YouTube mangled "[NGN W1.1 P1]" into "NGN W1 1 P1" on upload, but the
week/chapter/part numbers survive, so the title alone is a reliable sort key.)

Owner OAuth, WRITE scope (see tools/yt_oauth.py). Repositions items with
playlistItems.update. Moves only items that are out of place, front-to-back, so
the number of writes ~= the number of misplaced clips (an already-sorted
playlist costs zero writes).

  python tools/set_playlist_order.py PLGUlAx2L0tq4 --dry-run   # preview only
  python tools/set_playlist_order.py PLGUlAx2L0tq4 --yes

Quota: each move = 50 units (playlistItems.update); reads are 1. A fully
reversed 56-item playlist ~= 55 moves ~= 2,750 units (free daily quota 10,000).
"""
from __future__ import annotations
import argparse, json, re, sys, urllib.error

from yt_oauth import (get_access_token, authorized_get, authorized_request,
                      SCOPE_WRITE, DEFAULT_TOKEN_WRITE)


def _err(e: urllib.error.HTTPError):
    """(message, primary reason) from a YouTube API error body."""
    try:
        er = json.loads(e.read()).get("error", {})
        return er.get("message", ""), (er.get("errors") or [{}])[0].get("reason", "")
    except Exception:
        return getattr(e, "reason", str(e)), ""

# matches "NGN W1 2 P10 ...", "NGN W1 L P1 ...", "NGN W1 M P3 ..."
CODE = re.compile(r"\bNGN\s+W(\d+)\s+([0-9A-Za-z]+)\s+P(\d+)\b")
SECTION_RANK = {"L": 100, "M": 101}   # chapters (numeric) first, then Lab, then Mentor
UNPARSED = (999, 999, 999)


def sort_key(title, fallback_pos):
    """(week, chapter_rank, part) from the title code; unparseable sorts last (stable)."""
    m = CODE.search(title)
    if not m:
        return (UNPARSED[0], UNPARSED[1], fallback_pos)
    week, ch, part = int(m.group(1)), m.group(2), int(m.group(3))
    rank = int(ch) if ch.isdigit() else SECTION_RANK.get(ch.upper(), 900)
    return (week, rank, part)


def fetch_items(fetch, playlist_id):
    items, token = [], None
    while True:
        d = fetch("playlistItems", part="snippet", playlistId=playlist_id,
                  maxResults=50, **({"pageToken": token} if token else {}))
        for it in d.get("items", []):
            sn = it["snippet"]
            items.append({"id": it["id"], "vid": sn["resourceId"]["videoId"],
                          "pos": sn["position"], "title": sn["title"]})
        token = d.get("nextPageToken")
        if not token:
            return items


def plan_moves(current, target):
    """Minimal front-to-back move list: simulate list.remove/insert to mirror how
    playlistItems.update repositions (insert at index, shift the rest down)."""
    sim = [x["id"] for x in current]
    plan = []
    for i, x in enumerate(target):
        if sim[i] != x["id"]:
            plan.append((i, x["id"]))
            sim.remove(x["id"]); sim.insert(i, x["id"])
    return plan


def reorder_one(token, fetch, pl, a):
    items = fetch_items(fetch, pl)
    if not items:
        print(f"{pl}: no items found (check the ID and that you own it)."); return
    items.sort(key=lambda x: x["pos"])                      # current order
    for x in items:
        if not CODE.search(x["title"]):
            print(f"  ! {pl}: no NGN code in title, will sort last: {x['title'][:50]!r}")
    target = sorted(items, key=lambda x: sort_key(x["title"], x["pos"]))
    plan = plan_moves(items, target)

    moved = {mid for _, mid in plan}   # mark only the items that actually get a move call
    print(f"\n{pl}: {len(items)} items; {len(plan)} move(s) for canonical order.")
    print("  target order (* = will be moved):")
    for i, x in enumerate(target):
        mark = "*" if x["id"] in moved else " "
        print(f"   {i:>2} {mark} {x['title'][:58]}")

    if a.dry_run:
        print("  (dry run — nothing moved)"); return
    if not plan:
        print("  already in canonical order ✓"); return
    if not a.yes:
        if not sys.stdin.isatty():
            raise SystemExit("refusing to reorder non-interactively; re-run with --yes (after --dry-run).")
        if input(f"Apply {len(plan)} move(s)? type 'yes': ").strip().lower() != "yes":
            raise SystemExit("aborted.")

    by_id = {x["id"]: x for x in items}
    done = fail = 0
    for pos, item_id in plan:
        x = by_id[item_id]
        try:
            authorized_request("PUT", "playlistItems", token,
                body={"id": item_id, "snippet": {
                    "playlistId": pl,
                    "resourceId": {"kind": "youtube#video", "videoId": x["vid"]},
                    "position": pos}},
                part="snippet")
            done += 1
            print(f"  -> {pos:>2}: {x['title'][:58]}")
        except urllib.error.HTTPError as e:
            fail += 1
            msg, reason = _err(e)
            print(f"  x  pos {pos}: HTTP {e.code} {reason} — {x['title'][:30]}")
            # Stop on ANY error: later moves assume this one landed, so continuing
            # could leave a stale ordering. A re-run re-fetches and re-plans.
            if reason == "manualSortRequired":
                print("  ! This playlist uses an AUTOMATIC sort order, so YouTube blocks API")
                print("    repositioning. Fix it once in YouTube Studio: open the playlist and")
                print("    set its sort to MANUAL (drag any one video to a new spot, or pick")
                print("    'Manual' from the sort menu). Then re-run. Nothing was changed.")
            elif reason in ("quotaExceeded", "dailyLimitExceeded"):
                print("  ! daily quota exhausted — re-run tomorrow; already-moved items stay put.")
            else:
                print("  ! stopping; re-run to finish (it re-plans from the live order).")
            break
    print(f"\ndone: {done} moved, {fail} failed")


def main():
    ap = argparse.ArgumentParser(description="Reorder playlist(s) into NGN curriculum order.")
    ap.add_argument("playlists", nargs="+", metavar="PLAYLIST_ID")
    ap.add_argument("--client-secrets", metavar="PATH")
    ap.add_argument("--reauth", action="store_true", help="force a fresh OAuth login")
    ap.add_argument("--dry-run", action="store_true", help="preview target order; move nothing")
    ap.add_argument("--yes", action="store_true", help="skip the confirmation prompt")
    a = ap.parse_args()

    token = get_access_token(a.client_secrets, cache_path=DEFAULT_TOKEN_WRITE,
                             force_login=a.reauth, scope=SCOPE_WRITE)
    def fetch(path, **p):
        return authorized_get(path, token, **p)

    for pl in a.playlists:
        reorder_one(token, fetch, pl, a)


if __name__ == "__main__":
    main()
