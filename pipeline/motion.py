"""Motion-design toolkit (house style for all Pound for Pound videos from 20 Oct 2026) for 1080x1920 explainers (spec: navy/purple grid, Nunito 900,
green accent, cyan intermediates, spring entrances, karaoke captions, top bar + progress).

All shapes are drawn supersampled (x3) and scaled down, so edges are anti-aliased.
Elements are separate sprites composited with real alpha.
"""
import math
import os
from functools import lru_cache

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

W, H, FPS = 1080, 1920, 30
SS = 3  # supersampling for shapes

THEME = dict(
    bgTop=(14, 20, 48), bgBottom=(42, 42, 110),
    green=(155, 225, 93), cyan=(79, 195, 247), white=(255, 255, 255), muted=(138, 147, 184),
    ink=(10, 12, 28),
)
G, C, Wt, M, INK = THEME["green"], THEME["cyan"], THEME["white"], THEME["muted"], THEME["ink"]

FONT = os.environ.get("MOTION_FONT", os.path.expanduser("~/.p4p-assets/nunito/fonts/variable/Nunito[wght].ttf"))
EMOJI_DIR = os.environ.get("MOTION_EMOJI", os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets", "emoji"))


# ---- timing -------------------------------------------------------------------------
def spring(t, start=0.0, damping=14.0, stiffness=120.0, mass=1.0):
    """Remotion-style spring step response (0 -> 1 with slight overshoot)."""
    x = t - start
    if x <= 0:
        return 0.0
    w0 = math.sqrt(stiffness / mass)
    z = damping / (2 * math.sqrt(stiffness * mass))
    if z >= 1:
        return 1 - math.exp(-w0 * x) * (1 + w0 * x)
    wd = w0 * math.sqrt(1 - z * z)
    return 1 - math.exp(-z * w0 * x) * (math.cos(wd * x) + (z * w0 / wd) * math.sin(wd * x))


def clamp(v, a=0.0, b=1.0):
    return max(a, min(b, v))


def ramp(t, start, dur):
    return clamp((t - start) / dur) if dur > 0 else float(t >= start)


def ease(x):
    x = clamp(x)
    return 1 - (1 - x) ** 3


# ---- fonts & text -------------------------------------------------------------------------
@lru_cache(maxsize=256)
def font(size, weight="Black"):
    f = ImageFont.truetype(FONT, max(6, int(round(size))))
    f.set_variation_by_name(weight)
    return f


@lru_cache(maxsize=2048)
def text_sprite(s, size, color, weight="Black", shadow=False):
    f = font(size, weight)
    l, _, r, _ = f.getbbox(s)
    # fixed vertical box from the cap height, so words share a baseline when centred
    cap = f.getbbox("H")
    top, bottom = cap[1], cap[3]
    pad = int(size * 0.35) if shadow else 4
    extra = int(size * 0.32)  # room for descenders / accents
    im = Image.new("RGBA", (r - l + 2 * pad, bottom - top + 2 * pad + 2 * extra), (0, 0, 0, 0))
    org = (pad - l, pad + extra - top)
    if shadow:
        sh = Image.new("RGBA", im.size, (0, 0, 0, 0))
        ImageDraw.Draw(sh).text((org[0], org[1] + size * 0.05), s, font=f, fill=(0, 0, 0, 200))
        im = Image.alpha_composite(im, sh.filter(ImageFilter.GaussianBlur(size * 0.08)))
    ImageDraw.Draw(im).text(org, s, font=f, fill=tuple(color) + (255,))
    return im


def text_width(s, size, weight="Black"):
    return font(size, weight).getlength(s)


# ---- shapes -----------------------------------------------------------------------------------
@lru_cache(maxsize=512)
def rrect_sprite(w, h, r, fill, border=None, bw=0, glow=None):
    """Rounded rectangle, anti-aliased. fill/border are RGBA tuples."""
    pad = 40 if glow else 2
    big = Image.new("RGBA", ((w + 2 * pad) * SS, (h + 2 * pad) * SS), (0, 0, 0, 0))
    d = ImageDraw.Draw(big)
    box = (pad * SS, pad * SS, (pad + w) * SS - 1, (pad + h) * SS - 1)
    d.rounded_rectangle(box, r * SS, fill=fill, outline=border, width=bw * SS if border else 0)
    im = big.resize((w + 2 * pad, h + 2 * pad), Image.LANCZOS)
    if glow:
        g = Image.new("RGBA", im.size, (0, 0, 0, 0))
        gd = ImageDraw.Draw(g)
        gd.rounded_rectangle((pad, pad, pad + w, pad + h), r, outline=glow, width=6)
        g = g.filter(ImageFilter.GaussianBlur(14))
        im = Image.alpha_composite(g, im)
    return im, pad


@lru_cache(maxsize=256)
def circle_sprite(d, fill, border=None, bw=0):
    big = Image.new("RGBA", (d * SS, d * SS), (0, 0, 0, 0))
    ImageDraw.Draw(big).ellipse((0, 0, d * SS - 1, d * SS - 1), fill=fill, outline=border, width=bw * SS)
    return big.resize((d, d), Image.LANCZOS)


@lru_cache(maxsize=256)
def emoji_sprite(name, size):
    im = Image.open(os.path.join(EMOJI_DIR, name + ".png")).convert("RGBA")
    return im.resize((int(size), int(size)), Image.LANCZOS)


def with_alpha(im, a):
    if a >= 0.999:
        return im
    im = im.copy()
    im.putalpha(im.getchannel("A").point([int(i * clamp(a)) for i in range(256)]))
    return im


def scaled(im, s):
    if abs(s - 1) < 0.004:
        return im
    w, h = max(1, int(im.width * s)), max(1, int(im.height * s))
    return im.resize((w, h), Image.BILINEAR)


class Layer:
    def __init__(self):
        self.im = Image.new("RGBA", (W, H), (0, 0, 0, 0))

    def put(self, sprite, cx, cy, alpha=1.0, scale=1.0):
        if alpha <= 0.003:
            return
        sp = with_alpha(scaled(sprite, scale), alpha)
        x, y = int(round(cx - sp.width / 2)), int(round(cy - sp.height / 2))
        sx, sy = max(0, -x), max(0, -y)
        if sx >= sp.width or sy >= sp.height or x >= W or y >= H:
            return
        self.im.alpha_composite(sp, (max(0, x), max(0, y)), (sx, sy))

    # ---- components -------------------------------------------------------------------------------
    def text(self, s, cx, cy, size, color=Wt, alpha=1.0, scale=1.0, weight="Black", shadow=False):
        self.put(text_sprite(s, size, tuple(color), weight, shadow), cx, cy, alpha, scale)

    def badge(self, label, cx, cy, t, start, variant="green", size=30):
        p = spring(t, start)
        if p <= 0:
            return
        fill = (G if variant == "green" else Wt) + (255,)
        tw = text_width(label, size)
        w, h = int(tw + size * 1.4), int(size * 1.9)
        sp, pad = rrect_sprite(w, h, h // 2, fill)
        s = 0.6 + 0.4 * p
        self.put(sp, cx, cy, clamp(p * 1.5), s)
        self.text(label, cx, cy + 1, size, INK, clamp(p * 1.5), s)

    def card(self, cx, cy, w, h, t, start, verified_at=None, r=24):
        p = spring(t, start)
        if p <= 0:
            return 0
        ok = verified_at is not None and t >= verified_at
        border = (G + (255,)) if ok else (255, 255, 255, 64)
        sp, pad = rrect_sprite(int(w), int(h), r, (255, 255, 255, 13), border, 3, (G + (150,)) if ok else None)
        self.put(sp, cx, cy + (1 - p) * 30, clamp(p * 1.4))
        return clamp(p * 1.4)

    def emoji(self, name, cx, cy, size, t, start, bounce=False):
        p = spring(t, start)
        if p <= 0:
            return
        s = (0.4 + 0.6 * p) * (1 + (0.04 * math.sin((t - start) * 6) if bounce else 0))
        self.put(emoji_sprite(name, size), cx, cy, clamp(p * 1.5), s)

    def math_line(self, tokens, cx, cy, size, t, start, stagger=0.12, gap=None):
        """tokens: list of (text, color). Each slides up 20px and fades in, one after another."""
        gap = size * 0.32 if gap is None else gap
        widths = [text_width(s, size) for s, _ in tokens]
        total = sum(widths) + gap * (len(tokens) - 1)
        x = cx - total / 2
        for i, ((s, col), w) in enumerate(zip(tokens, widths)):
            st = start + i * stagger
            p = spring(t, st)
            if p > 0:
                self.text(s, x + w / 2, cy + 20 * (1 - clamp(p)), size, col, clamp(p * 1.3))
            x += w + gap
        return total

    def price_card(self, emoji, label, price, cx, cy, t, start, w=440, h=150, price_color=G, price_size=58,
                   verified_at=None, price_at=None):
        a = self.card(cx, cy, w, h, t, start, verified_at)
        if a <= 0:
            return
        self.emoji(emoji, cx - w / 2 + 78, cy, 100, t, start + 0.08)
        lx = cx - w / 2 + 156
        lab = text_sprite(label, 26, tuple(M), "ExtraBold")
        self.put(lab, lx + lab.width / 2, cy - 32, a)
        pa = a if price_at is None else clamp(spring(t, price_at) * 1.3)
        if pa > 0:
            pr = text_sprite(price, price_size, tuple(price_color))
            self.put(pr, lx + pr.width / 2, cy + 22 + 14 * (1 - pa), pa)

    def arrow(self, x0, y0, x1, y1, progress, color=Wt, width=6, alpha=1.0):
        if progress <= 0:
            return
        xs, ys = x0 + (x1 - x0) * progress, y0 + (y1 - y0) * progress
        minx, miny = int(min(x0, xs) - 40), int(min(y0, ys) - 40)
        maxx, maxy = int(max(x0, xs) + 40), int(max(y0, ys) + 40)
        big = Image.new("RGBA", ((maxx - minx) * SS, (maxy - miny) * SS), (0, 0, 0, 0))
        d = ImageDraw.Draw(big)
        P = lambda x, y: ((x - minx) * SS, (y - miny) * SS)
        col = tuple(color) + (255,)
        d.line([P(x0, y0), P(xs, ys)], fill=col, width=width * SS)
        if progress > 0.6:
            ang = math.atan2(ys - y0, xs - x0)
            L = 26
            for da in (2.6, -2.6):
                d.line([P(xs, ys), P(xs + L * math.cos(ang + da), ys + L * math.sin(ang + da))], fill=col, width=width * SS)
        sp = big.resize((maxx - minx, maxy - miny), Image.LANCZOS)
        self.put(sp, (minx + maxx) / 2, (miny + maxy) / 2, alpha)


# ---- background and fixed layers ----------------------------------------------------------------
_bg = None
_glow = None


def background(t):
    global _bg, _glow
    if _bg is None:
        top, bot = np.array(THEME["bgTop"], float), np.array(THEME["bgBottom"], float)
        g = np.linspace(0, 1, H)[:, None, None]
        arr = top * (1 - g) + bot * g
        arr = np.repeat(arr, W, axis=1)
        grid = np.zeros((H, W), bool)
        grid[::60, :] = True
        grid[:, ::60] = True
        arr[grid] = arr[grid] * 0.96 + 255 * 0.04
        _bg = Image.fromarray(arr.astype(np.uint8), "RGB").convert("RGBA")
        r = 900
        yy, xx = np.mgrid[0:2 * r, 0:2 * r]
        dist = np.sqrt((xx - r) ** 2 + (yy - r) ** 2) / r
        a = np.clip(1 - dist / 0.6, 0, 1) ** 1.6 * 0.35 * 255
        glow = np.zeros((2 * r, 2 * r, 4), np.uint8)
        glow[..., 0], glow[..., 1], glow[..., 2], glow[..., 3] = 90, 80, 200, a.astype(np.uint8)
        _glow = Image.fromarray(glow, "RGBA")
    im = _bg.copy()
    cx = int(W * 0.70 + 40 * math.sin(t * 0.25))
    cy = int(H * 0.75 + 30 * math.cos(t * 0.2))
    gx, gy = cx - _glow.width // 2, cy - _glow.height // 2
    im.alpha_composite(_glow, (max(0, gx), max(0, gy)), (max(0, -gx), max(0, -gy)))
    return im


def top_bar(L, t, total, badge, title):
    sp_w = int(text_width(badge, 28) + 40)
    sp, _ = rrect_sprite(sp_w, 52, 26, G + (255,))
    x0 = 70
    L.put(sp, x0 + sp_w / 2, 130)
    L.text(badge, x0 + sp_w / 2, 131, 28, INK)
    tt = text_sprite(title, 28, (220, 224, 240), "ExtraBold")
    L.put(tt, x0 + sp_w + 24 + tt.width / 2, 130)
    track, _ = rrect_sprite(W - 140, 6, 3, (255, 255, 255, 46))
    L.put(track, W / 2, 190)
    fw = max(6, int((W - 140) * clamp(t / total)))
    fill, _ = rrect_sprite(fw, 6, 3, G + (255,))
    L.put(fill, 70 + fw / 2, 190)


# ---- karaoke captions ----------------------------------------------------------------------------
def caption_groups(timings):
    groups = []
    for s in timings["sentences"]:
        cur = []
        for tk in s["tokens"]:
            cur.append(tk)
            if len(cur) >= 4 or (len(cur) >= 2 and tk["text"][-1] in ".,!?:") :
                groups.append(cur)
                cur = []
        if cur:
            groups.append(cur)
    # merge single-word tail into previous group when short
    out = []
    for g in groups:
        if out and len(g) == 1 and len(out[-1]) <= 3 and out[-1][-1]["text"][-1] not in ".!?":
            out[-1] = out[-1] + g
        else:
            out.append(g)
    return out


def captions(L, t, groups, cy=1190, size=56):
    cur = None
    for i, g in enumerate(groups):
        end = groups[i + 1][0]["start"] if i + 1 < len(groups) else g[-1]["end"] + 0.6
        if g[0]["start"] - 0.05 <= t < min(end, g[-1]["end"] + 0.5):
            cur = (g, end)
    if not cur:
        return
    g, end = cur
    a = min(ramp(t, g[0]["start"] - 0.05, 0.12), 1 - ramp(t, min(end, g[-1]["end"] + 0.5) - 0.1, 0.1))
    words = [tk["text"] for tk in g]
    widths = [text_width(w, size) for w in words]
    gap = size * 0.3
    total = sum(widths) + gap * (len(words) - 1)
    sz = size if total <= 960 else size * 960 / total
    if sz != size:
        widths = [text_width(w, sz) for w in words]
        gap = sz * 0.3
        total = sum(widths) + gap * (len(words) - 1)
    x = W / 2 - total / 2
    for tk, w, wd in zip(g, words, widths):
        active = tk["start"] - 0.03 <= t < tk["end"]
        L.text(w, x + wd / 2, cy, sz, G if active else Wt, a, shadow=True)
        x += wd + gap


# ---- per-video glue ------------------------------------------------------------------------------
# make_v3.py sets T (timings) and SCENE (the video's scenes.py module) before rendering.
T = None
SCENE = None
GROUPS = None


def S(i):
    """Start time of sentence i."""
    return T["sentences"][i]["start"]


def tk(si, prefix):
    """Start time of the first shown token in sentence si that starts with prefix."""
    for t in T["sentences"][si]["tokens"]:
        if t["text"].startswith(prefix):
            return t["start"]
    raise KeyError((si, prefix))


def gbp(v, dp=0):
    return f"£{v:,.{dp}f}"


def frame(t):
    img = background(t)
    base = Layer()
    top_bar(base, t, T["total"], getattr(SCENE, "BADGE", "MONEY MATHS"), getattr(SCENE, "TITLE", "POUND FOR POUND"))
    img.alpha_composite(base.im)
    scenes = SCENE.SCENES
    k = 0
    for i, (a, b) in enumerate(scenes):
        if t >= S(a) - 0.001:
            k = i
    start = S(scenes[k][0]) if k > 0 else 0.0
    end = S(scenes[k + 1][0]) if k + 1 < len(scenes) else T["total"] + 1
    alpha = min(ramp(t, start, 0.35) if k > 0 else 1.0, 1 - ramp(t, end - 0.27, 0.27))
    sc = Layer()
    SCENE.DRAW[k](sc, t)
    img.alpha_composite(with_alpha(sc.im, alpha))
    cap = Layer()
    captions(cap, t, GROUPS)
    img.alpha_composite(cap.im)
    return img.convert("RGB")
