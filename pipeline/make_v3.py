"""Render a house-style video (motion.py) from its folder.

  python3 -I pipeline/make_v3.py <video_dir> events            write <video_dir>/build/events.json, print length
  python3 -I pipeline/make_v3.py <video_dir> stills 0.5,4,12   write preview PNGs to <video_dir>/build/
  python3 -I pipeline/make_v3.py <video_dir> cover             write <video_dir>/build/cover.png + cover.jpg (frame 0)
  python3 -I pipeline/make_v3.py <video_dir> render            write <video_dir>/build/video.mp4

<video_dir>/scenes.py must define:
  SCENES  list of (first_sentence, last_sentence) per scene, in order
  DRAW    list of functions draw(L, t), one per scene
  events()  list of {"t": seconds, "kind": "whoosh"|"pop"|"coin"|"boom"|"crash"}
and may set BADGE / TITLE for the top bar. It does `from motion import *`.
With `BRAND = True` (and `from brand import *`) it renders with the brand kit: pipeline/brand.py, BRAND.md.
"""
import importlib.util
import json
import math
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import motion as Mo  # noqa: E402


def load(video_dir):
    num = os.path.basename(os.path.normpath(video_dir)).split("-")[0]
    spec_theme = json.load(open(os.path.join(video_dir, "spec.json"), encoding="utf-8")).get("theme")
    import brand as Br
    src = open(os.path.join(video_dir, "scenes.py"), encoding="utf-8").read()
    is_brand = re.search(r"^BRAND\s*=\s*True", src, re.M) is not None
    # daily palette for brand videos: spec.json "theme" wins, else rotate by video number; older videos: classic
    if is_brand and (spec_theme or num.isdigit()):
        Br.set_theme(spec_theme or Br.theme_for(num))
    else:
        Br.set_theme("classic")
    Mo.T = json.load(open(os.path.join(video_dir, "build", "timings.json"), encoding="utf-8"))
    Mo.T["total"] = Mo.T["duration"] + 0.8
    Mo.GROUPS = Mo.caption_groups(Mo.T)
    spec = importlib.util.spec_from_file_location("scenes", os.path.join(video_dir, "scenes.py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    Mo.SCENE = mod
    global FRAME
    if getattr(mod, "BRAND", False):  # brand kit (pipeline/brand.py): locked frame, captions, cover and loop
        Br.EPISODE = num if num.isdigit() else None
        FRAME = Br.frame
    else:
        FRAME = Mo.frame
    return mod


FRAME = None


def main():
    video_dir, cmd = sys.argv[1], sys.argv[2]
    b = os.path.join(video_dir, "build")
    os.makedirs(b, exist_ok=True)
    mod = load(video_dir)
    if cmd == "events":
        json.dump(mod.events(), open(os.path.join(b, "events.json"), "w"), indent=1)
        print(f"{Mo.T['total']:.3f}")
    elif cmd == "stills":
        for ts in sys.argv[3].split(","):
            FRAME(float(ts)).save(os.path.join(b, f"still_{float(ts):05.2f}.png"))
    elif cmd in ("thumb", "cover"):  # frame 0 = the cover (and the loop target for brand videos)
        im = FRAME(0.0)
        im.save(os.path.join(b, "cover.png"))
        im.save(os.path.join(b, "cover.jpg"), quality=92)
        print(os.path.join(b, "cover.png"))
    elif cmd == "render":
        out = os.path.join(b, "video.mp4")
        n = int(math.ceil(Mo.T["total"] * Mo.FPS))
        ff = subprocess.Popen(
            ["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{Mo.W}x{Mo.H}",
             "-r", str(Mo.FPS), "-i", "-", "-i", os.path.join(b, "mix.wav"), "-c:v", "libx264", "-preset", "medium",
             "-crf", "18", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart",
             out], stdin=subprocess.PIPE)
        for i in range(n):
            ff.stdin.write(FRAME(i / Mo.FPS).tobytes())
        ff.stdin.close()
        if ff.wait() != 0:
            sys.exit("ffmpeg failed")
        print(out)
    else:
        sys.exit(f"unknown command {cmd}")


if __name__ == "__main__":
    main()
