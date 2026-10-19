"""Scenes for video 001: '£5 a day could grow to £178K' (Stocks & Shares ISA, 7% a year)."""
from vidlib import *  # noqa: F401,F403
import vidlib as V

# ---- figures -------------------------------------------------------------------
MONTHLY = 5 * 365 / 12
R_M = 1.07 ** (1 / 12) - 1


def paid(y):
    return MONTHLY * 12 * y


def pot(y):
    n = y * 12
    return MONTHLY * ((1 + R_M) ** n - 1) / R_M if n > 0 else 0.0


POT30, PAID30 = pot(30), paid(30)
GROWTH_PCT = (POT30 - PAID30) / POT30 * 100




# ---- scenes ----------------------------------------------------------------------
def s_hook(L, d, t):
    s0 = V.T["sentences"][0]
    a = back((t - s0["start"]) / 0.25)
    sc = 1.25 - 0.25 * a
    centered(d, 430, "£5 A DAY", font("Black", 150 * sc), WHITE, stroke=0)
    could = find_tok(0, "could")
    if t >= could["start"]:
        chevrons(d, W // 2, 560, t)
    big = find_tok(0, "£178K")
    if t < big["start"] - 0.1:
        q = 0.55 + 0.45 * abs(math.sin(t * 5))
        centered(d, 860, "£???,???", font("Black", 150), tuple(int(c * q) for c in YELLOW))
    if t >= big["start"] - 0.1:
        p = ease((t - big["start"] + 0.1) / max(0.4, big["end"] - big["start"]))
        glow_text(L, 860, money(POT30 * p), font("Black", 175), YELLOW, scale=1.0 + 0.12 * (1 - back((t - big["start"]) / 0.3)))
        if p >= 1:
            centered(d, 1010, "in 30 years", font("Bold", 64), SOFT)


def s_how(L, d, t, st):
    a = back((t - st) / 0.22)
    centered(d, 520, "HERE'S", font("Black", 170 * (0.6 + 0.4 * a)), WHITE)
    centered(d, 700, "HOW", font("Black", 210 * (0.6 + 0.4 * a)), YELLOW)
    chevrons(d, W // 2, 860, t)


def s_month(L, d, t, st):
    k = find_tok(2, "£152")
    p = back((t - k["start"] + 0.05) / 0.25)
    if t >= k["start"] - 0.05:
        glow_text(L, 600, money(MONTHLY), font("Black", 270), YELLOW, scale=0.7 + 0.3 * p)
    centered(d, 820, "A MONTH", font("Black", 96), WHITE)
    centered(d, 950, "£5 × 365 days ÷ 12", font("SemiBold", 54), MUTED)


def s_isa(L, d, t, st):
    a = back((t - st) / 0.25)
    f = font("Black", 64)
    label = "STOCKS & SHARES ISA"
    w = text_w(label, f) + 80
    x0, y0 = (W - w) / 2, 420 - (1 - a) * 60
    d.rounded_rectangle((x0, y0, x0 + w, y0 + 120), 60, fill=YELLOW)
    centered(d, y0 + 60, label, f, INK)
    k = find_tok(3, "30")
    yr = int(round(30 * ease((t - k["start"] + 0.9) / 0.9))) if t >= k["start"] - 0.9 else 0
    centered(d, 760, f"{yr}", font("Black", 320), WHITE)
    centered(d, 960, "YEARS · NO TOUCHING", font("Black", 62), SOFT)


def s_paid(L, d, t, st):
    k = find_tok(4, "£55K")
    centered(d, 470, "YOU PAY IN", font("Black", 92), WHITE)
    p = ease((t - k["start"]) / max(0.5, k["end"] - k["start"])) if t >= k["start"] else 0
    glow_text(L, 680, money(PAID30 * p), font("Black", 190), WHITE, glow=PAID, radius=24, strength=1)
    bar_w = 760 * p
    d.rounded_rectangle((160, 860, 160 + max(24, bar_w), 920), 30, fill=PAID)
    d.ellipse((160, 975, 196, 1011), fill=PAID)
    d.text((214, 968), "your money", font=font("SemiBold", 48), fill=SOFT)


CH = dict(x0=150, x1=930, y0=1110, y1=560, ymax=200_000)


def cx(y):
    return CH["x0"] + (CH["x1"] - CH["x0"]) * y / 30


def cy(v):
    return CH["y0"] - (CH["y0"] - CH["y1"]) * v / CH["ymax"]


def chart_years(t):
    """Years of growth drawn at time t across sentences 5-8."""
    s5, s6, s7, s8 = (V.T["sentences"][i] for i in (5, 6, 7, 8))
    m10, m20, m30 = find_tok(6, "£26K"), find_tok(7, "£77K"), find_tok(8, "£178K")
    keys = [(s5["start"] + 0.4, 0), (m10["start"], 10), (m20["start"], 20), (m30["start"], 30)]
    if t <= keys[0][0]:
        return 0.0
    for (ta, ya), (tb, yb) in zip(keys, keys[1:]):
        if t <= tb:
            return ya + (yb - ya) * ((t - ta) / max(0.1, tb - ta)) ** 1.15
    return 30.0


def s_chart(L, d, t, idx):
    # grid
    for v in (50_000, 100_000, 150_000, 200_000):
        y = cy(v)
        d.line((CH["x0"], y, CH["x1"], y), fill=(255, 255, 255, 40), width=2)
        lbl = f"£{v // 1000}k"
        f = font("SemiBold", 34)
        d.text((CH["x0"] - 16 - text_w(lbl, f), y - 21), lbl, font=f, fill=MUTED)
    d.line((CH["x0"], CH["y0"], CH["x1"], CH["y0"]), fill=MUTED, width=3)
    for yr in (0, 10, 20, 30):
        lbl = f"{yr}" if yr < 30 else "30 yrs"
        f = font("SemiBold", 34)
        d.text((cx(yr) - text_w(lbl, f) / 2, CH["y0"] + 14), lbl, font=f, fill=MUTED)
    # paid-in line draws in fast at the start of the chart
    pin = ease((t - V.T["sentences"][5]["start"]) / 0.6) * 30
    if pin > 0:
        d.line([(cx(0), cy(0)), (cx(pin), cy(paid(pin)))], fill=PAID, width=8)
    yrs = chart_years(t)
    if yrs > 0:
        steps = max(2, int(yrs * 8))
        pts = [(cx(yrs * i / steps), cy(pot(yrs * i / steps))) for i in range(steps + 1)]
        ov = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        ImageDraw.Draw(ov).polygon(pts + [(pts[-1][0], CH["y0"]), (pts[0][0], CH["y0"])], fill=GROWTH + (70,))
        L.alpha_composite(ov)
        d.line(pts, fill=GROWTH, width=10, joint="curve")
        ex, ey = pts[-1]
        d.ellipse((ex - 16, ey - 16, ex + 16, ey + 16), fill=WHITE, outline=GROWTH, width=6)
    # milestones
    for si, y, k in ((6, 10, "£26K"), (7, 20, "£77K"), (8, 30, "£178K")):
        tk = find_tok(si, k)
        if t >= tk["start"]:
            a = back((t - tk["start"]) / 0.25)
            px, py = cx(y), cy(pot(y))
            lbl = f"£{pot(y) / 1000:.0f}K"
            f = font("Black", int(52 * (0.5 + 0.5 * a)))
            tw = text_w(lbl, f)
            bx = min(CH["x1"] - tw - 30, max(CH["x0"], px - tw / 2 - 18))
            by = py - 100
            d.rounded_rectangle((bx, by, bx + tw + 36, by + 72), 18, fill=YELLOW)
            d.text((bx + 18, by + 8), lbl, font=f, fill=INK)
    # direct labels
    if pin >= 30:
        d.text((cx(30) - 175, cy(PAID30) + 18), "paid in", font=font("Bold", 42), fill=SOFT)
    # headline counter
    centered(d, 330, "YOUR POT", font("Black", 56), SOFT)
    glow_text(L, 440, money(pot(yrs)), font("Black", 130), YELLOW, radius=18, strength=1)


def s_split(L, d, t, st):
    a = back((t - st) / 0.25)
    glow_text(L, 500, f"{GROWTH_PCT:.0f}%", font("Black", 300), YELLOW, scale=0.7 + 0.3 * a)
    centered(d, 720, "OF THE POT IS GROWTH", font("Black", 76), WHITE)
    x0, x1, y0, y1 = 110, 970, 840, 950
    p = ease((t - st - 0.25) / 0.9)
    split = x0 + (x1 - x0) * (PAID30 / POT30)
    end = x0 + (x1 - x0) * p
    d.rounded_rectangle((x0, y0, min(split, end), y1), 14, fill=PAID)
    if end > split + 6:
        d.rounded_rectangle((split + 6, y0, end, y1), 14, fill=GROWTH)
    if p > 0.9:
        f = font("Bold", 46)
        d.ellipse((x0, 1000, x0 + 30, 1030), fill=PAID)
        d.text((x0 + 44, 990), f"You paid {money(PAID30)}", font=f, fill=SOFT)
        d.ellipse((x0, 1070, x0 + 30, 1100), fill=GROWTH)
        d.text((x0 + 44, 1060), f"Growth {money(POT30 - PAID30)}", font=f, fill=SOFT)


def s_tax(L, d, t, st):
    k = find_tok(10, "£0")
    centered(d, 460, "INSIDE AN ISA", font("Black", 80), SOFT)
    if t >= k["start"]:
        p = ease((t - k["start"]) / 0.14)
        sc = 2.3 - 1.3 * p
        stamp = Image.new("RGBA", (900, 520), (0, 0, 0, 0))
        sd = ImageDraw.Draw(stamp)
        sd.rounded_rectangle((20, 20, 880, 500), 40, outline=YELLOW, width=16)
        sd.text((450, 210), "£0", font=font("Black", 260), fill=YELLOW, anchor="mm")
        sd.text((450, 410), "TAX", font=font("Black", 130), fill=WHITE, anchor="mm")
        stamp = stamp.rotate(-6, resample=Image.BICUBIC, expand=True)
        sw, sh = int(stamp.width * sc), int(stamp.height * sc)
        stamp = stamp.resize((sw, sh), Image.BICUBIC)
        if p < 1:
            stamp.putalpha(stamp.getchannel("A").point(lambda v: int(v * (0.3 + 0.7 * p))))
        L.alpha_composite(stamp, (max(0, (W - sw) // 2), max(0, 800 - sh // 2)), (max(0, (sw - W) // 2), max(0, sh // 2 - 800)))
        centered(d, 1110, "on the growth", font("Bold", 60), SOFT)


def s_caveat(L, d, t, st):
    a = ease((t - st) / 0.25)
    d.rounded_rectangle((90, 420, 990, 1080), 40, fill=(10, 12, 30, int(220 * a)), outline=(255, 255, 255, int(60 * a)), width=3)
    centered(d, 520, "HEADS UP", font("Black", 70), YELLOW)
    lines = ["Returns aren't guaranteed.", "Investments can fall", "as well as rise.", "7% a year is an assumption.", "Not financial advice."]
    for i, ln in enumerate(lines):
        centered(d, 640 + i * 84, ln, font("SemiBold", 56), WHITE if i < 3 else SOFT)


def s_time(L, d, t, st):
    a = back((t - st) / 0.25)
    cxp, cyp, r = W // 2, 640, 250
    sweep = 360 * ease((t - st) / 1.4)
    d.arc((cxp - r, cyp - r, cxp + r, cyp + r), -90, -90 + sweep, fill=YELLOW, width=22)
    glow_text(L, cyp, "TIME", font("Black", 190), WHITE, glow=(0, 200, 255), radius=20, strength=1, scale=0.7 + 0.3 * a)
    centered(d, 990, "IS YOUR SUPERPOWER", font("Black", 72), YELLOW)


def s_follow(L, d, t, st):
    centered(d, 450, "A NEW MONEY IDEA", font("Black", 80), WHITE)
    centered(d, 550, "EVERY WEEK", font("Black", 80), YELLOW)
    pulse = 1 + 0.05 * math.sin((t - st) * 9)
    a = back((t - st) / 0.3)
    bw, bh = 620 * pulse * (0.6 + 0.4 * a), 170 * pulse * (0.6 + 0.4 * a)
    d.rounded_rectangle((W / 2 - bw / 2, 760 - bh / 2, W / 2 + bw / 2, 760 + bh / 2), bh / 2, fill=YELLOW)
    centered(d, 760, "FOLLOW", font("Black", 96 * pulse * (0.6 + 0.4 * a)), INK)
    centered(d, 940, "Pound for Pound", font("Bold", 58), SOFT)


def events():
    ev = []
    for i, s in enumerate(V.T["sentences"]):
        if i in (1, 2, 3, 4, 5, 9, 11, 12, 13):
            ev.append({"t": max(0, s["start"] - 0.12), "kind": "whoosh"})
    ev.append({"t": find_tok(0, "£5")["start"], "kind": "pop"})
    ev.append({"t": find_tok(0, "£178K")["end"], "kind": "coin"})
    ev.append({"t": find_tok(2, "£152")["start"], "kind": "pop"})
    ev.append({"t": find_tok(6, "£26K")["start"], "kind": "pop"})
    ev.append({"t": find_tok(7, "£77K")["start"], "kind": "pop"})
    ev.append({"t": find_tok(8, "£178K")["start"], "kind": "coin"})
    ev.append({"t": find_tok(8, "£178K")["start"], "kind": "crash"})
    ev.append({"t": find_tok(10, "£0")["start"], "kind": "boom"})
    return ev



NO_PUNCH = {6, 7, 8}


def shakes():
    return [find_tok(0, "£178K")["end"], find_tok(8, "£178K")["start"], find_tok(10, "£0")["start"] + 0.14]


def draw(L, d, t, si, st):
    if si == 0:
        s_hook(L, d, t)
    elif si == 1:
        s_how(L, d, t, st)
    elif si == 2:
        s_month(L, d, t, st)
    elif si == 3:
        s_isa(L, d, t, st)
    elif si == 4:
        s_paid(L, d, t, st)
    elif 5 <= si <= 8:
        s_chart(L, d, t, si)
    elif si == 9:
        s_split(L, d, t, st)
    elif si == 10:
        s_tax(L, d, t, st)
    elif si == 11:
        s_caveat(L, d, t, st)
    elif si == 12:
        s_time(L, d, t, st)
    else:
        s_follow(L, d, t, st)
