# 6. Titles, thumbnails and descriptions

## Titles

- Pattern: **"What If ... Except You?"** / **"What If You ...?"**, second person, under ~60 characters.
- Hint, never spoil. "What If Everyone on Earth Vanished... Except You?" works; anything mentioning the animals (the twist) would not.
- Shorts/Parts: `"Everyone on Earth vanished except you (Part N/5) #shorts"`.

## Thumbnails

Code-drawn in the same style as the video (`code/branding/thumbs_v2.py` renders the scene, `thumbs_v2_text.py` adds the text). Make **3 options** per video and let the owner pick in Telegram.

What we learned (the owner picked option D, `samples/thumb_D_where_is_everyone.jpg`):
- A **big shocked close-up of "you"** in the scene, readable at phone size.
- **2-4 words** of text max, high contrast (cream/orange on dark), not the title repeated.
- One clear focal point, the empty world behind.
- Never show the twist.

Custom thumbnails require a **phone-verified** channel. Until verification works, YouTube uses an auto frame.

## Description

Template in `episodes/everyone_vanished/metadata.py`:
1. 2-3 line hook in second person (no spoiler).
2. Chapters with timestamps (one per section card).
3. Comment question.
4. Sources for every factual claim (links).
5. Line: "Animated fiction. Narration and some visuals made with AI tools."
6. 3 hashtags (`#whatif #animation #<topic>`).

Tags: 8-10 search phrases plus "the unlikely you". Unverified channels cannot have clickable outside links, so the sources only work after verification.

## Branding

- Channel name **The Unlikely You**, handle **@theunlikelyyou**.
- Profile picture: the "C wordmark" (`samples/C_wordmark.png`), navy/orange/cream, Inter Display.
- Banner: `code/branding/banner.py` (stars + city silhouette).
