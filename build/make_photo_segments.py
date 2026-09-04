# -*- coding: utf-8 -*-
import subprocess, os

ROOT = r"C:\Users\Facundo\Downloads\barrobot"
PHOTOS_DIR = os.path.join(ROOT, "build", "photos_fixed")
SEG_DIR = os.path.join(ROOT, "build", "segments")

# (filename, output segment name, duration seconds, zoom direction: 'in' or 'out')
PHOTO_SEGMENTS = [
    ("01_-_estructura_inicial_ya_con_barro_fase_1.jpg", "p01.mp4", 1.8, "in"),
    ("01_-_estructura_levantada_-_buena_calidad_-_fase_3.jpg", "p02.mp4", 1.8, "in"),
    ("02_-_agustin_trabajando.jpg", "p03.mp4", 1.8, "in"),
    ("04_-_barro_calidad_buena.jpg", "p04.mp4", 1.8, "in"),
    ("01_-_estructura_+_fondo_-_me_gusta.jpg", "p05.mp4", 1.8, "in"),
]

FPS = 30

for fname, outname, dur, direction in PHOTO_SEGMENTS:
    src = os.path.join(PHOTOS_DIR, fname)
    out = os.path.join(SEG_DIR, outname)
    frames = int(dur * FPS)
    if direction == "in":
        zexpr = "min(zoom+0.0022,1.13)"
    else:
        zexpr = "if(eq(on,1),1.13,max(zoom-0.0022,1.0))"
    vf = (
        f"scale=3200:-2,"
        f"zoompan=z='{zexpr}':d={frames}:s=1920x1080:fps={FPS}:"
        f"x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)',"
        f"format=yuv420p"
    )
    cmd = [
        "ffmpeg", "-y", "-loop", "1", "-i", src,
        "-vf", vf, "-t", str(dur),
        "-c:v", "libx264", "-crf", "18", "-preset", "medium", "-an",
        out,
    ]
    print("Building", outname)
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        print("ERROR", outname)
        print(r.stderr[-2000:])
    else:
        print("OK", outname)
