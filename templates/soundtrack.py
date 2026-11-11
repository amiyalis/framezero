# Copyright 2026 Matheus Patricio Pessoa Santana — framezero (MIT)
"""
Soundtrack for templates/starter.html — calm lo-fi bed + sound effects synced to the scene.
Every time below is copied from the scene's seek(t). If you move an animation, move its sound.

    python3 templates/soundtrack.py templates/soundtrack.wav
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / 'kit'))
from sound import *  # noqa: E402,F403

DUR = 12.6
music, beat, fx = Mix(DUR), Mix(DUR), Mix(DUR)

# ---------------- music: lo-fi bed (rhodes chords + sub + swung half-time beat + vinyl) ----------------
lofi_keys(music, 0.0, DUR)
lofi_beat(beat, 0.0, 12.2)                       # drums stop when the loop wipe starts → clean loop point
music.add(vinyl(DUR), 0.0, 1.0)
for i, (dt, n) in enumerate([(0.0, 7), (0.5, 10), (1.0, 14), (1.75, 12)] * 3):   # a tiny bell motif every 4 s
    music.add(bell(note(n)), dt + 4.0 * (i // 4), 0.9, pan=(-0.25 if (i // 4) % 2 else 0.25))
music.duck([k * 2.0 + off for k in range(7) for off in (0.0, 0.805)], depth=0.28)   # sidechain feel on the kicks

# ---------------- effects: HOOK 0 → 2.4 ----------------
fx.add(impact(1.1, .9), 0.0)                     # frame 0 — the hook lands with a hit
fx.add(pop(620, .12), 0.5, 0.6)                  # POV pulse + first badge
fx.add(impact(.9, .8), 1.0)                      # PLANS / YOUR DAY pulse + shake
fx.add(pop(900, .14), 1.5, 0.7); fx.add(ding(1318.5, .8), 1.52, 0.5)   # "and it's free"
for k, a in enumerate([.5, .75, 1.0]):           # badges popping out of the phone
    fx.add(pop(1000 + k * 140, .1), a + .02, 0.55, pan=(-0.4 if k % 2 == 0 else 0.4))
fx.add(whoosh(.3, True, 1.0), 2.15)              # hook flies up and out

# ---------------- effects: FEATURES ----------------
FEATS = [(2.4, 0.95, 1.05), (5.0, 0.85, 1.55), (7.6, 0.85, 1.5)]   # (start, camera zoom-in, label) relative times
for S, zoom, label in FEATS:
    fx.add(whoosh(.3, True, .8), S - .1)         # diagonal wipe
    fx.add(impact(.9, .7), S)                    # number badge slam
    fx.add(pop(780, .12), S + .05, 0.7)
    for j in range(3): fx.add(click(.02), S + .12 + j * .06, 0.4)   # title words
    fx.add(whoosh(.4, False, .6), S + .02)       # phone swings in
    fx.add(whoosh(.45, True, .35), S + zoom - .45)                  # camera pushes in
    fx.add(pop(1040, .12), S + label, 0.65); fx.add(click(.02), S + label + .02, 0.4)   # label pops
T2, T3 = 5.0, 7.6
fx.add(click(), T2 + 1.05, 0.9)                  # finger tap
fx.add(pop(1200, .1), T2 + 1.25, 0.7)            # checkbox fills
fx.add(coin(), T2 + 1.35, 0.75)                  # +20 XP
fx.add(pop(700, .12), T3 + 1.2, 0.6); fx.add(ding(1760.0, .8), T3 + 1.25, 0.55)   # streak rolls 6 → 7

# ---------------- effects: CTA 10.2 → 12.6 ----------------
fx.add(whoosh(.3, True, .9), 10.1)
fx.add(impact(1.4, 1.1), 10.25); fx.add(impact(1.0, .8), 10.6)   # 100% / FREE slams
fx.add(pop(900, .16), 11.0, 0.8); fx.add(ding(1567.98, 1.2), 11.02, 0.9)   # COMING SOON pill
fx.add(pop(1040, .12), 11.35, 0.6); fx.add(pop(820, .12), 11.6, 0.5)
fx.add(whoosh(.45, True, .9), 12.1)              # loop wipe back to the hook

y = Mix.blend([(music, 1.0), (beat, 0.85), (fx, 0.9)], DUR).master(DUR, 0.70)
out = sys.argv[1] if len(sys.argv) > 1 else str(pathlib.Path(__file__).with_name('soundtrack.wav'))
Mix.save(y, out)
print('soundtrack', out, f'{DUR}s')
