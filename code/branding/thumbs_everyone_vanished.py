# Thumbnails for "What If Everyone Vanished... Except You?" (no twist reveal). Backgrounds: thumb_scene.py + one video frame.
from PIL import Image, ImageDraw, ImageFont, ImageEnhance, ImageFilter
F='/tmp/claude-0/thumbs/'; OUT='/mnt/project-files/episodes/ep02_everyone_vanished/thumbnails/'
BLK='/usr/share/fonts/opentype/inter/InterDisplay-Black.otf'
W,H=1280,720; ORANGE=(255,140,46); WHITE=(255,255,255)
def font(s): return ImageFont.truetype(BLK,s)
def text(d,xy,t,size,fill,anchor='la',stroke=12):
    d.text(xy,t,font=font(size),fill=fill,anchor=anchor,stroke_width=stroke,stroke_fill=(0,0,0))
def crop(img,cx,cy,zoom):
    w,h=img.size; cw,ch=w/zoom,h/zoom; x0=max(0,min(w-cw,cx-cw/2)); y0=max(0,min(h-ch,cy-ch/2))
    return img.crop((int(x0),int(y0),int(x0+cw),int(y0+ch))).resize((W,H),Image.LANCZOS)
# A (main): something in the alley
im=Image.open(F+'scene_A.png').convert('RGB').resize((W,H),Image.LANCZOS); d=ImageDraw.Draw(im)
text(d,(W/2,22),"EVERYONE'S GONE...",104,WHITE,anchor='ma')
text(d,(1000,560),"RIGHT?",120,ORANGE,anchor='ma')
im.save(OUT+'thumb_A_something_here.jpg',quality=92)
# B: 41 messages, all at 3:17 AM
im=crop(Image.open(F+'full_20.png').convert('RGB'),1680,330,1.35); im=ImageEnhance.Brightness(im).enhance(1.15); d=ImageDraw.Draw(im)
text(d,(50,90),"EVERYONE",112,WHITE); text(d,(50,215),"VANISHED",112,WHITE); text(d,(50,360),"AT 3:17 AM",112,ORANGE)
text(d,(54,520),"(except you)",64,(220,220,230),stroke=8)
im.save(OUT+'thumb_B_317am.jpg',quality=92)
# C: alone in daylight
im=Image.open(F+'scene_C.png').convert('RGB').resize((W,H),Image.LANCZOS); d=ImageDraw.Draw(im)
text(d,(W/2,40),"8 BILLION GONE",124,WHITE,anchor='ma'); text(d,(W/2,180),"EXCEPT YOU",100,ORANGE,anchor='ma')
im.save(OUT+'thumb_C_8_billion.jpg',quality=92)
