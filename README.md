# The Unlikely You: video pipeline handbook

This repo explains how we make videos for the YouTube channel **The Unlikely You** (@theunlikelyyou): animated, narrator-only "What If" stories where **you** are the main character. If you are an AI model starting in a new chat, read this page and then the docs in order. You should then be able to take a new topic from idea to finished long video, Shorts series, thumbnail and upload.

> No API keys, tokens or passwords are stored here. Ask the owner for access to ElevenLabs, n8n and YouTube when you need them.

## The channel in one paragraph

Second-person "What If" survival and physics stories ("What if everyone on Earth vanished except you?"), about 10 minutes long, told by one narrator voice (ElevenLabs "Eric"). The visuals are code-drawn 2D animation (Python + pycairo) with a moving virtual camera, fast transitions and kinetic text. Audience: teens and adults, never kids. The goal is views, retention and passive income with as little manual work as possible, while staying clearly original so YouTube's "inauthentic content" rules never hit the channel.

## Read in this order

| # | Doc | What it covers |
|---|-----|----------------|
| 1 | [docs/01-format-and-story.md](docs/01-format-and-story.md) | Format rules, story structure, what the owner likes and dislikes |
| 2 | [docs/02-voice.md](docs/02-voice.md) | Narrator voice, model, settings, how VO is generated and split |
| 3 | [docs/03-music.md](docs/03-music.md) | One Eleven Music cue per story section, mixing levels |
| 4 | [docs/04-sound-effects.md](docs/04-sound-effects.md) | Real CC0 sound sources, placement, the full mix recipe |
| 5 | [docs/05-visual-style.md](docs/05-visual-style.md) | The "dynamic style" look, renderer architecture, six character styles |
| 6 | [docs/06-thumbnails-titles.md](docs/06-thumbnails-titles.md) | Titles, thumbnails, descriptions, never spoil the twist |
| 7 | [docs/07-shorts-and-series.md](docs/07-shorts-and-series.md) | Part 1-5 series cut from each long video |
| 8 | [docs/08-upload-and-approval.md](docs/08-upload-and-approval.md) | n8n upload endpoints, Telegram approval, cross-posting |
| 9 | [docs/09-new-episode-workflow.md](docs/09-new-episode-workflow.md) | **Step-by-step checklist for a new topic** |
| 10 | [docs/10-elevenlabs-credit-budget.md](docs/10-elevenlabs-credit-budget.md) | Credit costs per episode and rules to save credits |
| 11 | [docs/11-upgrade-goals.md](docs/11-upgrade-goals.md) | **What must be better next time** (sound effects, visuals) |
| 12 | [docs/12-youtube-policy.md](docs/12-youtube-policy.md) | Monetisation and AI-content rules we design around |
| 13 | [docs/13-history-and-lessons.md](docs/13-history-and-lessons.md) | What we tried, what got rejected and why |

## Repo layout

```
code/
  pilot/              shared drawing library: style.py (palette, paper shapes, text, grain),
                      dynamic_test.py (camera, shake, kinetic words, transitions, blur)
  everyone_vanished/  full episode renderer for "Everyone Vanished Except You" (the reference episode)
    ep02.py           timeline + compositor + transitions + video/audio entry points
    shots.py          shot list: (id, section card, scene, params, narration)
    scenes_v3.py      later scenes (exec'd inside ep02.py)
    props.py, character.py   reusable props and the realistic adult "you"
    sound_design.py   places CC0 SFX + ambience beds on the timeline
    shorts.py, parts.py      vertical Shorts and the Part 1-5 series
    tools/            VO splitting, loudness normalising, music score layout, final mix
  characters/         six alternative "you" styles on one shared rig
  branding/           avatar, banner and thumbnail renderers
  sfx/fetch.py        builds a local CC0 sound library from Openverse
episodes/
  everyone_vanished/  final script, music cue list, launch metadata, series captions
  pilot_5_star_wanted_script.md   the first pilot (older format, had a host)
templates/            blank script and shot-list templates for a new episode
samples/              small reference images (character sheet, thumbnail, logo)
```

Big media (finished videos, voice files, music, backgrounds) is not in this repo. It lives in the owner's project files and on their PC under `C:\Users\VankuScarce\Videos`.

## Tools you need

- Python 3.11+ with `pycairo`, `numpy`, `pillow`, `soundfile`, `faster-whisper` (word timestamps for captions)
- `ffmpeg` (always encode AAC with `-aac_coder fast`, see the mix doc)
- Font: Inter Display (Bold/Black)
- ElevenLabs (voice, music, optional background paintings), n8n at n8n.cobaltsoft.eu (upload + Telegram approval)

## Status (26 Nov 2026)

- Channel: The Unlikely You, channel id `UC3kbMxX7usz33Oz6BhwPcaQ`. Phone verification is still failing, so custom thumbnails and outside links are blocked until it works.
- Published/queued: "Everyone Vanished Except You" (10:39 long video waits for verification; the Part 1-5 series goes out as Shorts).
- Next: the owner picks a new topic. Read [docs/11-upgrade-goals.md](docs/11-upgrade-goals.md) before starting; the next episode must sound and look better than the last.
