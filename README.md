<div align="center">

# framezero

### Your best frame is frame zero.

**Make scroll-stopping vertical promo videos for your app with HTML, a little JavaScript and code-generated music.**
**No video editor, no After Effects, no stock music, no subscriptions. 4K60 output from a laptop or a 1 GB cloud sandbox.**

Written for **humans** *and* for **AI coding agents** (Claude Code, Codex, Cursor, Copilot, Gemini CLI…).

[![smoke](https://github.com/matheusvibecoder-vibecodas/framezero/actions/workflows/smoke.yml/badge.svg)](https://github.com/matheusvibecoder-vibecodas/framezero/actions/workflows/smoke.yml)
[![License: MIT](https://img.shields.io/badge/license-MIT-FFC233)](LICENSE)
[![Agent Skill](https://img.shields.io/badge/Agent%20Skill-ready-6A4BFF)](skills/framezero/SKILL.md)
[![AGENTS.md](https://img.shields.io/badge/AGENTS.md-included-13D18C)](AGENTS.md)
[![PRs welcome](https://img.shields.io/badge/PRs-welcome-FF7A52)](CONTRIBUTING.md)

**[Website](https://matheusvibecoder-vibecodas.github.io/framezero/)** · **English** · [Português](LEIAME.md)

<img src="media/estuda-tour-hook.gif" width="230" alt="estuda+ tour video — hook">&nbsp;&nbsp;<img src="media/starter.gif" width="230" alt="starter template">&nbsp;&nbsp;<img src="media/estuda-tour-challenge.gif" width="230" alt="estuda+ tour video — daily challenge">

<sub>Left/right: real TikTok/Reels videos for <b>estuda+</b>, a free study app (on-screen text in Portuguese). Center: the English starter template in this repo.</sub>

</div>

---

## Why this exists

I'm an indie dev from Brazil. I built a free study app and needed videos for TikTok and Instagram. Editors were slow and the results looked generic. So I asked: *what if a video were just a web page that knows what to draw at any instant `t`?*

That turned into a tiny pipeline. With it I made five promo videos in two weeks, each one better than the last. This repo packages the **pipeline**, the **storytelling rules** I learned (some the hard way), and **instructions an AI agent can follow** to make a video for *your* app from scratch.

## How it works (30-second version)

```
scene.html  ──seek(t)──▶  Playwright screenshots every frame  ──▶  ffmpeg  ──▶  video.mp4 (1080p or 4K60)
soundtrack.py  ──numpy──▶  lo-fi music + whooshes/pops synced to the same timeline  ──▶  muxed in
```

1. **A scene is one HTML file** (1080×1920) with `const DURATION` and a pure function `seek(t)` that positions everything for instant `t`. There are no timers and no CSS animations. Because every frame is deterministic, each one can be rendered and reviewed individually.
2. **`kit/render.py`** opens it in headless Chromium, calls `seek(i/fps)` for every frame, screenshots, and pipes to ffmpeg.
3. **`kit/sound.py`** synthesizes the music and sound effects from math, so there's **zero copyright risk**. You place each sound at the same second the animation happens.
4. **`--stills`** renders single frames in seconds, so you (or your agent) can *look* at the video before spending minutes on a full render.

## Quickstart

```bash
git clone https://github.com/matheusvibecoder-vibecodas/framezero && cd framezero
pip install -r requirements.txt && python3 -m playwright install chromium   # add --with-deps on fresh Linux

# 1) look at a few frames (2 seconds)
python3 kit/render.py templates/starter.html out/shot --stills 0,3.5,6.6,10.9

# 2) make the soundtrack and the full video (1080p30, ~2 min)
python3 templates/soundtrack.py out/soundtrack.wav
python3 kit/render.py templates/starter.html out/starter.mp4 --audio out/soundtrack.wav

# 3) final quality: 4K60, low-RAM chunked mode
python3 kit/render.py templates/starter.html out/starter-4K.mp4 --scale 2 --fps 60 --crf 16 \
        --audio out/soundtrack.wav --frames-dir /tmp/frames
```

<img src="media/starter-strip.jpg" alt="starter template — contact sheet">

Then copy `templates/` and make it yours: change the CONFIG block, redraw `appUI()` (or drop in screenshots), and keep the soundtrack's times in sync.

## Using it with an AI coding agent

Point your agent at the repo and say something like:

> *"Read AGENTS.md. Make a 15–25 s vertical promo for my app (screenshots in `./shots`). The hook should be a POV. Lo-fi music. Show me stills before rendering."*

- [`AGENTS.md`](AGENTS.md) is the operating manual: the workflow, the hard rules, the QA loop and the known pitfalls. Claude Code, Codex, Cursor, Gemini CLI and Copilot all pick it up.
- [`skills/framezero/SKILL.md`](skills/framezero/SKILL.md) is the same knowledge as an installable **Agent Skill**. Copy the folder to `~/.claude/skills/` or to your agent's skills dir.
- [`llms.txt`](llms.txt) is a map of the repo for LLMs.

The workflow is designed around what agents are good at (writing deterministic code) and what they're bad at (judging motion they can't see). The answer is **contact sheets of stills**: agents can look at those and judge them. One rule matters most: *"vision points, the DOM decides."* Use the screenshot to spot a problem, then confirm it by measuring the element.

## The playbook (what actually makes people stop scrolling)

| Rule | Why |
|---|---|
| **Frame 0 is the thumbnail and the hook.** All hook text is fully visible at `t=0`. No fade-in and no black intro. | People decide in under a second, and the first frame is what shows in the grid. |
| **Context by second 3** (*"5 things it does"*), then a **pattern interrupt every 2–4 s**. | Use a new color, a zoom, a label or a sound to reset attention. |
| **Show the real product.** Use real screens in a phone, plus camera moves and labels. | Viewers trust UI more than adjectives. |
| **Save the best for last and say so** (*"the last one is the best"*). | An open loop keeps people watching. |
| **Text-only, big, inside the safe zone** (x 80–940, y 220–1480 at 1080×1920). | Most people watch muted, and the TikTok/Reels UI covers the edges. |
| **Every visual event has a sound.** Whoosh before cuts, impact on slams, pop on labels, coin on rewards. | Sound makes motion feel physical, even at low volume. |
| **Seamless loop.** The last 0.4 s wipes back into frame 0. | Rewatches count. |
| **End with a CTA that matches your stage.** Before launch, *"coming soon · follow to know when it launches"*. | A "link in bio" to nothing loses trust. |

Full guide: [`docs/`](docs/).

## Showcase: the estuda+ series

All of these were made with this kit, and every one has sound and a 4K60 master.

**#4 App tour** (39 s), *"POV: I found the app that studies with me"*. It shows 5 features on real screens, with a Stories-style progress bar and a lo-fi track. → [`examples/estuda-tour`](examples/estuda-tour)

<img src="media/estuda-tour-strip.jpg" alt="estuda+ tour — contact sheet">

**#3 Daily challenge quiz** (33.5 s), *"Bet you can't get all 3"*. It's built to get comments.

<img src="media/estuda-challenge-strip.jpg" alt="estuda+ challenge — contact sheet">

**#2 AI tutor** (25 s), *"Stuck on homework at 11:47 pm?"*

<img src="media/estuda-tutor-strip.jpg" alt="estuda+ tutor — contact sheet">

What we learned along the way, including the flops, is in [`docs/08-case-study-estuda.md`](docs/08-case-study-estuda.md).

## Made something with framezero?

Open a **[Show your video](https://github.com/matheusvibecoder-vibecodas/framezero/issues/new?template=showcase.yml)** issue. The best ones get featured here. New to the code? Try a [good first issue](https://github.com/matheusvibecoder-vibecodas/framezero/labels/good%20first%20issue) or read [CONTRIBUTING.md](CONTRIBUTING.md).

Want to see a video *about* framezero? It's in [`examples/framezero-promo`](examples/framezero-promo/), and the MP4 is attached to the [v0.1.0 release](https://github.com/matheusvibecoder-vibecodas/framezero/releases/tag/v0.1.0).

## Repo map

```
kit/            the engine — render.py, assemble.sh (4K in 1 GB RAM), motion.js (helpers), sound.py (synth), base.css (Inter), icons.svg
templates/      starter.html + soundtrack.py — a complete 12.6 s English promo to copy
examples/       estuda-tour/ — the real 39 s tour video (scene + screenshots + soundtrack)
docs/           01 method · 02 story & hooks · 03 animation · 04 phone & camera · 05 sound · 06 rendering · 07 publishing · 08 case study · 09 QA checklist
skills/         framezero/SKILL.md — Agent Skill
AGENTS.md       operating manual for AI agents
```

## FAQ

**Why not Remotion / After Effects / CapCut?** Remotion is great but needs React and a bundler. After Effects and CapCut are manual and hard for an agent to drive. framezero is plain HTML + JS + Python with nothing to configure, and your agent already knows all three.

**Do I need a GPU?** No. Rendering is CPU-only. A 39 s 4K60 video takes about 23 minutes on a tiny 1-vCPU sandbox, and much less on a laptop.

**Can I use trending TikTok sounds instead?** Yes. Render with the code-generated track as a safe default, then pick a trending sound in the app when posting and lower the original audio.

**Is the music really copyright-free?** Yes. It's generated by `kit/sound.py` from sine waves and noise, and nothing is sampled.

## License

Code and docs: [MIT](LICENSE). The bundled Inter font is under the SIL Open Font License. The **estuda+** name, logo and app screenshots in `examples/` and `media/` are © Matheus Patricio Pessoa Santana. They are included as a reference and are **not** covered by the MIT license, so don't reuse them in your own videos. See [NOTICE.md](NOTICE.md).

<div align="center"><sub>Made in Brazil 🇧🇷 by <a href="https://github.com/matheusvibecoder-vibecodas">@matheusvibecoder</a>. If this helped you ship a video, a ⭐ helps a lot.</sub></div>
