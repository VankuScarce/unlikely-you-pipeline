# Thumbnail set v2 for "What If Everyone Vanished... Except You?": close-up emotion, split before/after, lone figure. No twist.
import os, sys, math, random, cairo
R=os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'everyone_vanished')
sys.path.insert(0,R); sys.path.insert(0,os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'pilot'))
from ep02 import *
import character as CH
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
OUT='/tmp/claude-0/thumbs2/'
def surf(alpha=False):
    s=cairo.ImageSurface(cairo.FORMAT_ARGB32,W,H); return s,cairo.Context(s)
def topil(s):
    s.flush(); return Image.frombuffer('RGBA',(W,H),bytes(s.get_data()),'raw','BGRA',0,1)

def bust(ctx, x, y, k, mood='shock', glow=None):
    """Head+shoulders of YOU, head centre at (x,y), k = scale (1 = in-video size)."""
    ctx.save(); ctx.translate(x,y); ctx.scale(k,k)
    # shoulders / jacket
    ctx.move_to(-120,150); ctx.curve_to(-110,70,-60,52,-10,48); ctx.line_to(30,48); ctx.curve_to(80,52,130,70,140,150); ctx.line_to(150,260); ctx.line_to(-130,260); ctx.close_path()
    ctx.set_source_rgba(*CH.JACKET); ctx.fill()
    ctx.move_to(5,48); ctx.line_to(30,48); ctx.line_to(36,260); ctx.line_to(14,260); ctx.close_path(); ctx.set_source_rgba(*CH.TEE); ctx.fill()
    ctx.move_to(-14,46); ctx.line_to(6,90); ctx.line_to(2,46); ctx.close_path(); ctx.set_source_rgba(*CH.JACKET_D); ctx.fill()
    ctx.move_to(32,46); ctx.line_to(46,92); ctx.line_to(48,48); ctx.close_path(); ctx.set_source_rgba(*CH.JACKET_D); ctx.fill()
    # neck
    ctx.rectangle(-12,18,30,34); ctx.set_source_rgba(*CH.SKIN_D); ctx.fill()
    # face
    ctx.save(); ctx.translate(5,0); ctx.scale(33,40); ctx.arc(0,0,1,0,7); ctx.restore(); ctx.set_source_rgba(*CH.SKIN); ctx.fill()
    ctx.move_to(-10,20); ctx.curve_to(10,44,30,40,36,14); ctx.line_to(30,0); ctx.close_path(); ctx.fill()
    # hair
    ctx.move_to(-28,14); ctx.curve_to(-40,-20,-28,-48,2,-50); ctx.curve_to(28,-52,44,-36,40,-16)
    ctx.curve_to(30,-26,18,-24,8,-30); ctx.curve_to(4,-18,-6,-12,-12,-4); ctx.curve_to(-16,4,-20,12,-28,14)
    ctx.close_path(); ctx.set_source_rgba(*CH.HAIR); ctx.fill()
    ctx.save(); ctx.translate(-12,2); ctx.scale(7,10); ctx.arc(0,0,1,0,7); ctx.restore(); ctx.set_source_rgba(*CH.SKIN_D); ctx.fill()
    # eyes: white + pupil, worried brows
    for ex,r in ((15,6.2),(32,5.0)):
        ctx.save(); ctx.translate(ex,-2); ctx.scale(r,r*1.3); ctx.arc(0,0,1,0,7); ctx.restore(); ctx.set_source_rgb(1,1,1); ctx.fill()
        ctx.save(); ctx.translate(ex+1.6,-1.5); ctx.scale(r*0.5,r*0.62); ctx.arc(0,0,1,0,7); ctx.restore(); ctx.set_source_rgba(*CH.INK); ctx.fill()
        ctx.move_to(ex-7,-14); ctx.line_to(ex+6,-19 if ex<20 else -17); ctx.set_line_width(3.0); ctx.set_source_rgba(*CH.HAIR); ctx.stroke()
    # nose
    ctx.move_to(37,-1); ctx.line_to(43,12); ctx.line_to(36,14); ctx.set_line_width(2.2); ctx.set_source_rgba(*CH.SKIN_D); ctx.stroke()
    # mouth
    if mood=='shock':
        ctx.save(); ctx.translate(29,26); ctx.scale(4.2,5.4); ctx.arc(0,0,1,0,7); ctx.restore(); ctx.set_source_rgb(0.30,0.12,0.12); ctx.fill()
    else:
        ctx.move_to(22,25); ctx.curve_to(27,23,32,23,35,25); ctx.set_line_width(2.4); ctx.set_source_rgba(0.55,0.30,0.28,1); ctx.stroke()
    ctx.restore()

def light(ctx, x, y, r, col, a):
    g=cairo.RadialGradient(x,y,0,x,y,r); g.add_color_stop_rgba(0,*col,a); g.add_color_stop_rgba(1,*col,0); ctx.set_source(g); ctx.paint()

# ---------- D: close-up, phone glow, empty night city ----------
s,ctx=surf(); street_bg(ctx,'night',0,lit=0.0); stars(ctx,160,alpha=0.6,y1=500)
ctx.rectangle(1335,360,26,34); ctx.set_source_rgb(1,0.82,0.4); ctx.fill()   # one lit window far away
light(ctx,1348,377,90,(1,0.8,0.4),0.35)
bg=topil(s).convert('RGB').filter(ImageFilter.GaussianBlur(5)); bg=ImageEnhance.Brightness(bg).enhance(0.8)
s,ctx=surf(); bust(ctx,420,520,8.0,'shock')
# phone in hand, bottom right of face
ctx.save(); ctx.translate(800,1000); ctx.rotate(-0.25); ctx.rectangle(-70,-140,140,260); ctx.set_source_rgb(0.08,0.08,0.10); ctx.fill()
ctx.rectangle(-60,-128,120,236); ctx.set_source_rgb(0.75,0.88,1.0); ctx.fill(); ctx.restore()
ctx.arc(725,1040,70,0,7); ctx.set_source_rgba(*CH.SKIN); ctx.fill()
fg=topil(s)
# cold phone light on the face
gl,gctx=surf(); light(gctx,720,900,650,(0.55,0.78,1.0),0.45); glow=topil(gl)
mask=fg.split()[3]
lit=Image.alpha_composite(fg, Image.composite(glow, Image.new('RGBA',(W,H),(0,0,0,0)), mask))
im=bg.convert('RGBA'); im.alpha_composite(lit)
vig=Image.new('L',(W,H),0); ImageDraw.Draw(vig).ellipse((-400,-300,W+400,H+300),fill=255); vig=vig.filter(ImageFilter.GaussianBlur(160))
im=Image.composite(im, Image.new('RGBA',(W,H),(0,0,0,255)), vig)
im.convert('RGB').save(OUT+'bg_D.png')

# ---------- E: before / after split ----------
random.seed(4)
PAL=[(0.78,0.30,0.28),(0.95,0.70,0.25),(0.30,0.45,0.70),(0.55,0.35,0.60),(0.85,0.85,0.80),(0.35,0.60,0.45),(0.20,0.22,0.28),(0.90,0.50,0.40)]
def person(ctx,x,yy,sc,col):
    t=cairo.ImageSurface(cairo.FORMAT_ARGB32,W,H); tc=cairo.Context(t)
    CH.you(tc,x,yy,sc,phase=random.uniform(0,6),run=random.choice((0,0.5)),face=random.choice((1,-1)))
    ctx.set_source_rgb(*col); ctx.mask_surface(t,0,0)
s1,c1=surf(); street_bg(c1,'day',0)
for i in range(5): car(c1,random.uniform(100,W-100),975,0.95,wheel=0,bounce=0,beam=False)
pts=sorted([(random.uniform(880,1090),random.uniform(-60,W+60)) for i in range(60)])
for yy,x in pts: person(c1,x,yy,0.42+(yy-880)/210*0.45,random.choice(PAL))
A=topil(s1).convert('RGB')
s2,c2=surf(); street_bg(c2,'night',0,lit=0.0); stars(c2,150,alpha=0.6,y1=600)
car(c2,1450,990,1.3,wheel=0,bounce=0,beam=True)
CH.you(c2,1250,1040,1.45,phase=0,run=0,face=-1)
B=topil(s2).convert('RGB')
im=Image.new('RGB',(W,H)); im.paste(A.crop((0,0,W//2,H)),(0,0)); im.paste(B.crop((W//2,0,W,H)),(W//2,0))
d=ImageDraw.Draw(im); d.rectangle((W//2-10,0,W//2+10,H),fill=(255,255,255))
im.save(OUT+'bg_E.png')

# ---------- F: lone figure on a jammed, abandoned highway (high angle) ----------
s,ctx=surf()
g=cairo.LinearGradient(0,0,0,H); g.add_color_stop_rgb(0,0.98,0.62,0.35); g.add_color_stop_rgb(0.45,0.85,0.45,0.40); g.add_color_stop_rgb(1,0.30,0.22,0.30); ctx.set_source(g); ctx.paint()
skyline(ctx,0,520,120,360,(0.22,0.16,0.24,1),lit=0.0,seed=8)
# highway in perspective
ctx.move_to(W/2-60,520); ctx.line_to(W/2+60,520); ctx.line_to(W+500,H); ctx.line_to(-500,H); ctx.close_path(); ctx.set_source_rgb(0.24,0.23,0.27); ctx.fill()
for lane in (-1,0,1):
    for i in range(14):
        t0=(i/14)**1.8; t1=((i+0.5)/14)**1.8
        def P(t,l): return (W/2+l*60*(1-t)/3*0+ l*(t*(W/2+500)/1.6+20*(1-t)), 520+t*(H-520))
        if lane==0: continue
        x0,y0=P(t0,lane*0.5); x1,y1=P(t1,lane*0.5)
        ctx.move_to(x0,y0); ctx.line_to(x1,y1); ctx.set_line_width(2+t0*14); ctx.set_source_rgba(1,0.85,0.4,0.8); ctx.stroke()
random.seed(11)
cars=[]
for i in range(26):
    t=random.uniform(0.05,1.0)**1.3; lane=random.choice((-0.75,-0.25,0.25,0.75))
    x=W/2+lane*(t*(W/2+500)/1.0); y=520+t*(H-520)
    cars.append((y,x,0.15+t*1.05))
cars.sort()
for y,x,sc in cars:
    if y>960: continue
    car(ctx,x,y,sc,wheel=0,bounce=0,beam=False)
CH.you(ctx,380,1075,1.6,phase=0,run=0,face=1)
s.write_to_png(OUT+'bg_F.png')
print('ok')
