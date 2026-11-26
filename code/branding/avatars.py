import cairo, math, random, sys
S=1080; OUT=sys.argv[1] if len(sys.argv)>1 else '.'
NAVY=(0.055,0.075,0.16); NAVY2=(0.10,0.13,0.26); ORANGE=(1.0,0.55,0.18); CREAM=(0.97,0.93,0.85); INK=(0.05,0.05,0.08)
def surf(): s=cairo.ImageSurface(cairo.FORMAT_ARGB32,S,S); return s,cairo.Context(s)
def bg_grad(c,top,bot):
    g=cairo.LinearGradient(0,0,0,S); g.add_color_stop_rgb(0,*top); g.add_color_stop_rgb(1,*bot); c.set_source(g); c.paint()
def stars(c,n,seed=3,a=0.7,ymax=S):
    r=random.Random(seed)
    for _ in range(n):
        x,y=r.random()*S,r.random()*ymax; c.arc(x,y,r.choice([1.5,2,2.5,3.5]),0,7); c.set_source_rgba(1,1,1,a*r.random()); c.fill()
def figure(c,x,y,h,col):
    # simple style-neutral standing person, feet at (x,y), height h
    u=h/100
    c.set_source_rgb(*col)
    c.arc(x,y-88*u,8.5*u,0,7); c.fill()                                   # head
    c.move_to(x-10*u,y-76*u); c.curve_to(x-13*u,y-60*u,x-12*u,y-50*u,x-10*u,y-44*u)
    c.line_to(x+10*u,y-44*u); c.curve_to(x+12*u,y-50*u,x+13*u,y-60*u,x+10*u,y-76*u); c.close_path(); c.fill()  # torso
    c.set_line_cap(cairo.LINE_CAP_ROUND)
    for dx in (-5,5):
        c.move_to(x+dx*u,y-46*u); c.line_to(x+dx*1.1*u,y-2*u); c.set_line_width(8*u); c.stroke()  # legs
    for dx in (-12,12):
        c.move_to(x+dx*0.85*u,y-72*u); c.line_to(x+dx*1.05*u,y-46*u); c.set_line_width(6.5*u); c.stroke()  # arms
def font(c,w=cairo.FONT_WEIGHT_BOLD,f="Inter Display"): c.select_font_face(f,cairo.FONT_SLANT_NORMAL,w)
def ctext(c,t,y,size,col,f="Inter Display",w=cairo.FONT_WEIGHT_BOLD,x=S/2):
    font(c,w,f); c.set_font_size(size); e=c.text_extents(t); c.move_to(x-e.width/2-e.x_bearing,y); c.set_source_rgb(*col); c.show_text(t)

# A: spotlight - lone figure in a cone of light
s,c=surf(); bg_grad(c,(0.03,0.04,0.09),NAVY2); stars(c,70,a=0.5,ymax=600)
g=cairo.LinearGradient(0,120,0,860); g.add_color_stop_rgba(0,1,0.85,0.6,0.0); g.add_color_stop_rgba(1,1,0.78,0.5,0.42)
c.move_to(540-40,120); c.line_to(540+40,120); c.line_to(540+250,860); c.line_to(540-250,860); c.close_path(); c.set_source(g); c.fill()
c.save(); c.translate(540,860); c.scale(1,0.18); c.arc(0,0,250,0,7); c.restore(); c.set_source_rgba(1,0.8,0.55,0.55); c.fill()
figure(c,540,860,330,INK)
s.write_to_png(f"{OUT}/A_spotlight.png")

# B: question mark whose dot is the person
s,c=surf(); bg_grad(c,NAVY,(0.16,0.10,0.24))
c.set_line_cap(cairo.LINE_CAP_ROUND); c.set_line_width(110); c.set_source_rgb(*ORANGE)
c.arc(540,390,190,math.radians(190),math.radians(40)); 
c.curve_to(540+150,560,540,560,540,680); c.stroke()
figure(c,540,960,190,CREAM)
s.write_to_png(f"{OUT}/B_question_person.png")

# C: wordmark logo - "the UNLIKELY you"
s,c=surf(); c.set_source_rgb(*NAVY); c.paint()
ctext(c,"the",400,96,CREAM,w=cairo.FONT_WEIGHT_NORMAL)
ctext(c,"UNLIKELY",590,190,ORANGE,f="Inter Display",w=cairo.FONT_WEIGHT_BOLD)
ctext(c,"you",760,170,CREAM,w=cairo.FONT_WEIGHT_BOLD)
s.write_to_png(f"{OUT}/C_wordmark.png")

# D: monogram "U" with a lone figure inside + one lit window motif
s,c=surf(); bg_grad(c,(1.0,0.60,0.30),(0.55,0.20,0.35))
c.set_line_cap(cairo.LINE_CAP_ROUND); c.set_line_width(120); c.set_source_rgb(*NAVY)
c.move_to(300,200); c.line_to(300,560); c.arc_negative(540,560,240,math.pi,0); c.line_to(780,200); c.stroke()
figure(c,540,742,250,CREAM)
s.write_to_png(f"{OUT}/D_monogram_U.png")
