# -*- coding: utf-8 -*-
import subprocess, os

ROOT = r"C:\Users\Facundo\Downloads\barrobot"
SEG_DIR = os.path.join(ROOT, "build", "segments")

# (source filename, in_point_sec, span_sec, target_duration_sec, output name)
CLIPS = [
    ("01 - maquina trabajando, buena calidad, buen entorno - probar.mp4", 0, 8, 4.0, "v01.mp4"),
    ("02 - maquina trabajando.mp4", 0, 7, 3.0, "v02.mp4"),
    ("01 - maquina trabajando, buena calidad - probar.mp4", 5, 16, 4.0, "v03.mp4"),
    ("video nuevo acelerado este poner.mp4", 5, 7, 3.5, "v04.mp4"),
    ("video nuevo acelerado buena calidad.mp4", 3, 6, 3.5, "v05.mp4"),
    ("video maquina trabajando que usamos en la web.mp4", 5, 30, 5.0, "v06.mp4"),
    ("video maquina trabajando inicio no comienza muy bien luego mejora.mp4", 10, 22, 4.4, "v07.mp4"),
]

FPS = 30

for src_name, in_pt, span, target, outname in CLIPS:
    src = os.path.join(ROOT, src_name)
    out = os.path.join(SEG_DIR, outname)
    speed = span / target  # setpts factor = 1/speed
    vf = (
        f"scale=1920:1080:force_original_aspect_ratio=increase,"
        f"crop=1920:1080,"
        f"setpts=PTS/{speed:.6f},"
        f"fps={FPS},format=yuv420p"
    )
    cmd = [
        "ffmpeg", "-y",
        "-ss", str(in_pt), "-t", str(span), "-i", src,
        "-vf", vf,
        "-an", "-c:v", "libx264", "-crf", "18", "-preset", "medium",
        out,
    ]
    print("Building", outname, "speed=%.2fx" % speed)
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        print("ERROR", outname)
        print(r.stderr[-2000:])
    else:
        print("OK", outname)
