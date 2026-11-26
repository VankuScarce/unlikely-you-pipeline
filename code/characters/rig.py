"""Shared 2D rig for every 'you' style. All styles read the same joints, so any
style can be swapped into any episode. Units: feet at (0,0), body ~460 tall, faces +x."""
import math, cairo

def _p(o, a, L):
    return (o[0] + L*math.sin(a), o[1] + L*math.cos(a))

def pose(phase=0.0, run=0.0, reach=0.0, t=0.0, arm_off=(0.0, 0.0)):
    """run: 0 idle, 0.5 walk, 1 run. Returns dict of joints + bob/lean."""
    walk = min(1.0, run*2); sprint = max(0.0, run*2-1)
    amp = 0.42*walk + 0.25*sprint
    breathe = math.sin(t*2.2)*2.0*(1-walk)
    hip = (2, -215)
    def leg(ph):
        a = math.sin(ph)*amp
        flex = 0.08 + max(0.0, math.cos(ph))*(0.55*walk + 0.7*sprint) + 0.12*sprint
        knee = _p(hip, a, 102); ash = a - flex; ankle = _p(knee, ash, 100)
        r = -ash*0.6
        toe = (ankle[0] + 34*math.cos(r), ankle[1] + 34*math.sin(r))
        heel = (ankle[0] - 10*math.cos(r), ankle[1] - 10*math.sin(r))
        return dict(hip=hip, knee=knee, ankle=ankle, toe=toe, heel=heel, rot=r)
    sh_y = -360 + breathe
    def arm(ph, sx, off=0.0):
        a = -math.sin(ph)*(0.38*walk + 0.25*sprint) + reach*0.9 + 0.04 + off
        flex = 0.15 + 0.25*walk + 0.85*sprint - reach*0.1
        sh = (sx, sh_y); el = _p(sh, a, 78); af = a + flex; wr = _p(el, af, 70); hand = _p(wr, af, 11)
        return dict(sh=sh, el=el, wr=wr, hand=hand, ang=af)
    return dict(
        legN=leg(phase), legF=leg(phase+math.pi),
        armN=arm(phase, 6, arm_off[0]), armF=arm(phase+math.pi, -2, arm_off[1]),
        neck=(6, -384 + breathe), head=(8, -422 + breathe), hip=hip,
        bob=abs(math.cos(phase))*(7*walk + 10*sprint), lean=0.13*sprint + 0.03*walk,
        walk=walk, t=t, phase=phase)

def place(ctx, x, y, s, face, P):
    ctx.translate(x, y); ctx.scale(s*face, s); ctx.translate(0, -P['bob']); ctx.rotate(P['lean'])

def stroke_path(ctx, pts, w, col, cap=cairo.LINE_CAP_ROUND):
    ctx.set_line_cap(cap); ctx.set_line_join(cairo.LINE_JOIN_ROUND)
    ctx.move_to(*pts[0])
    for p in pts[1:]: ctx.line_to(*p)
    ctx.set_line_width(w); ctx.set_source_rgba(*col); ctx.stroke()

def taper(ctx, a, b, wa, wb):
    """Closed tapered capsule from a (width wa) to b (width wb)."""
    dx, dy = b[0]-a[0], b[1]-a[1]; L = math.hypot(dx, dy) or 1
    ang = math.atan2(dy, dx)
    ctx.new_sub_path()
    ctx.arc(a[0], a[1], wa/2, ang+math.pi/2, ang+3*math.pi/2)
    ctx.arc(b[0], b[1], wb/2, ang-math.pi/2, ang+math.pi/2)
    ctx.close_path()

def ellipse(ctx, x, y, rx, ry):
    ctx.save(); ctx.translate(x, y); ctx.scale(rx, ry); ctx.new_sub_path(); ctx.arc(0, 0, 1, 0, 2*math.pi); ctx.restore()

def contact_shadow(ctx, x, y, s, alpha=0.35, w=90):
    g = cairo.RadialGradient(0, 0, 0, 0, 0, 1)
    g.add_color_stop_rgba(0, 0, 0, 0, alpha); g.add_color_stop_rgba(1, 0, 0, 0, 0)
    ctx.save(); ctx.translate(x, y); ctx.scale(w*s, 14*s); ctx.arc(0, 0, 1, 0, 2*math.pi); ctx.set_source(g); ctx.fill(); ctx.restore()
