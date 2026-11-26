"""Cut the finished episode into a numbered Part 1..N series (Instagram / TikTok / Shorts), each ending on a cliffhanger.
Makes, per part: a 16:9 video (like the reference reel), a 9:16 video with captions, and a 9:16 cover with a big PART N.
Usage: python3 parts.py EPISODE.mp4 VO_DIR OUT_DIR"""
import sys, os, subprocess
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import ep02
from shorts import captions, ts, HEAD as HEAD_V
from PIL import Image, ImageDraw, ImageFont, ImageFilter

TITLE = "EVERYONE VANISHED\\NEXCEPT YOU"
# (part, first shot, last shot, cover shot, point in that shot's narration for the cover frame)
PARTS = [(1, 's01', 's06', 's04', 0.6), (2, 's07', 's19', 's19', 0.5), (3, 's20', 's36', 's30', 0.5),
         (4, 's37', 'n10', 'n10', 0.6), (5, 's41', 'n22', 'n20', 0.6)]
HOLD = 2.0   # seconds of end card ("PART N+1 NEXT") after each cliffhanger
FONT = '/usr/share/fonts/opentype/inter/InterDisplay-Black.otf'
FONT_B = '/usr/share/fonts/opentype/inter/InterDisplay-Bold.otf'

HEAD_H = """[Script Info]
ScriptType: v4.00+
PlayResX: 1920
PlayResY: 1080
WrapStyle: 2

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Part,Inter Display,52,&H00FFFFFF,&H00FFFFFF,&H00000000,&H90000000,1,0,0,0,100,100,2,0,3,14,0,9,60,48,40,1
Style: Next,Inter Display,150,&H0000E6FF,&H00FFFFFF,&H00000000,&H00000000,1,0,0,0,100,100,4,0,1,8,0,5,60,60,0,1
Style: Sub,Inter Display,54,&H00FFFFFF,&H00FFFFFF,&H00000000,&H00000000,1,0,0,0,100,100,2,0,1,5,0,5,60,60,0,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
EXTRA_V = """Style: Next,Inter Display,140,&H0000E6FF,&H00FFFFFF,&H00000000,&H00000000,1,0,0,0,100,100,4,0,1,8,0,5,60,60,0,1
Style: Sub,Inter Display,58,&H00FFFFFF,&H00FFFFFF,&H00000000,&H00000000,1,0,0,0,100,100,2,0,1,5,0,5,60,60,0,1
"""

def end_card(f, n, last, d, y_next, y_sub):
    if last:  # the final scene already asks the question on screen
        return
    f.write(f"Dialogue: 2,{ts(d+0.1)},{ts(d+HOLD)},Next,,0,0,0,,{{\\pos({f.cx},{y_next})\\fad(150,0)\\fscx70\\fscy70\\t(0,160,\\fscx100\\fscy100)}}PART {n+1}\n")
    f.write(f"Dialogue: 2,{ts(d+0.25)},{ts(d+HOLD)},Sub,,0,0,0,,{{\\pos({f.cx},{y_sub})\\fad(150,0)}}IS UP NEXT\n")

class Ass:
    def __init__(self, path, cx): self.h = open(path, 'w'); self.cx = cx
    def write(self, s): self.h.write(s)
    def close(self): self.h.close()

def run(cmd): subprocess.run(cmd, check=True)

def cover(ep, t, n, out):
    raw = out + '.frame.png'
    run(['ffmpeg', '-y', '-v', 'error', '-ss', f'{t:.2f}', '-i', ep, '-frames:v', '1', raw])
    fr = Image.open(raw).convert('RGB'); os.remove(raw)
    W, H = 1080, 1920
    bg = fr.resize((int(fr.width*H/fr.height), H))
    x0 = (bg.width-W)//2; bg = bg.crop((x0, 0, x0+W, H)).filter(ImageFilter.GaussianBlur(40))
    bg = Image.eval(bg, lambda v: int(v*0.55))
    fg = fr.resize((W, int(fr.height*W/fr.width)))
    bg.paste(fg, (0, (H-fg.height)//2 + 120))
    d = ImageDraw.Draw(bg)
    big = ImageFont.truetype(FONT, 260); mid = ImageFont.truetype(FONT_B, 76)
    def centred(y, txt, font, fill, stroke=10):
        w = d.textlength(txt, font=font); d.text(((W-w)/2, y), txt, font=font, fill=fill, stroke_width=stroke, stroke_fill=(0, 0, 0))
    centred(330, f"PART {n}", big, (255, 230, 0))
    centred(640, "EVERYONE VANISHED", mid, (255, 255, 255), 6)
    centred(730, "EXCEPT YOU", mid, (255, 255, 255), 6)
    bg.save(out, quality=92)

def main(ep, vo_dir, out_dir):
    tl = ep02.setup(vo_dir); os.makedirs(out_dir, exist_ok=True)
    idx = {sh['id']: i for i, sh in enumerate(tl)}; total = len(PARTS)
    for n, a, b, cov, frac in PARTS:
        shots = tl[idx[a]:idx[b]+1]
        t0 = 0.0 if n == 1 else shots[0]['start']; t1 = shots[-1]['start']+shots[-1]['dur']; d = t1-t0
        last = n == total; hold = 1.2 if last else HOLD; D = d+hold
        af = f"apad=pad_dur={hold},afade=t=in:st=0:d={0.0 if n == 1 else 0.25},afade=t=out:st={D-1.6:.2f}:d=1.6"
        dim = f"drawbox=x=0:y=0:w=iw:h=ih:color=black@0.55:t=fill:enable='gte(t,{d:.2f})'"
        # 16:9 version
        ass = os.path.join(out_dir, f'part{n}_16x9.ass'); f = Ass(ass, 960); f.write(HEAD_H)
        f.write(f"Dialogue: 1,{ts(0.2)},{ts(3.2)},Part,,0,0,0,,{{\\fad(200,300)}}PART {n}\n")
        end_card(f, n, last, d, 500, 640); f.close()
        run(['ffmpeg', '-y', '-v', 'error', '-ss', f'{t0:.3f}', '-t', f'{d:.3f}', '-i', ep,
             '-vf', f"tpad=stop_mode=clone:stop_duration={hold},{dim},subtitles={ass}", '-af', af,
             '-c:v', 'libx264', '-preset', 'medium', '-crf', '19', '-pix_fmt', 'yuv420p',
             '-c:a', 'aac', '-aac_coder', 'fast', '-b:a', '192k', '-movflags', '+faststart',
             os.path.join(out_dir, f'part{n}_16x9.mp4')])
        # 9:16 version with captions
        ass = os.path.join(out_dir, f'part{n}_9x16.ass'); f = Ass(ass, 540)
        f.write(HEAD_V.replace('[Events]', EXTRA_V + '\n[Events]').replace('\n\n' + EXTRA_V, '\n' + EXTRA_V))
        f.write(f"Dialogue: 0,{ts(0)},{ts(d)},Hook,,0,0,0,,{{\\fad(150,0)}}{{\\c&H00E6FF&}}PART {n}{{\\c&HFFFFFF&}}\\N{TITLE}\n")
        for s, e, tx in captions(shots, t0, os.path.join(vo_dir, 'words.json')):
            f.write(f"Dialogue: 1,{ts(s)},{ts(min(e, d))},Cap,,0,0,0,,{{\\fscx80\\fscy80\\t(0,90,\\fscx100\\fscy100)}}{tx}\n")
        end_card(f, n, last, d, 900, 1040); f.close()
        fc = (f"[0:v]tpad=stop_mode=clone:stop_duration={hold},split=2[a][b];"
              "[a]scale=-2:1920,crop=1080:1920,gblur=sigma=40,eq=brightness=-0.18[bg];"
              "[b]scale=1080:608[fg];"
              f"[bg][fg]overlay=0:596,{dim},subtitles={ass}[v]")
        run(['ffmpeg', '-y', '-v', 'error', '-ss', f'{t0:.3f}', '-t', f'{d:.3f}', '-i', ep, '-filter_complex', fc,
             '-map', '[v]', '-map', '0:a', '-af', af, '-c:v', 'libx264', '-preset', 'medium', '-crf', '20', '-pix_fmt', 'yuv420p',
             '-c:a', 'aac', '-aac_coder', 'fast', '-b:a', '192k', '-movflags', '+faststart',
             os.path.join(out_dir, f'part{n}_9x16.mp4')])
        sh = tl[idx[cov]]
        cover(ep, sh['start'] + sh['lead'] + frac*sh['vo'], n, os.path.join(out_dir, f'part{n}_cover.jpg'))
        print(f'part {n}: {a}-{b}  {d:.1f}s (+{hold}s end card)', flush=True)

if __name__ == '__main__':
    main(*sys.argv[1:4])
