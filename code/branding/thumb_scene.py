# Custom-drawn thumbnail backgrounds (1920x1080) using the episode renderer; text is added in thumbs_everyone_vanished.py.
import os, sys, math, cairo
R=os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'everyone_vanished')
sys.path.insert(0,R); sys.path.insert(0,os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'pilot'))
import ep02
from ep02 import *
OUT='/tmp/claude-0/thumbs/'
def surf():
    s=cairo.ImageSurface(cairo.FORMAT_ARGB32,W,H); return s,cairo.Context(s)
def eyes(ctx,x,y,r=13,gap=34):
    for dx in (0,gap):
        g=cairo.RadialGradient(x+dx,y,0,x+dx,y,r*5); g.add_color_stop_rgba(0,1,0.85,0.3,0.9); g.add_color_stop_rgba(1,1,0.7,0.2,0)
        ctx.set_source(g); ctx.arc(x+dx,y,r*5,0,7); ctx.fill()
        ctx.arc(x+dx,y,r,0,7); ctx.set_source_rgb(1,0.92,0.55); ctx.fill()

# A: night street, YOU in the foreground, eyes in a dark alley behind the knocked bin
s,ctx=surf()
street_bg(ctx,'night',0,lit=0.0)
stars(ctx,200,alpha=0.7,y1=600)
# alley gap between buildings (dark)
ctx.rectangle(1400,470,260,340); ctx.set_source_rgb(0.01,0.01,0.02); ctx.fill()
eyes(ctx,1490,700,r=16,gap=42)
# knocked bin
ctx.save(); ctx.translate(1300,905); ctx.rotate(-0.35); ctx.rectangle(-60,-70,120,140); ctx.set_source_rgb(0.30,0.33,0.36); ctx.fill(); ctx.restore()
# YOU, large, looking right toward it
ctx.save(); you(ctx,430,1075,1.45,phase=0,run=0,face=1); ctx.restore()
# cold moonlight wash
g=cairo.LinearGradient(0,0,W,0); g.add_color_stop_rgba(0,0,0,0,0.0); g.add_color_stop_rgba(1,0,0,0,0.25); ctx.set_source(g); ctx.paint()
s.write_to_png(OUT+'scene_A.png')

# C: day, YOU alone on an empty street next to the running car, wide
s,ctx=surf()
street_bg(ctx,'day',0)
cx=1350; car(ctx,cx,990,1.3,wheel=0,bounce=0,beam=False)
ctx.save(); ctx.translate(cx+10,880); ctx.move_to(0,0); ctx.line_to(90,-40); ctx.line_to(95,60); ctx.line_to(0,70); ctx.close_path(); ctx.set_source_rgba(0.50,0.53,0.58,1); ctx.fill(); ctx.restore()
for i in range(4):
    q=i*0.25; ctx.arc(cx-240-q*200,960-q*60,14+q*40,0,7); ctx.set_source_rgba(0.9,0.9,0.92,0.5*(1-q)); ctx.fill()
you(ctx,720,1000,1.25,phase=0,run=0,face=1)
s.write_to_png(OUT+'scene_C.png')
