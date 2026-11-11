---
name: framezero
description: Create vertical (9:16) promo videos for apps — TikTok, Reels, Shorts — as deterministic HTML scenes rendered to 4K60 MP4 with code-generated, copyright-free music. Use when the user asks for an app promo video, a product teaser, a social-media motion video, a "POV" or feature-tour video, or wants to animate real app screenshots inside a phone.
---

# framezero: app promo videos from HTML

<!-- Copyright 2026 Matheus Patricio Pessoa Santana — framezero (MIT) -->

Repo: https://github.com/matheusvibecoder-vibecodas/framezero. Clone it if `kit/render.py` isn't present.

## Workflow
1. **Ask** (once, briefly): what the app is and its ONE goal, the screenshots (or draw the UI), the launch stage (this sets the CTA), the music mood (lo-fi by default) and the language. Never invent stats or features.
2. **Script** a timeline table first: HOOK 0–2.5 s (readable at frame 0) → CONTEXT ("N things it does", "the last one is the best") → FEATURES of 2.5–6 s each (phone, camera push-in, 1–2 labels settled ≥ 0.8 s) → PAYOFF → CTA 3–4 s → 0.4 s loop wipe back to frame 0. Use a pattern interrupt every 2–4 s.
3. **Build**: copy `templates/starter.html` + `templates/soundtrack.py`. `seek(t)` must be pure (no timers, CSS animations or random). Reset every animated property on each call. Keep text in the safe zone x 80–940, y 220–1480.
4. **QA with stills**: `python3 kit/render.py scene.html out/q --stills 0,1.2,…`, then make a contact sheet and look at it. Check for wrapped text, labels off target, off-center zooms, layers hidden by z-index, and empty transition frames. Vision points, the DOM decides: measure before you fix.
5. **Sound**: give every visual event a sound at the same t (whoosh at t−0.1 before cuts, impact on slams, pop on labels, click on taps, coin/ding on rewards). Use a lo-fi bed and master at 0.70, which is about −13 LUFS.
6. **Render**: 1080p preview with `--audio`, then the 4K master with `--scale 2 --fps 60 --crf 16 --audio … --frames-dir …` (chunked, so it fits in ~1 GB RAM). Downscale to 1080p for posting. Check frames from the final MP4.
7. **Deliver**: the MP4s plus one caption for TikTok and Instagram (hook + question + max 5 hashtags).

The full rules, helper API and pitfalls are in `AGENTS.md` and `docs/` in the repo.
