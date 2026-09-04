# -*- coding: utf-8 -*-
from PIL import Image, ImageDraw, ImageFont, ImageOps
import os

ROOT = r"C:\Users\Facundo\Downloads\barrobot"
FONTS = os.path.join(ROOT, "fonts")
MEDIA = os.path.join(ROOT, "pptx_media", "ppt", "media")
OUT = os.path.join(ROOT, "build", "cards")

W, H = 1920, 1080

# Brand palette
VERDE_BOSQUE = (12, 67, 38)      # 0C4326
VERDE_SALVIA = (141, 167, 132)   # 8DA784
MARRON_TIERRA = (106, 46, 22)    # 6A2E16
MALVA = (157, 122, 115)          # 9D7A73
CREMA = (244, 240, 232)          # F4F0E8
PAPEL = (251, 249, 244)          # FBF9F4
TINTA = (35, 31, 32)             # 231F20

f_archivo_bold = os.path.join(FONTS, "Archivo-ExtraBold.ttf")
f_grotesk_bold = os.path.join(FONTS, "SpaceGrotesk-Bold.ttf")
f_grotesk_med = os.path.join(FONTS, "SpaceGrotesk-Medium.ttf")
f_worksans_reg = os.path.join(FONTS, "WorkSans-Regular.ttf")
f_worksans_semi = os.path.join(FONTS, "WorkSans-SemiBold.ttf")

logo_white = Image.open(os.path.join(MEDIA, "image-1-2.png")).convert("RGBA")   # negativa blanco
logo_color = Image.open(os.path.join(MEDIA, "image-9-1.png")).convert("RGBA")   # positiva full color


def centered_text(draw, cx, y, text, font, fill, tracking=0):
    if tracking:
        # manual letter spacing
        widths = [draw.textbbox((0, 0), ch, font=font)[2] for ch in text]
        total = sum(widths) + tracking * (len(text) - 1)
        x = cx - total / 2
        for ch, w in zip(text, widths):
            draw.text((x, y), ch, font=font, fill=fill)
            x += w + tracking
        return
    bbox = draw.textbbox((0, 0), text, font=font)
    w = bbox[2] - bbox[0]
    draw.text((cx - w / 2, y), text, font=font, fill=fill)


def paste_centered(base, img, cx, cy):
    x = int(cx - img.width / 2)
    y = int(cy - img.height / 2)
    base.paste(img, (x, y), img)


# ---------------------------------------------------------------
# INTRO CARD
# ---------------------------------------------------------------
img = Image.new("RGB", (W, H), VERDE_BOSQUE)
draw = ImageDraw.Draw(img)

# subtle "estratos" texture band at the bottom - thin horizontal sediment lines
import random
random.seed(7)
band_top = int(H * 0.72)
for i, y in enumerate(range(band_top, H, 10)):
    shade = VERDE_SALVIA if i % 3 else MARRON_TIERRA
    alpha_layer = Image.new("RGBA", (W, 6), shade + (18,))
    jitter = random.randint(-2, 2)
    img.paste(Image.alpha_composite(Image.new("RGBA", (W, 6), VERDE_BOSQUE + (255,)), alpha_layer).convert("RGB"), (0, y + jitter))

logo_w = int(W * 0.40)
logo_h = int(logo_w * logo_white.height / logo_white.width)
logo_resized = logo_white.resize((logo_w, logo_h), Image.LANCZOS)
paste_centered(img, logo_resized, W / 2, H * 0.42)

font_sub = ImageFont.truetype(f_grotesk_med, 36)

centered_text(draw, W / 2, H * 0.42 + logo_h / 2 + 56, "Impresión 3D con tierra local", font_sub, CREMA, tracking=2)

img.save(os.path.join(OUT, "intro.png"))
print("intro.png saved")

# ---------------------------------------------------------------
# OUTRO CARD
# ---------------------------------------------------------------
img2 = Image.new("RGB", (W, H), CREMA)
draw2 = ImageDraw.Draw(img2)

# thin top/bottom rule in verde bosque for structure
draw2.rectangle([0, 0, W, 10], fill=VERDE_BOSQUE)
draw2.rectangle([0, H - 10, W, H], fill=VERDE_BOSQUE)

logo_w2 = int(W * 0.30)
logo_h2 = int(logo_w2 * logo_color.height / logo_color.width)
logo_resized2 = logo_color.resize((logo_w2, logo_h2), Image.LANCZOS)
paste_centered(img2, logo_resized2, W / 2, H * 0.17)

font_headline = ImageFont.truetype(f_archivo_bold, 52)
headline = "Imprimimos tierra,\nconstruimos futuro."
lines = headline.split("\n")
ly = H * 0.30
for line in lines:
    centered_text(draw2, W / 2, ly, line, font_headline, VERDE_BOSQUE)
    ly += 64

# QR block
qr = Image.open(os.path.join(ROOT, "45947afc-7156-4d09-a505-8721f41b88a0.jpg")).convert("RGB")
qr_size = 340
qr_resized = qr.resize((qr_size, qr_size), Image.LANCZOS)
qr_cx, qr_cy = W / 2, H * 0.66

# frame around qr
pad = 22
frame = Image.new("RGB", (qr_size + pad * 2, qr_size + pad * 2), PAPEL)
fdraw = ImageDraw.Draw(frame)
fdraw.rectangle([0, 0, frame.width - 1, frame.height - 1], outline=VERDE_BOSQUE, width=4)
frame.paste(qr_resized, (pad, pad))
img2.paste(frame, (int(qr_cx - frame.width / 2), int(qr_cy - frame.height / 2)))

font_label = ImageFont.truetype(f_grotesk_med, 34)
font_web = ImageFont.truetype(f_worksans_semi, 36)
font_ig = ImageFont.truetype(f_worksans_reg, 28)

centered_text(draw2, W / 2, qr_cy - frame.height / 2 - 58, "ESCANEÁ Y CONOCÉ MÁS", font_label, MARRON_TIERRA, tracking=4)
centered_text(draw2, W / 2, qr_cy + frame.height / 2 + 30, "barrobot3d.com", font_web, VERDE_BOSQUE)
centered_text(draw2, W / 2, qr_cy + frame.height / 2 + 78, "@barrobot3d", font_ig, MALVA)

img2.save(os.path.join(OUT, "outro.png"))
print("outro.png saved")
