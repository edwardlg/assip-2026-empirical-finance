#!/usr/bin/env python3
"""
build_video_map.py -- recover YouTube links after manual bulk upload.

Path A (manual upload): you bulk-upload the clips to @LeiGao-gmu keeping the
generated titles, which begin with a stable code "[MEF Wx.y Pn]". This script
reads the channel's PUBLIC uploads via the YouTube Data API (read-only, API key
-- NO OAuth, no quota/audit headaches), parses those codes, and writes
video-map.json keyed by item_id, which the site include (video-embed.html)
consumes to embed the right clips on each subchapter page.

  export YOUTUBE_API_KEY=...          # a free read-only Data API key
  python tools/build_video_map.py [--handle @LeiGao-gmu] [--out video-map.json]

Reads codePrefix -> item_id from book/decks/chapters/_buildout_items.json.
"""
from __future__ import annotations
import argparse, json, os, re, urllib.parse, urllib.request

API = "https://www.googleapis.com/youtube/v3"
CODE_RE = re.compile(r"\[MEF\s+([A-Za-z0-9.]+)\s+P(\d+)\]\s*(.*)")


def api(path: str, **params) -> dict:
    key = os.environ.get("YOUTUBE_API_KEY")
    if not key:
        raise SystemExit("Set YOUTUBE_API_KEY (a free read-only YouTube Data API key).")
    params["key"] = key
    url = f"{API}/{path}?" + urllib.parse.urlencode(params)
    with urllib.request.urlopen(url) as r:
        return json.load(r)


def uploads_playlist(handle: str) -> str:
    d = api("channels", part="contentDetails", forHandle=handle.lstrip("@"))
    items = d.get("items", [])
    if not items:
        raise SystemExit(f"channel {handle} not found (check the handle).")
    return items[0]["contentDetails"]["relatedPlaylists"]["uploads"]


def all_uploads(playlist_id: str) -> list[tuple[str, str]]:
    vids, token = [], None
    while True:
        d = api("playlistItems", part="snippet,contentDetails",
                playlistId=playlist_id, maxResults=50,
                **({"pageToken": token} if token else {}))
        for it in d.get("items", []):
            vids.append((it["snippet"]["title"], it["contentDetails"]["videoId"]))
        token = d.get("nextPageToken")
        if not token:
            return vids


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--handle", default="@LeiGao-gmu")
    ap.add_argument("--items", default="book/decks/chapters/_buildout_items.json")
    ap.add_argument("--out", default="video-map.json")
    a = ap.parse_args()

    code2item = {it["codePrefix"]: it["outPrefix"] for it in json.load(open(a.items))}
    vmap: dict[str, list] = {}
    unmatched = []
    for title, vid in all_uploads(uploads_playlist(a.handle)):
        m = CODE_RE.search(title)
        if not m:
            continue
        code, part, disp = m.group(1), int(m.group(2)), m.group(3).strip()
        item = code2item.get(code)
        if not item:
            unmatched.append(title)
            continue
        vmap.setdefault(item, []).append({"part": part, "youtube_id": vid, "title": disp})
    for item in vmap:
        vmap[item].sort(key=lambda x: x["part"])

    json.dump(vmap, open(a.out, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    n = sum(len(v) for v in vmap.values())
    print(f"wrote {a.out}: {n} clips mapped across {len(vmap)} items")
    if unmatched:
        print(f"NOTE: {len(unmatched)} uploaded titles had no parseable [MEF ..] code "
              f"(e.g. {unmatched[0][:60]!r}) — they were skipped.")


if __name__ == "__main__":
    main()
