# DESIGN BRIEF — ASSIP 8-Week Empirical-Finance Video Course

**Date:** 2026-06-17
**Owner:** Prof. Lei Gao, Costello College of Business, George Mason University
**Goal:** Per-subchapter GMU-branded PowerPoint decks (with detailed speaker-note scripts) + one short teaching video per subchapter, with heavy TTS/render offloaded to GMU Hopper A100 GPUs.
**Repo root:** `/mnt/e/ccli/ASSIP8weeks`

---

## 1. Existing state (what the deck + video pipeline already does)

- **Per-week, not per-subchapter.** The unit today is `book/decks/week-NN.qmd` (8 fully authored decks) → `videos/week-NN.mp4`. The SLURM array is hardcoded to 8 weeks (`render_all_videos.sbatch`, `WEEKS=(week-01...week-08)`, `--array=1-8%4`).
- **Quarto → PPTX via Pandoc.** Decks are Quarto Markdown rendered with `quarto render <qmd> --to pptx` (driven by `book/decks/Makefile`). YAML pins `slide-level: 2` (one `##` = one slide), `fig-dpi: 200`. Each `##` slide closes with a `::: callout-tip` "Key takeaway" box.
- **`::: notes` → speaker notes → TTS.** Each slide's narration script lives in a `::: notes` fenced div that Pandoc converts to native PowerPoint speaker notes; `python-pptx` later extracts `notes_text_frame.text` per slide and feeds it to TTS. Scripts are already polished, spoken-voice, TTS-friendly prose (~120–220 words/slide; digits/symbols spelled out as words).
- **Rasterize chain:** PPTX → PDF (LibreOffice `--headless --convert-to pdf`) → one PNG/slide (Poppler `pdftoppm`; local path letterboxes to 1920×1080 via Pillow; Hopper computes DPI from target width).
- **Per-slide clip + concat (ffmpeg, software x264).** Each PNG is looped for the duration of its narration WAV (`-loop 1`), encoded `libx264 -crf 20`, `aac 192k`; clips are joined with `xfade`/`acrossfade` crossfades. Hopper adds a Ken-Burns `zoompan`. **No NVENC anywhere** — ffmpeg never touches the GPU.
- **Two renderers, two tiers.** `tools/make_video.py` (laptop, free CPU TTS: gTTS→pyttsx3). `tools/make_video_hopper.py` (A100, neural TTS auto-order `xtts→piper→gtts→pyttsx3`; default `TTS_BACKEND=xtts`). XTTS-v2 supports voice cloning from `--voice-sample` (plumbed end-to-end; defaults to baked-in "Damien Black" speaker if no sample).
- **A100 is justified by exactly one step: XTTS neural TTS.** Everything else is CPU/IO-bound. `slurm/render_video.sbatch` requests `--gres=gpu:a100:1`, hard-fails without a GPU, and **pip-installs the entire video stack `--user` at job start** because `environment.yml` ships none of it (burning A100 wall time on installs).
- **Known gaps/risks today:** `tools/manim_scenes.py` is missing → the Manim B-roll branch is dead (fails safe). README claims 1080p but Hopper defaults to `RES=4k` (slowest x264 step). No `.pptx`, no `assets/figures/`, no logo, no brand reference-doc exist in the repo yet. All cluster-specific SBATCH values (`--partition=gpuq`, `--account=nextgen2026`, `--qos=gpu`) are tagged `[CHECK]` / unverified against GMU ORC.

---

## 2. Scope & scale

### Enumeration (verified from `book/weeks/week-01..08`)
- **8 weeks · 40 chapter files (`ch*.md`, exactly 5/week) · 349 H2 (`##`) sections.**
- Non-chapter items: 6 labs (weeks 1–4, 7, 8), 8 mentor sessions (1/week), 2 reading-guide packs (weeks 5–6).
- Per-week H2 totals: W1=42, W2=50, W3=48, W4=53, W5=36, W6=36, W7=42, W8=42.

### Recommended granularity: **chapter-file (one video per `ch*.md`, "Ch X.Y")**

| Option | "Subchapter" = | # Videos | Verdict |
|---|---|---|---|
| **option-Chapter (RECOMMENDED)** | one `ch*.md` ("Ch X.Y") | **40** | Atomic, already named/titled as subchapters; H2s are intra-lesson beats |
| option-Section | one `##` H2 heading | **349** | Fragments a 12–20 min lesson into sub-2-min clips; ~9× production with no pedagogical boundary |

Rationale: the curriculum already advertises "Ch X.Y" as the unit; H2 headings (6–13/file, heaviest ch2.5/ch4.3=13, ch1.5=12) are motivation/derivation/example/pitfall beats, not lesson boundaries. **Adopt 40 = 5/week × 8.** Optional extensions: +14 (labs+mentors) → **54**, or +16 (incl. 2 reading-guide packs) → **56**.

### Estimated runtime & A100 GPU-hours (recommended 40-video plan)

Assumptions: ~13–18 min/video target (chapter-file granularity) → **~10 hours total** of finished video across 40 videos. Narration ≈ 130 wpm.

| Quantity | Estimate |
|---|---|
| Total finished video | **~600 min (~10 h)** across 40 videos (~15 min avg) |
| Narrated words total | ~78,000 words (~600 min × 130 wpm) |
| **GPU step = TTS only** (Chatterbox/XTTS, faster-than-realtime on A100, RTF ≈ 0.2–0.3) | **~3 GPU-h** of pure synthesis (~600 audio-min × ~0.25 RTF ÷ 60) |
| + WhisperX forced-alignment (GPU, ~10–20% of audio length, large-v2 <8 GB) | **~1.5–2 GPU-h** |
| + per-job pip-install overhead at ~5–8 min/task × 40 (eliminated once baked into env — see P3) | up to **~4 GPU-h wasted today** |
| **GPU-h subtotal (TTS + alignment), env pre-baked** | **~5 GPU-h** of genuine A100 work |
| Wall-clock with `%4` concurrency + headroom | small; the long pole is **CPU x264 encoding** (assembly), which should run on a **separate CPU array**, not hold the A100 |

Net: the A100 budget for the recommended stack is **single-digit GPU-hours** (≈5) if the conda env is pre-built so jobs don't pip-install on GPU time. ffmpeg assembly/normalize/caption-burn are CPU-bound and should be split off the GPU allocation.

---

## 3. GMU branding spec

Source of truth: **George Mason University Brand Cheat Sheet (updated April 2024)** — Mason completed a full rebrand in April 2024 (bolder green/gold, interlocking "GM" logo). **Do NOT use legacy `#006633`/`#1B5633`.**

### Palette (ready-to-use hex)

| Role | Name | Hex | Status |
|---|---|---|---|
| **Primary** | George Mason Green | `#005239` | **VERIFIED** (Cheat Sheet) |
| **Primary** | George Mason Gold | `#FFC733` | **VERIFIED** (Cheat Sheet) |
| Neutral / text | Logo Black | `#333333` | **VERIFIED** (Cheat Sheet) |
| Accent (charts only) | Red | `#CC4824` | **[LIKELY-OFFICIAL, not master-verified]** (ABS unit site) |
| Accent (charts only) | Teal | `#008285` | **[LIKELY-OFFICIAL, not master-verified]** |
| Accent (charts only) | Navy | `#004F71` | **[LIKELY-OFFICIAL, not master-verified]** |
| Accent (charts only) | Gray | `#727579` | **[LIKELY-OFFICIAL, not master-verified]** |

**Dominance rule:** Green + Gold must dominate any Mason-branded piece (Gold best on Green). Accents are for charts/wayfinding only. The repo's existing academic-restraint blue (`#1f4e79`, from `styles.scss`) may be retained as an optional secondary, but it is **not** a GMU brand color — keep it subordinate.

### Fonts (Office-safe mapping from the Cheat Sheet's Web/Canva sets)

| Role | Brand font | Office fallback |
|---|---|---|
| Headlines/display | **Figtree** or **Poppins** | Arial Bold / Calibri |
| Body | **Open Sans** | Calibri / Arial |
| Serif accents | **Noto Serif** | Cambria / Georgia |
| Code (course-specific) | JetBrains Mono (from repo `styles.scss`) | Consolas |

Avoid Acumin Pro / Kandal / Franklin Gothic (print-only licensed; do not embed in shared decks).

### Logo rules
- Current logo = **interlocking "GM" + George Mason wordmark**, full-color (green+gold+black). **Use full-color on light/white backgrounds.**
- **Clear space** = width of the interlocking GM on all sides.
- **Trademark rule:** any material using "George Mason"/"GMU"/"Mason" must carry an approved Mason logo.
- **Never:** GM monogram alone as a substitute; rotate/crop; one-color white/black logo; gold logo on black or white.
- **Asset status: [UNVERIFIED — no logo file in repo].** Must be downloaded from the Bynder brand portal (NetID-gated) and committed to `assets/brand/`.

### HOW to apply branding (Quarto pptx has ONE mechanism: a reference-doc)

Quarto cannot theme pptx with SCSS/CSS — `styles.scss` styles the **HTML book only** and never reaches slides. The only supported path is a **reference `.pptx`** whose Slide Master + layouts Pandoc copies:

1. Create `book/decks/templates/` and author `book/decks/templates/assip-reference.pptx` (start from `quarto render _template.qmd --to pptx` or `pandoc --print-default-data-file reference.pptx`). Edit **Master + layouts only**, not content slides.
2. In the master: map theme accent → Green `#005239` / Gold `#FFC733`; text → `#333333`; theme fonts → Figtree/Poppins headings, Open Sans body, Noto Serif accents; place the GMU/Costello/ASSIP logo on Title + Title-and-Content masters; **preserve Pandoc layout names** ("Title Slide", "Title and Content", "Section Header") so `# {.title}` and `##` map correctly; confirm callout "Key takeaway" boxes survive.
3. Wire it in: uncomment the `reference-doc:` line in `_template.qmd` and add `reference-doc: templates/assip-reference.pptx` under `pptx:` in every `week/ch` deck. (Makefile needs no change.)

**For python-pptx generation (alternative engine):** the same `assip-reference.pptx` is loaded as the template; python-pptx clones its layouts and populates placeholders programmatically — best-in-class brand fidelity, no Office/display needed. Either engine consumes the **one** reference `.pptx` as the single brand source of truth.

Also create `assets/figures/week-N/` trees — the decks' `../../assets/figures/...` image paths are currently dangling.

---

## 4. Recommended video stack

### DEFAULT pipeline (end-to-end, implementable against the existing `make_video_hopper.py`)

```
ch-NN.qmd
  └─(Quarto/Pandoc)→ ch-NN.pptx        # branded via reference-doc  [CPU]
       └─(LibreOffice --headless → PDF; Poppler pdftoppm → PNG/slide)  [CPU]
            └─ python-pptx extracts ::: notes per slide  [CPU]
                 └─ TTS narration: CHATTERBOX (Resemble AI)  [A100 ← the GPU step]
                      └─ ffmpeg: -loop 1 per PNG = audio_len, Ken-Burns, xfade concat  [CPU x264]
                           └─ WhisperX forced-align narration → ch-NN.vtt + .srt  [GPU, small]
                                └─ ffmpeg-normalize loudnorm I=-16 TP=-1.5 LRA=11  [CPU]
                                     └─ libx264 CRF 19 -preset slow yuv420p +faststart  [CPU]
                                          └─ FFMETADATA chapter markers (-c copy)  [CPU, ~free]
                                               └─ ffprobe validate + content-hash sentinel
ch-NN.mp4 (+ sidecar ch-NN.vtt)
```

| Step | Tool | License | Runs on |
|---|---|---|---|
| Slide engine | **Quarto → Pandoc → pptx** (keep current) | MIT/GPL-2, free | CPU |
| Brand reference | one `assip-reference.pptx` | — | (build-time) |
| Rasterize | **LibreOffice headless + Poppler `pdftoppm`** | MPL-2.0 / free | CPU |
| Notes extract | **python-pptx** | MIT | CPU |
| **TTS narration** | **Chatterbox / Chatterbox Multilingual (Resemble AI)** | **MIT (code + weights)** — commercial **and** non-commercial safe; zero-shot clone from ~7–10 s | **A100** |
| Talking head | **NO** (see below) | — | — |
| Assembly | **ffmpeg** (`-loop 1`, `xfade`, concat) | LGPL/GPL, free | CPU |
| Captions | **WhisperX** (forced-align to known narration) → `.vtt` primary + `.srt` | BSD-ish/free | GPU (small) |
| Loudness | **ffmpeg two-pass loudnorm** / `slhck/ffmpeg-normalize` | free | CPU |
| Encode | **libx264** CRF 19, `-preset slow`, `+faststart` | free | CPU |
| Chapters | **ffmpeg FFMETADATA** `-c copy` from slide timestamps | free | CPU |

**Talking head: NO (default).** For math-heavy finance, a constant presenter face causes split attention away from equations (Mayer image principle; eye-tracking evidence) with no learning gain. Default = clean narrated slides. **Optional corner presenter** (intro/transition/motivation only, shrinks during dense math) is the evidence-backed upside if wanted — if pursued, use **MuseTalk** (MIT, code+weights, real-time on A100, 256px is fine corner-sized). Avoid Wav2Lip (non-commercial + 96px blur) and LivePortrait (video-driven, no audio lip-sync).

**Why Chatterbox over the current XTTS default:** XTTS-v2 is **CPML non-commercial** and **orphaned** (Coqui shut down Jan 2024 → no commercial license obtainable). Chatterbox is true MIT on code **and** weights, so it is safe whether ASSIP videos are internal, free, or ever distributed/monetized; it clones from ~7–10 s, runs faster-than-realtime on A100, and is actively maintained (Turbo, Dec 2025). It drops into the existing `synthesize_narration` dispatcher as a new `TTS_BACKEND=chatterbox` tier with `speaker_wav`-style cloning, mirroring the XTTS plumbing.

### ALTERNATIVE (clearly labeled)
**If videos are guaranteed strictly non-commercial / internal-university only:** swap TTS to **F5-TTS** (comparable naturalness, RTF ≈ 0.15 on A100, clone from 5–15 s) — **but its pretrained weights are CC-BY-NC**, so it is unsafe for any distribution beyond internal/free use. Keep everything else identical. (No-GPU clone-free fallback: **Kokoro-82M**, Apache-2.0, 54 preset voices, CPU-realtime — clean license but loses the instructor's voice.)

This stack keeps the existing `make_video_hopper.py` shape: one `.pptx` in → one `.mp4` out; only the TTS backend, a WhisperX caption step, a normalize step, and the finishing chapter/encode steps are added.

---

## 5. Build plan (phased)

### P1 — GMU template + branded deck restyle  *(runs HERE)*
- Create `book/decks/templates/` + author `assip-reference.pptx` (Master/layouts only; Green/Gold/Black, Figtree/Open Sans/Noto Serif, GMU logo on title masters, preserved Pandoc layout names).
- Commit the GMU logo to `assets/brand/` (download from Bynder portal — needs NetID) and create `assets/figures/week-N/` trees.
- Wire `reference-doc:` into `_template.qmd` + all decks; `make` one week and visually verify masters/fonts/logo + that `::: notes` still land in pptx notes.

### P2 — Author per-subchapter decks + scripts  *(runs HERE)*
- Split the 8 monolithic `week-NN.qmd` into **40 `chXY.qmd` deck sources** (Quarto route — lower risk, aligns with the existing one-`.qmd`-per-deck Makefile wildcard; avoids python-pptx slide-range surgery). This is the load-bearing change: the deck currently has **no machine-readable subchapter boundary** (only `#` headings are the title + two code-comment lines).
- Carry over / refine the existing detailed `::: notes` scripts; keep the "Key takeaway" callout per slide; keep TTS-friendly prose (spell out digits/symbols).

### P3 — Wire per-subchapter Hopper render  *(generate HERE, submit ON HOPPER)*
- Replace the 8-week list with a 40-item `(week, subchapter)` manifest (`clips.jsonl`); grow `--array=1-40%4`; add `SUBCH` env; make `DECK_QMD/DECK_PPTX/OUT_MP4` subchapter-aware.
- **Bake the video stack into `environment.yml`** (TTS/Chatterbox, python-pptx, pdf2image, ffmpeg, WhisperX) so jobs stop pip-installing on A100 time.
- Add `TTS_BACKEND=chatterbox` tier + WhisperX caption step + loudnorm + libx264-CRF19/faststart + FFMETADATA chapters. **Split into two arrays:** GPU array (TTS + WhisperX) and CPU array (rasterize/encode/normalize/mux) so the A100 isn't held during x264.
- Verify the `[CHECK]`-tagged SBATCH values (`--partition`, `--account=nextgen2026`, `--qos`, `gpu:a100:1`, time) against current GMU ORC before mass submit.

### P4 — 1-subchapter PILOT before mass render  *(submit ON HOPPER)*
- Render **one** chapter (suggest `ch11`) end-to-end on Hopper: branded deck → Chatterbox narration (with/without Prof. Gao voice sample) → captions → normalized/encoded MP4 + VTT.
- Review brand fidelity, voice quality, caption alignment, loudness, file size, wall-time/GPU-h. Only then launch the `--array=1-40%4` mass render.

**Environment boundary:** decks, scripts, the reference `.pptx`, the SLURM/manifest plumbing, and a local CPU smoke-test (`make_video.py`, gTTS) can all be built/validated **in this environment**. The **A100 TTS + caption + mass array render must run on GMU Hopper** (per memory: Hopper is the workhorse; submit via SLURM, not locally).

---

## 6. Open decisions for the user

1. **Subchapter granularity.** Chapter-file (40 videos) vs H2-section (349). **Recommended default: chapter-file = 40 videos** (5/week × 8); revisit option-Section later only for specific dense chapters (ch2.5, ch4.3, ch1.5).
2. **Include labs/mentors/packs?** 40 (chapters only) vs 54 (+labs+mentors) vs 56 (+reading-guide packs). **Recommended default: 40 now**, add the 14 labs+mentors in a second wave if the pilot lands well.
3. **TTS narration voice — synthetic vs cloned from Prof. Gao.** **Recommended default: Chatterbox (MIT) cloned from a clean ~30 s Prof. Gao sample**, with a synthetic Chatterbox preset as the consistent fallback. (If strictly internal/non-commercial forever, F5-TTS is the higher-naturalness alt but CC-BY-NC.)
4. **Talking head: yes/no.** **Recommended default: NO** — narrated slides only (best pedagogy + cheapest + zero per-clip GPU). Optional add-on: a small **MuseTalk** corner presenter for intros/transitions only, decided after the pilot.
5. **Slide engine.** Keep **Quarto → pptx** (current, lowest-risk, reuses existing decks/Makefile/notes convention) vs switch to python-pptx generation. **Recommended default: keep Quarto**, branded via the single `assip-reference.pptx`.
6. **Where the heavy render runs.** **Recommended default: GMU Hopper A100** for TTS + captions (GPU array) with ffmpeg assembly/encode on a CPU array; this environment is for authoring decks/scripts/pipeline + a 1-chapter CPU smoke test, not the mass GPU render.

---

## 7. LOCKED DECISIONS (2026-06-17) — authoritative; overrides defaults above

| # | Decision | Choice |
|---|---|---|
| Granularity | Forced by the **≤5-minute hard cap** | **Chapter is the container; split into ≤5-min segments at `##` section boundaries** (~700 narration words/clip). "If more to cover, make more videos." |
| Scope | What becomes videos | **ALL 56 source items**: 40 chapters + 6 labs + 8 mentor sessions + 2 reading-guide packs |
| Est. clip count | from 56 items @ ≤5 min | **~160–200 clips** (same ~600–800 min total audio → **~6–8 A100 GPU-h** for TTS+captions; unchanged by chunking) |
| Narration voice | Cloned | **Chatterbox (MIT), cloned from a clean ~30 s Prof. Gao WAV sample** (user provides). Synthetic Chatterbox preset = fallback. |
| Talking head | None | **No presenter** — narrated slides only. (MuseTalk corner head revisitable post-pilot.) |
| Slide engine | Keep current | **Quarto `.qmd` → `.pptx`**, branded via one `assip-reference.pptx` master |
| Distribution | Path A | **Manual bulk upload to YouTube `@LeiGao-gmu`**; links auto-recovered via title-code → public-uploads read (free API key, no OAuth/quota/audit) → `video-map.json` |
| Site link | Embed | **Per-subchapter YouTube embed** injected via `_includes/` (like notebook-buttons), with **GitHub-archived MP4 fallback** (Git LFS / Releases) so no embed is dead |
| Title convention | for auto-map | `[MEF W{w}.{c} P{part}] {Section Title}` (carries the code the link-recovery parses) |

**Fact-check fixes applied (from adversarial verify):**
- The four accent hexes (Red `#CC4824`, Teal `#008285`, Navy `#004F71`, Gray `#727579`) are **VERIFIED** on the official gmu.edu guidelines page — upgrade from "[LIKELY-OFFICIAL]".
- **Chatterbox embeds inaudible PerTh watermarking** in every clip — harmless for teaching; documented so it isn't mistaken for an artifact.
- **Operational gate (unchanged):** the `[CHECK]` SLURM values (`--partition=gpuq`, `--account=nextgen2026`, `--qos=gpu`, `gpu:a100:1`, `--time`) must be confirmed against current GMU ORC **before** the mass `--array` submission.

**User-provided assets still needed (not blocking P1/P2 authoring):**
1. A clean **~30 s WAV** of Prof. Gao speaking (for the voice clone) — needed before the P4 pilot render.
2. The current **GMU logo** file from the NetID-gated Bynder brand portal → committed to `assets/brand/` — needed before publishing (P1 can proceed logo-light).

**Environment boundary:** Quarto + LibreOffice are **not** installed in the authoring environment, so all `.qmd→.pptx→png→mp4` rendering (and the pilot) runs on **Hopper**. Here we produce: the reference `.pptx`, the 56 segmented deck sources + scripts, the SLURM/manifest/`environment.yml` pipeline, and the site-embed plumbing.
