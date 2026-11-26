"""Ozzie's Odds visual style: flat paper cut-out, drop-shadowed layers, grain. Pure code (pycairo)."""
import cairo, math, numpy as np

W, H = 1920, 1080
PAL = dict(
    navy=(0.078,0.129,0.239), ink=(0.06,0.07,0.12), teal=(0.122,0.478,0.549),
    cream=(0.945,0.914,0.855), orange=(0.957,0.635,0.349), hivis=(1.0,0.50,0.07),
    red=(0.902,0.224,0.275), blue=(0.227,0.525,1.0), grey=(0.553,0.600,0.682),
    slate=(0.184,0.282,0.345), sand=(0.93,0.80,0.60), sky=(0.55,0.80,0.85),
    palm=(0.13,0.45,0.35), white=(1,1,1), yellow=(1.0,0.82,0.30),
)
def c(name, a=1.0):
    r,g,b = PAL[name]; return (r,g,b,a)

def ease(t): t=max(0,min(1,t)); return t*t*(3-2*t)
def back(t):
    t=max(0,min(1,t)); s=1.70158; t-=1; return t*t*((s+1)*t+s)+1
def prog(t,a,b): return max(0.0,min(1.0,(t-a)/(b-a)))

def paper(ctx, draw, color, shadow=(0,0,0,0.28), off=(7,9)):
    """draw(ctx) builds a path; render with paper drop shadow."""
    ctx.save(); ctx.translate(*off); draw(ctx); ctx.set_source_rgba(*shadow); ctx.fill(); ctx.restore()
    draw(ctx); ctx.set_source_rgba(*color); ctx.fill()

def rrect(ctx,x,y,w,h,r):
    ctx.new_sub_path()
    ctx.arc(x+w-r,y+r,r,-math.pi/2,0); ctx.arc(x+w-r,y+h-r,r,0,math.pi/2)
    ctx.arc(x+r,y+h-r,r,math.pi/2,math.pi); ctx.arc(x+r,y+r,r,math.pi,1.5*math.pi); ctx.close_path()

def text(ctx, s, x, y, size, color, weight='bold', anchor='c', font='Inter Display'):
    ctx.select_font_face(font, cairo.FONT_SLANT_NORMAL,
        cairo.FONT_WEIGHT_BOLD if weight=='bold' else cairo.FONT_WEIGHT_NORMAL)
    ctx.set_font_size(size); e = ctx.text_extents(s)
    dx = {'c':-e.width/2-e.x_bearing,'l':-e.x_bearing,'r':-e.width-e.x_bearing}[anchor]
    ctx.move_to(x+dx, y-e.height/2-e.y_bearing); ctx.set_source_rgba(*color); ctx.show_text(s)
    return e.width

def text_paper(ctx, s, x, y, size, color, anchor='c', off=(5,6)):
    text(ctx,s,x+off[0],y+off[1],size,(0,0,0,0.3),anchor=anchor); return text(ctx,s,x,y,size,color,anchor=anchor)

_grain = None
_gbuf = None
def grain(ctx, alpha=0.10):
    global _grain, _gbuf
    if _grain is None:
        rng = np.random.default_rng(7)
        n = rng.normal(0,1,(H//2,W//2))
        a = np.clip(128+n*60,0,255).astype(np.uint8)
        buf = np.zeros((H//2,W//2,4),np.uint8); buf[...,0]=a; buf[...,1]=a; buf[...,2]=a; buf[...,3]=255
        _grain = cairo.ImageSurface.create_for_data(memoryview(buf).cast('B'), cairo.FORMAT_ARGB32, W//2, H//2)
        _gbuf = buf
    ctx.save(); ctx.scale(2,2); ctx.set_source_surface(_grain,0,0)
    ctx.set_operator(cairo.OPERATOR_OVERLAY); ctx.paint_with_alpha(alpha); ctx.restore()

def vignette(ctx, a=0.45):
    g = cairo.RadialGradient(W/2,H/2,H*0.35,W/2,H/2,H*0.95)
    g.add_color_stop_rgba(0,0,0,0,0); g.add_color_stop_rgba(1,0,0,0,a)
    ctx.set_source(g); ctx.paint()

def star(ctx, cx, cy, r, filled_color, empty=False):
    def p(ctx):
        ctx.new_path()
        for i in range(10):
            ang = -math.pi/2 + i*math.pi/5; rr = r if i%2==0 else r*0.45
            ctx.line_to(cx+rr*math.cos(ang), cy+rr*math.sin(ang))
        ctx.close_path()
    if empty:
        p(ctx); ctx.set_source_rgba(1,1,1,0.18); ctx.fill()
    else:
        paper(ctx,p,filled_color,off=(4,5))

# ---------------- characters ----------------
def ozzie(ctx, x, y, s=1.0, blink=0.0, look=(0,0), wing=0.0, tilt=0.0):
    """Ozzie the owl: slate body, cream belly, huge orange eyes, hi-vis vest. (x,y)=feet centre."""
    ctx.save(); ctx.translate(x,y); ctx.rotate(tilt); ctx.scale(s,s)
    # tufts
    for sx in (-1,1):
        paper(ctx, lambda k,sx=sx:(k.new_path(),k.move_to(sx*70,-330),k.line_to(sx*130,-420),k.line_to(sx*20,-350),k.close_path()), c('slate'))
    # body
    paper(ctx, lambda k:(k.new_path(),k.save(),k.translate(0,-200),k.scale(1,1.18),k.arc(0,0,165,0,2*math.pi),k.restore()), c('slate'))
    # belly
    paper(ctx, lambda k:(k.new_path(),k.save(),k.translate(0,-120),k.scale(1,1.1),k.arc(0,0,105,0,2*math.pi),k.restore()), c('cream'), off=(3,4))
    # vest
    def vest(k):
        k.new_path(); k.move_to(-150,-170); k.line_to(-60,-210); k.line_to(-40,-20); k.line_to(-140,-40); k.close_path()
        k.move_to(150,-170); k.line_to(60,-210); k.line_to(40,-20); k.line_to(140,-40); k.close_path()
    paper(ctx, vest, c('hivis'), off=(4,5))
    for yy in (-130,-80):
        ctx.new_path(); ctx.move_to(-148,yy); ctx.line_to(-50,yy-12); ctx.line_to(-48,yy+4); ctx.line_to(-146,yy+16); ctx.close_path()
        ctx.move_to(148,yy); ctx.line_to(50,yy-12); ctx.line_to(48,yy+4); ctx.line_to(146,yy+16); ctx.close_path()
        ctx.set_source_rgba(0.92,0.93,0.95,1); ctx.fill()
    # wings
    for sx in (-1,1):
        a = -wing*0.9 if sx==1 else 0
        ctx.save(); ctx.translate(sx*150,-210); ctx.rotate(sx*0.15+a)
        paper(ctx, lambda k,sx=sx:(k.new_path(),k.save(),k.translate(sx*15,80),k.scale(0.45,1),k.arc(0,0,95,0,2*math.pi),k.restore()), c('slate',1), off=(4,5))
        ctx.restore()
    # eyes
    for sx in (-1,1):
        ex, ey = sx*72, -300
        paper(ctx, lambda k,ex=ex,ey=ey:(k.new_path(),k.arc(ex,ey,66,0,2*math.pi)), c('cream'), off=(3,4))
        ctx.arc(ex+look[0]*12, ey+look[1]*10, 44, 0, 2*math.pi); ctx.set_source_rgba(*c('orange')); ctx.fill()
        ctx.arc(ex+look[0]*18, ey+look[1]*14, 24, 0, 2*math.pi); ctx.set_source_rgba(*c('ink')); ctx.fill()
        ctx.arc(ex+look[0]*18+9, ey+look[1]*14-10, 7, 0, 2*math.pi); ctx.set_source_rgba(1,1,1,0.9); ctx.fill()
        if blink>0:
            ctx.save(); ctx.arc(ex,ey,68,0,2*math.pi); ctx.clip()
            ctx.rectangle(ex-70, ey-70, 140, 140*blink); ctx.set_source_rgba(*c('slate')); ctx.fill(); ctx.restore()
    # beak
    paper(ctx, lambda k:(k.new_path(),k.move_to(-20,-255),k.line_to(20,-255),k.line_to(0,-215),k.close_path()), c('orange'), off=(2,3))
    # feet
    for sx in (-1,1):
        for d in (-14,0,14):
            ctx.arc(sx*55+d, -4, 10, 0, 2*math.pi); ctx.set_source_rgba(*c('orange')); ctx.fill()
    ctx.restore()

def you(ctx, x, y, s=1.0, phase=0.0, run=0.0, hold=False, lean=0.0):
    """Faceless grey-hoodie everyperson. (x,y)=feet. run 0..1 blends idle->run cycle."""
    ctx.save(); ctx.translate(x,y); ctx.scale(s,s); ctx.rotate(lean)
    sw = math.sin(phase)*run; bob = abs(math.sin(phase))*18*run
    ctx.translate(0,-bob)
    ctx.set_line_cap(cairo.LINE_CAP_ROUND)
    def limb(x0,y0,a1,l1,a2,l2,w,col):
        x1=x0+l1*math.sin(a1); y1=y0+l1*math.cos(a1); x2=x1+l2*math.sin(a1+a2); y2=y1+l2*math.cos(a1+a2)
        for o,cc in (((6,8),(0,0,0,0.25)),((0,0),col)):
            ctx.move_to(x0+o[0],y0+o[1]); ctx.line_to(x1+o[0],y1+o[1]); ctx.line_to(x2+o[0],y2+o[1])
            ctx.set_line_width(w); ctx.set_source_rgba(*cc); ctx.set_line_join(cairo.LINE_JOIN_ROUND); ctx.stroke()
    # back leg/arm
    limb(0,-150, -sw*0.9-0.13*(1-run), 80, max(0,sw)*1.2+0.05, 80, 34, c('slate'))
    limb(0,-290, sw*1.1 if run>0 else 0.15, 70, -0.9*run-0.2*(1-run), 65, 26, (0.45,0.49,0.57,1))
    # torso
    paper(ctx, lambda k: rrect(k,-55,-320,110,185,40), c('grey'))
    # front leg
    limb(0,-150, sw*0.9+0.13*(1-run), 80, max(0,-sw)*1.2+0.05, 80, 34, (0.25,0.36,0.44,1))
    # head / hood
    paper(ctx, lambda k:(k.new_path(),k.arc(0,-370,62,0,2*math.pi)), c('grey'))
    ctx.save(); ctx.translate(18,-365); ctx.scale(0.72,0.9); ctx.arc(0,0,40,0,2*math.pi); ctx.restore()
    ctx.set_source_rgba(0.16,0.18,0.24,1); ctx.fill()
    # front arm
    if hold:
        limb(10,-290, 0.6, 70, -1.9, 55, 26, c('grey'))
        # iced coffee
        paper(ctx, lambda k: rrect(k,52,-330,40,62,6), (0.55,0.36,0.22,1), off=(3,4))
        ctx.rectangle(52,-318,40,10); ctx.set_source_rgba(*c('cream')); ctx.fill()
        ctx.move_to(78,-330); ctx.line_to(86,-372); ctx.set_line_width(6); ctx.set_source_rgba(*c('red')); ctx.stroke()
    else:
        limb(0,-290, -sw*1.1 if run>0 else -0.15, 70, -0.9*run-0.2*(1-run), 65, 26, c('grey'))
    ctx.restore()
