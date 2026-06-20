#!/usr/bin/env python3
"""
batch_render.py -- render a STRIPE of clips in ONE process so the Chatterbox
model loads once per SLURM task (keeps the A100 busy; respects ORC limits).

Usage:  batch_render.py <clips.jsonl> <task_id> <num_tasks>
Env:    VOICE_SAMPLE (optional), RES (default 1080)
Per clip: pre-rendered beamer <deck>.pdf + <deck>.qmd notes -> narrated mp4
(+ transcript .srt) -> finish_clip (loudnorm + caption burn-in) -> out_mp4.
Idempotent: skips clips whose out_mp4 already exists.
"""
import sys, os, json, shutil, tempfile, subprocess
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import make_video_hopper as mv

manifest, task, ntask = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
res = os.environ.get("RES", "1080")
voice = os.environ.get("VOICE_SAMPLE")
voice = Path(voice) if voice else None
W, H = mv.RES_PRESETS[res]
FINISH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "finish_clip.py")

clips = [json.loads(l) for l in open(manifest) if l.strip()]
mine = clips[task::ntask]                       # stripe-by-ntask
print(f"[batch] task {task}/{ntask}: {len(mine)} of {len(clips)} clips", flush=True)
done = fail = skip = 0

for c in mine:
    qmd = Path(c["deck"]); pdf = qmd.with_suffix(".pdf"); out = Path(c["out_mp4"])
    if out.exists() and out.stat().st_size > 2000:
        skip += 1; continue
    if not pdf.exists():
        # render the beamer PDF on demand (TinyTeX packages cached on /scratch)
        r = subprocess.run(["quarto", "render", str(qmd), "--to", "beamer"],
                           capture_output=True, text=True)
        if not pdf.exists():
            print(f"[batch] beamer render FAILED {qmd}: {r.stderr[-300:]}", flush=True)
            fail += 1; continue
    out.parent.mkdir(parents=True, exist_ok=True)
    work = Path(tempfile.mkdtemp(prefix="br_"))
    try:
        pngs = mv.pdf_to_pngs(pdf, work / "slides", W, H)
        notes = mv.extract_notes_from_qmd(qmd)
        notes = (notes + [""] * len(pngs))[:len(pngs)]
        clip_list, cap_notes, cap_durs = [], [], []
        for i, png in enumerate(pngs):
            cn, _ = mv.split_manim_marker(notes[i])
            wav = work / f"slide-{i+1:03d}.wav"
            mv.synthesize_narration(cn or " ", wav, voice)   # model cached across clips
            clip = work / f"clip-{i+1:03d}.mp4"
            shutil.copy2(wav, clip.with_suffix(".wav"))
            mv.build_clip(png, wav, clip, W, H)
            clip_list.append(clip); cap_notes.append(cn); cap_durs.append(mv.audio_duration(wav))
        raw = work / "raw.mp4"
        mv.concat_with_crossfades(clip_list, raw, W, H)
        srt = work / "raw.srt"; mv.write_srt(cap_notes, cap_durs, srt)
        subprocess.run([sys.executable, FINISH, "--input", str(raw),
                        "--output", str(out), "--srt", str(srt)], check=True)
        done += 1
        print(f"[batch] DONE {out.name}", flush=True)
    except Exception as exc:
        fail += 1
        print(f"[batch] FAIL {out.name}: {exc!r}", flush=True)
    finally:
        shutil.rmtree(work, ignore_errors=True)

print(f"[batch] task {task} complete: done={done} skip={skip} fail={fail}", flush=True)
