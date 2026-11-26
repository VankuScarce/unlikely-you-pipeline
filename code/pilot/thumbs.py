import sys, math, cairo
sys.path.insert(0, __import__('os').path.dirname(__file__))
from style import *
def new():
    s=cairo.ImageSurface(cairo.FORMAT_ARGB32,W,H); return s,cairo.Context(s)
def sirenbg(ctx):
    ctx.set_source_rgba(*c('ink')); ctx.paint()
    for col,x in (('red',0),('blue',W)):
        g=cairo.RadialGradient(x,H/2,50,x,H/2,1300); g.add_color_stop_rgba(0,*c(col,0.85)); g.add_color_stop_rgba(1,0,0,0,0); ctx.set_source(g); ctx.paint()
def big(ctx,s,x,y,size,col,anchor='c'):
    ctx.select_font_face('Inter Display',cairo.FONT_SLANT_NORMAL,cairo.FONT_WEIGHT_BOLD); ctx.set_font_size(size)
    e=ctx.text_extents(s); dx={'c':-e.width/2,'l':0,'r':-e.width}[anchor]-e.x_bearing
    ctx.move_to(x+dx,y-e.height/2-e.y_bearing); ctx.text_path(s)
    ctx.set_line_width(size*0.09); ctx.set_line_join(cairo.LINE_JOIN_ROUND); ctx.set_source_rgba(*c('ink')); ctx.stroke_preserve()
    ctx.set_source_rgba(*col); ctx.fill()
out=sys.argv[1]
# A: Ozzie shocked + 5 stars + HOW LONG?
s,ctx=new(); sirenbg(ctx)
you(ctx,1480,1000,1.6,phase=1.2,run=1.0,lean=0.15)
ozzie(ctx,430,1120,1.7,look=(0.8,-0.3))
for i in range(5): star(ctx,760+i*150,170,70,c('yellow'))
big(ctx,"HOW LONG?",1180,420,190,c('cream'))
vignette(ctx,0.4); grain(ctx,0.1); s.write_to_png(f"{out}/thumb_A_how_long.png")
# B: helicopter spotlight + timer
s,ctx=new(); ctx.set_source_rgba(0.03,0.05,0.10,1); ctx.paint()
ctx.save(); ctx.move_to(1500,-50); ctx.line_to(700,1080); ctx.line_to(1350,1080); ctx.close_path()
g=cairo.LinearGradient(1500,0,1000,1080); g.add_color_stop_rgba(0,1,1,0.9,0.05); g.add_color_stop_rgba(1,1,1,0.85,0.45); ctx.set_source(g); ctx.fill(); ctx.restore()
ctx.save(); ctx.translate(1025,1010); ctx.scale(1,0.18); ctx.arc(0,0,330,0,2*math.pi); ctx.restore(); ctx.set_source_rgba(1,1,0.85,0.5); ctx.fill()
you(ctx,1025,1010,1.5,phase=0.3,run=0.0)
# heli silhouette
ctx.save(); ctx.translate(1560,120); ctx.rotate(-0.15)
paper(ctx,lambda k:(k.new_path(),k.save(),k.scale(1.6,1),k.arc(0,0,70,0,2*math.pi),k.restore()),c('slate'))
paper(ctx,lambda k:k.rectangle(80,-15,240,30),c('slate')); ctx.rectangle(-220,-95,440,10); ctx.set_source_rgba(*c('slate')); ctx.fill(); ctx.restore()
paper(ctx,lambda k:rrect(k,60,90,720,220,30),c('red'))
text(ctx,"00:47:12",420,200,150,c('cream'),font='DejaVu Sans Mono')
big(ctx,"5 STARS.",60,560,170,c('yellow'),anchor='l'); big(ctx,"REAL LIFE.",60,760,170,c('cream'),anchor='l')
vignette(ctx,0.4); grain(ctx,0.1); s.write_to_png(f"{out}/thumb_B_spotlight.png")
# C: case file + typo
s,ctx=new(); ctx.set_source_rgba(0.86,0.80,0.70,1); ctx.paint()
ctx.save(); ctx.translate(1240,560); ctx.rotate(0.05)
paper(ctx,lambda k:rrect(k,-560,-430,1100,860,16),(0.86,0.66,0.38,1),off=(14,16))
paper(ctx,lambda k:k.rectangle(-500,-380,980,760),c('cream'))
paper(ctx,lambda k:k.rectangle(-440,-320,400,520),(0.70,0.74,0.80,1))
ctx.save(); ctx.rectangle(-440,-320,400,520); ctx.clip(); you(ctx,-240,380,1.15); ctx.restore()
ctx.save(); ctx.translate(180,40); ctx.rotate(-0.2); ctx.set_line_width(16); rrect(ctx,-300,-90,600,180,20); ctx.set_source_rgba(*c('red')); ctx.stroke()
text(ctx,"WANTED",0,0,130,c('red')); ctx.restore(); ctx.restore()
ozzie(ctx,330,1150,1.5,look=(1,0.2),wing=1.0)
big(ctx,"IT WAS A TYPO.",80,140,130,c('ink') if False else c('cream'),anchor='l')
vignette(ctx,0.3); grain(ctx,0.1); s.write_to_png(f"{out}/thumb_C_typo.png")
print('ok')
