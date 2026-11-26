"""Dynamic style test: 'racing the radio' (n2 VO). Virtual camera, parallax, whip/zoom transitions,
kinetic type, motion blur, screen shake. Pure pycairo + numpy.
Usage: python3 dynamic_test.py still T out.png | video out.mp4 t0 t1 | audio out.wav"""
import os, sys, math, subprocess, cairo, numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'pilot'))
from style import *

FPS = 24
DUR = 27.6
# sentence starts in n2.mp3
T_CAR, T_APART, T_LIGHT, T_NUM, T_MAP, T_NOT, T_RADIO, T_LOST = 1.84, 6.16, 8.04, 11.62, 15.14, 20.98, 23.06, 24.61
# scene boundaries (transition centred on boundary)
B = [0.0, 1.70, 7.85, 11.45, 14.95, 20.75, 24.45, DUR]
TRANS = ['whip_l', 'flash', 'zoom', 'spin', 'whip_u', 'flash']
TW = 0.32  # transition half-width

def noise1(t, seed=0):
    return (math.sin(t*12.9+seed)*0.5 + math.sin(t*7.3+seed*2.1)*0.3 + math.sin(t*23.1+seed*0.7)*0.2)

def shake(t, amp):
    return amp*noise1(t, 1), amp*noise1(t, 5)

def cam(ctx, cx, cy, z=1.0, rot=0.0, sh=(0, 0)):
    ctx.translate(W/2+sh[0], H/2+sh[1]); ctx.scale(z, z); ctx.rotate(rot); ctx.translate(-cx, -cy)

def bg(ctx, col1, col2):
    g = cairo.LinearGradient(0, 0, 0, H); g.add_color_stop_rgba(0, *col1); g.add_color_stop_rgba(1, *col2)
    ctx.set_source(g); ctx.paint()

def kword(ctx, s, x, y, size, col, lt, t0, anchor='c', pop=0.22):
    """Kinetic word: overshoot scale-in + slight rotation settle."""
    p = prog(lt, t0, t0+pop)
    if p <= 0: return
    sc = back(p); ctx.save(); ctx.translate(x, y); ctx.rotate((1-ease(p))*-0.12); ctx.scale(sc, sc)
    text_paper(ctx, s, 0, 0, size, col, anchor=anchor); ctx.restore()

def speedlines(ctx, lt, n=26, a=0.35, horiz=True, seed=3):
    rng = np.random.default_rng(seed)
    ys = rng.uniform(0, H, n); ln = rng.uniform(200, 700, n); sp = rng.uniform(2500, 5200, n); ph = rng.uniform(0, 1, n)
    ctx.set_line_cap(cairo.LINE_CAP_ROUND)
    for i in range(n):
        x = W+400 - ((lt*sp[i] + ph[i]*W*2) % (W*2+800))
        ctx.move_to(x, ys[i]); ctx.line_to(x+ln[i], ys[i]); ctx.set_line_width(3+ (i%3)*2)
        ctx.set_source_rgba(1, 1, 1, a*(0.4+0.6*(i%2))); ctx.stroke()

# ---------------- props ----------------
def car(ctx, x, y, s=1.0, wheel=0.0, bounce=0.0, lost_cap=False, beam=True):
    ctx.save(); ctx.translate(x, y-bounce); ctx.scale(s, s)
    if beam:
        g = cairo.LinearGradient(150, 0, 700, 0); g.add_color_stop_rgba(0, 1, 0.95, 0.7, 0.45); g.add_color_stop_rgba(1, 1, 0.95, 0.7, 0)
        ctx.move_to(150, -70); ctx.line_to(700, -150); ctx.line_to(700, 30); ctx.close_path(); ctx.set_source(g); ctx.fill()
    paper(ctx, lambda k: rrect(k, -170, -95, 340, 70, 22), (0.55, 0.58, 0.63, 1))
    paper(ctx, lambda k: (k.new_path(), k.move_to(-105, -92), k.line_to(-65, -150), k.line_to(55, -150), k.line_to(100, -92), k.close_path()), (0.50, 0.53, 0.58, 1), off=(4, 5))
    for wx0, wx1 in ((-90, -15), (-5, 75)):
        ctx.move_to(wx0, -98); ctx.line_to(wx0+20 if wx0 < 0 else wx0, -142); ctx.line_to(wx1-5 if wx0 < 0 else wx1-15, -142); ctx.line_to(wx1, -98); ctx.close_path()
        ctx.set_source_rgba(0.62, 0.80, 0.88, 1); ctx.fill()
    ctx.rectangle(150, -80, 18, 14); ctx.set_source_rgba(1, 0.95, 0.7, 1); ctx.fill()
    ctx.rectangle(-170, -80, 14, 14); ctx.set_source_rgba(*c('red')); ctx.fill()
    for wx in (-100, 100):
        ctx.arc(wx, -25, 36, 0, 2*math.pi); ctx.set_source_rgba(*c('ink')); ctx.fill()
        if not (lost_cap and wx == 100):
            ctx.arc(wx, -25, 18, 0, 2*math.pi); ctx.set_source_rgba(0.8, 0.82, 0.86, 1); ctx.fill()
        for i in range(4):
            a = wheel + i*math.pi/2
            ctx.move_to(wx, -25); ctx.line_to(wx+16*math.cos(a), -25+16*math.sin(a))
        ctx.set_line_width(4); ctx.set_source_rgba(*c('ink')); ctx.stroke()
    ctx.restore()

def cruiser_top(ctx, x, y, ang, s=1.0, flash=0.0):
    ctx.save(); ctx.translate(x, y); ctx.rotate(ang); ctx.scale(s, s)
    paper(ctx, lambda k: rrect(k, -26, -50, 52, 100, 12), c('white'), off=(4, 5))
    ctx.rectangle(-26, -12, 52, 26); ctx.set_source_rgba(*c('ink')); ctx.fill()
    ctx.rectangle(-22, -8, 20, 10); ctx.set_source_rgba(*(c('red') if flash > 0.5 else c('blue'))); ctx.fill()
    ctx.rectangle(2, -8, 20, 10); ctx.set_source_rgba(*(c('blue') if flash > 0.5 else c('red'))); ctx.fill()
    ctx.restore()

def buildings(ctx, offset, base, hmin, hmax, wmin, wmax, col, win, seed, span=W*3):
    rng = np.random.default_rng(seed); xs = []; x = 0
    while x < span:
        w = rng.uniform(wmin, wmax); h = rng.uniform(hmin, hmax); xs.append((x, w, h)); x += w+rng.uniform(4, 30)
    total = x
    for (bx, w, h) in xs:
        X = (bx - offset) % total - 300
        if X > W+300 or X+w < -300: continue
        ctx.rectangle(X, base-h, w, h); ctx.set_source_rgba(*col); ctx.fill()
        if win:
            r2 = np.random.default_rng(int(bx))
            for wy in np.arange(base-h+20, base-20, 34):
                for wx in np.arange(X+12, X+w-20, 28):
                    if r2.random() < 0.35:
                        ctx.rectangle(wx, wy, 12, 16); ctx.set_source_rgba(1, 0.85, 0.45, 0.85); ctx.fill()

def gauge(ctx, x, y, r, val, vmax=140):
    ctx.save(); ctx.translate(x, y)
    paper(ctx, lambda k: (k.new_path(), k.arc(0, 0, r, 0, 2*math.pi)), (0.06, 0.07, 0.12, 0.92))
    a0, a1 = math.pi*0.75, math.pi*2.25
    ctx.arc(0, 0, r*0.82, a0, a1); ctx.set_line_width(10); ctx.set_source_rgba(1, 1, 1, 0.15); ctx.stroke()
    av = a0+(a1-a0)*min(1, val/vmax)
    ctx.arc(0, 0, r*0.82, a0, av); ctx.set_line_width(10); ctx.set_source_rgba(*c('hivis')); ctx.stroke()
    ctx.move_to(0, 0); ctx.line_to(r*0.75*math.cos(av), r*0.75*math.sin(av)); ctx.set_line_width(6); ctx.set_source_rgba(*c('red')); ctx.stroke()
    ctx.arc(0, 0, 10, 0, 2*math.pi); ctx.set_source_rgba(*c('cream')); ctx.fill()
    text(ctx, f"{int(val)}", 0, r*0.42, r*0.42, c('cream')); text(ctx, "MPH", 0, r*0.72, r*0.16, c('grey'))
    ctx.restore()

# ---------------- scenes (lt = time since scene start, T = absolute) ----------------
def sc_title(ctx, lt, T):
    bg(ctx, (0.10, 0.16, 0.30, 1), (0.05, 0.08, 0.16, 1))
    ctx.save(); ctx.translate(W/2, H/2); ctx.rotate(lt*0.5)
    for i in range(16):
        ctx.move_to(0, 0); ctx.arc(0, 0, 1600, i*math.pi/8, i*math.pi/8+math.pi/16); ctx.close_path()
    ctx.set_source_rgba(1, 1, 1, 0.05); ctx.fill(); ctx.restore()
    eq = ['v = d / t', 'c = 299,792 km/s', 'E = mc²', 'F = ma', 'Δt', 'km/h']
    for i, e in enumerate(eq):
        x = (i*347 + lt*(120+i*40)) % (W+400) - 200; y = 120 + (i*173) % (H-240)
        text(ctx, e, x, y, 38+i*4, (1, 1, 1, 0.12), weight='n')
    z = 1 + 0.08*lt
    ctx.save(); ctx.translate(W/2, H/2); ctx.scale(z, z); ctx.translate(-W/2, -H/2)
    kword(ctx, "HERE'S A FUN BIT OF", W/2, H/2-120, 64, c('cream'), lt, 0.0)
    kword(ctx, "PHYSICS", W/2, H/2+40, 210, c('hivis'), lt, 0.55, pop=0.28)
    ctx.restore()

def sc_highway(ctx, lt, T):
    speed = 900 + 2600*ease(prog(T, T_CAR, 5.6))
    dist = 900*lt + 1300*max(0, lt-1.5)**1.6
    bg(ctx, (0.98, 0.62, 0.38, 1), (0.40, 0.25, 0.45, 1))
    ctx.arc(1400, 520, 140, 0, 2*math.pi); ctx.set_source_rgba(1, 0.86, 0.55, 0.9); ctx.fill()
    shk = shake(T, 4 + 14*prog(T, 4.0, 6.0) + 18*prog(T, T_APART, T_APART+0.3)*(1-prog(T, 7.2, 7.8)))
    z = 0.9 + 0.35*ease(prog(T, 2.2, 6.0)); rot = -0.04*ease(prog(T, 3.0, 6.0))
    ctx.save(); cam(ctx, W/2+120*ease(prog(T, 2, 6)), 640, z, rot, shk)
    buildings(ctx, dist*0.08, 760, 120, 360, 90, 220, (0.33, 0.22, 0.40, 1), False, 11)
    buildings(ctx, dist*0.25, 800, 160, 460, 120, 260, (0.20, 0.16, 0.30, 1), True, 12)
    ctx.rectangle(-2000, 800, 6000, 600); ctx.set_source_rgba(0.16, 0.17, 0.22, 1); ctx.fill()
    for i in range(-10, 30):
        x = i*260 - (dist*1.0) % 260
        ctx.rectangle(x, 905, 130, 14); ctx.set_source_rgba(*c('yellow', 0.9)); ctx.fill()
    for i in range(-4, 12):  # lamp posts (fast parallax)
        x = i*700 - (dist*1.4) % 700
        ctx.rectangle(x, 470, 16, 340); ctx.set_source_rgba(0.1, 0.1, 0.14, 1); ctx.fill()
        ctx.rectangle(x-40, 466, 70, 14); ctx.fill()
    lost = T > T_APART+0.25
    cx = W/2+40
    car(ctx, cx, 880, 1.25, wheel=-dist/40, bounce=abs(math.sin(T*18))*(3+6*prog(T, 4, 6)), lost_cap=lost)
    if lost:  # hubcap flying off backwards + smoke
        p = T-(T_APART+0.25)
        hx = cx+125 - p*1400; hy = 849 - 420*p + 900*p*p
        ctx.save(); ctx.translate(hx, hy); ctx.rotate(p*20); ctx.arc(0, 0, 24, 0, 2*math.pi); ctx.set_source_rgba(0.85, 0.86, 0.9, 1); ctx.fill()
        ctx.arc(0, 0, 10, 0, 2*math.pi); ctx.set_source_rgba(0.6, 0.6, 0.65, 1); ctx.fill(); ctx.restore()
        for i in range(8):
            q = (p*1.2 + i*0.13) % 1.0
            ctx.arc(cx-230 - q*500, 840 - q*80 + (i % 3)*10, 20+q*60, 0, 2*math.pi); ctx.set_source_rgba(0.85, 0.85, 0.88, 0.5*(1-q)); ctx.fill()
    ctx.restore()
    speedlines(ctx, T, a=0.10+0.25*prog(T, 3.5, 6.0))
    # HUD
    gauge(ctx, W-210, H-200, 150, 120*ease(prog(T, 2.4, 5.4)) + (2*math.sin(T*30) if T > 5.4 else 0))
    kword(ctx, "120 MPH", 330, 180, 120, c('cream'), T, 4.2)
    if T > T_APART+0.05:
        ctx.save(); ctx.translate(330, 290); ctx.rotate(0.04*math.sin(T*25))
        kword(ctx, "(if it doesn't fall apart)", 40, 30, 56, c('yellow'), T, T_APART+0.05); ctx.restore()

def sc_radio(ctx, lt, T):
    bg(ctx, (0.05, 0.08, 0.16, 1), (0.10, 0.16, 0.30, 1))
    z = 3.2 - 2.3*ease(prog(lt, 0.0, 1.4)); shk = shake(T, 3)
    ctx.save(); cam(ctx, W/2, 640, z, 0.03*math.sin(lt*2), shk)
    # skyline silhouette + tower
    buildings(ctx, 0, 1000, 150, 420, 100, 240, (0.12, 0.18, 0.32, 1), True, 21)
    ctx.set_line_width(10); ctx.set_source_rgba(*c('grey'))
    ctx.move_to(W/2-90, 1000); ctx.line_to(W/2, 420); ctx.line_to(W/2+90, 1000); ctx.stroke()
    for yy in range(500, 1000, 80):
        w = (yy-420)/580*90; ctx.move_to(W/2-w, yy); ctx.line_to(W/2+w, yy+60); ctx.stroke()
    blink = 1 if int(T*3) % 2 == 0 else 0.3
    ctx.arc(W/2, 410, 16, 0, 2*math.pi); ctx.set_source_rgba(1, 0.2, 0.2, blink); ctx.fill()
    # rings racing outward (speed of light)
    for i in range(10):
        r = ((lt*1600 + i*260) % 2600)
        a = max(0, 1 - r/2600)
        ctx.arc(W/2, 410, r, 0, 2*math.pi); ctx.set_line_width(10*a+2); ctx.set_source_rgba(0.45, 0.75, 1, 0.7*a); ctx.stroke()
    ctx.restore()
    # light streak
    p = prog(T, T_LIGHT+1.6, T_LIGHT+2.1)
    if 0 < p < 1:
        x = -400 + p*(W+800); g = cairo.LinearGradient(x-600, 0, x, 0)
        g.add_color_stop_rgba(0, 1, 1, 1, 0); g.add_color_stop_rgba(1, 1, 1, 1, 0.9)
        ctx.rectangle(x-600, H/2-6, 600, 12); ctx.set_source(g); ctx.fill()
    words = ["SPEED", "OF", "LIGHT"]
    for i, w_ in enumerate(words):
        kword(ctx, w_, W/2 - 420 + i*420, 190, 150 if i != 1 else 90, c('cream') if i != 2 else c('yellow'), T, T_LIGHT+1.2+i*0.25)
    kword(ctx, "POLICE RADIO CALL", W/2, H-120, 56, c('blue'), T, T_LIGHT+0.3)

def sc_number(ctx, lt, T):
    bg(ctx, (0.90, 0.22, 0.27, 1), (0.55, 0.10, 0.18, 1))
    for i in range(14):  # diagonal stripes sliding
        x = (i*220 + lt*500) % (W+600) - 300
        ctx.move_to(x, 0); ctx.line_to(x+120, 0); ctx.line_to(x-280, H); ctx.line_to(x-400, H); ctx.close_path()
    ctx.set_source_rgba(1, 1, 1, 0.05); ctx.fill()
    p = ease(prog(T, T_NUM+0.15, T_NUM+1.8))
    val = 120 + (670_000_000-120)*(p**3)
    sh = shake(T, 10*(1-prog(T, T_NUM+1.8, T_NUM+2.4)) + 2)
    zz = 1.0 + 0.06*math.sin(lt*3)
    ctx.save(); ctx.translate(W/2+sh[0], 430+sh[1]); ctx.scale(zz, zz)
    text_paper(ctx, f"{int(val):,}", 0, 0, 190, c('cream')); ctx.restore()
    kword(ctx, "MILES PER HOUR", W/2, 590, 60, c('yellow'), T, T_NUM+0.3)
    # comparison bars
    bp = ease(prog(T, T_NUM+1.9, T_NUM+2.8))
    ctx.set_source_rgba(0, 0, 0, 0.25); rrect(ctx, 200, 720, W-400, 70, 12); ctx.fill()
    ctx.set_source_rgba(*c('cream')); rrect(ctx, 200, 720, max(14, (W-400)*bp), 70, 12); ctx.fill()
    text(ctx, "RADIO", 230, 755, 34, c('ink'), anchor='l') if bp > 0.2 else None
    ctx.set_source_rgba(*c('grey')); ctx.rectangle(200, 830, 4, 50); ctx.fill()
    text(ctx, "YOUR CAR: 120  (that's the tiny line)", 220, 855, 32, c('cream'), anchor='l', weight='n') if bp > 0.5 else None

MAP_PATH = [(0, 0), (900, 0), (900, -600), (1800, -600), (1800, -1200)]
def _path_at(d):
    for (x0, y0), (x1, y1) in zip(MAP_PATH, MAP_PATH[1:]):
        L = math.hypot(x1-x0, y1-y0)
        if d <= L: return x0+(x1-x0)*d/L, y0+(y1-y0)*d/L, math.atan2(y1-y0, x1-x0)
        d -= L
    (x0, y0), (x1, y1) = MAP_PATH[-2], MAP_PATH[-1]; return x1, y1, math.atan2(y1-y0, x1-x0)

def sc_map(ctx, lt, T):
    ctx.set_source_rgba(0.09, 0.13, 0.22, 1); ctx.paint()
    d = 2400*ease(prog(lt, 0.2, 4.6)) if lt < 4.6 else 2400
    px, py, hd = _path_at(min(d, 2399))
    # camera rotates so the car always heads up, then pulls out at the reveal
    reveal = ease(prog(T, 19.4, 20.6))
    z = 1.25 - 0.85*reveal
    rot = (-hd - math.pi/2) * (1-reveal)
    ctx.save(); cam(ctx, px*(1-reveal)+900*reveal, py*(1-reveal)-600*reveal, z, rot, shake(T, 2))
    for i in range(-8, 12):  # streets
        ctx.rectangle(i*300-30, -3000, 60, 6000); ctx.rectangle(-3000, i*300-30 - 1200, 6000, 60)
    ctx.set_source_rgba(0.18, 0.24, 0.36, 1); ctx.fill()
    tower = (-600, 600)
    wr = max(0, (T - (T_MAP+0.6)))*1400
    if wr > 0:
        ctx.arc(*tower, wr, 0, 2*math.pi); ctx.set_line_width(18); ctx.set_source_rgba(0.45, 0.75, 1, 0.55); ctx.stroke()
        ctx.arc(*tower, wr, 0, 2*math.pi); ctx.set_source_rgba(0.45, 0.75, 1, 0.06); ctx.fill()
    ctx.arc(*tower, 22, 0, 2*math.pi); ctx.set_source_rgba(1, 0.3, 0.3, 1); ctx.fill()
    # cards pop at every intersection the wave reaches
    for ix in range(-2, 9):
        for iy in range(-6, 3):
            X, Y = ix*300, iy*300
            dd = math.hypot(X-tower[0], Y-tower[1])
            if wr > dd and (ix+iy) % 2 == 0:
                p = prog(wr, dd, dd+500)
                cruiser_top(ctx, X, Y, 0.0, 0.9*back(p), flash=(int(T*6)+ix) % 2)
    target = (1800, -600)
    tp = back(prog(T, 17.2, 17.6))
    if tp > 0:
        ctx.save(); ctx.translate(*target); ctx.rotate(-rot); ctx.scale(tp, tp)
        paper(ctx, lambda k: rrect(k, 40, -150, 360, 120, 14), c('cream'))
        text(ctx, "SUSPECT:", 64, -118, 30, c('red'), anchor='l'); text(ctx, "GREY SEDAN", 64, -70, 44, c('ink'), anchor='l')
        ctx.restore()
    # trail + car
    ctx.set_line_width(14); ctx.set_source_rgba(1, 1, 1, 0.25)
    dd2 = 0; ctx.move_to(*MAP_PATH[0])
    for pt in MAP_PATH[1:]:
        ctx.line_to(*pt)
    ctx.stroke()
    ctx.save(); ctx.translate(px, py); ctx.rotate(hd+math.pi/2)
    paper(ctx, lambda k: rrect(k, -26, -48, 52, 96, 12), (0.6, 0.63, 0.68, 1), off=(4, 5)); ctx.restore()
    ctx.restore()
    if T < 19.8:
        kword(ctx, "ALREADY THERE.", W/2, H-140, 120, c('yellow'), T, 18.3)
    kword(ctx, "...and there. And there. And there.", W/2, H-130, 64, c('cream'), T, 19.8)

def sc_split(ctx, lt, T):
    pan = ease(prog(T, T_RADIO-0.35, T_RADIO+0.25))
    ctx.save(); ctx.translate(-pan*W*0.5, 0)
    # left panel: rear-view mirror with cruiser
    ctx.rectangle(0, 0, W, H); ctx.set_source_rgba(0.10, 0.16, 0.30, 1); ctx.fill()
    ctx.save(); ctx.translate(W*0.5, H*0.5)
    paper(ctx, lambda k: rrect(k, -520, -220, 1040, 440, 200), (0.15, 0.15, 0.2, 1))
    ctx.save(); rrect(ctx, -490, -195, 980, 390, 180); ctx.clip(); bg(ctx, (0.55, 0.80, 0.85, 1), (0.3, 0.4, 0.5, 1))
    ctx.rectangle(-600, 40, 1200, 300); ctx.set_source_rgba(0.2, 0.2, 0.25, 1); ctx.fill()
    s = 1.0+0.15*math.sin(lt*2)
    ctx.save(); ctx.translate(0, 60); ctx.scale(s, s)
    paper(ctx, lambda k: rrect(k, -170, -120, 340, 160, 30), c('white'))
    ctx.rectangle(-120, -100, 240, 60); ctx.set_source_rgba(*c('ink')); ctx.fill()
    fl = int(T*8) % 2
    ctx.rectangle(-110, -150, 100, 34); ctx.set_source_rgba(*(c('red') if fl else c('blue'))); ctx.fill()
    ctx.rectangle(10, -150, 100, 34); ctx.set_source_rgba(*(c('blue') if fl else c('red'))); ctx.fill()
    ctx.restore(); ctx.restore(); ctx.restore()
    xp = back(prog(T, T_NOT+1.0, T_NOT+1.3))
    if xp > 0:
        ctx.save(); ctx.translate(W*0.5, H*0.5); ctx.scale(xp, xp); ctx.set_line_width(48); ctx.set_line_cap(cairo.LINE_CAP_ROUND)
        ctx.set_source_rgba(*c('red', 0.92)); ctx.move_to(-260, -200); ctx.line_to(260, 200); ctx.move_to(260, -200); ctx.line_to(-260, 200); ctx.stroke(); ctx.restore()
    kword(ctx, "NOT THE OFFICER", W*0.5, 120, 96, c('cream'), T, T_NOT+0.1)
    # right panel: oscilloscope radio
    ctx.rectangle(W, 0, W, H); ctx.set_source_rgba(0.05, 0.08, 0.10, 1); ctx.fill()
    for gx in range(0, W, 80):
        ctx.rectangle(W+gx, 0, 1, H); ctx.set_source_rgba(0.2, 0.9, 0.6, 0.1); ctx.fill()
    for gy in range(0, H, 80):
        ctx.rectangle(W, gy, W, 1); ctx.set_source_rgba(0.2, 0.9, 0.6, 0.1); ctx.fill()
    ctx.move_to(W, H/2)
    for x in range(0, W, 6):
        y = H/2 + math.sin(x*0.03 + lt*14)*120*math.sin(x*0.004+lt*3) + math.sin(x*0.11+lt*30)*25
        ctx.line_to(W+x, y)
    ctx.set_line_width(6); ctx.set_source_rgba(0.3, 1, 0.7, 0.9); ctx.stroke()
    kword(ctx, "THE RADIO.", W*1.5, 160, 140, c('yellow'), T, T_RADIO+0.1)
    ctx.restore()

def sc_score(ctx, lt, T):
    bg(ctx, (0.07, 0.10, 0.20, 1), (0.03, 0.05, 0.10, 1))
    z = 1.0 + 0.10*ease(prog(lt, 0, 3)); slam = prog(T, T_LOST+1.05, T_LOST+1.2)
    sh = shake(T, 22*(1-prog(T, T_LOST+1.2, T_LOST+1.7)) if slam > 0 else 1.5)
    ctx.save(); ctx.translate(W/2+sh[0], H/2+sh[1]); ctx.scale(z, z); ctx.translate(-W/2, -H/2)
    # scoreboard
    paper(ctx, lambda k: rrect(k, W/2-640, 180, 1280, 300, 26), (0.12, 0.14, 0.2, 1))
    text(ctx, "RADIO", W/2-330, 240, 48, c('grey')); text(ctx, "YOU", W/2+330, 240, 48, c('grey'))
    flips = int(min(1, prog(lt, 0.2, 1.4))*30)
    rv = ["0", "12", "348", "9,999", "1,000,000", "∞"][min(5, flips//5)]
    for x0, v, col in ((W/2-330, rv, c('hivis')), (W/2+330, "0", c('cream'))):
        paper(ctx, lambda k, x0=x0: rrect(k, x0-260, 290, 520, 160, 14), (0.06, 0.07, 0.11, 1), off=(3, 4))
        ctx.rectangle(x0-260, 369, 520, 3); ctx.set_source_rgba(0, 0, 0, 0.6); ctx.fill()
        text(ctx, v, x0, 372, 110, col)
    lines = [(["AND", "THE", "RADIO"], 650, 100), (["HAS", "NEVER", "LOST."], 800, 130)]
    k = 0
    for ws, yy, sz in lines:
        ctx.select_font_face('Inter Display', cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD); ctx.set_font_size(sz)
        widths = [ctx.text_extents(w_).x_advance for w_ in ws]; gap = sz*0.35
        x = W/2 - (sum(widths)+gap*(len(ws)-1))/2
        for w_, wd in zip(ws, widths):
            t0 = T_LOST + k*0.2 if w_ != "LOST." else T_LOST+1.05
            kword(ctx, w_, x+wd/2, yy, sz, c('red') if w_ == "LOST." else c('cream'), T, t0, pop=0.18)
            x += wd+gap; k += 1
    ctx.restore()
    if slam > 0 and T < T_LOST+1.4:
        ctx.set_source_rgba(1, 1, 1, 0.5*(1-prog(T, T_LOST+1.05, T_LOST+1.4))); ctx.paint()

SCENES = [sc_title, sc_highway, sc_radio, sc_number, sc_map, sc_split, sc_score]

def scene_surface(i, T):
    s = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H); k = cairo.Context(s)
    SCENES[i](k, T-B[i], T); return s

def blur_paint(ctx, surf, dx, dy, n=8, rot=0.0, zoom=0.0):
    for j in range(n):
        f = j/(n-1)-0.5
        ctx.save(); ctx.translate(W/2+dx*f, H/2+dy*f); ctx.rotate(rot*f); ctx.scale(1+zoom*f, 1+zoom*f); ctx.translate(-W/2, -H/2)
        ctx.set_source_surface(surf, 0, 0); ctx.paint_with_alpha(1.0/(j+1)); ctx.restore()

def frame(T):
    out = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H); ctx = cairo.Context(out)
    ctx.set_source_rgb(0, 0, 0); ctx.paint()
    idx = max(i for i in range(len(SCENES)) if B[i] <= T)
    # transition handling
    for bi in range(1, len(B)-1):
        if abs(T-B[bi]) < TW:
            kind = TRANS[bi-1]; p = (T-(B[bi]-TW))/(2*TW)  # 0..1
            a, b = bi-1, bi
            sa = scene_surface(a, T); sb = scene_surface(b, T)
            if kind in ('whip_l', 'whip_u'):
                horiz = kind == 'whip_l'; e = ease(p); sp = math.sin(p*math.pi)
                off = -e*(W if horiz else H)
                for surf, o in ((sa, off), (sb, off+(W if horiz else H))):
                    ctx.save(); ctx.translate(*( (o, 0) if horiz else (0, -o) ))
                    blur_paint(ctx, surf, (500*sp if horiz else 0), (0 if horiz else 500*sp), n=7)
                    ctx.restore()
            elif kind == 'flash':
                ctx.set_source_surface(sa if p < 0.5 else sb, 0, 0); ctx.paint()
                ctx.set_source_rgba(1, 1, 1, max(0, 1-abs(p-0.5)*3.2)); ctx.paint()
            elif kind == 'zoom':
                sp = math.sin(p*math.pi)
                if p < 0.5:
                    ctx.save(); ctx.translate(W/2, H/2); ctx.scale(1+4*ease(p*2)**2, 1+4*ease(p*2)**2); ctx.translate(-W/2, -H/2)
                    blur_paint(ctx, sa, 0, 0, n=6, zoom=0.25*sp); ctx.restore()
                else:
                    s_ = 1.8-0.8*ease((p-0.5)*2)
                    ctx.save(); ctx.translate(W/2, H/2); ctx.scale(s_, s_); ctx.translate(-W/2, -H/2)
                    blur_paint(ctx, sb, 0, 0, n=6, zoom=0.25*sp); ctx.restore()
            elif kind == 'spin':
                sp = math.sin(p*math.pi); surf = sa if p < 0.5 else sb
                ang = (p-0.5)*1.4
                ctx.save(); ctx.translate(W/2, H/2); ctx.rotate(ang); ctx.scale(1+0.5*sp, 1+0.5*sp); ctx.translate(-W/2, -H/2)
                blur_paint(ctx, surf, 0, 0, n=7, rot=0.35*sp); ctx.restore()
            grain(ctx, 0.08); vignette(ctx, 0.4)
            return out
    s = scene_surface(idx, T); ctx.set_source_surface(s, 0, 0); ctx.paint()
    grain(ctx, 0.08); vignette(ctx, 0.4)
    return out

# ---------------- audio ----------------
def audio(path, sr=48000):
    n = int(DUR*sr); t = np.arange(n)/sr; out = np.zeros(n)
    rng = np.random.default_rng(1)
    def add(sig, at):
        i = int(at*sr); j = min(n, i+len(sig))
        if i < n: out[i:j] += sig[:j-i]
    def kick():
        tt = np.arange(int(0.35*sr))/sr; f = 50+90*np.exp(-tt*28)
        return np.sin(2*np.pi*np.cumsum(f)/sr)*np.exp(-tt*9)*0.9
    def hat():
        tt = np.arange(int(0.06*sr))/sr; w = rng.normal(0, 1, len(tt)); w = np.diff(np.concatenate([[0], w]))
        return w*np.exp(-tt*70)*0.12
    def whoosh(d=0.6, up=True):
        m = int(d*sr); w = rng.normal(0, 1, m); env = np.sin(np.linspace(0, np.pi, m))**2
        # crude band sweep via moving-average of varying length
        acc = np.cumsum(w); k = np.linspace(40, 4, m).astype(int) if up else np.linspace(4, 40, m).astype(int)
        idx = np.arange(m); lo = np.maximum(0, idx-k); sig = (acc[idx]-acc[lo])/k
        return sig*env*0.6
    def impact():
        tt = np.arange(int(0.9*sr))/sr
        return (np.sin(2*np.pi*(45+60*np.exp(-tt*10))*tt)*np.exp(-tt*4)*0.9 + rng.normal(0, 1, len(tt))*np.exp(-tt*25)*0.25)
    def riser(d):
        m = int(d*sr); tt = np.arange(m)/sr; f = 200+1800*(tt/d)**2
        return np.sin(2*np.pi*np.cumsum(f)/sr)*(tt/d)**2*0.12 + rng.normal(0, 1, m)*(tt/d)**3*0.06
    bpm = 124; beat = 60/bpm
    # driving beat from the car scene to the end, drops out for the map 'reveal' breath
    bt = B[1]
    while bt < DUR-0.6:
        if not (19.3 < bt < 20.7):
            add(kick(), bt)
        add(hat(), bt+beat/2)
        bt += beat
    # bass pulse
    bass = np.zeros(n); notes = [41.2, 41.2, 49.0, 36.7]
    for i in range(int((DUR-B[1])/(beat*4))+1):
        st = B[1]+i*beat*4; f = notes[i % 4]
        i0 = int(st*sr); i1 = min(n, int((st+beat*4)*sr))
        tt = np.arange(i1-i0)/sr
        bass[i0:i1] += np.sign(np.sin(2*np.pi*f*tt))*0.05*np.exp(-((tt % beat))*3)
    out += bass
    for bnd in B[1:-1]:
        add(whoosh(0.7), bnd-0.35)
    add(riser(1.6), B[1]-1.6+0.05)
    for at in (0.55, 4.2, T_APART+0.25, T_LIGHT+1.2, T_NUM+1.8, 17.2, T_NOT+1.0, T_RADIO+0.1, T_LOST+1.05):
        add(impact()*0.8, at)
    # hubcap clatter
    for i in range(5):
        add(hat()*4, T_APART+0.3+i*0.09)
    out = np.clip(out, -1, 1)
    pcm = (out*32767*0.8).astype(np.int16)
    import wave
    with wave.open(path, 'wb') as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr); w.writeframes(pcm.tobytes())

if __name__ == '__main__':
    mode = sys.argv[1]
    if mode == 'still':
        frame(float(sys.argv[2])).write_to_png(sys.argv[3])
    elif mode == 'audio':
        audio(sys.argv[2])
    elif mode == 'video':
        out, t0, t1 = sys.argv[2], float(sys.argv[3]), float(sys.argv[4])
        p = subprocess.Popen(['ffmpeg', '-y', '-v', 'error', '-f', 'rawvideo', '-pix_fmt', 'bgra', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                              '-c:v', 'libx264', '-preset', 'medium', '-crf', '18', '-pix_fmt', 'yuv420p', out], stdin=subprocess.PIPE)
        for f in range(int(round(t0*FPS)), int(round(t1*FPS))):
            s = frame(f/FPS); p.stdin.write(bytes(s.get_data()))
        p.stdin.close(); p.wait()
