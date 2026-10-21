from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
import math

OUT = Path("imagens/shoe-name")
OUT.mkdir(parents=True, exist_ok=True)

COLORS = {
    "preto-branco": ("#111111","#FFFFFF"),
    "branco-preto": ("#F7F7F7","#111111"),
    "azul-branco": ("#2563EB","#FFFFFF"),
    "vermelho-branco": ("#EF4444","#FFFFFF"),
    "verde-branco": ("#16A34A","#FFFFFF"),
    "amarelo-preto": ("#FACC15","#111111"),
    "rosa-branco": ("#EC4899","#FFFFFF"),
    "lilas-branco": ("#A855F7","#FFFFFF"),
    "laranja-preto": ("#F97316","#111111"),
}

def font(size,bold=False):
    paths=[
      "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
      "/usr/share/fonts/truetype/liberation2/LiberationSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/liberation2/LiberationSans-Regular.ttf",
    ]
    for p in paths:
        if Path(p).exists():
            return ImageFont.truetype(p,size)
    return ImageFont.load_default()

F20=font(20); F26=font(26,True); F34=font(34,True); F44=font(44,True); F54=font(54,True)

def center(d,x,y,text,fnt,fill):
    b=d.textbbox((0,0),text,font=fnt)
    d.text((x-(b[2]-b[0])/2,y-(b[3]-b[1])/2),text,font=fnt,fill=fill)

def base(bg="white"):
    return Image.new("RGB",(1000,1000),bg)

def shoe(d, charm="#111111", text="#FFFFFF", name="RODRIGO", x=110,y=180,scale=1.0):
    # clean sneaker silhouette
    w=int(720*scale); h=int(440*scale)
    d.rounded_rectangle((x,y,x+w,y+h),radius=int(85*scale),fill="#F5F5F5",outline="#111111",width=max(4,int(8*scale)))
    d.polygon([(x+int(80*scale),y+int(80*scale)),(x+int(520*scale),y+int(30*scale)),(x+int(640*scale),y+int(180*scale)),(x+int(150*scale),y+int(210*scale))],fill="#E8E8E8")
    # lace area
    for i in range(5):
        yy=y+int((120+i*48)*scale)
        d.line((x+int(240*scale),yy,x+int(530*scale),yy-int(40*scale)),fill="#FFFFFF",width=max(8,int(18*scale)))
        d.ellipse((x+int(210*scale),yy-int(9*scale),x+int(228*scale),yy+int(9*scale)),fill="#BDBDBD")
        d.ellipse((x+int(545*scale),yy-int(45*scale),x+int(563*scale),yy-int(27*scale)),fill="#BDBDBD")
    # tag positioned across laces
    tx=x+int(290*scale); ty=y+int(250*scale); tw=int(260*scale); th=int(78*scale)
    d.rounded_rectangle((tx,ty,tx+tw,ty+th),radius=int(16*scale),fill=charm,outline="#333333",width=max(2,int(4*scale)))
    # two side lace slots
    slotw=int(26*scale)
    d.rounded_rectangle((tx+int(12*scale),ty+int(20*scale),tx+int(12*scale)+slotw,ty+int(58*scale)),radius=6,fill="#F5F5F5")
    d.rounded_rectangle((tx+tw-int(38*scale),ty+int(20*scale),tx+tw-int(12*scale),ty+int(58*scale)),radius=6,fill="#F5F5F5")
    f=font(max(20,int(34*scale)),True)
    center(d,tx+tw/2,ty+th/2,name[:10],f,text)

def loose_tag(d,cx,cy,w=430,h=120,charm="#111111",text="#FFFFFF",name="RODRIGO"):
    d.rounded_rectangle((cx-w//2+8,cy-h//2+10,cx+w//2+8,cy+h//2+10),radius=24,fill=(0,0,0,22))
    d.rounded_rectangle((cx-w//2,cy-h//2,cx+w//2,cy+h//2),radius=24,fill=charm,outline="#333333",width=4)
    d.rounded_rectangle((cx-w//2+18,cy-h//2+30,cx-w//2+54,cy+h//2-30),radius=8,fill="#FFFFFF")
    d.rounded_rectangle((cx+w//2-54,cy-h//2+30,cx+w//2-18,cy+h//2-30),radius=8,fill="#FFFFFF")
    center(d,cx,cy,name[:10],F44,text)

# 01 principal
im=base(); d=ImageDraw.Draw(im,"RGBA"); shoe(d); im.save(OUT/"01-principal.jpg",quality=92,optimize=True)

# 02 chamariz
im=base("#EAF4FF"); d=ImageDraw.Draw(im,"RGBA")
d.rectangle((0,0,1000,250),fill="#08111F")
center(d,500,72,"CHARM DE CADARÇO",F54,"#FFFFFF")
center(d,500,150,"PERSONALIZADO",F54,"#22C55E")
center(d,500,220,"Seu nome no seu estilo",F26,"#FFFFFF")
shoe(d,x=120,y=320,scale=1.0)
im.save(OUT/"02-chamariz.jpg",quality=92,optimize=True)

# 03 personalizacao
im=base(); d=ImageDraw.Draw(im,"RGBA")
center(d,500,65,"COMO PERSONALIZAR",F54,"#111111")
loose_tag(d,260,520,name="RODRIGO")
steps=[("1","Escolha a combinação de cores"),("2","Envie o nome ou número"),("3","Nós produzimos sob encomenda")]
for i,(n,t) in enumerate(steps):
    yy=280+i*210
    d.ellipse((560,yy-45,650,yy+45),fill="#111827")
    center(d,605,yy,n,F34,"white")
    d.rounded_rectangle((680,yy-60,950,yy+60),radius=18,fill="#F3F4F6",outline="#D1D5DB",width=2)
    d.multiline_text((705,yy-30),t,font=F20,fill="#111111",spacing=5)
im.save(OUT/"03-personalizacao.jpg",quality=92,optimize=True)

# 04 cores
im=base(); d=ImageDraw.Draw(im,"RGBA")
center(d,500,55,"9 COMBINAÇÕES DE CORES",F44,"#111111")
for i,(slug,(p,s)) in enumerate(COLORS.items()):
    row=i//3; col=i%3; x=175+col*325; y=220+row*280
    loose_tag(d,x,y,w=250,h=82,charm=p,text=s,name="NOME")
    center(d,x,y+90,slug.replace("-"," + ").title(),F20,"#111111")
im.save(OUT/"04-cores.jpg",quality=92,optimize=True)

# 05 uso
im=base("#DFF1FF"); d=ImageDraw.Draw(im,"RGBA")
center(d,500,70,"DIRETO NO CADARÇO",F54,"#111111")
shoe(d,x=130,y=230,scale=1.0)
d.rounded_rectangle((120,760,880,900),radius=30,fill="#FFFFFF")
center(d,500,805,"Sem argola. Sem cabo.",F34,"#111111")
center(d,500,860,"Dois canais traseiros seguram a peça no cadarço.",F20,"#444444")
im.save(OUT/"05-uso.jpg",quality=92,optimize=True)

# 06 dimensoes
im=base(); d=ImageDraw.Draw(im,"RGBA")
center(d,500,60,"MEDIDAS INICIAIS",F44,"#111111")
loose_tag(d,500,360,w=420,h=125,name="RODRIGO")
d.line((290,520,710,520),fill="#111111",width=4); d.polygon([(290,520),(310,510),(310,530)],fill="#111111"); d.polygon([(710,520),(690,510),(690,530)],fill="#111111")
center(d,500,555,"40 mm",F26,"#111111")
d.line((760,297,760,423),fill="#111111",width=4); d.polygon([(760,297),(750,317),(770,317)],fill="#111111"); d.polygon([(760,423),(750,403),(770,403)],fill="#111111")
d.text((790,345),"12 mm",font=F26,fill="#111111")
center(d,500,690,"Espessura cadastrada: 3 mm",F26,"#111111")
center(d,500,755,"Peso impresso simulado: 1,80 g",F26,"#111111")
center(d,500,820,"Material: PLA • 2 cores por peça",F26,"#111111")
im.save(OUT/"06-dimensoes.jpg",quality=92,optimize=True)

# 07 detalhes
im=base(); d=ImageDraw.Draw(im,"RGBA")
center(d,500,55,"DETALHES DO PRODUTO",F44,"#111111")
loose_tag(d,300,510,w=430,h=120,name="RODRIGO")
details=[("PLA","Leve e econômico"),("2 cores","Uso controlado do AMS"),("2 canais","Passagem direta do cadarço"),("Personalizado","Nome ou número em relevo")]
for i,(a,b) in enumerate(details):
    yy=250+i*170
    d.ellipse((600,yy-38,676,yy+38),fill="#111111")
    center(d,638,yy,str(i+1),F26,"white")
    d.text((710,yy-34),a,font=F26,fill="#111111")
    d.text((710,yy+4),b,font=F20,fill="#4B5563")
im.save(OUT/"07-detalhes.jpg",quality=92,optimize=True)

# 08 kits
im=base("#111827"); d=ImageDraw.Draw(im,"RGBA")
center(d,500,70,"IDEAL PARA GRUPOS",F54,"white")
center(d,500,140,"Times, escolas, eventos e equipes",F26,"#FACC15")
names=["PEDRO","LUCAS","SOFIA","MIGUEL","ANA","JOÃO"]
for i,name in enumerate(names):
    row=i//3; col=i%3; x=190+col*310; y=340+row*280
    slug=list(COLORS.keys())[i]
    p,s=COLORS[slug]
    loose_tag(d,x,y,w=250,h=82,charm=p,text=s,name=name)
center(d,500,900,"Pedidos de 5, 10, 20, 50 e 100 unidades",F26,"white")
im.save(OUT/"08-kits.jpg",quality=92,optimize=True)

# variações
for slug,(p,s) in COLORS.items():
    im=base(); d=ImageDraw.Draw(im,"RGBA")
    loose_tag(d,500,500,w=520,h=145,charm=p,text=s,name="NOME")
    center(d,500,650,slug.replace("-"," + ").title(),F26,"#111111")
    im.save(OUT/f"variacao-{slug}.jpg",quality=92,optimize=True)

print("Galeria e variações SHOE-NAME geradas")
