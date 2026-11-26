"""Episode 2 renderer: 'What If Everyone on Earth Vanished... Except You?'
Dynamic-test style: code-drawn flat paper art, virtual camera, whip/zoom/spin transitions, kinetic type.
Usage:
  python3 ep02.py plan VO_DIR                 -> writes timeline.json
  python3 ep02.py still T out.png VO_DIR
  python3 ep02.py video out.mp4 t0 t1 VO_DIR
  python3 ep02.py audio out_dir VO_DIR        -> vo.wav + bed.wav"""
import sys, os, json, math, subprocess, wave, cairo, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'pilot'))
from style import *
import dynamic_test as dt
from dynamic_test import kword, shake, cam, speedlines, car, gauge, blur_paint
from props import *
from character import you

def pgauge(ctx, x, y, r, val, vmax=100):
    ctx.save(); dt.gauge(ctx, x, y, r, val, vmax); ctx.restore()
    ctx.arc(x, y+r*0.72, r*0.2, 0, 2*math.pi); ctx.set_source_rgba(0.10, 0.11, 0.16, 1); ctx.fill()
    text(ctx, '%', x, y+r*0.72, r*0.16, c('grey'))
from shots import SHOTS

FPS = 24
LEAD_CARD, LEAD, TAIL = 1.25, 0.25, 0.45

def wav_dur(p):
    with wave.open(p) as w: return w.getnframes()/w.getframerate()

def plan(vo_dir):
    tl = []; t = 0.0
    for sid, card, scene, p, txt in SHOTS:
        if not txt:
            d = p.get('dur', 3.0); tl.append(dict(id=sid, card=card, scene=scene, p=p, start=t, dur=d, lead=0, vo=0)); t += d; continue
        f = os.path.join(vo_dir, sid+'.wav'); vo = wav_dur(f)
        lead = LEAD_CARD if card else LEAD
        d = lead + vo + TAIL
        tl.append(dict(id=sid, card=card, scene=scene, p=p, start=t, dur=d, lead=lead, vo=vo)); t += d
    return tl

class S:  # per-shot timing helper
    def __init__(s, sh, T): s.__dict__.update(sh); s.T = T; s.lt = T - sh['start']
    def at(s, f): return s.lead + f*s.vo
    def pr(s, f0, f1): return prog(s.lt, s.at(f0), s.at(f1))

KEEP = {'scraps': 'Scraps', 'friday': 'Friday', 'antarctic': 'Antarctic', 'us': 'US', 'japan': 'Japan', 'china': 'China', 'israel': 'Israel', 'monday,': 'Monday,', 'am': 'AM', 'tv': 'TV', 'milky': 'Milky', 'way.': 'Way.', 'earth': 'Earth', 'km\u00b2': 'km\u00b2', "neighbour's": "neighbour's"}
def sent(s_):
    if any(ch.isdigit() for ch in s_[:1]) and s_[1:3] == '. ': return s_[:3] + sent(s_[3:])
    ws = s_.lower().split(' ')
    ws = [KEEP.get(w, w) for w in ws]
    out = ' '.join(ws)
    out = '. '.join(x[:1].upper() + x[1:] for x in out.split('. '))
    return out[:1].upper() + out[1:]

def bword(ctx, s_, x, y, size, col, lt, t0, pop=0.22, box=(0.04, 0.05, 0.14, 0.72), anchor='c'):
    p = prog(lt, t0, t0+pop)
    if p <= 0: return
    s_ = sent(s_)
    ctx.select_font_face('Inter Display', cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD); ctx.set_font_size(size)
    e = ctx.text_extents(s_); pad = size*0.28
    sc = back(p); ctx.save(); ctx.translate(x, y); ctx.rotate((1-ease(p))*-0.10); ctx.scale(sc, sc)
    ox = 0 if anchor == 'c' else e.width/2
    rrect(ctx, ox-e.width/2-pad, -size*0.5-pad*0.8, e.width+2*pad, size+pad*1.6, size*0.25); ctx.set_source_rgba(*box); ctx.fill()
    text_paper(ctx, s_, ox, 0, size, col); ctx.restore()

def words_seq(ctx, s, items, y, size=90, col=None, x0=None, gap=40, f0=0.0, f1=0.9, boxed=False):
    """Pop a row of words across the VO window [f0,f1], centred as a row."""
    ctx.select_font_face('Inter Display', cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD); ctx.set_font_size(size)
    ws = [ctx.text_extents(w).x_advance for w in items]; tot = sum(ws)+gap*(len(items)-1)
    x = (W/2 - tot/2) if x0 is None else x0
    for i, (w, wd) in enumerate(zip(items, ws)):
        t0 = s.at(f0 + (f1-f0)*i/max(1, len(items)))
        (bword if boxed else kword)(ctx, w, x+wd/2, y, size, col or c('cream'), s.lt, t0)
        x += wd+gap

def push(ctx, s, z0=1.0, z1=1.15, cx=W/2, cy=H/2, rot0=0.0, rot1=0.0, sh=1.5):
    p = ease(prog(s.lt, 0, s.dur)); z = z0+(z1-z0)*p; r = rot0+(rot1-rot0)*p
    ctx.translate(cx+shake(s.T, sh)[0], cy+shake(s.T, sh)[1]); ctx.scale(z, z); ctx.rotate(r); ctx.translate(-cx, -cy)

# ======================= SCENES =======================
def sc_bedroom(ctx, s):
    sky(ctx, 'dawn'); ctx.save(); push(ctx, s, 1.0, 1.22, W*0.55, H*0.55)
    ctx.rectangle(0, 0, W, H); ctx.set_source_rgba(0.93, 0.88, 0.80, 1); ctx.fill()
    paper(ctx, lambda k: k.rectangle(1100, 160, 560, 420), (0.98, 0.86, 0.62, 1))  # window
    ctx.rectangle(1370, 160, 14, 420); ctx.rectangle(1100, 362, 560, 14); ctx.set_source_rgba(0.85, 0.78, 0.68, 1); ctx.fill()
    g = cairo.LinearGradient(1100, 160, 700, 900); g.add_color_stop_rgba(0, 1, 0.9, 0.6, 0.35); g.add_color_stop_rgba(1, 1, 0.9, 0.6, 0)
    ctx.move_to(1100, 160); ctx.line_to(1660, 580); ctx.line_to(1200, 1080); ctx.line_to(300, 1080); ctx.close_path(); ctx.set_source(g); ctx.fill()
    paper(ctx, lambda k: rrect(k, 200, 700, 900, 220, 30), (0.40, 0.48, 0.66, 1))  # bed
    paper(ctx, lambda k: rrect(k, 220, 640, 260, 90, 30), c('cream'))
    sit = ease(s.pr(0.05, 0.35))
    you(ctx, 620, 860, 0.95, lean=-0.25*(1-sit), t=s.T)
    paper(ctx, lambda k: rrect(k, 1180, 760, 300, 160, 20), (0.45, 0.32, 0.24, 1))  # nightstand
    paper(ctx, lambda k: rrect(k, 1220, 640, 220, 120, 18), c('ink'))
    blink = 1 if int(s.T*2) % 2 == 0 else 0.35
    text(ctx, "7:02", 1330, 702, 80, (1, 0.25, 0.25, blink))
    ctx.restore()
    bword(ctx, "MONDAY, 7:02 AM", W/2, 120, 70, c('cream'), s.lt, s.at(0.05))
    if s.lt > s.at(0.6):
        stamp(ctx, "SOMETHING'S WRONG", W/2, H-140, 80, c('red'), s.lt, s.at(0.62))

def sc_quiet_list(ctx, s):
    sky(ctx, 'day'); ctx.save(); push(ctx, s, 1.15, 1.0, sh=0.8)
    skyline(ctx, s.lt*8, 900, 200, 620, (0.42, 0.52, 0.62, 1), lit=0, seed=3)
    ground(ctx, 900, (0.30, 0.34, 0.40, 1)); ctx.restore()
    ctx.rectangle(0, 0, W, H); ctx.set_source_rgba(0.04, 0.05, 0.12, 0.35); ctx.fill()
    kword(ctx, "QUIET.", W/2, 230, 170, c('cream'), s.lt, s.at(0.0))
    items = ["NO TRAFFIC", "NO NEIGHBOUR'S TV", "NO LEAF BLOWER"]
    for i, it in enumerate(items):
        t0 = s.at(0.25+i*0.25); bword(ctx, it, W/2, 470+i*150, 70, c('cream'), s.lt, t0)
        p = prog(s.lt, t0+0.35, t0+0.6)
        if p > 0:
            ctx.select_font_face('Inter Display', cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD); ctx.set_font_size(70)
            w = ctx.text_extents(sent(it)).width
            ctx.move_to(W/2-w/2-30, 470+i*150); ctx.line_to(W/2-w/2-30+(w+60)*p, 470+i*150)
            ctx.set_line_width(12); ctx.set_source_rgba(*c('red')); ctx.stroke()

def sc_phone(ctx, s):
    ctx.set_source_rgb(0.06, 0.07, 0.12); ctx.paint()
    ctx.save(); push(ctx, s, 0.9, 1.08, rot0=0.06, rot1=-0.03, sh=1.0)
    phone(ctx, W/2, H/2+40, 1.18)
    n = int(41*ease(s.pr(0.05, 0.6)))
    for i in range(min(n, 8)):
        y = H/2-330 + i*92
        rrect(ctx, W/2-200, y, 400, 80, 16); ctx.set_source_rgba(0.22, 0.27, 0.40, 1); ctx.fill()
        text(ctx, ["Mom", "Work", "Dana", "Group chat", "Bank", "Unknown", "Alex", "News"][i], W/2-180, y+28, 26, c('cream'), anchor='l')
        text(ctx, "3:17 AM", W/2+180, y+28, 24, c('orange'), anchor='r')
        text(ctx, "...", W/2-180, y+58, 24, (1, 1, 1, 0.5), anchor='l')
    ctx.restore()
    p = back(s.pr(0.05, 0.2))
    if p > 0:
        ctx.save(); ctx.translate(W/2+260, 220); ctx.scale(p, p)
        ctx.arc(0, 0, 80, 0, 2*math.pi); ctx.set_source_rgba(*c('red')); ctx.fill(); text(ctx, str(max(1, n)), 0, 0, 72, c('cream')); ctx.restore()
    bword(ctx, "EVERY ONE STOPPED AT 3:17 AM", W/2, H-110, 66, c('yellow'), s.lt, s.at(0.62))

def street_bg(ctx, mode='day', off=0, lit=0.0):
    sky(ctx, mode)
    skyline(ctx, off*0.2, 760, 200, 560, (0.44, 0.52, 0.62, 1) if mode != 'night' else (0.10, 0.13, 0.22, 1), lit=lit, seed=8)
    skyline(ctx, off*0.5, 800, 120, 380, (0.32, 0.38, 0.48, 1) if mode != 'night' else (0.07, 0.09, 0.16, 1), lit=lit, seed=9)
    ground(ctx, 800, (0.55, 0.56, 0.60, 1)); road(ctx, 860, 200, dash_off=off)

def sc_street_car(ctx, s):
    ctx.save(); pan = 300*ease(s.pr(0, 1)); push(ctx, s, 1.0, 1.3, W/2+200, 820, sh=1.0)
    ctx.translate(-pan, 0)
    street_bg(ctx, 'day', 0)
    cx = 1250
    car(ctx, cx, 990, 1.3, wheel=0, bounce=abs(math.sin(s.T*30))*2, beam=False)
    # open door
    ctx.save(); ctx.translate(cx+10, 880); ctx.move_to(0, 0); ctx.line_to(90, -40); ctx.line_to(95, 60); ctx.line_to(0, 70); ctx.close_path()
    ctx.set_source_rgba(0.50, 0.53, 0.58, 1); ctx.fill(); ctx.restore()
    wa = math.sin(s.T*5)*0.6  # wiper
    ctx.save(); ctx.translate(cx+70, 845); ctx.rotate(-1.2+wa); ctx.move_to(0, 0); ctx.line_to(0, -60); ctx.set_line_width(5); ctx.set_source_rgba(*c('ink')); ctx.stroke(); ctx.restore()
    for i in range(5):  # exhaust
        q = (s.T*0.8+i*0.2) % 1
        ctx.arc(cx-240-q*200, 960-q*60, 14+q*40, 0, 2*math.pi); ctx.set_source_rgba(0.9, 0.9, 0.92, 0.5*(1-q)); ctx.fill()
    walk = s.pr(0.0, 0.4)
    you(ctx, 500+400*ease(walk), 990, 0.9, phase=s.T*8, run=0.6*(1-prog(walk, 0.95, 1.0)))
    ctx.restore()
    if s.lt > s.at(0.75): stamp(ctx, "NOBODY INSIDE", W/2, 160, 90, c('red'), s.lt, s.at(0.76))

def sc_population(ctx, s):
    ctx.set_source_rgb(0.05, 0.08, 0.16); ctx.paint()
    ctx.save(); z = 2.2-1.6*ease(s.pr(0, 0.6)); ctx.translate(W/2, H/2); ctx.scale(z, z); ctx.rotate(0.1*s.lt); ctx.translate(-W/2, -H/2)
    for i in range(-12, 24):
        ctx.rectangle(i*150-20, -1000, 40, 3000); ctx.rectangle(-1000, i*150-20, 4000, 40)
    ctx.set_source_rgba(0.16, 0.22, 0.34, 1); ctx.fill()
    for i in range(-8, 20):
        for j in range(-8, 14):
            ctx.rectangle(i*150+30, j*150+30, 90, 90); ctx.set_source_rgba(0.10, 0.14, 0.24, 1); ctx.fill()
    ctx.arc(W/2, H/2, 12, 0, 2*math.pi); ctx.set_source_rgba(*c('hivis')); ctx.fill()
    ctx.restore()
    p = s.pr(0.35, 0.75); val = int(8_000_000_000*(1-ease(p)**0.4)) if p < 1 else 0
    sh = shake(s.T, 6*(1-p) if p > 0 else 0)
    t1 = s.at(0.8)
    if s.lt < t1:
        text_paper(ctx, f"{max(val, 0):,}", W/2+sh[0], 380+sh[1], 160, c('cream'))
        kword(ctx, "PEOPLE ON EARTH", W/2, 520, 54, c('grey'), s.lt, s.at(0.3))
    else:
        pop = 1 + 0.25*math.exp(-8*(s.lt-t1))*math.cos(18*(s.lt-t1))
        ctx.save(); ctx.translate(W/2, 380); ctx.scale(pop, pop); ctx.translate(-W/2, -380)
        text_paper(ctx, "1", W/2, 380, 160, c('hivis')); ctx.restore()
        kword(ctx, "PERSON ON EARTH", W/2, 520, 54, c('grey'), s.lt, t1)
        kword(ctx, "EXCEPT YOU.", W/2, 700, 120, c('hivis'), s.lt, t1)

def sc_bin_crash(ctx, s):
    tc = s.at(0.05)  # crash moment
    ctx.save(); z = 1.0 + 0.5*ease(s.pr(0.25, 0.9)); sh = shake(s.T, 14*(1-prog(s.lt, tc, tc+0.6)) if s.lt > tc else 1)
    ctx.translate(W/2+sh[0], H*0.75+sh[1]); ctx.scale(z, z); ctx.translate(-W/2-200*ease(s.pr(0.25, 0.9)), -H*0.75)
    street_bg(ctx, 'dusk', 0)
    ctx.rectangle(0, 0, W, H); ctx.set_source_rgba(0.1, 0.05, 0.2, 0.35); ctx.fill()
    pc = prog(s.lt, tc, tc+0.5)
    bx = 1300 + 260*ease(prog(s.lt, tc, tc+1.6))
    bin_(ctx, bx, 845+40*ease(pc), ang=1.45*ease(pc) + 3*ease(prog(s.lt, tc, tc+1.6)), s=1.0)
    # something slipping away: just a tail + shadow, never seen
    p2 = prog(s.lt, tc+0.1, tc+0.9)
    if 0 < p2 < 1:
        x = 1420 + 700*p2
        ctx.save(); ctx.translate(x, 850); ctx.scale(1, 0.25); ctx.arc(0, 0, 90, 0, 2*math.pi); ctx.restore(); ctx.set_source_rgba(0, 0, 0, 0.45); ctx.fill()
        ctx.move_to(x-60, 820); ctx.curve_to(x-120, 790, x-150, 760, x-170, 700); ctx.set_line_width(14); ctx.set_source_rgba(0.08, 0.06, 0.1, 1); ctx.stroke()
    you(ctx, 600, 990, 0.9, lean=-0.1*ease(pc))
    ctx.restore()
    ctx.rectangle(0, 0, W, H); ctx.set_source_rgba(1, 1, 1, 0.5*(1-prog(s.lt, tc, tc+0.2)) if s.lt > tc else 0); ctx.fill()
    bword(ctx, "NOT COMPLETELY ALONE", W/2, 140, 80, c('cream'), s.lt, s.at(0.15))
    bword(ctx, "IT SOUNDS HUNGRY", W/2, H-130, 72, c('red'), s.lt, s.at(0.8))

def sc_host_intro(ctx, s):
    ctx.set_source_rgb(0.05, 0.07, 0.14); ctx.paint()
    ctx.save(); ctx.translate(W/2, H/2); ctx.rotate(s.lt*0.3)
    for i in range(16):
        ctx.move_to(0, 0); ctx.arc(0, 0, 1600, i*math.pi/8, i*math.pi/8+math.pi/16); ctx.close_path()
    ctx.set_source_rgba(1, 1, 1, 0.04); ctx.fill(); ctx.restore()
    p = back(s.pr(0.0, 0.15)); run = max(0, s.lt - s.at(0.85))
    ctx.save(); ctx.translate(W/2, H/2+40); ctx.scale(p, p); stopwatch(ctx, 0, 0, 300, (run/60.0) % 1, val=f"00:00:{int(run):02d}"); ctx.restore()
    kword(ctx, "TIME SINCE EVERYONE VANISHED", W/2, 120, 60, c('cream'), s.lt, s.at(0.1))
    for i, (w_, f, x, y) in enumerate((("WHAT DISAPPEARS FIRST", 0.12, 330, 420), ("WHAT YOU CAN SAVE", 0.32, 1590, 420), ("A WHOLE WORLD", 0.55, 330, 700), ("ALL TO YOURSELF", 0.62, 1590, 700))):
        if s.lt > s.at(f): bword(ctx, w_, x, y, 46, c('yellow') if i >= 2 else c('cream'), s.lt, s.at(f))
    if s.lt > s.at(0.85): stamp(ctx, "START", W/2, H-90, 80, c('hivis'), s.lt, s.at(0.85))

def sc_title_card(ctx, s):
    ctx.set_source_rgb(0.04, 0.05, 0.10); ctx.paint(); stars(ctx, 260, alpha=0.8)
    skyline(ctx, s.lt*6, 1080, 200, 520, (0.07, 0.09, 0.16, 1), lit=0, seed=4)
    z = 1+0.05*s.lt
    ctx.save(); ctx.translate(W/2, H/2); ctx.scale(z, z); ctx.translate(-W/2, -H/2)
    kword(ctx, "WHAT IF", W/2, 330, 80, c('grey'), s.lt, 0.1)
    kword(ctx, "EVERYONE VANISHED", W/2, 470, 150, c('cream'), s.lt, 0.35)
    kword(ctx, "...EXCEPT YOU?", W/2, 640, 120, c('hivis'), s.lt, 0.9)
    ctx.restore()

def sc_autopilot_words(ctx, s):
    sky(ctx, 'day'); ctx.save(); push(ctx, s, 1.0, 1.12)
    skyline(ctx, s.lt*30, 900, 200, 600, (0.42, 0.52, 0.62, 1), lit=0, seed=5); ground(ctx, 900, (0.3, 0.33, 0.4, 1)); ctx.restore()
    ctx.rectangle(0, 0, W, H); ctx.set_source_rgba(0.04, 0.05, 0.12, 0.45); ctx.fill()
    words_seq(ctx, s, ["THE", "WORLD", "DOESN'T", "STOP"], 420, 110, f0=0.15, f1=0.5)
    bword(ctx, "IT RUNS ON AUTOPILOT", W/2, 640, 90, c('hivis'), s.lt, s.at(0.65))

def traffic_light(ctx, x, y, t):
    paper(ctx, lambda k: rrect(k, x-50, y, 100, 270, 20), (0.12, 0.13, 0.16, 1))
    ph = int(t/1.2) % 3
    for i, col in enumerate(((1, 0.2, 0.2), (1, 0.8, 0.2), (0.2, 0.9, 0.4))):
        on = (2-i) == ph
        ctx.arc(x, y+50+i*85, 32, 0, 2*math.pi); ctx.set_source_rgba(*col, 1 if on else 0.18); ctx.fill()
    ctx.rectangle(x-8, y+270, 16, 400); ctx.set_source_rgba(0.12, 0.13, 0.16, 1); ctx.fill()

def sc_machines_triptych(ctx, s):
    ctx.set_source_rgb(0.08, 0.10, 0.18); ctx.paint()
    pw = W/3
    for i in range(3):
        p = ease(s.pr(i*0.3, i*0.3+0.08))
        if p <= 0: continue
        ctx.save(); ctx.rectangle(i*pw+8, 8, pw-16, H-16); ctx.clip()
        ctx.translate(0, (1-p)*H)
        if i == 0:
            sky(ctx, 'day'); ground(ctx, 900, (0.25, 0.27, 0.32, 1)); traffic_light(ctx, pw/2, 230, s.T)
            text(ctx, "for nobody", pw/2, 990, 46, c('cream'))
        elif i == 1:
            ctx.rectangle(pw, 0, pw, H); ctx.set_source_rgba(0.85, 0.84, 0.80, 1); ctx.fill()
            ctx.save(); ctx.translate(pw*1.5, H/2); ctx.rotate(-0.55)
            for k in range(-10, 10):
                yy = ((k*60 + s.T*80) % 1200) - 600
                ctx.rectangle(-180, yy, 360, 50); ctx.set_source_rgba(0.45, 0.47, 0.52, 1); ctx.fill()
            ctx.rectangle(-210, -700, 30, 1400); ctx.rectangle(180, -700, 30, 1400); ctx.set_source_rgba(0.15, 0.15, 0.18, 1); ctx.fill()
            ctx.restore()
        else:
            ctx.rectangle(2*pw, 0, pw, H); ctx.set_source_rgba(0.93, 0.90, 0.84, 1); ctx.fill()
            paper(ctx, lambda k: rrect(k, 2*pw+90, 360, pw-180, 440, 20), (0.80, 0.82, 0.86, 1))
            rrect(ctx, 2*pw+130, 400, pw-260, 80, 10); ctx.set_source_rgba(0.1, 0.1, 0.14, 1); ctx.fill()
            done = s.lt > s.at(0.85)
            text(ctx, "DONE" if done else "0:0%d" % (9-int(s.lt) % 9), 2*pw+pw/2, 440, 50, (0.3, 1, 0.5, 1) if (not done or int(s.T*4) % 2) else (0.3, 1, 0.5, 0.2))
            if done: stamp(ctx, "BEEP!", 2*pw+pw/2, 300, 60, c('red'), s.lt, s.at(0.86))
        ctx.restore()

def sc_fuel_servers(ctx, s):
    ctx.set_source_rgb(0.07, 0.09, 0.16); ctx.paint()
    ctx.save(); push(ctx, s, 1.05, 1.0)
    pgauge(ctx, 520, H/2, 260, 100*(1-ease(s.pr(0.0, 0.35))))
    text(ctx, "FUEL", 520, H/2+300, 50, c('grey'))
    for r in range(3):  # server racks
        x = 1050+r*260
        paper(ctx, lambda k, x=x: rrect(k, x, 200, 220, 700, 14), (0.14, 0.16, 0.22, 1))
        for j in range(16):
            for l in range(4):
                on = (math.sin(s.T*7 + r*3 + j*1.7 + l*2.3) > 0.2)
                ctx.rectangle(x+30+l*45, 230+j*42, 22, 10); ctx.set_source_rgba(*((0.3, 1, 0.6) if l % 2 else (0.3, 0.7, 1)), 1 if on else 0.15); ctx.fill()
    ctx.restore()
    bword(ctx, "STILL WORKING...", W/2, 110, 80, c('cream'), s.lt, s.at(0.7))
    kword(ctx, "FOR NOW", W/2, H-110, 100, c('hivis'), s.lt, s.at(0.88))

def sc_assumption(ctx, s):
    ctx.set_source_rgb(0.10, 0.06, 0.08); ctx.paint()
    blink = (math.sin(s.T*6) > 0)
    g = cairo.RadialGradient(W/2, H/2, 10, W/2, H/2, 900); g.add_color_stop_rgba(0, 1, 0.2, 0.2, 0.25 if blink else 0.08); g.add_color_stop_rgba(1, 0, 0, 0, 0)
    ctx.set_source(g); ctx.paint()
    ctx.save(); push(ctx, s, 1.0, 1.1, sh=1.2)
    kword(ctx, "ONE HIDDEN ASSUMPTION:", W/2, 230, 70, c('grey'), s.lt, s.at(0.12))
    words_seq(ctx, s, ["A PERSON", "WILL", "CHECK", "ON IT."], 420, 110, col=c('cream'), f0=0.3, f1=0.5)
    for i, w_ in enumerate(["REFUELS", "RESETS", "NOTICES"]):
        bword(ctx, w_, W/2-560+i*560, 700, 70, c('yellow'), s.lt, s.at(0.62+i*0.11))
    ctx.restore()
    ctx.arc(W/2, 900, 50, 0, 2*math.pi); ctx.set_source_rgba(1, 0.2, 0.2, 1 if blink else 0.25); ctx.fill()

def sc_machines_off(ctx, s):
    ctx.set_source_rgb(0.05, 0.06, 0.11); ctx.paint()
    icons = 24; cols = 8
    for i in range(icons):
        x = 260 + (i % cols)*200; y = 230 + (i//cols)*200
        off = s.lt > s.at(0.25 + 0.5*i/icons)
        rrect(ctx, x-70, y-70, 140, 140, 22); ctx.set_source_rgba(0.12, 0.15, 0.24, 1); ctx.fill()
        ctx.arc(x, y, 30, 0, 2*math.pi); ctx.set_source_rgba(*((0.25, 0.25, 0.3) if off else (1, 0.85, 0.4)), 1); ctx.fill()
    kword(ctx, "NOBODY IS COMING", W/2, 860, 110, c('cream'), s.lt, s.at(0.05))
    if s.lt > s.at(0.82): stamp(ctx, "THE BIGGEST ONE GOES FIRST", W/2, 990, 60, c('red'), s.lt, s.at(0.82))

def plant(ctx, x, y, s_=1.0, smoke_t=0.0, smoke=True):
    ctx.save(); ctx.translate(x, y); ctx.scale(s_, s_)
    paper(ctx, lambda k: k.rectangle(-300, -260, 600, 260), (0.40, 0.44, 0.52, 1))
    for cx_ in (-200, 200):
        paper(ctx, lambda k, cx_=cx_: (k.new_path(), k.move_to(cx_-30, -260), k.line_to(cx_-22, -620), k.line_to(cx_+22, -620), k.line_to(cx_+30, -260), k.close_path()), (0.50, 0.53, 0.60, 1), off=(4, 5))
        ctx.rectangle(cx_-24, -600, 48, 18); ctx.set_source_rgba(*c('red')); ctx.fill()
        if smoke:
            for i in range(6):
                q = (smoke_t*0.3 + i/6) % 1
                ctx.arc(cx_+q*160, -630-q*300, 30+q*80, 0, 2*math.pi); ctx.set_source_rgba(0.85, 0.85, 0.88, 0.5*(1-q)); ctx.fill()
    for i in range(8):
        ctx.rectangle(-270+i*70, -200, 40, 50); ctx.set_source_rgba(1, 0.85, 0.45, 0.9); ctx.fill()
    ctx.restore()

def sc_plant_exterior(ctx, s):
    sky(ctx, 'dusk'); ctx.save(); push(ctx, s, 1.25, 1.0, W/2, 800)
    skyline(ctx, 0, 880, 80, 200, (0.33, 0.22, 0.40, 1), lit=0, seed=12); ground(ctx, 880, (0.20, 0.17, 0.26, 1))
    plant(ctx, W/2, 900, 1.0, s.T)
    ctx.restore()
    bword(ctx, "THE BIGGEST BABYSITTING JOB", W/2, H-140, 70, c('cream'), s.lt, s.at(0.3))

def sc_control_room(ctx, s):
    ctx.set_source_rgb(0.10, 0.12, 0.17); ctx.paint()
    ctx.save(); push(ctx, s, 1.0, 1.25, W/2, H*0.45, sh=1.0)
    for i in range(5):
        x = 150+i*340; paper(ctx, lambda k, x=x: rrect(k, x, 150, 300, 330, 14), (0.16, 0.20, 0.28, 1))
        for j in range(3):
            on = math.sin(s.T*(3+i)+j) > 0
            ctx.arc(x+60+j*90, 420, 16, 0, 2*math.pi); ctx.set_source_rgba(*((1, 0.25, 0.25) if (on and s.lt > s.at(0.6)) else (0.3, 0.9, 0.5)), 1); ctx.fill()
    hz = 60.0 - 1.3*ease(s.pr(0.45, 0.95)) + 0.02*math.sin(s.T*9)
    paper(ctx, lambda k: rrect(k, W/2-330, 520, 660, 220, 20), c('ink'))
    text(ctx, f"{hz:.2f} Hz", W/2, 630, 120, (1, 0.3, 0.3, 1) if hz < 59.5 else (0.3, 1, 0.5, 1))
    paper(ctx, lambda k: rrect(k, 120, 840, W-240, 120, 20), (0.25, 0.27, 0.32, 1))  # desk
    for i in range(4):  # empty chairs
        x = 360+i*400; paper(ctx, lambda k, x=x: rrect(k, x-60, 760, 120, 150, 30), (0.20, 0.22, 0.28, 1))
    ctx.restore()
    bword(ctx, "EMPTY CHAIRS", W/2, 800, 60, c('cream'), s.lt, s.at(0.15))
    if s.lt > s.at(0.82): stamp(ctx, "SAFETY CUT-OFF", W/2, H-110, 80, c('red'), s.lt, s.at(0.82))

def sc_grid_map(ctx, s):
    ctx.set_source_rgb(0.03, 0.04, 0.09); ctx.paint()
    rng = np.random.default_rng(11)
    ctx.save(); push(ctx, s, 1.0, 1.1, rot0=-0.03, rot1=0.03)
    # abstract continent
    ctx.move_to(250, 400); ctx.curve_to(500, 150, 1300, 120, 1650, 330); ctx.curve_to(1800, 600, 1500, 900, 1100, 880)
    ctx.curve_to(700, 950, 300, 800, 250, 400); ctx.close_path(); ctx.set_source_rgba(0.08, 0.11, 0.2, 1); ctx.fill()
    for i in range(420):
        x, y = rng.uniform(320, 1650), rng.uniform(230, 850)
        out_t = s.at(0.05 + 0.8*((x-320)/1330)*0.7 + rng.uniform(0, 0.25))
        a = 1 - prog(s.lt, out_t, out_t+0.3)
        if a > 0:
            r = rng.uniform(2, 7); ctx.arc(x, y, r, 0, 2*math.pi); ctx.set_source_rgba(1, 0.85, 0.45, a); ctx.fill()
        else: rng.uniform(2, 7)
    ctx.restore()
    bword(ctx, "HOURS TO A COUPLE OF DAYS", W/2, H-110, 72, c('cream'), s.lt, s.at(0.62))

def sc_solar_house(ctx, s):
    sky(ctx, 'night'); stars(ctx, 120, alpha=0.6)
    focus = ease(s.pr(0.35, 0.65))
    ctx.save(); z = 1.0+1.0*focus; ctx.translate(W/2, H*0.7); ctx.scale(z, z); ctx.translate(-W/2-(1180-W/2)*focus, -H*0.7)
    skyline(ctx, 0, 820, 200, 520, (0.07, 0.09, 0.16, 1), lit=0.0, seed=21)
    ground(ctx, 820, (0.05, 0.06, 0.10, 1))
    for i, x in enumerate((300, 700, 1050, 1450)):
        house(ctx, x, 900, 300, 200, body=(0.20, 0.22, 0.30, 1), roof=(0.14, 0.15, 0.22, 1), lit=(x == 1050), solar=(x == 1050), glow=(0.9 if x == 1050 else 0))
    ctx.restore()
    if s.lt > s.at(0.15):
        bword(ctx, "HYDRO DAMS: A WHILE", 420, 180, 50, c('cream'), s.lt, s.at(0.12))
    bword(ctx, "SOLAR + BATTERY: YEARS", W-420, 180, 50, c('yellow'), s.lt, s.at(0.3))
    if s.lt > s.at(0.82): stamp(ctx, "REMEMBER THIS HOUSE", W/2, H-120, 76, c('hivis'), s.lt, s.at(0.82))

def sc_nuclear(ctx, s):
    sky(ctx, 'gray'); ctx.save(); push(ctx, s, 1.0, 1.15, sh=0.8)
    ground(ctx, 860, (0.40, 0.45, 0.42, 1))
    for x in (650, 1050):
        paper(ctx, lambda k, x=x: (k.new_path(), k.move_to(x-180, 860), k.curve_to(x-110, 600, x-110, 500, x-140, 300), k.line_to(x+140, 300), k.curve_to(x+110, 500, x+110, 600, x+180, 860), k.close_path()), (0.78, 0.78, 0.76, 1))
    steam = 1-ease(s.pr(0.0, 0.3))
    for i in range(8):
        q = (s.T*0.25+i/8) % 1
        for x in (650, 1050):
            ctx.arc(x+q*120, 280-q*260, 50+q*60, 0, 2*math.pi); ctx.set_source_rgba(1, 1, 1, 0.5*(1-q)*steam); ctx.fill()
    ctx.restore()
    if s.lt > s.at(0.12): stamp(ctx, "AUTO SHUTDOWN", 1500, 300, 64, c('red'), s.lt, s.at(0.12))
    pgauge(ctx, 1550, 680, 140, 100*(1-ease(s.pr(0.35, 0.7)))); text(ctx, "BACKUP FUEL", 1550, 860, 34, c('ink'))
    if s.lt > s.at(0.8):
        p = s.pr(0.8, 1.0); x = -300 + p*(W+600)
        car(ctx, x, 1000, 0.9, wheel=-s.T*20, beam=False)
        rrect(ctx, x-100, 840, 160, 40, 8); ctx.set_source_rgba(0.6, 0.3, 0.2, 1); ctx.fill()
        bword(ctx, "ROAD TRIP?", W/2, 120, 80, c('cream'), s.lt, s.at(0.82))

def sc_milky_way(ctx, s):
    ctx.set_source_rgb(0.02, 0.03, 0.08); ctx.paint()
    a = ease(s.pr(0.35, 0.8))
    tilt = 220*ease(s.pr(0.2, 0.9))
    ctx.save(); ctx.translate(0, tilt)
    stars(ctx, 400, alpha=0.3+0.7*a, y1=H*1.0); milky_way(ctx, a)
    ctx.restore()
    ctx.save(); ctx.translate(0, tilt*1.6)
    lit_frac = 1 - ease(s.pr(0.0, 0.3))
    skyline(ctx, 0, 1080, 260, 640, (0.04, 0.05, 0.10, 1), lit=0.4*lit_frac, seed=31)
    ctx.restore()
    bword(ctx, "THE MILKY WAY. DOWNTOWN.", W/2, 120, 70, c('cream'), s.lt, s.at(0.45))

def door_scene(ctx, s, open_p=0.0, scratch=True):
    ctx.set_source_rgb(0.06, 0.06, 0.09); ctx.paint()
    paper(ctx, lambda k: k.rectangle(W/2-260, 120, 520, 860), (0.30, 0.20, 0.15, 1))
    if open_p > 0:
        ctx.rectangle(W/2-260, 120, 520*open_p, 860); ctx.set_source_rgba(0.01, 0.01, 0.02, 1); ctx.fill()
    ctx.save(); ctx.translate(W/2-260+520*open_p, 0)
    if open_p < 1:
        ctx.rectangle(0, 120, 520*(1-open_p), 860); ctx.set_source_rgba(0.42, 0.28, 0.20, 1); ctx.fill()
        ctx.arc(520*(1-open_p)-60, 560, 18, 0, 2*math.pi); ctx.set_source_rgba(0.8, 0.7, 0.4, 1); ctx.fill()
    ctx.restore()
    # light under the door with shadows moving
    if open_p == 0:
        ctx.rectangle(W/2-260, 975, 520, 8); ctx.set_source_rgba(0.9, 0.8, 0.6, 0.6); ctx.fill()
        if scratch:
            for i in range(2):
                x = W/2 - 100 + 120*math.sin(s.T*2+i*2)
                ctx.rectangle(x, 975, 60, 8); ctx.set_source_rgba(0, 0, 0, 0.9); ctx.fill()

def sc_door_scratch(ctx, s):
    ctx.save(); sh = shake(s.T, 6 if (s.lt > s.at(0.15) and int(s.T*5) % 2) else 0.5)
    z = 1.0+0.25*ease(s.pr(0, 1)); ctx.translate(W/2+sh[0], H/2+sh[1]); ctx.scale(z, z); ctx.translate(-W/2, -H/2)
    door_scene(ctx, s); ctx.restore()
    for i, t0 in enumerate((0.15, 0.25, 0.33)):
        if s.lt > s.at(t0):
            ctx.save(); ctx.translate(W/2+(-380, 380, -340)[i], 300+i*180); ctx.rotate((-0.2, 0.15, -0.1)[i])
            kword(ctx, "SCRATCH", 0, 0, 70, c('cream'), s.lt, s.at(t0)); ctx.restore()
    if s.lt > s.at(0.75): stamp(ctx, "IT FOUND YOU", W/2, H-90, 80, c('red'), s.lt, s.at(0.75))

def sc_door_open(ctx, s):
    ctx.save(); z = 1.0+0.35*ease(s.pr(0, 1)); ctx.translate(W/2, H/2); ctx.scale(z, z); ctx.translate(-W/2, -H/2)
    door_scene(ctx, s, open_p=0.35*ease(s.pr(0.0, 0.6)), scratch=False)
    if s.lt > s.at(0.6): eyes_pair(ctx, W/2-200, 640, 1.4, a=ease(s.pr(0.6, 0.9)))
    ctx.restore()

def scruffy_dog_face(ctx, x, y, s_, t, tongue=True):
    ctx.save(); ctx.translate(x, y); ctx.scale(s_, s_); ctx.rotate(0.06*math.sin(t*3))
    for sx in (-1, 1):
        ctx.save(); ctx.translate(sx*150, -60); ctx.rotate(sx*(0.4+0.1*math.sin(t*4))); ctx.scale(0.55, 1.1)
        ctx.arc(0, 60, 80, 0, 2*math.pi); ctx.restore(); ctx.set_source_rgba(0.45, 0.32, 0.22, 1); ctx.fill()
    paper(ctx, lambda k: (k.new_path(), k.arc(0, 0, 190, 0, 2*math.pi)), (0.78, 0.60, 0.40, 1))
    for i in range(14):  # scruff
        a = -math.pi*0.9 + i*0.13
        ctx.move_to(185*math.cos(a), 185*math.sin(a)); ctx.line_to(230*math.cos(a+0.05), 230*math.sin(a+0.05)); ctx.line_to(185*math.cos(a+0.1), 185*math.sin(a+0.1))
        ctx.set_source_rgba(0.78, 0.60, 0.40, 1); ctx.fill()
    ctx.save(); ctx.translate(0, 70); ctx.scale(1.2, 0.8); ctx.arc(0, 0, 90, 0, 2*math.pi); ctx.restore(); ctx.set_source_rgba(0.93, 0.85, 0.72, 1); ctx.fill()
    for sx in (-1, 1):
        ctx.arc(sx*70, -30, 26, 0, 2*math.pi); ctx.set_source_rgba(0.1, 0.08, 0.07, 1); ctx.fill()
        ctx.arc(sx*70+8, -38, 8, 0, 2*math.pi); ctx.set_source_rgba(1, 1, 1, 1); ctx.fill()
    ctx.save(); ctx.translate(0, 40); ctx.scale(1.3, 1); ctx.arc(0, 0, 30, 0, 2*math.pi); ctx.restore(); ctx.set_source_rgba(0.1, 0.08, 0.07, 1); ctx.fill()
    if tongue:
        rrect(ctx, -28, 110, 56, 80+10*math.sin(t*8), 28); ctx.set_source_rgba(0.95, 0.45, 0.5, 1); ctx.fill()
    ctx.restore()

def sc_dog_reveal(ctx, s):
    ctx.set_source_rgb(0.95, 0.72, 0.40); ctx.paint()
    ctx.save(); ctx.translate(W/2, H/2); ctx.rotate(s.lt*0.4)
    for i in range(16):
        ctx.move_to(0, 0); ctx.arc(0, 0, 1600, i*math.pi/8, i*math.pi/8+math.pi/16); ctx.close_path()
    ctx.set_source_rgba(1, 1, 1, 0.15); ctx.fill(); ctx.restore()
    p = back(s.pr(0.0, 0.08))
    scruffy_dog_face(ctx, W/2 if s.lt < s.at(0.4) else W/2-500*ease(s.pr(0.4, 0.5)), H/2+60, 1.6*p if s.lt < s.at(0.4) else 1.6-0.6*ease(s.pr(0.4, 0.5)), s.T)
    if s.lt > s.at(0.4):
        ctx.rectangle(0, 0, W, H); ctx.set_source_rgba(0.05, 0.06, 0.12, 0.6*ease(s.pr(0.4, 0.5))); ctx.fill()
        kword(ctx, "EVERY PERSON VANISHED.", W/2+250, 360, 80, c('cream'), s.lt, s.at(0.5))
        kword(ctx, "THE ANIMALS", W/2+250, 560, 130, c('hivis'), s.lt, s.at(0.78))
        kword(ctx, "DIDN'T.", W/2+250, 720, 150, c('hivis'), s.lt, s.at(0.84))
        ctx.rectangle(0, 0, W, H); ctx.set_source_rgba(1, 1, 1, 0.45*(1-prog(s.lt, s.at(0.78), s.at(0.78)+0.25)) if s.lt > s.at(0.78) else 0); ctx.fill()

def sc_dog_windows(ctx, s):
    ctx.set_source_rgb(0.85, 0.80, 0.72); ctx.paint()
    ctx.save(); push(ctx, s, 1.3, 0.9, W/2, H/2)
    for i in range(-3, 13):
        for j in range(-2, 7):
            x, y = i*180, j*190
            ctx.rectangle(x, y, 130, 140); ctx.set_source_rgba(0.20, 0.24, 0.34, 1); ctx.fill()
            if (i*7+j*3) % 3 == 0:
                q = (i+j) % 3
                ctx.save(); ctx.translate(x+65, y+140)
                if q == 2:
                    ctx.arc(0, -40, 34, 0, 2*math.pi); ctx.set_source_rgba(0.30, 0.30, 0.34, 1); ctx.fill()
                    ctx.move_to(-28, -60); ctx.line_to(-18, -92); ctx.line_to(-4, -66); ctx.move_to(28, -60); ctx.line_to(18, -92); ctx.line_to(4, -66); ctx.fill()
                else:
                    scruffy_dog_face(ctx, 0, -45, 0.2, s.T+i, tongue=False)
                ctx.restore()
    ctx.restore()
    p = s.pr(0.1, 0.45); val = int(1_000_000_000*ease(p))
    ctx.rectangle(0, H/2-150, W, 300); ctx.set_source_rgba(0.04, 0.05, 0.12, 0.8); ctx.fill()
    text_paper(ctx, f"~{val:,}", W/2, H/2-30, 140, c('cream')); kword(ctx, "DOGS ON EARTH", W/2, H/2+90, 50, c('yellow'), s.lt, s.at(0.1))
    if s.lt > s.at(0.72): bword(ctx, "WAITING FOR SOMEONE TO COME BACK", W/2, H-90, 56, c('cream'), s.lt, s.at(0.72))

def sc_open_doors(ctx, s):
    sky(ctx, 'day'); ctx.save(); pan = 900*ease(s.pr(0.0, 0.7)); push(ctx, s, 1.0, 1.05)
    ctx.translate(-pan, 0); ground(ctx, 900, (0.55, 0.70, 0.45, 1))
    for i in range(7):
        x = 100+i*420; house(ctx, x, 900, 330, 230, body=((0.93, 0.86, 0.74, 1), (0.80, 0.86, 0.90, 1), (0.95, 0.80, 0.70, 1))[i % 3])
        t0 = 0.05+i*0.08; p = ease(s.pr(t0, t0+0.12))
        if p > 0:
            ctx.rectangle(x+135, 790, 60, 110); ctx.set_source_rgba(0.05, 0.05, 0.08, 1); ctx.fill()
            quad(ctx, x+165+p*500, 960, 'dog' if i % 3 else 'cat', 0.7, phase=s.T*10+i, run=1)
    ctx.restore()
    if s.lt > s.at(0.55): bword(ctx, "JOB #1: OPEN DOORS", W/2, 130, 90, c('hivis'), s.lt, s.at(0.55))
    if s.lt > s.at(0.8): bword(ctx, "YOU'RE THE ONLY ONE WITH THUMBS", W/2, H-100, 56, c('cream'), s.lt, s.at(0.8))

def sc_cat_king(ctx, s):
    sky(ctx, 'dusk'); ctx.save(); push(ctx, s, 1.0, 1.35, W/2, 620)
    skyline(ctx, 0, 860, 100, 300, (0.33, 0.22, 0.40, 1), lit=0, seed=41)
    ctx.rectangle(0, 700, W, 40); ctx.set_source_rgba(0.55, 0.40, 0.30, 1); ctx.fill()
    for i in range(30): ctx.rectangle(i*70, 700, 12, 380); ctx.set_source_rgba(0.50, 0.36, 0.27, 1); ctx.fill()
    quad(ctx, W/2, 700, 'cat', 1.6, phase=0.3, run=0.0)
    if s.lt > s.at(0.6):
        p = back(s.pr(0.6, 0.72)); ctx.save(); ctx.translate(W/2+170, 470-300*(1-p)); ctx.rotate(0.15)
        ctx.move_to(-50, 0); ctx.line_to(-50, -50); ctx.line_to(-25, -25); ctx.line_to(0, -60); ctx.line_to(25, -25); ctx.line_to(50, -50); ctx.line_to(50, 0); ctx.close_path()
        ctx.set_source_rgba(*c('yellow')); ctx.fill(); ctx.restore()
    ctx.restore()
    bword(ctx, "CATS: FINE", W/2, 130, 100, c('cream'), s.lt, s.at(0.05))
    if s.lt > s.at(0.65): bword(ctx, "RUNS THE WHOLE BLOCK", W/2, H-110, 70, c('yellow'), s.lt, s.at(0.65))

def sc_garage_pack(ctx, s):
    ctx.set_source_rgb(0.05, 0.05, 0.07); ctx.paint()
    ctx.save(); push(ctx, s, 1.0, 1.3, W/2, H/2+80, sh=1.5)
    for i in range(6):  # pillars in perspective
        x = 200+i*320; ctx.rectangle(x, 160, 70, 760); ctx.set_source_rgba(0.12, 0.12, 0.15, 1); ctx.fill()
    ctx.rectangle(0, 900, W, 200); ctx.set_source_rgba(0.09, 0.09, 0.11, 1); ctx.fill()
    for i in range(7):
        t0 = s.at(0.25+i*0.06); a = ease(prog(s.lt, t0, t0+0.3))
        if a > 0 and not (int(s.T*3+i) % 9 == 0): eyes_pair(ctx, 400+i*190 + 40*math.sin(i), 650 + (i % 3)*60, 1.0+0.2*(i % 2), a=a)
    if s.lt > s.at(0.55):
        for i in range(4):
            quad(ctx, 500+i*300, 900, 'dog', 0.9, phase=s.T*3+i, run=0.2, face=-1 if i % 2 else 1, sil=(0.02, 0.02, 0.03, 1), alpha=ease(s.pr(0.55, 0.7)))
    ctx.restore()
    bword(ctx, "LOOSE PACKS", W/2, 120, 90, c('cream'), s.lt, s.at(0.15))
    if s.lt > s.at(0.7): bword(ctx, "NOT IN A PARKING GARAGE", W/2, H-100, 62, c('red'), s.lt, s.at(0.7))

def sc_dog_lineup(ctx, s):
    ctx.set_source_rgb(0.92, 0.88, 0.80); ctx.paint()
    ground(ctx, 820, (0.80, 0.75, 0.66, 1))
    sizes = [0.35, 0.45, 0.75, 1.0, 1.3]
    for i, sz in enumerate(sizes):
        x = 250+i*360; gone = (i < 2) and s.lt > s.at(0.15+i*0.1)
        a = 1-ease(prog(s.lt, s.at(0.15+i*0.1), s.at(0.25+i*0.1))) if i < 2 else 1
        if a > 0: quad(ctx, x, 820, 'dog', sz, phase=s.T*2+i, run=0.1, alpha=a)
    if s.lt > s.at(0.75):
        g = cairo.RadialGradient(250+3*360, 600, 10, 250+3*360, 600, 380); g.add_color_stop_rgba(0, 1, 0.95, 0.6, 0.6); g.add_color_stop_rgba(1, 1, 0.95, 0.6, 0)
        ctx.set_source(g); ctx.paint()
        stamp(ctx, "SCRUFFY MUTT WINS", W/2, 140, 80, c('red'), s.lt, s.at(0.8))
    bword(ctx, "MEDIUM. CLEVER. NOT PICKY.", W/2, H-110, 62, c('cream'), s.lt, s.at(0.45))

def sc_barn_stats(ctx, s):
    sky(ctx, 'day'); ctx.save(); push(ctx, s, 1.0, 1.12)
    ground(ctx, 820, (0.55, 0.70, 0.40, 1))
    paper(ctx, lambda k: k.rectangle(300, 420, 700, 400), (0.70, 0.22, 0.20, 1))
    paper(ctx, lambda k: (k.new_path(), k.move_to(260, 420), k.line_to(650, 220), k.line_to(1040, 420), k.close_path()), (0.45, 0.15, 0.15, 1))
    ctx.rectangle(560, 560, 180, 260); ctx.set_source_rgba(0.95, 0.92, 0.85, 1); ctx.fill()
    for i in range(6): chicken(ctx, 1150+i*110, 860+(i % 2)*30, 0.9)
    quad(ctx, 1500, 800, 'cow', 1.0, phase=0.2)
    ctx.restore()
    p1 = ease(s.pr(0.18, 0.45)); p2 = ease(s.pr(0.45, 0.65))
    ctx.rectangle(0, 0, W, 300); ctx.set_source_rgba(0.04, 0.05, 0.12, 0.75); ctx.fill()
    text_paper(ctx, f"{int(20_000_000_000*p1):,}", W*0.3, 110, 80, c('cream')); text(ctx, "CHICKENS", W*0.3, 210, 40, c('yellow'))
    text_paper(ctx, f"{int(1_500_000_000*p2):,}", W*0.72, 110, 80, c('cream')); text(ctx, "CATTLE", W*0.72, 210, 40, c('yellow'))
    if s.lt > s.at(0.75): bword(ctx, "BUILT AROUND A HUMAN SCHEDULE", W/2, H-100, 60, c('cream'), s.lt, s.at(0.75))

def sc_pig_escape(ctx, s):
    sky(ctx, 'day'); tb = s.at(0.12)
    ctx.save(); sh = shake(s.T, 12*(1-prog(s.lt, tb, tb+0.5)) if s.lt > tb else 1)
    ctx.translate(sh[0], sh[1])
    off = max(0, s.lt-tb)*900
    ground(ctx, 800, (0.55, 0.72, 0.42, 1))
    for i in range(-2, 12):
        tree(ctx, i*300 - (off*0.4) % 300, 800, 0.9)
    for i in range(30):  # fence
        x = 200 + i*60 - off
        broken = 3 < i < 7 and s.lt > tb
        if not broken:
            ctx.rectangle(x, 760, 14, 120); ctx.set_source_rgba(0.55, 0.40, 0.28, 1); ctx.fill()
    ctx.rectangle(-W, 790, 600+W - off*(1 if s.lt > tb else 0), 12); ctx.set_source_rgba(0.55, 0.40, 0.28, 1); ctx.fill()
    px = 300 + 500*ease(prog(s.lt, 0, tb)) if s.lt < tb else 800
    quad(ctx, px, 960, 'pig', 1.2, phase=s.T*12, run=1.0)
    if s.lt > tb: speedlines(ctx, s.T, a=0.25)
    ctx.restore()
    if s.lt > tb: stamp(ctx, "BREAKOUT", W/2, 160, 100, c('red'), s.lt, tb)
    if s.lt > s.at(0.4): bword(ctx, "ONE OF THE MOST SUCCESSFUL INVADERS ON EARTH", W/2, H-90, 48, c('cream'), s.lt, s.at(0.4))

def sc_zoo_gate(ctx, s):
    ctx.save()
    if s.lt < s.at(0.72):
        sky(ctx, 'night'); stars(ctx, 120, alpha=0.5); push(ctx, s, 1.0, 1.25, W/2, 600)
        ground(ctx, 820, (0.12, 0.16, 0.14, 1))
        for i in range(12): ctx.rectangle(200+i*130, 420, 14, 420); ctx.set_source_rgba(0.35, 0.36, 0.40, 1); ctx.fill()
        powered = s.lt < s.at(0.45)
        for yy in (480, 580, 680):
            ctx.move_to(200, yy); ctx.line_to(1650, yy); ctx.set_line_width(4)
            ctx.set_source_rgba(*((0.5, 0.85, 1) if powered and int(s.T*10) % 2 else (0.3, 0.3, 0.35)), 1); ctx.stroke()
        if powered and int(s.T*6) % 3 == 0:
            x = 300+((s.T*700) % 1300); ctx.arc(x, 580, 14, 0, 2*math.pi); ctx.set_source_rgba(0.8, 0.95, 1, 0.9); ctx.fill()
        rrect(ctx, 760, 260, 400, 110, 14); ctx.set_source_rgba(0.25, 0.27, 0.30, 1); ctx.fill(); text(ctx, "ZOO", 960, 315, 70, c('cream'))
        if s.lt > s.at(0.45): stamp(ctx, "POWER: OFF", 1500, 250, 60, c('red'), s.lt, s.at(0.45))
        eyes_pair(ctx, 900, 700, 1.0, a=ease(s.pr(0.5, 0.65)))
    else:
        sky(ctx, 'dawn'); p = s.pr(0.72, 1.0)
        skyline(ctx, p*200, 760, 150, 400, (0.70, 0.60, 0.60, 1), lit=0, seed=51)
        ground(ctx, 760, (0.6, 0.6, 0.62, 1)); road(ctx, 820, 220, dash_off=0)
        quad(ctx, -200+p*1300, 980, 'zebra', 1.0, phase=s.T*7, run=0.6)
        bword(ctx, "...DOESN'T ANYMORE.", W/2, 140, 80, c('ink'), s.lt, s.at(0.74), box=(1, 1, 1, 0.75))
    ctx.restore()
    if s.lt < s.at(0.4): bword(ctx, "A MOAT IS STILL A MOAT", W/2, H-100, 62, c('cream'), s.lt, s.at(0.15))

def sc_cart_highway(ctx, s):
    sky(ctx, 'day'); ctx.save(); push(ctx, s, 1.0, 1.15, W/2, 850)
    off = s.lt*120
    skyline(ctx, off*0.3, 760, 150, 460, (0.55, 0.62, 0.70, 1), lit=0, seed=61)
    ground(ctx, 760, (0.6, 0.6, 0.62, 1)); road(ctx, 820, 220, dash_off=off)
    for i in range(4): car(ctx, 200+i*520 - off*0 , 930 if i % 2 else 1010, 0.9, beam=False)
    x = 700+off*0.0; y = 1000
    you(ctx, x, y, 0.9, phase=s.T*6, run=0.5, reach=1.0)
    paper(ctx, lambda k: rrect(k, x+60, y-200, 200, 130, 10), (0.75, 0.78, 0.82, 1))
    for i in range(5): rrect(ctx, x+75+i*36, y-250, 30, 50, 4); ctx.set_source_rgba(*((c('red'), c('orange'), c('teal'), c('yellow'), c('blue'))[i])); ctx.fill()
    ctx.restore()
    bword(ctx, "EVERYTHING IS FREE.", W/2, 130, 90, c('cream'), s.lt, s.at(0.55))
    if s.lt > s.at(0.78): bword(ctx, "NOTHING WORKS.", W/2, 270, 90, c('red'), s.lt, s.at(0.78))

def sc_water_tower(ctx, s):
    sky(ctx, 'day')
    ctx.save(); push(ctx, s, 1.0, 1.08)
    ground(ctx, 900, (0.55, 0.68, 0.45, 1))
    for x in (480, 580): ctx.move_to(x, 900); ctx.line_to(x+20 if x == 480 else x-20, 520)
    ctx.set_line_width(14); ctx.set_source_rgba(0.40, 0.42, 0.48, 1); ctx.stroke()
    lvl = 1 - 0.85*ease(s.pr(0.2, 0.6))
    paper(ctx, lambda k: rrect(k, 360, 220, 340, 300, 40), (0.70, 0.74, 0.80, 1))
    ctx.save(); rrect(ctx, 380, 240, 300, 260, 30); ctx.clip()
    ctx.rectangle(380, 240+260*(1-lvl), 300, 260*lvl); ctx.set_source_rgba(0.25, 0.55, 0.85, 1); ctx.fill(); ctx.restore()
    text(ctx, "PRESSURE", 530, 580, 40, c('ink'))
    # bathtub filling
    fill = ease(s.pr(0.65, 0.95))
    paper(ctx, lambda k: rrect(k, 1050, 640, 600, 220, 60), c('white'))
    ctx.save(); rrect(ctx, 1070, 660, 560, 180, 50); ctx.clip()
    ctx.rectangle(1070, 660+180*(1-fill), 560, 180*fill); ctx.set_source_rgba(0.35, 0.65, 0.95, 1); ctx.fill(); ctx.restore()
    ctx.rectangle(1560, 560, 20, 90); ctx.set_source_rgba(0.6, 0.62, 0.66, 1); ctx.fill()
    if 0 < fill < 1:
        ctx.rectangle(1565, 650, 10, 100); ctx.set_source_rgba(0.35, 0.65, 0.95, 1); ctx.fill()
    ctx.restore()
    if s.lt > s.at(0.3): bword(ctx, "PUMPS NEED POWER", 530, 130, 60, c('cream'), s.lt, s.at(0.3))
    if s.lt > s.at(0.65): bword(ctx, "TIP: FILL EVERY BATHTUB", 1350, 460, 56, c('yellow'), s.lt, s.at(0.65))

def sc_supermarket(ctx, s):
    ctx.set_source_rgb(0.92, 0.92, 0.88); ctx.paint()
    ctx.save(); push(ctx, s, 1.1, 1.0, sh=0.6)
    rot = ease(s.pr(0.05, 0.35))
    for j in range(3):
        y = 260+j*230; ctx.rectangle(80, y+120, 760, 18); ctx.set_source_rgba(0.5, 0.5, 0.55, 1); ctx.fill()
        for i in range(9):
            col = (0.35+0.25*(1-rot), 0.70*(1-rot)+0.35*rot, 0.25+0.2*rot)
            ctx.arc(130+i*80, y+80, 34, 0, 2*math.pi); ctx.set_source_rgba(*col, 1); ctx.fill()
    for j in range(3):
        y = 260+j*230; ctx.rectangle(1080, y+120, 760, 18); ctx.set_source_rgba(0.5, 0.5, 0.55, 1); ctx.fill()
        n = int(9*ease(s.pr(0.4+j*0.08, 0.55+j*0.08)))
        for i in range(n):
            rrect(ctx, 1100+i*80, y+20, 64, 100, 8); ctx.set_source_rgba(*(c('red'), c('teal'), c('orange'))[j]); ctx.fill()
            ctx.rectangle(1100+i*80, y+50, 64, 34); ctx.set_source_rgba(*c('cream')); ctx.fill()
    ctx.restore()
    bword(ctx, "FRESH: 1 WEEK", 460, 180, 64, c('red'), s.lt, s.at(0.05))
    bword(ctx, "CANNED: YEARS", 1460, 180, 64, c('teal'), s.lt, s.at(0.4))
    if s.lt > s.at(0.7):
        p = back(s.pr(0.7, 0.8)); ctx.save(); ctx.translate(W/2, H-200); ctx.scale(p, p)
        paper(ctx, lambda k: rrect(k, -90, -120, 180, 220, 40), (0.95, 0.70, 0.20, 1)); text(ctx, "HONEY", 0, -20, 40, c('ink')); text(ctx, "∞", 0, 50, 70, c('ink'))
        ctx.restore()

def sc_boring_dangers(ctx, s):
    ctx.set_source_rgb(0.10, 0.08, 0.10); ctx.paint()
    kword(ctx, "THE REAL DANGER IS BORING", W/2, 140, 80, c('cream'), s.lt, s.at(0.0))
    items = [("INFECTED CUT", 0.2), ("BAD TOOTH", 0.33), ("A FALL. NOBODY TO CALL.", 0.45)]
    for i, (w_, f) in enumerate(items):
        bword(ctx, w_, W/2, 360+i*170, 80, c('yellow'), s.lt, s.at(f))
    if s.lt > s.at(0.72):
        stamp(ctx, "NO DOCTORS. JUST YOU.", W/2, 920, 80, c('red'), s.lt, s.at(0.72))

def sc_pharmacy_car(ctx, s):
    sky(ctx, 'day'); ctx.save(); push(ctx, s, 1.0, 1.1)
    ground(ctx, 860, (0.6, 0.6, 0.62, 1))
    paper(ctx, lambda k: k.rectangle(1050, 380, 720, 480), (0.95, 0.95, 0.93, 1))
    ctx.rectangle(1050, 380, 720, 100); ctx.set_source_rgba(0.2, 0.6, 0.4, 1); ctx.fill(); text(ctx, "PHARMACY", 1410, 430, 64, c('white'))
    ctx.rectangle(1380, 540, 60, 180); ctx.rectangle(1320, 600, 180, 60); ctx.set_source_rgba(0.2, 0.75, 0.4, 1); ctx.fill()
    car(ctx, 500, 960, 1.25, beam=False)
    ctx.restore()
    if s.lt > s.at(0.15):
        p = ease(s.pr(0.15, 0.25)); ctx.move_to(330, 700); ctx.line_to(330+340*p, 700+260*p); ctx.move_to(670, 700); ctx.line_to(670-340*p, 700+260*p)
        ctx.set_line_width(26); ctx.set_source_rgba(*c('red', 0.9)); ctx.stroke()
        bword(ctx, "NOT FIRST", 500, 620, 60, c('red'), s.lt, s.at(0.15))
    if s.lt > s.at(0.35): bword(ctx, "1. ANTIBIOTICS + FIRST-AID BOOK", 1410, 230, 52, c('cream'), s.lt, s.at(0.35))
    if s.lt > s.at(0.85): bword(ctx, "2. THEN THE SPORTS CAR", 1410, 320, 52, c('yellow'), s.lt, s.at(0.85))

def sc_porch_dog(ctx, s):
    night = s.p.get('night', False)
    sky(ctx, 'night' if night else 'dusk')
    if night: stars(ctx, 300, alpha=0.9); milky_way(ctx, 0.9)
    ctx.save()
    if night:
        z = 1.5-0.6*ease(s.pr(0, 1)); ctx.translate(W/2, H*0.75); ctx.scale(z, z); ctx.translate(-W/2-300*(1-ease(s.pr(0, 1))), -H*0.75)
    else: push(ctx, s, 1.0, 1.15, W/2, 800)
    skyline(ctx, 0, 820, 150, 420, (0.06, 0.08, 0.14, 1) if night else (0.33, 0.22, 0.40, 1), lit=0, seed=71)
    ground(ctx, 820, (0.08, 0.10, 0.12, 1) if night else (0.30, 0.25, 0.30, 1))
    house(ctx, 650, 960, 620, 320, body=(0.40, 0.35, 0.40, 1) if night else (0.85, 0.75, 0.62, 1), lit=night, solar=night, glow=0.9 if night else 0.0)
    ctx.rectangle(560, 940, 800, 30); ctx.set_source_rgba(0.40, 0.28, 0.20, 1); ctx.fill()
    you(ctx, 860, 945, 0.7)
    arrive = ease(s.pr(0.25, 0.5)) if not night else 1
    quad(ctx, 1300-280*arrive, 945, 'dog', 0.55, phase=s.T*8, run=(1-arrive) if not night else 0, face=-1)
    ctx.restore()
    if not night:
        bword(ctx, "LONELINESS HITS FIRST", W/2, 130, 76, c('cream'), s.lt, s.at(0.15))
        if s.lt > s.at(0.55): bword(ctx, "BEST DECISION: ADOPT A DOG", W/2, H-100, 66, c('yellow'), s.lt, s.at(0.55))

def sc_water_fire_words(ctx, s):
    ctx.set_source_rgb(0.05, 0.06, 0.12); ctx.paint()
    kword(ctx, "NOT MONSTERS.", W/2, 260, 110, c('grey'), s.lt, s.at(0.45))
    p = s.lt > s.at(0.75)
    if p:
        ctx.rectangle(0, 400, W/2, 680); ctx.set_source_rgba(0.15, 0.40, 0.75, 1); ctx.fill()
        ctx.rectangle(W/2, 400, W/2, 680); ctx.set_source_rgba(0.85, 0.30, 0.15, 1); ctx.fill()
        flame(ctx, W*0.75, 900, 1.2, s.T)
        for i in range(5):
            ctx.move_to(0, 600+i*80+20*math.sin(s.T*3+i)); ctx.curve_to(W*0.15, 560+i*80, W*0.35, 640+i*80, W/2, 600+i*80)
            ctx.set_line_width(6); ctx.set_source_rgba(1, 1, 1, 0.3); ctx.stroke()
        kword(ctx, "WATER", W/4, 560, 140, c('cream'), s.lt, s.at(0.78))
        kword(ctx, "FIRE", W*0.75, 560, 140, c('cream'), s.lt, s.at(0.86))

def sc_subway_flood(ctx, s):
    ctx.set_source_rgb(0.12, 0.12, 0.15); ctx.paint()
    ctx.save(); push(ctx, s, 1.0, 1.12, sh=0.8)
    ctx.rectangle(0, 0, W, 300); ctx.set_source_rgba(0.40, 0.48, 0.40, 1); ctx.fill()  # soil
    skyline(ctx, 0, 300, 80, 260, (0.30, 0.34, 0.42, 1), lit=0.2, seed=81)
    ctx.rectangle(0, 300, W, 780); ctx.set_source_rgba(0.35, 0.28, 0.22, 1); ctx.fill()
    rrect(ctx, 120, 520, W-240, 380, 160); ctx.set_source_rgba(0.08, 0.08, 0.10, 1); ctx.fill()  # tunnel
    for i in range(20): ctx.rectangle(160+i*85, 860, 50, 14); ctx.set_source_rgba(0.35, 0.30, 0.26, 1); ctx.fill()
    lvl = ease(s.pr(0.45, 0.85))
    ctx.save(); rrect(ctx, 120, 520, W-240, 380, 160); ctx.clip()
    yw = 900 - 380*lvl
    ctx.move_to(0, yw)
    for x in range(0, W+20, 20): ctx.line_to(x, yw+8*math.sin(x*0.02+s.T*3))
    ctx.line_to(W, 1080); ctx.line_to(0, 1080); ctx.close_path(); ctx.set_source_rgba(0.20, 0.45, 0.75, 0.9); ctx.fill(); ctx.restore()
    for i, x in enumerate((360, 1560)):  # pumps
        paper(ctx, lambda k, x=x: rrect(k, x-70, 400, 140, 110, 12), (0.45, 0.48, 0.55, 1))
        on = s.lt < s.at(0.4); ctx.arc(x, 455, 20, 0, 2*math.pi); ctx.set_source_rgba(*((0.3, 1, 0.5) if on else (1, 0.2, 0.2)), 1); ctx.fill()
    ctx.restore()
    p = s.pr(0.15, 0.35)
    bword(ctx, f"{int(13_000_000*ease(p)):,} GALLONS A DAY", W/2, 110, 66, c('cream'), s.lt, s.at(0.12))
    if s.lt > s.at(0.6): bword(ctx, "FLOODED IN ~1.5 DAYS", W/2, H-90, 66, c('yellow'), s.lt, s.at(0.6))

def sc_suburb_fire(ctx, s):
    tl_ = s.at(0.05)
    sky(ctx, 'night'); ctx.save(); push(ctx, s, 1.0, 1.2, W/2, 800, sh=1.2)
    if abs(s.lt - tl_) < 0.15 or abs(s.lt-tl_-0.25) < 0.08:
        ctx.set_source_rgba(1, 1, 1, 0.6); ctx.paint()
        ctx.move_to(420, 0); ctx.line_to(380, 200); ctx.line_to(440, 230); ctx.line_to(360, 560); ctx.set_line_width(10); ctx.set_source_rgba(1, 1, 0.8, 1); ctx.stroke()
    ground(ctx, 860, (0.08, 0.10, 0.10, 1))
    for i in range(6):
        x = 120+i*300; house(ctx, x, 880, 260, 180, body=(0.30, 0.28, 0.32, 1), roof=(0.22, 0.18, 0.20, 1))
        t0 = s.at(0.12 + i*0.13)
        if s.lt > t0:
            fs = ease(prog(s.lt, t0, t0+1.0))
            flame(ctx, x+130, 680, 0.6+0.9*fs, s.T, seed=i)
            g = cairo.RadialGradient(x+130, 650, 10, x+130, 650, 400); g.add_color_stop_rgba(0, 1, 0.5, 0.2, 0.25*fs); g.add_color_stop_rgba(1, 1, 0.5, 0.2, 0)
            ctx.set_source(g); ctx.arc(x+130, 650, 400, 0, 2*math.pi); ctx.fill()
    ctx.restore()
    if s.lt > s.at(0.5): stamp(ctx, "NOBODY COMES", W/2, 150, 100, c('red'), s.lt, s.at(0.5))

def sc_main_street_wild(ctx, s):
    sky(ctx, 'day'); ctx.save(); off = s.lt*60; push(ctx, s, 1.0, 1.1, W/2, 850)
    for i in range(6):
        x = i*360 - off*0.5; paper(ctx, lambda k, x=x: k.rectangle(x, 380, 330, 480), ((0.85, 0.75, 0.60, 1), (0.70, 0.78, 0.80, 1), (0.88, 0.66, 0.55, 1))[i % 3])
        rrect(ctx, x+30, 440, 270, 60, 6); ctx.set_source_rgba(0.25, 0.28, 0.36, 1); ctx.fill()
        ctx.rectangle(x+40, 560, 250, 200); ctx.set_source_rgba(0.55, 0.70, 0.78, 1); ctx.fill()
    ground(ctx, 860, (0.62, 0.62, 0.64, 1)); road(ctx, 900, 180, dash_off=0)
    order = [('deer', 1.0), ('coyote', 0.8), ('boar', 0.7), ('deer', 0.9)]
    for i, (k, sz) in enumerate(order):
        t0 = s.at(0.05+i*0.08); p = prog(s.lt, t0, t0+6)
        if s.lt > t0: quad(ctx, -200 + p*1800 + i*60, 1000+(i % 2)*40, k, sz, phase=s.T*7+i, run=0.6)
    ctx.restore()
    bword(ctx, "MAIN STREET, BROAD DAYLIGHT", W/2, 120, 70, c('cream'), s.lt, s.at(0.1))
    if s.lt > s.at(0.6): stamp(ctx, "2020 PREVIEW", W-380, H-140, 70, c('red'), s.lt, s.at(0.6))

def sc_rat_fall(ctx, s):
    ctx.set_source_rgb(0.08, 0.09, 0.14); ctx.paint()
    base = 860
    for i, (lab, f) in enumerate((("RATS", 0.0), ("ROACHES", 0.1), ("PIGEONS", 0.2))):
        x = 450+i*500; h = 560*(1-0.8*ease(s.pr(0.45+f*0.5, 0.75+f*0.5)))
        paper(ctx, lambda k, x=x, h=h: rrect(k, x-110, base-h, 220, h, 14), (0.75, 0.30, 0.28, 1))
        text(ctx, lab, x, base+60, 48, c('cream'))
    p = s.pr(0.82, 0.95)
    quad(ctx, 450, base-560*(1-0.8*ease(s.pr(0.45, 0.75))) + 600*p*p, 'rat', 1.6, phase=s.T*3)
    if s.lt > s.at(0.82): stamp(ctx, "THE RAT KINGDOM FALLS", W/2, 140, 80, c('yellow'), s.lt, s.at(0.82))
    else: bword(ctx, "NO TRASH. NO HEAT.", W/2, 140, 72, c('cream'), s.lt, s.at(0.35))

def sc_green_words(ctx, s):
    ctx.set_source_rgb(0.10, 0.30, 0.18); ctx.paint()
    for i in range(40):
        g = ease(prog(s.lt, i*0.03, i*0.03+0.8)); x = (i*97) % W
        ctx.move_to(x, H); ctx.curve_to(x-30, H-200*g, x+40, H-400*g, x+10*math.sin(i), H-(300+(i % 5)*80)*g)
        ctx.set_line_width(10); ctx.set_source_rgba(0.35, 0.70, 0.40, 1); ctx.stroke()
    kword(ctx, "PLANTS ARE WINNING", W/2, H/2-40, 130, c('cream'), s.lt, s.at(0.3))

def sc_sidewalk_crack(ctx, s):
    ctx.set_source_rgb(0.62, 0.62, 0.64); ctx.paint()
    ctx.save(); push(ctx, s, 1.0, 1.4, W/2, H/2)
    for i in range(5): ctx.rectangle(i*420, 0, 8, H); ctx.set_source_rgba(0.5, 0.5, 0.52, 1); ctx.fill()
    wid = 4 + 40*ease(s.pr(0.2, 0.85))
    ctx.move_to(300, 0)
    pts = [(300, 0), (520, 200), (480, 380), (900, 560), (860, 760), (1300, 900), (1250, 1080)]
    for p_ in pts: ctx.line_to(*p_)
    ctx.set_line_width(wid); ctx.set_line_join(cairo.LINE_JOIN_ROUND); ctx.set_source_rgba(0.20, 0.18, 0.16, 1); ctx.stroke()
    g = ease(s.pr(0.0, 0.9))
    for (x, y) in pts[1:-1]:
        for k in range(4):
            a = -math.pi/2 + (k-1.5)*0.4
            ctx.move_to(x, y); ctx.line_to(x+math.cos(a)*120*g, y+math.sin(a)*120*g); ctx.set_line_width(8); ctx.set_source_rgba(0.30, 0.62, 0.32, 1); ctx.stroke()
    if s.pr(0.3, 0.7) > 0:
        frz = (math.sin(s.T*2) > 0)
        for (x, y) in pts[1:-1]:
            ctx.arc(x, y, 18, 0, 2*math.pi); ctx.set_source_rgba(*((0.8, 0.92, 1) if frz else (0.3, 0.55, 0.85)), 0.9); ctx.fill()
    ctx.restore()
    bword(ctx, "FREEZE. EXPAND. CRACK.", W/2, 120, 76, c('cream'), s.lt, s.at(0.3))
    if s.lt > s.at(0.8): stamp(ctx, "HOW A ROAD DIES", W/2, H-110, 80, c('red'), s.lt, s.at(0.8))

def sc_car_chair(ctx, s):
    sky(ctx, 'gray'); ctx.save(); push(ctx, s, 1.0, 1.2, W/2, 850)
    ground(ctx, 860, (0.45, 0.55, 0.40, 1))
    car(ctx, W/2, 990, 1.6, beam=False)
    rng = np.random.default_rng(3)
    for i in range(60):
        x = W/2+rng.uniform(-260, 260); y = 760+rng.uniform(0, 150); r = rng.uniform(8, 16)
        ctx.arc(x, y, r, 0, 2*math.pi); ctx.set_source_rgba(*((0.75, 0.45, 0.20), (0.85, 0.65, 0.25), (0.55, 0.35, 0.18))[i % 3], 1); ctx.fill()
    ctx.restore()
    pgauge(ctx, 230, 260, 140, 0); text(ctx, "BATTERY", 230, 430, 34, c('ink'))
    if s.lt > s.at(0.55): stamp(ctx, "A VERY EXPENSIVE CHAIR", W/2, 150, 80, c('red'), s.lt, s.at(0.55))
    if s.lt > s.at(0.78):
        p = s.pr(0.78, 1.0); x = -200 + p*(W+400); ctx.save(); ctx.translate(x, 960)
        for wx in (-70, 70): ctx.arc(wx, 0, 55, 0, 2*math.pi); ctx.set_line_width(8); ctx.set_source_rgba(*c('ink')); ctx.stroke()
        ctx.move_to(-70, 0); ctx.line_to(-10, -90); ctx.line_to(70, 0); ctx.move_to(-10, -90); ctx.line_to(50, -90); ctx.line_to(70, 0); ctx.stroke(); ctx.restore()
        speedlines(ctx, s.T, n=14, a=0.3)

def sc_last_light(ctx, s):
    ctx.set_source_rgb(0.02, 0.03, 0.07); ctx.paint()
    z = 3.0*(1-ease(s.pr(0.3, 0.85)))+0.35
    ctx.save(); ctx.translate(W/2, H/2); ctx.scale(z, z); ctx.translate(-W/2, -H/2)
    ctx.move_to(250, 400); ctx.curve_to(500, 150, 1300, 120, 1650, 330); ctx.curve_to(1800, 600, 1500, 900, 1100, 880)
    ctx.curve_to(700, 950, 300, 800, 250, 400); ctx.close_path(); ctx.set_source_rgba(0.06, 0.08, 0.14, 1); ctx.fill()
    g = cairo.RadialGradient(W/2, H/2, 1, W/2, H/2, 60); g.add_color_stop_rgba(0, 1, 0.85, 0.4, 1); g.add_color_stop_rgba(1, 1, 0.85, 0.4, 0)
    ctx.set_source(g); ctx.arc(W/2, H/2, 60, 0, 2*math.pi); ctx.fill()
    ctx.restore()
    bword(ctx, "THE BEST HOME ON EARTH", W/2, 120, 72, c('cream'), s.lt, s.at(0.1))
    if s.lt > s.at(0.7): bword(ctx, "THE ONLY LIGHT ON THE CONTINENT", W/2, H-100, 62, c('yellow'), s.lt, s.at(0.7))

def sc_golf_horses(ctx, s):
    sky(ctx, 'dawn'); ctx.save(); push(ctx, s, 1.0, 1.12, W/2, 800)
    ctx.move_to(0, 760)
    for x in range(0, W+40, 40): ctx.line_to(x, 760+30*math.sin(x*0.004))
    ctx.line_to(W, H); ctx.line_to(0, H); ctx.close_path(); ctx.set_source_rgba(0.45, 0.68, 0.35, 1); ctx.fill()
    ctx.rectangle(1500, 520, 8, 260); ctx.set_source_rgba(0.9, 0.9, 0.9, 1); ctx.fill()
    ctx.move_to(1508, 520); ctx.line_to(1600, 550); ctx.line_to(1508, 580); ctx.close_path(); ctx.set_source_rgba(*c('red')); ctx.fill()
    p = s.pr(0.1, 0.7)
    for i in range(4): quad(ctx, -300+p*1800+i*230, 900+(i % 2)*50, 'horse', 0.8, phase=s.T*9+i, run=1.0)
    if s.lt > s.at(0.75):
        q = s.pr(0.75, 1.0)
        quad(ctx, 200+q*1400, 1010, 'deer', 0.7, phase=s.T*9, run=1.0)
        quad(ctx, -100+q*1400, 1030, 'wolf', 0.75, phase=s.T*9, run=1.0)
    ctx.restore()
    bword(ctx, "PROPERLY WILD", W/2, 120, 90, c('cream'), s.lt, s.at(0.05))
    if s.lt > s.at(0.8): bword(ctx, "PREDATORS FOLLOW", W/2, H-90, 66, c('red'), s.lt, s.at(0.8))

def sc_preview_words(ctx, s):
    ctx.set_source_rgb(0.08, 0.08, 0.10); ctx.paint()
    kword(ctx, "WE'VE SEEN", W/2, 400, 140, c('cream'), s.lt, s.at(0.4))
    kword(ctx, "THIS BEFORE.", W/2, 580, 140, c('hivis'), s.lt, s.at(0.6))

def sc_exclusion_zone(ctx, s):
    sky(ctx, 'gray'); ctx.save(); push(ctx, s, 1.15, 1.0, W/2, 800)
    ground(ctx, 860, (0.42, 0.50, 0.38, 1))
    for i in range(4):  # apartment blocks
        x = 120+i*460; paper(ctx, lambda k, x=x: k.rectangle(x, 300, 380, 560), (0.70, 0.70, 0.68, 1))
        for r in range(9):
            for cc in range(5):
                ctx.rectangle(x+30+cc*70, 330+r*58, 40, 34); ctx.set_source_rgba(0.25, 0.28, 0.30, 1); ctx.fill()
        for k in range(6):
            ctx.move_to(x+20+k*60, 860); ctx.curve_to(x+k*60, 760, x+40+k*60, 680, x+30+k*60, 600+(k % 3)*40); ctx.set_line_width(8); ctx.set_source_rgba(0.30, 0.50, 0.30, 1); ctx.stroke()
    for i in range(6): tree(ctx, 60+i*360, 900, 1.1)
    p = s.pr(0.35, 0.8)
    for i, (k, sz) in enumerate((('wolf', 0.9), ('wolf', 0.8), ('boar', 0.8), ('horse', 0.8))):
        if p > 0: quad(ctx, -200+p*1500+i*220, 990+(i % 2)*40, k, sz, phase=s.T*6+i, run=0.5)
    ctx.restore()
    stamp(ctx, "1986", 260, 160, 90, c('red'), s.lt, s.at(0.02))
    bword(ctx, "~2,600 KM² LEFT EMPTY", W-460, 160, 56, c('cream'), s.lt, s.at(0.15))
    if s.lt > s.at(0.82): bword(ctx, "THE BIGGEST PROBLEM WAS US", W/2, H-100, 70, c('yellow'), s.lt, s.at(0.82))

def sc_decay_timelapse(ctx, s):
    p = ease(s.pr(0.0, 0.95))
    sky(ctx, 'day' if int(s.T*4) % 2 else 'dawn')
    ground(ctx, 860, (0.40+0.1*(1-p), 0.55, 0.36, 1))
    road(ctx, 900, 160) if p < 0.4 else None
    for i in range(4):
        house(ctx, 120+i*460, 880, 340, 230, decay=min(1, p*1.3 - i*0.05))
    for i in range(8):
        g = max(0, p*1.4 - 0.3 - i*0.05)
        if g > 0: tree(ctx, 80+i*250, 1000, 0.4+1.1*min(1, g))
    yrs = int(1 + 99*p**1.5)
    stopwatch(ctx, W-200, 220, 130, (s.T*0.8) % 1)
    bword(ctx, f"{yrs} YEAR" + ("" if yrs == 1 else "S"), W-200, 420, 60, c('cream'), s.lt, 0)
    if s.p.get('stamp', True) and s.lt > s.at(0.82): stamp(ctx, "STEEL BRIDGES FAIL", W/2-200, 160, 70, c('red'), s.lt, s.at(0.82))

def sc_what_lasts(ctx, s):
    ctx.set_source_rgb(0.12, 0.12, 0.16); ctx.paint()
    kword(ctx, "WHAT LASTS?", W/2, 120, 100, c('cream'), s.lt, s.at(0.0))
    items = [("CONCRETE DAMS", 0.1), ("STONE BUILDINGS", 0.2), ("GLASS BOTTLES", 0.3), ("PLASTIC (SADLY)", 0.42)]
    for i, (w_, f) in enumerate(items):
        bword(ctx, w_, 480 if i % 2 == 0 else 1440, 300+(i//2)*150, 62, c('yellow'), s.lt, s.at(f))
    if s.lt > s.at(0.55):
        p = ease(s.pr(0.55, 0.7)); ctx.save(); ctx.translate(0, (1-p)*400)
        ctx.move_to(300, H); ctx.line_to(500, 700); ctx.line_to(900, 640); ctx.line_to(1300, 680); ctx.line_to(1600, 760); ctx.line_to(1700, H); ctx.close_path()
        ctx.set_source_rgba(0.62, 0.60, 0.58, 1); ctx.fill()
        for i in range(4):
            ctx.save(); ctx.translate(640+i*230, 820); ctx.scale(0.8, 1); ctx.arc(0, 0, 80, 0, 2*math.pi); ctx.restore(); ctx.set_source_rgba(0.70, 0.68, 0.66, 1); ctx.fill()
        ctx.restore()
        if s.lt > s.at(0.78): bword(ctx, "1 INCH PER 10,000 YEARS", W/2, 580, 66, c('cream'), s.lt, s.at(0.78))

def sc_results_board(ctx, s):
    ctx.set_source_rgb(0.06, 0.08, 0.15); ctx.paint()
    stopwatch(ctx, W-260, 260, 170, (s.T*0.3) % 1)
    text(ctx, "THE FINAL TIME", 640, 110, 70, c('cream'))
    rows = [("LIGHTS OUT", "~2 DAYS"), ("SUBWAY FLOODED", "~1.5 DAYS"), ("PETS GONE WILD", "A FEW WEEKS"),
            ("GASOLINE STALE", "~1 YEAR"), ("STREET = FOREST", "~20 YEARS"), ("MOST HOUSES GONE", "~100 YEARS")]
    for i, (a, b) in enumerate(rows):
        t0 = s.at(0.12 + i*0.145); p = ease(prog(s.lt, t0, t0+0.3))
        y = 250+i*130
        rrect(ctx, 120, y, 1200, 110, 14); ctx.set_source_rgba(0.10, 0.12, 0.20, 1); ctx.fill()
        if p > 0:
            ctx.save(); ctx.rectangle(120, y, 1200, 110); ctx.clip()
            text(ctx, a, 160, y+55, 46, (*c('cream')[:3], p), anchor='l'); text(ctx, b, 1290, y+55+(1-p)*60, 52, (*c('hivis')[:3], p), anchor='r')
            ctx.restore()

def sc_your_odds(ctx, s):
    ctx.set_source_rgb(0.06, 0.08, 0.15); ctx.paint()
    icons = [("PHARMACY", c('teal')), ("CANNED FOOD", c('red')), ("SOLAR", c('yellow')), ("A GOOD DOG", c('orange'))]
    for i, (w_, col) in enumerate(icons):
        bword(ctx, w_, 270+i*460, 200, 50, col, s.lt, s.at(0.1+i*0.08))
    kword(ctx, "YOUR ODDS:", W/2, 430, 80, c('grey'), s.lt, s.at(0.45))
    kword(ctx, "YEARS. MAYBE DECADES.", W/2, 580, 110, c('hivis'), s.lt, s.at(0.55))
    if s.lt > s.at(0.82): stamp(ctx, "WATCH OUT FOR SMALL INJURIES", W/2, 860, 66, c('red'), s.lt, s.at(0.82))

def sc_green_city(ctx, s):
    sky(ctx, 'dawn'); ctx.save(); pan = 600*ease(s.pr(0, 1)); push(ctx, s, 1.1, 1.0, W/2, 700); ctx.translate(-pan, 0)
    skyline(ctx, 0, 860, 260, 700, (0.55, 0.60, 0.58, 1), lit=0, seed=91, span=W*2)
    rng = np.random.default_rng(9)
    for i in range(70):
        x = rng.uniform(-200, W*1.8); y = rng.uniform(300, 860); r = rng.uniform(30, 90)
        ctx.arc(x, y, r, 0, 2*math.pi); ctx.set_source_rgba(0.28, 0.55, 0.32, 0.9); ctx.fill()
    ground(ctx, 860, (0.30, 0.52, 0.30, 1))
    for i in range(5): quad(ctx, 200+i*380, 960, ('deer', 'horse', 'wolf', 'boar', 'deer')[i], 0.6, phase=s.T*3+i, run=0.2)
    ctx.restore()
    bword(ctx, "IT NEVER NEEDED US", W/2, 130, 80, c('cream'), s.lt, s.at(0.45))
    if s.lt > s.at(0.82): bword(ctx, "THE ANIMALS GET THEIR WORLD BACK", W/2, H-100, 62, c('yellow'), s.lt, s.at(0.82))

def sc_outro_cta(ctx, s):
    ctx.set_source_rgb(0.05, 0.07, 0.14); ctx.paint(); stars(ctx, 200, alpha=0.6)
    kword(ctx, "NOW YOU DECIDE", W/2, 200, 100, c('cream'), s.lt, s.at(0.0))
    p = back(s.pr(0.12, 0.25))
    if p > 0:
        ctx.save(); ctx.translate(W/2, 520); ctx.scale(p, p)
        paper(ctx, lambda k: rrect(k, -620, -150, 1240, 300, 40), c('cream'))
        ctx.move_to(-420, 140); ctx.line_to(-480, 230); ctx.line_to(-330, 150); ctx.close_path(); ctx.set_source_rgba(*c('cream')); ctx.fill()
        text(ctx, "SHOULD THE ANIMALS", 0, -45, 76, c('ink')); text(ctx, "VANISH TOO?", 0, 55, 86, c('red'))
        ctx.restore()
    if s.lt > s.at(0.55): bword(ctx, "TELL ME IN THE COMMENTS", W/2, 830, 66, c('yellow'), s.lt, s.at(0.55))

exec(open(os.path.join(HERE, 'scenes_v3.py')).read())
SCENES = {k[3:]: v for k, v in globals().items() if k.startswith('sc_')}

# ======================= SECTION CARD + HUD =======================
def section_card(ctx, s):
    sw, title, sub = s.card
    lt = s.lt
    a = 1 - ease(prog(lt, 1.05, 1.4))
    if a > 0:
        ctx.set_source_rgba(0.03, 0.04, 0.09, 0.88*a); ctx.paint()
        p = back(prog(lt, 0.0, 0.3)); ctx.save(); ctx.translate(W/2, H/2-60); ctx.scale(p, p)
        ctx.push_group(); stopwatch(ctx, 0, -40, 200, (lt*0.6) % 1, val=sw)
        text_paper(ctx, title, 0, 290, 100, c('hivis'))
        if sub: text(ctx, sub, 0, 390, 56, c('cream'))
        ctx.pop_group_to_source(); ctx.paint_with_alpha(a); ctx.restore()

def hud(ctx, sw_text):
    if not sw_text: return
    rrect(ctx, 30, 26, 300, 64, 32); ctx.set_source_rgba(0.03, 0.04, 0.09, 0.7); ctx.fill()
    stopwatch(ctx, 66, 58, 22, 0.0)
    text(ctx, sw_text, 106, 58, 32, c('cream'), anchor='l')

# ======================= COMPOSITOR =======================
TL = None; HUDTXT = []
TRANS_CYCLE = ['whip_l', 'cut', 'flash', 'cut', 'whip_u', 'cut', 'spin', 'cut']
def setup(vo_dir):
    global TL, HUDTXT
    TL = plan(vo_dir); cur = None; HUDTXT = []
    for sh in TL:
        if sh['card']: cur = sh['card'][0]
        HUDTXT.append(cur)
    for i, sh in enumerate(TL):
        nxt = TL[i+1] if i+1 < len(TL) else None
        sh['trans'] = 'zoom' if (nxt and nxt['card']) else ('flash' if nxt and nxt['scene'] == 'title_card' else TRANS_CYCLE[i % len(TRANS_CYCLE)])
    return TL

def shot_surface(i, T):
    sh = TL[i]; s = S(sh, T)
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H); k = cairo.Context(surf)
    SCENES[sh['scene']](k, s)
    if sh['card']: section_card(k, s)
    if i >= 8 and not (sh['card'] and s.lt < 1.4): hud(k, HUDTXT[i])
    return surf

TW = 0.26
def frame(T):
    out = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H); ctx = cairo.Context(out)
    idx = max(i for i, sh in enumerate(TL) if sh['start'] <= T) if T >= 0 else 0
    done = False
    for bi in (idx, idx+1):
        if bi <= 0 or bi >= len(TL): continue
        b = TL[bi]['start']; kind = TL[bi-1]['trans']
        if kind != 'cut' and abs(T-b) < TW:
            p = (T-(b-TW))/(2*TW); sa = shot_surface(bi-1, T); sb = shot_surface(bi, T)
            if kind in ('whip_l', 'whip_u'):
                horiz = kind == 'whip_l'; e = ease(p); sp = math.sin(p*math.pi); off = -e*(W if horiz else H)
                for surf, o in ((sa, off), (sb, off+(W if horiz else H))):
                    ctx.save(); ctx.translate(*((o, 0) if horiz else (0, -o))); blur_paint(ctx, surf, 500*sp if horiz else 0, 0 if horiz else 500*sp, n=7); ctx.restore()
            elif kind == 'flash':
                ctx.set_source_surface(sa if p < 0.5 else sb, 0, 0); ctx.paint(); ctx.set_source_rgba(1, 1, 1, max(0, 1-abs(p-0.5)*3.2)); ctx.paint()
            elif kind == 'zoom':
                sp = math.sin(p*math.pi)
                if p < 0.5:
                    z = 1+4*ease(p*2)**2; ctx.save(); ctx.translate(W/2, H/2); ctx.scale(z, z); ctx.translate(-W/2, -H/2); blur_paint(ctx, sa, 0, 0, n=6, zoom=0.25*sp); ctx.restore()
                else:
                    z = 1.8-0.8*ease((p-0.5)*2); ctx.save(); ctx.translate(W/2, H/2); ctx.scale(z, z); ctx.translate(-W/2, -H/2); blur_paint(ctx, sb, 0, 0, n=6, zoom=0.25*sp); ctx.restore()
            elif kind == 'spin':
                sp = math.sin(p*math.pi); surf = sa if p < 0.5 else sb
                ctx.save(); ctx.translate(W/2, H/2); ctx.rotate((p-0.5)*1.4); ctx.scale(1+0.5*sp, 1+0.5*sp); ctx.translate(-W/2, -H/2); blur_paint(ctx, surf, 0, 0, n=7, rot=0.35*sp); ctx.restore()
            done = True; break
    if not done:
        ctx.set_source_surface(shot_surface(idx, T), 0, 0); ctx.paint()
    grain(ctx, 0.07); vignette(ctx, 0.38)
    return out

# ======================= AUDIO =======================
def audio(out_dir, vo_dir, sr=48000):
    total = TL[-1]['start']+TL[-1]['dur']; n = int(total*sr)+sr
    vo = np.zeros(n); bed = np.zeros(n); rng = np.random.default_rng(1)
    def add(buf, sig, at):
        i = int(at*sr); j = min(n, i+len(sig))
        if i < n: buf[i:j] += sig[:j-i]
    for sh in TL:
        if sh['vo'] <= 0: continue
        raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', os.path.join(vo_dir, sh['id']+'.wav'), '-ac', '1', '-ar', str(sr), '-f', 's16le', '-'], capture_output=True).stdout
        add(vo, np.frombuffer(raw, np.int16).astype(float)/32768, sh['start']+sh['lead'])
    def kick():
        tt = np.arange(int(0.35*sr))/sr; f = 50+90*np.exp(-tt*28); return np.sin(2*np.pi*np.cumsum(f)/sr)*np.exp(-tt*9)*0.7
    def hat():
        tt = np.arange(int(0.05*sr))/sr; w = np.diff(np.concatenate([[0], rng.normal(0, 1, len(tt))])); return w*np.exp(-tt*80)*0.08
    def whoosh(d=0.6):
        m = int(d*sr); w = rng.normal(0, 1, m); env = np.sin(np.linspace(0, np.pi, m))**2
        acc = np.cumsum(w); k = np.linspace(40, 4, m).astype(int); idx = np.arange(m); lo = np.maximum(0, idx-k)
        return (acc[idx]-acc[lo])/k*env*0.45
    def impact():
        tt = np.arange(int(0.9*sr))/sr
        return np.sin(2*np.pi*(45+60*np.exp(-tt*10))*tt)*np.exp(-tt*4)*0.8 + rng.normal(0, 1, len(tt))*np.exp(-tt*25)*0.2
    def pad(f, d, amp=0.05):
        tt = np.arange(int(d*sr))/sr; env = np.minimum(1, tt/2)*np.minimum(1, (d-tt)/2)
        return sum(np.sin(2*np.pi*f*m*tt + m) * amp/(m) for m in (1, 1.5, 2, 3)) * env
    # section-based mood: (root Hz, beat on?)
    moods = {'s01': (55, False), 's08': (49, True), 's13': (46, True), 's20': (52, True), 's30': (55, True), 's36': (41, True), 's41': (58, False), 's46': (44, False), 's50': (49, True), 's52': (55, False)}
    starts = [(sh['start'], moods[sh['id']]) for sh in TL if sh['id'] in moods] + [(total, None)]
    for (t0, m), (t1, _) in zip(starts, starts[1:]):
        f, beat = m; bed[int(t0*sr):int(t0*sr)+int((t1-t0)*sr)] += pad(f*2, t1-t0)[:max(0, min(n, int(t1*sr))-int(t0*sr))]
        if beat:
            bt = t0+1.3; b = 60/112
            while bt < t1-0.5: add(bed, kick()*0.6, bt); add(bed, hat(), bt+b/2); bt += b
    for i, sh in enumerate(TL):
        if i > 0 and TL[i-1]['trans'] != 'cut': add(bed, whoosh(0.6), sh['start']-0.3)
        if sh['card']: add(bed, impact(), sh['start']+0.05)
    for sid, at in (('s06', 'lead'), ('s21', 'reveal')):
        sh = next(x for x in TL if x['id'] == sid)
        add(bed, impact()*1.2, sh['start']+sh['lead']+(0.05*sh['vo'] if sid == 's06' else 0.78*sh['vo']))
    def w(p, x):
        pcm = (np.clip(x, -1, 1)*32767).astype(np.int16)
        with wave.open(p, 'wb') as f: f.setnchannels(1); f.setsampwidth(2); f.setframerate(sr); f.writeframes(pcm.tobytes())
    w(os.path.join(out_dir, 'vo.wav'), vo); w(os.path.join(out_dir, 'bed.wav'), bed*0.9)
    return total

if __name__ == '__main__':
    mode = sys.argv[1]
    if mode == 'plan':
        tl = setup(sys.argv[2]); print(json.dumps([(x['id'], round(x['start'], 2), round(x['dur'], 2), x['trans']) for x in tl]))
        print('TOTAL', round(tl[-1]['start']+tl[-1]['dur'], 2))
    elif mode == 'still':
        setup(sys.argv[4]); frame(float(sys.argv[2])).write_to_png(sys.argv[3])
    elif mode == 'shotstills':  # one still per shot at 60% of its length
        setup(sys.argv[3]); os.makedirs(sys.argv[2], exist_ok=True)
        for sh in TL:
            frame(sh['start']+sh['dur']*0.6).write_to_png(os.path.join(sys.argv[2], sh['id']+'.png'))
    elif mode == 'audio':
        setup(sys.argv[3]); print(audio(sys.argv[2], sys.argv[3]))
    elif mode == 'video':
        out, t0, t1 = sys.argv[2], float(sys.argv[3]), float(sys.argv[4]); setup(sys.argv[5])
        p = subprocess.Popen(['ffmpeg', '-y', '-v', 'error', '-f', 'rawvideo', '-pix_fmt', 'bgra', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                              '-c:v', 'libx264', '-preset', 'medium', '-crf', '19', '-pix_fmt', 'yuv420p', out], stdin=subprocess.PIPE)
        for f in range(int(round(t0*FPS)), int(round(t1*FPS))):
            p.stdin.write(bytes(frame(f/FPS).get_data()))
        p.stdin.close(); p.wait()
