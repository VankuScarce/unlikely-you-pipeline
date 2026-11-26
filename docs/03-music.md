# 3. Music

## The rule

**Music must be clearly audible and change mood with each story section.** In earlier versions the music sat ~18 dB under the voice and the owner could not hear it. Generic procedural/synth beds ("AI sound") are not allowed.

## How "Everyone Vanished" was scored (current standard)

- **One instrumental cue per story section**, made with ElevenLabs **Eleven Music** (`eleven_music_v2_5`), **one generation per cue** (no re-rolls unless a cue is clearly broken).
- 12 cues for a 10:39 video. Cue list with moods: `episodes/everyone_vanished/music_cues.txt` (tense drone, curious mechanical pulse, dark then awe, suspense, warm relief, playful, ominous, bittersweet, lonely piano, hopeful nature, building determined, wistful open).
- Prompt pattern: section mood + instruments + tempo + "instrumental, no vocals, cinematic underscore for narration, leaves room for a voice". Ask for the cue length you need (section length + 2-3 s).
- Each cue is normalised to **-23 LUFS**, laid on the timeline with fades and short overlaps by `code/everyone_vanished/tools/score.py SECTIONS.json CUE_DIR OUT.wav TOTAL_SECONDS` (`sections.json` = section start/end seconds from the timeline).
- Mix: music **+3 dB** relative to the stem, **gentle ducking** under the voice (sidechain threshold 0.16, ratio 2, attack 60 ms, release 650 ms). Result: music sits about **10-14 dB under the voice during speech** and comes up in pauses. Check it with `tools/speechgap.py VO.wav MUSIC_DUCKED.wav sections.json`.
- Big moments: let music swell or **drop to silence** right before a reveal line. The reference reels both use a drop-out at key beats.

## Saving credits on music

Eleven Music costs about **15 credits per second** (a 12-cue, 10-minute score was ~10,000 credits). See [10-elevenlabs-credit-budget.md](10-elevenlabs-credit-budget.md). Plan:

- Build a **reusable cue library** by mood (tense, mystery, awe, warm, playful, ominous, lonely, hopeful, determined, wistful). Generate 45-60 s per cue once, then reuse and loop them across episodes.
- Only generate new cues for moods the library doesn't have.
- Consider a short **channel signature** sting/bed used in every episode (the reference reels use one constant bed).

## Licensing

- Eleven Music on a paid plan: no attribution line needed. Check ElevenLabs' current terms for commercial YouTube use before monetising.
- Earlier versions used CC BY tracks from Jamendo. CC BY music can still get Content ID claims; YouTube Audio Library is the safer free source if we ever go back to stock music.
