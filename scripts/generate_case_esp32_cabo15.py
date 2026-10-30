from pathlib import Path
from io import BytesIO
import cairosvg
from PIL import Image
p=Path("imagens/case-esp32-micro-usb-30p-cabo15")
for f in sorted(p.glob("*.svg")):
    png=cairosvg.svg2png(url=str(f),output_width=1000,output_height=1000)
    Image.open(BytesIO(png)).convert("RGB").save(f.with_suffix(".jpg"),quality=90,optimize=True)
    print(f.with_suffix(".jpg"))
