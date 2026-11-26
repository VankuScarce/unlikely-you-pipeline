# 4. Sound effects and the final mix

## The rule

Use **real recorded sounds**, placed **frame-exactly** on the action, plus a quiet **ambience bed** for every scene. The owner finds typical "AI video" sound design annoying and recognisable: synthesized beeps, white-noise whooshes, the same pop on every word. **Do not generate SFX with numpy/sine waves** (the old `audio()` function in `ep02.py` did this; it is only a fallback).

See [11-upgrade-goals.md](11-upgrade-goals.md): the owner wants **better quality and better-chosen** effects next time. Treat this doc as the baseline, not the ceiling.

## Sources (free, no attribution needed where marked)

| Source | Licence | Notes |
|--------|---------|-------|
| Freesound.org (filter **CC0**) | CC0 | Biggest library. Read ratings and listen; many uploads are low quality. API needs a free key. |
| Openverse API (`api.openverse.org`, `license=cc0`) | CC0 | Search front-end mostly over Freesound. `code/sfx/fetch.py` uses it, no key needed. |
| Pixabay Sound Effects | Pixabay licence (free, no credit) | Often cleaner, more "produced" effects. |
| Sonniss GDC Game Audio Bundles | Royalty-free, commercial OK | Professional quality, tens of GB. Best for impacts, whooshes, ambiences. Download on the owner's PC. |
| YouTube Audio Library | Free for YouTube | Safe on YouTube, decent ambiences. |
| BBC Sound Effects | RemArc licence (personal/educational only) | **Do not use** for a monetised channel. |

ElevenLabs Sound Effects (text-to-SFX) also exists; it costs credits and can sound synthetic. Only use it for a sound you cannot find, and listen before keeping it.

## Building the library

`python3 code/sfx/fetch.py OUTDIR` downloads up to 4 CC0 variants per tag (whoosh, impact, wind, room_tone, dog_bark, door_creak, ...) into `OUTDIR` and writes `library.json` (file, title, creator, licence, source page). Add tags to the `Q` dict for a new episode's needs. Keep `library.json` so every sound can be traced back to its licence.

**Quality filter before using a sound** (this was too loose before):
- At least 44.1 kHz, no clipping, no background hiss or hum unless it's meant to be there.
- Trim leading silence, short fade-out (the loader does this).
- Listen to every candidate. Prefer sounds with a clear transient for hits, and long seamless recordings (2+ min) for ambiences.
- Pick variants so the same sound doesn't repeat audibly in one minute.

## Placing sounds

`code/everyone_vanished/sound_design.py VO_DIR LIB_DIR OUT_DIR` writes `sfx.wav`:
- `AMB` maps each **scene** to ambience tags and gains (e.g. `bedroom: room_tone -30 dB, birds_morning -34 dB`). Beds are looped with crossfades over the whole shot.
- Spot effects are added at exact times relative to each shot's VO (`at`, `gain_db`, `align_peak=True` puts the loudest moment of the sound on the action frame).
- Transitions get a real whoosh; section cards get an impact.

## Final mix recipe (gives -14 LUFS, true peak about -2.5 dB)

1. VO lines normalised to -22 LUFS (`tools/normvo.py`).
2. Stems: `vo.wav` (from `ep02.py audio`), `sfx.wav` (sound_design.py), `score.wav` (score.py).
3. `tools/mix5.sh MUSIC_GAIN_DB OUTDIR`: VO +8.1 dB, SFX +12.4 dB with light ducking under the voice, music +3 dB with gentle ducking, `amix` without normalising, `alimiter 0.95`, mono to stereo at -3 dB, 48 kHz.
4. Check loudness: about **-14 LUFS integrated**, true peak under -1 dB.
5. Mux with the video. **Always encode AAC with `-aac_coder fast`**: ffmpeg's default AAC coder produced +5-10 dB peak spikes (audible clicks) in our files. Example:

```
ffmpeg -i video.mp4 -i mix_st.wav -map 0:v -map 1:a -c:v copy -c:a aac -aac_coder fast -b:a 192k -shortest final.mp4
```

Edit the hard-coded stem paths at the top of `mix5.sh` for your machine.
