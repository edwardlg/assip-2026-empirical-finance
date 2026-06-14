#!/usr/bin/env python3
"""
make_video_hopper.py -- Hopper / A100 variant of the teaching-video pipeline.

Same CLI shape as tools/make_video.py (the local pipeline) so a SLURM batch job
can call it identically:

    python tools/make_video_hopper.py --input file.pptx --output file.mp4 [--res 4k]
                                      [--voice-sample sample.wav]

Differences from the local pipeline:
  * Neural TTS backend selection by TTS_BACKEND env var:
        xtts   -> Coqui XTTS-v2 (best quality, GPU; ~realtime on an A100)
        bark   -> suno/bark   (very expressive, slower, GPU)
        piper  -> rhasspy/piper-tts (excellent quality, CPU-only)
        gtts   -> Google Text-to-Speech (network, robotic-ish)
    Default order on Hopper:  xtts -> piper -> gtts -> pyttsx3
  * Optional voice cloning with --voice-sample sample.wav (XTTS-v2 native).
  * Higher-resolution slide rendering: --res 1080 (default) or --res 4k.
  * Optional Manim B-roll: if a slide note contains
        <!-- manim:expression -->
    a Manim animation is rendered for that slide in place of the static PNG.
    Skipped gracefully if manim is not installed.
  * ffmpeg compositing with crossfades + slight Ken-Burns zoom (matches local).

No emojis. No hard-coded secrets. GMU-cluster-specific strings live in the
SLURM scripts, not in this file.
"""
from __future__ import annotations

import argparse
import os
import re
import shlex
import shutil
import subprocess
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Optional


# ---------------------------------------------------------------------------
# Resolution presets
# ---------------------------------------------------------------------------

RES_PRESETS = {
    "720":  (1280, 720),
    "1080": (1920, 1080),
    "1440": (2560, 1440),
    "2k":   (2560, 1440),
    "4k":   (3840, 2160),
    "2160": (3840, 2160),
}


# ---------------------------------------------------------------------------
# Small helpers
# ---------------------------------------------------------------------------

def log(msg: str) -> None:
    print(f"[make_video_hopper] {msg}", flush=True)


def run(cmd: list[str], check: bool = True) -> subprocess.CompletedProcess:
    log("$ " + " ".join(shlex.quote(c) for c in cmd))
    return subprocess.run(cmd, check=check)


def have_cmd(name: str) -> bool:
    return shutil.which(name) is not None


def have_gpu() -> bool:
    """Best-effort GPU probe (Hopper compute nodes set CUDA_VISIBLE_DEVICES)."""
    if os.environ.get("CUDA_VISIBLE_DEVICES", "") not in ("", "-1"):
        return True
    if have_cmd("nvidia-smi"):
        try:
            r = subprocess.run(
                ["nvidia-smi", "-L"], capture_output=True, text=True, timeout=10
            )
            return r.returncode == 0 and "GPU" in r.stdout
        except Exception:
            return False
    return False


# ---------------------------------------------------------------------------
# Slide extraction (PPTX -> PNG + speaker notes)
# ---------------------------------------------------------------------------

@dataclass
class Slide:
    index: int
    image_path: Path
    notes: str          # speaker notes (the narration)
    manim_expr: Optional[str] = None   # populated if <!-- manim:... --> is found


def pptx_to_pngs(pptx: Path, out_dir: Path, width: int, height: int) -> list[Path]:
    """Render the pptx to one PNG per slide using libreoffice + pdftoppm.

    libreoffice writes a PDF; pdftoppm rasterizes each page to PNG at the
    requested resolution. This matches the local pipeline so a viewer cannot
    tell the rendering path apart -- only the narration changes.
    """
    out_dir.mkdir(parents=True, exist_ok=True)
    pdf_dir = out_dir / "_pdf"
    pdf_dir.mkdir(exist_ok=True)

    if not have_cmd("libreoffice") and not have_cmd("soffice"):
        raise RuntimeError(
            "libreoffice/soffice not found; cannot rasterize pptx. "
            "Load the libreoffice module or apt-install it before running."
        )
    soffice = "libreoffice" if have_cmd("libreoffice") else "soffice"

    run([soffice, "--headless", "--convert-to", "pdf",
         "--outdir", str(pdf_dir), str(pptx)])

    pdfs = sorted(pdf_dir.glob("*.pdf"))
    if not pdfs:
        raise RuntimeError(f"libreoffice produced no PDF for {pptx}")
    pdf = pdfs[0]

    # pdftoppm -r DPI gives us a width-controlled rasterization. Compute the
    # DPI needed to hit the requested pixel width on a standard 13.333"-wide
    # 16:9 slide.
    slide_width_in = 13.333
    dpi = max(96, int(round(width / slide_width_in)))
    if not have_cmd("pdftoppm"):
        raise RuntimeError("pdftoppm not found (apt: poppler-utils).")
    run(["pdftoppm", "-png", "-r", str(dpi), str(pdf), str(out_dir / "slide")])

    pngs = sorted(out_dir.glob("slide-*.png"))
    if not pngs:
        raise RuntimeError("pdftoppm produced no PNGs")
    return pngs


def extract_notes(pptx: Path) -> list[str]:
    """Pull speaker notes per slide using python-pptx. Empty string if absent."""
    try:
        from pptx import Presentation  # python-pptx
    except ImportError as exc:
        raise RuntimeError(
            "python-pptx not installed. pip install python-pptx"
        ) from exc

    prs = Presentation(str(pptx))
    notes: list[str] = []
    for slide in prs.slides:
        text = ""
        if slide.has_notes_slide and slide.notes_slide.notes_text_frame is not None:
            text = slide.notes_slide.notes_text_frame.text or ""
        notes.append(text.strip())
    return notes


MANIM_MARKER = re.compile(r"<!--\s*manim:(.+?)-->", re.IGNORECASE | re.DOTALL)


def split_manim_marker(notes: str) -> tuple[str, Optional[str]]:
    """Return (clean_notes_for_TTS, manim_expression_or_None)."""
    m = MANIM_MARKER.search(notes)
    if not m:
        return notes, None
    expr = m.group(1).strip()
    clean = MANIM_MARKER.sub("", notes).strip()
    return clean, expr


# ---------------------------------------------------------------------------
# TTS backends
# ---------------------------------------------------------------------------

def _tts_xtts(text: str, out_wav: Path, voice_sample: Optional[Path]) -> bool:
    """Coqui XTTS-v2. Requires `pip install TTS` and the model cached locally."""
    try:
        from TTS.api import TTS  # type: ignore
    except ImportError:
        log("XTTS: TTS package not installed; skipping.")
        return False
    try:
        import torch  # noqa: F401
    except ImportError:
        log("XTTS: torch not installed; skipping.")
        return False
    try:
        device = "cuda" if have_gpu() else "cpu"
        log(f"XTTS: loading model on {device}")
        tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to(device)
        kwargs = {"text": text, "file_path": str(out_wav), "language": "en"}
        if voice_sample is not None and voice_sample.exists():
            kwargs["speaker_wav"] = str(voice_sample)
        else:
            # Pick a reasonable default speaker baked into XTTS-v2.
            kwargs["speaker"] = os.environ.get("XTTS_SPEAKER", "Damien Black")
        tts.tts_to_file(**kwargs)
        return out_wav.exists() and out_wav.stat().st_size > 0
    except Exception as exc:
        log(f"XTTS failed: {exc!r}; will fall back.")
        return False


def _tts_bark(text: str, out_wav: Path) -> bool:
    try:
        from bark import SAMPLE_RATE, generate_audio, preload_models  # type: ignore
        from scipy.io.wavfile import write as wav_write  # type: ignore
    except ImportError:
        log("Bark: not installed; skipping.")
        return False
    try:
        preload_models()
        audio = generate_audio(text)
        wav_write(str(out_wav), SAMPLE_RATE, audio)
        return out_wav.exists()
    except Exception as exc:
        log(f"Bark failed: {exc!r}; will fall back.")
        return False


def _tts_piper(text: str, out_wav: Path) -> bool:
    """Piper CLI TTS -- CPU-only, very good quality."""
    if not have_cmd("piper"):
        log("Piper: binary not found; skipping.")
        return False
    voice = os.environ.get("PIPER_VOICE", "en_US-amy-medium.onnx")
    if not Path(voice).exists():
        log(f"Piper: voice file {voice} not found; skipping.")
        return False
    try:
        proc = subprocess.run(
            ["piper", "--model", voice, "--output_file", str(out_wav)],
            input=text, text=True, check=True,
        )
        return proc.returncode == 0 and out_wav.exists()
    except Exception as exc:
        log(f"Piper failed: {exc!r}; will fall back.")
        return False


def _tts_gtts(text: str, out_wav: Path) -> bool:
    try:
        from gtts import gTTS  # type: ignore
    except ImportError:
        log("gTTS: not installed; skipping.")
        return False
    try:
        mp3 = out_wav.with_suffix(".mp3")
        gTTS(text=text, lang="en").save(str(mp3))
        # transcode mp3 -> wav so the rest of the pipeline is format-agnostic
        run(["ffmpeg", "-y", "-loglevel", "error",
             "-i", str(mp3), str(out_wav)])
        mp3.unlink(missing_ok=True)
        return out_wav.exists()
    except Exception as exc:
        log(f"gTTS failed: {exc!r}; will fall back.")
        return False


def _tts_pyttsx3(text: str, out_wav: Path) -> bool:
    try:
        import pyttsx3  # type: ignore
    except ImportError:
        log("pyttsx3: not installed; nothing left to fall back to.")
        return False
    try:
        engine = pyttsx3.init()
        engine.save_to_file(text, str(out_wav))
        engine.runAndWait()
        return out_wav.exists()
    except Exception as exc:
        log(f"pyttsx3 failed: {exc!r}.")
        return False


def synthesize_narration(text: str, out_wav: Path,
                         voice_sample: Optional[Path]) -> Path:
    """Synthesize `text` to `out_wav` using the requested/auto backend.

    Order: env TTS_BACKEND if set, then xtts (if GPU) -> piper -> gtts -> pyttsx3.
    """
    if not text.strip():
        # Generate ~0.7s of silence so the slide still has a duration.
        run(["ffmpeg", "-y", "-loglevel", "error",
             "-f", "lavfi", "-i", "anullsrc=r=24000:cl=mono",
             "-t", "0.7", str(out_wav)])
        return out_wav

    requested = os.environ.get("TTS_BACKEND", "").lower().strip()
    auto_order = ["xtts", "piper", "gtts", "pyttsx3"]
    if not have_gpu() and "xtts" in auto_order:
        auto_order.remove("xtts")
        auto_order.insert(1, "xtts")  # try anyway (CPU fallback is slow but works)
    order = [requested] + [b for b in auto_order if b != requested] if requested else auto_order

    for backend in order:
        if not backend:
            continue
        log(f"TTS: trying backend={backend}")
        ok = False
        if backend == "xtts":
            ok = _tts_xtts(text, out_wav, voice_sample)
        elif backend == "bark":
            ok = _tts_bark(text, out_wav)
        elif backend == "piper":
            ok = _tts_piper(text, out_wav)
        elif backend == "gtts":
            ok = _tts_gtts(text, out_wav)
        elif backend == "pyttsx3":
            ok = _tts_pyttsx3(text, out_wav)
        else:
            log(f"Unknown backend {backend!r}, skipping.")
            continue
        if ok:
            return out_wav

    raise RuntimeError(
        "All TTS backends failed. Install at least one of: TTS, piper, gtts, pyttsx3."
    )


# ---------------------------------------------------------------------------
# Optional Manim B-roll
# ---------------------------------------------------------------------------

def render_manim(expr: str, out_png: Path, width: int, height: int) -> bool:
    """Render a Manim animation for this slide. Returns True on success.

    `expr` should be a self-contained Manim Scene name or a tiny snippet
    (e.g. "PlotCAPM"). To keep this safe, we only accept identifier-like
    names and look them up in tools/manim_scenes.py. Free-form expressions
    are NOT exec'd here.
    """
    if not re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", expr or ""):
        log(f"Manim expr {expr!r} is not a bare Scene name; skipping for safety.")
        return False
    if not have_cmd("manim"):
        log("Manim: not installed; skipping B-roll.")
        return False
    scenes_py = Path(__file__).parent / "manim_scenes.py"
    if not scenes_py.exists():
        log(f"Manim: {scenes_py} not found; skipping.")
        return False
    with tempfile.TemporaryDirectory() as td:
        td_p = Path(td)
        try:
            run(["manim", "-ql", "-o", "broll", "--media_dir", str(td_p),
                 str(scenes_py), expr])
        except subprocess.CalledProcessError as exc:
            log(f"Manim render failed: {exc}; skipping.")
            return False
        mp4s = list(td_p.rglob("*.mp4"))
        if not mp4s:
            log("Manim: no mp4 produced; skipping.")
            return False
        # Grab first/last frame as a PNG fallback so the rest of the pipeline
        # (which composites stills + audio) still works. For full B-roll
        # treatment we would splice the mp4 into the timeline; that is a
        # future extension.
        run(["ffmpeg", "-y", "-loglevel", "error",
             "-sseof", "-0.1", "-i", str(mp4s[0]),
             "-vframes", "1", "-vf", f"scale={width}:{height}",
             str(out_png)])
        return out_png.exists()


# ---------------------------------------------------------------------------
# ffmpeg compositing (matches local pipeline: per-slide MP4 with Ken-Burns,
# then concat with crossfades)
# ---------------------------------------------------------------------------

def audio_duration(path: Path) -> float:
    r = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=noprint_wrappers=1:nokey=1", str(path)],
        capture_output=True, text=True, check=True,
    )
    return float(r.stdout.strip() or "1.0")


def build_clip(png: Path, wav: Path, out_mp4: Path,
               width: int, height: int) -> None:
    """One slide -> one MP4 with a slow Ken-Burns zoom matched to audio length."""
    dur = max(1.5, audio_duration(wav) + 0.4)
    # zoompan zooms slowly from 1.0 to ~1.06 over the clip
    fps = 30
    frames = int(dur * fps)
    zoom_expr = f"zoom='min(zoom+0.0005,1.06)':d={frames}:s={width}x{height}:fps={fps}"
    vf = (
        f"scale={width*2}:{height*2},"
        f"zoompan={zoom_expr},"
        f"format=yuv420p"
    )
    run([
        "ffmpeg", "-y", "-loglevel", "error",
        "-loop", "1", "-i", str(png),
        "-i", str(wav),
        "-c:v", "libx264", "-preset", "medium", "-crf", "20",
        "-c:a", "aac", "-b:a", "192k",
        "-vf", vf,
        "-t", f"{dur:.3f}",
        "-pix_fmt", "yuv420p", "-shortest",
        str(out_mp4),
    ])


def concat_with_crossfades(clips: list[Path], out_mp4: Path,
                           width: int, height: int) -> None:
    """Concatenate per-slide MP4s with a 0.4s crossfade between each pair.

    For N clips we emit an ffmpeg filter_complex with N-1 xfade/acrossfade
    pairs. For small N this is fine; for very large N a simple concat demuxer
    (no crossfade) would be cheaper -- but our weekly decks are ~20-40 slides.
    """
    if not clips:
        raise RuntimeError("No clips to concatenate")
    if len(clips) == 1:
        shutil.copy2(clips[0], out_mp4)
        return

    xfade_dur = 0.4
    inputs: list[str] = []
    for c in clips:
        inputs += ["-i", str(c)]

    durations = [audio_duration(Path(c).with_suffix(".wav")) + 0.4 for c in clips]
    # The xfade `offset` is the cumulative start time of each crossfade in the
    # output, relative to the start of the running mix.
    parts: list[str] = []
    last_v, last_a = "[0:v]", "[0:a]"
    running = durations[0]
    for i in range(1, len(clips)):
        v_out = f"[v{i}]"
        a_out = f"[a{i}]"
        offset = running - xfade_dur
        parts.append(
            f"{last_v}[{i}:v]xfade=transition=fade:duration={xfade_dur}:"
            f"offset={offset:.3f}{v_out}"
        )
        parts.append(
            f"{last_a}[{i}:a]acrossfade=d={xfade_dur}{a_out}"
        )
        last_v, last_a = v_out, a_out
        running += durations[i] - xfade_dur

    filter_complex = ";".join(parts)
    run([
        "ffmpeg", "-y", "-loglevel", "error",
        *inputs,
        "-filter_complex", filter_complex,
        "-map", last_v, "-map", last_a,
        "-c:v", "libx264", "-preset", "medium", "-crf", "20",
        "-c:a", "aac", "-b:a", "192k",
        "-pix_fmt", "yuv420p",
        str(out_mp4),
    ])


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> int:
    ap = argparse.ArgumentParser(
        description="Hopper-side teaching-video render: PPTX -> narrated MP4."
    )
    ap.add_argument("--input", required=True, type=Path,
                    help="Source .pptx (deck rendered from week-NN.qmd).")
    ap.add_argument("--output", required=True, type=Path,
                    help="Destination .mp4.")
    ap.add_argument("--res", default="1080",
                    choices=sorted(RES_PRESETS.keys()),
                    help="Output resolution preset (default 1080).")
    ap.add_argument("--voice-sample", type=Path, default=None,
                    help="Optional 20-30s WAV for XTTS voice cloning.")
    ap.add_argument("--keep-work", action="store_true",
                    help="Keep the intermediate working directory.")
    args = ap.parse_args()

    pptx: Path = args.input
    out_mp4: Path = args.output
    if not pptx.exists():
        log(f"ERROR: input not found: {pptx}")
        return 2
    out_mp4.parent.mkdir(parents=True, exist_ok=True)

    width, height = RES_PRESETS[args.res]
    log(f"Resolution: {width}x{height} (--res {args.res})")
    log(f"GPU available: {have_gpu()}")

    work = Path(tempfile.mkdtemp(prefix="mvh_"))
    log(f"Working dir: {work}")
    try:
        # 1) PPTX -> per-slide PNGs at requested resolution
        pngs = pptx_to_pngs(pptx, work / "slides", width, height)
        notes_list = extract_notes(pptx)
        if len(notes_list) < len(pngs):
            notes_list += [""] * (len(pngs) - len(notes_list))

        # 2) Per slide: TTS narration (+ optional manim B-roll image)
        clips: list[Path] = []
        for i, png in enumerate(pngs):
            raw_notes = notes_list[i] if i < len(notes_list) else ""
            clean_notes, manim_expr = split_manim_marker(raw_notes)
            if manim_expr:
                broll_png = work / f"manim-{i+1:03d}.png"
                if render_manim(manim_expr, broll_png, width, height):
                    png = broll_png  # replace the slide still with the manim frame
            wav = work / f"slide-{i+1:03d}.wav"
            synthesize_narration(clean_notes or " ", wav, args.voice_sample)
            clip = work / f"clip-{i+1:03d}.mp4"
            # ensure the wav sits next to the clip so concat_with_crossfades
            # can locate it for duration probing
            shutil.copy2(wav, clip.with_suffix(".wav"))
            build_clip(png, wav, clip, width, height)
            clips.append(clip)

        # 3) Crossfade-concatenate
        concat_with_crossfades(clips, out_mp4, width, height)
        log(f"Wrote {out_mp4} ({out_mp4.stat().st_size/1e6:.1f} MB)")
        return 0
    finally:
        if not args.keep_work:
            shutil.rmtree(work, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main())
