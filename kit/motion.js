/* Copyright 2026 Matheus Patricio Pessoa Santana — framezero (MIT)
 * motion.js — tiny helpers for DETERMINISTIC animation: every value is a pure function of t.
 * Injected at <!--BASE-->. No timers, no requestAnimationFrame, no CSS transitions: seek(t) must
 * always draw the same picture for the same t, so frames can be rendered in any order.
 */

/* ---------- math ---------- */
const clamp = (x, a = 0, b = 1) => Math.min(b, Math.max(a, x));
/** 0 before a, 1 after b, linear in between — the building block of everything. */
const prog = (t, a, b) => clamp((t - a) / (b - a));
const lerp = (a, b, p) => a + (b - a) * p;

/* ---------- easings (x in 0..1) ---------- */
const E = {
  lin: x => x,
  out: x => 1 - Math.pow(1 - x, 3),        // default for entrances
  out5: x => 1 - Math.pow(1 - x, 5),       // snappy entrances, wipes
  inOut: x => (x < .5 ? 4 * x * x * x : 1 - Math.pow(-2 * x + 2, 3) / 2),  // camera moves
  in: x => x * x * x,                       // exits
  back: x => { const c1 = 1.9, c3 = c1 + 1; return 1 + c3 * Math.pow(x - 1, 3) + c1 * Math.pow(x - 1, 2); },  // overshoot pop
  expo: x => (x === 1 ? 1 : 1 - Math.pow(2, -10 * x)),  // slams
};

/* ---------- DOM ---------- */
const $ = s => document.querySelector(s);
const $$ = s => [...document.querySelectorAll(s)];

/** Set opacity + transform in one call. Elements should be position:absolute. */
function pose(el, { o = 1, x = 0, y = 0, s = 1, r = 0, sx, sy } = {}) {
  if (!el) return;
  el.style.opacity = o;
  el.style.transform = `translate(${x}px,${y}px) rotate(${r}deg) scale(${sx ?? s},${sy ?? s})`;
}

/** Presence 0..1: enters during a→a+d, leaves during b→b+d2. */
function presence(t, a, d, b, d2, ease = E.out, easeOut = E.in) {
  if (t < b) return ease(prog(t, a, a + d));
  return 1 - easeOut(prog(t, b, b + d2));
}
const janela = presence; // legacy name used by older scenes

/* ---------- scene building blocks ---------- */
/** Show/hide a whole scene layer. */
const show = (sel, on, z = 1) => { const e = typeof sel === 'string' ? $(sel) : sel; e.style.opacity = on ? 1 : 0; e.style.zIndex = z; };
/** Word SLAMS in from big to normal size (impact). Pair it with an impact sound at the same t. */
const slam = (el, t, a, from = 2.0, r = 0) => { const p = E.expo(prog(t, a, a + .3)); pose(el, { s: lerp(from, 1, p), r, o: t < a ? 0 : Math.min(1, prog(t, a, a + .05)) }); };
/** Text rises 30px while fading in (subtitles, small lines). */
const rise = (el, t, a, d = .3, dy = 30) => { const q = E.out(prog(t, a, a + d)); pose(el, { o: q, y: lerp(dy, 0, q) }); };
/** Multiplier that bumps to 1+amp and back during a→a+d (beat accents). */
const pulse = (t, a, amp = .14, d = .28) => (t >= a && t < a + d ? 1 + amp * Math.sin(prog(t, a, a + d) * Math.PI) : 1);
/** Horizontal shake offset in px, decaying over d (use on impacts). */
const shake = (t, a, d = .3, amp = 14) => (t > a && t < a + d ? Math.sin(t * 95) * amp * (1 - prog(t, a, a + d)) : 0);
/** Scene transition: reveal from the bottom up. */
const wipeUp = (el, t, a, d = .24) => { el.style.clipPath = `inset(${lerp(100, 0, E.out5(prog(t, a, a + d)))}% 0 0 0)`; };
/** Scene transition: diagonal reveal from the left. */
const wipeDiagonal = (el, t, a, d = .3) => { const p = E.out5(prog(t, a, a + d)) * 160; el.style.clipPath = `polygon(0 0, ${p}% 0, ${p - 60}% 100%, 0 100%)`; };
/** Endless background drift for a dot-grid layer (period 46px keeps it seamless). */
const drift = (el, t, vx = 18, vy = 30, period = 46) => { el.style.transform = `translate(${(t * vx) % period}px, ${(t * vy) % period}px)`; };

/** Wrap each character of el in <span class="l"> once, so letters() can animate them. */
function splitLetters(el) { el.innerHTML = [...el.textContent].map(c => c === ' ' ? ' ' : `<span class="l" style="display:inline-block">${c}</span>`).join(''); }
/** Letters drop in one by one with a little rotation. Call splitLetters(el) once at setup. */
function letters(el, t, a, { step = .03, d = .32, dy = -120, rot = 14 } = {}) {
  [...el.querySelectorAll('.l')].forEach((s, i) => { const p = prog(t, a + i * step, a + i * step + d);
    pose(s, { y: lerp(dy, 0, E.back(p)), r: lerp(i % 2 ? rot : -rot, 0, E.out(p)), o: p > 0 ? Math.min(1, p * 4) : 0 }); });
}

/* ---------- phone camera ----------
 * The app UI is drawn at its real size (e.g. 390x844 CSS px) inside a phone, scaled by k.
 * makeCamera() returns helpers that move a "camera" so that a point of the APP lands on a point of the VIDEO.
 *   const C = makeCamera({ k: 1.559, x: 220, y: 560, bezel: 16 });
 *   const shot = C.at(195, 440, 1.5, 540, 1010);   // app point (195,440) → video (540,1010), zoom 1.5
 *   C.apply($('#cam'), C.track(keys, localT));     // keys = [[time, shot], ...]
 */
function makeCamera({ k, x, y, bezel = 16 }) {
  const FULLSHOT = { tx: 0, ty: 0, s: 1 };
  const at = (ux, uy, s, X, Y) => ({ tx: X - x - s * (bezel + ux * k), ty: Y - y - s * (bezel + uy * k), s });
  const track = (keys, r) => {
    if (r <= keys[0][0]) return keys[0][1];
    for (let i = 1; i < keys.length; i++) if (r < keys[i][0]) {
      const p = E.inOut(prog(r, keys[i - 1][0], keys[i][0])), A = keys[i - 1][1], B = keys[i][1];
      return { tx: lerp(A.tx, B.tx, p), ty: lerp(A.ty, B.ty, p), s: lerp(A.s, B.s, p) };
    }
    return keys[keys.length - 1][1];
  };
  /** Where an app point currently is on the video (use it to place labels). */
  const onScreen = (shot, ux, uy) => [x + shot.tx + shot.s * (bezel + ux * k), y + shot.ty + shot.s * (bezel + uy * k)];
  const apply = (el, shot) => { el.style.transform = `translate(${shot.tx}px,${shot.ty}px) scale(${shot.s})`; };
  return { FULL: FULLSHOT, at, track, onScreen, apply };
}
