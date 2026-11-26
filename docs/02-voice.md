# 2. Narrator voice

## The standard

- **Voice:** ElevenLabs **"Eric"**, voice id `GllazL0Pu8NnMBPkxbGQ`.
- **Model:** `eleven_v4`.
- **Text:** **plain text, no audio tags.** No `[whispers]`, `[nervous]`, `[pause]`, `[dramatically]` etc. The owner tried a heavily tagged version and called it "way too much". Plain v4 text gives the right amount of emotion (the level of the pilot).
- Write numbers the way they should be spoken when the model might misread them ("seven-oh-two" rather than "7:02" if a test line reads it wrong).

## How the VO is generated (do it once)

1. **Lock the script first.** No voice generation until the owner has approved the script text. Every re-take costs credits.
2. **Test on 1-2 short lines** (one calm, one tense) before voicing anything long. Check pronunciation of names, numbers and odd words.
3. **Voice in section groups**, not line by line: about 14 takes of 400-900 characters each (one per story section). Longer takes keep a consistent tone and cost the same per character. `code/everyone_vanished/tools/vo_v4_groups.json` shows how "Everyone Vanished" was grouped (use the `plain` field; the `text` field is the rejected tagged version).
4. **Split each group into per-shot files** with `tools/split_v4.py`: it transcribes the take with faster-whisper (word timestamps), aligns the words to the script lines and cuts `vo/<shot_id>.wav` at the silences between lines.
5. **Normalise every line** with `tools/normvo.py SRC DST`: highpass 70 Hz, level-match to -22 LUFS, light compression, limiter.
6. Run `tools/words.py` to save word timestamps (`words.json`), used later for Shorts captions.

The renderer times every shot from the length of its VO file, so the picture always fits the voice.

## Free placeholder voice for drafts

Before spending credits, render the whole episode with a free local voice to check timing and pacing: `code/everyone_vanished/scratch_vo.py` (Kokoro, `am_michael`). Chatterbox (free, open source) is the better free option and was tested as a possible cheaper tier; samples exist in the owner's project files. Use these for drafts only. The published voice is Eric.

## Cheaper options being considered

The owner asked for a cheaper but still realistic option. Candidates: Chatterbox (free, self-hosted), Google Chirp 3 HD, Inworld, Cartesia. ElevenLabs Flash/Turbo are cheaper per character on paid plans, but the owner wanted more emotion than Flash gives. Do a blind A/B test with the owner before switching anything.
