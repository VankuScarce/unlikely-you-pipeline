"""Sample scenes, one per character style. scene_X(ctx, t) draws a 1920x1080 frame at time t (0..DUR)."""
import math, random, os, cairo
import numpy as np
from rig import pose, contact_shadow
from styles import ink_line, silhouette, geometric, mannequin, ink_wash, graphic

W, H = 1920, 1080
DUR = 5.0
HERE = os.path.dirname(os.path.abspath(__file__))
BG = os.path.join(HERE, '..', 'bg')
_cache = {}

def img(name):
    if name not in _cache: _cache[name] = cairo.ImageSurface.create_from_png(os.path.join(BG, name))
    return _cache[name]

def paint_bg(ctx, name, zoom=1.0, cx=0.5, cy=0.5, dx=0.0):
    im = img(name); sc = max(W/im.get_width(), H/im.get_height())*zoom
    ctx.save(); ctx.translate(W*cx + dx, H*cy); ctx.scale(sc, sc)
    ctx.translate(-im.get_width()*cx, -im.get_height()*cy)
    ctx.set_source_surface(im, 0, 0); ctx.get_source().set_filter(cairo.FILTER_GOOD); ctx.paint(); ctx.restore()

def ease(x): x = max(0.0, min(1.0, x)); return x*x*(3-2*x)

def text(ctx, s, x, y, size, col, font='Inter Display', weight=cairo.FONT_WEIGHT_BOLD, anchor='l', spacing=0):
    ctx.select_font_face(font, cairo.FONT_SLANT_NORMAL, weight); ctx.set_font_size(size)
    if spacing:
        widths = [ctx.text_extents(ch).x_advance + spacing for ch in s]; tw = sum(widths) - spacing
    else: tw = ctx.text_extents(s).x_advance
    x0 = x - (tw if anchor == 'r' else tw/2 if anchor == 'c' else 0)
    ctx.set_source_rgba(*col)
    if spacing:
        for ch, w in zip(s, widths): ctx.move_to(x0, y); ctx.show_text(ch); x0 += w
    else: ctx.move_to(x0, y); ctx.show_text(s)
    return tw

def rrect(ctx, x, y, w, h, r):
    ctx.new_sub_path(); ctx.arc(x+w-r, y+r, r, -math.pi/2, 0); ctx.arc(x+w-r, y+h-r, r, 0, math.pi/2)
    ctx.arc(x+r, y+h-r, r, math.pi/2, math.pi); ctx.arc(x+r, y+r, r, math.pi, 1.5*math.pi); ctx.close_path()

def card(ctx, x, y, lines, t_in, t, dark=False):
    """White diagram card that slides up and fades in."""
    k = ease((t - t_in)/0.45)
    if k <= 0: return
    ctx.save(); ctx.translate(0, (1-k)*24); ctx.push_group()
    w = max(len(l[0])*l[1]*0.56 for l in lines) + 56; h = sum(l[1]*1.25 for l in lines) + 36
    rrect(ctx, x+4, y+6, w, h, 14); ctx.set_source_rgba(0, 0, 0, 0.25); ctx.fill()
    rrect(ctx, x, y, w, h, 14); ctx.set_source_rgba(*((0.08, 0.09, 0.12, 0.88) if dark else (0.97, 0.96, 0.93, 0.95))); ctx.fill()
    yy = y + 18
    for s, size, col in lines:
        yy += size*1.05; text(ctx, s, x+28, yy, size, col); yy += size*0.2
    ctx.pop_group_to_source(); ctx.paint_with_alpha(k); ctx.restore()

_rng = np.random.default_rng(7)
_noise = _rng.integers(0, 255, (H+64, W+64), dtype=np.uint8)
def grain(ctx, t, amount=0.06):
    a = np.zeros((H, W, 4), dtype=np.uint8)
    ox, oy = int(t*977) % 64, int(t*631) % 64
    n = _noise[oy:oy+H, ox:ox+W]
    a[..., 0] = a[..., 1] = a[..., 2] = (n.astype(np.uint16)*int(amount*255)//255).astype(np.uint8)
    a[..., 3] = int(amount*255)
    sf = cairo.ImageSurface.create_for_data(a, cairo.FORMAT_ARGB32, W, H)
    ctx.set_operator(cairo.OPERATOR_SOFT_LIGHT if hasattr(cairo, 'OPERATOR_SOFT_LIGHT') else cairo.OPERATOR_OVER)
    ctx.set_source_surface(sf, 0, 0); ctx.paint(); ctx.set_operator(cairo.OPERATOR_OVER)

def vignette(ctx, strength=0.55, col=(0, 0, 0)):
    g = cairo.RadialGradient(W/2, H/2, H*0.35, W/2, H/2, H*1.0)
    g.add_color_stop_rgba(0, *col, 0); g.add_color_stop_rgba(1, *col, strength)
    ctx.rectangle(0, 0, W, H); ctx.set_source(g); ctx.fill()

def walker(t, x0, x1, t_walk, speed_phase=5.4):
    """Walk from x0 to x1 during [0, t_walk], then settle to idle."""
    k = min(1.0, t/t_walk); x = x0 + (x1-x0)*(k*(2-k) if False else k)
    run = 0.5 if t < t_walk else max(0.0, 0.5 - (t-t_walk)*2.5)
    ph = speed_phase*min(t, t_walk) + (0 if t < t_walk else 0)
    return x, ph, run

# ---------------------------------------------------------------- A
def scene_ink_line(ctx, t):
    paint_bg(ctx, 'stairwell.png', zoom=1.02 + 0.05*t/DUR, cx=0.55, cy=0.6)
    x, ph, run = walker(t, 520, 860, 3.0)
    fx, fy, s = x, 965, 1.18
    contact_shadow(ctx, fx+10, fy, s, 0.45)
    P = pose(ph, run, t=t)
    ctx.push_group(); ink_line(ctx, fx+3, fy-2, s, P); m = ctx.pop_group()     # cold moonlight rim
    ctx.set_source_rgba(0.62, 0.80, 1.0, 0.85); ctx.mask(m)
    ink_line(ctx, fx, fy, s, P)
    # breath fog
    for k in range(4):
        tb = (t - k*1.5)
        if 0 < tb < 1.6:
            hx = fx + (P['head'][0]+40)*s + tb*60; hy = fy + (P['head'][1]+18-P['bob'])*s - tb*28
            r = 14 + tb*40; a = 0.28*(1 - tb/1.6)
            g = cairo.RadialGradient(hx, hy, 0, hx, hy, r); g.add_color_stop_rgba(0, 0.9, 0.95, 1, a); g.add_color_stop_rgba(1, 0.9, 0.95, 1, 0)
            ctx.arc(hx, hy, r, 0, 2*math.pi); ctx.set_source(g); ctx.fill()
    rnd = random.Random(3)
    for i in range(70):   # drifting frost specks
        px = (rnd.uniform(0, W) + t*rnd.uniform(-8, 14)) % W; py = (rnd.uniform(0, H) + t*rnd.uniform(10, 30)) % H
        ctx.arc(px, py, rnd.uniform(1, 2.6), 0, 2*math.pi); ctx.set_source_rgba(0.85, 0.93, 1, rnd.uniform(0.2, 0.6)); ctx.fill()
    vignette(ctx, 0.55, (0.0, 0.03, 0.08))
    card(ctx, 120, 110, [("HOUR 31", 54, (0.07, 0.07, 0.09, 1)), ("-27 °C inside the building", 30, (0.75, 0.16, 0.14, 1))], 0.5, t)

# ---------------------------------------------------------------- B
def scene_silhouette(ctx, t):
    paint_bg(ctx, 'saltflat.png', zoom=1.06 - 0.03*t/DUR, cx=0.5, cy=0.55, dx=-t*6)
    x = 720 + t*62; ph = t*4.6; fy, s = 790, 0.72
    P = pose(ph, 0.5, t=t)
    # mirror reflection on the wet salt
    ctx.save(); ctx.push_group(); ctx.translate(0, 2*fy); ctx.scale(1, -1)
    silhouette(ctx, x, fy, s, P, lantern=True); ctx.pop_group_to_source(); ctx.paint_with_alpha(0.32); ctx.restore()
    silhouette(ctx, x, fy, s, P)
    vignette(ctx, 0.5, (0.04, 0.0, 0.08))
    k = ease((t-0.6)/0.8)
    text(ctx, "DAY 412", 120, 150, 46, (1, 0.93, 0.85, 0.9*k), weight=cairo.FONT_WEIGHT_NORMAL, spacing=14)
    text(ctx, "no signal since day 3", 122, 196, 26, (1, 0.8, 0.65, 0.7*k), weight=cairo.FONT_WEIGHT_NORMAL, spacing=3)

# ---------------------------------------------------------------- C
def scene_geometric(ctx, t):
    g = cairo.LinearGradient(0, 0, 0, H); g.add_color_stop_rgb(0, 0.03, 0.04, 0.10); g.add_color_stop_rgb(1, 0.08, 0.10, 0.22)
    ctx.rectangle(0, 0, W, H); ctx.set_source(g); ctx.fill()
    rnd = random.Random(11)
    for i in range(160):
        px, py = rnd.uniform(0, W), rnd.uniform(0, H*0.75); tw = 0.5 + 0.5*math.sin(t*rnd.uniform(1, 3) + i)
        ctx.arc(px - t*4, py, rnd.uniform(0.8, 2.2), 0, 2*math.pi); ctx.set_source_rgba(1, 1, 1, 0.25 + 0.5*tw*rnd.random()); ctx.fill()
    # Earth: flat, geometric
    ex, ey, er = 1450 - t*5, 300, 190
    halo = cairo.RadialGradient(ex, ey, er*0.9, ex, ey, er*1.5); halo.add_color_stop_rgba(0, 0.35, 0.65, 1, 0.35); halo.add_color_stop_rgba(1, 0.35, 0.65, 1, 0)
    ctx.arc(ex, ey, er*1.5, 0, 2*math.pi); ctx.set_source(halo); ctx.fill()
    ctx.arc(ex, ey, er, 0, 2*math.pi); ctx.set_source_rgb(0.18, 0.45, 0.85); ctx.fill()
    ctx.save(); ctx.arc(ex, ey, er, 0, 2*math.pi); ctx.clip()
    for (dx, dy, rx, ry, a) in ((-60, -60, 90, 60, 0.3), (70, 40, 70, 110, -0.4), (-90, 90, 60, 40, 0.2)):
        ctx.save(); ctx.translate(ex+dx+t*3, ey+dy); ctx.rotate(a); ctx.scale(rx, ry); ctx.arc(0, 0, 1, 0, 2*math.pi); ctx.restore()
        ctx.set_source_rgb(0.30, 0.68, 0.48); ctx.fill()
    sh = cairo.LinearGradient(ex-er*0.2, ey, ex+er, ey); sh.add_color_stop_rgba(0, 0, 0.02, 0.1, 0); sh.add_color_stop_rgba(0.35, 0, 0.02, 0.1, 0.6); sh.add_color_stop_rgba(1, 0, 0.02, 0.1, 0.75)
    ctx.rectangle(ex-er, ey-er, 2*er, 2*er); ctx.set_source(sh); ctx.fill()   # night side
    ctx.restore()
    # Moon ground: a huge disc
    gx, gy, gr = W/2, 3400, 2620
    ctx.arc(gx, gy, gr, 0, 2*math.pi); ctx.set_source_rgb(0.55, 0.56, 0.62); ctx.fill()
    ctx.save(); ctx.arc(gx, gy, gr, 0, 2*math.pi); ctx.clip()
    rnd = random.Random(5)
    for i in range(14):
        cx = (rnd.uniform(-200, W+200) - t*40) ; cy = rnd.uniform(830, 1080); r = rnd.uniform(30, 120)
        ctx.save(); ctx.translate(cx, cy); ctx.scale(r, r*0.28); ctx.arc(0, 0, 1, 0, 2*math.pi); ctx.restore(); ctx.set_source_rgb(0.44, 0.45, 0.52); ctx.fill()
        ctx.save(); ctx.translate(cx+r*0.1, cy+r*0.04); ctx.scale(r*0.85, r*0.2); ctx.arc(0, 0, 1, 0, 2*math.pi); ctx.restore(); ctx.set_source_rgb(0.38, 0.39, 0.46); ctx.fill()
    ctx.restore()
    # low-gravity bounding walk
    ph = t*3.4; hop = abs(math.sin(ph))*46
    fx, fy, s = 860, 868, 0.95
    ctx.save(); ctx.translate(fx+30, fy); ctx.scale(1, 0.22); ctx.arc(0, 0, 70*(1-hop/120), 0, 2*math.pi); ctx.restore()
    ctx.set_source_rgba(0, 0, 0.05, 0.35); ctx.fill()
    geometric(ctx, fx, fy - hop, s, pose(ph, 0.5, t=t))
    k = ease((t-0.4)/0.5)
    ctx.save(); ctx.translate(140, 190); ctx.scale(0.9+0.1*k, 0.9+0.1*k)
    text(ctx, "1/6", 0, 0, 120, (0.98, 0.78, 0.25, k)); text(ctx, "GRAVITY", 4, 58, 44, (1, 1, 1, k), spacing=6)
    ctx.restore()
    card(ctx, 140, 330, [("You weigh 12 kg here", 32, (0.12, 0.2, 0.29, 1))], 1.6, t)

# ---------------------------------------------------------------- D
def scene_mannequin(ctx, t):
    ctx.rectangle(0, 0, W, H); ctx.set_source_rgb(0.05, 0.11, 0.19); ctx.fill()
    off = (t*900) % 200
    for i in range(-1, W//40 + 2):
        ctx.move_to(i*40, 0); ctx.line_to(i*40, H)
    for j in range(-6, H//40 + 6):
        ctx.move_to(0, j*40 - off % 40); ctx.line_to(W, j*40 - off % 40)
    ctx.set_line_width(1); ctx.set_source_rgba(0.45, 0.70, 1, 0.08); ctx.stroke()
    for j in range(-2, H//200 + 3):
        ctx.move_to(0, j*200 - off); ctx.line_to(W, j*200 - off)
    for i in range(0, W//200 + 2): ctx.move_to(i*200, 0); ctx.line_to(i*200, H)
    ctx.set_line_width(1.5); ctx.set_source_rgba(0.45, 0.70, 1, 0.16); ctx.stroke()
    rnd = random.Random(2)
    for i in range(40):   # wind streaks rushing up
        px = rnd.uniform(0, W); sp = rnd.uniform(1400, 2600); L = rnd.uniform(60, 220)
        py = (rnd.uniform(0, H+400) - t*sp) % (H+400) - 200
        ctx.move_to(px, py); ctx.line_to(px, py+L); ctx.set_line_width(rnd.uniform(1, 2.5)); ctx.set_source_rgba(0.8, 0.9, 1, 0.25); ctx.stroke()
    # falling body, belly down, arms out
    P = pose(0.4, 0.2, t=t, arm_off=(2.0 + 0.1*math.sin(t*3), -1.9 + 0.1*math.sin(t*3+1)))
    cx, cy = 960, 520 + math.sin(t*1.3)*12
    ctx.save(); ctx.translate(cx, cy); ctx.rotate(-1.35 + 0.08*math.sin(t*1.1)); mannequin(ctx, 0, 250, 1.25, P); ctx.restore()
    # velocity arrow + counter
    v = int(195*ease(t/3.2))
    ax = 1360
    ctx.move_to(ax, 380); ctx.line_to(ax, 640); ctx.set_line_width(5); ctx.set_source_rgba(0.98, 0.80, 0.12, 1); ctx.stroke()
    ctx.move_to(ax-18, 630); ctx.line_to(ax, 666); ctx.line_to(ax+18, 630); ctx.close_path(); ctx.fill()
    text(ctx, f"{v} km/h", ax+34, 530, 64, (1, 1, 1, 1), font='JetBrains Mono')
    text(ctx, "TERMINAL VELOCITY", ax+36, 572, 22, (0.98, 0.80, 0.12, 0.9 if v >= 195 else 0.0), spacing=4)
    # dimension line
    ctx.set_source_rgba(0.6, 0.8, 1, 0.6); ctx.set_line_width(1.5)
    ctx.move_to(700, 690); ctx.line_to(1220, 690); ctx.stroke()
    for xx in (700, 1220): ctx.move_to(xx, 678); ctx.line_to(xx, 702); ctx.stroke()
    text(ctx, "1.78 m", 960, 728, 24, (0.6, 0.8, 1, 0.8), font='JetBrains Mono', weight=cairo.FONT_WEIGHT_NORMAL, anchor='c')
    text(ctx, "ALTITUDE  9,412 m", 120, 140, 30, (0.6, 0.8, 1, 0.85), font='JetBrains Mono', weight=cairo.FONT_WEIGHT_NORMAL)
    vignette(ctx, 0.5, (0, 0.02, 0.05))

# ---------------------------------------------------------------- E
def scene_ink_wash(ctx, t):
    paint_bg(ctx, 'street1347.png', zoom=1.03 + 0.04*t/DUR, cx=0.52, cy=0.7)
    x, ph, run = walker(t, 780, 1020, 3.6, speed_phase=4.4)
    fx, fy, s = x, 975, 0.98
    contact_shadow(ctx, fx+10, fy, s, 0.28)
    ink_wash(ctx, fx, fy, s, pose(ph, run, t=t))
    for i in range(3):   # drifting mist
        mx = (300 + i*700 + t*30) % (W+600) - 300; my = 760 + i*60
        g = cairo.RadialGradient(mx, my, 0, mx, my, 420); g.add_color_stop_rgba(0, 0.95, 0.92, 0.85, 0.28); g.add_color_stop_rgba(1, 0.95, 0.92, 0.85, 0)
        ctx.save(); ctx.translate(mx, my); ctx.scale(1, 0.35); ctx.translate(-mx, -my); ctx.arc(mx, my, 420, 0, 2*math.pi); ctx.set_source(g); ctx.fill(); ctx.restore()
    vignette(ctx, 0.35, (0.25, 0.18, 0.10))
    k = ease((t-0.5)/1.0)
    ctx.save(); ctx.translate(0, (1-k)*20); rrect(ctx, 96, 80, 440, 180, 6); ctx.set_source_rgba(0.95, 0.91, 0.82, 0.93*k); ctx.fill()
    ctx.set_line_width(2); rrect(ctx, 106, 90, 420, 160, 4); ctx.set_source_rgba(0.35, 0.25, 0.18, 0.5*k); ctx.stroke()
    text(ctx, "1347", 130, 180, 96, (0.20, 0.13, 0.10, k), font='Caladea')
    text(ctx, "the year the ships came in", 132, 226, 30, (0.60, 0.16, 0.12, k), font='Caladea', weight=cairo.FONT_WEIGHT_NORMAL); ctx.restore()

# ---------------------------------------------------------------- F
def scene_graphic(ctx, t):
    g = cairo.LinearGradient(0, 0, 0, H); g.add_color_stop_rgb(0, 0.06, 0.03, 0.14); g.add_color_stop_rgb(0.7, 0.20, 0.07, 0.25); g.add_color_stop_rgb(1, 0.05, 0.04, 0.08)
    ctx.rectangle(0, 0, W, H); ctx.set_source(g); ctx.fill()
    spd = 900
    for layer, (col, par, hmin, hmax, wmin, wmax, base) in enumerate((
            ((0.12, 0.06, 0.20), 0.15, 300, 600, 120, 220, 780), ((0.07, 0.04, 0.12), 0.45, 200, 520, 160, 300, 800))):
        rnd = random.Random(20 + layer); xx = -(t*spd*par) % 2400 - 2400
        blds = []
        while len(blds) < 30:
            w = rnd.uniform(wmin, wmax); h = rnd.uniform(hmin, hmax); blds.append((w, h, rnd.random()))
        x = xx
        while x < W + 400:
            for w, h, r in blds:
                ctx.rectangle(x, base - h, w - 6, h + 300); ctx.set_source_rgb(*col); ctx.fill()
                if layer == 1:
                    for wy in range(int(base - h + 30), base - 40, 46):
                        for wx in range(int(x + 18), int(x + w - 30), 38):
                            if (wx*7 + wy*3) % 5 == 0:
                                ctx.rectangle(wx, wy, 16, 22); ctx.set_source_rgba(1, 0.78, 0.45, 0.55); ctx.fill()
                    if r > 0.6:   # neon sign
                        nc = (1, 0.25, 0.6) if r > 0.8 else (0.3, 0.95, 1)
                        ctx.rectangle(x + 20, base - h + 50, 22, 120); ctx.set_source_rgba(*nc, 0.95); ctx.fill()
                        gl = cairo.RadialGradient(x+31, base-h+110, 0, x+31, base-h+110, 120); gl.add_color_stop_rgba(0, *nc, 0.35); gl.add_color_stop_rgba(1, *nc, 0)
                        ctx.arc(x+31, base-h+110, 120, 0, 2*math.pi); ctx.set_source(gl); ctx.fill()
                x += w
                if x > W + 400: break
    # wet street
    ctx.rectangle(0, 800, W, H-800); ctx.set_source_rgb(0.06, 0.05, 0.09); ctx.fill()
    for i in range(12):
        lx = (i*260 - t*spd) % (W+260) - 130
        ctx.rectangle(lx, 930, 120, 10); ctx.set_source_rgba(0.95, 0.8, 0.3, 0.5); ctx.fill()
    # police light wash from behind
    ph = t*6
    for side, col in ((0, (1, 0.1, 0.15)), (1, (0.15, 0.35, 1))):
        a = max(0.0, math.sin(ph + side*math.pi))**3
        gl = cairo.RadialGradient(-100, 700, 0, -100, 700, 1100); gl.add_color_stop_rgba(0, *col, 0.55*a); gl.add_color_stop_rgba(1, *col, 0)
        ctx.set_operator(cairo.OPERATOR_ADD); ctx.rectangle(0, 0, W, H); ctx.set_source(gl); ctx.fill(); ctx.set_operator(cairo.OPERATOR_OVER)
    fx, fy, s = 900, 900, 1.12
    contact_shadow(ctx, fx+10, fy, s, 0.5)
    graphic(ctx, fx, fy, s, pose(t*11.5, 1.0, t=t))
    rnd = random.Random(9)
    for i in range(140):   # rain
        rx = (rnd.uniform(0, W+300) - t*300) % (W+300); ry = (rnd.uniform(0, H) + t*rnd.uniform(1500, 2100)) % H
        ctx.move_to(rx, ry); ctx.line_to(rx - 8, ry + 34); ctx.set_line_width(1.4); ctx.set_source_rgba(0.75, 0.85, 1, 0.35); ctx.stroke()
    vignette(ctx, 0.6)
    secs = max(0, 240 - int(t*13))
    k = ease((t-0.3)/0.4)
    ctx.save(); ctx.translate(120, 110); rrect(ctx, 0, 0, 360, 110, 12); ctx.set_source_rgba(0.04, 0.04, 0.07, 0.8*k); ctx.fill()
    text(ctx, "HEAD START", 24, 36, 22, (1, 0.35, 0.35, k), spacing=4)
    text(ctx, f"{secs//60}:{secs%60:02d}", 24, 94, 56, (1, 1, 1, k), font='JetBrains Mono'); ctx.restore()

SCENES = [
    ('A', 'INK LINE', 'survival & physics', scene_ink_line),
    ('B', 'SILHOUETTE', 'mystery, alone, space', scene_silhouette),
    ('C', 'GEOMETRIC', 'science & space what-ifs', scene_geometric),
    ('D', 'TEST DUMMY', 'body limits & extreme physics', scene_mannequin),
    ('E', 'INK WASH', 'history & past eras', scene_ink_wash),
    ('F', 'GRAPHIC NOVEL', 'action, crime, chases', scene_graphic),
]

def label(ctx, letter, name, use, alpha=1.0):
    ctx.select_font_face('Inter Display', cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD); ctx.set_font_size(30)
    s1 = f"{letter}  ·  {name}"; w1 = ctx.text_extents(s1).x_advance
    ctx.set_font_size(24); w2 = ctx.text_extents(use).x_advance
    w = max(w1, w2) + 48
    rrect(ctx, 60, H-150, w, 96, 12); ctx.set_source_rgba(0.04, 0.04, 0.06, 0.72*alpha); ctx.fill()
    text(ctx, s1, 84, H-108, 30, (1, 1, 1, alpha))
    text(ctx, use, 84, H-74, 24, (1, 0.82, 0.45, alpha), weight=cairo.FONT_WEIGHT_NORMAL)

def frame(i, t, labelled=True, fade=True):
    sf = cairo.ImageSurface(cairo.FORMAT_RGB24, W, H); ctx = cairo.Context(sf)
    letter, name, use, fn = SCENES[i]
    fn(ctx, t); grain(ctx, t)
    if labelled: label(ctx, letter, name, use, ease((t-0.2)/0.4))
    if fade:
        a = max(1 - t/0.25, 1 - (DUR - t)/0.25, 0)
        if a > 0: ctx.rectangle(0, 0, W, H); ctx.set_source_rgba(0, 0, 0, min(1, a)); ctx.fill()
    return sf
