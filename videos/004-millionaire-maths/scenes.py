"""004: Millionaire maths: how much a month to reach £1 million by 60, starting at 20, 30 or 40.
(figures checked 20 Oct 2026)

ISA allowance 2026/27: £20,000 a year, 18 or over (gov.uk/individual-savings-accounts).
Bank of England inflation target: 2% CPI (bankofengland.co.uk, MPC September 2026).
Assumption: 7% a year effective after fees, compounded monthly, paid in at the end of each month, to age 60.
"""
from motion import *  # noqa: F401,F403
from PIL import Image, ImageDraw

BADGE, TITLE = "MONEY MATHS", "POUND FOR POUND"

# ---- figures --------------------------------------------------------------------------------------
TARGET, END_AGE = 1_000_000, 60
R_M = 1.07 ** (1 / 12) - 1
ISA_LIMIT = 20_000
INFL = 0.02


def monthly_needed(start_age):
    n = (END_AGE - start_age) * 12
    return TARGET * R_M / ((1 + R_M) ** n - 1)


SAVERS = [("Lucy", "woman", 20), ("Tom", "man", 30), ("Maya", "woman", 40)]
NEED = {a: monthly_needed(a) for _, _, a in SAVERS}
PAID = {a: NEED[a] * (END_AGE - a) * 12 for _, _, a in SAVERS}
GROWTH_SHARE = {a: 1 - PAID[a] / TARGET for _, _, a in SAVERS}
REAL_40 = TARGET / (1 + INFL) ** 40
ISA_MONTH = ISA_LIMIT / 12
NEED_25 = monthly_needed(25)  # comment-question answer, never shown


def k(v):
    return f"£{round(v / 1000):,}K"


# ---- scenes ------------------------------------------------------------------------------------------
def s_hook(L, t):
    L.badge("MILLIONAIRE BY 60?", 540, 300, t, -0.35, "white", 32)
    L.emoji("money_bag", 540, 480, 190, t, -0.3, bounce=True)
    st = tk(0, "millionaire")
    p = ease(ramp(t, st - 0.2, 0.9))
    if t >= st - 0.2:
        L.text(gbp(TARGET * p), 540, 650, 120, G, clamp((t - st + 0.2) * 4))
    L.text("how much a month?", 540, 750, 42, M, ramp(t, tk(0, "sixty"), 0.25), weight="ExtraBold")
    L.price_card("calendar", "START AT 20, PER MONTH", gbp(NEED[20]), 540, 900, t, tk(1, "twenty") - 0.1, w=720,
                 price_at=tk(1, "£405"))
    L.badge("MEET 3 SAVERS", 540, 1045, t, tk(2, "three"), "green", 30)


def s_savers(L, t):
    L.badge("STOCKS & SHARES ISA · 7% A YEAR", 540, 300, t, S(3), "white", 28)
    X = lambda age: 230 + (age - 20) * 710 / 40
    # intro beat (sentence 3) before the savers arrive
    fade = 1 - ramp(t, S(4) - 0.35, 0.3)
    if fade > 0:
        e = spring(t, tk(3, "Stocks") - 0.1)
        if e > 0:
            L.put(emoji_sprite("chart_increasing", 200), 540, 560, clamp(e * 1.5) * fade, 0.4 + 0.6 * e)
        p = spring(t, tk(3, "7%"))
        if p > 0:
            L.text("7% a year", 540, 780, 110, G, clamp(p * 1.3) * fade, 0.7 + 0.3 * p)
            L.text("assumed growth, after fees", 540, 880, 34, M, ramp(t, tk(3, "7%") + 0.3, 0.25) * fade,
                   weight="ExtraBold")
    for i, (name, emo, age) in enumerate(SAVERS):
        si = 4 + i
        cy = 470 + i * 215
        st = S(si) - 0.1
        a = L.card(540, cy, 940, 190, t, st)
        if a <= 0:
            continue
        L.emoji(emo, 140, cy - 10, 100, t, st + 0.08)
        nm = text_sprite(name, 42, Wt)
        L.put(nm, 230 + nm.width / 2, cy - 45, a)
        sub = text_sprite(f"starts at {age} · {END_AGE - age} years", 26, M, "ExtraBold")
        L.put(sub, 230 + sub.width / 2, cy + 2, a)
        lab = gbp(NEED[age])
        pt = tk(si, lab.rstrip(",."))
        q = spring(t, pt)
        if q > 0:
            pr = text_sprite(lab, 62, G)
            L.put(pr, 975 - pr.width / 2, cy - 30 + 12 * (1 - clamp(q)), clamp(q * 1.3))
            pm = text_sprite("a month", 24, M, "ExtraBold")
            L.put(pm, 975 - pm.width / 2, cy + 18, clamp(q * 1.3))
        # timeline bar: years of investing, age -> 60
        g = ease(ramp(t, st + 0.3, 0.8))
        track, _ = rrect_sprite(int(X(60) - X(20)), 12, 6, (255, 255, 255, 30))
        L.put(track, (X(20) + X(60)) / 2, cy + 58, a)
        if g > 0:
            w = max(12, int((X(60) - X(age)) * g))
            bar, _ = rrect_sprite(w, 12, 6, C + (255,))
            L.put(bar, X(age) + w / 2, cy + 58, a)
    st = S(7)
    r1, r2 = NEED[30] / NEED[20], NEED[40] / NEED[30]
    L.math_line([("each 10-year wait:", M), (f"×{r1:.1f}", G), ("then", M), (f"×{r2:.1f}", G)], 540, 1065, 44, t,
                tk(7, "doubles") - 0.4, stagger=0.12)


def s_paid(L, t):
    L.badge("WHAT THEY ACTUALLY PAY IN", 540, 300, t, S(8), "white", 28)
    a = ramp(t, S(8) + 0.1, 0.3)
    # legend
    for i, (lab, col) in enumerate((("PAID IN", C), ("GROWTH", G))):
        x = 330 + i * 290
        L.put(circle_sprite(22, col + (255,)), x, 385, a)
        sp = text_sprite(lab, 30, col)
        L.put(sp, x + 22 + sp.width / 2, 385, a)
    x0, x1, y0, y1 = 170, 960, 1000, 450
    Y = lambda v: y0 - (y0 - y1) * v / TARGET
    ss = 2
    left, top, right, bottom = 40, 420, 1040, 1020
    big = Image.new("RGBA", ((right - left) * ss, (bottom - top) * ss), (0, 0, 0, 0))
    d = ImageDraw.Draw(big)
    P = lambda x, y: ((x - left) * ss, (y - top) * ss)
    for v in (250_000, 500_000, 750_000, 1_000_000):
        d.line([P(x0, Y(v)), P(x1, Y(v))], fill=(255, 255, 255, 28), width=2 * ss)
    d.line([P(x0, y0), P(x1, y0)], fill=(255, 255, 255, 110), width=2 * ss)
    g = ease(ramp(t, S(8) + 0.3, 1.0))
    xs = [320, 565, 810]
    bw = 170
    for (name, emo, age), cx in zip(SAVERS, xs):
        if g <= 0:
            continue
        top_v = TARGET * g
        paid_v = min(PAID[age], top_v)
        d.rounded_rectangle([P(cx - bw / 2, Y(top_v)), P(cx + bw / 2, y0)], radius=14 * ss, fill=G + (255,))
        d.rectangle([P(cx - bw / 2, Y(paid_v)), P(cx + bw / 2, y0)], fill=C + (255,))
    sp = big.resize((right - left, bottom - top), Image.LANCZOS)
    L.put(sp, (left + right) / 2, (top + bottom) / 2, a)
    for v, lab in ((500_000, "£500K"), (1_000_000, "£1M")):
        L.text(lab, 100, Y(v), 24, M, a, weight="ExtraBold")
    times = {20: (tk(9, "£194,000"), tk(9, "81%")), 30: (S(10) - 0.2, S(10) - 0.1),
             40: (tk(10, "£473,000"), tk(10, "half"))}
    for (name, emo, age), cx in zip(SAVERS, xs):
        L.text(name, cx, 1050, 36, Wt, a)
        pt, gt = times[age]
        p = spring(t, pt)
        if p > 0:
            L.text(k(PAID[age]), cx, (Y(PAID[age]) + y0) / 2, 40, INK, clamp(p * 1.4), 0.7 + 0.3 * p)
        q = spring(t, gt)
        if q > 0:
            cy = (Y(PAID[age]) + Y(TARGET)) / 2
            L.text(f"{GROWTH_SHARE[age] * 100:.0f}%", cx, cy - 16, 48, INK, clamp(q * 1.4), 0.7 + 0.3 * q)
            L.text("growth", cx, cy + 24, 26, INK, clamp(q * 1.4), weight="ExtraBold")


def s_twist(L, t):
    L.badge("THE TWIST", 540, 300, t, S(11), "green", 32)
    L.emoji("hourglass_done", 540, 410, 100, t, tk(11, "forty") - 0.1)
    a = L.card(540, 570, 800, 170, t, tk(11, "million") - 0.1)
    if a > 0:
        L.text("£1,000,000 IN 40 YEARS", 540, 540, 30, M, a, weight="ExtraBold")
        L.text("buys less than today", 540, 600, 44, Wt, a)
    L.arrow(540, 670, 540, 790, ease(ramp(t, S(12), 0.4)), C, 6)
    L.text("2% inflation a year", 770, 730, 32, C, ramp(t, tk(12, "2%"), 0.25))
    st = tk(12, "£453,000")
    b = L.card(540, 900, 800, 190, t, tk(12, "worth") - 0.1)
    if b > 0:
        L.text("IN TODAY'S MONEY", 540, 850, 30, M, b, weight="ExtraBold")
        q = ease(ramp(t, st - 0.3, 0.8))
        if t >= st - 0.3:
            L.text("≈ " + gbp(round(TARGET - (TARGET - REAL_40) * q, -3) if q < 1 else round(REAL_40, -3)),
                   540, 920, 80, G, clamp((t - st + 0.3) * 4))
    L.text("2% = the Bank of England's inflation target", 540, 1060, 28, M, ramp(t, tk(12, "Bank"), 0.3),
           weight="ExtraBold")


def s_tip(L, t):
    L.badge("ONE THING PEOPLE MISS", 540, 300, t, S(13), "white", 30)
    L.price_card("bank", "ISA LIMIT, PER YEAR", gbp(ISA_LIMIT), 540, 450, t, tk(14, "ISA") - 0.1, w=760,
                 price_at=tk(14, "£20,000"))
    L.math_line([(gbp(ISA_LIMIT), Wt), ("÷", M), ("12", Wt), ("=", M), (gbp(ISA_MONTH), C)], 540, 620, 60, t,
                tk(14, "£1,667") - 0.4, stagger=0.1)
    L.text("a month, at most", 540, 690, 30, M, ramp(t, tk(14, "£1,667") + 0.3, 0.25), weight="ExtraBold")
    pt = tk(14, "Maya")
    a = L.card(540, 900, 900, 260, t, pt - 0.1)
    if a > 0:
        L.emoji("woman", 190, 850, 90, t, pt)
        sp = text_sprite("Maya needs " + gbp(NEED[40]), 44, Wt)
        L.put(sp, 260 + sp.width / 2, 835, a)
        sp2 = text_sprite("a month: more than the limit", 28, M, "ExtraBold")
        L.put(sp2, 260 + sp2.width / 2, 885, a)
    q = spring(t, tk(14, "pension"))
    if q > 0:
        L.text("ISA + PENSION", 540, 960 + 12 * (1 - clamp(q)), 64, G, clamp(q * 1.3))


def s_turn(L, t):
    L.badge("YOUR TURN", 540, 310, t, S(15), "green", 34)
    st = tk(15, "Starting")
    L.emoji("thinking_face", 540, 470, 150, t, st)
    L.math_line([("start at 25", Wt), ("for", M), ("£1M at 60", G)], 540, 640, 60, t, tk(15, "twenty") - 0.1,
                stagger=0.14)
    h = tk(15, "how")
    L.math_line([("=", M), ("?", G)], 540, 800, 140, t, h - 0.1, stagger=0.15)
    L.text("a month, at 7% a year", 540, 905, 30, M, ramp(t, h + 0.3, 0.25), weight="ExtraBold")
    c = tk(15, "Comment")
    L.badge("COMMENT YOUR GUESS", 470, 1045, t, c, "white", 30)
    L.arrow(780, 1045, 1000, 1150, ease(ramp(t, c + 0.3, 0.45)), Wt, 6)


def s_outro(L, t):
    lines = ["Illustration only. Assumes 7% a year after fees,", "paid in monthly. Before inflation unless shown.",
             "Investments can fall as well as rise.", "Not financial advice."]
    for i, ln in enumerate(lines):
        L.text(ln, 540, 330 + i * 52, 32, M, ramp(t, S(16) + 0.1 * i, 0.3), weight="ExtraBold")
    st = S(17)
    p = spring(t, st)
    if p > 0:
        ring = circle_sprite(280, (155, 225, 93, 40), G + (255,), 6)
        L.put(ring, 540, 760, clamp(p * 1.4), 0.6 + 0.4 * p)
        L.emoji("thumbs_up", 540, 755, 170, t, tk(17, "like") - 0.05, bounce=True)
    L.text("LIKE & FOLLOW", 540, 970, 58, Wt, ramp(t, tk(17, "follow"), 0.3))


SCENES = [(0, 2), (3, 7), (8, 10), (11, 12), (13, 14), (15, 15), (16, 17)]
DRAW = [s_hook, s_savers, s_paid, s_twist, s_tip, s_turn, s_outro]


def events():
    ev = [{"t": max(0, S(a) - 0.15), "kind": "whoosh"} for a, _ in SCENES[1:]]
    for si, p in ((1, "£405"), (4, "£405"), (5, "£855"), (6, "£1,970"), (9, "£194,000"), (10, "£473,000"),
                  (14, "£20,000"), (14, "£1,667"), (14, "pension")):
        ev.append({"t": tk(si, p), "kind": "pop"})
    ev += [{"t": tk(0, "millionaire") + 0.7, "kind": "coin"}, {"t": tk(9, "81%"), "kind": "coin"},
           {"t": tk(12, "£453,000") + 0.5, "kind": "crash"}]
    return ev
