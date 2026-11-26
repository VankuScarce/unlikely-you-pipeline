"""'YOU' v2: a flat-illustration adult (no hoodie), adult proportions, real walk/run cycle.
Drop-in replacement for style.you(ctx, x, y, s, phase, run, hold, lean). (x, y) = feet, faces +x (face=-1 flips)."""
import math, cairo
from style import paper, rrect, c

SKIN = (0.87, 0.68, 0.55, 1); SKIN_D = (0.76, 0.56, 0.44, 1)
HAIR = (0.19, 0.13, 0.10, 1)
JACKET = (0.22, 0.34, 0.30, 1); JACKET_D = (0.16, 0.25, 0.22, 1)
TEE = (0.93, 0.91, 0.86, 1)
JEANS = (0.24, 0.31, 0.46, 1); JEANS_D = (0.18, 0.23, 0.35, 1)
SHOE = (0.95, 0.95, 0.93, 1); SOLE = (0.55, 0.55, 0.58, 1)
INK = (0.10, 0.09, 0.10, 1)

def _seg(ctx, x0, y0, a, L):
    return x0 + L*math.sin(a), y0 + L*math.cos(a)

def _limb(ctx, pts, widths, col, shadow=True):
    ctx.set_line_cap(cairo.LINE_CAP_ROUND); ctx.set_line_join(cairo.LINE_JOIN_ROUND)
    for o, cc in ((((4, 5),), (0, 0, 0, 0.18)), (((0, 0),), col)):
        if o[0] != (0, 0) and not shadow: continue
        for (p0, p1), w in zip(zip(pts, pts[1:]), widths):
            ctx.move_to(p0[0]+o[0][0], p0[1]+o[0][1]); ctx.line_to(p1[0]+o[0][0], p1[1]+o[0][1])
            ctx.set_line_width(w); ctx.set_source_rgba(*cc); ctx.stroke()

def _leg(ctx, hip, a_thigh, flex, col, dark=False):
    knee = _seg(ctx, *hip, a_thigh, 102)
    a_shin = a_thigh - flex                      # knee bends backward
    ankle = _seg(ctx, *knee, a_shin, 100)
    _limb(ctx, [hip, knee, ankle], [40, 32], col)
    # shoe: points forward, tilts with the shin a little
    ctx.save(); ctx.translate(*ankle); ctx.rotate(-(a_shin)*0.6)
    rrect(ctx, -16, -6, 50, 22, 10); ctx.set_source_rgba(*(SHOE if not dark else (0.80, 0.80, 0.79, 1))); ctx.fill()
    ctx.rectangle(-16, 10, 50, 6); ctx.set_source_rgba(*SOLE); ctx.fill()
    ctx.restore()

def _arm(ctx, sh, a_up, flex, sleeve, dark=False, hand=True):
    elbow = _seg(ctx, *sh, a_up, 78)
    a_fore = a_up + flex                         # elbow bends forward
    wrist = _seg(ctx, *elbow, a_fore, 70)
    _limb(ctx, [sh, elbow, wrist], [27, 23], sleeve)
    if hand:
        hx, hy = _seg(ctx, *wrist, a_fore, 10)
        ctx.arc(hx, hy, 11.5, 0, 2*math.pi); ctx.set_source_rgba(*(SKIN if not dark else SKIN_D)); ctx.fill()

def _head(ctx, t=0.0, blink=False):
    ctx.save(); ctx.translate(0, -420)
    # neck
    ctx.rectangle(-11, 18, 24, 34); ctx.set_source_rgba(*SKIN_D); ctx.fill()
    # face
    paper(ctx, lambda k: (k.new_path(), k.save(), k.translate(5, 0), k.scale(33, 40), k.arc(0, 0, 1, 0, 2*math.pi), k.restore()), SKIN, off=(3, 4))
    # jaw toward the front
    ctx.move_to(-10, 20); ctx.curve_to(10, 44, 30, 40, 36, 14); ctx.line_to(30, 0); ctx.close_path(); ctx.set_source_rgba(*SKIN); ctx.fill()
    # hair: back + top, short fringe
    ctx.move_to(-28, 14); ctx.curve_to(-40, -20, -28, -48, 2, -50); ctx.curve_to(28, -52, 44, -36, 40, -16)
    ctx.curve_to(30, -26, 18, -24, 8, -30); ctx.curve_to(4, -18, -6, -12, -12, -4); ctx.curve_to(-16, 4, -20, 12, -28, 14)
    ctx.close_path(); ctx.set_source_rgba(*HAIR); ctx.fill()
    # ear
    ctx.save(); ctx.translate(-12, 2); ctx.scale(7, 10); ctx.arc(0, 0, 1, 0, 2*math.pi); ctx.restore(); ctx.set_source_rgba(*SKIN_D); ctx.fill()
    # eyes (3/4 view: near eye bigger), brows, nose, mouth
    for ex, r in ((15, 4.6), (32, 3.8)):
        if blink:
            ctx.move_to(ex-5, -2); ctx.line_to(ex+5, -2); ctx.set_line_width(2.5); ctx.set_source_rgba(*INK); ctx.stroke()
        else:
            ctx.save(); ctx.translate(ex, -2); ctx.scale(r, r*1.25); ctx.arc(0, 0, 1, 0, 2*math.pi); ctx.restore(); ctx.set_source_rgba(*INK); ctx.fill()
        ctx.move_to(ex-7, -13); ctx.line_to(ex+6, -15); ctx.set_line_width(3.2); ctx.set_source_rgba(*HAIR); ctx.stroke()
    ctx.move_to(37, -2); ctx.line_to(43, 12); ctx.line_to(36, 14); ctx.set_line_width(2.4); ctx.set_source_rgba(*SKIN_D); ctx.stroke()
    ctx.move_to(22, 24); ctx.curve_to(27, 26, 32, 25, 35, 22); ctx.set_line_width(2.6); ctx.set_source_rgba(0.55, 0.30, 0.28, 1); ctx.stroke()
    ctx.restore()

def _torso(ctx):
    # jacket body
    def body(k):
        k.new_path(); k.move_to(-34, -350); k.curve_to(-36, -374, -18, -384, 4, -384)
        k.curve_to(26, -384, 40, -374, 40, -350); k.curve_to(40, -320, 36, -290, 33, -260)
        k.line_to(36, -220); k.line_to(-30, -220); k.line_to(-28, -260); k.curve_to(-32, -290, -34, -320, -34, -350); k.close_path()
    paper(ctx, body, JACKET, off=(4, 5))
    # tee showing at the open front
    ctx.move_to(14, -370); ctx.line_to(30, -368); ctx.line_to(30, -228); ctx.line_to(18, -228); ctx.close_path(); ctx.set_source_rgba(*TEE); ctx.fill()
    # collar + zip line + pocket + hem
    ctx.move_to(4, -378); ctx.line_to(16, -346); ctx.line_to(14, -372); ctx.close_path(); ctx.set_source_rgba(*JACKET_D); ctx.fill()
    ctx.move_to(16, -350); ctx.line_to(17, -228); ctx.set_line_width(2.5); ctx.set_source_rgba(*JACKET_D); ctx.stroke()
    ctx.move_to(-8, -270); ctx.line_to(10, -272); ctx.set_line_width(3); ctx.stroke()
    ctx.rectangle(-28, -234, 62, 12); ctx.set_source_rgba(*JACKET_D); ctx.fill()
    # hips (jeans top)
    rrect(ctx, -26, -228, 56, 30, 10); ctx.set_source_rgba(*JEANS); ctx.fill()

def you(ctx, x, y, s=1.0, phase=0.0, run=0.0, hold=False, lean=0.0, face=1, reach=0.0, t=0.0):
    """run: 0 idle, ~0.5 walk, 1 run. reach: arms forward (pushing a cart)."""
    ctx.save(); ctx.translate(x, y); ctx.scale(s*0.95*face, s*0.95)
    walk = min(1.0, run*2); sprint = max(0.0, run*2-1)
    amp_leg = 0.42*walk + 0.25*sprint
    bob = abs(math.cos(phase))*(7*walk + 10*sprint)
    ctx.translate(0, -bob); ctx.rotate(lean + 0.13*sprint)
    hip = (2, -215)
    def leg_state(ph):
        a = math.sin(ph)*amp_leg
        flex = 0.08 + max(0.0, math.cos(ph))*(0.55*walk + 0.7*sprint) + 0.12*sprint
        return a, flex
    def arm_state(ph):
        a = -math.sin(ph)*(0.38*walk + 0.25*sprint) + reach*0.9
        flex = 0.15 + 0.25*walk + 0.85*sprint - reach*0.1
        return a, flex
    # far side (darker)
    a, f = arm_state(phase+math.pi); _arm(ctx, (-2, -360), a, f, JACKET_D, dark=True)
    a, f = leg_state(phase+math.pi); _leg(ctx, hip, a, f, JEANS_D, dark=True)
    _torso(ctx)
    a, f = leg_state(phase); _leg(ctx, hip, a, f, JEANS)
    _head(ctx, t, blink=(int(t*10) % 37 == 0) if t else False)
    a, f = arm_state(phase); _arm(ctx, (6, -358), a, f, JACKET)
    ctx.arc(6, -360, 15, 0, 2*math.pi); ctx.set_source_rgba(*JACKET); ctx.fill()
    ctx.restore()
