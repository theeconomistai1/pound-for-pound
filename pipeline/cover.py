"""Covers: a full-bleed illustrated scene that fits the subject + one or two huge words, one highlighted.

The cover is frame 0 of every brand video (and the loop target), and is also written to build/cover.png.
Objects are Microsoft Fluent Emoji (MIT licence) rendered from their vector files at full size with resvg,
then lit, blurred for depth and colour-graded in the day's palette. Words use Anton (SIL Open Font Licence).

  python3 -I pipeline/cover.py out.png --words "1p" "CHALLENGE" --highlight 0 --theme emerald \
          --hero "Jar" --left "Calendar" --right "Pound banknote" --particles "Coin"

Object names are Fluent asset folder names (https://github.com/microsoft/fluentui-emoji/tree/main/assets),
e.g. "House with garden", "Credit card", "Money bag", "Hot beverage", "Automobile", "Baby", "Old man".
"""
import argparse
import glob
import hashlib
import math
import os
import random
import subprocess
from functools import lru_cache

import numpy as np
from PIL import Image, ImageChops, ImageDraw, ImageFilter, ImageFont

W, H = 1080, 1920
A = os.environ.get("P4P_ASSETS", os.path.expanduser("~/.p4p-assets"))
FLUENT = os.path.join(A, "fluent")
RESVG = os.path.join(A, "resvg", "resvg")
CACHE = os.path.join(A, "cache")
TITLE_FONT = os.path.join(A, "gfonts", "ofl", "anton", "Anton-Regular.ttf")
EMOJI_3D = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets", "emoji")


# ---- objects ----------------------------------------------------------------------------------------------
def _svg_path(name):
    base = os.path.join(FLUENT, "assets", name)
    if not os.path.isdir(base) and os.path.isdir(os.path.join(FLUENT, ".git")):
        subprocess.run(["git", "-C", FLUENT, "sparse-checkout", "add", f"/assets/{name}/"], check=False,
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    for pat in ("Color/*.svg", "Default/Color/*.svg"):
        hits = sorted(glob.glob(os.path.join(base, pat)))
        if hits:
            return hits[0]
    return None


def _pound_sign(size):
    """A gold 3D-style £ (the channel's own hero object)."""
    import motion as Mo
    S = size * 2
    f = ImageFont.truetype(Mo.FONT, int(S * 0.95))
    f.set_variation_by_name("Black")
    mask = Image.new("L", (S, S), 0)
    ImageDraw.Draw(mask).text((S / 2, S / 2), "£", font=f, fill=255, anchor="mm")
    edge = Image.new("L", (S, S), 0)
    ImageDraw.Draw(edge).text((S / 2, S / 2), "£", font=f, fill=255, anchor="mm", stroke_width=int(S * 0.025),
                              stroke_fill=255)
    g = np.linspace(0, 1, S)[:, None]
    top, bot = np.array([255, 232, 140]), np.array([206, 128, 18])
    grad = (top * (1 - g[..., None]) + bot * g[..., None]).repeat(S, axis=1).astype(np.uint8)
    body = Image.fromarray(grad, "RGB").convert("RGBA")
    out = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    rim = Image.new("RGBA", (S, S), (140, 78, 6, 255))
    out.paste(rim, (0, int(S * 0.018)), edge)          # darker extruded edge, a little lower
    out.paste(body, (0, 0), mask)
    shine = Image.new("L", (S, S), 0)
    ImageDraw.Draw(shine).ellipse((S * 0.15, S * 0.05, S * 0.75, S * 0.42), fill=110)
    shine = ImageChops.multiply(shine.filter(ImageFilter.GaussianBlur(S * 0.04)), mask)
    out.paste(Image.new("RGBA", (S, S), (255, 255, 255, 255)), (0, 0), shine)
    return out.resize((size, size), Image.LANCZOS)


@lru_cache(maxsize=64)
def obj(name, size):
    """RGBA image of a Fluent emoji at `size` px ("£" = the gold pound sign). Falls back to the repo's 3D
    PNGs (soft when enlarged)."""
    size = int(size)
    if name == "£":
        return _pound_sign(size)
    os.makedirs(CACHE, exist_ok=True)
    key = hashlib.md5(f"{name}|{size}".encode()).hexdigest()[:12]
    cached = os.path.join(CACHE, f"obj_{key}.png")
    if os.path.exists(cached):
        return Image.open(cached).convert("RGBA")
    svg = _svg_path(name)
    if svg and os.path.exists(RESVG):
        subprocess.run([RESVG, "-w", str(size), "-h", str(size), svg, cached], check=True,
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return Image.open(cached).convert("RGBA")
    png = os.path.join(EMOJI_3D, name.lower().replace(" ", "_").replace("-", "_") + ".png")
    if os.path.exists(png):
        return Image.open(png).convert("RGBA").resize((size, size), Image.LANCZOS)
    raise FileNotFoundError(f"no art for {name!r} (Fluent asset folder name) — run pipeline/setup_assets.sh")


# ---- scene ---------------------------------------------------------------------------------------------------
def _radial(w, h, cx, cy, r, color, power=1.6, amount=1.0):
    yy, xx = np.mgrid[0:h, 0:w]
    d = np.sqrt((xx - cx) ** 2 + (yy - cy) ** 2) / r
    a = (np.clip(1 - d, 0, 1) ** power * 255 * amount).astype(np.uint8)
    im = np.zeros((h, w, 4), np.uint8)
    im[..., 0], im[..., 1], im[..., 2], im[..., 3] = color[0], color[1], color[2], a
    return Image.fromarray(im, "RGBA")


def _shadowed(im, blur=26, offset=(0, 34), strength=170):
    pad = blur * 3
    out = Image.new("RGBA", (im.width + 2 * pad, im.height + 2 * pad), (0, 0, 0, 0))
    sh = Image.new("RGBA", im.size, (0, 0, 0, 0))
    sh.putalpha(im.getchannel("A").point(lambda v: v * strength // 255))
    out.alpha_composite(sh, (pad + offset[0], pad + offset[1]))
    out = out.filter(ImageFilter.GaussianBlur(blur))
    out.alpha_composite(im, (pad, pad))
    return out, pad


def _shade(im, k):
    """Darken an RGBA image (depth): k in 0..1, 1 = unchanged."""
    r, g, b, a = im.split()
    f = lambda v: int(v * k)
    return Image.merge("RGBA", (r.point(f), g.point(f), b.point(f), a))


def _skyline(rnd, glow, warm):
    """Night city behind the scene: two layers of buildings with lit windows, out of focus."""
    layers = []
    for depth, (base, hmin, hmax, shade, blur, wcount) in enumerate(
            ((1380, 380, 980, 0.30, 7, 0.10), (1460, 220, 760, 0.16, 4, 0.16))):
        im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        d = ImageDraw.Draw(im)
        x = -40
        while x < W + 40:
            bw = rnd.uniform(90, 190)
            bh = rnd.uniform(hmin, hmax)
            col = tuple(int(c * shade) for c in glow)
            d.rectangle((x, base - bh, x + bw, H), fill=col + (255,))
            if rnd.random() < 0.3:  # rooftop detail
                d.rectangle((x + bw * 0.4, base - bh - 40, x + bw * 0.46, base - bh), fill=col + (255,))
            for wy in np.arange(base - bh + 24, base, 34):
                for wx in np.arange(x + 14, x + bw - 14, 26):
                    if rnd.random() < wcount:
                        c = rnd.choice([warm, glow, (255, 245, 220)])
                        d.rectangle((wx, wy, wx + 12, wy + 16), fill=tuple(c) + (int(rnd.uniform(90, 200)),))
            x += bw + rnd.uniform(4, 22)
        layers.append(im.filter(ImageFilter.GaussianBlur(blur)))
    return layers


def _fill_with(hero_img, filler, rnd):
    """A container (e.g. "Jar") filled with objects (e.g. "Coin"): fill drawn behind a see-through body."""
    hs = hero_img.width
    a = np.asarray(hero_img.getchannel("A"))
    ys, xs = np.where(a > 200)
    x0, x1, y0, y1 = xs.min(), xs.max(), ys.min(), ys.max()
    inner = (x0 + (x1 - x0) * 0.1, y0 + (y1 - y0) * 0.3, x1 - (x1 - x0) * 0.1, y1 - (y1 - y0) * 0.05)
    fill = Image.new("RGBA", (hs, hs), (0, 0, 0, 0))
    cs = int((inner[2] - inner[0]) / 3.2)
    y = inner[3] - cs * 0.45
    while y > inner[1]:
        x = inner[0] + rnd.uniform(-cs * 0.2, cs * 0.3)
        while x < inner[2] - cs * 0.3:
            c = obj(filler, cs).rotate(rnd.uniform(-60, 60), Image.BICUBIC)
            fill.alpha_composite(c, (int(x - cs * 0.15), int(y - cs * 0.5)))
            x += cs * rnd.uniform(0.55, 0.75)
        y -= cs * 0.42
    fill.putalpha(ImageChops.multiply(fill.getchannel("A"), hero_img.getchannel("A")))
    body = hero_img.copy()
    lid = int(y0 + (y1 - y0) * 0.2)
    ba = np.asarray(body.getchannel("A")).astype(np.float32)
    ba[lid:] *= 0.24
    body.putalpha(Image.fromarray(ba.astype(np.uint8)))
    out = Image.new("RGBA", (hs, hs), (0, 0, 0, 0))
    out.alpha_composite(fill)
    out.alpha_composite(body)
    return out


@lru_cache(maxsize=8)
def backdrop(theme_key, hero, left=None, right=None, particles=None, seed="p4p", fill=None, env="city"):
    """The illustrated scene (no words), 1080x1920 RGB. theme_key: a key of brand.PALETTES.
    hero: the big object; left/right: blurred objects behind; particles: small objects scattered;
    fill: fill the hero with this object (e.g. hero "Jar", fill "Coin"); env: "city" (night skyline) or "plain"."""
    import brand  # palettes live in the brand kit
    th = brand.PALETTES[theme_key]
    rnd = random.Random(seed)
    top, bot, glow = np.array(th["bgTop"], float), np.array(th["bgBottom"], float), th["glow"]
    g = np.linspace(0, 1, H)[:, None, None] ** 0.9
    arr = np.repeat(top * (1 - g) + bot * g, W, axis=1)
    img = Image.fromarray(arr.astype(np.uint8), "RGB").convert("RGBA")
    # light: big soft spotlight behind the hero + beams from above
    img.alpha_composite(_radial(W, H, 540, 1080, 1050, glow, 1.5, 0.75))
    beams = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    bd = ImageDraw.Draw(beams)
    for i in range(6):
        x = 540 + (i - 2.5) * 190 + rnd.uniform(-40, 40)
        w0, w1 = rnd.uniform(18, 40), rnd.uniform(160, 260)
        bd.polygon([(540 + (x - 540) * 0.15 - w0, -40), (540 + (x - 540) * 0.15 + w0, -40), (x + w1, 1500),
                    (x - w1, 1500)], fill=tuple(glow) + (int(rnd.uniform(14, 30)),))
    img.alpha_composite(beams.filter(ImageFilter.GaussianBlur(38)))
    # bokeh
    bk = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    kd = ImageDraw.Draw(bk)
    cols = [tuple(glow), tuple(th["highlight"]), (255, 255, 255)]
    for _ in range(34):
        r = rnd.uniform(8, 58)
        x, y = rnd.uniform(0, W), rnd.uniform(120, 1500)
        kd.ellipse((x - r, y - r, x + r, y + r), fill=rnd.choice(cols) + (int(rnd.uniform(18, 70)),))
    img.alpha_composite(bk.filter(ImageFilter.GaussianBlur(7)))
    if env == "city":
        for layer in _skyline(rnd, glow, th["highlight"]):
            img.alpha_composite(layer)
    # floor glow line under the hero
    floor_y = 1630
    img.alpha_composite(_radial(W, H, 540, floor_y, 620, glow, 2.2, 0.55))
    # back objects: blurred, darker, partly off-frame for depth
    for name, cx, cy, size, rot, blur, k in (
            (left, 175, 1180, 520, 12, 5, 0.72), (right, 915, 1090, 470, -10, 6, 0.68)):
        if not name:
            continue
        o = _shade(obj(name, size).rotate(rot, Image.BICUBIC, expand=True), k).filter(ImageFilter.GaussianBlur(blur))
        o, pad = _shadowed(o, 30, (0, 30), 120)
        img.alpha_composite(o, (int(cx - o.width / 2), int(cy - o.height / 2)))
    # hero: big, sharp, with a soft shadow and a faint floor reflection
    hs = 840
    ho = obj(hero, hs)
    if fill:
        ho = _fill_with(ho, fill, rnd)
    ref = ho.transpose(Image.FLIP_TOP_BOTTOM)
    grad = Image.linear_gradient("L").resize((hs, hs)).point(lambda v: max(0, 70 - v // 2))
    ref.putalpha(ImageChops.multiply(ref.getchannel("A"), grad))
    hx, hy = 540, floor_y - hs / 2 + 30
    img.alpha_composite(ref.filter(ImageFilter.GaussianBlur(4)), (int(hx - hs / 2), int(floor_y + 20)))
    hsd, pad = _shadowed(ho, 34, (0, 40), 190)
    img.alpha_composite(hsd, (int(hx - hsd.width / 2), int(hy - hsd.height / 2)))
    # foreground particles (e.g. coins): a few sharp, a few big and blurred close to camera
    if particles:
        for i in range(9):
            near = i < 3
            size = int(rnd.uniform(170, 240) if near else rnd.uniform(70, 130))
            o = obj(particles, size).rotate(rnd.uniform(-35, 35), Image.BICUBIC, expand=True)
            if near:
                o = o.filter(ImageFilter.GaussianBlur(9))
            x = rnd.choice([rnd.uniform(-30, 260), rnd.uniform(820, 1110)])
            y = rnd.uniform(250, 1750) if near else rnd.uniform(300, 1650)
            img.alpha_composite(o, (int(x - o.width / 2), int(y - o.height / 2)))
    # grade: vignette + light grain
    vig = _radial(W, H, 540, 960, 1250, (0, 0, 0), 1.0, 1.0)
    va = np.asarray(vig.getchannel("A"), float) / 255
    dark = (1 - va) * 0.62
    rgb = np.asarray(img.convert("RGB"), float) * (1 - dark[..., None])
    rgb += np.random.default_rng(7).normal(0, 3.2, rgb.shape)
    return Image.fromarray(np.clip(rgb, 0, 255).astype(np.uint8), "RGB")


# ---- title ---------------------------------------------------------------------------------------------------
@lru_cache(maxsize=64)
def _font(size):
    return ImageFont.truetype(TITLE_FONT, int(size))


def _word(s, size, fill, inner, outer):
    """One word: fill, inner stroke, outer stroke, drop shadow."""
    f = _font(size)
    so, si = int(size * 0.075), int(size * 0.045)
    l, t, r, b = f.getbbox(s, stroke_width=so)
    pad = int(size * 0.25)
    w, h = r - l + 2 * pad, b - t + 2 * pad
    org = (pad - l, pad - t)
    sh = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    ImageDraw.Draw(sh).text((org[0], org[1] + size * 0.06), s, font=f, fill=(0, 0, 0, 210), stroke_width=so,
                            stroke_fill=(0, 0, 0, 210))
    im = sh.filter(ImageFilter.GaussianBlur(size * 0.06))
    d = ImageDraw.Draw(im)
    d.text(org, s, font=f, fill=tuple(outer) + (255,), stroke_width=so, stroke_fill=tuple(outer) + (255,))
    d.text(org, s, font=f, fill=tuple(fill) + (255,), stroke_width=si, stroke_fill=tuple(inner) + (255,))
    return im


@lru_cache(maxsize=16)
def title(words, highlight, hl_color, max_size=250, max_w=860):
    """words: tuple of 1-2 strings. highlight: index of the highlighted word (or -1)."""
    words = tuple(w.upper() if not any(c.isdigit() for c in w) else w for w in words)
    def width(s, size):
        f = _font(size)
        l, _, r, _ = f.getbbox(s)
        return r - l
    one = " ".join(words)
    size = max_size
    if len(words) == 1 or width(one, max_size) <= max_w:
        lines = [list(range(len(words)))]
        size = min(max_size, max_size * max_w / width(one, max_size))
    else:
        lines = [[0], [1]]
        size = min(max_size, *(max_size * max_w / width(w, max_size) for w in words))
    rows = []
    for ln in lines:
        parts = []
        for i in ln:
            if i == highlight:
                parts.append(_word(words[i], size, hl_color, (255, 255, 255), (0, 0, 0)))
            else:
                parts.append(_word(words[i], size, (255, 255, 255), (0, 0, 0), (0, 0, 0)))
        gap = int(size * 0.02)
        rw = sum(p.width for p in parts) - (len(parts) - 1) * int(size * 0.3) + gap
        row = Image.new("RGBA", (rw, max(p.height for p in parts)), (0, 0, 0, 0))
        x = 0
        for p in parts:
            row.alpha_composite(p, (x, 0))
            x += p.width - int(size * 0.3) + gap
        rows.append(row)
    lh = int(size * 0.98)
    out = Image.new("RGBA", (max(r.width for r in rows), rows[0].height + lh * (len(rows) - 1)), (0, 0, 0, 0))
    for i, r in enumerate(rows):
        out.alpha_composite(r, ((out.width - r.width) // 2, i * lh))
    return out


TITLE_X, TITLE_Y = 525, 860  # centre of the cover words (a touch left of centre: clear of the button column)


def render(theme_key, words, highlight, hero, left=None, right=None, particles=None, fill=None, env="city"):
    import brand
    bg = backdrop(theme_key, hero, left, right, particles, "|".join(words), fill, env).convert("RGBA")
    t = title(tuple(words), highlight, tuple(brand.PALETTES[theme_key]["highlight"]))
    bg.alpha_composite(t, (int(TITLE_X - t.width / 2), int(TITLE_Y - t.height / 2)))
    return bg.convert("RGB")


def main():
    import sys
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    ap = argparse.ArgumentParser()
    ap.add_argument("out")
    ap.add_argument("--words", nargs="+", required=True)
    ap.add_argument("--highlight", type=int, default=0)
    ap.add_argument("--theme", default="emerald")
    ap.add_argument("--hero", required=True)
    ap.add_argument("--left")
    ap.add_argument("--right")
    ap.add_argument("--particles")
    ap.add_argument("--fill")
    ap.add_argument("--env", default="city")
    a = ap.parse_args()
    if len(a.words) > 2:
        sys.exit("one or two words only")
    render(a.theme, a.words, a.highlight, a.hero, a.left, a.right, a.particles, a.fill, a.env).save(a.out, quality=95)
    print(a.out)


if __name__ == "__main__":
    main()
