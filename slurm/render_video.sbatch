#!/bin/bash
# ----------------------------------------------------------------------------
# render_video.sbatch -- render ONE weekly teaching video on a Hopper A100.
#
# This is the per-week SLURM job. The array dispatcher in
# slurm/render_all_videos.sbatch sets WEEK and submits one task per week.
# You can also run it standalone for a single week:
#
#     sbatch --export=WEEK=week-03 slurm/render_video.sbatch
#
# Every GMU-cluster-specific string is marked [CHECK] -- confirm with GMU ORC
# (or your group's allocation email) before the first submission.
# ----------------------------------------------------------------------------

#SBATCH --job-name=render-video
#SBATCH --partition=gpuq                # [CHECK] GPU partition name (ORC docs)
#SBATCH --account=nextgen2026           # [CHECK] your allocation/account
#SBATCH --qos=gpu                       # [CHECK] some Hopper queues require a GPU QOS
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=8
#SBATCH --mem=32G
#SBATCH --gres=gpu:a100:1               # [CHECK] gres name; might be gpu:A100:1
#SBATCH --time=01:00:00                 # one video: 10-30 min on A100; pad to 1h
#SBATCH --output=slurm-logs/render-video-%x-%j.out
#SBATCH --error=slurm-logs/render-video-%x-%j.err

set -euo pipefail

# ---------- 0. inputs --------------------------------------------------------
# WEEK is set by the array dispatcher; allow override for standalone runs.
: "${WEEK:?WEEK env var is required (e.g. WEEK=week-03)}"

# Resolution: 1080 by default; pass RES=4k for the production render.
: "${RES:=4k}"

# Optional voice-cloning sample (Prof. Gao's 30s reference). Leave empty to
# use the XTTS default speaker. Secrets/personal samples MUST NOT be committed
# to the repo -- keep this file on scratch.
: "${VOICE_SAMPLE:=}"

REPO_DIR="${REPO_DIR:-$SLURM_SUBMIT_DIR}"
cd "$REPO_DIR"

mkdir -p slurm-logs videos book/decks

LOG="slurm-logs/render-video-${WEEK}-${SLURM_JOB_ID:-local}.log"
exec > >(tee -a "$LOG") 2>&1

echo "============================================================"
echo "render_video.sbatch"
echo "  job id     : ${SLURM_JOB_ID:-N/A}"
echo "  node       : $(hostname)"
echo "  date       : $(date)"
echo "  repo dir   : $REPO_DIR"
echo "  WEEK       : $WEEK"
echo "  RES        : $RES"
echo "  voice clone: ${VOICE_SAMPLE:-(default speaker)}"
echo "============================================================"

# ---------- 1. modules + conda env ------------------------------------------
module purge
module load miniconda                   # [CHECK] exact module name on Hopper
module load cuda                        # [CHECK] CUDA toolkit version for XTTS/torch
module load ffmpeg          || true     # [CHECK] some sites bundle ffmpeg; ok if absent
module load libreoffice     || true     # [CHECK] needed for pptx -> pdf rasterization
module load poppler         || true     # [CHECK] provides pdftoppm

# The repo's pinned env (see environment.yml at repo root).
source activate finlab || conda activate finlab

# ---------- 2. extra video-pipeline deps (idempotent --user installs) -------
# These are NOT in environment.yml because they are only needed on Hopper for
# the video render. --user keeps them out of the shared env.
python -m pip install --user --quiet --upgrade \
    "TTS>=0.22"            \
    "python-pptx>=0.6"     \
    "pdf2image>=1.17"      \
    "ffmpeg-python>=0.2"   \
    "gTTS"                 \
    "pyttsx3"              \
    "manim>=0.18"          || true

# ---------- 3. (one-time) Coqui XTTS-v2 model weights ------------------------
# XTTS-v2 weights (~2 GB) live in scratch so the home quota survives. The TTS
# package auto-downloads on first use, but pre-warming avoids first-run delays
# in array jobs.
#
# Manual prewarm (run ONCE on a login or interactive node before the array job):
#
#   export XDG_CACHE_HOME="/scratch/$USER/.cache"   # [CHECK] scratch path
#   mkdir -p "$XDG_CACHE_HOME"
#   python -c "from TTS.api import TTS; TTS('tts_models/multilingual/multi-dataset/xtts_v2')"
#
# Alternative: curl/wget from HuggingFace (license: CPML, non-commercial):
#   wget -P "$XDG_CACHE_HOME/tts/tts_models--multilingual--multi-dataset--xtts_v2/" \
#        https://huggingface.co/coqui/XTTS-v2/resolve/main/model.pth \
#        https://huggingface.co/coqui/XTTS-v2/resolve/main/config.json \
#        https://huggingface.co/coqui/XTTS-v2/resolve/main/vocab.json
#
# Either way, the env var below routes the cache off $HOME for every job:
export XDG_CACHE_HOME="${XDG_CACHE_HOME:-/scratch/$USER/.cache}"     # [CHECK]
mkdir -p "$XDG_CACHE_HOME"

# ---------- 4. sanity-check GPU ---------------------------------------------
nvidia-smi || { echo "ERROR: no GPU visible; check --gres line"; exit 3; }
echo "CUDA_VISIBLE_DEVICES=${CUDA_VISIBLE_DEVICES:-unset}"

# ---------- 5. render the deck (Quarto -> PPTX) ------------------------------
DECK_QMD="book/decks/${WEEK}.qmd"
DECK_PPTX="book/decks/${WEEK}.pptx"
OUT_MP4="videos/${WEEK}.mp4"

if [[ ! -f "$DECK_QMD" ]]; then
    echo "ERROR: deck source $DECK_QMD not found"
    exit 4
fi

echo "[$(date)] quarto render $DECK_QMD -> pptx"
quarto render "$DECK_QMD" --to pptx

if [[ ! -f "$DECK_PPTX" ]]; then
    echo "ERROR: quarto did not produce $DECK_PPTX"
    exit 5
fi

# ---------- 6. render the narrated video -------------------------------------
echo "[$(date)] make_video_hopper.py -> $OUT_MP4"
VOICE_ARGS=()
if [[ -n "$VOICE_SAMPLE" && -f "$VOICE_SAMPLE" ]]; then
    VOICE_ARGS+=(--voice-sample "$VOICE_SAMPLE")
fi

export TTS_BACKEND="${TTS_BACKEND:-xtts}"

python tools/make_video_hopper.py \
    --input  "$DECK_PPTX" \
    --output "$OUT_MP4"   \
    --res    "$RES"       \
    "${VOICE_ARGS[@]}"

echo "[$(date)] DONE: $OUT_MP4 ($(du -h "$OUT_MP4" | cut -f1))"
