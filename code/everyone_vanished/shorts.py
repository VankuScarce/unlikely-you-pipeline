"""Cut vertical Shorts (1080x1920) from the finished episode, with a hook title and burned-in captions.
Usage: python3 shorts.py EPISODE.mp4 VO_DIR OUT_DIR"""
import sys, os, re, subprocess
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import ep02
from shots import SHOTS

SHORTS = [  # (name, first shot, last shot, hook title)
    ("short1_3_17am", "s01", "s06", "EVERYONE VANISHED\\NAT 3:17 AM"),
    ("short2_scratching", "s19", "n01", "SOMETHING IS SCRATCHING\\NAT YOUR DOOR"),
    ("short3_free_nothing_works", "s30", "s31", "EVERYTHING IS FREE.\\NNOTHING WORKS."),
    ("short4_the_quiet", "n07", "n10", "4 MONTHS ALONE ON EARTH.\\NTHIS IS THE HARD PART"),
    ("short5_restart_humanity", "n12", "n15", "COULD ONE MAN\\NRESTART HUMANITY?"),
    ("short6_lit_window", "n19", "n21", "ONE WINDOW\\NIS STILL LIT"),
]
TXT = {sid: t for sid, _, _, _, t in SHOTS}

def ts(t):
    h = int(t//3600); m = int(t % 3600//60); s = t % 60
    return f"{h}:{m:02d}:{s:05.2f}"

def _norm(w):
    return re.sub(r'[^a-z0-9]', '', w.lower())

def _aligned(words, wt):
    """Give each script word a (start, end) from Whisper word timings; unmatched words are interpolated."""
    import difflib
    a = [_norm(w) for w in words]; b = [_norm(w) for w, _, _ in wt]
    tim = [None]*len(words)
    for blk in difflib.SequenceMatcher(None, a, b, autojunk=False).get_matching_blocks():
        for k in range(blk.size):
            tim[blk.a+k] = (wt[blk.b+k][1], wt[blk.b+k][2])
    known = [i for i, x in enumerate(tim) if x]
    if not known: return None
    for i in range(len(tim)):
        if tim[i]: continue
        prv = max([k for k in known if k < i], default=None); nxt = min([k for k in known if k > i], default=None)
        s = tim[prv][1] if prv is not None else max(0.0, tim[nxt][0]-0.3)
        e = tim[nxt][0] if nxt is not None else tim[prv][1]+0.35
        n0 = prv if prv is not None else i-1; n1 = nxt if nxt is not None else i+1
        f0 = (i-n0)/(n1-n0); f1 = (i-n0+1)/(n1-n0)
        tim[i] = (s+(e-s)*f0, s+(e-s)*f1)
    return tim

def _chunks(words):
    """Split at sentence ends and commas, then cut each clause into even pieces of at most 3 words."""
    clauses, cur = [], []
    for i, w in enumerate(words):
        cur.append(i)
        if w[-1] in '.?!,;:':
            clauses.append(cur); cur = []
    if cur: clauses.append(cur)
    merged = []  # glue a one-word clause onto its neighbour inside the same sentence
    for cl in clauses:
        if merged and (len(cl) == 1 or len(merged[-1]) == 1) and words[merged[-1][-1]][-1] not in '.?!' and len(merged[-1])+len(cl) <= 3:
            merged[-1] += cl
        else:
            merged.append(cl)
    out = []
    for cl in merged:
        n = -(-len(cl)//3); size = [len(cl)//n + (1 if k < len(cl) % n else 0) for k in range(n)]; j = 0
        for sz in size:
            out.append(cl[j:j+sz]); j += sz
    return out

def captions(shots, t0, words_json=None):
    """Captions timed to the spoken words (Whisper word timings when available, else spread by length)."""
    import json
    wj = json.load(open(words_json)) if words_json and os.path.exists(words_json) else {}
    ev = []
    for sh in shots:
        if sh['vo'] <= 0: continue
        words = TXT[sh['id']].split(); base = sh['start']+sh['lead']-t0
        tim = _aligned(words, wj[sh['id']]) if sh['id'] in wj else None
        if tim:
            for ch in _chunks(words):
                ev.append([base+tim[ch[0]][0], base+tim[ch[-1]][1], ' '.join(words[i] for i in ch).upper()])
        else:
            chunks = [' '.join(words[i:i+3]) for i in range(0, len(words), 3)]
            tot = sum(len(c)+2 for c in chunks); t = base
            for ch in chunks:
                d = sh['vo']*(len(ch)+2)/tot
                ev.append([t, t+d, ch.upper()]); t += d
    for k in range(len(ev)-1):  # hold each caption until the next one if the gap is short
        if 0 < ev[k+1][0]-ev[k][1] < 0.6: ev[k][1] = ev[k+1][0]
    return [tuple(e) for e in ev]

HEAD = """[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
WrapStyle: 2

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Hook,Inter Display,82,&H00FFFFFF,&H00FFFFFF,&H00000000,&HB0000000,1,0,0,0,100,100,0,0,3,18,0,8,60,60,230,1
Style: Cap,Inter Display,76,&H0000E6FF,&H00FFFFFF,&H00000000,&H64000000,1,0,0,0,100,100,0,0,1,7,3,2,60,60,430,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""

def main(ep, vo_dir, out_dir):
    tl = ep02.setup(vo_dir); os.makedirs(out_dir, exist_ok=True)
    idx = {sh['id']: i for i, sh in enumerate(tl)}
    for name, a, b, hook in SHORTS:
        shots = tl[idx[a]:idx[b]+1]
        t0 = shots[0]['start']; t1 = shots[-1]['start']+shots[-1]['dur']; d = t1-t0
        ass = os.path.join(out_dir, name+'.ass')
        with open(ass, 'w') as f:
            f.write(HEAD)
            f.write(f"Dialogue: 0,{ts(0)},{ts(d)},Hook,,0,0,0,,{{\\fad(150,0)}}{hook}\n")
            for s, e, tx in captions(shots, t0, os.path.join(vo_dir, 'words.json')):
                f.write(f"Dialogue: 1,{ts(s)},{ts(e)},Cap,,0,0,0,,{{\\fscx80\\fscy80\\t(0,90,\\fscx100\\fscy100)}}{tx}\n")
        fc = ("[0:v]split=2[a][b];"
              "[a]scale=-2:1920,crop=1080:1920,gblur=sigma=40,eq=brightness=-0.18[bg];"
              "[b]scale=1080:608[fg];"
              f"[bg][fg]overlay=0:596,subtitles={ass}[v]")
        subprocess.run(['ffmpeg', '-y', '-v', 'error', '-ss', f'{t0:.3f}', '-t', f'{d:.3f}', '-i', ep, '-filter_complex', fc,
                        '-map', '[v]', '-map', '0:a', '-c:v', 'libx264', '-preset', 'medium', '-crf', '20', '-pix_fmt', 'yuv420p',
                        '-c:a', 'aac', '-aac_coder', 'fast', '-b:a', '192k', '-af', 'afade=t=out:st=%.2f:d=0.4' % (d-0.4),
                        os.path.join(out_dir, name+'.mp4')], check=True)
        print(name, round(d, 1), 's')

if __name__ == '__main__':
    main(*sys.argv[1:4])
