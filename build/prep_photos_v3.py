# -*- coding: utf-8 -*-
from PIL import Image, ImageOps
import os

ROOT = r"C:\Users\Facundo\Downloads\barrobot"
IMG_DIR = os.path.join(ROOT, "imagenes")
OUT_DIR = os.path.join(ROOT, "build", "photos_fixed")

PHOTOS = [
    ("no - 0.jpeg", "n_no0.jpg"),
    ("no - 3.jpg", "n_no3.jpg"),
    ("no - 7.jpg", "n_no7.jpg"),
    ("no - 8.jpg", "n_no8.jpg"),
]

TARGET_RATIO = 1920 / 1080

for name, outname in PHOTOS:
    path = os.path.join(IMG_DIR, name)
    im = Image.open(path)
    im = ImageOps.exif_transpose(im).convert("RGB")
    w, h = im.size
    cur_ratio = w / h
    if cur_ratio > TARGET_RATIO:
        new_w = int(h * TARGET_RATIO)
        x0 = (w - new_w) // 2
        im = im.crop((x0, 0, x0 + new_w, h))
    else:
        new_h = int(w / TARGET_RATIO)
        y0 = (h - new_h) // 2
        im = im.crop((0, y0, w, y0 + new_h))
    max_w = 2880
    if im.width > max_w:
        new_h2 = int(max_w * im.height / im.width)
        im = im.resize((max_w, new_h2), Image.LANCZOS)
    out_path = os.path.join(OUT_DIR, outname)
    im.save(out_path, quality=92)
    print(f"{name} -> {outname}  {im.size}")
