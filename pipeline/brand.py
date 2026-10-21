"""Pound for Pound brand kit v1 — the locked look for every Short from 21 Oct 2026.

A video opts in with `BRAND = True` in its scenes.py (make_v3.py then renders with `brand.frame`).
Everything here is fixed so every Short is recognisably ours: the frame (logo bar, episode number,
progress), the layout grid, the signature hook frame, the beat chips, the source stamp, the
"your turn" and "send this to" end cards, the captions and the seamless loop back to frame 0.
Scenes are assembled from these blocks; free drawing with motion.py primitives is still allowed
inside the content zone, in the brand colours. See BRAND.md for the rules.
"""
import math
from functools import lru_cache

from PIL import Image, ImageDraw, ImageEnhance, ImageFilter

import motion as Mo
from motion import (C, G, INK, M, SS, W, H, Wt, Layer, circle_sprite, clamp, ease, emoji_sprite, font, ramp,
                    rrect_sprite, scaled, spring, text_sprite, text_width, with_alpha)

VERSION = "brand-v2"
RED = (255, 112, 112)       # costs, losses, warnings
GOLD = (255, 205, 86)       # rare highlight (records, "best")
LOGO_GREEN = (155, 225, 93)  # the logo never changes colour
TONES = {"green": G, "white": Wt, "red": RED, "cyan": C, "gold": GOLD}

# ---- daily palettes ----------------------------------------------------------------------------------------
# Every video gets a different background colour. The roles stay fixed: "green" = the key-result accent
# (captions' spoken word, payoff numbers), "cyan" = in-between results, "red" = costs, "muted" = labels,
# "highlight" = the highlighted cover word, "glow" = lighting. White text must read on every palette.
PALETTES = {
    "emerald":  dict(bgTop=(3, 32, 26), bgBottom=(8, 84, 64), glow=(36, 200, 140), green=(255, 212, 72),
                     cyan=(125, 225, 255), red=(255, 128, 128), muted=(146, 186, 170), highlight=(255, 214, 0)),
    "royal":    dict(bgTop=(6, 18, 66), bgBottom=(24, 60, 170), glow=(90, 150, 255), green=(155, 225, 93),
                     cyan=(255, 206, 90), red=(255, 120, 120), muted=(164, 180, 224), highlight=(255, 56, 56)),
    "ember":    dict(bgTop=(34, 10, 4), bgBottom=(130, 50, 12), glow=(255, 140, 60), green=(155, 225, 93),
                     cyan=(130, 214, 255), red=(255, 150, 150), muted=(212, 176, 150), highlight=(255, 214, 0)),
    "plum":     dict(bgTop=(28, 8, 44), bgBottom=(88, 24, 108), glow=(190, 80, 255), green=(155, 225, 93),
                     cyan=(255, 186, 100), red=(255, 118, 140), muted=(184, 160, 200), highlight=(255, 214, 0)),
    "ocean":    dict(bgTop=(2, 26, 40), bgBottom=(6, 84, 104), glow=(30, 200, 220), green=(155, 225, 93),
                     cyan=(255, 196, 100), red=(255, 120, 120), muted=(140, 184, 198), highlight=(255, 56, 56)),
    "wine":     dict(bgTop=(34, 4, 14), bgBottom=(116, 18, 44), glow=(255, 80, 110), green=(255, 212, 72),
                     cyan=(130, 214, 255), red=(255, 170, 180), muted=(206, 164, 174), highlight=(255, 214, 0)),
    "graphite": dict(bgTop=(12, 12, 14), bgBottom=(48, 44, 40), glow=(255, 190, 80), green=(255, 204, 80),
                     cyan=(90, 200, 250), red=(255, 112, 112), muted=(172, 166, 156), highlight=(255, 56, 56)),
    "magenta":  dict(bgTop=(36, 4, 32), bgBottom=(120, 14, 90), glow=(255, 80, 190), green=(155, 225, 93),
                     cyan=(130, 226, 255), red=(255, 170, 120), muted=(208, 164, 198), highlight=(255, 214, 0)),
    "classic":  dict(bgTop=(14, 20, 48), bgBottom=(42, 42, 110), glow=(90, 80, 200), green=(155, 225, 93),
                     cyan=(79, 195, 247), red=(255, 112, 112), muted=(138, 147, 184), highlight=(255, 56, 56)),
}
ROTATION = ["emerald", "royal", "ember", "plum", "ocean", "wine", "graphite", "magenta"]  # 005 = emerald
THEME_KEY = "classic"
PAL = PALETTES["classic"]


def theme_for(number):
    """Palette for video number NNN: consecutive videos (and the two daily slots) always differ."""
    return ROTATION[(int(number) - 5) % len(ROTATION)]


def set_theme(key):
    """Switch every colour role to palette `key`. Call before the video's scenes.py is executed."""
    global THEME_KEY, PAL, G, C, M, RED, TONES, _first, _cov
    pal = PALETTES[key]
    THEME_KEY, PAL = key, pal
    G, C, M, RED = pal["green"], pal["cyan"], pal["muted"], pal["red"]
    TONES = {"green": G, "white": Wt, "red": RED, "cyan": C, "gold": GOLD}
    Mo.THEME.update(bgTop=pal["bgTop"], bgBottom=pal["bgBottom"], glow=pal["glow"], green=G, cyan=C, muted=M)
    Mo.G, Mo.C, Mo.M = G, C, M
    Mo._bg = Mo._glow = None
    _first = _cov = None

# ---- layout grid (1080x1920) ------------------------------------------------------------------------
# YouTube hides ~120px top, ~300px bottom and a ~96px button column on the right of the lower half.
BAR_Y, PROGRESS_Y = 165, 228          # logo bar + progress
BEAT_Y = 305                          # beat chip, same place in every scene
TOP, BOTTOM = 370, 1240               # content zone
CAPTION_Y = 1365                      # karaoke captions
CLEAR_Y = 1480                        # nothing below this line (title/channel overlay)
X0, X1 = 70, 1010                     # content margins
RIGHT_SAFE = 960                      # below y=900 keep content left of this (like/comment/share buttons)
LOOP = 0.5                            # seconds of crossfade back to frame 0 at the end

BEATS = {  # the fixed beat labels; use these words so viewers learn the format
    "example": ("THE EXAMPLE", "white"),
    "maths": ("THE MATHS", "white"),
    "catch": ("THE CATCH", "red"),
    "twist": ("THE TWIST", "green"),
    "miss": ("ONE THING PEOPLE MISS", "white"),
    "levelup": ("LEVEL UP", "green"),
    "turn": ("YOUR TURN", "green"),
    "share": ("SEND THIS TO", "green"),
    # brand-v2 formats (BRAND.md §1)
    "myth": ("THE MYTH", "red"),
    "truth": ("THE TRUTH", "green"),
    "why": ("WHY", "white"),
    "changed": ("WHAT CHANGED", "white"),
    "who": ("WHO IT AFFECTS", "white"),
    "means": ("WHAT IT MEANS", "green"),
    "then": ("BACK THEN", "white"),
    "today": ("TODAY", "green"),
    "take": ("MY TAKE", "gold"),
}

EPISODE = None  # set from the video folder name by make_v3.py ("005")


# ---- logo ------------------------------------------------------------------------------------------------
@lru_cache(maxsize=16)
def logo_sprite(d):
    """Green coin with a £ — the channel mark."""
    D = d * SS
    big = Image.new("RGBA", (D, D), (0, 0, 0, 0))
    dr = ImageDraw.Draw(big)
    dr.ellipse((0, 0, D - 1, D - 1), fill=LOGO_GREEN + (255,))
    inset = int(D * 0.085)
    dr.ellipse((inset, inset, D - 1 - inset, D - 1 - inset), outline=INK + (70,), width=max(2, int(D * 0.03)))
    f = font(D * 0.6, "Black")
    dr.text((D / 2, D / 2 + D * 0.02), "£", font=f, fill=INK + (255,), anchor="mm")
    # small shine top-left
    sh = Image.new("RGBA", (D, D), (0, 0, 0, 0))
    ImageDraw.Draw(sh).ellipse((D * 0.16, D * 0.12, D * 0.42, D * 0.3), fill=(255, 255, 255, 70))
    big = Image.alpha_composite(big, sh.filter(ImageFilter.GaussianBlur(D * 0.03)))
    return big.resize((d, d), Image.LANCZOS)


def brand_bar(L, t, total):
    L.put(logo_sprite(66), 104, BAR_Y)
    wm = text_sprite("POUND FOR POUND", 30, Wt)
    L.put(wm, 152 + wm.width / 2, BAR_Y - 14)
    tg = text_sprite("UK MONEY · EXPLAINED WITH DATA", 18, M, "ExtraBold")
    L.put(tg, 152 + tg.width / 2, BAR_Y + 20)
    if EPISODE:
        lab = f"#{EPISODE}"
        w = int(text_width(lab, 24) + 34)
        sp, _ = rrect_sprite(w, 44, 22, (255, 255, 255, 18), G + (200,), 2)
        L.put(sp, X1 - w / 2, BAR_Y)
        L.text(lab, X1 - w / 2, BAR_Y + 1, 24, G)
    track, _ = rrect_sprite(X1 - X0, 6, 3, (255, 255, 255, 46))
    L.put(track, W / 2, PROGRESS_Y)
    fw = max(6, int((X1 - X0) * clamp(t / total)))
    fill, _ = rrect_sprite(fw, 6, 3, G + (255,))
    L.put(fill, X0 + fw / 2, PROGRESS_Y)


# ---- chips, stamps, cards -----------------------------------------------------------------------------------
def chip(L, label, cx, cy, t, start, tone="white", size=30, emoji=None, static=False, outline=False):
    """Pill label. tone: green | white | red | cyan | gold. outline=True draws a ghost pill."""
    p = 1.0 if static else spring(t, start)
    if p <= 0:
        return
    col = TONES[tone]
    tw = text_width(label, size)
    ew = size * 1.25 if emoji else 0
    w, h = int(tw + ew + size * 1.4), int(size * 1.9)
    if outline:
        sp, _ = rrect_sprite(w, h, h // 2, col + (28,), col + (220,), 3)
        txt = col
    else:
        sp, _ = rrect_sprite(w, h, h // 2, col + (255,))
        txt = INK
    s = 0.6 + 0.4 * p
    a = clamp(p * 1.5)
    L.put(sp, cx, cy, a, s)
    x = cx - (w * s) / 2 + size * 0.7 * s
    if emoji:
        L.put(emoji_sprite(emoji, int(size * 1.1)), x + size * 0.55 * s, cy, a, s)
        x += ew * s
    L.text(label, x + tw * s / 2, cy + 1, size, txt, a, s)


def beat(L, key_or_label, t, start, tone=None, sub=None, sub_at=None):
    """The beat chip at the top of every scene (fixed position). key: one of BEATS, or free text."""
    label, default_tone = BEATS.get(key_or_label, (key_or_label, "white"))
    chip(L, label, W / 2, BEAT_Y, t, start, tone or default_tone, 30)
    if sub:
        L.text(sub, W / 2, BEAT_Y + 62, 30, M, ramp(t, sub_at if sub_at is not None else start + 0.2, 0.3),
               weight="ExtraBold")


def checked(L, text, cx, cy, t, start, static=False):
    """Source stamp: ✓ CHECKED · GOV.UK · 20 OCT 2026. Show it when an official figure appears."""
    chip(L, text.upper(), cx, cy, t, start, "green", 22, emoji="check_mark_button", static=static, outline=True)


def panel(L, cx, cy, w, h, t, start, tone=None, r=26, static=False):
    """Glass card. tone None = white hairline; green/red/cyan = coloured border with glow. Returns alpha."""
    p = 1.0 if static else spring(t, start)
    if p <= 0:
        return 0.0
    if tone:
        col = TONES[tone]
        sp, _ = rrect_sprite(int(w), int(h), r, (255, 255, 255, 14), col + (255,), 3, col + (140,))
    else:
        sp, _ = rrect_sprite(int(w), int(h), r, (255, 255, 255, 13), (255, 255, 255, 64), 3)
    a = clamp(p * 1.4)
    L.put(sp, cx, cy + (1 - p) * 30, a)
    return a


def value_card(L, cx, cy, w, t, start, emoji, label, value, color=None, value_at=None, h=150, tone=None, sub=None):
    """Card: emoji left, muted label + big value. The value pops in on value_at (the spoken word)."""
    color = color or G
    a = panel(L, cx, cy, w, h, t, start, tone)
    if a <= 0:
        return
    left = cx - w / 2
    if emoji:
        L.emoji(emoji, left + 80, cy, 96, t, start + 0.08)
        lx = left + 150
    else:
        lx = left + 40
    lab = text_sprite(label, 26, M, "ExtraBold")
    L.put(lab, lx + lab.width / 2, cy - 30, a)
    if sub:
        sb = text_sprite(sub, 24, M, "ExtraBold")
        L.put(sb, lx + sb.width / 2, cy + 30, a)
    pa = a if value_at is None else clamp(spring(t, value_at) * 1.3)
    if pa > 0:
        pr = text_sprite(value, 64, tuple(color))
        if sub:  # value right-aligned when there is a sub line
            L.put(pr, cx + w / 2 - 40 - pr.width / 2, cy + 10 * (1 - pa), pa)
        else:
            L.put(pr, lx + pr.width / 2, cy + 22 + 14 * (1 - pa), pa)


@lru_cache(maxsize=64)
def glow_sprite(s, size, color):
    base = text_sprite(s, size, color)
    pad = int(size * 0.5)
    g = Image.new("RGBA", (base.width + 2 * pad, base.height + 2 * pad), (0, 0, 0, 0))
    a = base.getchannel("A").point(lambda v: int(v * 0.55))
    layer = Image.new("RGBA", base.size, tuple(color) + (0,))
    layer.putalpha(a)
    g.alpha_composite(layer, (pad, pad))
    return g.filter(ImageFilter.GaussianBlur(size * 0.18))


def big_number(L, s, cx, cy, t, at=None, size=190, color=None, maxw=920, alpha=1.0, glow=True):
    """The brand's hero number: huge, accent colour, glowing; pulses when it is spoken (at)."""
    color = color or G
    tw = text_width(s, size)
    if tw > maxw:
        size = size * maxw / tw
    bump = 0.0
    if at is not None and t >= at:
        x = t - at
        bump = math.sin(min(x / 0.35, 1) * math.pi) * 0.09
    if glow:
        L.put(glow_sprite(s, int(size), tuple(color)), cx, cy, alpha * 0.9, 1 + bump)
    L.text(s, cx, cy, size, color, alpha, 1 + bump)


def timed_line(L, tokens, cx, cy, size, t, gap=None):
    """A maths line whose tokens each appear on their own spoken word.
    tokens: [(text, color, at)], e.g. [("=", M, tk(4, "365")), ("365", Wt, tk(4, "365")), ...]."""
    gap = size * 0.32 if gap is None else gap
    widths = [text_width(s, size) for s, _, _ in tokens]
    x = cx - (sum(widths) + gap * (len(tokens) - 1)) / 2
    for (s, col, at), w in zip(tokens, widths):
        p = spring(t, at)
        if p > 0:
            L.text(s, x + w / 2, cy + 20 * (1 - clamp(p)), size, col, clamp(p * 1.3))
        x += w + gap


def underline(L, cx, cy, w, t, start, color=None, dur=0.35):
    color = color or G
    p = ease(ramp(t, start, dur))
    if p <= 0:
        return
    sp, _ = rrect_sprite(max(8, int(w * p)), 10, 5, tuple(color) + (255,))
    L.put(sp, cx - w / 2 + w * p / 2, cy)


# ---- signature scenes ------------------------------------------------------------------------------------
def hook(L, t, lines, number, sub=None, emoji=None, number_at=None, stamp=None, extra=None):
    """Signature hook frame. Fully visible on frame 0 (it is also the loop target and the cover frame).
    lines: 1-2 short headline lines (<= 22 characters each). number: the payoff, e.g. "£667.95".
    extra: optional fn(L, t) for one small element revealed later in the hook (e.g. a red chip)."""
    if emoji:
        L.put(emoji_sprite(emoji, 170), W / 2, 470 + 8 * math.sin(t * 2.6))
    y = 650
    for ln in lines:
        size = 66 if text_width(ln, 66) <= 900 else 66 * 900 / text_width(ln, 66)
        L.text(ln, W / 2, y, size, Wt)
        y += 84
    ny = y + 120
    big_number(L, number, W / 2, ny, t, number_at)
    if number_at is not None:
        underline(L, W / 2, ny + 112, min(700, text_width(number, 190) * 0.8), t, number_at + 0.1)
    if sub:
        L.text(sub, W / 2, ny + 165, 40, M, weight="ExtraBold")
    if stamp:
        checked(L, stamp, W / 2, 1215, t, 0, static=True)
    if extra:
        extra(L, t)


COVER_HOLD = 0.45  # seconds the clean cover stays on screen before the hook builds on it
DRAW_COVER_BG = True
_cov = None


def cover_layers():
    """(sharp backdrop, darkened blurred backdrop, title sprite) for this video's COVER, built once."""
    global _cov
    if _cov is None:
        import cover as Cv
        c = Mo.SCENE.COVER
        bg = Cv.backdrop(THEME_KEY, c["hero"], c.get("left"), c.get("right"), c.get("particles"),
                         "|".join(c["words"]), c.get("fill"), c.get("env", "city")).convert("RGBA")
        dark = ImageEnhance.Brightness(bg.filter(ImageFilter.GaussianBlur(9))).enhance(0.42)
        ttl = Cv.title(tuple(c["words"]), c.get("highlight", 0), tuple(PAL["highlight"]))
        _cov = (bg, dark, ttl)
    return _cov


def cover_hook(L, t, number, sub=None, number_at=None, kicker=None, extra=None):
    """Signature opening for videos with a COVER (every brand video from 21 Oct 2026).
    Frame 0 is the clean cover: the illustrated scene + the 1-2 cover words. After COVER_HOLD the scene
    dims and blurs, the words shrink to the top and the payoff number lands. The loop returns here."""
    import cover as Cv
    bg, dark, ttl = cover_layers()
    p = ease(ramp(t, COVER_HOLD, 0.45))
    zoom = 1 + 0.045 * clamp(t / 9)
    if DRAW_COVER_BG:  # qa.py turns this off to lint only the elements drawn on top of the scene
        L.put(bg, W / 2, H / 2, 1.0, zoom)
        if p > 0:
            L.put(dark, W / 2, H / 2, p, zoom)
    ty = Cv.TITLE_Y + (470 - Cv.TITLE_Y) * p
    L.put(ttl, Cv.TITLE_X + (W / 2 - Cv.TITLE_X) * p, ty, 1.0, 1 - 0.44 * p)
    if p <= 0:
        return
    if kicker:
        L.text(kicker, W / 2, 690, 44, Wt, ramp(t, COVER_HOLD + 0.3, 0.3), shadow=True)
    q = spring(t, COVER_HOLD + 0.35)
    if q > 0:
        big_number(L, number, W / 2, 860 + 30 * (1 - clamp(q)), t, number_at, alpha=clamp(q * 1.4))
        if number_at is not None:
            underline(L, W / 2, 972, min(700, text_width(number, 190) * 0.8), t, number_at + 0.1)
        if sub:
            L.text(sub, W / 2, 1030, 40, Wt, clamp(q * 1.4), weight="ExtraBold", shadow=True)
    if extra:
        extra(L, t)


def your_turn(L, t, si, lines, answer_shape="= £?", hint=None, comment_word="Comment", label="COMMENT YOUR ANSWER"):
    """Signature comment card. Never show the answer. si: the sentence index of the question."""
    beat(L, "turn", t, Mo.S(si))
    L.emoji("thinking_face", W / 2, 500, 150, t, Mo.S(si) + 0.1)
    y = 690
    for i, ln in enumerate(lines):
        L.text(ln, W / 2, y + 20 * (1 - clamp(spring(t, Mo.S(si) + 0.25 + 0.12 * i))), 58, Wt,
               clamp(spring(t, Mo.S(si) + 0.25 + 0.12 * i) * 1.3))
        y += 78
    q = spring(t, Mo.S(si) + 0.6)
    if q > 0:
        L.text(answer_shape, W / 2, y + 90, 150, G, clamp(q * 1.3), 0.7 + 0.3 * q)
    if hint:
        L.text(hint, W / 2, y + 190, 30, M, ramp(t, Mo.S(si) + 0.8, 0.3), weight="ExtraBold")
    c = Mo.tk(si, comment_word)
    chip(L, label, 470, 1170, t, c, "white", 30, emoji="speech_balloon")
    L.arrow(800, 1185, 950, 1300, ease(ramp(t, c + 0.3, 0.45)), Wt, 6)


def share_close(L, t, si, lines, follow="FOLLOW FOR DAILY MONEY MATHS"):
    """Signature share end card — the last scene of every Short. si: the 'Send this to…' sentence.
    lines: who to send it to, 1-2 lines (<= 24 characters each), e.g. ["the friend who says", "pennies don't matter"]."""
    st = Mo.S(si)
    beat(L, "share", t, st - 0.1)
    p = spring(t, st)
    if p > 0:
        ring = circle_sprite(250, G + (36,), G + (255,), 5)
        L.put(ring, W / 2, 520, clamp(p * 1.4), 0.6 + 0.4 * p)
        L.emoji("envelope", W / 2, 515, 150, t, st + 0.05, bounce=True)
    y = 730
    for i, ln in enumerate(lines):
        q = spring(t, st + 0.2 + 0.12 * i)
        if q > 0:
            L.text(ln, W / 2, y + 20 * (1 - clamp(q)), 60, Wt if i == 0 else G, clamp(q * 1.3))
        y += 80
    # arrow towards the share button column (right edge, lower half)
    L.arrow(850, 960, 955, 1310, ease(ramp(t, st + 0.5, 0.5)), G, 7)
    f = ramp(t, st + 0.7, 0.35)
    if f > 0:
        tw = text_width(follow, 30)
        x0 = 480 - (84 + 18 + tw) / 2
        L.put(logo_sprite(84), x0 + 42, 1190, f)
        L.text(follow, x0 + 84 + 18 + tw / 2, 1191, 30, Wt, f)


def verdict_stamp(L, word, cx, cy, t, start, tone="red", size=120, angle=-8):
    """A rubber-stamp verdict (MYTH / FALSE / TRUE / HALF TRUE) that slams in at `start`."""
    p = spring(t, start, damping=18, stiffness=260)
    if p <= 0:
        return
    col = TONES[tone]
    tw = text_width(word, size)
    w, h = int(tw + size * 0.9), int(size * 1.45)
    im = Image.new("RGBA", (w + 40, h + 40), (0, 0, 0, 0))
    box, pad = rrect_sprite(w, h, int(size * 0.18), col + (34,), col + (255,), 9)
    im.alpha_composite(box, (20 - pad, 20 - pad))
    tx = text_sprite(word, size, col)
    im.alpha_composite(tx, (int(20 + w / 2 - tx.width / 2), int(20 + h / 2 - tx.height / 2)))
    im = im.rotate(angle, Image.BICUBIC, expand=True)
    s = 1.0 + 0.6 * (1 - clamp(p))
    L.put(im, cx, cy, clamp(p * 2), s)


def take_card(L, t, si, lines, label="MY TAKE", cy=760):
    """The owner's own take (BRAND.md §7): a gold-edged quote card. si: the sentence that says it."""
    st = Mo.S(si)
    a = panel(L, W / 2, cy, 900, 120 + 70 * len(lines), t, st - 0.1, "gold")
    if a <= 0:
        return
    top = cy - (120 + 70 * len(lines)) / 2
    chip(L, label, W / 2, top, t, st - 0.05, "gold", 28)
    L.text("\u201c", 150, top + 70, 120, GOLD, a)
    for i, ln in enumerate(lines):
        q = clamp(spring(t, st + 0.15 + 0.12 * i) * 1.3)
        L.text(ln, W / 2, top + 95 + 70 * i + 12 * (1 - q), 46, Wt, q)


_LOOP_SEEN = False


def loop_close(L, t, si, comment=None):
    """Last scene of every brand-v2 Short. The last line is spoken while the picture rebuilds the cover,
    so the end runs straight back into frame 0 (and the last line runs into the first one).
    comment: optional short chip text, e.g. "LEAP YEAR TOTAL? COMMENT ↓" (no arrows: use words)."""
    import cover as Cv
    st = Mo.S(si)
    end = Mo.T["total"] - LOOP
    bg, dark, ttl = cover_layers()
    back = ease(ramp(t, end - 1.3, 1.2))  # 0 -> 1: dimmed scene -> the clean cover
    if DRAW_COVER_BG:
        L.put(bg, W / 2, H / 2, 1.0)
        L.put(dark, W / 2, H / 2, 1 - back)
    ty = 470 + (Cv.TITLE_Y - 470) * back
    L.put(ttl, W / 2 + (Cv.TITLE_X - W / 2) * back, ty, ramp(t, st, 0.3), 0.56 + 0.44 * back)
    global _LOOP_SEEN
    _LOOP_SEEN = True
    if comment:
        fade = 1 - ramp(t, end - 1.4, 0.3)
        if fade > 0:
            sub = Layer()
            chip(sub, comment, W / 2, 900, t, st + 0.2, "white", 32, emoji="speech_balloon")
            L.put(sub.im, W / 2, H / 2, fade)


def caveat(L, t, start, lines, cy=1150, size=28):
    for i, ln in enumerate(lines):
        L.text(ln, W / 2, cy + i * 42, size, M, ramp(t, start + 0.08 * i, 0.3), weight="ExtraBold")


def versus(L, t, left, right, cy=700, h=300, w=420):
    """Two cards side by side with a VS coin between. Keep cy + h/2 above 900 (button column).
    left/right: dict(title, label, value, color, start, at, tone, emoji)."""
    for side, cx in ((left, W / 2 - w / 2 - 30), (right, W / 2 + w / 2 + 30)):
        a = panel(L, cx, cy, w, h, t, side["start"], side.get("tone"))
        if a <= 0:
            continue
        top = cy - h / 2
        if side.get("emoji"):
            L.emoji(side["emoji"], cx, top + 66, 84, t, side["start"] + 0.05)
        L.text(side["title"], cx, top + 140, 36, Wt, a)
        if side.get("label"):
            L.text(side["label"], cx, top + 190, 24, M, a, weight="ExtraBold")
        q = clamp(spring(t, side.get("at", side["start"])) * 1.3)
        if q > 0:
            L.text(side["value"], cx, top + h - 62 + 12 * (1 - q), 64, side.get("color", G), q)
    p = spring(t, min(left["start"], right["start"]) + 0.15)
    if p > 0:
        L.put(circle_sprite(86, INK + (255,), (255, 255, 255, 120), 3), W / 2, cy, clamp(p * 1.4), 0.6 + 0.4 * p)
        L.text("VS", W / 2, cy + 1, 30, Wt, clamp(p * 1.4), 0.6 + 0.4 * p)


# ---- charts ------------------------------------------------------------------------------------------------
def bar_chart(L, t, start, values, labels, box, colors, dur=1.0, value_tags=None, label_size=24, gap=0.28,
              vmax=None, stagger=0.0):
    """Vertical bars growing up from the baseline. box=(x0, y_top, x1, y_base).
    value_tags: {index: (text, color, at)} — a value label above that bar, revealed at `at`."""
    x0, yt, x1, yb = box
    n = len(values)
    vmax = vmax or max(values)
    slot = (x1 - x0) / n
    bw = slot * (1 - gap)
    a = ramp(t, start, 0.3)
    if a <= 0:
        return
    left, top = int(x0 - 10), int(yt - 10)
    big = Image.new("RGBA", (int(x1 - x0 + 20) * SS, int(yb - yt + 20) * SS), (0, 0, 0, 0))
    d = ImageDraw.Draw(big)
    P = lambda x, y: ((x - left) * SS, (y - top) * SS)
    d.line([P(x0, yb), P(x1, yb)], fill=(255, 255, 255, 110), width=2 * SS)
    for i, v in enumerate(values):
        g = ease(ramp(t, start + 0.15 + i * stagger, dur))
        if g <= 0:
            continue
        h = (yb - yt) * v / vmax * g
        cx = x0 + slot * (i + 0.5)
        col = tuple(colors[i] if isinstance(colors, (list, tuple)) and isinstance(colors[0], tuple) else colors)
        r = min(bw / 2, 12)
        if h > 2 * r:
            d.rounded_rectangle([P(cx - bw / 2, yb - h), P(cx + bw / 2, yb)], radius=r * SS, fill=col + (255,))
            d.rectangle([P(cx - bw / 2, yb - r), P(cx + bw / 2, yb)], fill=col + (255,))
        elif h > 0:
            d.rectangle([P(cx - bw / 2, yb - h), P(cx + bw / 2, yb)], fill=col + (255,))
    sp = big.resize((int(x1 - x0 + 20), int(yb - yt + 20)), Image.LANCZOS)
    L.put(sp, left + sp.width / 2, top + sp.height / 2, a)
    for i, lab in enumerate(labels):
        if lab:
            L.text(lab, x0 + slot * (i + 0.5), yb + 30, label_size, M, a, weight="ExtraBold")
    for i, (txt, col, at) in (value_tags or {}).items():
        q = spring(t, at)
        if q > 0:
            h = (yb - yt) * values[i] / vmax
            L.text(txt, x0 + slot * (i + 0.5), yb - h - 34 + 12 * (1 - clamp(q)), 40, col, clamp(q * 1.3))


def line_chart(L, t, start, dur, series, box, xmax, ymax, x_labels=(), y_labels=(), end_tags=()):
    """Lines drawn left to right. series: [(points [(x, y)...], color, width)]. box=(x0, y_top, x1, y_base).
    x_labels/y_labels: [(value, text)]. end_tags: [(series_index, text, color, at, dy)] at the line ends."""
    x0, yt, x1, yb = box
    X = lambda x: x0 + (x1 - x0) * x / xmax
    Y = lambda y: yb - (yb - yt) * y / ymax
    a = ramp(t, start - 0.2, 0.3)
    if a <= 0:
        return
    left, top = int(x0 - 20), int(yt - 20)
    w, h = int(x1 - x0 + 40), int(yb - yt + 40)
    big = Image.new("RGBA", (w * SS, h * SS), (0, 0, 0, 0))
    d = ImageDraw.Draw(big)
    P = lambda x, y: ((X(x) - left) * SS, (Y(y) - top) * SS)
    for v, _ in y_labels:
        d.line([P(0, v), P(xmax, v)], fill=(255, 255, 255, 28), width=2 * SS)
    d.line([P(0, 0), P(xmax, 0)], fill=(255, 255, 255, 110), width=2 * SS)
    p = ease(ramp(t, start, dur))
    for pts, col, lw in series:
        upto = pts[0][0] + (pts[-1][0] - pts[0][0]) * p
        seg = [pt for pt in pts if pt[0] <= upto]
        if len(seg) >= 1 and seg[-1][0] < upto:
            # interpolate the moving tip
            j = len(seg)
            if j < len(pts):
                (xa, ya), (xb, yb2) = pts[j - 1], pts[j]
                f = (upto - xa) / (xb - xa)
                seg = seg + [(upto, ya + (yb2 - ya) * f)]
        if len(seg) >= 2:
            d.line([P(*pt) for pt in seg], fill=tuple(col) + (255,), width=lw * SS, joint="curve")
            ex, ey = P(*seg[-1])
            rr = lw * SS * 1.3
            d.ellipse((ex - rr, ey - rr, ex + rr, ey + rr), fill=tuple(col) + (255,))
    sp = big.resize((w, h), Image.LANCZOS)
    L.put(sp, left + w / 2, top + h / 2, a)
    for v, txt in x_labels:
        L.text(txt, X(v), yb + 32, 24, M, a, weight="ExtraBold")
    for v, txt in y_labels:
        tx = text_sprite(txt, 24, M, "ExtraBold")
        L.put(tx, x0 - 18 - tx.width / 2, Y(v), a)
    for si_, txt, col, at, dy in end_tags:  # label just right of the line's end point
        q = spring(t, at)
        if q > 0:
            px, py = series[si_][0][-1]
            sp2 = text_sprite(txt, 44, tuple(col))
            L.put(sp2, X(px) + 26 + sp2.width / 2, Y(py) + dy + 12 * (1 - clamp(q)), clamp(q * 1.3))


# ---- captions -------------------------------------------------------------------------------------------------
def captions(L, t, groups, cy=CAPTION_Y, size=60, maxw=840):
    cur = None
    for i, g in enumerate(groups):
        end = groups[i + 1][0]["start"] if i + 1 < len(groups) else g[-1]["end"] + 0.6
        if g[0]["start"] - 0.05 <= t < min(end, g[-1]["end"] + 0.5):
            cur = (g, end)
    if not cur:
        return
    g, end = cur
    a = min(ramp(t, g[0]["start"] - 0.05, 0.12), 1 - ramp(t, min(end, g[-1]["end"] + 0.5) - 0.1, 0.1))
    words = [tk_["text"] for tk_ in g]
    widths = [text_width(w_, size) for w_ in words]
    gap = size * 0.3
    total = sum(widths) + gap * (len(words) - 1)
    sz = size if total <= maxw else size * maxw / total
    if sz != size:
        widths = [text_width(w_, sz) for w_ in words]
        gap = sz * 0.3
        total = sum(widths) + gap * (len(words) - 1)
    x = W / 2 - total / 2
    for tk_, w_, wd in zip(g, words, widths):
        active = tk_["start"] - 0.03 <= t < tk_["end"]
        L.text(w_, x + wd / 2, cy, sz, G if active else Wt, a, shadow=True)
        x += wd + gap


# ---- frame ----------------------------------------------------------------------------------------------------
_first = None


def _content(t):
    scenes = Mo.SCENE.SCENES
    k = 0
    for i, (a, b) in enumerate(scenes):
        if t >= Mo.S(a) - 0.001:
            k = i
    start = Mo.S(scenes[k][0]) if k > 0 else 0.0
    end = Mo.S(scenes[k + 1][0]) if k + 1 < len(scenes) else Mo.T["total"] + 1
    alpha = min(ramp(t, start, 0.35) if k > 0 else 1.0, 1 - ramp(t, end - 0.27, 0.27))
    sc = Layer()
    Mo.SCENE.DRAW[k](sc, t)
    return with_alpha(sc.im, alpha)


def frame(t, captions_on=True):
    global _first
    total = Mo.T["total"]
    has_cover = getattr(Mo.SCENE, "COVER", None) is not None
    lp = ramp(t, total - LOOP, LOOP)
    img = Mo.background(t)
    content = _content(t)
    if lp > 0:  # seamless loop: dissolve into the hook frame exactly as it is on frame 0
        if _first is None:
            _first = _content(0.0)
        content = Image.blend(content, _first, lp)  # linear mix: no dip to the plain background
    img.alpha_composite(content)
    bar_a = (ramp(t, COVER_HOLD, 0.4) if has_cover else 1.0) * (1 - lp if has_cover else 1.0)
    if has_cover and _LOOP_SEEN:
        bar_a *= 1 - ramp(t, total - LOOP - 1.3, 1.2)  # the bar leaves as the cover rebuilds
    if bar_a > 0:  # the cover itself stays clean: no logo bar, no captions on frame 0
        base = Layer()
        brand_bar(base, t, total)
        img.alpha_composite(with_alpha(base.im, bar_a))
    if captions_on and not (has_cover and t < COVER_HOLD):
        cap = Layer()
        captions(cap, t, Mo.GROUPS)
        img.alpha_composite(cap.im)
    return img.convert("RGB")


def scene_events(extra=()):
    """Standard sound design: a whoosh into every scene and the brand sting on the share card."""
    scenes = Mo.SCENE.SCENES
    ev = [{"t": max(0, Mo.S(a) - 0.15), "kind": "whoosh"} for a, _ in scenes[1:]]
    ev.append({"t": Mo.S(scenes[-1][0]) + 0.05, "kind": "sting"})
    return ev + list(extra)
