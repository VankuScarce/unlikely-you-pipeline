# 7. Shorts and the Part 1-5 series

The fastest route to the YouTube Partner Program is a Shorts-heavy cadence, so every long video becomes a **5-part series**. Views before YPP acceptance are never paid retroactively, so volume of good Shorts matters early.

## Part series (current standard)

`code/everyone_vanished/parts.py EPISODE.mp4 VO_DIR OUT_DIR` cuts the finished episode at planned cliffhanger shots:

```
PARTS = [(part, first shot, last shot, cover shot, cover frame fraction), ...]
```

For each part it makes:
- a **16:9** version with a "PART N" label top-right (Instagram/TikTok, like the reference reels),
- a **9:16** version: the full 16:9 frame over a blurred copy of itself, with **burned-in captions** timed from faster-whisper word timestamps,
- a **9:16 cover** with a big "PART N",
- a 2 s end card **"PART N+1 IS UP NEXT"**.

Parts are 1-3 minutes. Each must end on an unanswered line. For YouTube Shorts we append a 0.5 s cover frame at the end (`series/yt_shorts/partN.mp4`) so the Shorts shelf shows the cover.

Posting: the owner wanted **all five parts posted at once**, Part 5 first and Part 1 last so Part 1 sits on top of the channel. Captions for Instagram/TikTok: short, casual, funnel to the full video on YouTube.

## Single teaser Shorts (older approach)

`shorts.py` cuts standalone Shorts with a hook title. These were dropped for "Everyone Vanished" in favour of the series, but the code still works for one-off clips.

## Where things go

- **YouTube:** the long video + the 9:16 parts as Shorts. Don't upload the 16:9 parts as separate long videos (duplicate content).
- **Instagram Reels / TikTok:** the 9:16 (or 16:9) parts with the cover.
