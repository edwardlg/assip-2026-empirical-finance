#!/bin/bash
# ----------------------------------------------------------------------------
# render_clips.sbatch -- SLURM array: render ONE ≤5-min teaching clip per task.
#
# Each array task renders one segment deck (chXY-pN.qmd) end-to-end:
#   Quarto qmd -> branded pptx -> (make_video_hopper) narrated mp4 -> finish_clip
#   (loudnorm + H.264 1080p +faststart + WhisperX .vtt captions).
#
# Submit (array size = number of clips in the manifest):
#   N=$(wc -l < book/decks/chapters/clips.jsonl)
#   sbatch --array=1-${N}%4 slurm/render_clips.sbatch
#
# Voice cloning: export VOICE_SAMPLE=/path/to/lei_gao_30s.wav before submit
# (omit to use Chatterbox's built-in voice). TTS_BACKEND defaults to chatterbox.
#
# This pipeline is EDITION-AGNOSTIC: set REPO_DIR + MANIFEST to point at a
# different camp (e.g. the NextGen 8-week edition) and the same script renders it.
#
# Every GMU-cluster-specific string below is [CHECK] -- confirm with GMU ORC
# (Office of Research Computing) before a mass submit.
# ----------------------------------------------------------------------------
#SBATCH --job-name=assip-render-clips
#SBATCH --partition=gpuq                # [CHECK] GPU partition name on Hopper
#SBATCH --account=nextgen2026           # [CHECK] allocation / account string
#SBATCH --qos=gpu                       # [CHECK] some clusters require a GPU QOS
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=8
#SBATCH --mem=32G
#SBATCH --gres=gpu:a100:1               # [CHECK] gres name (TTS + WhisperX use the A100)
#SBATCH --time=00:40:00                 # generous per ≤5-min clip; tune after pilot
#SBATCH --output=slurm-logs/render-clip-%A_%a.out
#SBATCH --error=slurm-logs/render-clip-%A_%a.err

set -euo pipefail

REPO_DIR="${REPO_DIR:-$SLURM_SUBMIT_DIR}"
cd "$REPO_DIR"
mkdir -p slurm-logs videos/clips

MANIFEST="${MANIFEST:-book/decks/chapters/clips.jsonl}"
export TTS_BACKEND="${TTS_BACKEND:-chatterbox}"
RES="${RES:-1080}"

# Map array task id (1-based) to a clip record.
LINE=$(sed -n "${SLURM_ARRAY_TASK_ID}p" "$MANIFEST")
if [ -z "$LINE" ]; then
  echo "No manifest line ${SLURM_ARRAY_TASK_ID} in $MANIFEST"; exit 1
fi
read -r DECK OUT_MP4 OUT_VTT SLUG < <(python3 -c "
import json,sys
c=json.loads(sys.argv[1])
print(c['deck'], c['out_mp4'], c['out_vtt'], c['slug'])
" "$LINE")

echo "=== clip $SLUG ==="
echo "deck=$DECK  out=$OUT_MP4  backend=$TTS_BACKEND  voice=${VOICE_SAMPLE:-<builtin>}"

# Idempotency: skip if the final mp4 already exists and is newer than the deck.
if [ -f "$OUT_MP4" ] && [ "$OUT_MP4" -nt "$DECK" ]; then
  echo "up-to-date; skipping."; exit 0
fi

WORK="$(mktemp -d)"
trap 'rm -rf "$WORK"' EXIT

# 1) Quarto: branded deck -> pptx (inherits assip-reference.pptx via _metadata.yml)
quarto render "$DECK" --to pptx
PPTX="${DECK%.qmd}.pptx"
[ -f "$PPTX" ] || { echo "quarto produced no pptx for $DECK"; exit 1; }

# 2) Narrated raw video (Chatterbox TTS on the A100; voice-clone if VOICE_SAMPLE set)
#    VOICE_SAMPLE may be .m4a/.mp3/.wav; convert non-wav to wav once per task.
VOICE_ARGS=()
if [ -n "${VOICE_SAMPLE:-}" ]; then
  if [ "${VOICE_SAMPLE##*.}" = "wav" ]; then
    VOICE_WAV="$VOICE_SAMPLE"
  else
    VOICE_WAV="$WORK/voice.wav"
    ffmpeg -y -loglevel error -i "$VOICE_SAMPLE" -ac 1 -ar 24000 "$VOICE_WAV"
  fi
  VOICE_ARGS=(--voice-sample "$VOICE_WAV")
fi
python3 tools/make_video_hopper.py --input "$PPTX" --output "$WORK/raw.mp4" \
        --res "$RES" "${VOICE_ARGS[@]}"

# 3) Finish: loudnorm + H.264 1080p +faststart + WhisperX captions sidecar
python3 tools/finish_clip.py --input "$WORK/raw.mp4" --output "$OUT_MP4" --vtt "$OUT_VTT"

echo "DONE: $OUT_MP4 (+ $OUT_VTT if captions available)"
