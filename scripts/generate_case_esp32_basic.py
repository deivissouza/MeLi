from pathlib import Path
from io import BytesIO
import cairosvg
from PIL import Image
p=Path("imagens/case-esp32-micro-usb-30p")
for f in sorted(p.glob("*.svg")):
    png=cairosvg.svg2png(url=str(f), output_width=1000, output_height=1000)
    img=Image.open(BytesIO(png)).convert("RGB")
    target=f.with_suffix(".jpg")
    img.save(target,quality=91,optimize=True,subsampling=0)
    print(target)
