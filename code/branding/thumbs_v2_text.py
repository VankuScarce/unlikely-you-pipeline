from PIL import Image, ImageDraw, ImageFont
F='/tmp/claude-0/thumbs2/'; OUT='/mnt/project-files/episodes/ep02_everyone_vanished/thumbnails/v2/'
import os; os.makedirs(OUT,exist_ok=True)
BLK='/usr/share/fonts/opentype/inter/InterDisplay-Black.otf'
W,H=1280,720; OR=(255,140,46); WH=(255,255,255)
def f(s): return ImageFont.truetype(BLK,s)
def t(d,xy,s,size,fill,anchor='la',stroke=12): d.text(xy,s,font=f(size),fill=fill,anchor=anchor,stroke_width=stroke,stroke_fill=(0,0,0))
def tag(d,xy,s,size,bg,fg,anchor='la'):
    b=d.textbbox(xy,s,font=f(size),anchor=anchor); p=18
    d.rounded_rectangle((b[0]-p,b[1]-p,b[2]+p,b[3]+p),radius=14,fill=bg); d.text(xy,s,font=f(size),fill=fg,anchor=anchor)
L=lambda k: Image.open(F+f'bg_{k}.png').convert('RGB').resize((W,H),Image.LANCZOS)
im=L('D'); d=ImageDraw.Draw(im)
t(d,(1230,120),"WHERE IS",118,WH,anchor='ra'); t(d,(1230,255),"EVERYONE?",118,OR,anchor='ra')
im.save(OUT+'thumb_D_where_is_everyone.jpg',quality=92)
im=L('E'); d=ImageDraw.Draw(im)
tag(d,(320,70),"8,000,000,000",74,(255,255,255),(20,20,24),anchor='ma')
tag(d,(960,70),"1",110,OR,(20,20,24),anchor='ma')
im.save(OUT+'thumb_E_8_billion_to_1.jpg',quality=92)
im=L('F'); d=ImageDraw.Draw(im)
t(d,(1230,60),"DAY 1.",140,WH,anchor='ra'); t(d,(1230,215),"ALONE.",140,OR,anchor='ra')
im.save(OUT+'thumb_F_day_1_alone.jpg',quality=92)
ims=[Image.open(OUT+n) for n in sorted(os.listdir(OUT)) if n.startswith('thumb_')]
sheet=Image.new('RGB',(W,H*3+40),(245,245,245))
for i,im in enumerate(ims): sheet.paste(im,(0,i*(H+20)))
sheet.resize((W//2,(H*3+40)//2)).save(OUT+'thumbnail_options_v2.jpg',quality=90)
