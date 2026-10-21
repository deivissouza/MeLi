from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
import math

OUT = Path("imagens/sport-tag-futebol")
OUT.mkdir(parents=True, exist_ok=True)

def font(size, bold=False):
    paths = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation2/LiberationSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/liberation2/LiberationSans-Regular.ttf",
    ]
    for p in paths:
        if Path(p).exists():
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()

F18=font(18); F22=font(22,True); F28=font(28,True); F34=font(34,True); F42=font(42,True); F52=font(52,True)

def text_center(d, x, y, txt, fnt, fill):
    b=d.textbbox((0,0),txt,font=fnt)
    d.text((x-(b[2]-b[0])/2,y-(b[3]-b[1])/2),txt,font=fnt,fill=fill)

def cable(d,cx,cy,r=95):
    d.ellipse((cx-r,cy-r,cx+r,cy+r),outline="#111111",width=12)
    d.rounded_rectangle((cx+r-35,cy-r+25,cx+r+10,cy-r+65),radius=8,fill="#BDBDBD",outline="#777777",width=2)

def tag(d,cx,cy,r,primary="#111111",secondary="#FFFFFF",name="RODRIGO",num="10",with_cable=True):
    if with_cable: cable(d,cx,cy-r-58,int(r*.67))
    d.ellipse((cx-r+6,cy-r+12,cx+r+10,cy+r+16),fill=(0,0,0,24))
    d.ellipse((cx-r,cy-r,cx+r,cy+r),fill=secondary,outline=primary,width=max(4,int(r*.055)))
    # soccer panels
    angs=[-90,-18,54,126,198]
    for a in angs:
        rad=math.radians(a)
        px=cx+int(r*.68*math.cos(rad)); py=cy+int(r*.68*math.sin(rad))
        rr=int(r*.21)
        d.regular_polygon((px,py,rr),5,rotation=a,fill=primary)
    d.regular_polygon((cx,cy-r+int(r*.25),int(r*.22)),5,rotation=-90,fill=primary)
    # tab
    d.rounded_rectangle((cx-int(r*.20),cy-r-int(r*.18),cx+int(r*.20),cy-r+int(r*.16)),radius=10,fill=primary)
    d.ellipse((cx-8,cy-r-int(r*.06),cx+8,cy-r+int(r*.10)),fill="#FFFFFF")
    # lettering
    nf = font(max(22,int(r*.22)),True); ff=font(max(28,int(r*.32)),True)
    text_center(d,cx,cy-int(r*.05),name,nf,primary)
    text_center(d,cx,cy+int(r*.32),num,ff,primary)

def base(bg="white"):
    return Image.new("RGB",(1000,1000),bg)

# 1 principal
im=base(); d=ImageDraw.Draw(im,"RGBA")
tag(d,500,590,260,name="RODRIGO",num="10")
im.save(OUT/"01-principal.jpg",quality=92,optimize=True)

# 2 chamariz
im=base("#DDF1FF"); d=ImageDraw.Draw(im,"RGBA")
d.rectangle((0,0,1000,300),fill="#08111F")
text_center(d,500,75,"TAG DE FUTEBOL",F52,"#FFFFFF")
text_center(d,500,150,"PERSONALIZADA",F52,"#7CFC00")
text_center(d,500,235,"Nome + número para mochila e bolsa esportiva",F28,"#FFFFFF")
for x,n,nu in [(260,"RODRIGO","10"),(500,"LUCAS","7"),(740,"PEDRO","9")]:
    tag(d,x,650,170,name=n,num=nu)
im.save(OUT/"02-chamariz.jpg",quality=92,optimize=True)

# 3 personalizacao
im=base(); d=ImageDraw.Draw(im,"RGBA")
text_center(d,500,60,"COMO PERSONALIZAR",F52,"#111111")
tag(d,265,550,180,name="RODRIGO",num="10")
steps=[("1","Escolha a cor"),("2","Envie o nome"),("3","Envie o número")]
for i,(n,t) in enumerate(steps):
    y=280+i*190
    d.ellipse((560,y-42,640,y+38),fill="#E11D2E")
    text_center(d,600,y,n,F34,"white")
    d.rounded_rectangle((655,y-55,940,y+55),radius=18,fill="#F4F4F4",outline="#DDDDDD",width=2)
    d.text((690,y-20),t,font=F28,fill="#111111")
im.save(OUT/"03-personalizacao.jpg",quality=92,optimize=True)

# 4 cores
im=base(); d=ImageDraw.Draw(im,"RGBA")
text_center(d,500,55,"CORES DISPONÍVEIS",F52,"#111111")
colors=[
("Preto + Branco","#111111","#FFFFFF"),("Branco + Preto","#F7F7F7","#111111"),("Azul + Branco","#2563EB","#FFFFFF"),
("Vermelho + Branco","#EF4444","#FFFFFF"),("Verde + Branco","#16A34A","#FFFFFF"),("Amarelo + Preto","#FACC15","#111111"),
("Rosa + Branco","#EC4899","#FFFFFF"),("Lilás + Branco","#A855F7","#FFFFFF"),("Laranja + Preto","#F97316","#111111")]
for i,(lab,p,s) in enumerate(colors):
    row=i//3; col=i%3; x=180+col*320; y=260+row*285
    tag(d,x,y,105,primary=p,secondary=s,name="NOME",num="10")
    text_center(d,x,y+155,lab,F18,"#111111")
im.save(OUT/"04-cores.jpg",quality=92,optimize=True)

# 5 uso
im=base("#BFE7FF"); d=ImageDraw.Draw(im,"RGBA")
d.rectangle((520,120,930,880),fill="#151515")
d.rounded_rectangle((590,190,860,780),radius=35,fill="#252525")
tag(d,690,555,175,name="RODRIGO",num="10")
d.text((60,130),"USE NA",font=F52,fill="#111111")
d.text((60,200),"MOCHILA",font=F52,fill="#166534")
d.text((60,270),"OU BOLSA",font=F52,fill="#166534")
d.text((65,365),"Identifique seu material\nesportivo com facilidade",font=F28,fill="#222222")
im.save(OUT/"05-uso.jpg",quality=92,optimize=True)

# 6 conteudo
im=base(); d=ImageDraw.Draw(im,"RGBA")
text_center(d,500,70,"CONTEÚDO DA EMBALAGEM",F42,"#111111")
tag(d,300,515,185,name="RODRIGO",num="10",with_cable=False)
cable(d,720,470,145)
d.ellipse((90,820,135,865),fill="#E11D2E"); text_center(d,112,842,"✓",F28,"white")
d.text((155,815),"1 tag personalizada",font=F28,fill="#111111")
d.ellipse((540,820,585,865),fill="#E11D2E"); text_center(d,562,842,"✓",F28,"white")
d.text((605,815),"1 cabo com rosqueio",font=F28,fill="#111111")
im.save(OUT/"06-conteudo.jpg",quality=92,optimize=True)

# 7 detalhes
im=base(); d=ImageDraw.Draw(im,"RGBA")
text_center(d,500,60,"DETALHES DO PRODUTO",F42,"#111111")
tag(d,300,560,200,name="RODRIGO",num="10")
for y,title,desc in [(260,"Impressão 3D","Nome e número em relevo"),(500,"2 cores por peça","Uso econômico do AMS"),(740,"Leve e resistente","Cabo com fecho de rosca")]:
    d.ellipse((600,y-55,700,y+45),fill="#111111")
    text_center(d,650,y-5,"•",F52,"white")
    d.text((730,y-35),title,font=F28,fill="#111111")
    d.text((730,y+10),desc,font=F18,fill="#444444")
im.save(OUT/"07-detalhes.jpg",quality=92,optimize=True)

# 8 times
im=base("#163A25"); d=ImageDraw.Draw(im,"RGBA")
d.rectangle((0,0,1000,300),fill="#09120D")
text_center(d,500,70,"IDEAL PARA",F52,"white")
text_center(d,500,145,"TIMES E ESCOLINHAS",F52,"#FACC15")
text_center(d,500,230,"Pedidos em quantidade",F28,"white")
for x,n,nu,r in [(150,"LUCAS","7",125),(330,"PEDRO","9",135),(520,"RODRIGO","10",160),(725,"GABRIEL","11",135),(885,"MIGUEL","4",115)]:
    tag(d,x,650,r,name=n,num=nu)
im.save(OUT/"08-times.jpg",quality=92,optimize=True)

print("Galeria SPORT-TAG gerada")

# 9 variacoes individuais
variation_colors = [
    ("preto-branco","#111111","#FFFFFF"),
    ("branco-preto","#F7F7F7","#111111"),
    ("azul-branco","#2563EB","#FFFFFF"),
    ("vermelho-branco","#EF4444","#FFFFFF"),
    ("verde-branco","#16A34A","#FFFFFF"),
    ("amarelo-preto","#FACC15","#111111"),
    ("rosa-branco","#EC4899","#FFFFFF"),
    ("lilas-branco","#A855F7","#FFFFFF"),
    ("laranja-preto","#F97316","#111111"),
]
for slug, primary, secondary in variation_colors:
    im=base(); d=ImageDraw.Draw(im,"RGBA")
    tag(d,500,590,260,primary=primary,secondary=secondary,name="NOME",num="10")
    im.save(OUT/f"variacao-{slug}.jpg",quality=92,optimize=True)

print("Variações individuais SPORT-TAG geradas")

