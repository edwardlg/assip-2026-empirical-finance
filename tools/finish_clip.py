#!/usr/bin/env python3
"""
finish_clip.py -- finishing pass for one teaching clip.

  1. Loudness-normalize to EBU R128 (I=-16, TP=-1.5, LRA=11).
  2. Re-encode H.264 1080p, CRF 19, yuv420p, +faststart (web-streamable).
  3. Emit a caption sidecar (.vtt) via WhisperX (best-effort; skipped if absent).

Usage:
  python tools/finish_clip.py --input raw.mp4 --output final.mp4 [--vtt out.vtt]
"""
from __future__ import annotations
import argparse, glob, os, shutil, subprocess
from pathlib import Path


def have(cmd: str) -> bool:
    return shutil.which(cmd) is not None


def run(cmd: list[str], check: bool = True):
    print("$ " + " ".join(cmd), flush=True)
    return subprocess.run(cmd, check=check)


def normalize_encode(src: Path, dst: Path) -> None:
    if not have("ffmpeg"):
        raise SystemExit("ffmpeg not found (load the ffmpeg module / apt install).")
    dst.parent.mkdir(parents=True, exist_ok=True)
    run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(src),
         "-af", "loudnorm=I=-16:TP=-1.5:LRA=11",
         "-c:v", "libx264", "-preset", "slow", "-crf", "19", "-pix_fmt", "yuv420p",
         "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", str(dst)])


def make_captions(src: Path, vtt: Path) -> bool:
    """Best-effort English captions. WhisperX preferred (GPU forced-align)."""
    vtt.parent.mkdir(parents=True, exist_ok=True)
    model = os.environ.get("WHISPER_MODEL", "large-v2")
    tool = "whisperx" if have("whisperx") else ("whisper" if have("whisper") else None)
    if tool is None:
        print("captions: no whisperx/whisper on PATH; skipping (.vtt not produced).")
        return False
    tmp = vtt.parent / f"_cap_{src.stem}"
    tmp.mkdir(parents=True, exist_ok=True)
    cmd = [tool, str(src), "--language", "en", "--output_format", "vtt",
           "--output_dir", str(tmp)]
    if tool == "whisperx":
        cmd += ["--model", model]
    run(cmd, check=False)
    produced = sorted(glob.glob(str(tmp / "*.vtt")))
    if produced:
        shutil.move(produced[0], str(vtt))
        shutil.rmtree(tmp, ignore_errors=True)
        return True
    shutil.rmtree(tmp, ignore_errors=True)
    print("captions: tool produced no .vtt; skipping.")
    return False


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", required=True)
    ap.add_argument("--output", required=True)
    ap.add_argument("--vtt", default=None)
    args = ap.parse_args()
    src, dst = Path(args.input), Path(args.output)
    normalize_encode(src, dst)
    if args.vtt:
        make_captions(dst, Path(args.vtt))
    print(f"finished -> {dst}")


if __name__ == "__main__":
    main()
