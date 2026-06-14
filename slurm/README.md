# slurm/ — Hopper SLURM scripts for the teaching-video pipeline

This directory holds the SLURM batch scripts that render the ASSIP weekly
teaching videos on GMU's Hopper cluster. They are the production counterpart
to `tools/make_video.py` (the local, laptop-sized proof-of-pipeline that lives
alongside `tools/make_video_hopper.py`).

Use Hopper when you want neural-quality narration (Coqui XTTS-v2 on an A100),
4K rendering, optional voice cloning, and parallel rendering of the whole
8-week deck set in roughly the time it takes one local render. Use the local
pipeline for a single revised slide or a quick draft.

> Everything tagged `[CHECK]` in these scripts is a GMU-cluster-specific
> string — partition name, account/allocation, module names, the `gres`
> qualifier, the scratch path. Confirm them against the latest GMU ORC docs
> (or the allocation email you got from ORC) **before your first submission**.
> Background on the cluster, SSH access, and how SLURM works lives in
> `book/appendices/B-python-latex-setup/B4-hopper-slurm.md`.

---

## Files in this directory

| File                          | Purpose                                                   |
|-------------------------------|-----------------------------------------------------------|
| `render_video.sbatch`         | Render ONE week's video on one A100. Reads `$WEEK`.       |
| `render_all_videos.sbatch`    | Array job: render all 8 weekly videos, 4 in parallel.     |
| `README.md`                   | This file.                                                |

The Python that the scripts call lives at `tools/make_video_hopper.py`.

---

## 4-step workflow

### 1. SSH onto a Hopper login node

```bash
ssh NETID@hopper.orc.gmu.edu              # [CHECK] login hostname with ORC
```

(See Appendix B.4 for SSH-key setup and the `~/.ssh/config` alias.)

### 2. Clone the repo (first time) or pull (subsequent)

```bash
cd $HOME
git clone https://github.com/<you>/ASSIP8weeks.git    # or rsync from your laptop
cd ASSIP8weeks
git pull
```

Big intermediates and the XTTS-v2 model weights live in `/scratch/$USER`,
not in `$HOME`. The first time you run the pipeline, pre-warm the model:

```bash
export XDG_CACHE_HOME="/scratch/$USER/.cache"       # [CHECK] scratch path
mkdir -p "$XDG_CACHE_HOME"
module load miniconda                                # [CHECK] module name
conda activate finlab
pip install --user "TTS>=0.22"
python -c "from TTS.api import TTS; TTS('tts_models/multilingual/multi-dataset/xtts_v2')"
```

This downloads ~2 GB of weights once; subsequent jobs reuse the cache.

### 3. Submit the array job

```bash
sbatch slurm/render_all_videos.sbatch                       # production 4k
sbatch --export=RES=1080 slurm/render_all_videos.sbatch     # quick draft
sbatch --array=3,7 slurm/render_all_videos.sbatch           # only weeks 3 & 7
```

Optional voice cloning (Prof. Gao's 30s reference WAV must already be on
scratch — never commit it):

```bash
sbatch --export=VOICE_SAMPLE=/scratch/$USER/voice/prof_gao_30s.wav \
       slurm/render_all_videos.sbatch
```

### 4. Monitor and retrieve

```bash
squeue -u $USER                                 # which array tasks are running
sacct -j <ARRAY_JOB_ID> --format=JobID,State,Elapsed,MaxRSS    # post-mortem
tail -f slurm-logs/render-all-<JOB>_<TASK>.out  # live log of one task
```

When the queue empties, rsync the videos back to your laptop:

```bash
# Run on your LAPTOP, not on Hopper.
rsync -avzP NETID@hopper.orc.gmu.edu:ASSIP8weeks/videos/  ./videos/
```

---

## Publishing the videos

Rendered 4K videos are ~200–800 MB each. **Do not commit them to git** — they
exceed GitHub's 100 MB per-file hard limit and bloat clones. Pick a hosting
tier:

| Storage tier               | When to use                                         |
|----------------------------|-----------------------------------------------------|
| GitHub Releases            | Simplest. Up to 2 GB per file, free, public.        |
| Cloudflare R2 / Backblaze B2 | Custom domain, cheap egress, served from a CDN.    |
| YouTube (unlisted)         | Free CDN, autoplay/captions; trades off privacy.    |
| GMU MediaSpace             | If captions/transcripts are required by GMU policy. |

Recommended default: upload each rendered MP4 to the repo's GitHub Release
for that ASSIP cohort, and embed it in the Quarto site with a plain
`<video src="...">` tag pointing at the Release asset URL.

---

## Right-sizing the job

After the first end-to-end run, look at the accounting record:

```bash
sacct -j <ARRAY_JOB_ID> --format=JobID,JobName,Elapsed,MaxRSS,ReqMem,State
```

Common adjustments:

- `MaxRSS` well under 32 G → drop `--mem=32G` to `--mem=16G`. Tighter requests
  start sooner.
- `Elapsed` well under 1 h → drop `--time=01:00:00` to `00:30:00`.
- Multiple tasks queued behind one A100 → raise `%4` to `%6` *only* if your
  allocation allows it (check with ORC; some accounts cap concurrent GPUs).

---

## When to use the local pipeline instead

Skip Hopper and just run `python tools/make_video.py ...` on your laptop when:

- You changed one slide and want to re-render that single deck.
- You are previewing narration text and do not need neural TTS quality.
- The cluster is busy / down / you are on travel without VPN.

The two pipelines emit the same MP4 schema (1080p H.264 + AAC), so a viewer
cannot tell which produced a given video — only the narration audio differs.

---

## Where this connects

- **Cluster basics**: `book/appendices/B-python-latex-setup/B4-hopper-slurm.md`
- **Pinned conda env**: `environment.yml` (env name `finlab`)
- **Local pipeline**: `tools/make_video.py`
- **Hopper pipeline**: `tools/make_video_hopper.py`
- **Deck sources**: `book/decks/week-NN.qmd` → `.pptx` via Quarto
