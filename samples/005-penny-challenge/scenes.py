"""005: The 1p savings challenge — the worked example of the brand template (pipeline/brand.py, BRAND.md).
(figures computed below, 20 Oct 2026)

1p on day 1, 2p on day 2 ... 365p on day 365 (2027 is not a leap year).
Total = 365 x 366 / 2 = 66,795p = £667.95. December (days 335-365) = £108.50.
Backwards (365p on 1 Jan down to 1p on 31 Dec): December = 31p + ... + 1p = £4.96.
Assumption: £667.95 invested at the end of each year for 10 years at 7% a year after fees.
"""
from motion import *  # noqa: F401,F403
from brand import *  # noqa: F401,F403
from PIL import Image, ImageDraw

BRAND = True

# ---- figures (every number on screen comes from here) -------------------------------------------------
DAYS = 365
MONTH_DAYS = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
TOTAL_P = DAYS * (DAYS + 1) // 2
TOTAL = TOTAL_P / 100
_starts = [sum(MONTH_DAYS[:k]) for k in range(12)]
FORWARD = [sum(range(s + 1, s + m + 1)) / 100 for s, m in zip(_starts, MONTH_DAYS)]
BACKWARD = [sum(DAYS + 1 - d for d in range(s + 1, s + m + 1)) / 100 for s, m in zip(_starts, MONTH_DAYS)]
RATE, YEARS = 0.07, 10
POT = [sum(TOTAL * (1 + RATE) ** (y - k) for k in range(1, y + 1)) for y in range(YEARS + 1)]
PAID = [TOTAL * y for y in range(YEARS + 1)]
LEAP = 366 * 367 / 2 / 100  # comment-question answer, never shown

assert TOTAL_P == 66_795 and f"{TOTAL:.2f}" == "667.95"
assert f"{FORWARD[11]:.2f}" == "108.50" and f"{BACKWARD[11]:.2f}" == "4.96"
assert round(POT[-1], -1) == 9_230


def p2(v):
    return f"£{v:,.2f}"


# ---- scenes -----------------------------------------------------------------------------------------------
def s_hook(L, t):
    hook(L, t, ["1p TODAY,", "2p TOMORROW…"], p2(TOTAL), sub="by New Year's Eve", emoji="coin",
         number_at=tk(0, "£667"),
         extra=lambda L, t: chip(L, "MOST QUIT IN DECEMBER", W / 2, 1215, t, tk(1, "December") - 0.1, "red", 30,
                                 emoji="face_screaming_in_fear"))


def s_example(L, t):
    beat(L, "example", t, S(2) - 0.1)
    x0, x1, yt, yb = 190, 900, 470, 980
    X = lambda d: x0 + (x1 - x0) * d / DAYS
    Y = lambda p: yb - (yb - yt) * p / DAYS
    a = ramp(t, S(2), 0.3)
    # the daily amount climbs 1p a day: day reached follows the voice
    k1, k2, k3 = tk(2, "1p"), tk(2, "100"), tk(3, "£3.65")
    if t < k2:
        day = 1.0
    elif t < k3:
        day = 1 + 99 * ease(ramp(t, k2 - 0.3, 0.6))
    else:
        day = 100 + 265 * ease(ramp(t, k3 - 0.5, 0.7))
    day = max(1.0, day)
    left, top = x0 - 20, yt - 20
    big = Image.new("RGBA", ((x1 - x0 + 40) * SS, (yb - yt + 40) * SS), (0, 0, 0, 0))
    d = ImageDraw.Draw(big)
    P = lambda x, y: ((x - left) * SS, (y - top) * SS)
    d.line([P(x0, yb), P(x1, yb)], fill=(255, 255, 255, 110), width=2 * SS)
    d.polygon([P(X(0), Y(0)), P(X(day), Y(0)), P(X(day), Y(day))], fill=C + (60,))
    d.line([P(X(0), Y(0)), P(X(day), Y(day))], fill=C + (255,), width=6 * SS)
    sp = big.resize((x1 - x0 + 40, yb - yt + 40), Image.LANCZOS)
    L.put(sp, left + sp.width / 2, top + sp.height / 2, a)
    L.text("SAVED THAT DAY", x0 + 120, yt - 10, 24, M, a, weight="ExtraBold")
    for dd, lab, val, col, at in ((1, "DAY 1", "1p", Wt, k1), (100, "DAY 100", "£1", Wt, tk(2, "£1")),
                                  (365, "DAY 365", "£3.65", G, k3)):
        q = spring(t, at)
        if q > 0:
            L.put(circle_sprite(22, col + (255,)), X(dd), Y(dd), clamp(q * 1.4))
            L.text(lab, X(dd), yb + 34, 24, M, clamp(q * 1.4), weight="ExtraBold")
            dx = 0 if dd < 300 else -70
            L.text(val, X(dd) + dx, Y(dd) - 50 + 10 * (1 - clamp(q)), 50, col, clamp(q * 1.4))
    chip(L, "+1p EVERY DAY", W / 2, 1140, t, tk(3, "last") - 0.1, "white", 30, emoji="coin")


def s_maths(L, t):
    beat(L, "maths", t, S(4) - 0.1)
    r1 = S(4) + 0.05
    timed_line(L, [("1p", Wt, r1), ("+", M, r1 + 0.08), ("2p", Wt, r1 + 0.16), ("+", M, r1 + 0.24),
                   ("3p", Wt, r1 + 0.32), ("+ … +", M, r1 + 0.4), ("365p", Wt, r1 + 0.48)], W / 2, 450, 52, t)
    a, b, c = tk(4, "365"), tk(4, "366"), tk(4, "halved")
    timed_line(L, [("=", M, a), ("365", Wt, a), ("×", M, b), ("366", Wt, b), ("÷", M, c), ("2", Wt, c)],
               W / 2, 580, 80, t)
    p = S(5) - 0.15
    timed_line(L, [("=", M, p), (f"{TOTAL_P:,}p", C, p)], W / 2, 715, 80, t)
    q = tk(5, "£667")
    pa = panel(L, W / 2, 935, 760, 230, t, q - 0.15, "green")
    if pa > 0:
        L.text("IN POUNDS", W / 2, 865, 28, M, pa, weight="ExtraBold")
        big_number(L, p2(TOTAL), W / 2, 955, t, q, size=130, alpha=pa)
    checked(L, "MATHS CHECKED · 20 OCT 2026", W / 2, 1140, t, q + 0.45)


def s_catch(L, t):
    beat(L, "catch", t, S(6) - 0.1)
    L.text("DECEMBER ALONE", W / 2, 420, 54, Wt, ramp(t, tk(6, "December"), 0.25))
    cols = [C] * 11 + [RED]
    bar_chart(L, t, S(6), FORWARD, ["J", "F", "M", "A", "M", "J", "J", "A", "S", "O", "N", "D"],
              (130, 560, 950, 1000), cols, dur=1.0, stagger=0.04,
              value_tags={11: (p2(FORWARD[11]), RED, tk(6, "£108.50"))})
    chip(L, "RIGHT BEFORE CHRISTMAS", W / 2, 1150, t, tk(6, "Christmas") - 0.1, "red", 30, emoji="wrapped_gift")


def s_fix(L, t):
    beat(L, "miss", t, S(7) - 0.1)
    st = tk(7, "backwards")
    p = spring(t, st - 0.05)
    if p > 0:
        L.text("DO IT BACKWARDS", W / 2, 440, 84, G, clamp(p * 1.3), 0.7 + 0.3 * p)
    versus(L, t,
           dict(title="FORWARDS", label="DECEMBER COSTS", value=p2(FORWARD[11]), color=RED, tone="red",
                emoji="chart_increasing", start=S(8) - 0.05, at=S(8) + 0.15),
           dict(title="BACKWARDS", label="DECEMBER COSTS", value=p2(BACKWARD[11]), color=G, tone="green",
                emoji="chart_decreasing", start=tk(8, "£3.65") - 0.1, at=tk(8, "£4.96")),
           cy=715, h=300)
    a = tk(8, "£3.65")
    timed_line(L, [("1 JAN:", M, a), ("£3.65,", Wt, a), ("DOWN TO", M, a + 0.3), ("1p", Wt, a + 0.3),
                   ("ON 31 DEC", M, a + 0.3)], W / 2, 920, 38, t)
    pa = panel(L, W / 2, 1100, 860, 170, t, S(9) - 0.05)
    if pa > 0:
        L.emoji("bank", 180, 1100, 90, t, S(9))
        s1 = text_sprite(f"SAME TOTAL · {p2(TOTAL)}", 40, Wt)
        L.put(s1, 250 + s1.width / 2, 1075, pa)
        q = ramp(t, tk(9, "interest") - 0.1, 0.3)
        s2 = text_sprite("earns interest for longer", 34, G)
        L.put(s2, 250 + s2.width / 2, 1130, q)


def s_levelup(L, t):
    beat(L, "levelup", t, S(10) - 0.1, sub="10 YEARS · 7% A YEAR (ASSUMED)", sub_at=tk(10, "7%"))
    a = ramp(t, S(10) + 0.1, 0.3)
    for i, (lab, col) in enumerate((("INVESTED", G), ("PAID IN", C))):
        x = 360 + i * 260
        L.put(circle_sprite(22, col + (255,)), x, 450, a)
        sp = text_sprite(lab, 28, col)
        L.put(sp, x + 22 + sp.width / 2, 450, a)
    end = tk(10, "£9,230")
    line_chart(L, t, S(10) + 0.3, end - S(10) - 0.2,
               [([(y, POT[y]) for y in range(YEARS + 1)], G, 7), ([(y, PAID[y]) for y in range(YEARS + 1)], C, 5)],
               (180, 530, 790, 980), YEARS, 10_000,
               x_labels=[(0, "YEAR 0"), (5, "5"), (10, "10")], y_labels=[(5_000, "£5K"), (10_000, "£10K")],
               end_tags=[(0, f"£{round(POT[-1], -1):,.0f}", G, end, 0),
                         (1, f"£{round(PAID[-1], -1):,.0f}", C, end + 0.5, 6)])
    caveat(L, t, S(11), ["Illustration only. Assumes 7% a year after fees,",
                         "invested at each year end. Investments can fall."], cy=1110)


def s_turn(L, t):
    your_turn(L, t, 12, ["IN A LEAP YEAR,", "366 DAYS:"], "= £?", hint="1p + 2p + 3p + … + 366p")


def s_share(L, t):
    share_close(L, t, 13, ["the friend who says", "pennies don't matter"])


SCENES = [(0, 1), (2, 3), (4, 5), (6, 6), (7, 9), (10, 11), (12, 12), (13, 13)]
DRAW = [s_hook, s_example, s_maths, s_catch, s_fix, s_levelup, s_turn, s_share]


def events():
    ev = [{"t": tk(0, "£667") + 0.1, "kind": "coin"}, {"t": S(5) - 0.15, "kind": "pop"}, {"t": tk(5, "£667"), "kind": "coin"},
          {"t": tk(6, "£108.50"), "kind": "boom"}, {"t": tk(10, "£9,230"), "kind": "coin"}]
    for si, p in ((2, "1p"), (2, "£1"), (3, "£3.65"), (4, "365"), (4, "366"), (4, "halved"),
                  (8, "£4.96")):
        ev.append({"t": tk(si, p), "kind": "pop"})
    return scene_events(ev)
