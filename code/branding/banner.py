import cairo, random
W,H=2560,1440; NAVY=(0.055,0.075,0.16); ORANGE=(1.0,0.55,0.18); CREAM=(0.97,0.93,0.85)
s=cairo.ImageSurface(cairo.FORMAT_ARGB32,W,H); c=cairo.Context(s)
g=cairo.LinearGradient(0,0,0,H); g.add_color_stop_rgb(0,0.03,0.04,0.09); g.add_color_stop_rgb(0.62,*NAVY); g.add_color_stop_rgb(1,0.16,0.10,0.24); c.set_source(g); c.paint()
r=random.Random(7)
for _ in range(420):
    c.arc(r.random()*W,r.random()*H*0.75,r.choice([1.5,2,2.5,3]),0,7); c.set_source_rgba(1,1,1,0.55*r.random()); c.fill()
# city silhouette along the bottom
x=0; r=random.Random(4)
while x<W:
    w=r.randint(60,170); h=r.randint(90,300); c.rectangle(x,H-h,w,h); c.set_source_rgb(0.035,0.045,0.10); c.fill()
    if r.random()<0.12: c.rectangle(x+w*0.35,H-h+40,22,22); c.set_source_rgb(1,0.85,0.45); c.fill()
    x+=w+r.randint(0,10)
def txt(t,size,col,w,x,y):
    c.select_font_face("Inter Display",cairo.FONT_SLANT_NORMAL,w); c.set_font_size(size); c.move_to(x,y); c.set_source_rgb(*col); c.show_text(t)
    return c.text_extents(t)
B=cairo.FONT_WEIGHT_BOLD; N=cairo.FONT_WEIGHT_NORMAL
def ext(t,size,w): c.select_font_face("Inter Display",cairo.FONT_SLANT_NORMAL,w); c.set_font_size(size); return c.text_extents(t)
parts=[("the ",96,CREAM,N),("UNLIKELY",190,ORANGE,B),(" you",170,CREAM,B)]
tot=sum(ext(t,sz,w).x_advance for t,sz,_,w in parts); x=W/2-tot/2; base=H/2+40
for t,sz,col,w in parts:
    txt(t,sz,col,w,x,base); x+=ext(t,sz,w).x_advance
tag="What would you do?  Unlikely scenarios, real science."
e=ext(tag,54,N); txt(tag,54,(0.80,0.80,0.86),N,W/2-e.width/2-e.x_bearing,base+105)
s.write_to_png("/mnt/project-files/branding/youtube_banner.png")
# preview with safe area (1546x423)
c.rectangle((W-1546)/2,(H-423)/2,1546,423); c.set_source_rgba(0,1,0.5,0.8); c.set_line_width(4); c.stroke()
s.write_to_png("/tmp/claude-0/banner_safe.png")
