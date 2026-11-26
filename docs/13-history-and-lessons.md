# 13. History and lessons

Short log of what was tried, so a new session doesn't repeat it.

## Pilot: "How Long Would You Survive a Real 5-Star Wanted Level?" (24 Nov 2026)

- Had a host (Ozzie, an owl in a hi-vis vest) and a grey-hoodie "you". 6:20, then extended to 9:23 (under 8 min means no mid-roll ads, so scripts now target ~1,600 words).
- The owner found the visuals too static, so we made the **dynamic style test** (camera moves, whip/zoom/spin transitions, kinetic type), which became the house style.
- 10 host concepts (owl, fox, TV robot, analyst, pigeon...) were all rejected as too childish. **Decision: no host, narrator only.**
- Voice samples: Eric, Older Joe, Oz Geordie, Callum, Ember. **Eric chosen.**
- Calibration: ~145 spoken words per finished minute.

## "Everyone Vanished Except You" (25 Nov 2026), 4 versions

- v1-v2: lots of animal/pet stats. The owner disliked it: too stat-heavy, and the twist (the animals stay) was given away in the opening. **Rule: never reveal the twist early.**
- v3: new story the owner approved: comforts switch off one by one with small wins, month-4 boredom, Scraps the dog as companion (not the focus), the mission to restart humanity (real science: two-father mice, frozen embryos, artificial wombs), open ending. Music was CC BY from Jamendo and far too quiet (~18 dB under the voice).
- Sound: the owner disliked synthesized "AI" whooshes and beeps. **Switched to real CC0 SFX** + ambience beds.
- v4 (final, 10:39): re-voiced on eleven_v4. A version with heavy audio tags (whispers, pauses) was rejected as "way too much"; final is **plain text**. Music replaced with **12 Eleven Music cues**, one per section, audible and changing with mood.
- Found that ffmpeg's default AAC encoder added clicks: **always `-aac_coder fast`**.
- Cut into a **5-part series** after studying the reference reels (We Suppose So, Absolute Zero). The 6 single teaser Shorts were dropped.
- Realistic "you" v2 (no hoodie) for this episode; afterwards six alternative character styles were made and the owner likes all six.
- Feedback after release prep: **upgrade SFX quality/choice and make visuals more detailed and dynamic** ([11](11-upgrade-goals.md)); experiments used about half the monthly ElevenLabs credits ([10](10-elevenlabs-credit-budget.md)).

## Operations

- Phone verification for the channel keeps failing (several carriers tried). Long video waits; Shorts go out meanwhile.
- Unverified channel daily upload limit is about 10.
- Telegram Markdown breaks on underscores in ids; escape them.
