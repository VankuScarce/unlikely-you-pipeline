# 1. Format and story rules

## Fixed rules (agreed with the owner)

- **Language:** English.
- **Audience:** teens and adults. No cute mascots, no kids' tone, never "made for kids". The owner rejected 10 cartoon host concepts as "too childish".
- **Format:** "What If" story in the **second person** ("You wake up at 7:02..."). **Narrator only**, no host character on screen.
- **Length:** long video about **10 minutes** (must be over 8:00 so mid-roll ads are possible). That is about **1,500-1,650 spoken words** at our pace (~145-160 words per finished minute) and roughly **8,500-9,000 characters** of narration.
- **Shorts built in:** every long video is planned so it can be cut into a **Part 1-5 series** (each part ends on a cliffhanger). See [07-shorts-and-series.md](07-shorts-and-series.md).
- **Cadence goal:** about 2 long videos per week plus their Shorts, once the pipeline is smooth. The owner can review 10-15 hours a week, no more.
- **Never reveal the twist** in the title, thumbnail or opening. Hint at it, build a curiosity gap, and reveal it about a third of the way in. (Example: in "Everyone Vanished" the animals staying behind was hidden until Day 3; the opening only says "you're not completely alone... something knocked that bin over".)
- **Refer to videos by their title** when talking to the owner, not "episode 2".

## What the owner likes

- **Interesting over emotional.** Favourite reference: the "Absolute Zero" Part 1 reel by @traficstory (survival driven by real physics). Second reference: We Suppose So ("What if you could see how many more times you'll see each person?").
- The **human experience**: comforts disappearing one by one, small wins, boredom, routine, finding a purpose or mission.
- **Open endings** that leave the big question unanswered.
- Animals or pets only as **supporting** elements, not the focus. No long stat blocks.

## Story structure that works

Taken from "Everyone Vanished Except You" (the reference episode, script in `episodes/everyone_vanished/script.md`) and from the two reference reels:

1. **Cold open (0:00-1:00).** Hook within 12-15 seconds: a personal, concrete situation plus 2-3 shocking images. A warning or mystery line. A hidden threat or question that is NOT answered yet ("something knocked that bin over"). End with a promise line ("So let's find out what disappears first... The clock starts now.").
2. **Title card** (3-4 s).
3. **Sections with a running clock.** Each section opens with a **section card**: a stopwatch value plus a title ("HOUR 4 / THE WORLD ON AUTOPILOT", "DAY 2 / THE LIGHTS GO OUT", "MONTH 4 / THE QUIET"). The stopwatch then stays in the top-left HUD. Small, exact scope works best (one city, one building, 100 hours, one year).
4. **Alternate story and facts.** About 30% facts, each fact block under ~50 seconds, and **every fact must change a decision you make**. Facts come from real sources, and the description lists them.
5. **Running mystery thread** that spans several parts (the scratching at the door, the knocking upstairs).
6. **Twist reveal around 1/3** of the way in.
7. **Peak around 70-75%** (biggest stakes or the mission).
8. **Ending:** open question plus a comment prompt ("Would you last a year? Tell me in the comments.").

Each of the five Part cut points must land on a cliffhanger line, so plan them while writing (see the `PARTS` table in `code/everyone_vanished/parts.py`).

## Fact-checking

Mark each factual line in the script as `FACT` (checked against a real source, link it) or `GUESS` (our estimate, phrase it as an estimate: "experts generally expect..."). Put the sources in the YouTube description. Never invent studies or numbers.

## Topic ideas

The owner chooses topics. A planned side experiment: make **Part 1 only** for 4-5 different topics, each ending on a cliffhanger, post them and see which gets the most views and "Part 2?" comments; the winner becomes the next full story. Good topic shape: a personal premise, one hook device (a number, a clock, a rule), a small setting, real science/physics that changes your choices.

Character style per topic: see [05-visual-style.md](05-visual-style.md) (six styles with a story-type mapping).
