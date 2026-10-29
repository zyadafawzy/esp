"""يحوّل كل الصور اللي في فولدر images/ لمقاس الشاشة (320x240) ويطلع src/images_data.h
الترتيب بالاسم: 01.jpg ثم 02.jpg ... الصورة بتتقص من النص عشان تملا الشاشة."""
import glob, os, sys
from PIL import Image

W, H = 320, 240
root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
files = sorted(
    f for ext in ("jpg", "jpeg", "png", "webp")
    for f in glob.glob(os.path.join(root, "images", f"*.{ext}"))
)
if not files:
    sys.exit("مفيش صور في فولدر images/")

def cover(im):
    r = max(W / im.width, H / im.height)
    im = im.resize((round(im.width * r), round(im.height * r)), Image.LANCZOS)
    l, t = (im.width - W) // 2, (im.height - H) // 2
    return im.crop((l, t, l + W, t + H))

out = ["// ملف متولّد تلقائياً - متعدّلوش بإيدك", "#pragma once", "#include <Arduino.h>",
       f"#define IMG_W {W}", f"#define IMG_H {H}"]
names = []
for i, f in enumerate(files):
    im = cover(Image.open(f).convert("RGB"))
    px = []
    for r, g, b in im.getdata():
        px.append("0x%04X" % (((r & 0xF8) << 8) | ((g & 0xFC) << 3) | (b >> 3)))
    out.append(f"// {os.path.basename(f)}")
    out.append(f"const uint16_t img{i}[{W*H}] PROGMEM = {{")
    for k in range(0, len(px), 16):
        out.append(",".join(px[k:k+16]) + ",")
    out.append("};")
    names.append(f"img{i}")
out.append(f"#define IMAGE_COUNT {len(names)}")
out.append("const uint16_t* const IMAGES[IMAGE_COUNT] = {" + ",".join(names) + "};")
with open(os.path.join(root, "src", "images_data.h"), "w") as fh:
    fh.write("\n".join(out) + "\n")
print(f"تمام: {len(files)} صورة")
