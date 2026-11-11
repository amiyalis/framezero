# 03 · Animation: helpers, easing and timing

<!-- Copyright 2026 Matheus Patricio Pessoa Santana — framezero (MIT) -->

Everything below lives in `kit/motion.js` and is injected at `<!--BASE-->`.

## Primitives

| Helper | What it does |
|---|---|
| `prog(t, a, b)` | 0 → 1 between `a` and `b` (clamped) |
| `lerp(a, b, p)` | interpolate |
| `E.out` / `E.out5` | decelerating entrances (out5 = snappier) |
| `E.in` | accelerating exits |
| `E.inOut` | camera moves |
| `E.back` | overshoot pop (badges, labels) |
| `E.expo` | hard slam |
| `pose(el, {o, x, y, s, r, sx, sy})` | sets opacity + transform in one go |
| `presence(t, a, d, b, d2)` | 0→1 entering at `a`, 1→0 leaving at `b` |

## Building blocks

| Helper | Use for | Pair with sound |
|---|---|---|
| `slam(el, t, a, from=2)` | Big words or numbers landing | `impact()` at `a` |
| `rise(el, t, a)` | Subtitles, small lines | — |
| `pulse(t, a, amp)` | A multiplier for beat accents (`s: pulse(t, 1.0, .1)`) | kick or impact |
| `shake(t, a)` | x-offset after an impact | `impact()` |
| `wipeUp(el, t, a)` / `wipeDiagonal(el, t, a)` | Scene transitions | `whoosh()` at `a − 0.1` |
| `drift(el, t)` | Endless dot-grid background motion | — |
| `splitLetters(el)` + `letters(el, t, a)` | Letter-by-letter drop | `click(.02)` per few letters |
| `show(sel, on, z)` | Turn a scene layer on or off | — |

## Timing cheat-sheet

| Thing | Duration |
|---|---|
| Entrance | 0.25–0.4 s |
| Exit | 0.15–0.2 s (exits are faster than entrances) |
| Scene wipe | 0.24–0.3 s |
| Camera push-in | 0.45–0.55 s, `E.inOut` |
| Label settled before it leaves | ≥ 0.8 s |
| Gap between interrupts | 2–4 s |
| Stagger between list items | 0.12–0.18 s |

## Patterns

**Hold, then accent.** Put the motion on the beat (120 BPM = every 0.5 s): `pulse(t, 0.5)`, `pulse(t, 1.0)`, `pulse(t, 1.5)`. Viewers feel the sync even when muted.

**Exit everything together.** At the end of a scene, push all elements up with `E.in` over 0.2 s, and stagger the distance a little (`600 + i * 50` px). It reads as one confident move.

**Pure-function hygiene:**
```js
// ❌ accumulates every frame
el.style.transform += ' translateY(-10px)';
// ✅ set the base first in the same call, then append
pose(el, { s: pulse(t, 1.0) });
if (t > 2.2) el.style.transform += ` translateY(${-600 * E.in(prog(t, 2.2, 2.4))}px)`;
```

**Counters and state changes** are just functions of t: `el.textContent = t >= 6.25 ? 3 : 2`. For a roll effect, stack both numbers and translate: `translateY(-36 * E.back(prog(t, a, a + .35)))`.

**Typing:** `text.slice(0, Math.floor(prog(t, a, a + 1.1) * text.length))`, plus a blinking caret `Math.floor(t * 2) % 2`.
