# 10. ElevenLabs credit budget

## Where we are (26 Nov 2026)

- Plan: **Creator**, **122,457 credits per month**, next reset **25 Dec 2026**.
- Used so far this period: **~57,200** (47%). That covered the pilot, four versions of "Everyone Vanished", voice tests, music and images. About **10,800 credits went on tagged v4 voice takes the owner rejected**, and several thousand on voice/host/style experiments that are now finished.

## What one episode costs (measured on "Everyone Vanished Except You")

| Item | How it's charged | Ep. cost |
|---|---|---|
| Narration, Eric on eleven_v4 | ~1 credit per character | 8,809 characters ≈ **8,800** |
| Voice tests (2 short lines) | 1 credit/char | ~300 |
| Music, 12 new cues (eleven_music_v2_5) | ~15 credits per second of music | ~640 s ≈ **9,600-10,000** |
| Painted backgrounds (optional) | ~190 per image | 3-6 images ≈ 600-1,150 |
| Shorts/Parts, thumbnails, SFX, captions | reuse existing audio, code-drawn, CC0, local whisper | **0** |

**Estimate per new episode, done once and cleanly:**

- **Full fresh score:** about **19,000-20,000 credits** → only ~6 episodes per month on the current plan.
- **Lean (reuse a music library, ~3 new cues):** about **9,000-12,000 credits** → 10-13 episodes per month, enough for the 2-per-week goal (~9/month) with room for tests.

Before the music library exists, building it once costs about 10 moods × 50 s × 15 = **~7,500 credits**, then it's reused.

## Rules to save credits

1. **Lock the script before any voice generation.** The owner approves the text first. No "let's hear it and then edit".
2. **Test on short lines only** (1-2 lines, under 300 characters) for pronunciation or a new setting. Never test by voicing a whole section.
3. **Plain text, no audio tags.** Tagged takes were rejected and cost ~10,800 credits for nothing.
4. **Voice once, in section-sized takes.** Fix a single bad word by re-voicing that sentence only, then splice it in, not the whole take.
5. **Draft with a free voice** (Kokoro/Chatterbox) for timing and the draft render.
6. **One generation per music cue.** Don't re-roll for small taste differences; adjust in the mix instead.
7. **Reuse music cues** across episodes (mood library). Only generate moods we don't have.
8. **Shorts and Parts never need new audio.** They're cut from the long video's mix.
9. **Code-drawn visuals and CC0 SFX cost nothing.** Avoid ElevenLabs SFX and image generation unless a sound or picture can't be made otherwise; reuse painted backgrounds with camera moves.
10. **Check usage before and after** each generation batch (ElevenLabs `account_get_usage`) and log it in the episode notes. Stop and ask the owner if one episode goes over **20,000**.
11. Never run more than one take per call (`generations_count` default), never retry a generation by calling it again blindly; it charges twice.

## Cheaper voice options (to test, not adopted)

- ElevenLabs **Flash/Turbo** are listed at ~0.5 credit/char on paid plans (our connector billed 1/char in tests, so verify with a short line and the usage counter). Less emotion than v4.
- **Chatterbox** (free, open source) for drafts, possibly finals if a blind test passes.
- Google Chirp 3 HD, Inworld, Cartesia: need accounts; compare in a blind A/B with the owner.
