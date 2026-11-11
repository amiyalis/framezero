# 09 · QA checklist (run before every full render)

<!-- Copyright 2026 Matheus Patricio Pessoa Santana — framezero (MIT) -->

Render stills at: `0`, one moment inside **every** scene, every **transition midpoint**, every **max zoom**, every **label**, and the **last 0.4 s**. Paste them into a contact sheet and go down the list.

### Story
- [ ] Frame 0 has the full hook and the product, and could be the cover
- [ ] Context ("N things…") appears by ~3 s
- [ ] Something changes every 2–4 s
- [ ] The CTA is true today (coming soon vs. download)
- [ ] No invented stats, reviews or features

### Layout
- [ ] All important text is inside x 80–940, y 220–1480
- [ ] No word wraps or gets cut (check the longest word at the biggest size)
- [ ] Labels point at the right detail and don't cover it
- [ ] Zooms are centered and nothing is cropped at the edges at max zoom
- [ ] No layer is hidden behind a background (z-index)
- [ ] No empty or flat-color frames mid-transition

### Motion
- [ ] Labels stay settled ≥ 0.8 s; ≈ 0.3 s per word of reading time
- [ ] Exits are faster than entrances
- [ ] The loop is seamless: the last frame flows into frame 0
- [ ] No `PAGE ERROR` in the render log

### Sound
- [ ] Every cut, slam, label, tap and reward has a sound at the same t
- [ ] Whooshes lead the cuts by ~0.1 s
- [ ] ≈ −13 LUFS integrated, peak ≤ 0.7–0.9
- [ ] The drums stop cleanly at the loop point

### Output
- [ ] Check 6–8 frames sampled from the **final MP4**
- [ ] 1080p upload file made from the 4K master, H.264 High, BT.709, AAC, faststart
- [ ] A caption with a question and ≤ 5 hashtags is ready
