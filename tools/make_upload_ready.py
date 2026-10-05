#!/usr/bin/env python3
"""
make_upload_ready.py -- build a drag-and-drop YouTube upload folder.

YouTube Studio sets a new video's title from the uploaded *filename* (minus the
extension). So we copy each rendered clip into

    videos/upload_ready/Week-N/<sanitized "[MEF Wx.y Pn] Title">.mp4

foldered by week (each folder == one playlist). Drag a week folder into Studio
-> every title auto-fills with the [MEF|NGN ...] recovery code intact; then
bulk-select the folder and add it to its playlist, and publish. After upload,
tools/build_video_map.py reads the codes back from the channel and wires the
site embeds.

Filenames must be valid on Windows/NTFS (the clips live on /mnt/e), so a few
reserved characters are replaced. The code prefix never contains reserved
characters, so recovery is always preserved. The exact, unmodified titles
remain in videos/upload_manifest.csv if you prefer to paste them.

Usage:  python make_upload_ready.py <repo_dir>
"""
from __future__ import annotations
import argparse, csv, re, shutil
from collections import Counter, OrderedDict
from pathlib import Path

HANDLE = "@LeiGao-gmu"

# Reserved on Windows/NTFS: < > : " / \ | ? *  -> readable, title-safe swaps.
REPLACE = OrderedDict([
    (":", " -"), ("/", "-"), ("\\", "-"), ('"', "'"),
    ("|", ""), ("?", ""), ("*", ""), ("<", ""), (">", ""),
])
CODE_RE = re.compile(r"^\[(MEF|NGN)\s+W([0-9A-Za-z.]+)\s+P(\d+)\]")


def sanitize(title: str) -> str:
    s = title
    for k, v in REPLACE.items():
        s = s.replace(k, v)
    s = re.sub(r"\s+", " ", s).strip()
    s = s.rstrip(". ")            # Windows forbids trailing dot/space
    return s


def week_of(row: dict) -> str:
    m = re.search(r"Week\s+(\d+)", row["playlist"])      # authoritative
    if m:
        return m.group(1)
    cm = CODE_RE.match(row["youtube_title"])             # fallback
    return cm.group(2).split(".")[0] if cm else "Misc"


def write_guide(repo: Path, code: str, per_week: Counter,
                playlists: "OrderedDict[str,str]", total: int, over100: list) -> None:
    edition = "ASSIP Empirical Finance Camp" if code == "MEF" else "NextGen Empirical Finance Camp"
    g = []
    g.append(f"# YouTube Upload Guide — {edition}\n")
    g.append(f"**Channel:** {HANDLE}  •  **Clips:** {total}  •  **Title code:** `[{code} Wx.y Pn]`\n")
    g.append(f"The site embeds videos by reading the `[{code} …]` code from each YouTube\n"
             "title. These files are **named as their titles**, so uploading auto-fills\n"
             "the titles — you never type them.\n")

    g.append("\n> **Upload as Unlisted.** The lessons stay off your public channel listing/search\n"
             "> but still embed on the site. Recovery (step 4) reads them via a one-time owner\n"
             "> **OAuth** login — an API key can't see Unlisted videos. (Don't use *Private*:\n"
             "> private videos refuse to embed on a public page.)\n")

    g.append("\n## 1. (Once) Smoke-test one video\n")
    g.append("YouTube sets each title from the filename. Upload **one** clip (Unlisted), then run\n"
             "step 4's command — if it reports `1 clip mapped`, titles are preserved and you can\n"
             "bulk-upload with confidence.\n")

    g.append("\n## 2. Upload, one week-folder at a time\n")
    g.append("For each `Week-N/` folder under `videos/upload_ready/`:\n")
    g.append("1. YouTube Studio → **Create → Upload videos** → drag in *all* files from the folder.\n")
    g.append(f"2. Titles auto-fill from the filenames (the `[{code} …]` code is what matters).\n")
    g.append("3. Set visibility to **Unlisted**. Optionally paste the description from the manifest.\n")
    g.append("4. After processing, select them all → **Add to playlist** → the playlist below.\n")

    g.append("\n## 3. Folders → playlists\n")
    g.append("| Folder | Playlist (create in Studio) | Clips |\n|---|---|---|\n")
    for wk in sorted(playlists, key=lambda x: (len(x), x)):
        g.append(f"| `Week-{wk}/` | {playlists[wk]} | {per_week[wk]} |\n")
    g.append(f"| | **Total** | **{total}** |\n")

    g.append("\n## 4. Recover the links into the site (owner OAuth)\n")
    g.append("One-time Google Cloud setup (see `tools/yt_oauth.py` for the click-path):\n")
    g.append("1. Cloud Console → enable **YouTube Data API v3**.\n")
    g.append("2. **OAuth consent screen**: User type *External*; add your Google account as a *Test user*.\n")
    g.append("3. **Credentials → Create OAuth client ID → \"TVs and Limited Input devices\"**; download the JSON.\n")
    g.append("4. Save it as `~/.config/leigao-video/client_secrets.json`.\n")
    g.append("\nThen, from this repo:\n")
    g.append("```bash\n"
             "python tools/build_video_map.py --oauth\n"
             "```\n")
    g.append("It prints a URL + code to authorize once (device flow), then prints\n"
             "`N clips mapped across X/Y items` and a coverage line; a `WARNING:` names any\n"
             "subchapter still missing a video. Writes `video-map.json` (keyed by item id: ch11,\n"
             "lab1, mentor3, …). Both editions share the channel — the script's `[%s]` regex\n"
             "picks only its own videos and ignores the other edition's.\n" % code)
    g.append("\n> The login is cached at `~/.config/leigao-video/yt_token.json`; later runs reuse\n"
             "> it silently. In OAuth *Testing* mode the token expires after ~7 days — if a run\n"
             "> says it must re-authorize, just approve the code again.\n")
    g.append("\nWant to preview the result *before* uploading? Dry-run it against the\n"
             "filenames YouTube will receive (no API, no upload):\n")
    g.append("```bash\n"
             "ls videos/upload_ready/*/*.mp4 | sed 's#.*/##; s#\\.mp4$##' > /tmp/titles.txt\n"
             "python tools/build_video_map.py --titles-from /tmp/titles.txt --out /tmp/preview.json\n"
             "```\n")

    g.append("\n## 5. Publish to the site\n")
    g.append("```bash\n"
             "git add video-map.json && git commit -m 'Wire YouTube video embeds' && git push\n"
             "```\n")
    g.append("GitHub Actions rebuilds; every subchapter page then shows a *“Watch this lesson”*\n"
             "player with one button per ≤5-min part. Pages with no map entry simply omit it.\n")

    g.append("\n## Notes\n")
    g.append(f"- A few titles contained characters illegal in filenames (`: | ? \\ \" /`); those\n"
             f"  were replaced for the filename only (e.g. `:` → ` -`). The **exact** titles are\n"
             f"  in `videos/upload_manifest.csv`. The `[{code} …]` code is never affected, so\n"
             f"  link recovery is unaffected — this only changes the on-screen title text.\n")
    if over100:
        g.append(f"- {len(over100)} titles exceed YouTube's 100-char limit and will be truncated\n"
                 f"  (the leading code survives, so embeds still resolve).\n")
    else:
        g.append("- All titles are within YouTube's 100-char limit (no truncation).\n")

    (repo / "videos" / "UPLOAD_GUIDE.md").write_text("".join(g), encoding="utf-8")


def main() -> None:
    ap = argparse.ArgumentParser(description="Build drag-ready YouTube upload folders.")
    ap.add_argument("repo", help="edition repo dir (contains videos/upload_manifest.csv)")
    ap.add_argument("--guide-only", action="store_true",
                    help="regenerate UPLOAD_GUIDE.md only; do NOT (re)copy the ~GBs of clips")
    a = ap.parse_args()

    repo = Path(a.repo).resolve()
    man = repo / "videos" / "upload_manifest.csv"
    clips = repo / "videos" / "clips"
    out = repo / "videos" / "upload_ready"
    rows = list(csv.DictReader(open(man, encoding="utf-8")))

    # ---- plan: derive folder/name for every row (no I/O), guarding collisions ----
    code = None
    seen: dict[str, str] = {}          # dest relpath -> source file (collision guard)
    per_week: Counter = Counter()
    playlists: "OrderedDict[str,str]" = OrderedDict()
    over100: list = []
    plan: list = []                    # (src, dst_dir, name)
    for r in rows:
        title = r["youtube_title"]
        m = CODE_RE.match(title)
        if not m:
            raise SystemExit(f"FATAL: title has no [CODE] prefix: {title!r}")
        code = code or m.group(1)
        wk = week_of(r)
        playlists.setdefault(wk, r["playlist"])
        name = sanitize(title) + ".mp4"
        rel = f"Week-{wk}/{name}"
        if rel in seen:
            raise SystemExit(f"FATAL collision: {rel}\n  <- {r['file']}\n  <- {seen[rel]}")
        seen[rel] = r["file"]
        if len(name) - 4 > 100:
            over100.append(name)
        per_week[wk] += 1
        plan.append((clips / r["file"], out / f"Week-{wk}", name))
    total = len(rows)

    # ---- copy (unless --guide-only), then verify loudly ----
    if a.guide_only:
        if not out.exists():
            print("NOTE: --guide-only but videos/upload_ready/ does not exist yet "
                  "(guide written; run without --guide-only to copy clips).")
    else:
        if out.exists():
            shutil.rmtree(out)
        missing = []
        for src, dst_dir, name in plan:
            if not src.exists():
                missing.append(src.name)
                continue
            dst_dir.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dst_dir / name)
        assert not missing, f"missing source clips: {missing[:5]} ... ({len(missing)})"
        on_disk = sum(1 for _ in out.rglob("*.mp4"))
        assert on_disk == total, f"count mismatch: rows={total} on_disk={on_disk}"
        for f in out.rglob("*.mp4"):
            assert f.stat().st_size > 2000, f"empty/short dest: {f}"

    write_guide(repo, code, per_week, playlists, total, over100)

    edition = "ASSIP" if code == "MEF" else "NextGen"
    verb = "guide refreshed" if a.guide_only else f"copied {total} clips into {out.relative_to(repo)}/"
    print(f"[{code}] {edition}: {verb} across {len(per_week)} week folders")
    print(f"  per-week: {dict(sorted(per_week.items(), key=lambda x:(len(x[0]),x[0])))}")
    print(f"  over-100-char titles: {len(over100)} | wrote videos/UPLOAD_GUIDE.md")


if __name__ == "__main__":
    main()
