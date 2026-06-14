#!/bin/bash
# ----------------------------------------------------------------------------
# render_all_videos.sbatch -- SLURM array job that renders all 8 weekly
# teaching videos for ASSIP in parallel on Hopper A100s.
#
# Submit:    sbatch slurm/render_all_videos.sbatch
# Override:  sbatch --export=RES=1080 slurm/render_all_videos.sbatch
#
# The --array=1-8%4 line caps the cluster footprint at 4 concurrent A100s,
# so all 8 videos finish in ~1 hour of wall time (each ~15-30 min at 4k).
#
# Every GMU-cluster-specific string is marked [CHECK]; confirm with GMU ORC.
# ----------------------------------------------------------------------------

#SBATCH --job-name=render-all-videos
#SBATCH --partition=gpuq                # [CHECK] GPU partition name on Hopper
#SBATCH --account=nextgen2026           # [CHECK] allocation / account string
#SBATCH --qos=gpu                       # [CHECK] some clusters require a GPU QOS
#SBATCH --array=1-8%4                   # 8 weeks, 4 concurrent
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=8
#SBATCH --mem=32G
#SBATCH --gres=gpu:a100:1               # [CHECK] gres name
#SBATCH --time=01:00:00
#SBATCH --output=slurm-logs/render-all-%A_%a.out
#SBATCH --error=slurm-logs/render-all-%A_%a.err

set -euo pipefail

REPO_DIR="${REPO_DIR:-$SLURM_SUBMIT_DIR}"
cd "$REPO_DIR"
mkdir -p slurm-logs videos

# Map array task id (1..8) to the week label used by deck filenames.
WEEKS=( \
    week-01 week-02 week-03 week-04 \
    week-05 week-06 week-07 week-08 \
)
IDX=$((SLURM_ARRAY_TASK_ID - 1))
if (( IDX < 0 || IDX >= ${#WEEKS[@]} )); then
    echo "ERROR: array task id $SLURM_ARRAY_TASK_ID out of range 1..${#WEEKS[@]}"
    exit 1
fi
WEEK="${WEEKS[$IDX]}"
export WEEK

# Default resolution; override with --export=RES=1080 for a quick draft.
export RES="${RES:-4k}"

# Optional voice-cloning sample; keep on scratch (do NOT commit).
export VOICE_SAMPLE="${VOICE_SAMPLE:-}"

echo "============================================================"
echo "render_all_videos.sbatch -- task $SLURM_ARRAY_TASK_ID -> $WEEK"
echo "  array job  : $SLURM_ARRAY_JOB_ID"
echo "  task id    : $SLURM_ARRAY_TASK_ID"
echo "  node       : $(hostname)"
echo "  date       : $(date)"
echo "  RES        : $RES"
echo "============================================================"

bash slurm/render_video.sbatch
