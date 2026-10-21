from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

OUT = Path("imagens/bottle-tag")
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

def cable(d,cx,cy,r=90,color="#111111"):
    d.ellipse((cx-r,cy-r,cx+r,cy+r),outline=color,width=14)
    d.rounded_rectangle((cx+r-28,cy-r+16,cx+r+12,cy-r+55),radius=7,fill=color)

def tag(d,cx,cy,w=220,h=560,primary="#EC4899",secondary="#FFFFFF",name="ANA",symbol="♥",with_cable=True):
    if with_cable:
        cable(d,cx,cy-h//2-95,95,primary)
    d.rounded_rectangle((cx-w//2+8,cy-h//2+10,cx+w//2+8,cy+h//2+10),radius=28,fill=(0,0,0,20))
    d.rounded_rectangle((cx-w//2,cy-h//2,cx+w//2,cy+h//2),radius=28,fill=primary,outline=secondary,width=8)
    # top loop
    d.rounded_rectangle((cx-40,cy-h//2-30,cx+40,cy-h//2+35),radius=18,fill=primary,outline=secondary,width=6)
    # vertical name
    f=font(50,True)
    # rotate text image for consistent output
    txt=Image.new("RGBA",(h-120,90),(0,0,0,0)); td=ImageDraw.Draw(txt)
    b=td.textbbox((0,0),name,font=f); td.text(((txt.width-(b[2]-b[0]))/2,10),name,font=f,fill=secondary)
    rot=txt.rotate(90,expand=True)
    im.paste(rot,(int(cx-rot.width/2),int(cy-rot.height/2)),rot)
    sf=font(42,True)
    center(d,cx,cy+h//2-72,symbol,sf,secondary)

# 01 principal
im=base("#FFF7FB"); d=ImageDraw.Draw(im,"RGBA")
# bottle
d.rounded_rectangle((170,120,720,900),radius=90,fill="#F7B6D2",outline="#D18AA8",width=8)
d.rounded_rectangle((230,60,660,200),radius=45,fill="#F3A2C3",outline="#D18AA8",width=6)
tag(d,610,540,220,500,name="ANA",symbol="♥")
im.save(OUT/"01-principal.jpg",quality=92,optimize=True)

# 02 chamariz
im=base("#EEF6FF"); d=ImageDraw.Draw(im,"RGBA")
d.rectangle((0,0,1000,245),fill="#0B1B34")
center(d,500,72,"BOTTLE-TAG",F54,"#FFFFFF")
center(d,500,145,"TAG PERSONALIZADA",F54,"#22C55E")
center(d,500,212,"Para garrafa, mochila, bolsa ou mala",F26,"#FFFFFF")
for x,n,c in [(220,"ANA","#EC4899"),(500,"PEDRO","#2563EB"),(780,"LUCAS","#111111")]:
    tag(d,x,640,150,360,primary=c,name=n,symbol="★")
im.save(OUT/"02-chamariz.jpg",quality=92,optimize=True)

# 03 personalizacao
im=base(); d=ImageDraw.Draw(im,"RGBA")
center(d,500,60,"COMO PERSONALIZAR",F54,"#111111")
tag(d,260,560,150,360,name="ANA",symbol="♥")
steps=[("1","Escolha a combinação de cores"),("2","Envie o nome ou iniciais"),("3","Escolha um símbolo opcional")]
for i,(n,t) in enumerate(steps):
    yy=280+i*210
    d.ellipse((560,yy-45,650,yy+45),fill="#0B1B34")
    center(d,605,yy,n,F34,"white")
    d.rounded_rectangle((680,yy-60,950,yy+60),radius=18,fill="#F4F4F5",outline="#D4D4D8",width=2)
    d.multiline_text((705,yy-28),t,font=F20,fill="#111111",spacing=5)
im.save(OUT/"03-personalizacao.jpg",quality=92,optimize=True)

# 04 cores
im=base(); d=ImageDraw.Draw(im,"RGBA")
center(d,500,55,"9 COMBINAÇÕES DE CORES",F44,"#111111")
for i,(slug,(p,s)) in enumerate(COLORS.items()):
    row=i//3; col=i%3; x=175+col*325; y=230+row*275
    tag(d,x,y,115,235,primary=p,secondary=s,name="NOME",symbol="♥",with_cable=False)
    center(d,x,y+165,slug.replace("-"," + ").title(),F20,"#111111")
im.save(OUT/"04-cores.jpg",quality=92,optimize=True)

# 05 usos
im=base("#F7FAFC"); d=ImageDraw.Draw(im,"RGBA")
center(d,500,55,"USE ONDE QUISER",F54,"#111111")
labels=[("Garrafa",180,"#EC4899"),("Mochila",410,"#111111"),("Bolsa",640,"#EC4899"),("Mala",850,"#2563EB")]
for lab,x,c in labels:
    d.rounded_rectangle((x-100,210,x+100,790),radius=40,fill="#E5E7EB",outline="#CBD5E1",width=4)
    tag(d,x,520,100,250,primary=c,name=lab[:5].upper(),symbol="★")
    center(d,x,855,lab,F26,"#111111")
im.save(OUT/"05-usos.jpg",quality=92,optimize=True)

# 06 dimensoes
im=base(); d=ImageDraw.Draw(im,"RGBA")
center(d,500,55,"MEDIDAS INICIAIS",F44,"#111111")
tag(d,420,500,170,430,name="ANA",symbol="♥")
d.line((620,285,620,715),fill="#111111",width=4)
center(d,690,500,"70 mm",F26,"#111111")
d.line((335,780,505,780),fill="#111111",width=4)
center(d,420,820,"20 mm",F26,"#111111")
center(d,500,900,"Espessura cadastrada: 8 mm",F26,"#111111")
im.save(OUT/"06-dimensoes.jpg",quality=92,optimize=True)

# 07 detalhes
im=base(); d=ImageDraw.Draw(im,"RGBA")
center(d,500,55,"DETALHES DO PRODUTO",F44,"#111111")
tag(d,300,530,160,380,name="ANA",symbol="♥")
details=[("PLA","Leve e resistente"),("2 cores","Nome em alto-relevo"),("Cabo com rosca","Fecho simples e seguro"),("Personalização","Nome, iniciais ou símbolo")]
for i,(a,b) in enumerate(details):
    yy=250+i*170
    d.ellipse((600,yy-38,676,yy+38),fill="#111111")
    center(d,638,yy,str(i+1),F26,"white")
    d.text((710,yy-34),a,font=F26,fill="#111111")
    d.text((710,yy+4),b,font=F20,fill="#4B5563")
im.save(OUT/"07-detalhes.jpg",quality=92,optimize=True)

# 08 kits
im=base("#0F172A"); d=ImageDraw.Draw(im,"RGBA")
center(d,500,70,"IDEAL PARA KITS",F54,"white")
center(d,500,140,"Escolas, empresas, viagens, times e presentes",F26,"#FACC15")
names=["ANA","PEDRO","SOFIA","LUCAS","BIA","MIGUEL"]
color_keys=list(COLORS.keys())
for i,name in enumerate(names):
    row=i//3; col=i%3; x=190+col*310; y=360+row*280
    p,s=COLORS[color_keys[i]]
    tag(d,x,y,105,245,primary=p,secondary=s,name=name,symbol="★",with_cable=False)
center(d,500,900,"Pedidos de 5, 10, 20, 50 e 100 unidades",F26,"white")
im.save(OUT/"08-kits.jpg",quality=92,optimize=True)

# variações
for slug,(p,s) in COLORS.items():
    im=base(); d=ImageDraw.Draw(im,"RGBA")
    tag(d,500,500,220,520,primary=p,secondary=s,name="NOME",symbol="♥")
    center(d,500,835,slug.replace("-"," + ").title(),F26,"#111111")
    im.save(OUT/f"variacao-{slug}.jpg",quality=92,optimize=True)

print("Galeria e variações BOTTLE-TAG geradas")
