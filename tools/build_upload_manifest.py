#!/usr/bin/env python3
"""
build_upload_manifest.py -- turn clips.jsonl into a YouTube bulk-upload sheet.

Output: videos/upload_manifest.csv with columns
  file, youtube_title, playlist, description
Keep the youtube_title verbatim on upload -- build_video_map.py parses the
[MEF Wx.y Pn] / [NGN Wx.y Pn] code from it to wire the site embeds.

Usage:  python tools/build_upload_manifest.py [--site URL] [--camp "ASSIP ..."]
"""
from __future__ import annotations
import argparse, csv, json
from pathlib import Path

CH = Path("book/decks/chapters")
WK = {1:"Probability & Inference",2:"OLS & Inference",3:"Causal Inference",
      4:"Quasi-Experiments",5:"Reading the Canon",6:"Text, AI & Alt-Data",
      7:"Your Project I",8:"Your Project II"}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--camp", default="ASSIP Empirical Finance Camp")
    ap.add_argument("--site", default="")
    ap.add_argument("--out", default="videos/upload_manifest.csv")
    a = ap.parse_args()
    clips = [json.loads(l) for l in open(CH / "clips.jsonl") if l.strip()]
    Path(a.out).parent.mkdir(parents=True, exist_ok=True)
    n = 0
    with open(a.out, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["file", "youtube_title", "playlist", "description"])
        for c in clips:
            wk = c["week"]
            playlist = f"Week {wk} — {WK.get(wk, '')}".strip(" —")
            part = f"Part {c['part']} of {c['total_parts']}" if c["total_parts"] > 1 else ""
            desc = (f"{c['display_title']} — {a.camp}. {part}\n"
                    f"Prof. Lei Gao, George Mason University. "
                    f"A research-grade empirical-finance lesson for advanced high-school students."
                    + (f"\nFull course: {a.site}" if a.site else ""))
            w.writerow([Path(c["out_mp4"]).name, c["youtube_title"], playlist, desc])
            n += 1
    print(f"wrote {a.out}: {n} rows")


if __name__ == "__main__":
    main()
