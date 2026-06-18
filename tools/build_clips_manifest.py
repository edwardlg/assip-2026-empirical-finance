#!/usr/bin/env python3
"""
build_clips_manifest.py -- assemble the per-clip render manifest (clips.jsonl).

Scans the authored segment decks in book/decks/chapters/ (chXY-pN.qmd,
labN-pN.qmd, mentorN-pN.qmd, rgpackN-pN.qmd), joins them with the buildout
items manifest for the YouTube title-code, and emits one JSON line per clip:

  {clip_id, item_id, type, week, part, total_parts, deck, slug,
   display_title, youtube_title, out_mp4, out_vtt}

`youtube_title` carries the "[MEF Wx.y Pn] Title" code that the link-recovery
step (build_video_map.py) parses back from the channel after manual upload.

Usage:
  python tools/build_clips_manifest.py [--out clips.jsonl]
"""
from __future__ import annotations
import argparse, glob, json, os, re
from pathlib import Path

CH = Path("book/decks/chapters")
ITEMS = CH / "_buildout_items.json"


def deck_title(qmd: Path) -> str:
    """Read the YAML front-matter `title:` of a deck."""
    txt = qmd.read_text(encoding="utf-8")
    m = re.search(r'(?m)^\s*title:\s*"?(.+?)"?\s*$', txt)
    return m.group(1).strip().strip('"') if m else qmd.stem


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=str(CH / "clips.jsonl"))
    args = ap.parse_args()

    items = {it["outPrefix"]: it for it in json.loads(ITEMS.read_text())}

    # group segment decks by item prefix: "{prefix}-p{N}.qmd"
    groups: dict[str, list[tuple[int, Path]]] = {}
    for f in sorted(glob.glob(str(CH / "*.qmd"))):
        name = os.path.basename(f)
        if name.startswith("_"):
            continue
        m = re.match(r"(.+)-p(\d+)\.qmd$", name)
        if not m:
            continue
        prefix, part = m.group(1), int(m.group(2))
        groups.setdefault(prefix, []).append((part, Path(f)))

    clips, missing = [], []
    for prefix, parts in groups.items():
        it = items.get(prefix)
        if it is None:
            missing.append(prefix)
            continue
        parts.sort(key=lambda t: t[0])
        total = len(parts)
        for part, qmd in parts:
            slug = f"{prefix}-p{part}"
            title = deck_title(qmd)
            clips.append({
                "clip_id": slug,
                "item_id": prefix,
                "type": it["type"],
                "week": it["week"],
                "part": part,
                "total_parts": total,
                "deck": str(qmd).replace("\\", "/"),
                "slug": slug,
                "display_title": title,
                "youtube_title": f"[MEF {it['codePrefix']} P{part}] {title}",
                "out_mp4": f"videos/clips/{slug}.mp4",
                "out_vtt": f"videos/clips/{slug}.vtt",
            })

    # deterministic order: week, then item, then part
    clips.sort(key=lambda c: (c["week"], c["item_id"], c["part"]))
    with open(args.out, "w", encoding="utf-8") as fh:
        for c in clips:
            fh.write(json.dumps(c, ensure_ascii=False) + "\n")

    print(f"wrote {args.out}: {len(clips)} clips across {len(groups)} items")
    if missing:
        print(f"WARNING: {len(missing)} deck prefixes not in items manifest: {missing}")


if __name__ == "__main__":
    main()
