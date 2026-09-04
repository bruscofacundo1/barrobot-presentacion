# -*- coding: utf-8 -*-
from PIL import Image, ImageOps
import os

ROOT = r"C:\Users\Facundo\Downloads\barrobot"
IMG_DIR = os.path.join(ROOT, "imagenes")
OUT_DIR = os.path.join(ROOT, "build", "photos_fixed")

PHOTOS = [
    "01 - estructura inicial ya con barro fase 1.jpeg",
    "01 - estructura levantada - buena calidad - fase 3.jpg",
    "02 - agustin trabajando.jpg",
    "video nuevo acelerado buena calidad.mp4",  # placeholder removed below
]

PHOTOS = [
    "01 - estructura inicial ya con barro fase 1.jpeg",
    "01 - estructura levantada - buena calidad - fase 3.jpg",
    "02 - agustin trabajando.jpg",
    "04 - barro calidad buena.jpg",
    "01 - estructura + fondo - me gusta.jpg",
]

TARGET_RATIO = 1920 / 1080

for name in PHOTOS:
    path = os.path.join(IMG_DIR, name)
    im = Image.open(path)
    im = ImageOps.exif_transpose(im)  # fix rotation from EXIF
    im = im.convert("RGB")
    w, h = im.size
    cur_ratio = w / h
    if cur_ratio > TARGET_RATIO:
        # too wide -> crop sides
        new_w = int(h * TARGET_RATIO)
        x0 = (w - new_w) // 2
        im = im.crop((x0, 0, x0 + new_w, h))
    else:
        # too tall -> crop top/bottom
        new_h = int(w / TARGET_RATIO)
        y0 = (h - new_h) // 2
        im = im.crop((0, y0, w, y0 + new_h))
    # cap resolution for zoom headroom but keep decent size
    max_w = 2880
    if im.width > max_w:
        new_h2 = int(max_w * im.height / im.width)
        im = im.resize((max_w, new_h2), Image.LANCZOS)
    out_name = os.path.splitext(name)[0].replace(" ", "_") + ".jpg"
    out_path = os.path.join(OUT_DIR, out_name)
    im.save(out_path, quality=92)
    print(f"{name} -> {out_name}  {im.size}")
