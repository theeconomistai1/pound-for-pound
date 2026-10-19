"""Shared drawing toolkit for Pound for Pound Shorts (1080x1920, 30 fps).

A video's scenes.py does `from vidlib import *` and `import vidlib as V`, and defines:
  draw(L, d, t, si, st)  draw sentence si's scene onto layer L (d = ImageDraw on L)
  events()               list of {"t": seconds, "kind": whoosh|pop|coin|boom|crash}
  shakes()               list of times for a screen shake
  NO_PUNCH               set of sentence indexes that skip the zoom punch-in
V.T holds the timings from tts2.py once make.py has loaded them.
"""
import math

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

W, H, FPS = 1080, 1920, 30
WHITE = (255, 255, 255)
SOFT = (214, 216, 240)
MUTED = (150, 154, 196)
YELLOW = (255, 210, 63)
GROWTH = (26, 168, 101)     # validated pair on the dark surface
PAID = (238, 85, 36)
INK = (12, 14, 34)
TOP, BOTTOM = np.array([11, 16, 48]), np.array([36, 16, 79])
import os
FD = os.environ.get("P4P_FONTS", "/usr/share/fonts/opentype/inter/")
if not FD.endswith("/"):
    FD += "/"
_f = {}


def font(weight, size):
    size = max(8, int(size))
    if (weight, size) not in _f:
        _f[(weight, size)] = ImageFont.truetype(f"{FD}Inter-{weight}.otf", size)
    return _f[(weight, size)]



def money(v):
    return f"£{v:,.0f}"


def ease(x):
    x = max(0.0, min(1.0, x))
    return 1 - (1 - x) ** 3


def back(x, s=1.9):  # overshoot ease for pops
    x = max(0.0, min(1.0, x)) - 1
    return 1 + (s + 1) * x ** 3 + s * x ** 2


# ---- timings -------------------------------------------------------------------
T = None


def tok(si, ti):
    return T["sentences"][si]["tokens"][ti]


def find_tok(si, text):
    for tk in T["sentences"][si]["tokens"]:
        if tk["text"].startswith(text):
            return tk
    raise KeyError(text)


# ---- background ----------------------------------------------------------------
_grid = None


def background(t):
    global _grid
    w, h = 135, 240
    if _grid is None:
        yy, xx = np.mgrid[0:h, 0:w]
        _grid = (xx / w, yy / h)
    gx, gy = _grid
    base = TOP[None, None, :] * (1 - gy[..., None]) + BOTTOM[None, None, :] * gy[..., None]
    out = base.astype(np.float64)
    blobs = [((0, 200, 255), 0.28, 0.30 + 0.18 * math.sin(t * 0.35), 0.25 + 0.08 * math.cos(t * 0.27), 0.38),
             ((255, 60, 170), 0.22, 0.72 + 0.15 * math.cos(t * 0.31), 0.70 + 0.10 * math.sin(t * 0.23), 0.42),
             ((255, 200, 60), 0.10, 0.55 + 0.25 * math.sin(t * 0.19), 0.48 + 0.2 * math.cos(t * 0.17), 0.30)]
    for col, a, cx, cy, r in blobs:
        d2 = ((gx - cx) / r) ** 2 + ((gy - cy) / (r * 0.6)) ** 2
        k = a * np.exp(-d2 * 2.2)
        out = out * (1 - k[..., None]) + np.array(col)[None, None, :] * k[..., None]
    vig = 1 - 0.35 * (((gx - 0.5) / 0.75) ** 2 + ((gy - 0.5) / 0.9) ** 2)
    out *= np.clip(vig, 0.55, 1)[..., None]
    img = Image.fromarray(np.clip(out, 0, 255).astype(np.uint8), "RGB").resize((W, H), Image.BICUBIC)
    return img.convert("RGBA")


# ---- drawing helpers -------------------------------------------------------------
def text_w(s, f):
    return f.getlength(s)


def centered(d, cy, s, f, fill, cx=W // 2, stroke=0, stroke_fill=INK):
    bb = f.getbbox(s)
    x = cx - (bb[2] - bb[0]) / 2 - bb[0]
    y = cy - (bb[3] - bb[1]) / 2 - bb[1]
    d.text((x, y), s, font=f, fill=fill, stroke_width=stroke, stroke_fill=stroke_fill)


def glow_text(layer, cy, s, f, fill, glow=YELLOW, radius=22, strength=2, cx=W // 2, scale=1.0):
    if scale != 1.0:
        f = font(f.path.rsplit("Inter-", 1)[1][:-4], f.size * scale)
    bb = f.getbbox(s)
    tw, th = bb[2] - bb[0], bb[3] - bb[1]
    pad = radius * 3
    g = Image.new("RGBA", (int(tw + 2 * pad), int(th + 2 * pad)), (0, 0, 0, 0))
    gd = ImageDraw.Draw(g)
    gd.text((pad - bb[0], pad - bb[1]), s, font=f, fill=glow + (200,))
    g = g.filter(ImageFilter.GaussianBlur(radius))
    ox, oy = int(cx - tw / 2 - pad), int(cy - th / 2 - pad)
    for _ in range(strength):
        layer.alpha_composite(g, (max(0, ox), max(0, oy)), (max(0, -ox), max(0, -oy)))
    d = ImageDraw.Draw(layer)
    d.text((cx - tw / 2 - bb[0], cy - th / 2 - bb[1]), s, font=f, fill=fill)


def chevrons(d, cx, cy, t, color=YELLOW):
    for i in range(3):
        y = cy + i * 46 + 10 * math.sin(t * 7 - i * 0.8)
        a = 0.45 + 0.55 * (i + 1) / 3
        c = tuple(int(v * a + 30 * (1 - a)) for v in color)
        d.line([(cx - 52, y), (cx, y + 40), (cx + 52, y)], fill=c, width=14, joint="curve")


# ---- captions ---------------------------------------------------------------------
def chunks(sentence):
    out, cur = [], []
    for tk in sentence["tokens"]:
        cur.append(tk)
        if len(cur) == 3 or tk["text"][-1] in ".,!?":
            out.append(cur)
            cur = []
    if cur:
        out.append(cur)
    return out


def captions(img, t, si):
    s = T["sentences"][si]
    groups = chunks(s)
    g = groups[0]
    for grp in groups:
        if t >= grp[0]["start"] - 0.03:
            g = grp
    pop = back((t - g[0]["start"] + 0.03) / 0.12)
    size = 92
    words = [tk["text"].upper() for tk in g]
    f = font("Black", size)
    total = sum(text_w(w, f) for w in words) + 26 * (len(words) - 1)
    if total > 940:
        size = size * 940 / total
        f = font("Black", size)
        total = 940
    sc = 0.8 + 0.2 * pop
    f = font("Black", size * sc)
    total *= sc
    d = ImageDraw.Draw(img)
    cur = g[0]
    for tk in g:
        if t >= tk["start"] - 0.03:
            cur = tk
    x = W / 2 - total / 2
    for tk, w in zip(g, words):
        active = tk is cur
        d.text((x, 1340), w, font=f, fill=YELLOW if active else WHITE, stroke_width=8, stroke_fill=(5, 6, 18), anchor="ls")
        x += text_w(w, f) + 26 * sc


# ---- frame --------------------------------------------------------------------------
def sentence_at(t):
    idx = 0
    for i, s in enumerate(T["sentences"]):
        if t >= s["start"]:
            idx = i
    return idx


SHAKES = []
SCENES = None


def frame(t):
    img = background(t)
    L = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(L)
    si = sentence_at(t)
    st = T["sentences"][si]["start"]
    SCENES.draw(L, d, t, si, st)
    # punch-in on scene changes (not between chart beats)
    if si not in SCENES.NO_PUNCH:
        z = 1 + 0.08 * (1 - ease((t - st) / 0.22))
        if z > 1.001:
            nw, nh = int(W * z), int(H * z)
            L = L.resize((nw, nh), Image.BILINEAR).crop(((nw - W) // 2, (nh - H) // 2 - 40, (nw - W) // 2 + W, (nh - H) // 2 - 40 + H))
    # shake on big moments
    dx = dy = 0
    for ts in SHAKES:
        k = t - ts
        if 0 <= k < 0.35:
            amp = 14 * (1 - k / 0.35)
            dx += int(amp * math.sin(k * 90))
            dy += int(amp * math.cos(k * 73))
    img.alpha_composite(L, (max(0, dx), max(0, dy)), (max(0, -dx), max(0, -dy)))
    dd = ImageDraw.Draw(img)
    dd.text((90, 240), "POUND FOR POUND", font=font("Black", 34), fill=(255, 255, 255, 170))
    captions(img, t, si)
    dd.rectangle((0, 0, int(W * t / T["total"]), 10), fill=YELLOW)
    return img.convert("RGB")


