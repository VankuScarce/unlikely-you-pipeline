# 9. New episode: step by step

Owner checkpoints are marked **[OWNER]**. Everything else should run without them. Credit-spending steps are marked **[CREDITS]**.

## A. Topic and story (no credits)

1. **[OWNER] Agree the topic.** Pitch 3 premises in one line each: personal "you" situation, the hook device (clock/number/rule), the small setting, the hidden twist, and which of the six character styles fits ([05](05-visual-style.md)).
2. **Outline** the sections with in-story clock values (HOUR 4 / DAY 2 / MONTH 1 ...), the twist position (~1/3), the peak (~70-75%), the open ending, and the **five Part cut points** (each a cliffhanger).
3. **Research facts.** Every fact gets a source link and a `FACT`/`GUESS` label. Each fact must change a decision "you" make.
4. **Write the script** with `templates/script_template.md`: ~1,550-1,650 words, second person, short sentences, spoken style. Hook in the first 12-15 s. No twist in the opening.
5. **[OWNER] Approve the script.** After this point the text is locked. Changing a voiced line costs credits.

## B. Draft render (no credits)

6. Write `shots.py` (one row per narration line, with scene names and section cards) and new `sc_` scene functions. Reuse props/character/camera code.
7. Generate a **free scratch voice** (`scratch_vo.py`, Kokoro or Chatterbox) into `vo_scratch/`.
8. `ep02.py plan vo_scratch` to check the total length (target 9:30-11:00). Adjust the script now if it's short or long.
9. `ep02.py shotstills` and review every still. Fix dull or empty frames (see [11-upgrade-goals.md](11-upgrade-goals.md)).
10. Optional: render a low-res draft with the scratch voice for the owner.

## C. Audio (credits)

11. **[CREDITS] Test 2 short lines** with Eric on eleven_v4 (names, numbers). Max ~300 characters.
12. **[CREDITS] Voice the locked script once**, in ~14 section-sized takes, plain text ([02](02-voice.md)). Don't regenerate a take for small things; only for a real mistake (wrong word, glitch).
13. Split (`split_v4.py`), normalise (`normvo.py`), word timestamps (`words.py`).
14. **[CREDITS] Music:** reuse library cues first; generate only missing moods, one generation each ([03](03-music.md)). Lay them with `score.py`.
15. **SFX:** extend the `fetch.py` tag list, listen and pick, place them in a `sound_design.py` for this episode ([04](04-sound-effects.md)).
16. Mix with `mix5.sh`; check -14 LUFS and the speech/music gap.

## D. Final render and packaging (no credits)

17. Render the video in parallel chunks, concatenate, mux the mix with `-aac_coder fast`.
18. Watch the whole thing once at 1x. Check sync, levels, and any frozen or empty shots.
19. `parts.py` for the 5-part series (16:9, 9:16 with captions, covers).
20. Three thumbnails (`branding/thumbs_v2*.py` adapted), title, description with chapters and sources (`metadata.py` pattern).

## E. Publish

21. Upload via n8n (chunk upload for the long video, review workflow for the parts) as **private** ([08](08-upload-and-approval.md)).
22. **[OWNER] Telegram:** pick the thumbnail, tap Publish or Hold.
23. Cross-post parts to Instagram/TikTok.
24. After 48 h and 7 days: note views, average view duration, retention dips, and comments asking for more. Write what to change into `docs/13-history-and-lessons.md`.

## Typical time and cost

- Owner time: about 1-2 h per episode (topic, script approval, final watch, Telegram taps).
- ElevenLabs: about 9,000-19,000 credits per episode depending on music reuse ([10](10-elevenlabs-credit-budget.md)).
