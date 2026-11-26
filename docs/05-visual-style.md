# 5. Visual style and the renderer

## The look

The owner liked the **"dynamic style test"** (a 27 s test clip from the pilot, `code/pilot/dynamic_test.py`) and every later video follows it:

- **Code-drawn flat 2D "paper cut-out" art** in Python + pycairo. Layered shapes with soft drop shadows, film grain, vignette. No stock footage, no AI video.
- **Palette** (from `code/pilot/style.py`): navy `#14213D`, ink, teal `#1F7A8C`, cream `#F1E9DA`, orange `#F4A259`, hi-vis orange, red `#E63946`, plus grey/slate/sand/sky.
- **Virtual camera on every shot:** slow push-ins, drifts, slight rotation, handheld shake (`push()`, `cam()`, `shake()`).
- **Transitions** cycle through whip-pan left/up with motion blur, flash, spin and zoom-through (`TRANS_CYCLE` in `ep02.py`); zoom always goes into a section card.
- **Kinetic type:** key words pop in on the beat of the narration (`kword`, `bword`, `words_seq`), in sentence case. Avoid ALL CAPS everywhere and identical pop-ins every second (the owner noticed).
- **HUD:** a stopwatch with the in-story clock in the top-left after the cold open; section cards with a big stopwatch.
- 1920x1080, 24 fps, x264 CRF 19.

## Renderer architecture (`code/everyone_vanished/`)

```
shots.py     SHOTS = [(id, card, scene, params, narration), ...]
             card = (stopwatch text, title, subtitle) or None
ep02.py      plan(): each shot lasts lead + VO length + tail (from vo/<id>.wav)
             sc_<scene>(ctx, s): one function per scene; s.lt = local time,
             s.at(f) = time at fraction f of the shot's narration, s.pr(f0,f1) = 0..1 progress
             frame(T): picks the shot, applies the transition, grain, vignette
scenes_v3.py more sc_ functions, exec'd into ep02's namespace
props.py     reusable props (stopwatch, phone, car, buildings, ...)
character.py you(): the realistic adult "you" (no hoodie)
```

Commands:

```
python3 ep02.py plan VO_DIR                  # timeline and total length
python3 ep02.py shotstills OUT_DIR VO_DIR     # one still per shot, for review
python3 ep02.py still 123.4 out.png VO_DIR
python3 ep02.py video out.mp4 T0 T1 VO_DIR    # render a range (split into chunks and run in parallel)
python3 ep02.py audio OUT_DIR VO_DIR          # vo.wav on the timeline
```

For a new episode, copy `everyone_vanished/` to a new folder, write a new `shots.py` and new `sc_` scene functions, and reuse the props, character, camera and transition code. Always review `shotstills` before rendering the full video.

## Character: the "you"

Rules: **no hoodie**, more realistic adult proportions, styled like big hand-made animation channels, must not look cheap. Reference sheet: `samples/character_v2_sheet.png`.

### Six alternative styles (pick one per story)

All six share one rig (`code/characters/rig.py`, poses and joints), so any style can drop into any episode. Draw functions in `code/characters/styles.py`, sample scenes in `scenes.py`. Overview: `samples/character_styles_sheet.jpg`. The owner likes all six.

| Style | Look | Best for |
|-------|------|----------|
| A Ink Line | black line figure, mustard beanie + red scarf, on a painted background | survival and physics (Absolute Zero-like) |
| B Silhouette | solid dark figure, rim light, lantern, reflection | mystery, alone, space |
| C Geometric | faceless flat shapes, orange coat, backpack, code-drawn background | science and space what-ifs |
| D Test Dummy | shaded crash-test mannequin on a blueprint grid | body limits, extreme physics |
| E Ink Wash | hooded cloak, brush strokes, red sash, painted background | history, past eras |
| F Graphic Novel | outlined cel-shaded adult, bomber jacket | action, crime, chases |

Painted backgrounds for styles A and E were made with an image model via ElevenLabs (about 190 credits each). Make a small, consistent set per episode (3-6 locations) and reuse them with camera moves, rather than a new image per shot.

## What needs to improve

See [11-upgrade-goals.md](11-upgrade-goals.md): more interesting, dynamic visuals with more detail, same style.
