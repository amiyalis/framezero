# 04 · The phone, the camera and labels

<!-- Copyright 2026 Matheus Patricio Pessoa Santana — framezero (MIT) -->

Showing the real app is the most convincing thing a promo can do. Here's how to make it cinematic.

## Two ways to put the app on screen

| | Screenshots (`<img>`) | Drawn UI (HTML/CSS) |
|---|---|---|
| Effort | Low: capture at 1170×2532 (iPhone 3×) | Higher: rebuild the layout |
| Sharpness at 4K + 1.9× zoom | Slightly soft | Razor sharp |
| Can animate inside (taps, typing, counters) | Only overlays | Everything |
| Used in | estuda+ tour (Home, Books, League) | starter template, estuda+ tutor chat, quiz sheet |

Mixing both works well: screenshots for static screens, and drawn HTML for the screen where something happens (a chat, a quiz).

## Geometry

The UI is laid out at **real phone size** (390×844 CSS px), then scaled into the phone:

```
phone: 640×1385 px, bezel 16 px  →  screen width 608 px  →  k = 608 / 390 = 1.559
```

```css
.ui { width:390px; height:844px; transform-origin:0 0; transform:scale(1.559) }
```

So you write UI coordinates as if designing for a phone, and the phone is just a picture frame.

## The camera

Put the phone inside a `#cam` element, and the `#cam` inside a window (`#win`, `overflow:hidden`, below the title area). Moving and scaling `#cam` is the camera.

```js
const C = makeCamera({ k: 1.559, x: 220, y: 560 });   // x,y = where the phone's top-left sits on the video
const shot = C.at(195, 400, 1.45, 540, 1000);         // app point (195,400) → video (540,1000) at 1.45×
const keys = [[0, C.FULL], [0.45, C.FULL], [0.95, shot], [2.6, shot]];   // times relative to the beat
C.apply($('#cam'), C.track(keys, t - beatStart));
```

**Rules learned the hard way:**
- **Keep `ux` at the UI's horizontal center (≈195)** and move the camera mostly vertically. Off-center zooms push labels and chips off the frame edge.
- A zoom of **1.4–1.6** shows a card clearly. Use **1.9** for a single number. Above 2 looks soft with screenshots.
- Hold the zoom long enough for the label (≥ 0.8 s settled), then return to `C.FULL` before the next beat.
- **Swing the phone in** at each new beat (`rotateY` ±35° → 0 over 0.45 s with `E.out5`) so beats feel distinct.
- Fade the top edge of the camera window with a mask so the phone slides under the title cleanly: `-webkit-mask-image: linear-gradient(to bottom, transparent 0, #000 46px)`.
- Give the window `z-index: 5`. Beat backgrounds wiping in with their own z-index will otherwise hide the phone.

## Labels that point at things

A label is a **gold ring** on the detail plus a **dark pill** with 2–4 words (one bold accent word). Its position follows the camera:

```js
const [X, Y] = C.onScreen(shot, ux, uy);    // where that app point is on the video right now
lab.style.transform = `translate(${X}px,${Y}px)`;
pill.style.left = dx + 'px'; pill.style.top = dy + 'px';   // offset so it doesn't cover the detail
```

- Pop in with `E.back` (scale 0.3 → 1) and a `pop()` sound. Leave fast.
- Keep the pill inside the safe zone. Check the extreme zoom frame in your stills.
- One label at a time, two per beat at most.

## Hook phone

In the hook, the phone is decoration plus proof:
- It starts **already on screen at frame 0**, slightly tilted (`rotateZ(-7deg)`).
- It hops on the beat (sine bumps at 0.5 / 1.0 / 1.5 s) with a gentle 3D sway (`rotateY(-13° · sin(2.6t))` inside a `perspective` parent).
- It **cycles screens** in rhythm, sliding each one in from the right like a finger swipe.
- **Badges** pop out from behind it with an `E.back` overshoot and float a little.
- To exit, it flies up toward the camera (`translateY(-900px) scale(1.7)` over 0.2 s) and hands off to the next scene.
