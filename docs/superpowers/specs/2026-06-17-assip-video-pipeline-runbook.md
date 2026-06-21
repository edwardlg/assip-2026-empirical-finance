# RUNBOOK — ASSIP teaching-video pipeline

Companion to `2026-06-17-assip-video-course-research.md` (the design brief).
This is the operator's guide: how to render, upload, link, and clone.

## What got built (authoring environment)

| Piece | Path | Role |
|---|---|---|
| GMU brand master | `book/decks/templates/assip-reference.pptx` (+ `build_reference_pptx.py`) | Mason Green/Gold, Poppins/Open Sans, 16:9; every deck inherits it |
| Shared deck config | `book/decks/chapters/_metadata.yml` | points decks at the reference-doc; no per-deck format block |
| Segment decks | `book/decks/chapters/{item}-p{N}.qmd` | one ≤5-min video each; slides + `::: notes` TTS scripts |
| Buildout manifest | `book/decks/chapters/_buildout_items.json` | the 56 source items (codePrefix, paths) |
| Clip manifest | `book/decks/chapters/clips.jsonl` (gen: `tools/build_clips_manifest.py`) | one line per clip: deck, out_mp4, youtube_title `[MEF Wx.y Pn] …` |
| TTS tier | `tools/make_video_hopper.py` → `_tts_chatterbox` | Chatterbox (MIT) voice-clone narration, preferred backend |
| Finishing | `tools/finish_clip.py` | loudnorm (R128) + H.264 1080p +faststart + WhisperX `.vtt` |
| Render array | `slurm/render_clips.sbatch` | one A100 task per clip; edition-agnostic (REPO_DIR/MANIFEST) |
| Env | `environment.yml` | chatterbox-tts, whisperx, python-pptx, pdf2image, ffmpeg, poppler baked in |
| Link recovery | `tools/build_video_map.py` | reads @LeiGao-gmu uploads → `video-map.json` |
| Site embed | `_includes/video-embed.html` (+ wired in `_quarto.yml`) | per-subchapter YouTube player |

## Prereqs on Hopper (one-time)

```bash
conda env create -f environment.yml && conda activate finlab
pip install torch torchaudio --index-url https://download.pytorch.org/whl/cu121  # match Hopper CUDA
module load quarto libreoffice            # or install; both must be on PATH
```
**Before any mass submit, confirm the `[CHECK]` SBATCH values** in `slurm/render_clips.sbatch`
(`--partition=gpuq`, `--account=nextgen2026`, `--qos=gpu`, `--gres=gpu:a100:1`, `--time`)
against current GMU ORC.

## Assets from Prof. Gao — IN ✅

1. **Voice sample** — `assets/voice/Lei_Gao_30s.m4a` (the render auto-converts m4a→wav).
2. **GMU logo** — `assets/brand/Logo.png`; already stamped into the reference template
   (`build_reference_pptx.py --logo assets/brand/Logo.png` was run; logo sits top-right on the master).

## P4 — Pilot (render ONE chapter, review, then scale)

```bash
python tools/build_clips_manifest.py                 # refresh clips.jsonl
export VOICE_SAMPLE=$PWD/assets/voice/Lei_Gao_30s.m4a # auto-converted to wav; omit -> built-in voice
# render just ch11's parts interactively (or a 5-task array):
grep '"item_id": "ch11"' book/decks/chapters/clips.jsonl  # see the lines
sbatch --array=1-5%2 slurm/render_clips.sbatch       # if ch11 is lines 1-5; else set MANIFEST to a ch11-only file
```
Review `videos/clips/ch11-p*.mp4`: brand fidelity, voice quality/pace, caption alignment,
loudness, file size, GPU-h. **Lock the per-segment word budget here** (measure actual wpm).

### Deck-set status & pilot-time polish
- **457 segment decks across all 56 items; 0 `[CHECK]` leftovers; max narration 660 words** (no deck exceeds it).
  Median ~635 words; ~31 h of finished video total. On-slide bullets clean (the only >14-word "bullets"
  are short inline-LaTeX equations, not prose).
- **~45 decks sit in the 641–660-word band** — ≤5:00 at ≥132 wpm (Chatterbox typically runs faster).
  The pilot measures the cloned voice's actual wpm; if any clip exceeds 5:00, run a one-shot trim pass
  (tighten wording to ≤620; no content cut needed) keyed off `tools/build_clips_manifest.py` + a word scan.

## Full render

```bash
N=$(wc -l < book/decks/chapters/clips.jsonl)
sbatch --array=1-${N}%4 slurm/render_clips.sbatch    # ~350-400 clips; idempotent (skips up-to-date)
```

## Upload (Path A) + link

1. Bulk-upload `videos/clips/*.mp4` to **@LeiGao-gmu**, KEEPING the titles from
   `clips.jsonl` `youtube_title` (`[MEF Wx.y Pn] …`). A playlist per week is nice-to-have.
2. Recover links (read-only API key, no OAuth):
   ```bash
   export YOUTUBE_API_KEY=...            # free Data API key
   python tools/build_video_map.py       # writes video-map.json
   ```
3. Rebuild the site; `_includes/video-embed.html` now embeds each chapter's parts on its page.
   Archive masters to Git LFS / a GitHub Release as the embed fallback.

## Clone to another edition (e.g. NextGen `8weeks2`)

The pipeline is edition-agnostic. In the target repo:
1. Copy `book/decks/templates/`, `book/decks/chapters/_metadata.yml`, all of `tools/*.py`,
   `slurm/render_clips.sbatch`, `_includes/video-embed.html`, and the `environment.yml` video block.
2. Re-run the enumerator (the `_buildout_items.json` builder) against that repo's `book/weeks/week-01..08`
   — adjust for its chapter set (NextGen folds in ch46/ch76/ch86/ch87).
3. Re-run the **same fan-out workflow** to author segment decks, then `build_clips_manifest.py`.
4. Use a distinct title code (e.g. `[NGN Wx.y Pn]`) so the two editions' uploads don't collide
   in `build_video_map.py`.
5. Render on Hopper, upload, map — same steps.
