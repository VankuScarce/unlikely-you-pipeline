# Episode 2 v3 scenes (conveniences fading, the quiet, the mission, open ending).
# Executed inside ep02.py's namespace (exec) so it can use bword, push, kword, stamp, you, quad, etc.

def mouse_icon(ctx, x, y, s_=1.0, col=(0.85, 0.85, 0.88, 1), face=1, t=0.0):
    ctx.save(); ctx.translate(x, y); ctx.scale(face*s_, s_)
    ctx.move_to(-70, 10); ctx.curve_to(-140, 20, -170, -30, -200, -10); ctx.set_line_width(6); ctx.set_source_rgba(0.85, 0.6, 0.65, 1); ctx.stroke()
    paper(ctx, lambda k: (k.new_path(), k.save(), k.scale(1.0, 0.62), k.arc(0, 0, 80, 0, 2*math.pi), k.restore()), col, off=(4, 5))
    ctx.save(); ctx.translate(70, -10); ctx.scale(1.0, 0.8); ctx.arc(0, 0, 42, 0, 2*math.pi); ctx.restore(); ctx.set_source_rgba(*col); ctx.fill()
    for ex in (45, 80):
        ctx.arc(ex, -58, 22, 0, 2*math.pi); ctx.set_source_rgba(*col); ctx.fill()
        ctx.arc(ex, -58, 13, 0, 2*math.pi); ctx.set_source_rgba(0.95, 0.65, 0.70, 1); ctx.fill()
    ctx.arc(95, -18, 5, 0, 2*math.pi); ctx.set_source_rgba(0.08, 0.08, 0.1, 1); ctx.fill()
    ctx.arc(112, -4, 6, 0, 2*math.pi); ctx.set_source_rgba(0.9, 0.45, 0.5, 1); ctx.fill()
    ctx.restore()

def male_sign(ctx, x, y, r, col):
    ctx.arc(x, y, r, 0, 2*math.pi); ctx.set_line_width(r*0.28); ctx.set_source_rgba(*col); ctx.stroke()
    ctx.move_to(x+r*0.7, y-r*0.7); ctx.line_to(x+r*1.6, y-r*1.6); ctx.stroke()
    ctx.move_to(x+r*0.95, y-r*1.6); ctx.line_to(x+r*1.6, y-r*1.6); ctx.line_to(x+r*1.6, y-r*0.95); ctx.stroke()

def arrow(ctx, x0, y0, x1, y1, p, col, w=10):
    if p <= 0: return
    xe, ye = x0+(x1-x0)*p, y0+(y1-y0)*p
    ctx.move_to(x0, y0); ctx.line_to(xe, ye); ctx.set_line_width(w); ctx.set_source_rgba(*col); ctx.stroke()
    a = math.atan2(ye-y0, xe-x0)
    ctx.move_to(xe, ye); ctx.line_to(xe-28*math.cos(a-0.5), ye-28*math.sin(a-0.5)); ctx.line_to(xe-28*math.cos(a+0.5), ye-28*math.sin(a+0.5)); ctx.close_path(); ctx.fill()

def dewar(ctx, x, y, h=420, r=120, level=1.0, t=0.0, vapor=1.0):
    """Steel liquid-nitrogen tank, (x,y)=bottom centre."""
    paper(ctx, lambda k: rrect(k, x-r, y-h, 2*r, h, 30), (0.72, 0.75, 0.80, 1))
    ctx.rectangle(x-r+18, y-h+30, 22, h-60); ctx.set_source_rgba(1, 1, 1, 0.35); ctx.fill()
    rrect(ctx, x-r*0.55, y-h-40, r*1.1, 50, 14); ctx.set_source_rgba(0.45, 0.48, 0.55, 1); ctx.fill()
    for i in range(5):
        ph = (t*0.35 + i*0.2) % 1
        a = vapor*(1-ph)*0.35
        ctx.arc(x+math.sin(t*1.3+i)*25, y-h-60-ph*160, 26+ph*50, 0, 2*math.pi); ctx.set_source_rgba(0.92, 0.96, 1, a); ctx.fill()

def sc_scraps_named(ctx, s):
    if s.lt < s.at(0.24):
        ctx.set_source_rgb(0.06, 0.08, 0.15); ctx.paint()
        kinds = ['dog', 'cat', 'cow', 'dog', 'cat', 'dog', 'cow', 'cat']
        for row in range(3):
            for i in range(9):
                k = kinds[(i+row*3) % len(kinds)]
                x = ((i*260 + s.lt*(90+row*30)) % (W+400)) - 200
                quad(ctx, x, 560+row*190, k, 0.42, phase=s.T*6+i, run=0.5, sil=(0.30+0.08*row, 0.36+0.06*row, 0.52, 1))
        kword(ctx, "HUNDREDS OF MILLIONS", W/2, 220, 110, c('cream'), s.lt, s.at(0.0))
        bword(ctx, "DOGS · CATS · COWS", W/2, 360, 64, c('yellow'), s.lt, s.at(0.06))
        return
    sky(ctx, 'day'); ctx.save(); push(ctx, s, 1.0, 1.18, W/2+120, 760)
    skyline(ctx, 0, 820, 200, 520, (0.62, 0.70, 0.78, 1), lit=0, seed=33)
    ground(ctx, 820, (0.55, 0.62, 0.48, 1)); road(ctx, 900, 150)
    you(ctx, 760, 900, 0.85, t=s.T, face=1)
    look = s.lt > s.at(0.78)
    quad(ctx, 1060, 900, 'dog', 0.95, phase=s.T*9, run=0.0, face=-1)
    p = back(s.pr(0.3, 0.38))
    if p > 0:
        ctx.save(); ctx.translate(1180, 640); ctx.scale(p, p)
        ctx.move_to(-60, 60); ctx.line_to(-110, 110); ctx.set_line_width(4); ctx.set_source_rgba(*c('ink')); ctx.stroke()
        rrect(ctx, -110, -40, 220, 80, 40); ctx.set_source_rgba(*c('hivis')); ctx.fill()
        text(ctx, "SCRAPS", 0, 2, 40, c('ink')); ctx.restore()
    if look:
        a = ease(s.pr(0.78, 0.86))
        for i in range(3):
            hx, hy, r = 960-i*50, 560-i*40, 14+i*5
            ctx.move_to(hx, hy+r); ctx.curve_to(hx-2*r, hy-0.2*r, hx-r, hy-1.6*r, hx, hy-0.6*r); ctx.curve_to(hx+r, hy-1.6*r, hx+2*r, hy-0.2*r, hx, hy+r)
            ctx.set_source_rgba(*c('red', a)); ctx.fill()
    ctx.restore()
    if s.lt > s.at(0.3): bword(ctx, "YOU CALL HIM SCRAPS", W/2, 130, 74, c('cream'), s.lt, s.at(0.3))
    if s.lt > s.at(0.5): bword(ctx, "NOT A REPLACEMENT FOR 8 BILLION", W/2, 250, 56, c('grey'), s.lt, s.at(0.5))
    if s.lt > s.at(0.78): bword(ctx, "BUT HE STILL LOOKS AT YOU WHEN YOU TALK", W/2, H-100, 54, c('yellow'), s.lt, s.at(0.78))

def sc_phone_dead(ctx, s):
    ctx.set_source_rgb(0.07, 0.08, 0.13); ctx.paint()
    ctx.save(); push(ctx, s, 1.0, 1.08, sh=0.6)
    # cell tower
    tx, ty = 520, 940
    ctx.move_to(tx-120, ty); ctx.line_to(tx, ty-620); ctx.line_to(tx+120, ty); ctx.set_line_width(14); ctx.set_source_rgba(0.55, 0.58, 0.66, 1); ctx.stroke()
    for i in range(1, 6):
        yy = ty-i*110; ww = 120*(1-i*110/620)
        ctx.move_to(tx-ww, yy); ctx.line_to(tx+ww, yy); ctx.set_line_width(8); ctx.stroke()
    alive = 1-ease(s.pr(0.45, 0.6))
    for i in range(3):
        r = 80+i*70+((s.T*120) % 70)
        ctx.arc(tx, ty-620, r, -2.4, -0.74); ctx.set_line_width(10); ctx.set_source_rgba(*c('teal', 0.8*alive*(1-i*0.25))); ctx.stroke()
    # battery + generator readouts
    bat = 1-ease(s.pr(0.12, 0.35))
    rrect(ctx, 720, 260, 220, 100, 14); ctx.set_line_width(8); ctx.set_source_rgba(*c('cream')); ctx.stroke()
    ctx.rectangle(940, 290, 16, 40); ctx.fill()
    ctx.rectangle(732, 272, 196*bat, 76); ctx.set_source_rgba(*(c('teal') if bat > 0.3 else c('red'))); ctx.fill()
    ctx.restore()
    bword(ctx, "BACKUP BATTERY: HOURS", 1040, 180, 46, c('cream'), s.lt, s.at(0.12), anchor='l')
    if s.lt > s.at(0.33): bword(ctx, "GENERATORS: DAYS", 1040, 270, 46, c('cream'), s.lt, s.at(0.33), anchor='l')
    kword(ctx, "THE INTERNET", 1060, 560, 80, c('grey'), s.lt, s.at(0.0))
    if s.lt > s.at(0.55): stamp(ctx, "GONE", 1060, 680, 90, c('red'), s.lt, s.at(0.55))
    # phone becomes a flashlight
    if s.lt > s.at(0.62):
        p = ease(s.pr(0.62, 0.72))
        ctx.save(); ctx.translate(1620, 860)
        ctx.move_to(-40, -110); ctx.line_to(-300, -900); ctx.line_to(300, -900); ctx.line_to(40, -110); ctx.close_path()
        g = cairo.LinearGradient(0, -110, 0, -900); g.add_color_stop_rgba(0, 1, 0.98, 0.85, 0.55*p); g.add_color_stop_rgba(1, 1, 0.98, 0.85, 0)
        ctx.set_source(g); ctx.fill()
        ctx.rotate(math.pi); phone(ctx, 0, 0, 0.3); ctx.restore()
        text(ctx, "NO SERVICE", 1620, 870, 22, c('red', p))
        bword(ctx, "A VERY NICE FLASHLIGHT", 1520, H-90, 58, c('yellow'), s.lt, s.at(0.78))

def sc_ice_cream(ctx, s):
    ctx.set_source_rgb(0.10, 0.12, 0.16); ctx.paint()
    ctx.save(); push(ctx, s, 1.12, 1.0, W/2, 700)
    # freezer case
    paper(ctx, lambda k: rrect(k, 120, 380, 980, 420, 20), (0.30, 0.50, 0.66, 1))
    rrect(ctx, 150, 410, 920, 200, 12); ctx.set_source_rgba(0.55, 0.78, 0.92, 0.55); ctx.fill()
    for i in range(10):
        ph = (s.T*0.7 + i*0.13) % 1
        ctx.arc(180+i*92, 800+ph*180, 9, 0, 2*math.pi); ctx.set_source_rgba(0.6, 0.85, 1, 0.8*(1-ph)); ctx.fill()
    ground(ctx, 880, (0.20, 0.22, 0.26, 1))
    # you on the floor with a giant tub
    for i in range(6):
        rrect(ctx, 190+i*145, 470, 110, 110, 10); ctx.set_source_rgba(*(c('red'), c('cream'), c('teal'), c('orange'), c('cream'), c('red'))[i]); ctx.fill()
    text(ctx, "FREEZER: OFF", 610, 700, 40, c('cream'))
    paper(ctx, lambda k: rrect(k, 1480, 760, 260, 160, 12), (0.55, 0.40, 0.28, 1))
    paper(ctx, lambda k: (k.new_path(), k.move_to(1520, 610), k.line_to(1700, 610), k.line_to(1685, 760), k.line_to(1535, 760), k.close_path()), (0.97, 0.92, 0.85, 1))
    ctx.rectangle(1528, 660, 164, 44); ctx.set_source_rgba(*c('red')); ctx.fill()
    text(ctx, "VANILLA", 1610, 684, 26, c('cream'))
    ctx.save(); ctx.translate(1610, 610); ctx.scale(1.0, 0.3); ctx.arc(0, 0, 90, 0, 2*math.pi); ctx.restore(); ctx.set_source_rgba(0.99, 0.96, 0.86, 1); ctx.fill()
    you(ctx, 1340, 920, 0.9, reach=0.45+0.2*math.sin(s.T*5), t=s.T)
    ctx.restore()
    kword(ctx, "SMALL WIN", W/2, 120, 90, c('hivis'), s.lt, s.at(0.0))
    if s.lt > s.at(0.22): bword(ctx, "DAY 2: ICE CREAM FOR BREAKFAST", W/2, 250, 58, c('cream'), s.lt, s.at(0.22))
    if s.lt > s.at(0.55): stamp(ctx, "NOBODY CAN STOP YOU", 1480, 420, 60, c('yellow'), s.lt, s.at(0.55))
    if s.lt > s.at(0.74): bword(ctx, "BEST MEAL FOR THE NEXT 100 YEARS?", W/2, H-90, 52, c('yellow'), s.lt, s.at(0.74))

def sc_cold_shower(ctx, s):
    split = ease(s.pr(0.5, 0.6))
    ctx.set_source_rgb(0.86, 0.88, 0.90); ctx.paint()
    # left: shower with steam that fades as gas pressure drops
    press = 1-ease(s.pr(0.2, 0.5))
    ctx.save(); ctx.translate(-split*W*0.5, 0)
    paper(ctx, lambda k: rrect(k, 200, 160, 760, 820, 24), (0.80, 0.90, 0.94, 1))
    ctx.move_to(580, 160); ctx.line_to(580, 300); ctx.line_to(680, 300); ctx.set_line_width(16); ctx.set_source_rgba(0.6, 0.62, 0.66, 1); ctx.stroke()
    paper(ctx, lambda k: rrect(k, 620, 290, 140, 40, 18), (0.65, 0.67, 0.72, 1))
    for i in range(22):
        ph = (s.T*1.4 + i*0.07) % 1
        ctx.move_to(635+i*5.5, 330+ph*560); ctx.line_to(632+i*5.5, 360+ph*560); ctx.set_line_width(4); ctx.set_source_rgba(0.4, 0.65, 0.85, 0.7*max(0.25, press)); ctx.stroke()
    for i in range(6):
        ph = (s.T*0.3 + i*0.17) % 1
        ctx.arc(690+math.sin(i*2+s.T)*120, 820-ph*600, 60+ph*80, 0, 2*math.pi); ctx.set_source_rgba(1, 1, 1, 0.35*press*(1-ph)); ctx.fill()
    pgauge(ctx, 1500, 520, 170, 100*press)
    text(ctx, "GAS PRESSURE", 1500, 760, 44, c('ink'))
    ctx.restore()
    # right: bucket + camping stove
    if split > 0:
        ctx.save(); ctx.translate(W*(1-split), 0)
        ctx.set_source_rgb(0.20, 0.18, 0.20); ctx.rectangle(0, 0, W, H); ctx.fill()
        ground(ctx, 880, (0.30, 0.26, 0.24, 1))
        rrect(ctx, 520, 760, 320, 120, 16); ctx.set_source_rgba(0.35, 0.38, 0.44, 1); ctx.fill()
        flame(ctx, 680, 760, 0.45, s.T, 2)
        paper(ctx, lambda k: (k.new_path(), k.move_to(560, 560), k.line_to(800, 560), k.line_to(770, 740), k.line_to(590, 740), k.close_path()), (0.55, 0.58, 0.62, 1))
        for i in range(4):
            ph = (s.T*0.5 + i*0.25) % 1
            ctx.arc(680+math.sin(s.T*2+i)*30, 540-ph*240, 22+ph*40, 0, 2*math.pi); ctx.set_source_rgba(1, 1, 1, 0.4*(1-ph)); ctx.fill()
        paper(ctx, lambda k: (k.new_path(), k.move_to(1080, 520), k.line_to(1420, 520), k.line_to(1380, 880), k.line_to(1120, 880), k.close_path()), (0.25, 0.50, 0.75, 1))
        ctx.move_to(1080, 520); ctx.curve_to(1120, 360, 1380, 360, 1420, 520); ctx.set_line_width(8); ctx.set_source_rgba(0.5, 0.5, 0.55, 1); ctx.stroke()
        ctx.restore()
    kword(ctx, "THE COMFORTS GO ONE BY ONE", W/2, 90, 64, c('ink') if split < 0.5 else c('cream'), s.lt, s.at(0.0))
    if s.lt > s.at(0.15) and split < 0.5: bword(ctx, "HOT SHOWERS: WHILE THE GAS LASTS", W/2, 200, 52, c('cream'), s.lt, s.at(0.15))
    if s.lt > s.at(0.62): bword(ctx, "THEN: A BUCKET + A CAMPING STOVE", W/2, H-100, 56, c('yellow'), s.lt, s.at(0.62))

def sc_siphon(ctx, s):
    sky(ctx, 'gray'); ctx.save(); push(ctx, s, 1.0, 1.1, W/2, 700)
    ground(ctx, 700, (0.42, 0.42, 0.44, 1))
    # canopy + pump
    ctx.rectangle(150, 180, 1000, 70); ctx.set_source_rgba(*c('red')); ctx.fill()
    ctx.rectangle(200, 250, 40, 450); ctx.rectangle(1060, 250, 40, 450); ctx.set_source_rgba(0.85, 0.85, 0.86, 1); ctx.fill()
    paper(ctx, lambda k: rrect(k, 520, 420, 200, 280, 16), (0.94, 0.94, 0.92, 1))
    rrect(ctx, 545, 450, 150, 70, 8); ctx.set_source_rgba(0.08, 0.08, 0.10, 1); ctx.fill()
    text(ctx, "NO POWER", 620, 485, 22, c('red', 0.6+0.4*(int(s.T*3) % 2)))
    # underground tank cutaway
    ctx.rectangle(0, 760, W, 320); ctx.set_source_rgba(0.36, 0.28, 0.22, 1); ctx.fill()
    rrect(ctx, 300, 820, 700, 200, 100); ctx.set_source_rgba(0.25, 0.27, 0.30, 1); ctx.fill()
    ctx.save(); rrect(ctx, 300, 820, 700, 200, 100); ctx.clip(); ctx.rectangle(300, 870, 700, 150); ctx.set_source_rgba(0.95, 0.70, 0.20, 0.9); ctx.fill(); ctx.restore()
    text(ctx, "THOUSANDS OF LITRES", 650, 945, 34, c('ink'))
    # car + you siphoning
    car(ctx, 1500, 700, 1.0, beam=False)
    if s.lt > s.at(0.45):
        p = ease(s.pr(0.45, 0.6))
        you(ctx, 1260, 700, 0.6, lean=0.5, reach=0.6, t=s.T)
        ctx.move_to(1330, 560); ctx.curve_to(1380, 640, 1420, 600, 1420+30*p, 640+30*p); ctx.set_line_width(8); ctx.set_source_rgba(0.3, 0.75, 0.45, 1); ctx.stroke()
        paper(ctx, lambda k: rrect(k, 1180, 600, 90, 100, 10), c('red'))
    ctx.restore()
    bword(ctx, "THE FUEL IS STILL THERE", W/2, 90, 64, c('cream'), s.lt, s.at(0.0))
    if s.lt > s.at(0.3): bword(ctx, "THE PUMPS NEED POWER", 640, 360, 50, c('red'), s.lt, s.at(0.3))
    if s.lt > s.at(0.55): bword(ctx, "NEW SKILL: SIPHONING", 1450, 360, 54, c('yellow'), s.lt, s.at(0.55))
    if s.lt > s.at(0.82): stamp(ctx, "TASTES AS BAD AS YOU THINK", 860, 560, 58, c('hivis'), s.lt, s.at(0.82))

def sc_movie_night(ctx, s):
    ctx.set_source_rgb(0.04, 0.05, 0.09); ctx.paint()
    ctx.save(); push(ctx, s, 1.1, 1.0, W/2, 600)
    # screen (sheet on wall) with flickering movie
    boom = (math.sin(s.T*2.1) > 0.6)
    scr = (0.95, 0.55, 0.20) if boom else (0.40, 0.55, 0.85)
    ctx.save(); rrect(ctx, 520, 180, 880, 440, 10); ctx.clip()
    ctx.set_source_rgba(*scr, 0.9); ctx.paint()
    if boom:
        for i in range(5):
            ctx.arc(960+math.cos(i*1.3)*160, 420+math.sin(i*1.7)*90, 90+20*i, 0, 2*math.pi); ctx.set_source_rgba(1, 0.85-0.1*i, 0.3, 0.35); ctx.fill()
    else:
        skyline(ctx, s.lt*40, 620, 80, 260, (0.15, 0.20, 0.40, 1), lit=0.4, seed=8, span=W*2)
    ctx.restore()
    ctx.move_to(1720, 700); ctx.line_to(1400, 180); ctx.line_to(1400, 620); ctx.close_path(); ctx.set_source_rgba(1, 1, 0.9, 0.08); ctx.fill()
    paper(ctx, lambda k: rrect(k, 1660, 680, 140, 70, 10), (0.25, 0.25, 0.28, 1))
    ground(ctx, 960, (0.08, 0.08, 0.12, 1))
    sil = (0.17, 0.16, 0.24, 1)
    # viewers from behind: you (head + shoulders) and Scraps (head + ears), lit by the screen
    rrect(ctx, 700, 840, 260, 200, 90); ctx.set_source_rgba(*sil); ctx.fill()
    ctx.arc(830, 790, 62, 0, 2*math.pi); ctx.fill()
    hide = ease(s.pr(0.82, 0.9)); dy = 120*hide
    ctx.arc(1110, 870+dy, 48, 0, 2*math.pi); ctx.fill()
    for sx in (-1, 1):
        ctx.save(); ctx.translate(1110+sx*44, 870+dy); ctx.rotate(sx*(0.35+0.6*hide)); ctx.scale(0.45, 1.0); ctx.arc(0, 30, 40, 0, 2*math.pi); ctx.restore(); ctx.fill()
    rrect(ctx, 560, 930, 820, 150, 40); ctx.set_source_rgba(0.36, 0.24, 0.20, 1); ctx.fill()
    ctx.rectangle(580, 930, 780, 8); ctx.set_source_rgba(*scr, 0.35); ctx.fill()
    ctx.restore()
    kword(ctx, "SOLAR MOVIE NIGHT", W/2, 90, 74, c('yellow'), s.lt, s.at(0.05))
    if s.lt > s.at(0.45): bword(ctx, "2 HOURS OF A NORMAL FRIDAY", W/2, 700, 54, c('cream'), s.lt, s.at(0.45))
    if s.lt > s.at(0.82): stamp(ctx, "SCRAPS HATES EXPLOSIONS", W/2, H-90, 60, c('hivis'), s.lt, s.at(0.82))

def sc_boredom_words(ctx, s):
    ctx.set_source_rgb(0.42, 0.43, 0.46); ctx.paint()
    kword(ctx, "THE PART SURVIVAL GUIDES", W/2, 200, 70, c('cream'), s.lt, s.at(0.0))
    kword(ctx, "NEVER MENTION", W/2, 290, 70, c('cream'), s.lt, s.at(0.12))
    you(ctx, 300, 1040, 0.6, lean=0.12, t=s.T); quad(ctx, 470, 1040, 'dog', 0.4, phase=0, run=0, face=-1)
    dang = 1-ease(s.pr(0.35, 0.6))
    rrect(ctx, 560, 430, 800, 60, 30); ctx.set_source_rgba(0.3, 0.3, 0.34, 1); ctx.fill()
    rrect(ctx, 560, 430, max(60, 800*dang), 60, 30); ctx.set_source_rgba(*c('red')); ctx.fill()
    text(ctx, "DANGER", 960, 530, 40, c('cream'))
    if s.lt > s.at(0.82):
        p = ease(s.pr(0.82, 1.0)); z = 1+0.08*p
        ctx.save(); ctx.translate(W/2, 790); ctx.scale(z, z); kword(ctx, "BOREDOM.", 0, 0, 220, c('ink'), s.lt, s.at(0.82)); ctx.restore()

def sc_same_day(ctx, s):
    if s.lt < s.at(0.42):
        ctx.set_source_rgb(0.90, 0.88, 0.84); ctx.paint()
        flip = int(s.lt*3)
        for i in range(3):
            off = (2-i)*14
            paper(ctx, lambda k: rrect(k, 660+off, 220+off, 600, 560, 20), (0.98, 0.97, 0.95, 1))
        ctx.rectangle(674, 248, 600, 110); ctx.set_source_rgba(*c('red')); ctx.fill()
        text(ctx, "DAY %d" % (100+flip), 974, 303, 60, c('cream'))
        text(ctx, "SAME", 974, 500, 120, c('ink')); text(ctx, "DAY", 974, 640, 120, c('ink'))
        for i, (w_, f) in enumerate((("NO NEWS", 0.08), ("NO WORK", 0.15), ("NO GROUP CHAT", 0.22), ("NOBODY TO TELL", 0.3))):
            bword(ctx, w_, 330 if i % 2 == 0 else 1590, 400+(i//2)*200, 50, c('cream'), s.lt, s.at(f))
        return
    # Antarctic station
    sky(ctx, 'night'); stars(ctx, 160, alpha=0.7)
    for i in range(4):
        ctx.move_to(0, 300+i*30); ctx.curve_to(600, 160+i*40+40*math.sin(s.T+i), 1300, 380+i*30, W, 220+i*30)
        ctx.set_line_width(40); ctx.set_source_rgba(0.3, 0.95, 0.6, 0.10); ctx.stroke()
    ground(ctx, 760, (0.90, 0.93, 0.97, 1))
    paper(ctx, lambda k: rrect(k, 760, 600, 420, 180, 16), (0.95, 0.45, 0.20, 1))
    for i in range(3): ctx.rectangle(800+i*120, 640, 60, 40); ctx.set_source_rgba(1, 0.9, 0.5, 0.9); ctx.fill()
    bword(ctx, "ANTARCTIC WINTER CREWS", W/2, 120, 64, c('cream'), s.lt, s.at(0.45))
    if s.lt > s.at(0.66): bword(ctx, "TIME BLURS", 480, 880, 56, c('cream'), s.lt, s.at(0.66), box=(0.1, 0.15, 0.3, 0.85))
    if s.lt > s.at(0.74): bword(ctx, "SLEEP DRIFTS", 1440, 880, 56, c('cream'), s.lt, s.at(0.74), box=(0.1, 0.15, 0.3, 0.85))
    if s.lt > s.at(0.83): bword(ctx, "SMALL PROBLEMS FEEL HUGE", W/2, 1000, 56, c('yellow'), s.lt, s.at(0.83), box=(0.1, 0.15, 0.3, 0.85))

def sc_routine(ctx, s):
    sky(ctx, 'dawn'); ctx.save(); push(ctx, s, 1.0, 1.08)
    ground(ctx, 860, (0.55, 0.60, 0.45, 1))
    house(ctx, 1320, 880, 520, 300, body=(0.88, 0.80, 0.68, 1), solar=True)
    you(ctx, 1000, 900, 0.72, t=s.T, face=1)
    quad(ctx, 1210, 900, 'dog', 0.6, phase=s.T*8, run=0, face=-1)
    if s.lt > s.at(0.7):
        for i in range(3):
            a = ease(prog(s.lt, s.at(0.7)+i*0.35, s.at(0.7)+i*0.35+0.3))
            paper(ctx, lambda k: rrect(k, 1060+i*20, 520-i*80, 150, 60, 30), (1, 1, 1, a))
            text(ctx, "...", 1135+i*20, 545-i*80, 40, c('ink', a))
    ctx.restore()
    # checklist
    paper(ctx, lambda k: rrect(k, 120, 200, 760, 700, 24), (0.98, 0.96, 0.90, 1))
    text(ctx, "DAILY ROUTINE", 500, 270, 54, c('ink'))
    items = [("WAKE UP", 0.30), ("FEED SCRAPS", 0.38), ("CHECK THE PANELS", 0.46), ("READ ONE BOOK", 0.55)]
    for i, (w_, f) in enumerate(items):
        y = 380+i*120
        rrect(ctx, 170, y-30, 60, 60, 10); ctx.set_line_width(6); ctx.set_source_rgba(*c('ink')); ctx.stroke()
        text(ctx, w_, 260, y, 46, c('ink'), anchor='l')
        p = ease(prog(s.lt, s.at(f), s.at(f)+0.25))
        if p > 0:
            ctx.move_to(178, y); ctx.line_to(178+20*min(1, p*2), y+20*min(1, p*2))
            if p > 0.5: ctx.line_to(198+40*(p-0.5)*2, y+20-60*(p-0.5)*2)
            ctx.set_line_width(10); ctx.set_source_rgba(*c('teal')); ctx.stroke()
    bword(ctx, "A ROUTINE + A REASON TO GET UP", W/2+200, 110, 54, c('ink'), s.lt, s.at(0.02), box=(0.98, 0.96, 0.90, 0.9))
    if s.lt > s.at(0.88): stamp(ctx, "GOOD LISTENER", 1450, 700, 56, c('hivis'), s.lt, s.at(0.88))

def sc_porch_question(ctx, s):
    sc_porch_dog(ctx, s)
    if s.lt > s.at(0.05): bword(ctx, "A ROUTINE ISN'T A REASON", W/2, 120, 64, c('cream'), s.lt, s.at(0.05))
    if s.lt > s.at(0.7):
        ctx.rectangle(0, 0, W, H); ctx.set_source_rgba(0.02, 0.03, 0.08, 0.45*ease(s.pr(0.7, 0.8))); ctx.fill()
        kword(ctx, "WHAT IS ALL OF THIS FOR?", W/2, H/2, 110, c('hivis'), s.lt, s.at(0.72))

def sc_mission_decide(ctx, s):
    sky(ctx, 'dawn')
    ctx.save(); ctx.translate(W/2, 820); ctx.rotate(s.lt*0.15)
    for i in range(18):
        ctx.move_to(0, 0); ctx.arc(0, 0, 1800, i*math.pi/9, i*math.pi/9+math.pi/18); ctx.close_path()
    ctx.set_source_rgba(1, 1, 1, 0.18); ctx.fill(); ctx.restore()
    skyline(ctx, 0, 860, 180, 460, (0.62, 0.55, 0.60, 1), lit=0, seed=12)
    ctx.move_to(-50, H); ctx.curve_to(500, 760, 1400, 760, W+50, H); ctx.close_path(); ctx.set_source_rgba(0.25, 0.40, 0.30, 1); ctx.fill()
    you(ctx, 900, 830, 0.7, t=s.T); quad(ctx, 1080, 832, 'dog', 0.42, phase=0, run=0)
    kword(ctx, "NOT JUST SURVIVE.", W/2, 230, 100, c('ink'), s.lt, s.at(0.2))
    kword(ctx, "BRING PEOPLE BACK.", W/2, 380, 120, c('red'), s.lt, s.at(0.55))

def sc_one_man(ctx, s):
    ctx.set_source_rgb(0.05, 0.05, 0.08); ctx.paint()
    g = cairo.RadialGradient(W/2, 700, 10, W/2, 700, 520); g.add_color_stop_rgba(0, 1, 0.95, 0.8, 0.35); g.add_color_stop_rgba(1, 1, 0.95, 0.8, 0)
    ctx.set_source(g); ctx.paint()
    ctx.move_to(W/2-120, 0); ctx.line_to(W/2+120, 0); ctx.line_to(W/2+420, 980); ctx.line_to(W/2-420, 980); ctx.close_path(); ctx.set_source_rgba(1, 0.95, 0.8, 0.07); ctx.fill()
    you(ctx, W/2, 960, 0.95, t=s.T)
    rrect(ctx, 80, 80, 420, 110, 20); ctx.set_source_rgba(0.12, 0.12, 0.18, 1); ctx.fill()
    text(ctx, "HUMANS LEFT: 1", 290, 135, 48, c('cream'))
    if s.lt > s.at(0.15): bword(ctx, "NOBODY TO START A FAMILY WITH", W/2, 200, 56, c('cream'), s.lt, s.at(0.15))
    if s.lt > s.at(0.5): stamp(ctx, "NATURE SAYS NO", 460, 620, 70, c('red'), s.lt, s.at(0.5))
    if s.lt > s.at(0.8): stamp(ctx, "ASK SCIENCE", 1460, 620, 76, c('teal'), s.lt, s.at(0.8), rot=0.1)

def sc_library_lab(ctx, s):
    pan = 1300*ease(s.pr(0.1, 0.75))
    ctx.set_source_rgb(0.30, 0.20, 0.16); ctx.paint()
    ctx.save(); ctx.translate(-pan, 0)
    rng = np.random.default_rng(4)
    for sh in range(4):
        y = 200+sh*200; ctx.rectangle(0, y+150, 1900, 20); ctx.set_source_rgba(0.45, 0.30, 0.20, 1); ctx.fill()
        x = 40
        while x < 1850:
            w = rng.uniform(26, 50); h = rng.uniform(100, 145)
            ctx.rectangle(x, y+150-h, w, h); ctx.set_source_rgba(*[(0.70, 0.25, 0.25), (0.25, 0.40, 0.60), (0.85, 0.70, 0.35), (0.30, 0.55, 0.40), (0.55, 0.50, 0.65)][int(rng.integers(0, 5))], 1); ctx.fill()
            x += w+4
    # lab
    ctx.rectangle(1900, 0, 2000, H); ctx.set_source_rgba(0.88, 0.92, 0.94, 1); ctx.fill()
    ctx.rectangle(2000, 700, 1400, 60); ctx.set_source_rgba(0.40, 0.45, 0.50, 1); ctx.fill()
    for i in range(4):
        bx = 2100+i*330
        cols = [(0.3, 0.7, 0.9), (0.9, 0.5, 0.6), (0.5, 0.85, 0.5), (0.95, 0.8, 0.3)]
        ctx.move_to(bx-50, 700); ctx.line_to(bx-20, 560); ctx.line_to(bx-20, 480); ctx.line_to(bx+20, 480); ctx.line_to(bx+20, 560); ctx.line_to(bx+50, 700); ctx.close_path()
        ctx.set_source_rgba(0.85, 0.92, 0.96, 0.9); ctx.fill_preserve(); ctx.set_line_width(5); ctx.set_source_rgba(0.4, 0.45, 0.5, 1); ctx.stroke()
        ctx.move_to(bx-42, 690); ctx.line_to(bx-28, 620); ctx.line_to(bx+28, 620); ctx.line_to(bx+42, 690); ctx.close_path(); ctx.set_source_rgba(*cols[i], 0.9); ctx.fill()
    paper(ctx, lambda k: rrect(k, 3420, 380, 300, 320, 20), (0.80, 0.82, 0.86, 1))
    rrect(ctx, 3450, 410, 240, 180, 12); ctx.set_source_rgba(0.55, 0.75, 0.85, 0.8); ctx.fill()
    text(ctx, "INCUBATOR", 3570, 650, 30, c('ink'))
    ctx.restore()
    you(ctx, 760, 1000, 0.9, phase=s.T*6, run=0.5, t=s.T)
    for i, (w_, f, col) in enumerate((("LIBRARIES: OPEN", 0.0, 'cream'), ("LABS: EMPTY", 0.2, 'cream'), ("SOLAR POWER", 0.38, 'yellow'), ("ALL THE TIME IN THE WORLD", 0.52, 'hivis'))):
        if s.lt > s.at(f): bword(ctx, w_, 520 + (i % 2)*880, 170 + (i // 2)*110, 52, c(col), s.lt, s.at(f))
    if s.lt > s.at(0.82): bword(ctx, "HERE'S WHAT YOU FIND", W/2, H-110, 64, c('yellow'), s.lt, s.at(0.82))

def sc_two_dads(ctx, s):
    ctx.set_source_rgb(0.95, 0.94, 0.90); ctx.paint()
    if s.lt < s.at(0.5):
        text(ctx, "2023 · JAPAN", W/2, 90, 58, c('red'))
        mouse_icon(ctx, 260, 330, 0.9, face=1); male_sign(ctx, 260, 470, 30, c('blue'))
        # skin cell -> stem cell -> egg
        steps = [(700, "SKIN CELL", (0.95, 0.75, 0.65)), (1100, "STEM CELL", (0.65, 0.85, 0.80)), (1500, "EGG", (1.0, 0.88, 0.55))]
        for i, (x, lab, col) in enumerate(steps):
            f = 0.06+i*0.08
            p = back(s.pr(f, f+0.05))
            if p > 0:
                ctx.save(); ctx.translate(x, 330); ctx.scale(p, p)
                paper(ctx, lambda k: (k.new_path(), k.arc(0, 0, 90 if i < 2 else 110, 0, 2*math.pi)), (*col, 1))
                ctx.arc(0, 0, 30, 0, 2*math.pi); ctx.set_source_rgba(*(c('slate') if i < 2 else (0.9, 0.6, 0.2, 1))); ctx.fill()
                text(ctx, lab, 0, 160, 38, c('ink')); ctx.restore()
            arrow(ctx, x-300, 330, x-130, 330, ease(s.pr(f-0.03, f)), c('ink'), 8)
        if s.lt > s.at(0.3):
            arrow(ctx, 1440, 520, 1060, 700, ease(s.pr(0.3, 0.36)), c('ink'), 8)
            mouse_icon(ctx, 400, 760, 0.6, face=1); male_sign(ctx, 400, 870, 22, c('blue'))
            arrow(ctx, 560, 760, 780, 760, ease(s.pr(0.3, 0.36)), c('ink'), 8)
            p = back(s.pr(0.36, 0.42))
            if p > 0:
                ctx.save(); ctx.translate(960, 760); ctx.scale(p, p); mouse_icon(ctx, 0, 0, 0.5, col=(0.98, 0.90, 0.88, 1)); ctx.restore()
                bword(ctx, "BABY MICE WITH TWO FATHERS", 1400, 760, 50, c('cream'), s.lt, s.at(0.4))
        return
    ctx.set_source_rgb(0.12, 0.14, 0.20); ctx.paint()
    text(ctx, "2025 · CHINA", W/2, 90, 58, c('hivis'))
    grow = ease(s.pr(0.55, 0.75))
    for i in range(8):
        x = 260+i*200; alive = i in (2, 5)
        sz = 0.35+(0.5*grow if alive else 0.0)
        a = 1.0 if alive or s.lt < s.at(0.75) else 0.25
        mouse_icon(ctx, x, 560, sz, col=(0.9, 0.9, 0.92, a))
    if s.lt > s.at(0.55): bword(ctx, "GREW UP INTO ADULTS", W/2, 250, 60, c('cream'), s.lt, s.at(0.55))
    if s.lt > s.at(0.78): stamp(ctx, "VERY FEW MADE IT", 640, 860, 64, c('red'), s.lt, s.at(0.78))
    if s.lt > s.at(0.9): stamp(ctx, "BUT IT WORKED", 1320, 860, 70, c('teal'), s.lt, s.at(0.9), rot=0.08)

def sc_embryo_freezer(ctx, s):
    ctx.set_source_rgb(0.86, 0.90, 0.93); ctx.paint()
    z = 1.0 + 2.2*ease(s.pr(0.45, 0.58))
    ctx.save(); ctx.translate(960, 600); ctx.scale(z, z); ctx.translate(-960, -600)
    ground(ctx, 900, (0.70, 0.74, 0.78, 1))
    for i in range(5): dewar(ctx, 280+i*340, 900, 380, 110, t=s.T+i, vapor=0.8)
    ctx.restore()
    if s.lt > s.at(0.52):
        a = ease(s.pr(0.52, 0.6))
        ctx.rectangle(0, 0, W, H); ctx.set_source_rgba(0.05, 0.08, 0.16, 0.85*a); ctx.fill()
        r = 80+6*math.sin(s.T*3)
        g = cairo.RadialGradient(W/2, H/2+40, 5, W/2, H/2+40, r*2.2); g.add_color_stop_rgba(0, 0.8, 0.95, 1, a); g.add_color_stop_rgba(1, 0.8, 0.95, 1, 0)
        ctx.set_source(g); ctx.arc(W/2, H/2+40, r*2.2, 0, 2*math.pi); ctx.fill()
        for i in range(8):
            an = i*math.pi/4; ctx.arc(W/2+28*math.cos(an), H/2+40+28*math.sin(an), 24, 0, 2*math.pi); ctx.set_source_rgba(0.9, 0.97, 1, 0.8*a); ctx.fill()
        if s.lt > s.at(0.55): bword(ctx, "A TINY FUTURE PERSON", W/2, 200, 64, c('cream'), s.lt, s.at(0.55))
        if s.lt > s.at(0.68): bword(ctx, "PARENTS: GONE", W/2, 860, 56, c('grey'), s.lt, s.at(0.68))
        if s.lt > s.at(0.8): stamp(ctx, "GENETIC VARIETY", W/2, 980, 64, c('hivis'), s.lt, s.at(0.8))
        return
    kword(ctx, "FROZEN EMBRYOS", W/2, 110, 90, c('ink'), s.lt, s.at(0.0))
    if s.lt > s.at(0.2):
        n = int(1000000*ease(s.pr(0.2, 0.38)))
        bword(ctx, f"{n:,}+" if n >= 1000000 else f"{n:,}", W/2, 260, 80, c('hivis'), s.lt, s.at(0.2))
        if s.lt > s.at(0.3): text(ctx, "IN THE US ALONE (ESTIMATE)", W/2, 360, 40, c('ink'))

def sc_nitrogen(ctx, s):
    ctx.set_source_rgb(0.10, 0.12, 0.18); ctx.paint()
    lvl = 1-0.85*ease(s.pr(0.15, 0.95))
    dewar(ctx, 640, 960, 620, 180, t=s.T, vapor=1.0)
    rrect(ctx, 1080, 260, 120, 620, 20); ctx.set_source_rgba(0.2, 0.22, 0.3, 1); ctx.fill()
    col = c('teal') if lvl > 0.45 else (c('orange') if lvl > 0.25 else c('red'))
    rrect(ctx, 1092, 272+596*(1-lvl), 96, 596*lvl, 14); ctx.set_source_rgba(*col); ctx.fill()
    text(ctx, f"{int(lvl*100)}%", 1140, 920, 50, c('cream'))
    kword(ctx, "LIQUID NITROGEN", 1400, 150, 70, c('cream'), s.lt, s.at(0.0), anchor='c')
    if s.lt > s.at(0.35): bword(ctx, "NOBODY TOPS IT UP", 1560, 460, 54, c('cream'), s.lt, s.at(0.35))
    if s.lt > s.at(0.55): bword(ctx, "IT SLOWLY BOILS AWAY", 1560, 580, 54, c('grey'), s.lt, s.at(0.55))
    if s.lt > s.at(0.82): stamp(ctx, "DEADLINE", 1560, 780, 90, c('red'), s.lt, s.at(0.82))

def sc_womb(ctx, s):
    if s.lt < s.at(0.17):
        ctx.set_source_rgb(0.92, 0.80, 0.78); ctx.paint()
        kword(ctx, "THE BIGGEST PROBLEM:", W/2, 380, 80, c('ink'), s.lt, s.at(0.0))
        kword(ctx, "A BABY NEEDS A WOMB", W/2, 560, 120, c('red'), s.lt, s.at(0.06))
        return
    if s.lt < s.at(0.5):
        ctx.set_source_rgb(0.90, 0.94, 0.96); ctx.paint()
        text(ctx, "2017 · PHILADELPHIA", W/2, 90, 56, c('red'))
        cx, cy = W/2, 560
        ctx.save(); ctx.translate(cx, cy)
        paper(ctx, lambda k: (k.new_path(), k.save(), k.scale(1.35, 1.0), k.arc(0, 0, 300, 0, 2*math.pi), k.restore()), (0.70, 0.85, 0.95, 0.75))
        for i in range(10):
            ph = (s.T*0.25+i*0.1) % 1
            ctx.arc(-300+i*60, 220-ph*440, 8, 0, 2*math.pi); ctx.set_source_rgba(1, 1, 1, 0.5*(1-ph)); ctx.fill()
        ctx.restore()
        ctx.save(); ctx.translate(cx, cy+40); ctx.rotate(0.05*math.sin(s.T*1.2))
        for (lx, ly) in ((-70, 130), (70, 130), (-40, 130), (40, 130)):
            ctx.move_to(lx, 60); ctx.line_to(lx, ly); ctx.set_line_width(14); ctx.set_source_rgba(0.25, 0.22, 0.22, 1); ctx.stroke()
        for (wx, wy, wr) in ((-80, 20, 50), (-30, 0, 58), (30, 0, 58), (80, 20, 50), (-50, 50, 48), (20, 55, 50), (70, 50, 44)):
            ctx.arc(wx, wy, wr, 0, 2*math.pi); ctx.set_source_rgba(0.97, 0.94, 0.88, 1); ctx.fill()
        ctx.save(); ctx.translate(140, -30); ctx.rotate(0.3); ctx.scale(0.8, 1.0); ctx.arc(0, 0, 42, 0, 2*math.pi); ctx.restore(); ctx.set_source_rgba(0.30, 0.26, 0.26, 1); ctx.fill()
        ctx.arc(150, -40, 6, 0, 2*math.pi); ctx.set_source_rgba(1, 1, 1, 1); ctx.fill()
        ctx.restore()
        ctx.move_to(cx+380, cy+60); ctx.curve_to(cx+520, cy+60, cx+560, cy+300, cx+700, cy+320); ctx.set_line_width(14); ctx.set_source_rgba(0.85, 0.35, 0.35, 1); ctx.stroke()
        if s.lt > s.at(0.25): bword(ctx, "PREMATURE LAMBS", 380, 260, 50, c('cream'), s.lt, s.at(0.25))
        if s.lt > s.at(0.33): bword(ctx, "4 WEEKS IN A BAG", 1540, 260, 54, c('hivis'), s.lt, s.at(0.33))
        return
    if s.lt < s.at(0.76):
        ctx.set_source_rgb(0.10, 0.12, 0.18); ctx.paint()
        text(ctx, "2021 · ISRAEL", W/2, 90, 56, c('hivis'))
        ctx.save(); ctx.translate(W/2, 600)
        ctx.arc(0, 0, 330, 0, 2*math.pi); ctx.set_line_width(14); ctx.set_source_rgba(0.6, 0.62, 0.7, 1); ctx.stroke()
        ctx.rotate(s.lt*1.2)
        for i in range(6):
            an = i*math.pi/3; x, y = 250*math.cos(an), 250*math.sin(an)
            paper(ctx, lambda k: rrect(k, x-40, y-60, 80, 120, 20), (0.80, 0.90, 1.0, 0.85))
            ctx.arc(x, y+10, 12, 0, 2*math.pi); ctx.set_source_rgba(0.95, 0.55, 0.60, 1); ctx.fill()
        ctx.restore()
        if s.lt > s.at(0.56): bword(ctx, "MOUSE EMBRYOS OUTSIDE THE BODY", W/2, 220, 54, c('cream'), s.lt, s.at(0.56))
        if s.lt > s.at(0.64): stamp(ctx, "ABOUT 6 DAYS", 1560, 860, 66, c('hivis'), s.lt, s.at(0.64))
        return
    ctx.set_source_rgb(0.04, 0.05, 0.09); ctx.paint()
    a = ease(s.pr(0.76, 0.84))
    ctx.save(); ctx.translate(W/2, 560); ctx.scale(1.0, 1.0)
    ctx.arc(0, -200, 90, 0, 2*math.pi); ctx.move_to(-150, -60); ctx.line_to(150, -60); ctx.line_to(110, 300); ctx.line_to(-110, 300); ctx.close_path()
    ctx.set_line_width(8); ctx.set_dash([24, 18]); ctx.set_source_rgba(*c('cream', a)); ctx.stroke(); ctx.set_dash([])
    text(ctx, "?", 0, 80, 220, c('hivis', a)); ctx.restore()
    if s.lt > s.at(0.8): bword(ctx, "NEVER DONE WITH A HUMAN", W/2, 140, 66, c('cream'), s.lt, s.at(0.8))
    if s.lt > s.at(0.9): stamp(ctx, "NOT FROM START TO FINISH", W/2, 980, 60, c('red'), s.lt, s.at(0.9))

def sc_mission_board(ctx, s):
    ctx.set_source_rgb(0.62, 0.45, 0.30); ctx.paint()
    rng = np.random.default_rng(3)
    for i in range(300):
        ctx.arc(rng.uniform(0, W), rng.uniform(0, H), rng.uniform(1, 3), 0, 2*math.pi); ctx.set_source_rgba(0.45, 0.30, 0.18, 0.6); ctx.fill()
    text_paper(ctx, "THE MISSION", W/2, 110, 90, c('cream'))
    cards = [("1", "MAKE THE EGGS", 0.12, -0.04), ("2", "SAVE THE EMBRYOS", 0.25, 0.03), ("3", "BUILD A WOMB", 0.38, -0.02)]
    for i, (n, w_, f, rot) in enumerate(cards):
        p = back(s.pr(f, f+0.08))
        if p <= 0: continue
        x = 380+i*580
        ctx.save(); ctx.translate(x, 420); ctx.rotate(rot); ctx.scale(p, p)
        paper(ctx, lambda k: k.rectangle(-240, -140, 480, 280), (0.99, 0.97, 0.88, 1))
        ctx.arc(0, -120, 16, 0, 2*math.pi); ctx.set_source_rgba(*c('red')); ctx.fill()
        text(ctx, n, 0, -40, 90, c('red')); text(ctx, w_, 0, 70, 44, c('ink'))
        ctx.restore()
    for i, (w_, f) in enumerate((("A LIBRARY CARD", 0.6), ("A GENERATOR", 0.72), ("A DOG", 0.84))):
        if s.lt > s.at(f): bword(ctx, w_, 380+i*580, 760, 54, c('yellow'), s.lt, s.at(f))
    if s.lt > s.at(0.84): quad(ctx, 1540, 980, 'dog', 0.85*back(s.pr(0.84, 0.9)), phase=s.T*9, run=0)

def sc_lit_window(ctx, s):
    sky(ctx, 'night'); stars(ctx, 220, alpha=0.8)
    z = 1.0 + 1.6*ease(s.pr(0.0, 0.95))
    ctx.save(); ctx.translate(1180, 520); ctx.scale(z, z); ctx.translate(-1180, -520)
    ctx.move_to(-100, H); ctx.curve_to(400, 640, 1500, 600, W+100, H); ctx.close_path(); ctx.set_source_rgba(0.05, 0.10, 0.08, 1); ctx.fill()
    paper(ctx, lambda k: k.rectangle(900, 360, 560, 340), (0.16, 0.18, 0.22, 1))
    for i in range(14):
        x = 900+i*42; ctx.move_to(x, 360); ctx.curve_to(x+20, 450, x-15, 560, x+10, 700); ctx.set_line_width(10); ctx.set_source_rgba(0.12, 0.30, 0.16, 0.9); ctx.stroke()
    for (wx, lit) in ((960, 0), (1080, 0), (1140, 1), (1300, 0)):
        if wx == 1140:
            pulse = 0.75+0.25*math.sin(s.T*2.2)
            g = cairo.RadialGradient(1180, 500, 5, 1180, 500, 160); g.add_color_stop_rgba(0, 1, 0.85, 0.5, 0.5*pulse); g.add_color_stop_rgba(1, 1, 0.85, 0.5, 0)
            ctx.set_source(g); ctx.arc(1180, 500, 160, 0, 2*math.pi); ctx.fill()
            ctx.rectangle(1140, 450, 80, 100); ctx.set_source_rgba(1, 0.86, 0.5, pulse); ctx.fill()
            ctx.rectangle(1160, 500, 40, 50); ctx.set_source_rgba(0.35, 0.30, 0.25, 0.8); ctx.fill()
            ctx.arc(1180, 500, 10*pulse, 0, 2*math.pi); ctx.set_source_rgba(0.95, 0.5, 0.55, 0.9); ctx.fill()
        else:
            ctx.rectangle(wx, 450, 80, 100); ctx.set_source_rgba(0.06, 0.07, 0.10, 1); ctx.fill()
    ctx.restore()
    if s.lt > s.at(0.05): bword(ctx, "ONE WINDOW STILL LIT", W/2-400, 120, 60, c('yellow'), s.lt, s.at(0.05))
    if s.lt > s.at(0.6): bword(ctx, "SOMETHING MIGHT BE GROWING", W/2, H-180, 58, c('cream'), s.lt, s.at(0.6))
    if s.lt > s.at(0.86): bword(ctx, "OR MAYBE IT ISN'T", W/2, H-80, 54, c('grey'), s.lt, s.at(0.86))

def sc_open_question(ctx, s):
    ctx.set_source_rgb(0.02, 0.02, 0.05); ctx.paint()
    kword(ctx, "DID YOU DO IT?", W/2, 260, 120, c('cream'), s.lt, s.at(0.0))
    if s.lt > s.at(0.2): bword(ctx, "COULD ONE PERSON RESTART THE HUMAN RACE?", W/2, 440, 56, c('yellow'), s.lt, s.at(0.2))
    if s.lt > s.at(0.6):
        p = ease(s.pr(0.6, 0.75)); pulse = 1+0.05*math.sin(s.T*3)
        ctx.save(); ctx.translate(W/2, 760); ctx.scale(pulse, pulse)
        text(ctx, "?", 0, 0, 300, c('hivis', p)); ctx.restore()
        if s.lt > s.at(0.72): bword(ctx, "NEVER ANSWERED", W/2, 1000, 50, c('grey'), s.lt, s.at(0.72))

def sc_outro_try(ctx, s):
    ctx.set_source_rgb(0.05, 0.07, 0.14); ctx.paint(); stars(ctx, 200, alpha=0.6)
    kword(ctx, "YOU TELL ME", W/2, 180, 100, c('cream'), s.lt, s.at(0.0))
    p = back(s.pr(0.1, 0.22))
    if p > 0:
        ctx.save(); ctx.translate(W/2, 460); ctx.scale(p, p)
        paper(ctx, lambda k: rrect(k, -560, -120, 1120, 240, 40), c('cream'))
        ctx.move_to(-380, 110); ctx.line_to(-440, 200); ctx.line_to(-290, 120); ctx.close_path(); ctx.set_source_rgba(*c('cream')); ctx.fill()
        text(ctx, "WOULD YOU EVEN TRY?", 0, 0, 86, c('red')); ctx.restore()
    if s.lt > s.at(0.32): bword(ctx, "TELL ME IN THE COMMENTS", W/2, 720, 62, c('yellow'), s.lt, s.at(0.32))
    if s.lt > s.at(0.6): bword(ctx, "NEXT: THE ANIMALS VANISH TOO", W/2, 880, 66, c('hivis'), s.lt, s.at(0.6))
