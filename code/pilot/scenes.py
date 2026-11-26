"""JSON-driven scene library for Ozzie Runs the Odds.
Episode spec: {"fps":24,"scenes":[{"type":"stat_card","dur":5,"p":{...}}, ...]}
Each template: fn(ctx, lt, dur, p). Reuses the cold-open scenes as templates too."""
import sys, os, json, math, subprocess, cairo, numpy as np
sys.path.insert(0, os.path.dirname(__file__))
from style import *
import coldopen as co

def _wrap(fn, orig_start):
    return lambda ctx, lt, dur, p: fn(ctx, orig_start + lt)

def camera_map(ctx, lt, dur, p):
    """Top-down city grid; plate cameras blink on one by one; optional route arrow."""
    ctx.set_source_rgba(*c('navy')); ctx.paint()
    ctx.set_line_width(26); ctx.set_source_rgba(0.22,0.32,0.40,1)
    for i in range(9): ctx.move_to(0,80+i*120); ctx.line_to(W,80+i*120); ctx.stroke()
    for i in range(15): ctx.move_to(60+i*130,0); ctx.line_to(60+i*130,H); ctx.stroke()
    n = p.get('cameras', 40); rng = np.random.default_rng(5)
    pts = [(60+rng.integers(0,15)*130, 80+rng.integers(0,9)*120) for _ in range(n)]
    shown = int(n * ease(lt/max(0.1,dur*0.8)))
    for i,(x,y) in enumerate(pts[:shown]):
        pop = back(min(1,(lt - i*dur*0.8/n)*4))
        paper(ctx, lambda k,x=x,y=y,pop=pop: rrect(k,x-14*pop,y-10*pop,28*pop,20*pop,4), c('cream'), off=(3,4))
        ctx.arc(x+6,y,4,0,2*math.pi); ctx.set_source_rgba(*c('red', 0.5+0.5*math.sin(lt*6+i))); ctx.fill()
    if p.get('route'):
        k = ease(lt/dur); path = [(190,80+4*120),(190+k*1300,80+4*120)]
        ctx.set_line_width(10); ctx.set_source_rgba(*c('orange')); ctx.move_to(*path[0]); ctx.line_to(*path[1]); ctx.stroke()
        ctx.arc(*path[1],18,0,2*math.pi); ctx.fill()
    if p.get('caption'):
        paper(ctx, lambda k: rrect(k,60,H-170,1100,110,18), c('ink',0.92))
        text(ctx, p['caption'], 100, H-115, 44, c('cream'), anchor='l')

def thermal(ctx, lt, dur, p):
    """Helicopter thermal-camera view: dark blue city, hot orange target, HUD reticle."""
    ctx.set_source_rgba(0.04,0.06,0.18,1); ctx.paint()
    rng = np.random.default_rng(9)
    for i in range(60):
        x,y,w,h = rng.integers(0,W),rng.integers(0,H),rng.integers(60,240),rng.integers(60,240)
        ctx.rectangle(x,y,w,h); ctx.set_source_rgba(0.10,0.14,0.32,1); ctx.fill()
    tx = 300 + (W-600)*ease(lt/dur); ty = 560 + 60*math.sin(lt*0.8)
    for r,a in ((120,0.15),(70,0.35),(34,0.9)):
        g = cairo.RadialGradient(tx,ty,0,tx,ty,r); g.add_color_stop_rgba(0,1,0.95,0.8,a); g.add_color_stop_rgba(0.5,1,0.5,0.1,a*0.7); g.add_color_stop_rgba(1,1,0.2,0,0)
        ctx.set_source(g); ctx.paint()
    ctx.set_line_width(4); ctx.set_source_rgba(1,1,1,0.85)
    for sx,sy in ((-1,-1),(1,-1),(-1,1),(1,1)):
        ctx.move_to(tx+sx*90,ty+sy*60); ctx.line_to(tx+sx*90,ty+sy*90); ctx.line_to(tx+sx*60,ty+sy*90); ctx.stroke()
    text(ctx, "FLIR  WHT-HOT   ALT 1,200 FT", 60, 60, 30, (1,1,1,0.8), anchor='l', font='DejaVu Sans Mono')
    text(ctx, p.get('callout','TARGET NORTHBOUND'), 60, H-60, 30, (1,1,1,0.8), anchor='l', font='DejaVu Sans Mono')

def stat_card(ctx, lt, dur, p):
    """Big number reveal with counter roll-up + caption. Mark FACT numbers in the script."""
    ctx.set_source_rgba(*c(p.get('bg','teal'))); ctx.paint()
    v = p['value']; k = ease(prog(lt,0.2,1.4)); cur = v*k
    s = p.get('fmt','{:,.0f}').format(cur) + p.get('suffix','')
    a = back(prog(lt,0,0.4))
    ctx.save(); ctx.translate(W/2,H/2-60); ctx.scale(a,a); text_paper(ctx, s, 0, 0, 230, c('cream')); ctx.restore()
    text(ctx, p.get('caption',''), W/2, H/2+130, 52, c('ink'))
    if p.get('estimate'): text(ctx, "ESTIMATE", W/2, H/2+210, 30, c('ink',0.6))

def exits_closing(ctx, lt, dur, p):
    """Peninsula map; escape routes flash then turn red one by one."""
    ctx.set_source_rgba(*c('navy')); ctx.paint()
    def land(k):
        k.new_path(); k.move_to(500,0); k.line_to(1500,0); k.curve_to(1450,400,1300,700,1050,1080); k.line_to(900,1080); k.curve_to(860,700,700,350,500,0); k.close_path()
    paper(ctx, land, (0.16,0.30,0.32,1), off=(10,12))
    exits = p.get('exits', [(620,120),(1420,160),(1300,520),(980,1000),(820,420)])
    for i,(x,y) in enumerate(exits):
        t0 = 0.5 + i*(dur-1)/len(exits); closed = lt > t0
        col = c('red') if closed else c('yellow', 0.5+0.5*math.sin(lt*8))
        ctx.arc(x,y,30 + (8*back(min(1,(lt-t0)*3)) if closed else 0),0,2*math.pi); ctx.set_source_rgba(*col); ctx.fill()
        if closed:
            ctx.set_line_width(8); ctx.set_source_rgba(*c('cream'))
            ctx.move_to(x-14,y-14); ctx.line_to(x+14,y+14); ctx.move_to(x+14,y-14); ctx.line_to(x-14,y+14); ctx.stroke()
    if p.get('caption'):
        paper(ctx, lambda k: rrect(k,60,H-170,900,110,18), c('ink',0.92))
        text(ctx, p['caption'], 100, H-115, 44, c('cream'), anchor='l')

def ozzie_explains(ctx, lt, dur, p):
    """Ozzie at the desk next to a big caption board (for explanation beats)."""
    ctx.set_source_rgba(*c('navy')); ctx.paint()
    paper(ctx, lambda k: rrect(k,900,170,920,560,30), c('cream'), off=(10,12))
    lines = p.get('lines', [])
    for i,l in enumerate(lines):
        a = ease(prog(lt, 0.3+i*0.8, 0.8+i*0.8))
        text(ctx, l, 960, 260+i*110, 56, c('ink',a), anchor='l')
    paper(ctx, lambda k: k.rectangle(0,820,W,260), (0.30,0.20,0.16,1), off=(0,-10))
    blink = 1.0 if (lt % 3.7) < 0.12 else 0.0
    ozzie(ctx, 470, 880, 1.25, blink=blink, look=(0.7,-0.1), wing=0.6*abs(math.sin(lt*1.3)))

def odds_board(ctx, lt, dur, p):
    """Full-screen Odds Board update: stars + survival time, the recurring section break."""
    ctx.set_source_rgba(*c('ink')); ctx.paint()
    n = p.get('stars',1)
    for i in range(5):
        pop = back(prog(lt, 0.2+i*0.12, 0.5+i*0.12)) if i < n else 1
        star(ctx, W/2-240+i*120, 260, 52*(pop if i<n else 1), c('yellow'), empty=i>=n)
    co.oddsboard(ctx, W/2, 600, p.get('label','SURVIVAL TIME'), p.get('value','00:00:00'))
    if p.get('heading'): text_paper(ctx, p['heading'], W/2, 900, 70, c('orange'))

TEMPLATES = {
    'location_gas_station': _wrap(co.s1, 0), 'record_screen': _wrap(co.s2, 8.6), 'case_file': _wrap(co.s3, 14.0),
    'scanner_map': _wrap(co.s4, 19.0), 'choice': _wrap(co.s5, 22.2), 'chase': _wrap(co.s6, 26.0),
    'ozzie_reveal': _wrap(co.s7, 33.2), 'title_card': _wrap(co.title, 36.4),
    'camera_map': camera_map, 'thermal': thermal, 'stat_card': stat_card, 'exits_closing': exits_closing,
    'ozzie_explains': ozzie_explains, 'odds_board': odds_board,
}

def render(spec, out, t0=0.0, t1=None):
    fps = spec.get('fps',24); scenes = spec['scenes']
    starts = np.cumsum([0]+[s['dur'] for s in scenes]); total = starts[-1] if t1 is None else min(t1, starts[-1])
    p = subprocess.Popen(['ffmpeg','-loglevel','error','-y','-f','rawvideo','-pix_fmt','bgra','-s',f'{W}x{H}','-r',str(fps),'-i','-',
                          '-c:v','libx264','-preset','medium','-crf','18','-pix_fmt','yuv420p',out], stdin=subprocess.PIPE)
    for n in range(int(round(t0*fps)), int(round(total*fps))):
        t = n/fps; i = int(np.searchsorted(starts, t, side='right')-1); s = scenes[i]; lt = t-starts[i]
        surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H); ctx = cairo.Context(surf)
        TEMPLATES[s['type']](ctx, lt, s['dur'], s.get('p',{}))
        if lt < 0.2 and i>0:
            ctx.rectangle(0,0,W*(1-ease(lt/0.2)),H); ctx.set_source_rgba(*c('ink')); ctx.fill()
        vignette(ctx,0.35); grain(ctx,0.12)
        p.stdin.write(bytes(surf.get_data()))
    p.stdin.close(); p.wait()


def dispatch_grid(ctx, lt, dur, p):
    """Top-down chase: your orange arrow; blue units converge on where you're going, not where you are."""
    ctx.set_source_rgba(*c('navy')); ctx.paint()
    ctx.set_line_width(30); ctx.set_source_rgba(0.22,0.32,0.40,1)
    for i in range(8): ctx.move_to(0,100+i*130); ctx.line_to(W,100+i*130); ctx.stroke()
    for i in range(12): ctx.move_to(100+i*160,0); ctx.line_to(100+i*160,H); ctx.stroke()
    k = lt/dur; yx = 100 + k*1500; yy = 100+4*130
    target = (1700, yy)
    ctx.set_line_width(6); ctx.set_dash([18,14]); ctx.set_source_rgba(*c('orange',0.6)); ctx.move_to(yx,yy); ctx.line_to(*target); ctx.stroke(); ctx.set_dash([])
    paper(ctx, lambda kk:(kk.new_path(),kk.move_to(yx+30,yy),kk.line_to(yx-20,yy-22),kk.line_to(yx-20,yy+22),kk.close_path()), c('orange'), off=(4,5))
    # follower
    fx = yx-180; ctx.arc(fx,yy,16,0,2*math.pi); ctx.set_source_rgba(*c('red' if int(lt*6)%2 else 'blue')); ctx.fill()
    rng = np.random.default_rng(11)
    for i in range(p.get('units',7)):
        sx, sy = 100+rng.integers(0,12)*160, 100+rng.integers(0,8)*130
        e = ease(prog(lt, 0.5+i*0.4, dur))
        ux = sx + (target[0]-60*math.cos(i) - sx)*e; uy = sy + (target[1]-60*math.sin(i) - sy)*e
        ctx.arc(ux,uy,16,0,2*math.pi); ctx.set_source_rgba(*c('blue')); ctx.fill()
        ctx.arc(ux,uy,24+6*math.sin(lt*6+i),0,2*math.pi); ctx.set_line_width(3); ctx.set_source_rgba(*c('blue',0.5)); ctx.stroke()
    if p.get('caption'):
        paper(ctx, lambda kk: rrect(kk,60,H-170,1000,110,18), c('ink',0.92))
        text(ctx, p['caption'], 100, H-115, 44, c('cream'), anchor='l')

TEMPLATES['dispatch_grid'] = dispatch_grid

if __name__ == '__main__':
    a=sys.argv; render(json.load(open(a[1])), a[2], float(a[3]) if len(a)>3 else 0.0, float(a[4]) if len(a)>4 else None)
