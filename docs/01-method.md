# 01 · The method: a video is a function of time

<!-- Copyright 2026 Matheus Patricio Pessoa Santana — framezero (MIT) -->

## The idea

Most web animation is *imperative*: start a timer, move things a bit every tick. That's terrible for video, because you can't jump to second 7.3, frames depend on how fast the machine is, and two renders never match.

framezero scenes are **declarative**: one function, `seek(t)`, computes the whole picture for any instant.

```js
const DURATION = 12.6;
function seek(t) {
  const p = E.out(prog(t, 0.2, 0.6));          // 0 → 1 between 0.2 s and 0.6 s, eased
  pose($('#title'), { o: p, y: lerp(40, 0, p) }); // fade + rise
}
```

`prog(t, a, b)` is the core of everything. It's 0 before `a`, 1 after `b`, and linear in between. Pass it through an easing and map it to any property. Because nothing depends on the previous frame:

- **Any frame can be rendered alone**, which makes instant stills for review.
- **Renders are reproducible**: same HTML, same video, bit for bit.
- **Slow machines don't drop frames.** They just take longer.
- **AI agents can reason about it**, since "at t = 3.4 the label is at x = 600" is just arithmetic.

## The pipeline

```
scene.html ── <!--BASE--> gets Inter font + motion.js ──┐
                                                        ▼
            Playwright (headless Chromium, 1080×1920, deviceScaleFactor 1 or 2)
                  for i in 0..N:  seek(i / fps) → screenshot
                                                        ▼
            ffmpeg (bundled by imageio-ffmpeg) → H.264 High, yuv420p, BT.709, AAC 320k
                                                        ▼
                                          video.mp4  (+ soundtrack.wav muxed in)
```

- **4K is just `deviceScaleFactor: 2`.** The layout stays 1080×1920 CSS px and Chromium paints at 2160×3840, so your coordinates never change.
- **`--frames-dir`** saves JPGs first and encodes in 4-second chunks (`kit/assemble.sh`). That keeps peak RAM low enough for a 1 GB sandbox.

## Why not…

| Tool | Trade-off |
|---|---|
| **After Effects / Premiere** | Manual, paid, not scriptable by an agent, hard to version. |
| **CapCut templates** | Fast but generic, and everyone recognizes them. |
| **Remotion** | Excellent, same deterministic idea. But it needs React, Node and a bundler, and its license has company terms. framezero is the no-build version. |
| **Manim** | Great for math explainers, not built for app UI and screenshots. |
| **CSS animations + screen recording** | Not deterministic, drops frames, can't seek, can't reach 4K60 on a small machine. |

## Anatomy of a scene file

```html
<!doctype html><html><head><meta charset="utf-8">
<!--BASE-->                         ← font + helpers injected here
<style> html,body{width:1080px;height:1920px;overflow:hidden} … </style>
</head><body>
<!--ICONS-->                        ← optional SVG sprite (use with <svg><use href="#i-star"/></svg>)
<div class="scene" id="sHook"> … </div>
<div class="scene" id="sFeat"> … </div>
<script>
  const DURATION = 12.6;
  /* setup: build DOM once (lists, split letters…) */
  function seek(t) { /* set EVERY animated property for instant t */ }
  seek(0);                          ← so opening the file in a browser shows frame 0
</script></body></html>
```

**Tip:** open the scene in a normal browser and type `seek(3.2)` in the console to scrub by hand.
