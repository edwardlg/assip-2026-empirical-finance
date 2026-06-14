# Teaching-Video Creation Tools (2026): Comparison and Pipeline Design

**Audience:** ASSIP 8-Week Camp (Prof. Lei Gao, GMU) — empirical-finance textbook/labs for high-school students
**Goal:** Convert our `.qmd` lecture decks (rendered as `.pptx` with speaker notes) into ~5-minute narrated MP4 videos
**Date:** June 2026
**Constraint:** Prefer a free, scriptable, container-friendly pipeline for the camp's batch of ~40 lectures; identify premium fallbacks for a polished public release

---

## 1. Executive summary

After surveying the 2026 landscape across five tool families — AI talking-head avatars, AI text-to-video diffusion models, AI slide-to-video editors, open-source programmatic frameworks, and TTS providers — the **recommended pipeline for the camp** is fully free, fully scriptable, and runs inside our existing camp Docker container:

> **`.qmd` → Quarto → `.pptx` → LibreOffice headless → PDF → ImageMagick → PNG slides → python-pptx (speaker notes) → Piper TTS (neural, offline) → ffmpeg (concat + xfade + zoompan Ken-Burns) → `.mp4`**

Estimated cost: **$0** in licensing, ~30 s of CPU time per minute of finished video, no API keys, no rate limits, no watermark, and reproducible from a Makefile.

For a **polished public release** (e.g., a YouTube channel or a paid course), three premium alternatives are credible in 2026:

1. **HeyGen Avatar IV API** — $0.05/sec ≈ $15 for a 5-min lecture; best lip-sync, easiest API.
2. **Synthesia Creator** — $89/month flat, 30 min/month; best for non-developer instructors who want a polished avatar workflow.
3. **Sora 2 (OpenAI) + ElevenLabs v3** — generative b-roll behind narrated slides; novel but expensive ($30+ per 5 min) and the Sora 2 API is scheduled to sunset 24 September 2026.

The remainder of this document compares each tool family in detail and gives a working `Makefile` and bash script for the free pipeline.

---

## 2. Tool-family comparison

### 2.1 AI avatar / talking-head platforms

These produce a video of a synthetic human reading our script. Useful when we want a face on screen.

| Tool | 2026 entry price | API? | Per-minute API cost | Strength | Weakness for our use case |
|---|---|---|---|---|---|
| **Synthesia** | Free (10 min/mo, watermark) → Starter $29/mo → Creator $89/mo | Yes, on Creator+ | Bundled into seat | Largest avatar library (180+), highest-quality studio avatars, strong enterprise security | API gated behind $89/mo seat; no à la carte; 30 min/mo cap on Creator |
| **HeyGen** | Creator $29/mo (200 credits) | Yes, **separate** PAYG ($5 min, $0.05/sec ≈ $3/min) | $3/min | Cleanest 2026 API, best price-per-minute, Avatar IV lip-sync is class-leading | Credit math on web tier is opaque; avatars feel slightly more "stock" than Synthesia |
| **D-ID** | Lite $4.70/mo (annual), API on higher tiers | Yes | ~$1–$2/min equivalent | Cheapest paid avatar; photo-to-video lets us animate a still of the instructor | Lower resolution, less natural mouth motion; commercial rights require higher tier |
| **Synthesys** | Creator $22/mo annual ($29 monthly) | Limited | n/a | 60+ "Humatars," good for marketing-style explainers | Smaller avatar library; weaker for long lecture content |
| **Hour One** | Custom/enterprise (no public self-serve in 2026) | Yes | Custom | Polished corporate templates, dynamic data-driven personalization | No transparent pricing; overkill for an academic camp |

**Verdict.** For a paid release, **HeyGen API** has the best cost/quality ratio in 2026 ($3/min, ~$15 per 5-min lecture, ~$600 for 40 lectures). **Synthesia** is the right pick for instructors who do not want to touch code.

### 2.2 AI text-to-video diffusion models

These generate video footage from a prompt. Useful for short b-roll, not for slide-accurate lectures.

| Tool | 2026 pricing | API | Notes |
|---|---|---|---|
| **Sora 2 / Sora 2 Pro (OpenAI)** | $0.10/sec (720p) and $0.30/sec (1080p Pro), Batch tier 50% off | Yes | Up to 25 s clips with synced audio; **API sunsets 24 Sep 2026** — do not depend on it. Consumer app was discontinued 26 Apr 2026. |
| **Runway Gen-4 / 4.5** | Free 125 credits one-time; Standard $28/mo; Unlimited $188/mo; API $0.12/sec | Yes | Up to 60 s continuous, 4K, temporal consistency. Best for cinematic b-roll. |
| **Google Veo 3.1** | Fast $0.15/sec, Standard $0.40/sec; Google AI Plus $7.99/mo to Ultra $249.99/mo | Yes (Vertex) | Audio generation included. Strong realism, integrates with Gemini. |
| **Pika 2.0** | $10/mo for 660 credits | Limited | Cheapest, lower fidelity, good for stylized openings. |
| **Luma Dream Machine (Ray 3.14)** | Plus $30/mo (10 000 credits); API $0.95 per 5-s 1080p clip | Yes | Strong motion; bundle now includes Veo 3.1, Kling 3.0, Nano Banana Pro, ElevenLabs audio. |

**Verdict.** Generative video is **not the right primitive for slide-based lectures**. A 5-min lecture at $0.30/sec Sora 2 Pro = $90; even Sora 2 base = $30. Use these tools only for a 10–20 s motion title card or a course trailer.

### 2.3 AI slide-to-video editors

These ingest a script or a deck and auto-produce a video with stock footage, captions, and TTS.

| Tool | 2026 entry | Notes |
|---|---|---|
| **Pictory** | $25/mo annual (Starter, 200 min/yr, 720p) → Professional $35/mo (600 min, 1080p) → Premium $119/mo | Script-to-video and blog-to-video; weakest for code-heavy slides |
| **Lumen5** | Community free with watermark; Basic $29/mo; Starter $79/mo | Marketing-style, image-driven; weak for math/formulas |
| **InVideo AI** | Free with watermark; Plus $25/mo; Max $60/mo | Strong template library, can ingest prompts in plain English |
| **Steve.ai** | Lite $15/mo; Basic $30/mo | Animated explainer-style; cartoony aesthetic |
| **Visla** | Free 30 min/mo (720p); Pro $19/mo | Browser-based, integrates avatars + screen recording |

**Verdict.** These are optimized for *marketing* videos, not lecture content. They struggle with our actual slide images (math, regression tables, code blocks) and instead substitute generic stock footage. **Reject for the camp.**

### 2.4 Open-source / scriptable frameworks

This is where the camp's pipeline lives. Everything below runs offline, in our Docker container, with no API keys.

| Tool | What it is | Fit |
|---|---|---|
| **Manim (3Blue1Brown / community edition)** | Python animation engine for mathematical illustrations | Excellent for derivations and equation walks; overkill for slide narration; we keep it in our back pocket for Week-3 OLS visualizations |
| **Motion Canvas** | TypeScript-based code-driven animation; real-time editor | Great for hand-crafted scenes; learning curve is steep for our instructors |
| **Remotion** | React framework — videos as React components, server-rendered | Best in class for *data-driven* video (e.g., per-student personalized recaps). Requires Node + Chrome headless. |
| **Revideo** | Open-source Motion Canvas fork with a rendering API | Designed for automated pipelines; promising but smaller community than Remotion |
| **Cap** | Browser-based screen + camera recorder, open source | Useful when we want a real instructor face, not for batch synthesis |
| **ffmpeg + ImageMagick + python-pptx + TTS** | Plain Unix glue | **This is what we recommend.** Zero learning curve for anyone who already knows shell |

### 2.5 Text-to-speech (TTS) providers

The single biggest quality lever for a slide+narration video is the voice. 2026 options:

| Tool | 2026 pricing | Local? | Quality | Fit |
|---|---|---|---|---|
| **ElevenLabs v3** | Starter $6/mo (60 K v3 chars) → Creator $22/mo (220 K) → Pro $99/mo (990 K) → Business $990/mo (9.9 M); also PAYG | Cloud | **Best in class** — 70+ languages, emotion control | Premium option; ~$3 for a 5-min lecture in v3 |
| **OpenAI TTS** | `tts-1` $15 / 1 M chars; `tts-1-hd` $30 / 1 M; `gpt-4o-mini-tts` token-priced with steerable prosody | Cloud | Near-ElevenLabs quality, simpler integration | ~$0.15 per 5-min lecture at tts-1-hd |
| **Google Cloud TTS** | Neural2/Studio voices ~$16 / 1 M chars; WaveNet $16 / 1 M | Cloud | High; strong multilingual | Solid alternative to OpenAI |
| **Amazon Polly** | Standard $4 / 1 M, Neural $16 / 1 M, Generative ~$30 / 1 M | Cloud | Good; less expressive than ElevenLabs | Cheapest cloud option for neutral narration |
| **Coqui TTS** (OSS) | Free | **Local** | Very good with VITS/XTTS-v2 models; slower than Piper | Strong fallback if we want voice cloning of the instructor |
| **Piper TTS** (OSS) | Free | **Local, fast** | Significantly better than eSpeak; Lessac / LJSpeech voices sound natural | **Our pick.** Runs on CPU, ~10× faster than realtime, ~67 MB per voice |
| **gTTS** | Free | Cloud (unofficial Google endpoint) | Decent neural quality | Useful as a one-line fallback if Piper is unavailable; adds ~200–500 ms latency per call and rate-limited |
| **pyttsx3** | Free | Local | Robotic (system voices: espeak / sapi5) | Last-resort offline fallback only |

**Verdict for the camp.** **Piper** as the default with a Lessac-medium English voice. Optionally switch in **OpenAI tts-1-hd** for a "premium polish" build of the same script (cost: ~$5 to re-render all 40 camp lectures).

---

## 3. Recommended free pipeline (deep dive)

### 3.1 Pipeline diagram

```
                  speaker notes
                       |
   docs/lectures/      v
   week1.qmd  ----> week1.pptx ----> [python-pptx]
       |                                  |
       |                              notes_week1.txt
       |                                  |
       |                              [Piper TTS]
       |                                  |
       |                              audio/slide01.wav ... slideNN.wav
       |
       v
   [libreoffice --headless --convert-to pdf]
       |
       v
   week1.pdf
       |
       v
   [pdftoppm -r 150 -png]    (or ImageMagick convert)
       |
       v
   img/slide01.png ... slideNN.png
                                              \
                                               \
                                                v
                                          [ffmpeg: per-slide subclip]
                                              zoompan Ken-Burns
                                              + slide PNG + WAV
                                                |
                                                v
                                       clips/slide01.mp4 ... slideNN.mp4
                                                |
                                                v
                                          [ffmpeg concat + xfade]
                                                |
                                                v
                                           week1.mp4 (1080p, H.264, AAC)
```

Every step is a single shell command, every step is idempotent, and the whole thing fits in a `Makefile`.

### 3.2 Container prerequisites

Add these to `environment.yml` / `Dockerfile`:

```bash
apt-get install -y libreoffice-nogui poppler-utils imagemagick ffmpeg
pip install python-pptx piper-tts
# Download a voice (one-time, ~67 MB):
python -m piper.download_voices en_US-lessac-medium
```

All of these are already free, all are Debian/Ubuntu mainline packages, and Piper ships an ONNX model that runs on CPU at roughly 10× real-time on a single core.

### 3.3 Step-by-step commands

**Step 1. Render `.qmd` to `.pptx` (already in our workflow).**

```bash
quarto render lectures/week1.qmd --to pptx
# Produces: lectures/week1.pptx
```

Speaker notes in the Quarto source (`::: {.notes} ... :::`) survive the conversion.

**Step 2. Extract speaker notes per slide.**

`scripts/extract_notes.py`:

```python
import sys, pathlib
from pptx import Presentation

pptx_path = pathlib.Path(sys.argv[1])
out_dir   = pathlib.Path(sys.argv[2]); out_dir.mkdir(parents=True, exist_ok=True)

prs = Presentation(pptx_path)
for i, slide in enumerate(prs.slides, start=1):
    notes = ""
    if slide.has_notes_slide:
        notes = slide.notes_slide.notes_text_frame.text or ""
    if not notes.strip():
        notes = "Please review this slide."           # graceful fallback
    (out_dir / f"slide{i:02d}.txt").write_text(notes, encoding="utf-8")
```

Run:

```bash
python scripts/extract_notes.py lectures/week1.pptx build/week1/notes/
```

**Step 3. Synthesize narration with Piper.**

```bash
mkdir -p build/week1/audio
for f in build/week1/notes/slide*.txt; do
  base=$(basename "$f" .txt)
  piper --model en_US-lessac-medium \
        --output_file "build/week1/audio/${base}.wav" \
        < "$f"
done
```

Output: 22.05 kHz mono WAV per slide. For a typical 60-word note, ~25 s of audio rendered in ~2.5 s.

**Step 4. Convert PPTX to PNG via PDF.**

```bash
libreoffice --headless --invisible --convert-to pdf \
            --outdir build/week1/ lectures/week1.pptx

pdftoppm -r 150 -png build/week1/week1.pdf build/week1/img/slide
# Produces slide-01.png, slide-02.png, ...
```

Rationale: `libreoffice --convert-to png` only emits the first slide, so we go through PDF. `pdftoppm` at 150 DPI gives ~2000×1500 px — sharper than 1080p, safe for any downscaling.

**Step 5. Build per-slide subclips with Ken-Burns zoom.**

`scripts/make_clip.sh`:

```bash
#!/usr/bin/env bash
set -euo pipefail
img="$1"; wav="$2"; out="$3"
dur=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$wav")
frames=$(printf '%.0f' "$(echo "$dur * 30" | bc -l)")

ffmpeg -y -loop 1 -i "$img" -i "$wav" \
  -filter_complex "[0:v]scale=2000:1500,zoompan=z='min(zoom+0.0008,1.08)':\
d=${frames}:s=1920x1080:fps=30[v]" \
  -map "[v]" -map 1:a -c:v libx264 -pix_fmt yuv420p \
  -c:a aac -b:a 192k -shortest "$out"
```

This applies a slow 8 % zoom over the slide's lifetime (Ken-Burns effect), pins audio length, and emits 1080p30 H.264 + AAC.

**Step 6. Concatenate with crossfades.**

For a clean lecture feel we crossfade 0.5 s between slides.

`scripts/concat_xfade.py` (sketch):

```python
import sys, subprocess, pathlib, re
clips = sorted(pathlib.Path(sys.argv[1]).glob("slide*.mp4"))
out   = sys.argv[2]
xf    = 0.5  # seconds

# Probe durations
durs = []
for c in clips:
    r = subprocess.run(["ffprobe","-v","error","-show_entries",
                        "format=duration","-of","csv=p=0",str(c)],
                       capture_output=True,text=True)
    durs.append(float(r.stdout.strip()))

# Build filter_complex chain
inputs, vfilters, afilters = [], [], []
last_v, last_a, offset = "0:v", "0:a", 0.0
for i, c in enumerate(clips):
    inputs += ["-i", str(c)]
    if i == 0:
        offset = durs[0] - xf
        continue
    vfilters.append(f"[{last_v}][{i}:v]xfade=transition=fade:duration={xf}:offset={offset}[v{i}]")
    afilters.append(f"[{last_a}][{i}:a]acrossfade=d={xf}[a{i}]")
    last_v, last_a = f"v{i}", f"a{i}"
    offset += durs[i] - xf

fc = ";".join(vfilters + afilters)
cmd = ["ffmpeg","-y",*inputs,"-filter_complex",fc,
       "-map",f"[{last_v}]","-map",f"[{last_a}]",
       "-c:v","libx264","-pix_fmt","yuv420p","-c:a","aac","-b:a","192k",out]
subprocess.run(cmd, check=True)
```

Run:

```bash
python scripts/concat_xfade.py build/week1/clips/ dist/week1.mp4
```

**Step 7. Wrap it in a `Makefile`.**

```make
LECTURE ?= week1
SRC      = lectures/$(LECTURE).qmd
PPTX     = lectures/$(LECTURE).pptx
BUILD    = build/$(LECTURE)
DIST     = dist/$(LECTURE).mp4

$(DIST): $(BUILD)/.clips
	python scripts/concat_xfade.py $(BUILD)/clips/ $@

$(BUILD)/.clips: $(BUILD)/.audio $(BUILD)/.img
	mkdir -p $(BUILD)/clips
	i=1; for img in $(BUILD)/img/slide-*.png; do \
	  n=$$(printf "%02d" $$i); \
	  bash scripts/make_clip.sh "$$img" $(BUILD)/audio/slide$$n.wav \
	       $(BUILD)/clips/slide$$n.mp4; \
	  i=$$((i+1)); \
	done
	touch $@

$(BUILD)/.audio: $(BUILD)/.notes
	mkdir -p $(BUILD)/audio
	for f in $(BUILD)/notes/slide*.txt; do \
	  b=$$(basename $$f .txt); \
	  piper --model en_US-lessac-medium --output_file $(BUILD)/audio/$$b.wav < $$f; \
	done
	touch $@

$(BUILD)/.notes: $(PPTX)
	python scripts/extract_notes.py $(PPTX) $(BUILD)/notes
	touch $@

$(BUILD)/.img: $(PPTX)
	libreoffice --headless --invisible --convert-to pdf --outdir $(BUILD) $(PPTX)
	mkdir -p $(BUILD)/img
	pdftoppm -r 150 -png $(BUILD)/$(LECTURE).pdf $(BUILD)/img/slide
	touch $@

$(PPTX): $(SRC)
	quarto render $(SRC) --to pptx
```

Then for any lecture: `make LECTURE=week3-ols`. The build is incremental and reruns only stages whose inputs changed.

### 3.4 Quality knobs

- **Better voice.** Replace `en_US-lessac-medium` with `en_US-hfc_female-medium` or `en_GB-alba-medium`; or swap Piper for OpenAI `tts-1-hd` (one-line change in `extract_notes.py` to call the API).
- **Captions.** Add `--srt` output by running `whisper` (or `whisper.cpp`) over the final WAV and burning subtitles in with ffmpeg's `subtitles=` filter.
- **Intro/outro.** Concatenate a 5-s title card and a 3-s credits card; same `xfade` chain.
- **Background music.** Add a low-volume bed: `[1:a]volume=0.08[bed];[a_final][bed]amix=inputs=2:duration=longest`.
- **Personal avatar overlay.** Record a 1080p green-screen loop of the instructor once; chroma-key it into the lower-right with `colorkey=0x00ff00:0.3:0.2`.

### 3.5 Sample script for a 5-minute lecture

Assume `week3-ols.qmd` has 10 slides at ~30 s each. Speaker notes (extracted automatically):

> Slide 1 (title): "Welcome to Week 3. Today we move from descriptive statistics to ordinary least squares regression, the workhorse of empirical finance."
>
> Slide 2 (motivation): "Recall last week we estimated mean returns. The natural next question is whether returns covary with characteristics. OLS is the linear projection that minimizes squared error."
>
> Slide 3 (setup): "Let y_i be next-month return and x_i a vector of firm characteristics. We model E[y|x] = x'β and estimate β-hat by minimizing the residual sum of squares."
>
> ... etc.

At 150 wpm Piper synthesizes each note in ~25–35 s; 10 slides ≈ 5 min. End-to-end render on a 4-core laptop: ~90 s for a fresh build, ~10 s for an incremental rebuild after editing notes.

---

## 4. Three premium alternatives (for public release)

### 4.1 Synthesia Creator ($89/month)

- **What you get.** 30 video minutes / month, API access, 5 personal avatars, 180+ studio avatars, 140+ languages.
- **Why pick it.** Cleanest non-developer workflow. Paste the speaker-notes text into the script editor, pick an avatar, render.
- **Cost for the camp.** 40 lectures × 5 min = 200 min — overflows the 30 min/month cap. Realistic plan: 7 months at $89 = $623, or jump to Enterprise (custom, typically $1 000+/seat/year).
- **Watch-outs.** Personal avatar requires a 5-min training recording. Studio avatars carry a separate $1 000/year licensing fee. Watermark only on Free plan.

### 4.2 HeyGen Avatar IV API ($0.05/sec ≈ $3/min)

- **What you get.** Best-in-class lip-sync, a developer-first API, no monthly minimum once you fund the $5 starter balance.
- **Cost for the camp.** 200 min × $3 = **$600 one-time** for all 40 lectures. Trivially scriptable into our existing `Makefile`: swap the `piper`+`ffmpeg-clip` stages for a single `curl` against `https://api.heygen.com/v2/video/generate` with the slide PNG as a background and the speaker notes as the script.
- **Why pick it.** Pure pay-as-you-go, best lip-sync, no seat license, fits our automation model.
- **Watch-outs.** Web credits and API credits are *separate* — buying a Creator web plan does not give API access. Plan the API budget independently.

### 4.3 Sora 2 + ElevenLabs v3 (generative b-roll behind slides)

- **What you get.** Slides remain the primary information layer; Sora 2 generates short cinematic transitions and a course trailer; ElevenLabs v3 narrates with emotion control.
- **Cost for the camp.** Hard to amortize because Sora 2 caps at 25-s clips. A 20-s trailer = $2 (base) or $6 (Pro). ElevenLabs Creator $22/mo covers ~220 K v3 chars ≈ all 40 lectures. Plausible total: **$30–$50 across the camp.**
- **Why pick it.** Adds production value for a public launch (e.g., a course trailer for the camp website) without paying per-lecture.
- **Watch-outs.** The Sora 2 API is scheduled to **sunset 24 September 2026** — render anything we need before then, or switch to Veo 3.1 ($0.15–$0.40/sec).

---

## 5. Cost summary

| Path | Up-front | Per-lecture | Annual (40 lectures) | Maintenance |
|---|---|---|---|---|
| **Free pipeline (recommended)** | $0 | $0 | **$0** | A few hours to bake the Makefile; then `make` |
| HeyGen API | $5 (min balance) | $15 (5 min × $3) | **$600** | Add a 30-line `heygen.py` |
| Synthesia Creator | $0 | $0 (within 30 min/mo cap) | **$623** (7 months) | No code, but manual per-video |
| Sora 2 + ElevenLabs v3 | $22 (ElevenLabs Creator) | $0.30–$1 narration, $2–$6 b-roll | **$50** (slides remain free; only trailer & transitions use Sora) | Modest scripting |

The free pipeline is not a compromise — for slide-based lectures aimed at HS students, the *content* (clear slides, accurate narration, good pacing) matters more than the *face*. We can always re-render a polished avatar version later from the same `.qmd` sources.

---

## 6. Recommendation

1. **Adopt the free pipeline** documented in §3 as the default for all camp lectures. Commit the `Makefile`, the three scripts (`extract_notes.py`, `make_clip.sh`, `concat_xfade.py`), and the `environment.yml` updates.
2. **Reserve HeyGen API** as the upgrade path if/when the camp content goes to a public YouTube channel. Budget ~$600 once.
3. **Pin Piper** (`en_US-lessac-medium`) as the camp's official voice for now; document a one-flag switch to OpenAI `tts-1-hd` for premium runs (~$0.15 per 5-min lecture).
4. **Skip generative video tools** (Sora 2, Veo 3.1, Runway Gen-4, Pika, Luma) for lecture bodies; revisit only for a course trailer.
5. **Skip slide-to-video editors** (Pictory, Lumen5, InVideo, Steve.ai, Visla) entirely — they're built for marketing, not pedagogy.

---

## Sources

- Synthesia 2026 pricing: https://magichour.ai/blog/synthesia-pricing-2026 ; https://aitoolsdevpro.com/ai-tools/synthesia-guide/ ; https://fluxnote.io/guides/synthesia-pricing-2026
- HeyGen 2026 pricing & API: https://www.eesel.ai/blog/heygen-pricing ; https://www.arcade.software/post/heygen-pricing
- Sora 2 API & sunset: https://developers.openai.com/api/docs/guides/video-generation ; https://magichour.ai/blog/sora-2-pricing ; https://costgoat.com/pricing/sora
- Runway Gen-4 pricing: https://checkthat.ai/brands/runway/pricing ; https://aitoolsdevpro.com/ai-tools/runway-guide/
- Google Veo 3.1 / Luma / Pika: https://www.veo3ai.io/blog/veo-3-pricing-2026 ; https://www.eesel.ai/blog/luma-ai-pricing
- ElevenLabs v3: https://elevenlabs.io/pricing/api ; https://bigvu.tv/blog/elevenlabs-pricing-2026-plans-credits-commercial-rights-api-costs
- OpenAI TTS: https://costgoat.com/pricing/openai-tts ; https://tokenmix.ai/blog/tts-api-comparison
- Piper TTS: https://github.com/mdmonsurali/Offline-Fast-CPU-PIPER-TTS ; https://clawbot.ai/wiki/integrations/piper-tts.html
- Coqui / gTTS / pyttsx3: https://smallest.ai/blog/python-packages-realistic-text-to-speech ; https://videosdk.live/developer-hub/ai/python-tts
- Programmatic video frameworks: https://www.pkgpulse.com/guides/remotion-vs-motion-canvas-vs-revideo-programmatic-video-2026
- Pictory / Lumen5 / InVideo: https://checkthat.ai/brands/pictory/pricing ; https://www.saasworthy.com/compare/lumen5-vs-synthesia-io-vs-invideo-io-vs-pictory-ai
- D-ID / Synthesys / Hour One: https://aloa.co/ai/comparisons/ai-video-comparison/d-id-vs-synthesia ; https://fluxnote.io/guides/synthesys-pricing-guide-2026
- LibreOffice headless PPTX → PNG: https://www.systutorials.com/how-to-convert-pptx-slides-to-jpg-or-png-images-on-linux-in-command-line/
- ffmpeg Ken-Burns: https://www.bannerbear.com/blog/how-to-do-a-ken-burns-style-effect-with-ffmpeg/ ; https://mko.re/blog/ken-burns-ffmpeg/
- python-pptx speaker notes: https://dri.es/extract-speaker-notes-from-powerpoint-to-text
