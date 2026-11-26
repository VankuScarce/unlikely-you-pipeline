import sys, math, subprocess, cairo, numpy as np
sys.path.insert(0, __import__('os').path.dirname(__file__))
from style import *

FPS = 24
DUR = 40.0

def bg(ctx, top, bot):
    g = cairo.LinearGradient(0,0,0,H); g.add_color_stop_rgba(0,*top); g.add_color_stop_rgba(1,*bot)
    ctx.set_source(g); ctx.paint()

# ---------- S1 gas station 0-8.6 ----------
def s1(ctx, t):
    bg(ctx, c('sky'), (0.98,0.88,0.72,1))
    z = 1+0.06*ease(t/8.6); ctx.save(); ctx.translate(W/2,H/2); ctx.scale(z,z); ctx.translate(-W/2,-H/2)
    # sun + palms
    ctx.arc(1600,230,110,0,2*math.pi); ctx.set_source_rgba(1,0.93,0.7,1); ctx.fill()
    for px,sc in ((180,1.0),(1750,0.8)):
        paper(ctx, lambda k,px=px,sc=sc:(k.new_path(),k.move_to(px-14*sc,880),k.curve_to(px-10*sc,600,px+30*sc,450,px+40*sc,330),k.line_to(px+60*sc,330),k.curve_to(px+50*sc,460,px+15*sc,620,px+14*sc,880),k.close_path()),(0.55,0.42,0.30,1))
        for a in range(6):
            ang = -2.6 + a*0.55 + 0.04*math.sin(t*1.5+a)
            paper(ctx, lambda k,px=px,sc=sc,ang=ang:(k.new_path(),k.save(),k.translate(px+50*sc,330),k.rotate(ang),k.scale(1,0.22),k.arc(130*sc,0,130*sc,0,2*math.pi),k.restore()), c('palm'), off=(4,5))
    # ground
    ctx.rectangle(0,860,W,220); ctx.set_source_rgba(0.42,0.44,0.48,1); ctx.fill()
    for i in range(8): ctx.rectangle(i*260+40,955,140,14); ctx.set_source_rgba(1,1,1,0.6); ctx.fill()
    # station
    paper(ctx, lambda k: k.rectangle(430,470,1060,400), c('cream'))
    paper(ctx, lambda k: k.rectangle(380,400,1160,90), c('red'))
    text(ctx, "QUIK STOP", 960, 446, 58, c('cream'))
    # windows w/ interior
    paper(ctx, lambda k: k.rectangle(480,540,620,300), (0.30,0.52,0.58,1), off=(4,5))
    ctx.rectangle(480,540,620,300); ctx.set_source_rgba(0.75,0.88,0.9,0.35); ctx.fill()
    for i in range(4):
        ctx.rectangle(500+i*150,600,120,240); ctx.set_source_rgba(0.95,0.95,0.9,0.25); ctx.fill()
    # door
    paper(ctx, lambda k: k.rectangle(1180,560,220,310), (0.30,0.52,0.58,1), off=(4,5))
    # you inside window
    ctx.save(); ctx.rectangle(480,540,620,300); ctx.clip(); you(ctx, 790, 900, 0.72, hold=True); ctx.restore()
    ctx.restore()
    # clock card
    a = ease(prog(t,0.2,0.9))
    ctx.save(); ctx.translate(250, 170 - 40*(1-a))
    paper(ctx, lambda k: rrect(k,-170,-75,340,150,22), c('ink',0.92*a))
    text(ctx, "9:14 AM", 0, -10, 76, c('orange',a)); text(ctx, "TUESDAY", 0, 48, 28, c('cream',a))
    ctx.restore()
    # "nothing wrong" stamp-ish caption
    a2 = back(prog(t,6.4,6.9)); 
    if a2>0:
        ctx.save(); ctx.translate(1380,250); ctx.scale(a2,a2); ctx.rotate(-0.05)
        paper(ctx, lambda k: rrect(k,-300,-55,600,110,16), c('teal'))
        text(ctx, "INNOCENT. FOR NOW.", 0, 0, 50, c('cream')); ctx.restore()

# ---------- S2 clerk office 8.6-14.0 ----------
def s2(ctx, t):
    lt = t-8.6
    bg(ctx, (0.06,0.08,0.16,1), (0.10,0.12,0.22,1))
    z = 1+0.25*ease(lt/5.4); ctx.save(); ctx.translate(W/2,H/2); ctx.scale(z,z); ctx.translate(-W/2,-H/2+30*ease(lt/5.4))
    # desk
    paper(ctx, lambda k: k.rectangle(0,820,W,260), (0.20,0.16,0.18,1))
    # monitor
    paper(ctx, lambda k: rrect(k,560,230,800,520,24), c('ink'))
    ctx.rectangle(590,260,740,460); ctx.set_source_rgba(0.12,0.30,0.35,1); ctx.fill()
    paper(ctx, lambda k: k.rectangle(910,750,100,70), c('ink'))
    # glow
    g = cairo.RadialGradient(960,490,50,960,490,700); g.add_color_stop_rgba(0,0.3,0.8,0.85,0.18); g.add_color_stop_rgba(1,0,0,0,0)
    ctx.set_source(g); ctx.paint()
    # record
    text(ctx, "STATE RECORDS  //  CASE 88-204", 620, 300, 30, c('cream',0.8), anchor='l', font='DejaVu Sans Mono')
    rows = [("NAME", "[ YOU ]"), ("STATUS", "CLEAR"), ("LINK ID", "4471-0")]
    flip = prog(lt, 2.4, 2.6)
    for i,(k,v) in enumerate(rows):
        yy = 380+i*80
        text(ctx, k, 640, yy, 34, c('cream',0.6), anchor='l', font='DejaVu Sans Mono')
        if k=="LINK ID":
            v = "4471-0" if flip<1 else "4471-9"
            col = c('cream') if flip<1 else c('red')
        elif k=="STATUS":
            v = "CLEAR" if lt<3.6 else "FLAGGED: FELONY x5"
            col = c('yellow') if lt<3.6 else c('red')
        else: col = c('yellow')
        text(ctx, v, 900, yy, 38, col, anchor='l', font='DejaVu Sans Mono')
    # cursor blink
    if int(lt*3)%2==0: ctx.rectangle(1090,600,22,40); ctx.set_source_rgba(*c('cream')); ctx.fill()
    # hands silhouette
    for hx,ph in ((760,0),(1160,1.3)):
        dy = 12*max(0,math.sin(lt*14+ph)) if 1.4<lt<2.8 else 0
        paper(ctx, lambda k,hx=hx,dy=dy:(k.new_path(),k.save(),k.translate(hx,900+dy),k.scale(1.6,0.7),k.arc(0,0,80,0,2*math.pi),k.restore()), (0.04,0.05,0.09,1))
    paper(ctx, lambda k: rrect(k,640,860,640,60,10), (0.15,0.16,0.20,1), off=(3,4))
    ctx.restore()
    a = ease(prog(lt,0.1,0.7))*(1-ease(prog(lt,4.8,5.4)))
    paper(ctx, lambda k: rrect(k,70,70,520,100,18), c('orange',a))
    text(ctx, "200 MILES AWAY", 330, 120, 50, c('ink',a))
    if 2.4<lt<3.0:
        ctx.set_source_rgba(*c('red', 0.25*(1-prog(lt,2.4,3.0)))); ctx.paint()

# ---------- S3 file + stamp 14.0-19.0 ----------
def s3(ctx, t):
    lt = t-14.0
    bg(ctx, (0.85,0.80,0.70,1), (0.75,0.68,0.58,1))
    # desk wood stripes
    for i in range(12): ctx.rectangle(0,i*95,W,4); ctx.set_source_rgba(0,0,0,0.05); ctx.fill()
    a = back(prog(lt,0,0.6)); x = 960 + (1-a)*-1300
    ctx.save(); ctx.translate(x,560); ctx.rotate(-0.04)
    paper(ctx, lambda k: rrect(k,-560,-380,1120,760,14), (0.86,0.66,0.38,1), off=(12,14))
    paper(ctx, lambda k: rrect(k,-560,-430,300,80,14), (0.86,0.66,0.38,1), off=(0,0))
    paper(ctx, lambda k: k.rectangle(-500,-330,1000,640), c('cream'), off=(5,6))
    # photo
    paper(ctx, lambda k: k.rectangle(-460,-280,330,420), (0.70,0.74,0.80,1), off=(5,6))
    ctx.save(); ctx.rectangle(-460,-280,330,420); ctx.clip(); you(ctx,-295,320,0.95); ctx.restore()
    for i,l in enumerate(["SUBJECT: YOU","AGE: ADULT","LAST SEEN: QUIK STOP, 9:14 AM","THREAT LEVEL: ?????"]):
        text(ctx, l, -80, -230+i*70, 36, c('ink',0.85), anchor='l', font='DejaVu Sans Mono')
    # stamp
    sa = prog(lt,1.4,1.65)
    if sa>0:
        s = 2.2-1.2*ease(sa)
        ctx.save(); ctx.translate(120,180); ctx.rotate(-0.12); ctx.scale(s,s)
        al = min(1,sa*1.5)
        ctx.set_line_width(12); rrect(ctx,-330,-80,660,160,20); ctx.set_source_rgba(*c('red',al)); ctx.stroke()
        text(ctx, "MOST WANTED", 0, 0, 96, c('red',al))
        ctx.restore()
    ctx.restore()
    if 1.6<lt<1.9:
        ctx.save(); ctx.translate(math.sin(lt*90)*10, math.cos(lt*80)*8); ctx.restore()

# ---------- S4 map + scanners 19.0-22.2 ----------
def s4(ctx, t):
    lt = t-19.0
    bg(ctx, c('navy'), (0.05,0.08,0.16,1))
    # stylised peninsula
    def land(k):
        k.new_path(); k.move_to(300,0); k.line_to(1500,0); k.line_to(1480,200); k.curve_to(1400,350,1380,500,1300,650)
        k.curve_to(1250,800,1180,950,1100,1080); k.line_to(980,1080); k.curve_to(960,900,900,700,820,560)
        k.curve_to(700,380,520,280,300,220); k.close_path()
    paper(ctx, land, (0.16,0.30,0.32,1), off=(10,12))
    # roads
    ctx.set_line_width(4); ctx.set_source_rgba(1,1,1,0.12)
    for i in range(10): ctx.move_to(400+i*110,0); ctx.line_to(800+i*60,1080); ctx.stroke()
    towers = [(700,260),(1100,180),(1250,520),(1050,820),(900,450),(1350,330)]
    for i,(tx,ty) in enumerate(towers):
        st = 0.25*i
        for r in range(3):
            p = ((lt-st)*0.8 + r/3) % 1
            if lt<st: continue
            ctx.arc(tx,ty,30+p*260,0,2*math.pi); ctx.set_line_width(5); ctx.set_source_rgba(*c('red',0.7*(1-p))); ctx.stroke()
        paper(ctx, lambda k,tx=tx,ty=ty:(k.new_path(),k.move_to(tx,ty-34),k.line_to(tx+20,ty+20),k.line_to(tx-20,ty+20),k.close_path()), c('cream'), off=(3,4))
    # you dot
    pulse = 0.5+0.5*math.sin(lt*8)
    ctx.arc(1180,640,16+6*pulse,0,2*math.pi); ctx.set_source_rgba(*c('orange')); ctx.fill()
    a = ease(prog(lt,0.3,0.8))
    paper(ctx, lambda k: rrect(k,80,820,720,170,20), c('ink',0.9*a))
    text(ctx, "ALL UNITS:", 120, 870, 40, c('red',a), anchor='l', font='DejaVu Sans Mono')
    text(ctx, "BE ON THE LOOKOUT FOR [YOU]", 120, 940, 34, c('cream',a), anchor='l', font='DejaVu Sans Mono')

# ---------- S5 choice 22.2-26.0 ----------
def s5(ctx, t):
    lt = t-22.2
    ctx.set_source_rgba(*c('ink')); ctx.paint()
    calm = ease(prog(lt,1.6,2.1)); run = back(prog(lt,3.0,3.3))
    # left calm
    ctx.rectangle(0,0,W/2,H); ctx.set_source_rgba(*c('teal', 0.35+0.4*calm*(1-run*0.8))); ctx.fill()
    ctx.rectangle(W/2,0,W/2,H); ctx.set_source_rgba(*c('red', 0.25+0.7*run)); ctx.fill()
    a0 = ease(prog(lt,0,0.4))
    text_paper(ctx, "ONE CHOICE", W/2, 150, 64, c('cream',a0))
    ctx.save(); ctx.translate(W/4,560); s=0.8+0.2*calm-0.25*run; ctx.scale(s,s)
    text_paper(ctx, "STAY CALM", 0, 0, 130, c('cream', 0.3+0.7*calm*(1-0.6*run))); ctx.restore()
    ctx.save(); ctx.translate(3*W/4,560); s=0.6+0.6*run; ctx.scale(s,s); ctx.rotate(-0.06*run)
    text_paper(ctx, "RUN", 0, 0, 220, c('cream', 0.25+0.75*run)); ctx.restore()

# ---------- S6 running + stars 26.0-33.2 ----------
def s6(ctx, t):
    lt = t-26.0
    bg(ctx, (0.98,0.75,0.55,1), (0.95,0.55,0.45,1))
    speed = 900
    # skyline parallax
    for layer,(col,hgt,sp,seed) in enumerate([((0.55,0.40,0.50,1),380,0.25,1),((0.35,0.25,0.38,1),260,0.5,2)]):
        rng = np.random.default_rng(seed); ws = rng.integers(90,200,40); hs = rng.integers(80,hgt,40)
        x = -((lt*speed*sp) % 3000)
        for i in range(40):
            paper(ctx, lambda k,x=x,i=i: k.rectangle(x,780-hs[i],ws[i]-10,hs[i]+10), col, off=(5,6)); x += ws[i]
    # palms passing
    for i in range(6):
        px = (i*520 - lt*speed*0.8) % 3120 - 300
        paper(ctx, lambda k,px=px:(k.new_path(),k.rectangle(px,520,24,300)), (0.40,0.30,0.25,1))
        for a in range(5):
            ang=-2.6+a*0.55
            paper(ctx, lambda k,px=px,ang=ang:(k.new_path(),k.save(),k.translate(px+12,520),k.rotate(ang),k.scale(1,0.22),k.arc(100,0,100,0,2*math.pi),k.restore()), (0.10,0.32,0.28,1), off=(3,4))
    ctx.rectangle(0,800,W,280); ctx.set_source_rgba(0.30,0.30,0.36,1); ctx.fill()
    for i in range(10):
        x = (i*300 - lt*speed) % 3000 - 200
        ctx.rectangle(x,920,160,14); ctx.set_source_rgba(1,1,1,0.5); ctx.fill()
    # siren glow
    ph = (math.sin(lt*10)+1)/2
    g = cairo.RadialGradient(-100,700,10,-100,700,900); g.add_color_stop_rgba(0,*c('red',0.5*ph)); g.add_color_stop_rgba(1,0,0,0,0)
    ctx.set_source(g); ctx.paint()
    g = cairo.RadialGradient(-100,700,10,-100,700,900); g.add_color_stop_rgba(0,*c('blue',0.5*(1-ph))); g.add_color_stop_rgba(1,0,0,0,0)
    ctx.set_source(g); ctx.paint()
    you(ctx, 900, 900, 1.15, phase=lt*11, run=1.0, lean=0.12)
    # wanted stars, fill over 2.5..7.0
    n = 1 + int(min(4, max(0,(lt-2.5)/0.9)))
    paper(ctx, lambda k: rrect(k,1300,60,560,130,24), c('ink',0.85))
    for i in range(5):
        filled = i < n
        pop = back(prog(lt, 2.5+(i-1)*0.9, 2.5+(i-1)*0.9+0.3)) if i>0 else 1
        r = 44*(pop if filled else 1)
        star(ctx, 1360+i*110, 125, r, c('yellow'), empty=not filled)

# ---------- S7 Ozzie reveal 33.2-36.4, title 36.4-40 ----------
def oddsboard(ctx, x, y, label, value, a=1.0, flipt=0.0):
    paper(ctx, lambda k: rrect(k,x-380,y-120,760,240,24), c('ink',a), off=(8,10))
    text(ctx, label, x, y-70, 30, c('orange',a), font='DejaVu Sans Mono')
    cw = 74
    for i,ch in enumerate(value):
        cx = x - (len(value)*cw)/2 + i*cw + cw/2
        rrect(ctx, cx-32, y-30, 64, 100, 8); ctx.set_source_rgba(0.16,0.17,0.22,a); ctx.fill()
        ctx.rectangle(cx-32, y+19, 64, 2); ctx.set_source_rgba(0,0,0,a); ctx.fill()
        text(ctx, ch, cx, y+20, 70, c('cream',a), font='DejaVu Sans Mono')

def s7(ctx, t):
    lt = t-33.2
    bg(ctx, c('navy'), (0.05,0.07,0.14,1))
    # desk lamp pool
    g = cairo.RadialGradient(700,800,50,700,800,800); g.add_color_stop_rgba(0,1,0.85,0.6,0.25); g.add_color_stop_rgba(1,0,0,0,0)
    ctx.set_source(g); ctx.paint()
    secs = max(0, t-34.6)
    hh, mm, ss = 0, int(secs)//60, int(secs)%60
    oddsboard(ctx, 1360, 380, "SURVIVAL TIME", f"{hh:02d}:{mm:02d}:{ss:02d}")
    # desk
    paper(ctx, lambda k: k.rectangle(0,820,W,260), (0.30,0.20,0.16,1), off=(0,-10))
    up = back(prog(lt,0,0.5))
    blink = 1.0 if (1.6<lt<1.75) else 0.0
    ozzie(ctx, 640, 860 + (1-up)*500, 1.25, blink=blink, look=(0.6,0.1) if lt<1.2 else (0,0.2), wing=ease(prog(lt,1.1,1.4))*(1-ease(prog(lt,2.2,2.6))))
    a = ease(prog(lt,0.2,0.6))
    paper(ctx, lambda k: rrect(k,1060,700,600,110,18), c('hivis',a))
    text(ctx, "OZZIE  ·  RUNS THE ODDS", 1360, 755, 40, c('ink',a))

def title(ctx, t):
    lt = t-36.4
    ctx.set_source_rgba(*c('ink')); ctx.paint()
    # rotating siren beams
    for col,off in (('red',0),('blue',math.pi)):
        ang = lt*2.2+off
        ctx.save(); ctx.translate(W/2,1180); ctx.rotate(ang)
        ctx.move_to(0,0); ctx.line_to(-260,-1500); ctx.line_to(260,-1500); ctx.close_path()
        ctx.set_source_rgba(*c(col,0.22)); ctx.fill(); ctx.restore()
    a = back(prog(lt,0,0.5))
    ctx.save(); ctx.translate(W/2,H/2); ctx.scale(a,a)
    text_paper(ctx, "HOW LONG WOULD YOU SURVIVE", 0, -150, 88, c('cream'))
    text_paper(ctx, "A REAL", -330, 0, 120, c('cream'))
    for i in range(5): star(ctx, 0+i*120, 0, 52, c('yellow'))
    text_paper(ctx, "WANTED LEVEL?", 0, 160, 120, c('orange'))
    ctx.restore()

SCENES = [(0,8.6,s1),(8.6,14.0,s2),(14.0,19.0,s3),(19.0,22.2,s4),(22.2,26.0,s5),(26.0,33.2,s6),(33.2,36.4,s7),(36.4,40.0,title)]

def frame(t):
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H); ctx = cairo.Context(surf)
    for i,(a,b,f) in enumerate(SCENES):
        if a <= t < b:
            f(ctx, t)
            # quick paper-wipe transition into next scene
            if i+1 < len(SCENES) and t > b-0.25:
                p = ease((t-(b-0.25))/0.25)
                ctx.rectangle(W*(1-p),0,W*p+20,H); ctx.set_source_rgba(*c('ink')); ctx.fill()
            if i>0 and t < a+0.25:
                p = 1-ease((t-a)/0.25)
                ctx.rectangle(0,0,W*p,H); ctx.set_source_rgba(*c('ink')); ctx.fill()
            break
    vignette(ctx, 0.35); grain(ctx, 0.12)
    return surf

if __name__ == '__main__':
    mode = sys.argv[1]
    if mode == 'still':
        for ts in sys.argv[3:]:
            frame(float(ts)).write_to_png(f"{sys.argv[2]}/still_{ts}.png")
    else:
        out = sys.argv[2]; start=float(sys.argv[3]); end=float(sys.argv[4])
        p = subprocess.Popen(['ffmpeg','-loglevel','error','-y','-f','rawvideo','-pix_fmt','bgra','-s',f'{W}x{H}','-r',str(FPS),'-i','-',
                              '-c:v','libx264','-preset','medium','-crf','18','-pix_fmt','yuv420p',out], stdin=subprocess.PIPE)
        n0, n1 = int(start*FPS), int(end*FPS)
        for n in range(n0, n1):
            p.stdin.write(bytes(frame(n/FPS).get_data()))
        p.stdin.close(); p.wait()
