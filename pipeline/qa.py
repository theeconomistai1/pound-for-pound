"""Brand QA for one Short: script rules, safe zones, cover frame, metadata, and a contact sheet to eyeball.

  python3 -I pipeline/qa.py <video_dir>

Needs <video_dir>/build/timings.json (run the build first, or at least tts2.py). Writes:
  build/thumb.png    frame 0 (the cover frame and loop target)
  build/contact.png  frame 0, the end of every scene, and the loop frame, on one sheet
Prints PASS / WARN / FAIL lines and exits 1 if anything FAILs. Fix every FAIL before publishing.
"""
import json
import os
import re
import sys

import numpy as np
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import motion as Mo  # noqa: E402

SEEN = set()  # every string drawn, for the glyph check
_text_sprite = Mo.text_sprite


def _recording_text_sprite(s, *a, **k):
    SEEN.add(s)
    return _text_sprite(s, *a, **k)


Mo.text_sprite = _recording_text_sprite  # before brand / scenes import it
import brand as Br  # noqa: E402
import make_v3  # noqa: E402

results = []


def report(level, msg):
    results.append(level)
    print(f"{level:4}  {msg}")


def spoken(sentence):
    return re.sub(r"\{[^|}]*\|([^}]*)\}", r"\1", sentence)


def check_script(spec):
    ss = spec["sentences"]
    n = len(ss)
    (report("PASS", f"{n} sentences") if 11 <= n <= 16 else report("WARN", f"{n} sentences (aim for 11-16)"))
    first = ss[0]
    if re.search(r"[£%]|\d", first):
        report("PASS", "hook sentence carries the payoff number")
    else:
        report("FAIL", "sentence 1 must contain the payoff number (the hook)")
    turn = [i for i, s in enumerate(ss) if s.startswith("Your turn")]
    report("PASS", "has a 'Your turn' comment question") if turn else report("FAIL", "no 'Your turn.' sentence")
    if ss[-1].startswith("Send this to"):
        report("PASS", "ends on the share line (loops into the hook)")
    else:
        report("FAIL", "last sentence must start 'Send this to …' (the share line)")
    if not any(re.search(r"illustration|can fall|not financial advice|could change|may get back less", s, re.I)
               for s in ss):
        report("WARN", "no spoken caveat found (needed for anything about investing or risk)")
    long = [i for i, s in enumerate(ss) if len(spoken(s).split()) > 26]
    if long:
        report("WARN", f"long sentences (>26 spoken words): {long}")


def check_timing():
    total = Mo.T["total"]
    first = Mo.T["sentences"][0]["start"]
    (report("PASS", f"length {total:.1f}s") if 40 <= total <= 65 else
     report("WARN", f"length {total:.1f}s (aim for 45-60s; rewrite tighter if over 65s)"))
    (report("PASS", f"voice starts at {first:.2f}s") if first <= 0.35 else
     report("FAIL", f"voice starts late ({first:.2f}s) — the hook must start immediately"))


def check_layout():
    total = Mo.T["total"]
    zones = {
        "above the beat chip (y<255)": (slice(0, 255), slice(0, Mo.W)),
        "bottom overlay (y>1480)": (slice(Br.CLEAR_Y, Mo.H), slice(0, Mo.W)),
        "left edge (x<40)": (slice(0, Mo.H), slice(0, 40)),
        "right edge (x>1040)": (slice(0, Mo.H), slice(1040, Mo.W)),
        "button column (x>975, y>900)": (slice(900, Mo.H), slice(975, Mo.W)),
    }
    hits = {}
    for t in np.arange(0, total, 0.25):
        a = np.asarray(Br._content(float(t)))[..., 3]
        for name, (ys, xs) in zones.items():
            if (a[ys, xs] > 60).sum() > 30:
                hits.setdefault(name, []).append(round(float(t), 2))
        if t % 1.0 < 0.01:
            cap = Mo.Layer()
            Br.captions(cap, float(t), Mo.GROUPS)
            ca = np.asarray(cap.im)[..., 3]
            if (ca[:, :90] > 60).sum() + (ca[:, 990:] > 60).sum() > 30:
                hits.setdefault("captions too wide", []).append(round(float(t), 2))
    if not hits:
        report("PASS", "safe zones clear on every frame checked (every 0.25s)")
    for name, ts in hits.items():
        report("FAIL", f"content in {name} at t={ts[:8]}{' …' if len(ts) > 8 else ''}")
    a0 = np.asarray(Br._content(0.0))[..., 3]
    filled = (a0 > 60).mean()
    (report("PASS", f"frame 0 shows the hook ({filled * 100:.1f}% of the frame)") if filled > 0.02 else
     report("FAIL", "frame 0 is nearly empty — the hook must be fully visible on the first frame"))


def check_glyphs():
    """Characters the font cannot draw render as empty boxes. Every drawn string is checked."""
    try:
        from fontTools.ttLib import TTFont
    except ImportError:
        report("WARN", "fontTools not installed (pip install fonttools) — glyph check skipped; look for boxes")
        return
    cmap = TTFont(Mo.FONT).getBestCmap()
    bad = sorted({ch for s in SEEN for ch in s if ord(ch) not in cmap and not ch.isspace()})
    if bad:
        report("FAIL", f"characters missing from the font (they show as boxes): {bad} — reword or draw them")
    else:
        report("PASS", f"all {len(SEEN)} on-screen strings use characters the font has")


def check_meta(video_dir, spec):
    path = os.path.join(video_dir, "meta.json")
    if not os.path.exists(path):
        report("WARN", "no meta.json yet")
        return
    m = json.load(open(path, encoding="utf-8"))
    title = m.get("title", "")
    (report("PASS", f"title {len(title)} chars") if len(title) <= 100 and title.endswith("#shorts") else
     report("FAIL", "title must be <= 100 characters and end with #shorts"))
    d = m.get("description", "")
    for need in ("General education, not financial advice.", "Music and sound effects: original, made for this channel.",
                 "Your turn", "Send this to"):
        if need not in d:
            report("FAIL", f"description is missing: {need!r}")
    tags = m.get("tags", [])
    (report("PASS", f"{len(tags)} tags") if 6 <= len(tags) <= 10 else report("WARN", f"{len(tags)} tags (aim 6-10)"))
    if not m.get("first_comment"):
        report("WARN", "no first_comment (the share prompt posted as the first comment)")
    shown = set(re.findall(r"£[\d,]+(?:\.\d+)?[KkMm]?|\d+(?:\.\d+)?%", " ".join(
        re.sub(r"\{([^|}]*)\|[^}]*\}", r"\1", s) for s in spec["sentences"])))
    missing = sorted(x.rstrip(".,") for x in shown if x.rstrip(".,") not in d)
    if missing:
        report("WARN", f"numbers said in the video but not in the description: {missing}")


def contact_sheet(video_dir):
    b = os.path.join(video_dir, "build")
    total = Mo.T["total"]
    times = [0.0]
    sc = Mo.SCENE.SCENES
    for k, (a, _) in enumerate(sc):
        start = Mo.S(a)
        end = Mo.S(sc[k + 1][0]) if k + 1 < len(sc) else total - Br.LOOP
        times.append(max(start + 0.5, end - 0.45))
    times.append(total - 0.05)
    make_v3.FRAME(0.0).save(os.path.join(b, "thumb.png"))
    tw, th = 360, 640
    cols = 5
    rows = (len(times) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * tw + (cols + 1) * 12, rows * (th + 40) + 12), (8, 8, 16))
    for i, t in enumerate(times):
        im = make_v3.FRAME(t).resize((tw, th), Image.LANCZOS)
        x, y = 12 + (i % cols) * (tw + 12), 12 + (i // cols) * (th + 40)
        sheet.paste(im, (x, y))
        lab = Mo.text_sprite(f"{t:.1f}s", 22, (200, 200, 220), "ExtraBold")
        sheet.paste(lab, (x, y + th + 2), lab)
    out = os.path.join(b, "contact.png")
    sheet.save(out)
    report("INFO", f"contact sheet: {out} — read it: no clipped or overlapping text, numbers match meta.json")


def main():
    video_dir = sys.argv[1]
    mod = make_v3.load(video_dir)
    if not getattr(mod, "BRAND", False):
        sys.exit("this video does not use the brand kit (BRAND = True)")
    spec = json.load(open(os.path.join(video_dir, "spec.json"), encoding="utf-8"))
    check_script(spec)
    check_timing()
    check_layout()
    check_glyphs()
    check_meta(video_dir, spec)
    contact_sheet(video_dir)
    if "FAIL" in results:
        print("RESULT: FAIL — fix the lines above before publishing")
        sys.exit(1)
    print("RESULT: PASS" + (" (with warnings)" if "WARN" in results else ""))


if __name__ == "__main__":
    main()
