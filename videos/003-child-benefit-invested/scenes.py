"""003: What if you invested your baby's Child Benefit? (rates checked on gov.uk, 19 Oct 2026)

Child Benefit 2026/27: £27.05 a week for the eldest/only child, £17.90 for others; paid until 16 (under 20 in
approved education). HICBC: charge from £60,000, all repaid over £80,000. NI credits while the child is under 12.
Junior ISA limit 2026/27: £9,000; money locked until 18.
Assumption: 7% a year effective, compounded monthly, Child Benefit held at today's rate.
"""
from motion import *  # noqa: F401,F403
from PIL import Image, ImageDraw

BADGE, TITLE = "MONEY MATHS", "POUND FOR POUND"

# ---- figures --------------------------------------------------------------------------------------
WEEKLY, WEEKLY2 = 27.05, 17.90
R_M = 1.07 ** (1 / 12) - 1
MONTHLY = WEEKLY * 52 / 12
ANNUAL = WEEKLY * 52
PAID16 = ANNUAL * 16


def invested(age):
    """Pot value at a given age (contributions monthly from birth to 16)."""
    if age <= 0:
        return 0.0
    n = min(age, 16) * 12
    v = MONTHLY * ((1 + R_M) ** n - 1) / R_M
    return v * 1.07 ** max(0.0, age - 16)


def paid_in(age):
    return ANNUAL * min(max(age, 0), 16)


F16, F18, F30 = invested(16), invested(18), invested(30)


# ---- scenes ------------------------------------------------------------------------------------------
def s_hook(L, t):
    L.badge("WHAT IF YOU INVESTED IT?", 540, 300, t, -0.35, "white", 32)
    L.emoji("baby", 540, 500, 210, t, -0.3, bounce=True)
    L.text("your baby's Child Benefit", 540, 650, 40, M, ramp(t, -0.2, 0.2), weight="ExtraBold")
    st = tk(1, "£46,000")
    p = ease(ramp(t, st - 0.3, 0.9))
    if t >= st - 0.3:
        L.text(gbp(F18 * p), 540, 790, 130, G, clamp((t - st + 0.3) * 4))
        L.emoji("birthday_cake", 330, 915, 80, t, st + 0.6)
        L.text("by their 18th birthday", 590, 915, 38, Wt, ramp(t, st + 0.6, 0.25), weight="ExtraBold")
    L.badge("LET'S DO THE MATHS", 540, 1045, t, S(2), "green", 30)


def s_facts(L, t):
    L.badge("CHILD BENEFIT 2026/27", 540, 300, t, S(3))
    L.price_card("baby", "FIRST CHILD, PER WEEK", "£27.05", 540, 440, t, tk(3, "£27.05") - 0.15, w=720)
    L.price_card("calendar", "PAID UNTIL AGE", "16", 540, 610, t, tk(4, "16") - 0.15, w=720)
    L.text("or under 20 in approved education", 540, 712, 28, M, ramp(t, tk(4, "education"), 0.25), weight="ExtraBold")
    st = tk(5, "£1,406")
    L.math_line([("£27.05", Wt), ("×", M), ("52", Wt), ("=", M), ("£1,406.60", C)], 540, 820, 56, t, st - 0.3,
                stagger=0.1)
    L.text("a year · about £117 a month", 540, 890, 30, M, ramp(t, tk(5, "£117"), 0.25), weight="ExtraBold")
    L.math_line([("£1,406.60", Wt), ("×", M), ("16", Wt), ("=", M), (gbp(PAID16), G)], 540, 990, 56, t, S(6),
                stagger=clamp((tk(6, "£22,500") - S(6)) / 4, 0.08, 0.4))
    L.text("paid to you over 16 years", 540, 1058, 30, M, ramp(t, tk(6, "£22,500"), 0.25), weight="ExtraBold")


def chart(L, t, prog, a):
    ss = 2
    x0, x1, y0, y1 = 150, 930, 1020, 560
    ymax = 50_000
    X = lambda age: x0 + (x1 - x0) * age / 18
    Y = lambda v: y0 - (y0 - y1) * v / ymax
    left, top, right, bottom = 40, 500, 1040, 1080
    big = Image.new("RGBA", ((right - left) * ss, (bottom - top) * ss), (0, 0, 0, 0))
    d = ImageDraw.Draw(big)
    P = lambda x, y: ((x - left) * ss, (y - top) * ss)
    for v in (10_000, 20_000, 30_000, 40_000, 50_000):
        d.line([P(x0, Y(v)), P(x1, Y(v))], fill=(255, 255, 255, 28), width=2 * ss)
    d.line([P(x0, y0), P(x1, y0)], fill=(255, 255, 255, 110), width=2 * ss)
    if prog > 0:
        for fn, col in ((paid_in, C), (invested, G)):
            ages = [prog * i / 90 for i in range(91)]
            pts = [P(X(g), Y(fn(g))) for g in ages]
            d.line(pts, fill=col + (255,), width=7 * ss, joint="curve")
            ex, ey = pts[-1]
            r = 11 * ss
            d.ellipse((ex - r, ey - r, ex + r, ey + r), fill=col + (255,), outline=(14, 20, 48, 255), width=4 * ss)
    sp = big.resize((right - left, bottom - top), Image.LANCZOS)
    L.put(sp, (left + right) / 2, (top + bottom) / 2, a)
    for v in (10_000, 20_000, 30_000, 40_000, 50_000):
        L.text(f"£{v // 1000}K", 95, Y(v), 24, M, a, weight="ExtraBold")
    for age in (0, 4, 8, 12, 16, 18):
        L.text(str(age), X(age), 1058, 26, M, a, weight="ExtraBold")
    return X, Y


def s_invest(L, t):
    L.badge("JUNIOR STOCKS & SHARES ISA", 540, 300, t, S(7), "green", 30)
    a = ramp(t, S(7) + 0.3, 0.3)
    a16, a18 = tk(8, "16."), tk(9, "£46,000")
    if t < a16:
        prog = 16 * ease(ramp(t, S(8), max(0.5, a16 - S(8))))
    else:
        prog = 16 + 2 * ease(ramp(t, tk(9, "18"), max(0.4, a18 - tk(9, "18"))))
    X, Y = chart(L, t, prog, a)
    # legend
    for i, (lab, col, val) in enumerate((("INVESTED AT 7%", G, invested(prog)), ("JUST SAVED (0%)", C, paid_in(prog)))):
        y = 410 + i * 54
        L.put(circle_sprite(22, col + (255,)), 160, y, a)
        sp = text_sprite(f"{lab}: {gbp(val)}", 32, col)
        L.put(sp, 185 + sp.width / 2, y, a)
    # milestone pills
    for at, age, val in ((a16, 16, F16), (a18, 18, F18)):
        p = spring(t, at)
        if p > 0:
            lab = gbp(val)
            tw = text_width(lab, 34)
            pill, _ = rrect_sprite(int(tw + 34), 54, 27, G + (255,))
            x = min(X(age), 1030 - (tw + 34) / 2)
            dx, dy = (40, 72) if age == 16 else (0, -52)  # 16: below-right of the point, 18: above the end point
            L.put(pill, x + dx, Y(val) + dy, clamp(p * 1.4), 0.6 + 0.4 * p)
            L.text(lab, x + dx, Y(val) + dy + 1, 34, INK, clamp(p * 1.4), 0.6 + 0.4 * p)
    # leave it until 30
    st = tk(10, "£100,000") - 0.35
    p = spring(t, S(10) + 0.2)
    if p > 0:
        panel, _ = rrect_sprite(820, 300, 28, (22, 26, 70, 245), G + (255,), 3, G + (140,))
        L.put(panel, 540, 760, clamp(p * 1.4), 0.7 + 0.3 * p)
        L.emoji("rocket", 540, 670, 110, t, S(10) + 0.3)
        L.text("LEFT UNTIL AGE 30?", 540, 760, 36, M, clamp(p * 1.4), weight="ExtraBold")
        q = ease(ramp(t, st, 0.8))
        if t >= st:
            L.text(gbp(F30 * q), 540, 840, 92, G, clamp((t - st) * 4))


def s_tips(L, t):
    L.badge("2 THINGS PARENTS MISS", 540, 300, t, S(11), "white", 30)
    L.card(540, 540, 900, 350, t, S(12) - 0.1)
    L.badge("1 · EARN OVER £80K?", 540, 410, t, S(12), "green", 28)
    L.text("you'd repay it all through tax, but", 540, 478, 32, M, ramp(t, tk(12, "You'd"), 0.25), weight="ExtraBold")
    p = spring(t, tk(12, "claim"))
    if p > 0:
        L.text("STILL CLAIM IT", 540, 548 + 14 * (1 - clamp(p)), 70, G, clamp(p * 1.3))
    L.text("and opt out of the payments", 540, 615, 32, M, ramp(t, tk(12, "opt"), 0.25), weight="ExtraBold")
    L.text("+ NI credits for your State Pension (child under 12)", 540, 670, 28, C, ramp(t, tk(13, "National"), 0.3))
    L.card(540, 880, 900, 250, t, S(14) - 0.1)
    L.badge("2 · JUNIOR ISA LIMIT", 540, 800, t, S(14), "green", 28)
    q = spring(t, tk(14, "£9,000"))
    if q > 0:
        L.text("£9,000 a year", 540, 870 + 14 * (1 - clamp(q)), 66, G, clamp(q * 1.3))
    L.text("grandparents and family can pay in too", 540, 940, 30, M, ramp(t, tk(14, "grandparents"), 0.25),
           weight="ExtraBold")


def s_turn(L, t):
    L.badge("YOUR TURN", 540, 310, t, S(15), "green", 34)
    two = tk(15, "two")
    L.emoji("baby", 420, 470, 150, t, two)
    L.emoji("baby", 660, 470, 150, t, two + 0.12)
    L.math_line([("£27.05", Wt), ("+", M), ("£17.90", Wt)], 540, 630, 64, t, two + 0.3, stagger=0.14)
    L.text("a week, for two children", 540, 700, 30, M, ramp(t, two + 0.6, 0.25), weight="ExtraBold")
    e = tk(15, "eighteen")
    L.math_line([("=", M), ("?", G)], 540, 830, 140, t, e - 0.2, stagger=0.15)
    L.text("at 18, invested at 7% a year", 540, 935, 30, M, ramp(t, e, 0.25), weight="ExtraBold")
    c = tk(15, "Comment")
    L.badge("COMMENT YOUR GUESS", 470, 1045, t, c, "white", 30)
    L.arrow(780, 1045, 1000, 1150, ease(ramp(t, c + 0.3, 0.45)), Wt, 6)


def s_outro(L, t):
    lines = ["Illustration only. Assumes 7% a year after", "fees, and Child Benefit at today's rate.",
             "Investments can fall as well as rise.", "Not financial advice."]
    for i, ln in enumerate(lines):
        L.text(ln, 540, 330 + i * 52, 32, M, ramp(t, S(16) + 0.1 * i, 0.3), weight="ExtraBold")
    st = S(17)
    p = spring(t, st)
    if p > 0:
        ring = circle_sprite(280, (79, 195, 247, 40), (79, 195, 247, 255), 6)
        L.put(ring, 540, 760, clamp(p * 1.4), 0.6 + 0.4 * p)
        L.emoji("bell", 540, 755, 180, t, st + 0.05, bounce=True)
    L.text("FOLLOW FOR MORE", 540, 970, 58, Wt, ramp(t, st + 0.2, 0.3))


SCENES = [(0, 2), (3, 6), (7, 10), (11, 14), (15, 15), (16, 17)]
DRAW = [s_hook, s_facts, s_invest, s_tips, s_turn, s_outro]


def events():
    ev = [{"t": max(0, S(a) - 0.15), "kind": "whoosh"} for a, _ in SCENES[1:]]
    for si, p in ((3, "£27.05"), (4, "16"), (5, "£1,406"), (6, "£22,500"), (8, "16."), (12, "claim"), (14, "£9,000")):
        ev.append({"t": tk(si, p), "kind": "pop"})
    ev += [{"t": tk(1, "£46,000") + 0.6, "kind": "coin"}, {"t": tk(9, "£46,000"), "kind": "coin"},
           {"t": tk(10, "£100,000") + 0.45, "kind": "coin"}, {"t": tk(10, "£100,000") + 0.45, "kind": "crash"}]
    return ev
