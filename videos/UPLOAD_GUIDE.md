# YouTube Upload Guide — ASSIP Empirical Finance Camp
**Channel:** @LeiGao-gmu  •  **Clips:** 457  •  **Title code:** `[MEF Wx.y Pn]`
The site embeds videos by reading the `[MEF …]` code from each YouTube
title. These files are **named as their titles**, so uploading auto-fills
the titles — you never type them.

> **Upload as Unlisted.** The lessons stay off your public channel listing/search
> but still embed on the site. Recovery (step 4) reads them via a one-time owner
> **OAuth** login — an API key can't see Unlisted videos. (Don't use *Private*:
> private videos refuse to embed on a public page.)

## 1. (Once) Smoke-test one video
YouTube sets each title from the filename. Upload **one** clip (Unlisted), then run
step 4's command — if it reports `1 clip mapped`, titles are preserved and you can
bulk-upload with confidence.

## 2. Upload, one week-folder at a time
For each `Week-N/` folder under `videos/upload_ready/`:
1. YouTube Studio → **Create → Upload videos** → drag in *all* files from the folder.
2. Titles auto-fill from the filenames (the `[MEF …]` code is what matters).
3. Set visibility to **Unlisted**. Optionally paste the description from the manifest.
4. After processing, select them all → **Add to playlist** → the playlist below.

## 3. Folders → playlists
| Folder | Playlist (create in Studio) | Clips |
|---|---|---|
| `Week-1/` | Week 1 — Probability & Inference | 54 |
| `Week-2/` | Week 2 — OLS & Inference | 54 |
| `Week-3/` | Week 3 — Causal Inference | 56 |
| `Week-4/` | Week 4 — Quasi-Experiments | 65 |
| `Week-5/` | Week 5 — Reading the Canon | 52 |
| `Week-6/` | Week 6 — Text, AI & Alt-Data | 62 |
| `Week-7/` | Week 7 — Your Project I | 54 |
| `Week-8/` | Week 8 — Your Project II | 60 |
| | **Total** | **457** |

## 4. Recover the links into the site (owner OAuth)
One-time Google Cloud setup (see `tools/yt_oauth.py` for the click-path):
1. Cloud Console → enable **YouTube Data API v3**.
2. **OAuth consent screen**: User type *External*; add your Google account as a *Test user*.
3. **Credentials → Create OAuth client ID → "TVs and Limited Input devices"**; download the JSON.
4. Save it as `~/.config/leigao-video/client_secrets.json`.

Then, from this repo:
```bash
python tools/build_video_map.py --oauth
```
It prints a URL + code to authorize once (device flow), then prints
`N clips mapped across X/Y items` and a coverage line; a `WARNING:` names any
subchapter still missing a video. Writes `video-map.json` (keyed by item id: ch11,
lab1, mentor3, …). Both editions share the channel — the script's `[MEF]` regex
picks only its own videos and ignores the other edition's.

> The login is cached at `~/.config/leigao-video/yt_token.json`; later runs reuse
> it silently. In OAuth *Testing* mode the token expires after ~7 days — if a run
> says it must re-authorize, just approve the code again.

Want to preview the result *before* uploading? Dry-run it against the
filenames YouTube will receive (no API, no upload):
```bash
ls videos/upload_ready/*/*.mp4 | sed 's#.*/##; s#\.mp4$##' > /tmp/titles.txt
python tools/build_video_map.py --titles-from /tmp/titles.txt --out /tmp/preview.json
```

## 5. Publish to the site
```bash
git add video-map.json && git commit -m 'Wire YouTube video embeds' && git push
```
GitHub Actions rebuilds; every subchapter page then shows a *“Watch this lesson”*
player with one button per ≤5-min part. Pages with no map entry simply omit it.

## Notes
- A few titles contained characters illegal in filenames (`: | ? \ " /`); those
  were replaced for the filename only (e.g. `:` → ` -`). The **exact** titles are
  in `videos/upload_manifest.csv`. The `[MEF …]` code is never affected, so
  link recovery is unaffected — this only changes the on-screen title text.
- All titles are within YouTube's 100-char limit (no truncation).
