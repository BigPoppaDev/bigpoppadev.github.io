# Builds the pictures and icons for the Large Print Reader page into <out> (default: largeprintreader).
# The two photographs were generated for this page; this script fetches the originals once and saves web-sized copies.
import json, os, sys, urllib.request
from PIL import Image, ImageDraw, ImageFont

out = sys.argv[1] if len(sys.argv) > 1 else "largeprintreader"
os.makedirs(os.path.join(out, "assets"), exist_ok=True)

PHOTOS = {
    "table-reading.jpg": "https://d8j0ntlcm91z4.cloudfront.net/user_3LjhMsZJHZ46qR7tFBXlRXmmOvT/hf_20261118_105708_8525184a-c8cd-4677-af6c-650f70071354.png",
    "headphones.jpg": "https://d8j0ntlcm91z4.cloudfront.net/user_3LjhMsZJHZ46qR7tFBXlRXmmOvT/hf_20261118_105707_f75a1a3b-06d7-46ab-a148-0295ee996bb0.png",
}
for name, url in PHOTOS.items():
    dest = os.path.join(out, "assets", name)
    if os.path.exists(dest):
        continue
    tmp = dest + ".src.png"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=60) as r, open(tmp, "wb") as f:
        f.write(r.read())
    Image.open(tmp).convert("RGB").save(dest, "JPEG", quality=84, optimize=True)
    os.remove(tmp)

def font(bold, size):
    names = ["DejaVuSans-Bold.ttf", "Verdana Bold.ttf", "verdanab.ttf"] if bold else ["DejaVuSans.ttf", "Verdana.ttf", "verdana.ttf"]
    dirs = ["/usr/share/fonts/truetype/dejavu", "/usr/share/fonts/dejavu", "/Library/Fonts", "C:/Windows/Fonts"]
    for d in dirs:
        for n in names:
            p = os.path.join(d, n)
            if os.path.exists(p):
                return ImageFont.truetype(p, size)
    raise SystemExit("No DejaVu or Verdana font found")

ACC = (122, 74, 0); BG = (251, 245, 230); FG = (26, 26, 26)

def tile(size, maskable=False, radius_ratio=0.22):
    s = size * 4
    im = Image.new("RGBA", (s, s), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    if maskable:
        d.rectangle([0, 0, s, s], fill=ACC)
    else:
        d.rounded_rectangle([0, 0, s - 1, s - 1], radius=max(1, int(s * radius_ratio)), fill=ACC)
    f = font(True, int(s * (0.36 if maskable else 0.5)))
    box = d.textbbox((0, 0), "Aa", font=f)
    w, h = box[2] - box[0], box[3] - box[1]
    d.text(((s - w) / 2 - box[0], (s - h) / 2 - box[1]), "Aa", font=f, fill=BG)
    return im.resize((size, size), Image.LANCZOS)

tile(16).save(os.path.join(out, "favicon-16.png"))
tile(32).save(os.path.join(out, "favicon-32.png"))
tile(180, maskable=True).convert("RGB").save(os.path.join(out, "apple-touch-icon.png"))
tile(192).save(os.path.join(out, "icon-192.png"))
tile(512).save(os.path.join(out, "icon-512.png"))
tile(512, maskable=True).convert("RGB").save(os.path.join(out, "icon-maskable-512.png"))

W, H = 1200, 630
card = Image.new("RGB", (W, H), BG)
d = ImageDraw.Draw(card)
d.rectangle([0, H - 18, W, H], fill=ACC)
t = tile(150)
card.paste(t, (80, 90), t)
d.text((80, 285), "Large Print Reader", font=font(True, 92), fill=FG)
d.text((84, 415), "Articles in large print, in one click.", font=font(False, 44), fill=FG)
d.text((84, 485), "A Chrome extension", font=font(False, 44), fill=ACC)
card.save(os.path.join(out, "assets", "og.png"))
print("images built in", out)
