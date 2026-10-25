from PIL import Image, ImageDraw, ImageFilter
from pathlib import Path
import math

OUT = Path("imagens/chaveiro-placa-laser")
OUT.mkdir(parents=True, exist_ok=True)

W=H=1000

COLORS = {
    "preto": ((32,32,32),(22,22,22)),
    "cinza": ((150,150,150),(120,120,120)),
    "marrom": ((154,82,47),(130,64,35)),
}

def rounded(draw, box, r, fill, outline=None, width=1):
    draw.rounded_rectangle(box, radius=r, fill=fill, outline=outline, width=width)

def draw_keychain(name, base, dark):
    im = Image.new("RGB",(W,H),(250,248,244))
    d=ImageDraw.Draw(im)

    # soft shadow
    sh=Image.new("RGBA",(W,H),(0,0,0,0))
    sd=ImageDraw.Draw(sh)
    sd.ellipse((320,850,680,900), fill=(0,0,0,40))
    sh=sh.filter(ImageFilter.GaussianBlur(18))
    im.paste(sh,(0,0),sh)
    d=ImageDraw.Draw(im)

    # strap
    x0,x1=405,595
    y0,y1=80,520
    rounded(d,(x0,y0,x1,y1),26,base,outline=dark,width=5)
    # stitch lines
    stitch=(220,220,220) if name!="marrom" else (205,145,105)
    for x in (430,570):
        for y in range(105,500,20):
            d.line((x,y,x,y+10), fill=stitch, width=3)

    # plaque shadow
    rounded(d,(360,475,640,710),34,(35,35,35),outline=(70,70,70),width=4)

    # metallic beaded border
    rounded(d,(372,487,628,698),30,(185,185,185),outline=(75,75,75),width=4)
    for xx in range(390,612,14):
        d.ellipse((xx,494,xx+6,500), fill=(235,235,235))
        d.ellipse((xx,685,xx+6,691), fill=(100,100,100))
    for yy in range(510,676,14):
        d.ellipse((379,yy,385,yy+6), fill=(230,230,230))
        d.ellipse((615,yy,621,yy+6), fill=(110,110,110))

    # center engraving pad
    rounded(d,(400,515,600,674),18,base,outline=dark,width=4)

    # swivel
    rounded(d,(445,700,555,765),18,(90,90,90),outline=(40,40,40),width=4)
    d.polygon([(466,742),(500,770),(534,742),(525,716),(475,716)], fill=(105,105,105))

    # ring
    d.ellipse((355,735,645,965), outline=(65,65,65), width=25)
    d.ellipse((380,760,620,940), outline=(180,180,180), width=4)

    # visual highlight
    gloss=Image.new("RGBA",(W,H),(0,0,0,0))
    gd=ImageDraw.Draw(gloss)
    gd.rounded_rectangle((410,90,455,500),radius=18,fill=(255,255,255,20))
    gd.arc((368,482,632,704),180,300,fill=(255,255,255,120),width=3)
    im=Image.alpha_composite(im.convert("RGBA"),gloss).convert("RGB")

    path=OUT/f"variacao-{name}.jpg"
    im.save(path,"JPEG",quality=94,subsampling=0,optimize=True)
    print(path)

for n,(base,dark) in COLORS.items():
    draw_keychain(n,base,dark)

# trigger workflow
