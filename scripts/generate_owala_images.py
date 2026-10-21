from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

OUT = Path("imagens/owala-name")
OUT.mkdir(parents=True, exist_ok=True)

COLORS = {
    "preto": ("#171717", "#FFFFFF"),
    "branco": ("#F6F6F6", "#111111"),
    "rosa": ("#F48FB1", "#FFFFFF"),
    "lilas": ("#A78BFA", "#FFFFFF"),
    "azul": ("#2563EB", "#FFFFFF"),
    "amarelo": ("#FACC15", "#111111"),
    "vermelho": ("#EF4444", "#FFFFFF"),
    "verde": ("#22C55E", "#FFFFFF"),
    "laranja": ("#F97316", "#111111"),
}

def font(size):
    for p in [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/usr/share/fonts/truetype/liberation2/LiberationSans-Bold.ttf",
    ]:
        if Path(p).exists():
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()

FONT_NAME = font(38)
FONT_SMALL = font(22)
FONT_TITLE = font(36)

def centered(draw, xy, text, fnt, fill):
    box = draw.textbbox((0, 0), text, font=fnt)
    w = box[2] - box[0]
    h = box[3] - box[1]
    draw.text((xy[0] - w/2, xy[1] - h/2 - 2), text, font=fnt, fill=fill)

def draw_bottle(draw, plate_color, text_color):
    # subtle floor shadow
    draw.ellipse((120, 525, 455, 565), fill=(0,0,0,18))
    # bottle body
    draw.rounded_rectangle((155, 155, 405, 525), radius=68, fill="#181818")
    draw.rounded_rectangle((145, 90, 415, 260), radius=75, fill="#1E1E1E")
    # flip cap
    draw.rounded_rectangle((205, 48, 355, 160), radius=50, fill="#111111")
    # hinge details
    draw.ellipse((187, 125, 202, 140), fill="#777777")
    draw.ellipse((358, 125, 373, 140), fill="#777777")
    # installed plate
    draw.pieslice((190, 118, 370, 270), start=0, end=180, fill=plate_color)
    centered(draw, (280, 190), "Nome", FONT_NAME, text_color)

def draw_detached_plate(draw, x, y, plate_color, text_color):
    # shadow
    draw.ellipse((x-12, y+142, x+218, y+175), fill=(0,0,0,20))
    # IMPORTANT: upper fitting tab / aba that encaixa, visible behind front face
    draw.rounded_rectangle((x+45, y, x+175, y+72), radius=16, fill=plate_color)
    # front semicircle-like face
    draw.pieslice((x, y+40, x+220, y+220), start=0, end=180, fill=plate_color)
    # small alignment hole
    draw.ellipse((x+105, y+62, x+115, y+72), fill="#FFFFFF")
    centered(draw, (x+110, y+125), "Nome", FONT_NAME, text_color)

def variation(name, plate_color, text_color):
    im = Image.new("RGB", (600, 600), "white")
    d = ImageDraw.Draw(im, "RGBA")
    draw_bottle(d, plate_color, text_color)
    draw_detached_plate(d, 340, 360, plate_color, text_color)
    centered(d, (300, 575), name.capitalize(), FONT_SMALL, "#222222")
    im.save(OUT / f"variacao-{name}.jpg", quality=92, optimize=True)

def principal():
    im = Image.new("RGB", (600, 600), "white")
    d = ImageDraw.Draw(im, "RGBA")
    draw_bottle(d, COLORS["laranja"][0], COLORS["laranja"][1])
    centered(d, (300, 32), "Plaquinha com Nome Personalizada", FONT_TITLE, "#111111")
    # color samples at bottom-right
    names = list(COLORS.items())
    for i, (name, (c, tc)) in enumerate(names):
        col = i % 3
        row = i // 3
        x = 355 + col * 68
        y = 345 + row * 65
        d.rounded_rectangle((x, y, x+52, y+40), radius=12, fill=c, outline="#DDDDDD")
    centered(d, (445, 555), "9 cores", FONT_SMALL, "#222222")
    im.save(OUT / "01-principal.jpg", quality=92, optimize=True)

principal()
for name, (c, tc) in COLORS.items():
    variation(name, c, tc)

print("Imagens OWA-NAME geradas:", len(COLORS) + 1)
