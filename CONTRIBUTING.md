# Contributing to framezero

<!-- Copyright 2026 Matheus Patricio Pessoa Santana — framezero (MIT) -->

Thanks for helping! Small, focused PRs are the easiest to review.

## Great first contributions
- New **motion helpers** in `kit/motion.js` (they must be pure functions of `t`)
- New **sounds or music recipes** in `kit/sound.py` (code-generated only, no samples)
- New **templates**: other formats (16:9, 1:1), other genres (quiz, countdown, before/after)
- Docs fixes, translations, and testing on macOS or Windows

Check the [good first issues](https://github.com/matheusvibecoder-vibecodas/framezero/labels/good%20first%20issue).

## Rules
1. `seek(t)` stays **deterministic**: no timers, CSS animations, `Date.now()` or unseeded random.
2. No new heavy dependencies (no React, bundlers or GPUs). Plain HTML/JS + Python.
3. Bundled media must be yours or freely licensed. **Don't add copyrighted music or fonts.**
4. Run the smoke test locally before opening a PR:
   ```bash
   python3 kit/render.py templates/starter.html out/s --stills 0,3.5,6.6,10.9
   python3 templates/soundtrack.py out/s.wav
   ```
5. If your change affects visuals, attach a contact sheet (stills side by side) to the PR.

## Show your video
Made something with framezero? Open a **"Show your video"** issue or post in Discussions. We'll add the best ones to the README showcase.
