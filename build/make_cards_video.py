# -*- coding: utf-8 -*-
import subprocess, os

ROOT = r"C:\Users\Facundo\Downloads\barrobot"
CARDS = os.path.join(ROOT, "build", "cards")
SEG_DIR = os.path.join(ROOT, "build", "segments")

FPS = 30

# Intro: 3.0s, fade in from black over 0.5s
intro_dur = 3.0
cmd = [
    "ffmpeg", "-y", "-loop", "1", "-i", os.path.join(CARDS, "intro.png"),
    "-vf", f"fps={FPS},format=yuv420p,fade=t=in:st=0:d=0.5",
    "-t", str(intro_dur),
    "-c:v", "libx264", "-crf", "18", "-preset", "medium", "-an",
    os.path.join(SEG_DIR, "intro.mp4"),
]
r = subprocess.run(cmd, capture_output=True, text=True)
print("intro", "OK" if r.returncode == 0 else r.stderr[-1500:])

# Outro: 5.0s, fade in 0.4s at start, fade out 0.6s at end (loop-friendly)
outro_dur = 5.0
cmd = [
    "ffmpeg", "-y", "-loop", "1", "-i", os.path.join(CARDS, "outro.png"),
    "-vf", f"fps={FPS},format=yuv420p,fade=t=in:st=0:d=0.4,fade=t=out:st={outro_dur-0.6}:d=0.6",
    "-t", str(outro_dur),
    "-c:v", "libx264", "-crf", "18", "-preset", "medium", "-an",
    os.path.join(SEG_DIR, "outro.mp4"),
]
r = subprocess.run(cmd, capture_output=True, text=True)
print("outro", "OK" if r.returncode == 0 else r.stderr[-1500:])
