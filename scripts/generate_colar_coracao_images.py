from PIL import Image, ImageDraw, ImageFont, ImageFilter
from pathlib import Path
import os, math

OUT = Path("imagens/colar-coracao-personalizado")
OUT.mkdir(parents=True, exist_ok=True)
W=H=1000

def font(size,bold=False):
    candidates = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation2/LiberationSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/liberation2/LiberationSans-Regular.ttf",
    ]
    for p in candidates:
        if os.path.exists(p):
            return ImageFont.truetype(p,size)
    return ImageFont.load_default()

def heart_points(cx,cy,s):
    pts=[]
    for i in range(361):
        t=math.radians(i)
        x=16*math.sin(t)**3
        y=13*math.cos(t)-5*math.cos(2*t)-2*math.cos(3*t)-math.cos(4*t)
        pts.append((cx+x*s,cy-y*s))
    return pts

def draw_necklace(im, color, text="Mãe", photo=False, front_back=False, title=None):
    d=ImageDraw.Draw(im)
    metal=(225,225,230) if color=="Prata" else (232,177,42)
    edge=(110,110,115) if color=="Prata" else (145,92,10)

    # Chain
    for x in range(200,801,18):
        y=110+abs(x-500)*0.33
        d.ellipse((x,y,x+12,y+7),outline=metal,width=3)
    # Bail
    d.polygon([(470,300),(530,300),(520,380),(480,380)],fill=metal,outline=edge)

    # Heart
    pts=heart_points(500,545,11.5)
    d.polygon(pts,fill=metal,outline=edge)
    if photo:
        # Simulated engraving portrait silhouette
        d.ellipse((425,460,495,535),fill=(90,90,90))
        d.ellipse((505,470,575,540),fill=(120,120,120))
        d.arc((400,440,600,625),200,340,fill=(70,70,70),width=4)
        d.text((500,590),"FOTO",font=font(34,True),fill=(70,70,70),anchor="mm")
    else:
        d.text((500,535),text,font=font(64,False),fill=(25,25,25),anchor="mm")
        d.text((500,600),"♡",font=font(48),fill=(25,25,25),anchor="mm")

    if title:
        d.text((500,65),title,font=font(44,True),fill=(35,35,35),anchor="mm")

    return im

def base(bg=(249,247,243)):
    return Image.new("RGB",(W,H),bg)

def save_variant(fn,color,mode):
    im=base()
    d=ImageDraw.Draw(im)
    title=f"{color} • {'1 Face' if mode=='1F' else 'Frente e Verso'}"
    draw_necklace(im,color,text="Mãe",photo=False,title=title)
    if mode=="2F":
        # inset back photo
        inset=Image.new("RGB",(320,320),(245,245,245))
        draw_necklace(inset.resize((1000,1000)),color,photo=True)
        # create cropped heart-ish symbolic back
        inset=base((242,242,242)).resize((320,320))
        di=ImageDraw.Draw(inset)
        pts=heart_points(160,170,7)
        di.polygon(pts,fill=(225,225,230) if color=="Prata" else (232,177,42),outline=(100,100,100))
        di.ellipse((115,120,155,160),fill=(80,80,80))
        di.ellipse((165,125,205,165),fill=(110,110,110))
        di.text((160,220),"FOTO",font=font(28,True),fill=(60,60,60),anchor="mm")
        im.paste(inset,(640,625))
        d.rounded_rectangle((620,605,980,965),radius=24,outline=(160,120,40),width=5)
        d.text((800,585),"VERSO",font=font(30,True),fill=(80,60,20),anchor="mm")
    d.text((500,915),"Colar Coração Personalizado",font=font(34,True),fill=(45,45,45),anchor="mm")
    im.save(OUT/fn,"JPEG",quality=92,optimize=True)

# principal
im=base()
d=ImageDraw.Draw(im)
d.text((500,75),"Colar Coração Personalizado",font=font(48,True),fill=(35,35,35),anchor="mm")
left=base().crop((0,0,500,900)); left=left.resize((500,900))
right=base().crop((0,0,500,900)); right=right.resize((500,900))
# draw two separate pendants on same canvas
draw_necklace(im,"Prata",text="Mãe")
# redraw gold offset manually
metal=(232,177,42); edge=(145,92,10)
for x in range(560,861,14):
    y=220+abs(x-710)*0.28
    d.ellipse((x,y,x+10,y+6),outline=metal,width=3)
d.polygon([(690,360),(730,360),(724,410),(696,410)],fill=metal,outline=edge)
pts=heart_points(710,565,8)
d.polygon(pts,fill=metal,outline=edge)
d.text((710,555),"Pai",font=font(48),fill=(25,25,25),anchor="mm")
d.text((710,605),"♡",font=font(38),fill=(25,25,25),anchor="mm")
d.text((500,900),"Prata • Dourado | Foto • Nome • Data • Frase curta",font=font(28,True),fill=(70,70,70),anchor="mm")
im.save(OUT/"01-principal.jpg","JPEG",quality=92,optimize=True)

save_variant("variacao-prata-1f.jpg","Prata","1F")
save_variant("variacao-prata-2f.jpg","Prata","2F")
save_variant("variacao-dourado-1f.jpg","Dourado","1F")
save_variant("variacao-dourado-2f.jpg","Dourado","2F")

# frente/verso
im=base()
d=ImageDraw.Draw(im)
d.text((500,70),"Frente e Verso Personalizáveis",font=font(46,True),fill=(35,35,35),anchor="mm")
# left heart
pts=heart_points(290,500,10)
d.polygon(pts,fill=(225,225,230),outline=(100,100,100))
d.text((290,485),"Mãe",font=font(58),fill=(30,30,30),anchor="mm")
d.text((290,545),"♡",font=font(42),fill=(30,30,30),anchor="mm")
# right heart photo
pts=heart_points(710,500,10)
d.polygon(pts,fill=(225,225,230),outline=(100,100,100))
d.ellipse((650,440,700,495),fill=(80,80,80)); d.ellipse((715,445,765,500),fill=(120,120,120))
d.text((290,760),"Frente: nome, data ou frase",font=font(28,True),fill=(50,50,50),anchor="mm")
d.text((710,760),"Verso: foto ou outra personalização",font=font(28,True),fill=(50,50,50),anchor="mm")
im.save(OUT/"02-frente-verso.jpg","JPEG",quality=92,optimize=True)

# personalizacao
im=base()
d=ImageDraw.Draw(im)
d.text((500,90),"Personalize do seu jeito",font=font(48,True),fill=(35,35,35),anchor="mm")
opts=["Foto","Nome","Iniciais","Data","Frase curta"]
for i,o in enumerate(opts):
    y=230+i*125
    d.rounded_rectangle((180,y-45,820,y+45),radius=20,fill=(255,255,255),outline=(190,160,80),width=3)
    d.text((500,y),o,font=font(38,True),fill=(50,50,50),anchor="mm")
d.text((500,900),"Após a compra, envie a personalização pelo chat.",font=font(27,True),fill=(70,70,70),anchor="mm")
im.save(OUT/"03-personalizacao.jpg","JPEG",quality=92,optimize=True)

# medidas
im=base()
d=ImageDraw.Draw(im)
d.text((500,85),"Medidas aproximadas",font=font(48,True),fill=(35,35,35),anchor="mm")
pts=heart_points(500,470,10)
d.polygon(pts,fill=(225,225,230),outline=(100,100,100))
d.line((300,700,700,700),fill=(60,60,60),width=4)
d.polygon([(300,700),(320,690),(320,710)],fill=(60,60,60)); d.polygon([(700,700),(680,690),(680,710)],fill=(60,60,60))
d.text((500,745),"23,5 mm",font=font(34,True),fill=(50,50,50),anchor="mm")
d.line((270,320,270,650),fill=(60,60,60),width=4)
d.text((175,485),"23 mm",font=font(34,True),fill=(50,50,50),anchor="mm")
d.text((500,835),"Espessura aprox.: 1 mm   |   Corrente: aprox. 45 cm",font=font(30,True),fill=(55,55,55),anchor="mm")
im.save(OUT/"04-medidas.jpg","JPEG",quality=92,optimize=True)

print("generated", len(list(OUT.glob("*.jpg"))), "images")

# trigger
