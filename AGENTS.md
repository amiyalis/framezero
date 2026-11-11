# AGENTS.md — operating manual for AI coding agents

<!-- Copyright 2026 Matheus Patricio Pessoa Santana — framezero (MIT) -->

You are making a **vertical promo video (1080×1920, 9:16)** for an app, using this repo's pipeline. These instructions work in Claude Code, Codex, Cursor, Gemini CLI, Copilot agents and anything else that can run shell commands and look at images.

## 0. Setup (once per machine/session)

```bash
pip install -r requirements.txt
python3 -m playwright install chromium        # on a fresh Linux box: python3 -m playwright install --with-deps chromium
python3 kit/render.py templates/starter.html out/check --stills 0   # smoke test → out/check-0s.png
```
- There's no system ffmpeg? That's fine. `imageio-ffmpeg` ships its own binary: `python3 -c "import imageio_ffmpeg;print(imageio_ffmpeg.get_ffmpeg_exe())"`.
- If Chromium can't find shared libraries on a minimal box, put them in a folder and set `FRAMEZERO_CHROME_LIBS=/path/to/libs`.
- Sandboxes that reset can wipe pip packages and `/tmp`. If imports fail mid-task, reinstall. Keep scratch output in a stable folder.

## 1. Gather inputs before writing code

Ask the human (in one message, max 3–4 questions) only for what you can't infer:
1. **What's the app and the ONE thing it should make the viewer feel/do?** (download, follow, comment)
2. **Screens:** real screenshots (best: 1170×2532 or any phone-ratio PNG) or should you draw the UI in HTML?
3. **Launch stage → CTA:** not launched = *"coming soon · follow to know when it launches"*. Launched = *"free on the App Store / Play Store"*. Never write "link in bio" if there's nothing there.
4. **Music mood:** calm lo-fi (default; works for study, productivity and lifestyle) or energetic (120 BPM, kicks, claps).
5. **Language** of the on-screen text.

Never invent stats, user counts, ratings or testimonials. Only show features that really exist.

## 2. Write the script as a timeline table first

Write it before you touch any HTML, like this:

| t (s) | Scene | On screen | Sound |
|---|---|---|---|
| 0–2.5 | HOOK | "POV: you found the app that PLANS YOUR DAY", plus the phone already visible | impact at 0 |
| 2.5–4.5 | CONTEXT | "3 things it does" · "the last one is the best" | impact, pops |
| 4.5–… | FEATURE ×N | number + title, phone, camera push-in, 1–2 labels | whoosh, pop per label |
| … | PAYOFF | "and the BEST is #N" | riser → impact |
| last 3–4 s | CTA | "100% FREE", "coming soon", "follow…" | slams, ding |
| last 0.4 s | LOOP | wipe back to frame 0 | whoosh |

Rules of thumb:
- **Total 15–40 s.** 12–20 s for one feature, 30–40 s for a full tour.
- **Feature beats run 2.5–6 s.** A label must stay settled for **≥ 0.8 s**. Allow **≈ 0.3 s per word** of reading time.
- Use a **pattern interrupt every 2–4 s**: a new background color, a camera move, a label, a scene cut or a counter.
- See `docs/02-story-and-hooks.md` for hook formulas.

## 3. Build the scene

Copy `templates/starter.html` (and `templates/soundtrack.py`) to a new folder. Then:

**Hard rules (breaking these produces broken videos):**
- `seek(t)` must be **pure**: the same `t` gives the same pixels. **No** `setTimeout`, `requestAnimationFrame`, CSS `transition`/`animation`, `Date.now()` or `Math.random()`. If you need randomness, seed it.
- **Every element touched by `seek` must have all its animated properties set on every call.** If you write `el.style.transform += …`, first reset `el.style.transform` in the same call, or it accumulates across frames.
- **Frame 0 must be the best-looking frame.** The hook text should be fully visible at t=0 (scale pulses are OK, fade-ins are not).
- **Safe zone:** important text stays inside x 80–940 and y 220–1480. Below 1480 and to the right of 940 are covered by the caption, the buttons and the username.
- **Fonts:** use `Inter` (embedded by `<!--BASE-->`). Never rely on web fonts or remote images, because rendering is offline.
- **Big words wrap.** A single 9-letter word at 300 px won't fit in 1080 px. Fit text to ≤ 920 px (the starter has a `.fit` helper) or drop to ~240 px.
- Assets use **relative paths** next to the scene (`screens/home.png`). The renderer writes its temporary page in the same folder.
- `z-index`: once a layer gets an explicit `z-index` (scene wipes do), anything that must stay on top needs a higher explicit one.

**Helpers you get for free** (`kit/motion.js`, documented in `docs/03-animation.md`): `prog`, `lerp`, `E.*` easings, `pose`, `presence`, `show`, `slam`, `rise`, `pulse`, `shake`, `wipeUp`, `wipeDiagonal`, `drift`, `splitLetters`/`letters`, and `makeCamera()` for phone zooms (`docs/04-phone-and-camera.md`).

## 4. QA loop: look before you render

Full renders are slow (4K60 runs at about 1.7 frames/s on a small box). Stills are instant:

```bash
python3 kit/render.py my/scene.html out/q --stills 0,1.2,2.6,4.0,6.5,9.0,12.0
```
Combine them into **one contact sheet** and look at it (PIL: paste the frames resized to 270×480 side by side). For each frame, check that:
- the text is fully inside the safe zone and **not wrapped or cut** (e.g. "MELHO/R" means the font is too big);
- labels point at the right UI element and don't cover what they describe;
- zooms keep the subject **centered**. Off-center zooms crop labels at the edges. Keep the camera target at the horizontal center of the UI;
- nothing is invisible because a background layer covers it (z-index);
- there are no frames between scenes that are empty or a flat color. Pick times inside transitions too.

**Vision points, the DOM decides.** If a screenshot suggests something is off, confirm it by measuring (`page.evaluate` + `getBoundingClientRect()`) before you "fix" it. Also measure text only after `document.fonts.ready`, or the widths will be wrong.

Watch for `PAGE ERROR:` lines from `render.py`. A JS exception freezes the scene silently.

## 5. Sound

Edit the soundtrack script to match **your** timeline. Every visual event gets a sound at the **same second**:

| Event | Sound |
|---|---|
| scene cut / wipe | `whoosh(.3)` at **t − 0.1** |
| word slam / number | `impact()` + optional `pop()` |
| label / badge / chip appears | `pop(1040, .12)` + `click(.02)` |
| tap on screen | `click()` |
| reward / XP / correct | `ding()` or `coin()` |
| big reveal | `riser(.8)` before, then `impact()` |
| typing | `click(.018)` per character |

Default bed: `lofi_keys()` + `lofi_beat()` + `vinyl()`. Master with `.master(dur, 0.70)`, which lands near **−13 LUFS** (verify with ffmpeg `-af ebur128`). Stop the drums at the loop point. See `docs/05-sound.md`.

## 6. Render

```bash
python3 my/soundtrack.py out/track.wav
python3 kit/render.py my/scene.html out/preview.mp4 --audio out/track.wav                   # 1080p30, check timing with sound
python3 kit/render.py my/scene.html out/final-4K.mp4 --scale 2 --fps 60 --crf 16 \
        --audio out/track.wav --frames-dir /tmp/frames-final                               # master
# 1080p for upload from the 4K master:
FF=$(python3 -c "import imageio_ffmpeg;print(imageio_ffmpeg.get_ffmpeg_exe())")
$FF -i out/final-4K.mp4 -vf scale=1080:1920:flags=lanczos -c:v libx264 -crf 17 -profile:v high -level:v 4.2 -pix_fmt yuv420p -c:a copy -movflags +faststart out/final-1080p.mp4
```
- Long renders: run them **in the background** and poll by counting files in `--frames-dir`. Don't `pgrep -f "<pattern>"` inside the same shell loop, because it matches itself.
- Audio-only changes don't need a re-render: remux with `-map 0:v -map 1:a -c:v copy`.
- After the render, sample 6–8 frames from the **final MP4** (not the HTML) into a contact sheet and check them.

## 7. Deliver

Give the human: the MP4 (1080p for posting, 4K master), **one caption** that works on TikTok + Instagram (hook line + question to drive comments + **max 5 hashtags**, since both platforms cap at 5), and a one-line note on what to post with (e.g. "add a trending sound at low volume"). See `docs/07-publishing.md`.

## Pitfalls we hit (so you don't)

- A 4K single-process ffmpeg can exceed 1 GB of RAM and get OOM-killed. That's why `--frames-dir` + `kit/assemble.sh` encode in 4 s chunks.
- `getBoundingClientRect()` inside a scaled element returns **scaled** px. Use `offsetWidth` for layout px, or better, pure CSS.
- If text measured at setup comes out with the wrong width, the font hadn't loaded yet. Use CSS sizing (`left:0;right:0`) instead of JS measurement where possible.
- `transform +=` without a reset in the same `seek` call means transforms accumulate between frames.
- A 300 px single word wraps ("MELHO/R"); use 240 px.
- An off-center camera zoom crops the labels; center it.
- Wipes add `z-index` to background layers, which hides the phone behind them. Give the camera window `z-index: 5`.
- Don't fake engagement (fake stats, fake reviews). It gets noticed.
