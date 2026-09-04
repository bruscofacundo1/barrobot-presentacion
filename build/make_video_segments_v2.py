# -*- coding: utf-8 -*-
import subprocess, os

ROOT = r"C:\Users\Facundo\Downloads\barrobot"
SRC_DIR = os.path.join(ROOT, "videos-nuevos")
SEG_DIR = os.path.join(ROOT, "build", "segments")

# (source filename, output name, pre-crop or None)
# pre-crop removes pillarbox/letterbox bars baked in by the user's editing app
CLIPS = [
    ("prueba 2-1.mp4", "n_v1.mp4", None),
    ("prueba 3-1.mp4", "n_v2.mp4", None),
    ("prueba 4-1.mp4", "n_v3.mp4", None),
    ("prueba 5-1.mp4", "n_v4.mp4", "crop=1214:2160:1308:0"),
    ("prueba 6-1.mp4", "n_v5.mp4", "crop=2878:2160:476:0"),
    ("prueba 7-1.mp4", "n_v6.mp4", None),
    ("prueba acelerada-1.mp4", "n_v7.mp4", None),
]

FPS = 30

for src_name, outname, precrop in CLIPS:
    src = os.path.join(SRC_DIR, src_name)
    out = os.path.join(SEG_DIR, outname)
    filters = []
    if precrop:
        filters.append(precrop)
    filters.append("scale=1920:1080:force_original_aspect_ratio=increase")
    filters.append("crop=1920:1080")
    filters.append(f"fps={FPS}")
    filters.append("format=yuv420p")
    vf = ",".join(filters)
    cmd = [
        "ffmpeg", "-y", "-i", src,
        "-vf", vf,
        "-an", "-c:v", "libx264", "-crf", "18", "-preset", "medium",
        out,
    ]
    print("Building", outname, "from", src_name)
    r = subprocess.run(cmd, capture_output=True, text=True)
    print("OK" if r.returncode == 0 else "ERROR:\n" + r.stderr[-1500:])
