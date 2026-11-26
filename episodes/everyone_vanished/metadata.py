import json
LONG_TITLE = "What If Everyone on Earth Vanished... Except You?"
SOURCES = """Sources for the science bits:
- Mice with two fathers reach adulthood (2025): https://www.livescience.com/health/fertility-pregnancy-birth/chinese-scientists-created-mice-with-2-dads-and-they-survived-to-adulthood
- Egg cells from male mouse cells (2023): https://www.scientificamerican.com/article/mice-with-two-fathers-researchers-develop-egg-cells-from-male-mice/
- Frozen IVF embryos in limbo: https://www.technologyreview.com/2025/01/13/1109922/inside-the-strange-limbo-facing-ivf-embryos/
- Artificial womb keeps lambs alive (2017): https://www.pbs.org/newshour/health/artificial-womb-keeps-premature-lambs-alive-weeks-humans-next
- Mouse embryos grown outside the uterus (2021): https://www.technologyreview.com/2021/03/17/1020969/mouse-embryo-grown-in-a-jar-humans-next/"""
LONG_DESC = f"""You wake up at 3:17 AM. Your phone is still glowing. Every car on the street is still running. And every other person on Earth is gone.

What actually happens next? The power grid, the food, the silence, and the one question nobody wants to answer: could one person bring humanity back?

Chapters
0:00 3:17 AM
1:01 Hour 4: The world on autopilot
1:51 Day 2: The lights go out
3:07 Day 3: Something at the door
3:50 Week 1: Everything is free, nothing works
5:25 Month 1: The comforts go one by one
6:49 Month 4: The quiet
7:42 Year 1: The green comes back
8:14 The mission
10:00 What happens next

Would you last a year? Tell me in the comments.

{SOURCES}

Animated fiction. Narration and some visuals made with AI tools.

#whatif #animation #alone"""
LONG_TAGS = "what if,what if everyone vanished,last person on earth,alone on earth,everyone disappeared,what if scenario,animated story,hypothetical,survival,the unlikely you"

def short_desc(line, long_url):
    return f"""{line}

Watch the full story: {long_url}

#shorts #whatif #animation"""

SHORTS = [
  ("short1_3_17am.mp4", "Everyone on Earth vanished at 3:17 AM. Except you. #shorts", "Every person on Earth is gone. Your phone is still glowing."),
  ("short2_scratching.mp4", "Something is scratching at your door... #shorts", "You're supposed to be the last one left. So what's at the door?"),
  ("short3_free_nothing_works.mp4", "Everything is free. Nothing works. #shorts", "Every store is open to you. None of it helps for long."),
  ("short4_the_quiet.mp4", "4 months alone on Earth. This is the hard part. #shorts", "It isn't hunger that gets you. It's the quiet."),
  ("short5_restart_humanity.mp4", "Could one man restart humanity? #shorts", "The science says it isn't impossible. It's just very, very hard."),
  ("short6_lit_window.mp4", "One window in the city is still lit... #shorts", "Everyone vanished. So who left the light on?"),
]
SHORT_TAGS = "what if,shorts,everyone vanished,last person on earth,alone on earth,animation,the unlikely you"
# UTC publish times: long + short1 Fri 27 Nov 17:00 UTC (19:00 Sofia), then daily
SCHEDULE = ["2026-11-27T17:00:00Z","2026-11-27T17:00:00Z","2026-11-28T17:00:00Z","2026-11-29T17:00:00Z","2026-11-30T17:00:00Z","2026-12-01T17:00:00Z","2026-12-02T17:00:00Z"]
