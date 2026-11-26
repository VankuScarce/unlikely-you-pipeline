"""Episode 2 sound design v2: real recorded CC0 sounds placed on the action, scene ambience, optional music.
Usage: python3 sound_design.py VO_DIR LIB_DIR OUT_DIR [music.wav ...]
Writes sfx.wav (spot effects + ambience) and music.wav (bed) next to vo.wav (from ep02.audio)."""
import sys, os, json, subprocess, wave, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import ep02

SR = 48000
LIB = None; META = {}; CACHE = {}

def load(tag, k=0, max_s=None):
    """Decode library sound tag variant k -> mono float, leading silence trimmed, peak-normalised."""
    vs = META.get(tag) or []
    if not vs: return None
    f = os.path.join(LIB, vs[k % len(vs)]['file'])
    key = (f, max_s)
    if key in CACHE: return CACHE[key]
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', f, '-ac', '1', '-ar', str(SR), '-f', 's16le', '-'], capture_output=True).stdout
    x = np.frombuffer(raw, np.int16).astype(float)/32768
    if len(x) == 0: return None
    thr = 0.02*np.abs(x).max(); i = np.argmax(np.abs(x) > thr); x = x[i:]
    if max_s: x = x[:int(max_s*SR)]
    fade = min(len(x)//4, int(0.08*SR))
    if fade > 0: x[-fade:] *= np.linspace(1, 0, fade)
    x = x/(np.abs(x).max()+1e-9)
    CACHE[key] = x
    return x

def db(v): return 10**(v/20)

class Mix:
    def __init__(s, n): s.buf = np.zeros(n); s.n = n
    def add(s, x, at, gain_db=0.0, align_peak=False):
        if x is None: return
        if align_peak:  # put the loudest moment of the sound at `at`
            env = np.convolve(np.abs(x), np.ones(480)/480, 'same'); at -= np.argmax(env)/SR
        i = int(at*SR)
        if i < 0: x = x[-i:]; i = 0
        j = min(s.n, i+len(x))
        if i < s.n and j > i: s.buf[i:j] += x[:j-i]*db(gain_db)
    def bed(s, x, t0, t1, gain_db, fade=0.8):
        """Loop x across [t0,t1] with crossfades and fade in/out."""
        if x is None or t1 <= t0: return
        L = int((t1-t0)*SR); out = np.zeros(L); xf = int(0.5*SR); pos = 0
        if len(x) < 2*xf: x = np.tile(x, int(2*xf/len(x))+2)
        while pos < L:
            seg = x.copy(); seg[:xf] *= np.linspace(0, 1, xf); seg[-xf:] *= np.linspace(1, 0, xf)
            e = min(L, pos+len(seg)); out[pos:e] += seg[:e-pos]; pos += len(seg)-xf
        f = min(int(fade*SR), L//2); out[:f] *= np.linspace(0, 1, f); out[-f:] *= np.linspace(1, 0, f)
        s.add(out, t0, gain_db)

# scene -> list of (ambience tag, gain dB)
AMB = {
 'bedroom': [('room_tone', -30), ('birds_morning', -34)],
 'quiet_list': [('wind', -30)], 'street_car': [('wind', -32)], 'population': [('wind', -36)],
 'bin_crash': [('wind', -30)], 'autopilot_words': [('wind', -34)], 'machines_triptych': [('room_tone', -32)],
 'fuel_servers': [('server_room', -28)], 'control_room': [('hum_electric', -30)], 'plant_exterior': [('wind', -32)],
 'grid_map': [('hum_electric', -34)], 'solar_house': [('night_crickets', -30)], 'nuclear': [('wind', -30)],
 'milky_way': [('night_crickets', -28)], 'door_scratch': [('room_tone', -28)], 'door_open': [('night_crickets', -32)],
 'open_doors': [('birds_morning', -32)], 'cat_king': [('wind', -32)], 'garage_pack': [('water_drip', -30)],
 'barn_stats': [('chickens', -30)], 'pig_escape': [('birds_morning', -32)], 'zoo_gate': [('night_crickets', -30)],
 'cart_highway': [('wind', -32)], 'water_tower': [('birds_morning', -34)], 'supermarket': [('hum_electric', -32)],
 'pharmacy_car': [('wind', -32)], 'porch_dog': [('night_crickets', -30)], 'subway_flood': [('water_drip', -26), ('water_flow', -32)],
 'suburb_fire': [('fire', -24)], 'main_street_wild': [('birds_morning', -30), ('wind', -34)], 'green_words': [('grass', -30)],
 'sidewalk_crack': [('wind', -32)], 'car_chair': [('wind', -32)], 'last_light': [('wind', -34)], 'golf_horses': [('birds_morning', -30)],
 'exclusion_zone': [('wind', -28), ('birds_morning', -34)], 'decay_timelapse': [('wind', -30)], 'what_lasts': [('wind', -34)],
 'green_city': [('birds_morning', -28)], 'outro_cta': [('night_crickets', -34)], 'results_board': [('clock_tick', -30)],
 'scraps_named': [('wind', -34), ('birds_morning', -34)], 'phone_dead': [('hum_electric', -34)], 'ice_cream': [('water_drip', -32)],
 'cold_shower': [('water_flow', -30)], 'siphon': [('wind', -32)], 'movie_night': [('night_crickets', -36)], 'boredom_words': [('room_tone', -30)],
 'same_day': [('clock_tick', -32), ('wind', -30)], 'routine': [('birds_morning', -32)], 'porch_question': [('night_crickets', -30)],
 'mission_decide': [('birds_morning', -32)], 'one_man': [('room_tone', -30)], 'library_lab': [('room_tone', -30)], 'two_dads': [('hum_electric', -36)],
 'embryo_freezer': [('hum_electric', -30)], 'nitrogen': [('hum_electric', -32)], 'womb': [('hum_electric', -36)], 'mission_board': [('room_tone', -32)],
 'lit_window': [('night_crickets', -30), ('wind', -36)], 'open_question': [('wind', -36)], 'outro_try': [('night_crickets', -34)],
}
# shot id -> list of (tag, fraction of VO window or 'lead'/abs seconds via ('t', x), gain dB, max seconds)
SPOT = {
 's01': [('alarm_clock', -0.08, -20, 2.0)], 's03': [('phone_buzz', 0.02, -18, 1.2), ('notif', 0.1, -24, 0.6)],
 's04': [('car_idle', 0.15, -22, 6.0), ('wipers', 0.25, -24, 4.0)], 's06': [('bin_crash', 0.05, -10, 2.5), ('metal_clang', 0.09, -18, 1.2)],
 's09': [('traffic_light', 0.0, -26, 2.0), ('escalator', 0.3, -26, 3.0), ('appliance_beep', 0.85, -18, 1.5)],
 's12': [('power_down', 0.25, -22, 2.5)], 's14': [('power_down', 0.82, -16, 3.0)], 's15': [('power_down', 0.2, -24, 2.0)],
 's17': [('power_down', 0.12, -20, 2.5)], 's19': [('scratch_door', 0.12, -14, 4.0), ('scratch_door', 0.32, -16, 3.0)],
 's20': [('door_creak', -0.05, -14, 3.0)], 's21': [('dog_bark', 0.0, -12, 1.5), ('dog_pant', 0.1, -22, 3.0)],
 's22': [('dog_whine', 0.6, -22, 2.0)], 's23': [('door_creak', 0.05, -22, 2.0), ('dog_bark', 0.3, -18, 1.0)],
 's24': [('cat_meow', 0.15, -18, 1.5)], 's25': [('dog_bark', 0.5, -22, 2.0), ('dog_bark', 0.58, -26, 2.0)],
 's27': [('chickens', 0.2, -22, 3.0), ('cow', 0.5, -20, 2.5)], 's28': [('pig', 0.05, -16, 2.0), ('metal_clang', 0.12, -16, 1.2)],
 's29': [('fence_buzz', 0.05, -24, 5.0), ('power_down', 0.45, -18, 2.0)], 's30': [('shopping_cart', 0.1, -20, 5.0)],
 's31': [('water_flow', 0.66, -22, 5.0)], 's32': [('glass_bottle', 0.42, -22, 1.0)], 's35': [('dog_pant', 0.3, -22, 3.0)],
 's37': [('water_flow', 0.45, -20, 8.0)], 's38': [('thunder', 0.02, -10, 4.0)], 's39': [('footsteps', 0.1, -28, 3.0)],
 's42': [('crack', 0.45, -16, 1.5)], 's43': [('bicycle', 0.85, -16, 1.5)], 's45': [('horse_gallop', 0.1, -18, 5.0), ('wolf_howl', 0.78, -18, 3.0)],
 's47': [('wolf_howl', 0.45, -18, 4.0)], 's49': [('glass_bottle', 0.3, -20, 1.0)], 's53': [('dog_pant', 0.5, -28, 2.0)],
}
SPOT.update({
 'n01': [('dog_pant', 0.32, -24, 2.5), ('dog_bark', 0.8, -24, 1.0)], 'n02': [('power_down', 0.5, -18, 2.5), ('appliance_beep', 0.6, -22, 0.8)],
 'n03': [('water_drip', 0.1, -26, 2.0)], 'n04': [('water_flow', 0.05, -24, 4.0), ('fire', 0.62, -24, 4.0)],
 'n05': [('metal_clang', 0.3, -22, 1.0), ('water_flow', 0.6, -28, 3.0)], 'n06': [('boom', 0.35, -26, 2.0), ('boom', 0.7, -24, 2.0), ('dog_whine', 0.84, -20, 1.5)],
 'n08': [('clock_tick', 0.0, -26, 5.0)], 'n09': [('dog_pant', 0.38, -26, 2.0)], 'n12': [('sub_drop', 0.5, -18, 2.0)],
 'n15': [('hum_electric', 0.5, -28, 4.0)], 'n16': [('alarm_clock', 0.84, -26, 1.2)], 'n18': [('dog_bark', 0.86, -22, 1.0)],
 'n20': [('hum_electric', 0.35, -26, 5.0)], 'n21': [('sub_drop', 0.6, -16, 2.5)],
})
STAMPS = {  # shot -> fraction where a stamp lands (matches ep02 scene code)
 'n02': 0.55, 'n03': 0.55, 'n05': 0.82, 'n06': 0.82, 'n12': 0.8, 'n14': 0.78, 'n15': 0.8, 'n16': 0.82, 'n17': 0.9, 'n09': 0.88,
 's01': 0.62, 's04': 0.76, 's12': 0.82, 's14': 0.82, 's16': 0.82, 's17': 0.12, 's19': 0.75, 's26': 0.8, 's28': None,
 's38': 0.5, 's39': 0.6, 's40': 0.82, 's42': 0.8, 's43': 0.55, 's47': 0.02, 's48': 0.82, 's51': 0.82,
}

def build(vo_dir, lib, out_dir, music=()):
    global LIB, META
    LIB = lib; META = json.load(open(os.path.join(lib, 'library.json')))
    TL = ep02.setup(vo_dir); total = TL[-1]['start']+TL[-1]['dur']; n = int(total*SR)+SR
    sfx = Mix(n); mus = Mix(n); k = 0
    # ambience: merge consecutive shots with the same tags into one bed
    runs = []
    for sh in TL:
        a = tuple(AMB.get(sh['scene'], []))
        if runs and runs[-1][0] == a: runs[-1][2] = sh['start']+sh['dur']
        else: runs.append([a, sh['start'], sh['start']+sh['dur']])
    for a, t0, t1 in runs:
        for tag, g in a:
            k += 1; sfx.bed(load(tag, k), t0-0.3, t1+0.3, g)
    for i, sh in enumerate(TL):
        vo0 = sh['start']+sh['lead']
        # transitions: real whooshes peaking just after the cut
        if i > 0 and TL[i-1]['trans'] not in ('cut',):
            tr = TL[i-1]['trans']; tag = {'whip_l': 'swoosh_fast', 'whip_u': 'paper_whoosh', 'spin': 'whoosh', 'zoom': 'whoosh', 'flash': 'swoosh_fast'}[tr]
            sfx.add(load(tag, i, 1.2), sh['start']+0.04, -17, align_peak=True)
        elif i > 0:
            sfx.add(load('paper_rustle', i, 0.5), sh['start'], -30)
        if sh['card']:
            sfx.add(load('impact', i, 2.5), sh['start']+0.05, -12)
            sfx.add(load('stopwatch', i, 0.4), sh['start']+0.25, -20)
        for tag, f, g, mx in SPOT.get(sh['id'], []):
            sfx.add(load(tag, i, mx), vo0+f*sh['vo'], g)
        f = STAMPS.get(sh['id'])
        if f is not None: sfx.add(load('stamp', i, 0.6), vo0+f*sh['vo'], -16)
        if sh['scene'] == 'title_card':
            sfx.add(load('riser', 0, 3.0), sh['start']-2.6, -18); sfx.add(load('boom', 0, 3.0), sh['start']+0.1, -10)
        if sh['id'] == 's21':  # the reveal
            sfx.add(load('sub_drop', 0, 2.0), vo0+0.78*sh['vo'], -10)
        if sh['id'] == 's20':
            sfx.add(load('riser', 1, 3.0), sh['start']-2.8, -20)
    # music: user-supplied or CC0 tracks, laid end to end with crossfades, quiet under the voice
    if music:
        tracks = []
        for f in music:
            raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', f, '-ac', '1', '-ar', str(SR), '-f', 's16le', '-'], capture_output=True).stdout
            x = np.frombuffer(raw, np.int16).astype(float)/32768; tracks.append(x/(np.abs(x).max()+1e-9))
        t = 0.0; mi = 0
        while total-t > 3.0:  # stop when less than a crossfade is left (avoids going backwards)
            x = tracks[mi % len(tracks)]; mi += 1
            d = min(len(x)/SR, total-t); mus.bed(x[:int(d*SR)], t, t+d, -20, fade=2.0); t += d-2.0
    def w(p, x):
        pcm = (np.clip(x, -1, 1)*32767).astype(np.int16)
        with wave.open(p, 'wb') as f: f.setnchannels(1); f.setsampwidth(2); f.setframerate(SR); f.writeframes(pcm.tobytes())
    w(os.path.join(out_dir, 'sfx.wav'), sfx.buf); w(os.path.join(out_dir, 'music.wav'), mus.buf)
    missing = sorted(({t for v in SPOT.values() for t, *_ in v} | {t for v in AMB.values() for t, _ in v}) - set(k for k, v in META.items() if v))
    print('total', round(total, 2), 'missing tags:', missing)

if __name__ == '__main__':
    build(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4:])
