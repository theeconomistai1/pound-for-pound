"""Render a video from its folder.

  python3 -I pipeline/make.py <video_dir> events            write <video_dir>/build/events.json
  python3 -I pipeline/make.py <video_dir> stills 0.5,4,12   write preview PNGs to <video_dir>/build/
  python3 -I pipeline/make.py <video_dir> render            write <video_dir>/build/video.mp4

Needs <video_dir>/scenes.py and <video_dir>/build/timings.json (from tts2.py);
render also needs <video_dir>/build/mix.wav.
"""
import importlib.util
import json
import math
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import vidlib as V  # noqa: E402


def load(video_dir):
    V.T = json.load(open(os.path.join(video_dir, "build", "timings.json"), encoding="utf-8"))
    V.T["total"] = V.T["duration"] + 0.6
    spec = importlib.util.spec_from_file_location("scenes", os.path.join(video_dir, "scenes.py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    V.SCENES = mod
    V.SHAKES[:] = list(mod.shakes())
    return mod


def main():
    video_dir, cmd = sys.argv[1], sys.argv[2]
    build = os.path.join(video_dir, "build")
    os.makedirs(build, exist_ok=True)
    mod = load(video_dir)
    if cmd == "events":
        json.dump(mod.events(), open(os.path.join(build, "events.json"), "w"), indent=1)
        print(f"{V.T['total']:.3f}")
    elif cmd == "stills":
        for ts in sys.argv[3].split(","):
            V.frame(float(ts)).save(os.path.join(build, f"still_{float(ts):05.2f}.png"))
    elif cmd == "render":
        out = os.path.join(build, "video.mp4")
        n = int(math.ceil(V.T["total"] * V.FPS))
        ff = subprocess.Popen(
            ["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{V.W}x{V.H}",
             "-r", str(V.FPS), "-i", "-", "-i", os.path.join(build, "mix.wav"), "-c:v", "libx264", "-preset", "medium",
             "-crf", "19", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart", out],
            stdin=subprocess.PIPE)
        for i in range(n):
            ff.stdin.write(V.frame(i / V.FPS).tobytes())
        ff.stdin.close()
        if ff.wait() != 0:
            sys.exit("ffmpeg failed")
        print(out)
    else:
        sys.exit(f"unknown command {cmd}")


if __name__ == "__main__":
    main()
