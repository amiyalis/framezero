# 05 · Sound: code-generated, copyright-free, frame-synced

<!-- Copyright 2026 Matheus Patricio Pessoa Santana — framezero (MIT) -->

Silent promos feel cheap even to people who watch muted, because when they *do* unmute it's dead air. `kit/sound.py` builds music and effects from math (numpy + scipy), so there's nothing to license and nothing to get muted.

## Structure of a soundtrack script

```python
from sound import *
DUR = 12.6
music, beat, fx = Mix(DUR), Mix(DUR), Mix(DUR)       # three buses

lofi_keys(music, 0, DUR); lofi_beat(beat, 0, 12.2); music.add(vinyl(DUR), 0)   # the bed
fx.add(impact(), 0.0)                                # effects at the SAME seconds as the scene
fx.add(whoosh(.3), 2.3)                              # 0.1 s before the 2.4 s wipe
...
y = Mix.blend([(music, 1.0), (beat, 0.85), (fx, 0.9)], DUR).master(DUR, 0.70)
Mix.save(y, 'soundtrack.wav')
```

## Sync map (visual → sound)

| On screen | Sound | Offset |
|---|---|---|
| Scene wipe / cut | `whoosh(.3, True)` | **−0.1 s** (the sound leads) |
| Word slam, number badge | `impact(.9–1.4)` | 0 |
| Label, badge, chip | `pop(1040, .12)` + `click(.02)` | 0 |
| Title words appearing | 3× `click(.02)` spaced 0.06 s | 0 |
| Tap / button | `click()` | 0 |
| Correct / reward / XP | `ding()` / `coin()` | +0.1 s after the visual |
| Wrong answer | a short detuned saw buzz (see `examples/estuda-tour/soundtrack.py → erro`) | 0 |
| Big reveal | `riser(.8)` then `impact(1.6)` | riser ends on the reveal |
| Typing | `click(.018)` per character, with varying gain and pan | per char |
| Camera push-in | soft `whoosh(.45, True, .35)` | starts with the move |
| Loop wipe | `whoosh(.45)` | −0.1 s |

**Tip:** keep a table of beat start times in the soundtrack (`FEATS = [(2.4, zoom, label), …]`) and generate effects in a loop. When you retime the scene, you change one table.

## Music recipes

**Lo-fi (default, calm):** Rhodes chords Em9 – Cmaj9 – Am9 – Bm7, 2 s each, with a sub bass under the root. Half-time swung drums (kick on 1 and the "and" of 2, snare on 3, a ghost note, soft hats), vinyl crackle, and a small bell motif every 4 s. Already packaged as `lofi_keys()` + `lofi_beat()` + `vinyl()` + `bell()`.

**Energetic (120 BPM):** `kick()` on every beat (0.5 s), `clap()` on 2 and 4, `hat()` 8ths, a `bass()` line, and `pad()` chords. Good for hype launches. Too aggressive for study or calm products: our first energetic track was called "kinda bad" by its target audience, and the lo-fi version fixed it.

**Sidechain feel:** `music.duck(kick_times, depth=.28)` dips the music on each kick, so effects and kicks punch through without raising the volume.

**Drops and pauses:** stop the drums for the payoff build ("and the BEST is…"), play a `riser`, then bring everything back on the reveal.

**Clean loop:** stop the drums ~0.4 s before the end so the loop seam isn't a cut-off beat.

## Loudness

`.master(dur, 0.70)` soft-saturates and normalizes the peak to 0.70. For these mixes that lands around **−13 LUFS integrated**, which suits TikTok and Reels. Verify:

```bash
FF=$(python3 -c "import imageio_ffmpeg;print(imageio_ffmpeg.get_ffmpeg_exe())")
$FF -i soundtrack.wav -af ebur128 -f null - 2>&1 | grep -A3 Summary
```

## Changing only the audio

You don't need to re-render frames:
```bash
$FF -i video.mp4 -i new.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 320k -shortest -movflags +faststart video-new.mp4
```
