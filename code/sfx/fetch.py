"""Build a CC0 sound library from Openverse (mostly Freesound). Usage: python3 fetch.py OUTDIR"""
import json, os, sys, time, urllib.request, urllib.parse
Q = {  # tag: query
 'whoosh': 'whoosh', 'swoosh_fast': 'fast swoosh', 'paper_whoosh': 'paper whoosh', 'paper_rustle': 'paper slide',
 'impact': 'cinematic impact', 'boom': 'deep boom hit', 'riser': 'riser tension', 'sub_drop': 'sub drop',
 'city_amb': 'city ambience', 'wind': 'wind ambience', 'night_crickets': 'crickets night', 'birds_morning': 'birds morning',
 'room_tone': 'room tone quiet', 'car_idle': 'car engine idle', 'wipers': 'windshield wiper', 'bin_crash': 'trash can fall',
 'metal_clang': 'metal clang', 'dog_bark': 'dog bark', 'dog_whine': 'dog whine', 'dog_pant': 'dog panting',
 'scratch_door': 'scratching door', 'door_creak': 'door creak open', 'phone_buzz': 'phone vibration', 'notif': 'notification ping',
 'alarm_clock': 'digital alarm clock', 'appliance_beep': 'microwave beep', 'hum_electric': 'electrical hum', 'power_down': 'power down',
 'fence_buzz': 'electric buzz', 'fire': 'fire crackling', 'thunder': 'thunder strike', 'water_drip': 'water dripping cave',
 'water_flow': 'water flowing', 'pig': 'pig grunt', 'horse_gallop': 'horses galloping', 'wolf_howl': 'wolf howl',
 'cat_meow': 'cat meow', 'chickens': 'chickens', 'cow': 'cow moo', 'footsteps': 'footsteps pavement', 'clock_tick': 'clock ticking',
 'stopwatch': 'stopwatch click', 'bicycle': 'bicycle bell', 'glass_bottle': 'glass bottle', 'stamp': 'rubber stamp',
 'ui_pop': 'pop', 'click': 'click', 'heartbeat': 'heartbeat', 'shopping_cart': 'shopping cart', 'escalator': 'escalator',
 'traffic_light': 'pedestrian crossing beep', 'server_room': 'server room', 'crack': 'ice crack', 'grass': 'grass rustle',
}
out = sys.argv[1]; os.makedirs(out, exist_ok=True)
meta_p = os.path.join(out, 'library.json'); meta = json.load(open(meta_p)) if os.path.exists(meta_p) else {}
for tag, q in Q.items():
    if tag in meta: continue
    url = 'https://api.openverse.org/v1/audio/?' + urllib.parse.urlencode({'q': q, 'license': 'cc0', 'page_size': 8})
    try:
        d = json.load(urllib.request.urlopen(urllib.request.Request(url, headers={'User-Agent': 'sfx-fetch/1.0'}), timeout=30))
    except Exception as e:
        print('ERR', tag, e); time.sleep(10); continue
    keep = []
    for r in d['results']:
        dur = (r.get('duration') or 0)/1000
        if not r.get('url') or dur > 90: continue
        fn = f"{tag}_{len(keep)}.{r.get('filetype') or 'mp3'}"
        try:
            urllib.request.urlretrieve(r['url'], os.path.join(out, fn))
        except Exception as e:
            print('dl fail', tag, e); continue
        keep.append(dict(file=fn, title=r['title'], creator=r.get('creator'), license=r['license'], source=r['source'], page=r.get('foreign_landing_url'), dur=dur))
        if len(keep) >= 4: break
    meta[tag] = keep; json.dump(meta, open(meta_p, 'w'), indent=1); print(tag, len(keep)); time.sleep(3.2)
