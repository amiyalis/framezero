# 06 · Rendering: stills, 1080p, 4K60 on 1 GB of RAM

<!-- Copyright 2026 Matheus Patricio Pessoa Santana — framezero (MIT) -->

## Modes

```bash
# Stills for QA: PNGs at chosen seconds, ~0.3 s each
python3 kit/render.py scene.html out/q --stills 0,1.5,3.2

# Preview: 1080×1920, 30 fps, piped straight to ffmpeg
python3 kit/render.py scene.html out/preview.mp4 --audio track.wav

# Master: 2160×3840, 60 fps, JPG frames first, then chunked encode
python3 kit/render.py scene.html out/master-4K.mp4 --scale 2 --fps 60 --crf 16 --audio track.wav --frames-dir /tmp/frames
```

| Option | Meaning |
|---|---|
| `--scale 2` | deviceScaleFactor 2 gives 4K with the same layout coordinates |
| `--fps 60` | smoother motion. Platforms accept 60 fps and it looks premium on fast moves |
| `--crf 16–18` | x264 quality. 16 for masters, 17 for uploads |
| `--audio` | WAV/MP3 to mux. Without it you get a silent stereo track (some platforms dislike video with no audio stream) |
| `--frames-dir` | two-step, low-RAM mode (needs `--audio`) |

## Speed (real numbers)

On a 1-vCPU, 1 GB sandbox: **≈ 1.7 frames/s at 4K**, so a 39 s video at 60 fps (2,340 frames) takes about 23 min, plus about 1 min to encode. 1080p30 runs at about 3 frames/s, so a 12.6 s starter takes about 2 min. A laptop is several times faster.

Run long renders in the background and track progress by counting frames in `--frames-dir`.

## Why chunked encoding

A single x264 process encoding 2160×3840 can use more than 1 GB of RAM and get OOM-killed near the end. `kit/assemble.sh` encodes 240-frame (4 s) chunks with 1–2 threads, then concatenates them with `-c copy` (no quality loss) and muxes the audio.

## Color

Output is tagged **BT.709, TV range, yuv420p, H.264 High** (level 5.2 for 4K, 4.2 for 1080p), which is what phones and platforms expect. Untagged files can look washed out or shifted on iOS.

**Vivid palettes survive compression** better than subtle gradients. Use saturated radial backgrounds (e.g. `#9C85FF → #6A4BFF → #3A1FC2`) and a dot grid. Avoid huge smooth dark gradients without texture, because they band.

## 1080p for upload

Platforms re-encode everything. Uploading a clean 1080p made from your 4K master often looks better than letting them downscale:

```bash
$FF -i master-4K.mp4 -vf scale=1080:1920:flags=lanczos -c:v libx264 -crf 17 -profile:v high -level:v 4.2 \
    -pix_fmt yuv420p -c:a copy -movflags +faststart upload-1080p.mp4
```

## Storage tips

- Videos are big (4K 39 s ≈ 40 MB). Keep scenes and soundtracks in git. Store MP4s in releases, Git LFS or cloud storage, and don't let them bloat the repo history.
- Frames dirs hold thousands of JPGs. Delete them after encoding (`render.py` does this automatically in `--frames-dir` mode).
