"""Shot list for a new episode. Copy to code/<episode>/shots.py.
Row: (id, section_card or None, scene_name, params, narration)
- section_card = (stopwatch text, TITLE, SUBTITLE): shows a big stopwatch card in the first ~1.4 s of the shot.
- scene_name must match a function sc_<scene_name>(ctx, s) in the episode renderer.
- params: dict passed to the scene (e.g. {'dur': 3.6} for a shot with no narration).
- narration: exactly the locked script line; the VO file vo/<id>.wav sets the shot length.
Every shot needs constant motion and enough detail (see docs/11-upgrade-goals.md)."""

HOST = None  # narrator only

SHOTS = [
 ('s01', None, 'opening_wide', {}, 'You wake up ...'),
 ('s02', None, 'closeup_object', {}, '...'),
 ('title', None, 'title_card', {'dur': 3.6}, ''),
 ('s08', ('04:00:00', 'HOUR 4', 'SECTION TITLE'), 'section_scene', {}, '...'),
]
