# Example · estuda+ App Tour (39 s, 4K60, lo-fi)

<!-- Copyright 2026 Matheus Patricio Pessoa Santana — framezero (MIT for code; brand assets © — see NOTICE.md) -->

A real video, posted on TikTok/Instagram for **estuda+**, a free study app from Brazil. The on-screen text is in **Portuguese**.

![contact sheet](../../media/estuda-tour-strip.jpg)

| t (s) | Scene | What happens |
|---|---|---|
| 0–2.5 | **Hook** | "POV: achei o app que ESTUDA COMIGO · e é 100% grátis" ("POV: I found the app that STUDIES WITH ME · and it's 100% free"). The phone cycles 4 real screens on the beat, badges pop out, and it flies toward the camera |
| 2.5–4.5 | **Context** | "5 coisas que ele faz" (5 things it does), tiles 1–5, "a última é a melhor" (the last one is the best) |
| 4.5–10 | 1 · Daily plan | Real Home screenshot, camera push-ins, 2 labels, a tap checks an activity |
| 10–15.5 | 2 · Daily challenge | A drawn quiz sheet: "15% of 200?", a tap on 30, green check, +25 XP |
| 15.5–21 | 3 · Free books | Books screenshot, "41 livros" label |
| 21–26.5 | 4 · Weekly league | League screenshot, a heart "like" on a classmate |
| 26.5–27.3 | **Payoff** | "E A MELHOR… é a número 5" (and the BEST is #5), with a riser and an impact |
| 27.3–33.3 | 5 · AI tutor | A drawn chat: the question types out, "typing…", a step-by-step answer with a highlighter |
| 33.3–35.3 | **Recap** | "Tudo isso num app só" (all of this in one app), 5 icons orbiting the logo |
| 35.3–39 | **CTA** | "100% GRÁTIS · Em breve disponível · segue pra saber quando lançar" (coming soon · follow to know when it launches) |
| 38.55–39 | **Loop** | Wipe back into frame 0 |

## Render it

```bash
python3 examples/estuda-tour/soundtrack.py out/tour.wav
python3 kit/render.py examples/estuda-tour/tour.html out/tour.mp4 --audio out/tour.wav                       # 1080p30 preview
python3 kit/render.py examples/estuda-tour/tour.html out/tour-4K.mp4 --scale 2 --fps 60 --crf 16 \
        --audio out/tour.wav --frames-dir /tmp/frames-tour                                                    # 4K60 master (~23 min on 1 vCPU)
```

## Things worth reading in `tour.html`

- `ITENS`: one object per feature with its title, the **camera keyframes** (`F(ux, uy, zoom, X, Y)`) and its **labels**. Most of the video is driven by this table.
- `hookPose(t)`: the animated hook phone (beat hops, 3D sway, screen swipes, badges).
- `camEm()` / `naTela()`: the original camera helpers that became `makeCamera()` in `kit/motion.js`.
- `soundtrack.py`: `ITENS` / `ZOOMS` / `ETQ` tables mirror the scene, so every whoosh and pop lands on its frame.

The code here is in Portuguese (it was written for the estuda+ repo). The starter template in `templates/` is the cleaned-up English version of the same ideas.

**Assets** (logo, screenshots) are © estuda+. They're here only so the example renders. Use your own in your videos.
