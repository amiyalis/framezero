# 08 · Case study: the estuda+ series

<!-- Copyright 2026 Matheus Patricio Pessoa Santana — framezero (MIT) -->

**estuda+** is a free study app for Brazilian students: a daily plan, a daily challenge, free classic books, weekly leagues and an AI tutor. Before launch it had zero marketing budget, so we made the videos with code. Here's what happened, honestly.

## Timeline

| # | Video | Length | What changed | Result / feedback |
|---|---|---|---|---|
| 1 | **Presentation v1** | 19 s | First try: hook "ENEM in 30 days?", energetic 120 BPM track | Hook too narrow. The app is for middle school too, not only the ENEM exam |
| 2 | **Presentation v2** | 25 s | Hook for everyone ("Test tomorrow?" → "studying alone?" → "NEVER AGAIN."), more seconds, CTA changed from "LINK IN BIO" to "COMING SOON" | Early posts: a Reel with 2 likes, a TikTok with ~60 views and 0 likes |
| 3 | **#1 AI Tutor** | 25 s | One feature, one pain: "Stuck on homework?" → clock 23:46→23:47 → "CALL THE TUTOR". The chat is drawn in HTML so it's sharp at 4K | Clearer story |
| 4 | **#2 Daily Challenge** (quiz) | 33.5 s | "More engaging" was the brief. Quiz format: "Bet you can't get all 3", 5 s timer each, the last one is unanswered, CTA "comment your answer" | Built for comments. The music was called "kinda bad", so we switched to **lo-fi**, kept the same effects, and swapped only the audio (`-c:v copy`) |
| 5 | **#4 App Tour** | 39 s | "Better than the previous ones, and talk about the app": POV hook, "5 things it does / the last is the best", Stories-style progress bar, real screens with a camera and labels, lo-fi | Then the owner asked for more motion in the hook. We added screen-cycling on the beat, badges, 3D sway and a fly-out |

By video 5 the TikTok account's latest post had passed 200 views. These are small numbers, but the direction was clear: **specific hooks + real UI + a question CTA** beat generic slogans.

## Lessons

1. **The audience decides the hook.** "ENEM" excluded 2/3 of the users. Broad pain ("test tomorrow?") and POV hooks worked for everyone.
2. **Never promise what doesn't exist.** "Link in bio" before launch became "Coming soon · follow to know when it launches", which also gains followers.
3. **Quizzes earn comments.** People love proving they know the answer. Leave the last question unanswered.
4. **Music must match the product's mood.** Energetic EDM felt wrong for a study app, and lo-fi fixed it instantly.
5. **"More seconds" ≠ slower.** We added beats, not padding.
6. **Animate the hook harder than anything else.** The first 2.5 s carry the video, so give the phone life: swipes on the beat, badges, hops.
7. **Draw the screens where something happens.** Drawn HTML chats and quiz sheets can type, tap and react, while screenshots can't.
8. **QA with contact sheets catches real bugs.** That's how we caught a giant word wrapping ("MELHO/R" at 300 px), labels cropped by off-center zooms, and a background layer covering the phone.

## Visual identity

- Brand: forest `#2F5D4C`, gold `#C8A24B`, ink `#16281F`, Inter font. The app itself is light-only and serious, with no emoji in the UI.
- Video palette ("vivid"): dark green radial `#0F6141 → #073323 → #021309`, gold text `#FFC233`, and one saturated background per beat (emerald, violet, blue, coral). The videos shout. The app stays calm.

## Files

The real tour is in [`examples/estuda-tour`](../examples/estuda-tour) (on-screen text in Portuguese).
