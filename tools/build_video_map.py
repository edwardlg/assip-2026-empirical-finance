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

Dry run (no API, no upload needed) -- prove the parse/map pipeline offline using
the titles YouTube will receive (one per line; optional TAB-separated videoId):
  ls videos/upload_ready/**/*.mp4 | sed 's#.*/##; s#\\.mp4$##' > /tmp/titles.txt
  python tools/build_video_map.py --titles-from /tmp/titles.txt --out /tmp/preview.json

NOTE: an API-key (unauthenticated) read of the uploads playlist returns only
PUBLIC videos -- upload as Public (not Unlisted/Private) or the script won't see
them. Both editions share one channel; this script's [MEF] regex matches only its
own videos and ignores the other edition's, so running it on the shared channel
is safe.

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


def titles_from_file(path: str) -> list[tuple[str, str]]:
    """Offline source: one title per line, optional TAB-separated videoId.
    Lines without an id get a DRYRUN_NNNN placeholder so the shape is real."""
    pairs = []
    for i, line in enumerate(open(path, encoding="utf-8")):
        line = line.rstrip("\n")
        if not line.strip():
            continue
        title, _, vid = line.partition("\t")
        pairs.append((title, vid.strip() or f"DRYRUN_{i:04d}"))
    return pairs


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--handle", default="@LeiGao-gmu")
    ap.add_argument("--items", default="book/decks/chapters/_buildout_items.json")
    ap.add_argument("--out", default="video-map.json")
    ap.add_argument("--titles-from", metavar="FILE",
                    help="dry run: read titles from FILE instead of the YouTube API")
    a = ap.parse_args()

    items = json.load(open(a.items))
    code2item = {it["codePrefix"]: it["outPrefix"] for it in items}

    if a.titles_from:
        pairs = titles_from_file(a.titles_from)
        source = f"{a.titles_from} (dry run, {len(pairs)} titles)"
    else:
        pairs = all_uploads(uploads_playlist(a.handle))
        source = f"{a.handle} ({len(pairs)} uploads)"

    vmap: dict[str, list] = {}
    unmatched = []
    for title, vid in pairs:
        m = CODE_RE.search(title)
        if not m:
            continue                       # other edition / unrelated video
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
    print(f"read {source}")
    print(f"wrote {a.out}: {n} clips mapped across {len(vmap)}/{len(items)} items")

    # Coverage report: which subchapters still have no video?
    missing = [it["outPrefix"] for it in items if it["outPrefix"] not in vmap]
    if missing:
        head = ", ".join(missing[:12]) + (" ..." if len(missing) > 12 else "")
        print(f"WARNING: {len(missing)} item(s) have NO video yet: {head}")
    else:
        print("coverage: every subchapter item has at least one clip ✓")
    if unmatched:
        print(f"NOTE: {len(unmatched)} title(s) carried a code not in {a.items} "
              f"(skipped): e.g. {unmatched[0][:60]!r}")


if __name__ == "__main__":
    main()
