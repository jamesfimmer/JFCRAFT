from pathlib import Path
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
png = ROOT / 'assets' / 'jfcraft-logo.png'
if png.is_file():
    source = Image.open(png).convert('RGBA')
    side = max(source.size)
    image = Image.new('RGBA', (side, side), (0, 0, 0, 0))
    image.alpha_composite(source, ((side-source.width)//2, (side-source.height)//2))
else:
    image = Image.new('RGBA', (256, 256), '#111917')
draw = ImageDraw.Draw(image) if not png.is_file() else None
gold, teal = '#d5b775', '#6c9380'
if draw:
 draw.rounded_rectangle((4, 4, 252, 252), radius=48, outline=gold, width=6)
if draw:
 draw.polygon([(72, 48), (184, 48), (184, 82), (146, 82), (146, 161),
              (134, 194), (105, 210), (76, 201), (50, 182), (74, 156),
              (94, 169), (108, 164), (108, 82), (72, 82)], fill=gold)
 draw.polygon([(165, 48), (195, 48), (224, 100), (195, 152), (165, 152),
              (193, 100)], fill=teal)
 draw.polygon([(184, 152), (214, 152), (195, 188), (165, 188)], fill=gold)
image.save(ROOT / 'assets' / 'jfcraft.ico', format='ICO', sizes=[(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)])
print(ROOT / 'assets' / 'jfcraft.ico')
