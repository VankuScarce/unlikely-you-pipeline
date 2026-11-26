# 11. Upgrade goals for the next episode

The owner reviewed "Everyone Vanished Except You" and asked for two upgrades. **The next episode must clearly improve on both**, without changing the visual style.

## Goal 1: better sound effects, in quality and in choice

What was wrong: many SFX came from a quick automatic Openverse fetch (first 4 CC0 hits per tag), so some were thin, noisy, or not quite the right sound for the action, and the same few sounds repeated.

What to do:
- **Curate, don't auto-pick.** For every important sound, listen to 5-10 candidates and pick the best. Prefer Sonniss GDC bundles and Pixabay for hits, whooshes and ambiences; use Freesound CC0 for specific real-world sounds (a particular door, a dog, a car).
- **Quality bar:** 44.1/48 kHz, clean, no clipping or hiss, recorded rather than synthesized. Reject anything that sounds like a cheap stock beep.
- **Layer key moments:** a big reveal = low impact + texture (debris, glass, cloth) + a short tail, not one generic "boom".
- **Match the picture exactly:** every visible action that would make a sound gets one (car door, footsteps, paper, switches, animals), placed on the frame with `align_peak`.
- **Richer ambience:** each location gets a proper bed (room tone, distant wind, birds, electrical hum, rain) that changes when the location changes. Silence the bed at dramatic beats.
- **Variety:** at least 2-3 variants for repeated sounds (footsteps, whooshes), never the same file twice within ~30 s.
- **Fewer, better transition whooshes.** Not every cut needs one; use real air/cloth swishes, quieter than before.
- Keep a `library.json` with source and licence for every sound used.

## Goal 2: more interesting, dynamic visuals with more detail (same style)

Keep: flat paper cut-out look, palette, camera moves, transitions, kinetic type, the chosen character style.

Add:
- **More detail in every scene:** foreground/midground/background layers with parallax, small props (signs, litter, plants, windows with curtains, cables, puddles), texture on surfaces (brick lines, wood grain, stains), and light (window glow, lamp pools, sky gradients, shadows that match the light).
- **Something moving in every shot at all times:** birds, leaves, dust, smoke, flickering lights, blinking LEDs, rain, clouds, water, the character breathing or shifting weight. No frozen frames.
- **More character acting:** "you" should walk, reach, react, turn the head, sit, carry things. Use the shared rig poses and add a few new ones per episode.
- **More shot variety:** wide establishing shots, close-ups on hands and objects, over-the-shoulder, top-down maps, inserts of screens/notes. Alternate shot scale every 1-2 shots.
- **Camera with purpose:** slow push for tension, quick snap-zoom on a reveal, track along with a walking character, rack between layers.
- **Diagram cards** for facts (clean white cards with a simple chart or icon, like the Absolute Zero reel) instead of floating text alone.
- **Text:** fewer words on screen, only the key word or number, varied placement, sentence case.
- **Review rule:** before the final render, look at `shotstills` and the 10 s preview of every section. If a frame would look boring as a paused screenshot, add detail or motion.

## How to check you met the goals

- Show the owner a 30-60 s **before/after** clip (same section in the old and new treatment) before rendering the whole episode.
- Watch retention in YouTube Studio after release: look for drops at static or fact-heavy stretches and note them in [13-history-and-lessons.md](13-history-and-lessons.md).
