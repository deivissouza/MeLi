from PIL import Image, ImageOps
from pathlib import Path

folder = Path("imagens/colar-coracao-personalizado-v2")
src = Image.open(folder / "01-principal.jpg").convert("RGB")
w, h = src.size
half_w, half_h = w//2, h//2
# Recorta os quatro quadrantes da montagem já aprovada, sem criar novos desenhos.
variants = [
 ("variacao-prata-1f.jpg", (0, 0, half_w, half_h)),
 ("variacao-prata-2f.jpg", (half_w, 0, w, half_h)),
 ("variacao-dourado-1f.jpg", (0, half_h, half_w, h)),
 ("variacao-dourado-2f.jpg", (half_w, half_h, w, h)),
]
for name, bounds in variants:
    image = src.crop(bounds)
    image = image.resize((1200, 1200), Image.Resampling.LANCZOS)
    image.save(folder/name, quality=92, optimize=True, subsampling=0)
    print(name, image.size)
