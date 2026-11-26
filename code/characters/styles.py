"""Six 'you' character styles on one shared rig (rig.pose).
Each style: draw(ctx, x, y, s, P, face=1, **opts). (x, y) = feet on screen."""
import math, random, cairo
from rig import place, stroke_path, taper, ellipse

def _limbs(P):
    """(far, near) segments for convenience."""
    return P['legF'], P['legN'], P['armF'], P['armN']

# --------------------------------------------------------------- A. INK LINE
INK = (0.07, 0.07, 0.09, 1)
BEANIE = (0.86, 0.63, 0.20, 1); BEANIE_D = (0.70, 0.48, 0.12, 1)
SCARF = (0.80, 0.17, 0.15, 1); SCARF_D = (0.60, 0.10, 0.10, 1)

def ink_line(ctx, x, y, s, P, face=1, wind=1.0):
    t = P['t']
    ctx.save(); place(ctx, x, y, s, face, P)
    lF, lN, aF, aN = _limbs(P)
    far = (0.07, 0.07, 0.09, 0.72)
    # scarf tail, behind everything
    w1 = math.sin(t*3.1)*10*wind; w2 = math.sin(t*3.1 - 1.2)*18*wind
    nx, ny = P['neck']
    ctx.move_to(nx-6, ny+8); ctx.curve_to(nx-40, ny+20+w1*0.4, nx-62, ny+30+w1, nx-92, ny+46+w2)
    ctx.line_to(nx-86, ny+64+w2); ctx.curve_to(nx-58, ny+46+w1, nx-34, ny+38, nx-2, ny+26); ctx.close_path()
    ctx.set_source_rgba(*SCARF_D); ctx.fill()
    for leg, c in ((lF, far),):
        stroke_path(ctx, [leg['hip'], leg['knee'], leg['ankle']], 13, c); stroke_path(ctx, [leg['heel'], leg['toe']], 13, c)
    stroke_path(ctx, [aF['sh'], aF['el'], aF['wr']], 11, far)
    # torso: slight taper, reads adult
    taper(ctx, (P['neck'][0]-1, P['neck'][1]+6), (P['hip'][0], P['hip'][1]+4), 24, 15); ctx.set_source_rgba(*INK); ctx.fill()
    stroke_path(ctx, [lN['hip'], lN['knee'], lN['ankle']], 14, INK); stroke_path(ctx, [lN['heel'], lN['toe']], 14, INK)
    # head
    hx, hy = P['head']; ctx.arc(hx, hy, 31, 0, 2*math.pi); ctx.set_source_rgba(*INK); ctx.fill()
    # beanie
    ctx.new_path(); ctx.arc(hx+1, hy-6, 33, math.pi*1.02, math.pi*1.98); ctx.close_path(); ctx.set_source_rgba(*BEANIE); ctx.fill()
    ctx.save(); ctx.translate(hx+1, hy-8); ctx.rotate(-0.06)
    ctx.rectangle(-35, -2, 70, 12); ctx.set_source_rgba(*BEANIE_D); ctx.fill()
    for i in range(-30, 34, 7):
        ctx.move_to(i, -1); ctx.line_to(i, 9); ctx.set_line_width(1.6); ctx.set_source_rgba(0.55, 0.36, 0.08, 1); ctx.stroke()
    ctx.restore()
    # scarf wrap
    ellipse(ctx, nx+2, ny+6, 26, 11); ctx.set_source_rgba(*SCARF); ctx.fill()
    ctx.move_to(nx-12, ny+2); ctx.line_to(nx+16, ny+10); ctx.set_line_width(2); ctx.set_source_rgba(*SCARF_D); ctx.stroke()
    stroke_path(ctx, [aN['sh'], aN['el'], aN['wr']], 12, INK)
    ctx.restore()

# --------------------------------------------------------------- B. SILHOUETTE
SIL = (0.035, 0.03, 0.06, 1)

def _sil_body(ctx, P, col):
    lF, lN, aF, aN = _limbs(P)
    ctx.set_source_rgba(*col)
    for leg, k in ((lF, 0.92), (lN, 1.0)):
        taper(ctx, leg['hip'], leg['knee'], 40*k, 30*k); taper(ctx, leg['knee'], leg['ankle'], 30*k, 21*k)
        taper(ctx, leg['heel'], leg['toe'], 22, 16)
    taper(ctx, aF['sh'], aF['el'], 25, 21); taper(ctx, aF['el'], aF['wr'], 21, 16); ctx.fill()
    # long coat, hem swings with the stride
    sw = math.sin(P['phase'])*14*P['walk']
    ctx.move_to(-30, -372); ctx.curve_to(-10, -386, 22, -386, 40, -370)
    ctx.curve_to(44, -320, 40, -260, 46+sw, -150); ctx.line_to(-38+sw*0.6, -150)
    ctx.curve_to(-34, -250, -36, -320, -30, -372); ctx.close_path(); ctx.fill()
    # collar + head + hair
    ctx.move_to(-8, -392); ctx.line_to(26, -392); ctx.line_to(30, -368); ctx.line_to(-12, -368); ctx.close_path(); ctx.fill()
    hx, hy = P['head']
    ellipse(ctx, hx+3, hy, 30, 35); ctx.fill()
    ctx.move_to(hx-28, hy+4); ctx.curve_to(hx-36, hy-30, hx-12, hy-46, hx+10, hy-42)
    ctx.curve_to(hx+34, hy-40, hx+40, hy-24, hx+36, hy-12); ctx.line_to(hx-26, hy+6); ctx.close_path(); ctx.fill()
    ctx.move_to(hx+30, hy-4); ctx.line_to(hx+40, hy+8); ctx.line_to(hx+30, hy+12); ctx.close_path(); ctx.fill()  # nose
    taper(ctx, aN['sh'], aN['el'], 26, 22); taper(ctx, aN['el'], aN['wr'], 22, 17); ctx.fill()
    ctx.arc(aN['hand'][0], aN['hand'][1], 11, 0, 2*math.pi); ctx.fill()

def silhouette(ctx, x, y, s, P, face=1, rim=(1.0, 0.62, 0.36, 1), lantern=True):
    ctx.save(); place(ctx, x, y, s, face, P)
    ctx.save(); ctx.translate(4, -3); _sil_body(ctx, P, rim); ctx.restore()      # rim light edge
    _sil_body(ctx, P, SIL)
    if lantern:
        hx, hy = P['armN']['hand']
        flick = 0.9 + 0.1*math.sin(P['t']*23) * math.sin(P['t']*7)
        g = cairo.RadialGradient(hx+4, hy+30, 0, hx+4, hy+30, 260)
        g.add_color_stop_rgba(0, 0.55, 0.95, 1.0, 0.42*flick); g.add_color_stop_rgba(0.3, 0.3, 0.7, 0.9, 0.12*flick)
        g.add_color_stop_rgba(1, 0.2, 0.5, 0.8, 0)
        ctx.set_operator(cairo.OPERATOR_ADD); ctx.arc(hx+4, hy+30, 260, 0, 2*math.pi); ctx.set_source(g); ctx.fill()
        ctx.set_operator(cairo.OPERATOR_OVER)
        stroke_path(ctx, [(hx, hy), (hx+4, hy+14)], 3, SIL)
        ctx.rectangle(hx-8, hy+14, 24, 30); ctx.set_source_rgba(0.75, 1.0, 1.0, flick); ctx.fill()
        ctx.rectangle(hx-11, hy+12, 30, 5); ctx.rectangle(hx-11, hy+42, 30, 5); ctx.set_source_rgba(*SIL); ctx.fill()
    ctx.restore()

# --------------------------------------------------------------- C. GEOMETRIC
GEO = dict(coat=(0.93, 0.45, 0.24, 1), coat_d=(0.78, 0.33, 0.17, 1), pants=(0.12, 0.20, 0.29, 1),
           pants_d=(0.08, 0.14, 0.21, 1), skin=(0.97, 0.82, 0.68, 1), hair=(0.16, 0.11, 0.12, 1),
           shoe=(0.96, 0.94, 0.88, 1), bag=(0.98, 0.78, 0.25, 1))

def geometric(ctx, x, y, s, P, face=1, pal=GEO):
    ctx.save(); place(ctx, x, y, s, face, P)
    lF, lN, aF, aN = _limbs(P)
    def leg(l, c):
        ctx.set_line_cap(cairo.LINE_CAP_BUTT); stroke_path(ctx, [l['hip'], l['knee'], l['ankle']], 34, c, cap=cairo.LINE_CAP_ROUND)
        ctx.save(); ctx.translate(*l['ankle']); ctx.rotate(l['rot'])
        ctx.new_path(); ctx.arc(10, 6, 20, math.pi, 2*math.pi); ctx.close_path(); ctx.set_source_rgba(*pal['shoe']); ctx.fill()
        ctx.restore()
    def arm(a, c):
        stroke_path(ctx, [a['sh'], a['el'], a['wr']], 30, pal['coat_d'])
        stroke_path(ctx, [a['sh'], a['el'], a['wr']], 24, c)
        ctx.arc(*a['hand'], 12, 0, 2*math.pi); ctx.set_source_rgba(*pal['skin']); ctx.fill()
    arm(aF, pal['coat_d']); leg(lF, pal['pants_d'])
    # backpack: a plain rounded square
    ctx.save(); ctx.translate(-44, -330); ctx.new_path()
    r = 14; w, h = 34, 96
    ctx.arc(r, r, r, math.pi, 1.5*math.pi); ctx.arc(w-r, r, r, 1.5*math.pi, 0); ctx.arc(w-r, h-r, r, 0, .5*math.pi); ctx.arc(r, h-r, r, .5*math.pi, math.pi)
    ctx.close_path(); ctx.set_source_rgba(*pal['bag']); ctx.fill(); ctx.restore()
    # coat: trapezoid with a soft top
    ctx.move_to(-30, -366); ctx.curve_to(-22, -390, 30, -390, 40, -366)
    ctx.line_to(46, -214); ctx.line_to(-36, -214); ctx.close_path(); ctx.set_source_rgba(*pal['coat']); ctx.fill()
    ctx.move_to(5, -386); ctx.line_to(46, -214); ctx.line_to(28, -214); ctx.line_to(2, -370); ctx.close_path()
    ctx.set_source_rgba(1, 1, 1, 0.10); ctx.fill()
    leg(lN, pal['pants'])
    # head: circle + hair as a tilted half disc, no face
    hx, hy = P['head']
    ctx.rectangle(hx-11, hy+20, 18, 22); ctx.set_source_rgba(*pal['skin']); ctx.fill()
    ctx.arc(hx+2, hy, 33, 0, 2*math.pi); ctx.set_source_rgba(*pal['skin']); ctx.fill()
    ctx.save(); ctx.translate(hx+2, hy); ctx.rotate(-0.35); ctx.new_path()
    ctx.arc(0, 0, 35, math.pi, 2*math.pi); ctx.close_path(); ctx.set_source_rgba(*pal['hair']); ctx.fill(); ctx.restore()
    arm(aN, pal['coat'])
    ctx.restore()

# --------------------------------------------------------------- D. MANNEQUIN
def _shade(ctx, a, b, w, base, light=(-0.6, -0.8)):
    """Fill current path with a cylinder-like gradient across the segment."""
    mx, my = (a[0]+b[0])/2, (a[1]+b[1])/2
    dx, dy = b[0]-a[0], b[1]-a[1]; L = math.hypot(dx, dy) or 1
    nx, ny = -dy/L, dx/L
    if nx*light[0] + ny*light[1] < 0: nx, ny = -nx, -ny
    g = cairo.LinearGradient(mx+nx*w/2, my+ny*w/2, mx-nx*w/2, my-ny*w/2)
    r, gg, bb, _ = base
    g.add_color_stop_rgb(0, min(1, r*1.18), min(1, gg*1.18), min(1, bb*1.18))
    g.add_color_stop_rgb(0.45, r, gg, bb)
    g.add_color_stop_rgb(1, r*0.55, gg*0.55, bb*0.6)
    ctx.set_source(g); ctx.fill()

def _ball(ctx, x, y, r, base):
    g = cairo.RadialGradient(x-r*0.35, y-r*0.4, r*0.1, x, y, r)
    g.add_color_stop_rgb(0, min(1, base[0]*1.2), min(1, base[1]*1.2), min(1, base[2]*1.2))
    g.add_color_stop_rgb(1, base[0]*0.5, base[1]*0.5, base[2]*0.56)
    ctx.arc(x, y, r, 0, 2*math.pi); ctx.set_source(g); ctx.fill()

MANNE = (0.80, 0.82, 0.86, 1); MANNE_F = (0.58, 0.60, 0.66, 1)

def _target(ctx, x, y, r):
    for i in range(4):
        ctx.move_to(x, y); ctx.arc(x, y, r, i*math.pi/2, (i+1)*math.pi/2); ctx.close_path()
        ctx.set_source_rgba(*((0.98, 0.80, 0.12, 1) if i % 2 == 0 else (0.08, 0.08, 0.08, 1))); ctx.fill()

def mannequin(ctx, x, y, s, P, face=1):
    ctx.save(); place(ctx, x, y, s, face, P)
    lF, lN, aF, aN = _limbs(P)
    def leg(l, base):
        for a, b, wa, wb in ((l['hip'], l['knee'], 36, 26), (l['knee'], l['ankle'], 26, 18)):
            ctx.new_path(); taper(ctx, a, b, wa, wb); _shade(ctx, a, b, wa, base)
        _ball(ctx, *l['knee'], 15, base)
        ctx.new_path(); taper(ctx, l['heel'], l['toe'], 22, 14); _shade(ctx, l['heel'], l['toe'], 22, base)
    def arm(a, base):
        for p, q, wa, wb in ((a['sh'], a['el'], 24, 19), (a['el'], a['wr'], 19, 14)):
            ctx.new_path(); taper(ctx, p, q, wa, wb); _shade(ctx, p, q, wa, base)
        _ball(ctx, *a['el'], 11, base); _ball(ctx, *a['hand'], 12, base)
    arm(aF, MANNE_F); leg(lF, MANNE_F)
    # pelvis + chest blocks + spine
    ctx.new_path(); ellipse(ctx, 4, -222, 36, 24); _shade(ctx, (4, -246), (4, -198), 70, MANNE)
    ctx.new_path(); taper(ctx, (4, -246), (6, -300), 16, 16); _shade(ctx, (4, -246), (6, -300), 16, MANNE)
    ctx.new_path(); ctx.move_to(-30, -370); ctx.curve_to(-20, -392, 34, -392, 42, -370)
    ctx.curve_to(44, -330, 34, -300, 6, -292); ctx.curve_to(-22, -300, -36, -330, -30, -370); ctx.close_path()
    _shade(ctx, (-34, -340), (44, -340), 90, MANNE)
    ctx.new_path(); taper(ctx, P['neck'], (6, -370), 16, 18); _shade(ctx, P['neck'], (6, -370), 16, MANNE)
    _target(ctx, 4, -224, 11)
    leg(lN, MANNE)
    hx, hy = P['head']
    g = cairo.RadialGradient(hx-8, hy-14, 4, hx+2, hy, 40)
    g.add_color_stop_rgb(0, 0.95, 0.96, 0.98); g.add_color_stop_rgb(1, 0.46, 0.48, 0.54)
    ellipse(ctx, hx+3, hy, 30, 37); ctx.set_source(g); ctx.fill()
    _target(ctx, hx-6, hy-4, 9)
    _ball(ctx, *aN['sh'], 15, MANNE)
    arm(aN, MANNE)
    ctx.restore()

# --------------------------------------------------------------- E. INK WASH
SEPIA = (0.20, 0.15, 0.12); WASH = (0.36, 0.30, 0.26); RED = (0.62, 0.16, 0.13)

def _brush(ctx, pts, w, rnd, col=SEPIA, passes=4, a=0.55):
    for i in range(passes):
        jit = [(p[0]+rnd.uniform(-2.5, 2.5), p[1]+rnd.uniform(-2.5, 2.5)) for p in pts]
        stroke_path(ctx, jit, w*rnd.uniform(0.55, 1.0), (*col, a*rnd.uniform(0.6, 1.0)))

def _wash(ctx, path_fn, rnd, col, passes=5, a=0.22):
    for i in range(passes):
        ctx.save(); ctx.translate(rnd.uniform(-3, 3), rnd.uniform(-3, 3)); path_fn(); ctx.restore()
        ctx.set_source_rgba(*col, a*rnd.uniform(0.7, 1.2)); ctx.fill()

def ink_wash(ctx, x, y, s, P, face=1, boil=8):
    rnd = random.Random(int(P['t']*boil))
    ctx.save(); place(ctx, x, y, s, face, P)
    lF, lN, aF, aN = _limbs(P)
    _brush(ctx, [lF['hip'], lF['knee'], lF['ankle'], lF['toe']], 17, rnd, col=WASH)
    _brush(ctx, [lN['hip'], lN['knee'], lN['ankle'], lN['toe']], 18, rnd)
    _brush(ctx, [aF['sh'], aF['el'], aF['wr']], 11, rnd, col=WASH)
    sw = math.sin(P['phase'])*12*P['walk']; hx, hy = P['head']
    def cloak():
        ctx.new_path(); ctx.move_to(-26, -378); ctx.curve_to(-6, -392, 26, -392, 40, -376)
        ctx.curve_to(50, -320, 56, -240, 60+sw, -160); ctx.curve_to(20, -150, -20, -150, -50+sw*0.5, -158)
        ctx.curve_to(-46, -240, -40, -330, -26, -378); ctx.close_path()
    def hood():
        ctx.new_path(); ctx.move_to(hx-30, hy+26); ctx.curve_to(hx-44, hy-10, hx-34, hy-46, hx-12, hy-54)
        ctx.curve_to(hx+8, hy-58, hx+34, hy-44, hx+40, hy-14); ctx.curve_to(hx+44, hy+8, hx+40, hy+26, hx+30, hy+36)
        ctx.curve_to(hx+10, hy+44, hx-14, hy+40, hx-30, hy+26); ctx.close_path()
    for fn in (cloak, hood):
        _wash(ctx, fn, rnd, (0.27, 0.23, 0.21), passes=4, a=0.34)
        ctx.save(); fn(); ctx.set_source_rgba(0.24, 0.20, 0.18, 0.55); ctx.fill_preserve()
        ctx.set_line_width(3); ctx.set_source_rgba(*SEPIA, 0.8); ctx.stroke(); ctx.restore()
    # front opening of the cloak, darker fold
    _brush(ctx, [(30, -372), (36, -290), (44+sw*0.8, -166)], 6, rnd, col=(0.10, 0.08, 0.07), passes=2, a=0.6)
    # face in the hood shadow: a pale sliver of profile
    ctx.new_path(); ctx.move_to(hx+14, hy-22); ctx.curve_to(hx+30, hy-24, hx+34, hy-4, hx+40, hy+2)
    ctx.curve_to(hx+34, hy+6, hx+34, hy+18, hx+24, hy+26); ctx.curve_to(hx+16, hy+8, hx+12, hy-6, hx+14, hy-22); ctx.close_path()
    ctx.set_source_rgba(0.93, 0.86, 0.74, 0.92); ctx.fill()
    # red sash, the one colour accent
    _brush(ctx, [(-40, -262), (8, -256), (46, -266)], 14, rnd, col=RED, passes=3, a=0.75)
    tail = math.sin(P['t']*2.6)*8
    _brush(ctx, [(-34, -258), (-52, -228+tail*0.4), (-62, -196+tail)], 10, rnd, col=RED, passes=3, a=0.7)
    _brush(ctx, [aN['sh'], aN['el'], aN['wr']], 13, rnd)
    ctx.restore()

# --------------------------------------------------------------- F. GRAPHIC NOVEL
OUT = (0.05, 0.05, 0.07, 1)
GN = dict(jacket=(0.86, 0.36, 0.20, 1), jacket_d=(0.62, 0.22, 0.14, 1), jeans=(0.18, 0.22, 0.30, 1),
          jeans_d=(0.12, 0.15, 0.21, 1), skin=(0.88, 0.67, 0.53, 1), skin_d=(0.68, 0.47, 0.38, 1),
          hair=(0.12, 0.09, 0.08, 1), shoe=(0.94, 0.94, 0.92, 1), rim=(0.40, 0.95, 1.0, 1))

def _of(ctx, col, w=5):
    ctx.set_source_rgba(*col); ctx.fill_preserve(); ctx.set_source_rgba(*OUT); ctx.set_line_width(w)
    ctx.set_line_join(cairo.LINE_JOIN_ROUND); ctx.stroke()

def graphic(ctx, x, y, s, P, face=1, pal=GN, rim=True):
    ctx.save(); place(ctx, x, y, s, face, P)
    lF, lN, aF, aN = _limbs(P)
    def leg(l, c):
        ctx.new_path(); taper(ctx, l['hip'], l['knee'], 40, 31); taper(ctx, l['knee'], l['ankle'], 31, 24); _of(ctx, c)
        ctx.save(); ctx.translate(*l['ankle']); ctx.rotate(l['rot']); ctx.new_path()
        ctx.move_to(-16, -6); ctx.line_to(26, -4); ctx.curve_to(38, -2, 40, 14, 32, 16); ctx.line_to(-16, 16); ctx.close_path()
        _of(ctx, pal['shoe']); ctx.restore()
    def arm(a, c, sk):
        ctx.new_path(); taper(ctx, a['sh'], a['el'], 30, 25); taper(ctx, a['el'], a['wr'], 25, 21); _of(ctx, c)
        ctx.new_path(); ctx.arc(*a['hand'], 12, 0, 2*math.pi); _of(ctx, sk, 4)
    arm(aF, pal['jacket_d'], pal['skin_d']); leg(lF, pal['jeans_d'])
    # bomber jacket
    ctx.new_path(); ctx.move_to(-32, -366); ctx.curve_to(-26, -392, 34, -392, 42, -366)
    ctx.curve_to(46, -320, 44, -270, 40, -236); ctx.line_to(-34, -236); ctx.curve_to(-38, -280, -38, -330, -32, -366); ctx.close_path()
    _of(ctx, pal['jacket'])
    ctx.move_to(-32, -360); ctx.curve_to(-30, -310, -30, -270, -34, -240); ctx.line_to(-10, -240); ctx.curve_to(-14, -290, -12, -330, -4, -380)
    ctx.close_path(); ctx.set_source_rgba(*pal['jacket_d']); ctx.fill()                       # cel shadow
    ctx.new_path(); ctx.rectangle(-36, -246, 80, 16); _of(ctx, pal['jacket_d'], 4)                  # ribbed hem
    ctx.move_to(18, -380); ctx.line_to(20, -246); ctx.set_line_width(3); ctx.set_source_rgba(*OUT); ctx.stroke()
    leg(lN, pal['jeans'])
    # head
    hx, hy = P['head']
    ctx.new_path(); ctx.rectangle(hx-12, hy+18, 22, 26); _of(ctx, pal['skin_d'], 4)
    ctx.new_path(); ctx.move_to(hx-26, hy-14); ctx.curve_to(hx-30, hy+24, hx-6, hy+42, hx+18, hy+40)
    ctx.curve_to(hx+34, hy+38, hx+36, hy+22, hx+38, hy+10); ctx.line_to(hx+44, hy+2); ctx.line_to(hx+38, hy-6)
    ctx.curve_to(hx+38, hy-30, hx+20, hy-42, hx+2, hy-42); ctx.curve_to(hx-16, hy-42, hx-26, hy-30, hx-26, hy-14); ctx.close_path()
    _of(ctx, pal['skin'])
    ctx.move_to(hx-24, hy+6); ctx.curve_to(hx-18, hy+30, hx-2, hy+38, hx+8, hy+39); ctx.curve_to(hx-6, hy+24, hx-14, hy+10, hx-24, hy+6)
    ctx.set_source_rgba(*pal['skin_d']); ctx.fill()
    # hair: swept, angular
    ctx.new_path(); ctx.move_to(hx-30, hy+4); ctx.line_to(hx-34, hy-26); ctx.line_to(hx-22, hy-46); ctx.line_to(hx+6, hy-54)
    ctx.line_to(hx+30, hy-48); ctx.line_to(hx+46, hy-30); ctx.line_to(hx+30, hy-30); ctx.line_to(hx+36, hy-20)
    ctx.line_to(hx+16, hy-26); ctx.line_to(hx+6, hy-16); ctx.line_to(hx-6, hy-22); ctx.line_to(hx-14, hy-4); ctx.close_path()
    _of(ctx, pal['hair'], 4)
    ctx.new_path(); ellipse(ctx, hx-16, hy+2, 6, 9); _of(ctx, pal['skin_d'], 3)                     # ear
    # face: one eye, brow, mouth
    blink = (int(P['t']*10) % 31) == 0
    if blink: stroke_path(ctx, [(hx+20, hy-3), (hx+30, hy-3)], 3, OUT)
    else: ctx.new_path(); ellipse(ctx, hx+25, hy-4, 3.6, 6); ctx.set_source_rgba(*OUT); ctx.fill()
    stroke_path(ctx, [(hx+16, hy-16), (hx+33, hy-14)], 4, OUT)
    stroke_path(ctx, [(hx+24, hy+24), (hx+33, hy+22)], 3, OUT)
    if rim:   # neon rim on the back edge
        ctx.new_path(); ctx.move_to(hx-30, hy+2); ctx.line_to(hx-33, hy-24); ctx.set_line_width(3); ctx.set_source_rgba(*pal['rim']); ctx.stroke()
        ctx.move_to(-31, -360); ctx.curve_to(-35, -320, -35, -280, -31, -242); ctx.stroke()
    arm(aN, pal['jacket'], pal['skin'])
    ctx.restore()

STYLES = dict(ink_line=ink_line, silhouette=silhouette, geometric=geometric,
              mannequin=mannequin, ink_wash=ink_wash, graphic=graphic)
