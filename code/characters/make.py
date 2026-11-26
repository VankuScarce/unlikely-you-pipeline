"""python3 make.py  -> ../character_styles_preview.mp4, ../stills/*.png, ../character_styles_sheet.png"""
import sys, os, subprocess
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from scenes import frame, SCENES, DUR, W, H
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
FPS = 30
os.makedirs(f'{OUT}/stills', exist_ok=True)
for i, (L, name, use, _) in enumerate(SCENES):
    frame(i, 2.6, labelled=False, fade=False).write_to_png(f'{OUT}/stills/{L}_{name.lower().replace(" ", "_")}.png')
if 'stills' in sys.argv: sys.exit()
p = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'bgra', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                      '-c:v', 'libx264', '-preset', 'medium', '-crf', '19', '-pix_fmt', 'yuv420p', '/tmp/claude-0/cs/preview.mp4'], stdin=subprocess.PIPE)
for i in range(len(SCENES)):
    for f in range(int(DUR*FPS)):
        p.stdin.write(bytes(frame(i, f/FPS).get_data()))
p.stdin.close(); p.wait()
