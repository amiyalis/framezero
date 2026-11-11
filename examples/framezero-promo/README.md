# framezero promo: a video about framezero, made with framezero

<!-- Copyright 2026 Matheus Patricio Pessoa Santana — framezero (MIT) -->

12.6 s, 1080×1920. It uses the same timeline as `templates/starter.html`, so `templates/soundtrack.py` syncs without changes. Good to read as a second example after the starter.

| t (s) | Beat | Technique |
|---|---|---|
| 0.0 | "POV: your app's promo video is just HTML" | Full hook on frame 0, staggered pulses at 0.5 / 1.0 / 1.5, code card bumps with each beat |
| 2.4 | 1/3 write seek(t) | Diagonal color wipe, code types in line by line, label pops |
| 5.0 | 2/3 render 4K60 | Film strip of real frames slides by, frame counter climbs to 2340, result badge |
| 7.6 | 3/3 music from code | Deterministic "waveform" (sines of t), sound chips pop on beat |
| 10.2 | CTA: free & open source | Wipe up, slams, wordmark, repo pill, star ask |
| 12.2 | Loop | Hook wipes back in over the CTA |

```bash
python3 templates/soundtrack.py out/promo.wav
python3 kit/render.py examples/framezero-promo/promo.html out/promo.mp4 --audio out/promo.wav
```

The finished video is attached to the [v0.1.0 release](https://github.com/matheusvibecoder-vibecodas/framezero/releases/tag/v0.1.0).
