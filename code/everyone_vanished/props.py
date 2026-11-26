"""Props for episode 2, flat paper style (pycairo)."""
import os, math, cairo, numpy as np, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'pilot'))
from style import *

SKIES = {
    'day':   ((0.55, 0.80, 0.88), (0.86, 0.93, 0.92)),
    'dawn':  ((0.98, 0.78, 0.60), (0.99, 0.90, 0.78)),
    'dusk':  ((0.98, 0.62, 0.38), (0.40, 0.25, 0.45)),
    'night': ((0.03, 0.05, 0.12), (0.10, 0.15, 0.28)),
    'gray':  ((0.55, 0.60, 0.66), (0.80, 0.82, 0.84)),
}
def sky(ctx, mode='day', y0=0, y1=H):
    a, b = SKIES[mode]; g = cairo.LinearGradient(0, y0, 0, y1)
    g.add_color_stop_rgb(0, *a); g.add_color_stop_rgb(1, *b); ctx.set_source(g); ctx.paint()

def stars(ctx, n=220, seed=2, alpha=1.0, y1=H*0.8):
    rng = np.random.default_rng(seed)
    for i in range(n):
        x, y, r = rng.uniform(0, W), rng.uniform(0, y1), rng.uniform(0.8, 2.6)
        ctx.arc(x, y, r, 0, 2*math.pi); ctx.set_source_rgba(1, 1, 0.95, alpha*rng.uniform(0.4, 1)); ctx.fill()

def milky_way(ctx, alpha=1.0, seed=5):
    rng = np.random.default_rng(seed)
    ctx.save(); ctx.translate(W/2, H*0.35); ctx.rotate(-0.45)
    for i in range(14):
        ctx.save(); ctx.scale(1, 0.12+0.02*i); ctx.arc(0, 0, 1300-i*40, 0, 2*math.pi); ctx.restore()
        ctx.set_source_rgba(0.75, 0.72, 0.95, alpha*0.035); ctx.fill()
    for i in range(900):
        x = rng.normal(0, 600); y = rng.normal(0, 70)
        ctx.arc(x, y, rng.uniform(0.6, 2.0), 0, 2*math.pi); ctx.set_source_rgba(1, 1, 1, alpha*rng.uniform(0.2, 0.9)); ctx.fill()
    ctx.restore()

def skyline(ctx, offset, base, hmin, hmax, col, lit=0.35, seed=1, win_col=(1, 0.85, 0.45), wmin=90, wmax=240, span=W*3, win_alpha=0.9):
    rng = np.random.default_rng(seed); xs = []; x = 0
    while x < span:
        w = rng.uniform(wmin, wmax); h = rng.uniform(hmin, hmax); xs.append((x, w, h)); x += w + rng.uniform(4, 30)
    total = x
    for (bx, w, h) in xs:
        X = (bx - offset) % total - 300
        if X > W+300 or X+w < -300: continue
        ctx.rectangle(X, base-h, w, h); ctx.set_source_rgba(*col); ctx.fill()
        if lit > 0:
            r2 = np.random.default_rng(int(bx*7) % 100000)
            for wy in np.arange(base-h+20, base-20, 34):
                for wx in np.arange(X+12, X+w-20, 28):
                    if r2.random() < lit:
                        ctx.rectangle(wx, wy, 12, 16); ctx.set_source_rgba(*win_col, win_alpha); ctx.fill()

def ground(ctx, y, col=(0.16, 0.17, 0.22, 1)):
    ctx.rectangle(-W, y, W*3, H*2); ctx.set_source_rgba(*col); ctx.fill()

def road(ctx, y, h=180, dash_off=0, col=(0.20, 0.21, 0.26, 1)):
    ctx.rectangle(-W, y, W*3, h); ctx.set_source_rgba(*col); ctx.fill()
    for i in range(-10, 30):
        ctx.rectangle(i*260 - dash_off % 260, y+h/2-6, 130, 12); ctx.set_source_rgba(*c('yellow', 0.85)); ctx.fill()
    ctx.rectangle(-W, y-18, W*3, 18); ctx.set_source_rgba(0.62, 0.62, 0.66, 1); ctx.fill()

def house(ctx, x, y, w=320, h=220, body=(0.93, 0.86, 0.74, 1), roof=(0.70, 0.27, 0.25, 1), lit=False, solar=False, door=True, decay=0.0, glow=0.0):
    """(x,y) = bottom-left. decay 0..1 sags the roof and fades walls."""
    ctx.save()
    sag = decay*60
    paper(ctx, lambda k: k.rectangle(x, y-h, w, h), body)
    def rf(k):
        k.new_path(); k.move_to(x-25, y-h); k.line_to(x+w/2, y-h-130+sag); k.line_to(x+w+25, y-h); k.close_path()
    if decay < 0.95: paper(ctx, rf, roof, off=(5, 6))
    if solar:
        for i in range(3):
            ctx.save(); ctx.translate(x+w*0.55+i*36, y-h-55+i*-14); ctx.rotate(-0.6)
            ctx.rectangle(0, 0, 34, 52); ctx.set_source_rgba(0.12, 0.25, 0.48, 1); ctx.fill()
            ctx.rectangle(2, 25, 30, 2); ctx.set_source_rgba(0.6, 0.75, 0.95, 0.6); ctx.fill(); ctx.restore()
    for wx in (x+40, x+w-110):
        ctx.rectangle(wx, y-h+50, 70, 60)
        ctx.set_source_rgba(*((1, 0.85, 0.45, 1) if lit else (0.16, 0.20, 0.30, 1))); ctx.fill()
    if door:
        ctx.rectangle(x+w/2-30, y-110, 60, 110); ctx.set_source_rgba(0.35, 0.22, 0.16, 1); ctx.fill()
    if glow > 0:
        g = cairo.RadialGradient(x+w/2, y-h/2, 10, x+w/2, y-h/2, 600)
        g.add_color_stop_rgba(0, 1, 0.8, 0.4, 0.35*glow); g.add_color_stop_rgba(1, 1, 0.8, 0.4, 0)
        ctx.set_source(g); ctx.arc(x+w/2, y-h/2, 600, 0, 2*math.pi); ctx.fill()
    if decay > 0.3:
        for i in range(int(decay*8)):
            ctx.move_to(x+20+i*35, y); ctx.curve_to(x+10+i*35, y-60*decay, x+40+i*35, y-120*decay, x+25+i*35, y-180*decay)
            ctx.set_line_width(6); ctx.set_source_rgba(0.25, 0.55, 0.30, 0.9); ctx.stroke()
    ctx.restore()

def tree(ctx, x, y, s=1.0, col=(0.20, 0.50, 0.34, 1)):
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    ctx.rectangle(-10, -90, 20, 90); ctx.set_source_rgba(0.40, 0.28, 0.20, 1); ctx.fill()
    for (dx, dy, r) in ((0, -150, 70), (-45, -115, 50), (45, -115, 50)):
        paper(ctx, lambda k, dx=dx, dy=dy, r=r: (k.new_path(), k.arc(dx, dy, r, 0, 2*math.pi)), col, off=(4, 5))
    ctx.restore()

def bin_(ctx, x, y, ang=0.0, s=1.0):
    ctx.save(); ctx.translate(x, y); ctx.rotate(ang); ctx.scale(s, s)
    paper(ctx, lambda k: (k.new_path(), k.move_to(-45, -120), k.line_to(45, -120), k.line_to(36, 0), k.line_to(-36, 0), k.close_path()), (0.30, 0.36, 0.40, 1))
    ctx.rectangle(-52, -132, 104, 16); ctx.set_source_rgba(0.22, 0.27, 0.30, 1); ctx.fill()
    ctx.restore()

def phone(ctx, x, y, s=1.0):
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    paper(ctx, lambda k: rrect(k, -200, -400, 400, 800, 48), (0.08, 0.09, 0.12, 1))
    rrect(ctx, -180, -370, 360, 740, 30); ctx.set_source_rgba(0.12, 0.16, 0.26, 1); ctx.fill()
    ctx.restore()

def stopwatch(ctx, x, y, r, frac, label=None, val=None, col=None):
    """Big stopwatch: frac 0..1 sweep of the hand."""
    ctx.save(); ctx.translate(x, y)
    paper(ctx, lambda k: rrect(k, -r*0.16, -r*1.28, r*0.32, r*0.22, 6), c('cream'))
    paper(ctx, lambda k: (k.new_path(), k.arc(0, 0, r, 0, 2*math.pi)), c('cream'))
    ctx.arc(0, 0, r*0.86, 0, 2*math.pi); ctx.set_source_rgba(*c('ink')); ctx.fill()
    for i in range(60):
        a = i/60*2*math.pi; l = 0.12 if i % 5 == 0 else 0.05
        ctx.move_to(math.sin(a)*r*0.80, -math.cos(a)*r*0.80); ctx.line_to(math.sin(a)*r*(0.80-l), -math.cos(a)*r*(0.80-l))
        ctx.set_line_width(4 if i % 5 == 0 else 2); ctx.set_source_rgba(1, 1, 1, 0.7); ctx.stroke()
    a = frac*2*math.pi
    ctx.arc(0, 0, r*0.62, -math.pi/2, -math.pi/2+a); ctx.set_line_width(r*0.08)
    ctx.set_source_rgba(*(col or c('hivis'))); ctx.stroke()
    ctx.move_to(0, 0); ctx.line_to(math.sin(a)*r*0.72, -math.cos(a)*r*0.72); ctx.set_line_width(r*0.035); ctx.set_source_rgba(*c('red')); ctx.stroke()
    ctx.arc(0, 0, r*0.06, 0, 2*math.pi); ctx.set_source_rgba(*c('cream')); ctx.fill()
    if val:
        fs = r*0.2
        ctx.select_font_face('Inter Display', cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD); ctx.set_font_size(fs)
        w_ = ctx.text_extents(val).width
        if w_ > r*0.95: fs *= r*0.95/w_
        text(ctx, val, 0, r*0.36, fs, c('cream'))
    ctx.restore()

QUAD = {
  'dog':   dict(body=(0.78, 0.60, 0.40, 1), dark=(0.45, 0.32, 0.22, 1), ears='flop', leg=1.0, size=1.0, tail='wag', snout=1.0),
  'cat':   dict(body=(0.30, 0.30, 0.34, 1), dark=(0.18, 0.18, 0.22, 1), ears='point', leg=0.8, size=0.6, tail='up', snout=0.5),
  'deer':  dict(body=(0.66, 0.45, 0.28, 1), dark=(0.45, 0.30, 0.18, 1), ears='point', leg=1.7, size=1.15, tail='short', snout=0.9),
  'pig':   dict(body=(0.92, 0.66, 0.66, 1), dark=(0.80, 0.48, 0.50, 1), ears='point', leg=0.6, size=1.1, tail='curl', snout=0.7),
  'boar':  dict(body=(0.36, 0.28, 0.22, 1), dark=(0.22, 0.16, 0.12, 1), ears='point', leg=0.7, size=1.1, tail='short', snout=0.9),
  'zebra': dict(body=(0.96, 0.95, 0.92, 1), dark=(0.10, 0.10, 0.12, 1), ears='point', leg=1.6, size=1.3, tail='short', snout=1.1, stripes=True),
  'horse': dict(body=(0.52, 0.32, 0.20, 1), dark=(0.24, 0.15, 0.10, 1), ears='point', leg=1.7, size=1.35, tail='long', snout=1.2),
  'wolf':  dict(body=(0.55, 0.57, 0.62, 1), dark=(0.30, 0.32, 0.38, 1), ears='point', leg=1.1, size=1.05, tail='long', snout=1.1),
  'cow':   dict(body=(0.96, 0.94, 0.90, 1), dark=(0.15, 0.13, 0.12, 1), ears='flop', leg=1.0, size=1.4, tail='long', snout=0.9, spots=True),
  'coyote':dict(body=(0.72, 0.58, 0.40, 1), dark=(0.45, 0.36, 0.26, 1), ears='point', leg=1.1, size=0.95, tail='long', snout=1.1),
  'rat':   dict(body=(0.45, 0.42, 0.42, 1), dark=(0.30, 0.28, 0.28, 1), ears='round', leg=0.4, size=0.35, tail='thin', snout=0.8),
}
def quad(ctx, x, y, kind='dog', s=1.0, phase=0.0, run=0.0, face=1, sil=None, alpha=1.0):
    """Side-view quadruped. (x,y)=feet centre. face=1 right, -1 left. sil = flat colour for silhouettes."""
    q = QUAD[kind]; S = s*q['size']; L = 60*q['leg']
    body = sil or q['body']; dark = sil or q['dark']
    ctx.save(); ctx.translate(x, y); ctx.scale(face*S, S)
    bob = abs(math.sin(phase))*8*run
    ctx.translate(0, -bob)
    sw = math.sin(phase)*0.6*run
    ctx.set_line_cap(cairo.LINE_CAP_ROUND)
    for lx, ph, colr in ((-55, sw, dark), (55, -sw, dark), (-40, -sw, body), (70, sw, body)):
        ctx.move_to(lx, -L-20); ctx.line_to(lx+math.sin(ph)*L*0.6, -4); ctx.set_line_width(16); ctx.set_source_rgba(*colr[:3], alpha); ctx.stroke()
    ctx.save(); ctx.translate(0, -L-45); ctx.scale(1, 0.55); ctx.arc(0, 0, 95, 0, 2*math.pi); ctx.restore()
    ctx.set_source_rgba(*body[:3], alpha); ctx.fill()
    if q.get('stripes') and not sil:
        for i in range(7):
            ctx.save(); ctx.translate(-70+i*24, -L-45); ctx.rotate(0.2)
            ctx.rectangle(-5, -45, 10, 90); ctx.restore()
        ctx.set_source_rgba(*dark[:3], alpha); ctx.fill()
    if q.get('spots') and not sil:
        for (sx, sy, r) in ((-30, -L-55, 22), (35, -L-40, 18), (0, -L-30, 12)):
            ctx.arc(sx, sy, r, 0, 2*math.pi); ctx.set_source_rgba(*dark[:3], alpha); ctx.fill()
    # tail
    t = q['tail']; wag = math.sin(phase*3)*0.5 if t == 'wag' else 0
    ctx.save(); ctx.translate(-90, -L-55); ctx.rotate(-0.9+wag)
    tl = {'wag': 55, 'up': 70, 'short': 22, 'curl': 25, 'long': 75, 'thin': 90}[t]
    ctx.move_to(0, 0); ctx.curve_to(-10, -tl*0.4, -20, -tl*0.8, -5 if t == 'curl' else -25, -tl)
    ctx.set_line_width(4 if t == 'thin' else 13); ctx.set_source_rgba(*dark[:3], alpha); ctx.stroke(); ctx.restore()
    # neck + head
    hx, hy = 100, -L-95 - (25 if q['leg'] > 1.4 else 0)
    ctx.move_to(60, -L-55); ctx.line_to(hx-10, hy+10); ctx.set_line_width(40); ctx.set_source_rgba(*body[:3], alpha); ctx.stroke()
    ctx.arc(hx, hy, 34, 0, 2*math.pi); ctx.set_source_rgba(*body[:3], alpha); ctx.fill()
    sn = q['snout']
    ctx.save(); ctx.translate(hx+30*sn, hy+10); ctx.scale(1, 0.7); ctx.arc(0, 0, 22*sn, 0, 2*math.pi); ctx.restore()
    ctx.set_source_rgba(*body[:3], alpha); ctx.fill()
    ctx.arc(hx+48*sn, hy+6, 7, 0, 2*math.pi); ctx.set_source_rgba(*(sil or (0.1, 0.08, 0.08, 1))[:3], alpha); ctx.fill()
    if not sil:
        ctx.arc(hx+10, hy-8, 5, 0, 2*math.pi); ctx.set_source_rgba(0.08, 0.08, 0.1, alpha); ctx.fill()
    e = q['ears']
    if e == 'point':
        ctx.move_to(hx-20, hy-20); ctx.line_to(hx-8, hy-62); ctx.line_to(hx+6, hy-26); ctx.close_path()
    elif e == 'flop':
        ctx.save(); ctx.translate(hx-18, hy-10); ctx.rotate(0.3+0.15*math.sin(phase*2)); ctx.scale(0.5, 1); ctx.arc(0, 12, 22, 0, 2*math.pi); ctx.restore()
    else:
        ctx.arc(hx-10, hy-26, 14, 0, 2*math.pi)
    ctx.set_source_rgba(*dark[:3], alpha); ctx.fill()
    ctx.restore()

def eyes_pair(ctx, x, y, s=1.0, a=1.0, col=(1.0, 0.85, 0.3)):
    for dx in (-14*s, 14*s):
        g = cairo.RadialGradient(x+dx, y, 1, x+dx, y, 16*s); g.add_color_stop_rgba(0, *col, a); g.add_color_stop_rgba(1, *col, 0)
        ctx.set_source(g); ctx.arc(x+dx, y, 16*s, 0, 2*math.pi); ctx.fill()
        ctx.arc(x+dx, y, 4*s, 0, 2*math.pi); ctx.set_source_rgba(*col, a); ctx.fill()

def chicken(ctx, x, y, s=1.0):
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    ctx.save(); ctx.scale(1, 0.8); ctx.arc(0, -40, 34, 0, 2*math.pi); ctx.restore(); ctx.set_source_rgba(0.98, 0.96, 0.92, 1); ctx.fill()
    ctx.arc(26, -70, 16, 0, 2*math.pi); ctx.fill()
    ctx.move_to(40, -72); ctx.line_to(54, -66); ctx.line_to(40, -62); ctx.close_path(); ctx.set_source_rgba(*c('orange')); ctx.fill()
    ctx.arc(24, -88, 7, 0, 2*math.pi); ctx.set_source_rgba(*c('red')); ctx.fill()
    ctx.restore()

def flame(ctx, x, y, s, t, seed=0):
    ctx.save(); ctx.translate(x, y); ctx.scale(s, s)
    for i, (col, sc) in enumerate((((0.95, 0.30, 0.15), 1.0), ((1.0, 0.60, 0.15), 0.7), ((1.0, 0.88, 0.40), 0.4))):
        w = math.sin(t*9+seed+i)*8
        ctx.move_to(-60*sc, 0); ctx.curve_to(-70*sc, -80*sc, -10*sc+w, -120*sc, 0+w, -200*sc)
        ctx.curve_to(10*sc+w, -120*sc, 70*sc, -80*sc, 60*sc, 0); ctx.close_path()
        ctx.set_source_rgba(*col, 0.95); ctx.fill()
    ctx.restore()

def stamp(ctx, s_, x, y, size, col, lt, t0, rot=-0.12):
    p = prog(lt, t0, t0+0.18)
    if p <= 0: return
    sc = 1+1.2*(1-ease(p)); ctx.save(); ctx.translate(x, y); ctx.rotate(rot); ctx.scale(sc, sc)
    ctx.select_font_face('Inter Display', cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD); ctx.set_font_size(size)
    e = ctx.text_extents(s_); pad = size*0.3
    rrect(ctx, -e.width/2-pad, -size*0.55-pad*0.6, e.width+2*pad, size*1.1+pad*1.2, 10)
    ctx.set_line_width(size*0.09); ctx.set_source_rgba(*col[:3], 0.9*ease(p)); ctx.stroke()
    text(ctx, s_, 0, 0, size, (*col[:3], 0.9*ease(p))); ctx.restore()
