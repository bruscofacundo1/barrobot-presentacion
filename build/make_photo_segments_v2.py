# -*- coding: utf-8 -*-
import subprocess, os

ROOT = r"C:\Users\Facundo\Downloads\barrobot"
PHOTOS_DIR = os.path.join(ROOT, "build", "photos_fixed")
SEG_DIR = os.path.join(ROOT, "build", "segments")

PHOTO_SEGMENTS = [
    ("n_si_0.jpg", "n_p0.mp4", 1.8),
    ("n_si_1.jpg", "n_p1.mp4", 1.8),
    ("n_si_2.jpg", "n_p2.mp4", 1.8),
    ("n_si_3.jpg", "n_p3.mp4", 1.8),
    ("n_si_4.jpg", "n_p4.mp4", 1.8),
    ("n_si_5.jpg", "n_p5.mp4", 1.8),
    ("n_si_6.jpg", "n_p6.mp4", 1.8),
    ("n_si_7.jpg", "n_p7.mp4", 1.8),
    ("n_si_8_b.jpg", "n_p8.mp4", 1.8),
    ("n_si_9.jpg", "n_p9.mp4", 1.8),
]

FPS = 30

for fname, outname, dur in PHOTO_SEGMENTS:
    src = os.path.join(PHOTOS_DIR, fname)
    out = os.path.join(SEG_DIR, outname)
    frames = int(dur * FPS)
    zexpr = "min(zoom+0.0022,1.13)"
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
    print("OK" if r.returncode == 0 else "ERROR:\n" + r.stderr[-1500:])
