"""Sample: 'Amy vs Ben' compound-interest explainer in the motion-design spec.

  python3 -I render_v3.py <dir> stills 1,5,12
  python3 -I render_v3.py <dir> events
  python3 -I render_v3.py <dir> render
"""
import json
import math
import os
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import motion as Mo  # noqa: E402
from motion import G, C, Wt, M, Layer, spring, ramp, ease, clamp, text_sprite  # noqa: E402

from PIL import Image, ImageDraw  # noqa: E402

# ---- figures (computed) ------------------------------------------------------------------------
R_M = 1.07 ** (1 / 12) - 1
MONTHLY = 200


def fv(months):
    return MONTHLY * ((1 + R_M) ** months - 1) / R_M


def amy(age):
    if age <= 25:
        return 0.0
    if age <= 35:
        return fv((age - 25) * 12)
    return fv(120) * 1.07 ** (age - 35)


def ben(age):
    return 0.0 if age <= 35 else fv((age - 35) * 12)


AMY35, AMY65, BEN65 = fv(120), amy(65), ben(65)
DIFF = AMY65 - BEN65


def gbp(v):
    return f"£{v:,.0f}"


T = None
GROUPS = None
SCENES = [(0, 3), (4, 6), (7, 9), (10, 12), (13, 14), (15, 17), (18, 19), (20, 21), (22, 23)]


def S(i):
    return T["sentences"][i]["start"]


def tk(si, prefix):
    for t in T["sentences"][si]["tokens"]:
        if t["text"].startswith(prefix):
            return t["start"]
    raise KeyError((si, prefix))


# ---- scenes ------------------------------------------------------------------------------------------
def scene_hook(L, t):
    L.badge("SAME 7% RETURN", 540, 300, t, -0.35, "white")
    L.price_card("woman", "AMY PUTS IN", "£24,000", 540, 480, t, -0.25, w=860, h=170,
                 verified_at=tk(2, "more"), price_at=-0.2)
    L.price_card("man", "BEN PUTS IN", "£72,000", 540, 690, t, S(1) - 0.1, w=860, h=170, price_color=C,
                 price_at=tk(1, "£72,000") - 0.1)
    L.badge("…AND AMY ENDS UP RICHER", 540, 890, t, tk(2, "Amy"), "green", 34)
    L.badge("HERE'S THE MATHS", 540, 1020, t, S(3), "white", 30)


def scene_plan(L, t):
    L.badge("THE PLAN", 540, 300, t, S(4))
    L.price_card("money_bag", "EVERY MONTH, EACH", "£200", 540, 450, t, tk(4, "£200") - 0.1, w=700)
    L.price_card("bank", "INTO A", "Stocks & Shares ISA", 540, 625, t, tk(4, "Stocks") - 0.1, w=700, price_size=42,
                 price_color=Wt)
    # age timeline 25 -> 65
    x0, x1, ay = 140, 940, 1035
    X = lambda age: x0 + (x1 - x0) * (age - 25) / 40
    pa = ease(ramp(t, S(5) - 0.1, 0.5))
    if pa > 0:
        L.arrow(x0, ay, x0 + (x1 - x0 + 30) * pa, ay, 1.0 if pa > 0.99 else pa * 0.99, Wt, 4, 0.6)
        for age in (25, 35, 45, 55, 65):
            if ramp(t, S(5), 0.6) * 40 >= age - 25:
                L.text(str(age), X(age), ay + 40, 28, M, 1, weight="ExtraBold")
    for who, a0, a1, y, start, end, col, emo in (
            ("AMY", 25, 35, 870, tk(5, "25"), tk(5, "35"), C, "woman"),
            ("BEN", 35, 65, 955, tk(6, "35"), tk(6, "65"), G, "man")):
        p = ease(ramp(t, start, max(0.4, end - start)))
        if p <= 0:
            continue
        w = (X(a1) - X(a0)) * p
        bar, _ = Mo.rrect_sprite(max(30, int(w)), 44, 22, col + (255,))
        L.put(bar, X(a0) + max(30, w) / 2, y)
        L.emoji(emo, X(a0) - 4, y - 2, 70, t, start)
        lab = text_sprite(f"{who} {a0}–{a1}", 28, Mo.INK)
        if w > lab.width + 70:
            L.put(lab, X(a0) + 44 + lab.width / 2, y + 1, clamp(p * 2))
        else:
            L.put(text_sprite(f"{who} {a0}–{a1}", 28, Wt), X(a0) + max(30, w) + 20 + lab.width / 2, y + 1, clamp(p * 2))


def way_amy_full(L, t):
    L.card(540, 680, 860, 780, t, S(7) - 0.05)
    L.badge("AMY · INVESTS AGE 25–35", 540, 350, t, S(7))
    a2400 = tk(7, "£2,400")
    L.text("pays in for 10 years", 540, 445, 30, M, ramp(t, a2400, 0.25), weight="ExtraBold")
    land = tk(7, "£24,000")
    L.math_line([("10", Wt), ("×", M), ("£2,400", Wt), ("=", M), ("£24,000", C)], 540, 515, 60, t, a2400,
                stagger=clamp((land - a2400) / 4, 0.08, 0.35))
    s7 = tk(8, "7%")
    L.text("by age 35, at 7% a year", 540, 625, 30, M, ramp(t, s7, 0.25), weight="ExtraBold")
    p = spring(t, tk(8, "£34,000"))
    if p > 0:
        L.text("≈ " + gbp(AMY35), 540, 695 + 20 * (1 - clamp(p)), 70, C, clamp(p * 1.3))
    s30 = tk(9, "30")
    L.text("then 30 years untouched", 540, 795, 30, M, ramp(t, s30, 0.25), weight="ExtraBold")
    L.math_line([(gbp(AMY35), Wt), ("×", M), ("1.07³⁰", G)], 540, 860, 52, t, s30 + 0.2, stagger=0.2)
    r = spring(t, tk(9, "£260,000"))
    if r > 0:
        L.text(gbp(AMY65), 540, 975, 104 * (0.7 + 0.3 * clamp(r)), G, clamp(r * 1.3))


def scene_amy(L, t):
    way_amy_full(L, t)


def compact_card(L, t, cx, title, variant, paid, paid_col, final, final_col, start, paid_at, final_at,
                 verified_at=None, extra=None):
    L.card(cx, 600, 470, 600, t, start, verified_at)
    L.badge(title, cx, 360, t, start + 0.05, variant, 32)
    L.text("PAID IN", cx, 450, 26, M, ramp(t, paid_at - 0.1, 0.25), weight="ExtraBold")
    p = spring(t, paid_at)
    if p > 0:
        L.text(paid, cx, 510 + 16 * (1 - clamp(p)), 60, paid_col, clamp(p * 1.3))
    if extra:
        e_txt, e_at = extra
        L.text(e_txt, cx, 575, 28, C, ramp(t, e_at, 0.25), weight="ExtraBold")
    L.text("AT 65", cx, 660, 26, M, ramp(t, final_at - 0.1, 0.25), weight="ExtraBold")
    q = spring(t, final_at)
    if q > 0:
        L.text(final, cx, 730 + 16 * (1 - clamp(q)), 66, final_col, clamp(q * 1.3))


def scene_compare(L, t):
    win = tk(12, "Amy")
    compact_card(L, t, 290, "AMY", "green", "£24,000", Wt, gbp(AMY65), G, S(10) - 0.3, S(10) - 0.2, S(10) - 0.1,
                 verified_at=win)
    compact_card(L, t, 790, "BEN", "white", "£72,000", Wt, gbp(BEN65), C, S(10), tk(10, "£72,000"),
                 tk(11, "£234,000"), extra=("3× MORE", tk(10, "three")))
    L.badge("SAME 7% RETURN", 540, 965, t, S(12), "white", 28)
    L.badge(f"AMY WINS BY {gbp(DIFF)}", 540, 1060, t, tk(12, "£26,000"), "green", 36)


def chart_sprite(t, prog_age, labels_a):
    ss = 2
    x0, x1, y0, y1 = 120, 930, 1000, 470  # in page coords
    ymax = 300_000
    X = lambda age: (x0 + (x1 - x0) * (age - 25) / 40)
    Y = lambda v: (y0 - (y0 - y1) * v / ymax)
    left, top, right, bottom = 40, 400, 1040, 1080
    big = Image.new("RGBA", ((right - left) * ss, (bottom - top) * ss), (0, 0, 0, 0))
    d = ImageDraw.Draw(big)
    P = lambda x, y: ((x - left) * ss, (y - top) * ss)
    for v in (100_000, 200_000, 300_000):
        d.line([P(x0, Y(v)), P(x1, Y(v))], fill=(255, 255, 255, 30), width=2 * ss)
    d.line([P(x0, y0), P(x1, y0)], fill=(255, 255, 255, 110), width=2 * ss)
    for name, fn, col, a_start in (("amy", amy, G, 25), ("ben", ben, C, 35)):
        if prog_age <= a_start:
            continue
        ages = [a_start + (prog_age - a_start) * i / 80 for i in range(81)]
        pts = [P(X(a), Y(fn(a))) for a in ages]
        d.line(pts, fill=col + (255,), width=7 * ss, joint="curve")
        ex, ey = pts[-1]
        r = 11 * ss
        d.ellipse((ex - r, ey - r, ex + r, ey + r), fill=col + (255,), outline=(14, 20, 48, 255), width=4 * ss)
    im = big.resize((right - left, bottom - top), Image.LANCZOS)
    return im, (left + right) / 2, (top + bottom) / 2, X, Y


def scene_chart(L, t):
    L.badge("THE REASON: TIME", 540, 300, t, S(13))
    a = ramp(t, S(13) - 0.05, 0.3)
    dur = (S(15) - 0.4) - S(13)
    prog = 25 + 40 * ease(ramp(t, S(13) + 0.2, dur * 0.8))
    sp, cx, cy, X, Y = chart_sprite(t, prog, None)
    L.put(sp, cx, cy, a)
    for v in (100_000, 200_000, 300_000):
        L.text(f"£{v // 1000}K", 80, Y(v), 24, M, a, weight="ExtraBold")
    for age in (25, 35, 45, 55, 65):
        L.text(str(age), X(age), 1040, 26, M, a, weight="ExtraBold")
    if prog >= 64.9:
        q = ramp(t, S(13) + 0.2 + dur * 0.8, 0.3)
        for i, (who, v, col) in enumerate((("AMY", AMY65, G), ("BEN", BEN65, C))):
            y = 500 + i * 56
            L.put(Mo.circle_sprite(22, col + (255,)), 175, y, q)
            lab = text_sprite(f"{who} AT 65: {gbp(v)}", 32, col)
            L.put(lab, 200 + lab.width / 2, y, q)
    if prog > 36:
        L.text("Amy stops adding", X(35), Y(AMY35) - 54, 24, M, ramp(t, S(13) + 0.6, 0.3), weight="ExtraBold")
    L.text("slow…", X(33), 940, 34, Wt, ramp(t, tk(14, "slow"), 0.25))
    L.text("…then fast", X(47), Y(amy(52)) - 40, 34, Wt, ramp(t, tk(14, "fast"), 0.25))


def scene_rule72(L, t):
    L.badge("RULE OF 72", 540, 300, t, S(15))
    st = tk(16, "72 ÷ 7")
    land = tk(16, "10")
    L.text("72 ÷ your yearly return", 540, 420, 34, M, ramp(t, tk(16, "Divide"), 0.3), weight="ExtraBold")
    L.math_line([("72", Wt), ("÷", M), ("7", G), ("≈", M), ("10", C)], 540, 540, 120, t, st,
                stagger=clamp((land - st) / 4, 0.1, 0.4))
    L.text("years to double", 540, 650, 34, M, ramp(t, land, 0.3), weight="ExtraBold")
    s17 = S(17)
    chips = [("£1", "NOW"), ("£2", "10 YRS"), ("£4", "20 YRS"), ("£8", "30 YRS")]
    xs = [165, 415, 665, 915]
    for i, ((v, lab), x) in enumerate(zip(chips, xs)):
        st_i = s17 + 0.35 * i
        a = L.card(x, 800, 190, 150, t, st_i, verified_at=(s17 + 1.5) if i == 3 else None)
        if a > 0:
            L.text(v, x, 785, 60, G if i == 3 else Wt, a)
            L.text(lab, x, 845, 24, M, a, weight="ExtraBold")
        if i > 0:
            L.arrow(xs[i - 1] + 100, 800, x - 100, 800, ease(ramp(t, st_i - 0.15, 0.25)), Wt, 4, 0.8)
    L.text("≈ ×8 roughly · exact at 7%: ×7.6", 540, 950, 30, M, ramp(t, s17 + 1.5, 0.3), weight="ExtraBold")


def scene_reallife(L, t):
    L.badge("IN REAL LIFE", 540, 300, t, S(18))
    L.price_card("money_bag", "A MONTH", "£200", 540, 450, t, tk(18, "£200") - 0.1, w=600)
    L.arrow(540, 545, 540, 615, ease(ramp(t, tk(18, "£6.60") - 0.4, 0.3)), Wt, 5, 0.8)
    L.price_card("hot_beverage", "A DAY", "≈ £6.60", 540, 710, t, tk(18, "£6.60") - 0.15, w=600, price_color=C)
    L.math_line([("START EARLY", Wt), (">", G), ("START BIG", Wt)], 540, 930, 62, t, S(19), stagger=0.18)


def scene_turn(L, t):
    L.badge("YOUR TURN", 540, 310, t, S(20), "green", 34)
    L.math_line([("72", Wt), ("÷", M), ("9", G), ("=", M), ("?", G)], 540, 520, 140, t, tk(20, "9%") - 0.2,
                stagger=0.16)
    L.text("years to double at 9%", 540, 650, 32, M, ramp(t, tk(20, "years"), 0.3), weight="ExtraBold")
    L.badge("USE THE RULE OF 72", 540, 770, t, tk(21, "rule"), "green", 30)
    c = tk(21, "comment")
    L.badge("COMMENT YOUR ANSWER", 470, 900, t, c, "white", 32)
    L.arrow(800, 900, 1000, 1060, ease(ramp(t, c + 0.3, 0.45)), Wt, 6)


def scene_outro(L, t):
    lines = ["Illustration only. 7% a year assumed,", "after fees and before inflation.",
             "Investments can fall as well as rise.", "Not financial advice."]
    for i, ln in enumerate(lines):
        L.text(ln, 540, 330 + i * 52, 32, M, ramp(t, S(22) + 0.1 * i, 0.3), weight="ExtraBold")
    st = S(23)
    p = spring(t, st)
    if p > 0:
        ring = Mo.circle_sprite(280, (79, 195, 247, 40), (79, 195, 247, 255), 6)
        L.put(ring, 540, 760, clamp(p * 1.4), 0.6 + 0.4 * p)
        L.emoji("thumbs_up", 540, 755, 190, t, st + 0.05, bounce=True)
    L.text("LIKE & SAVE", 540, 970, 60, Wt, ramp(t, st + 0.2, 0.3))


DRAW = [scene_hook, scene_plan, scene_amy, scene_compare, scene_chart, scene_rule72, scene_reallife, scene_turn,
        scene_outro]


# ---- frame ---------------------------------------------------------------------------------------------
def frame(t):
    img = Mo.background(t)
    base = Layer()
    Mo.top_bar(base, t, T["total"], "MONEY MATHS", "POUND FOR POUND")
    img.alpha_composite(base.im)
    # current scene with fade in/out
    k = 0
    for i, (a, b) in enumerate(SCENES):
        if t >= S(a) - 0.001:
            k = i
    start = S(SCENES[k][0]) if k > 0 else 0.0
    end = S(SCENES[k + 1][0]) if k + 1 < len(SCENES) else T["total"] + 1
    alpha = min(ramp(t, start, 0.35) if k > 0 else 1.0, 1 - ramp(t, end - 0.27, 0.27))
    sc = Layer()
    DRAW[k](sc, t)
    img.alpha_composite(Mo.with_alpha(sc.im, alpha))
    cap = Layer()
    Mo.captions(cap, t, GROUPS)
    img.alpha_composite(cap.im)
    return img.convert("RGB")


def events():
    ev = []
    for i, (a, b) in enumerate(SCENES[1:], 1):
        ev.append({"t": max(0, S(a) - 0.15), "kind": "whoosh"})
    for si, p in ((0, "£24,000"), (1, "£72,000"), (4, "£200"), (7, "£24,000"), (8, "£34,000"), (10, "£72,000"),
                  (11, "£234,000"), (16, "10"), (18, "£6.60")):
        ev.append({"t": tk(si, p), "kind": "pop"})
    ev += [{"t": tk(2, "Amy"), "kind": "coin"}, {"t": tk(9, "£260,000"), "kind": "coin"},
           {"t": tk(12, "£26,000"), "kind": "coin"}]
    return ev


def main():
    global T, GROUPS
    d, cmd = sys.argv[1], sys.argv[2]
    T = json.load(open(os.path.join(d, "build", "timings.json"), encoding="utf-8"))
    T["total"] = T["duration"] + 0.8
    GROUPS = Mo.caption_groups(T)
    b = os.path.join(d, "build")
    if cmd == "events":
        json.dump(events(), open(os.path.join(b, "events.json"), "w"), indent=1)
        print(f"{T['total']:.3f}")
    elif cmd == "stills":
        for ts in sys.argv[3].split(","):
            frame(float(ts)).save(os.path.join(b, f"still_{float(ts):05.2f}.png"))
    elif cmd == "render":
        out = os.path.join(b, "video.mp4")
        n = int(math.ceil(T["total"] * Mo.FPS))
        ff = subprocess.Popen(
            ["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{Mo.W}x{Mo.H}",
             "-r", str(Mo.FPS), "-i", "-", "-i", os.path.join(b, "mix.wav"), "-c:v", "libx264", "-preset", "medium",
             "-crf", "18", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart",
             out], stdin=subprocess.PIPE)
        for i in range(n):
            ff.stdin.write(frame(i / Mo.FPS).tobytes())
        ff.stdin.close()
        ff.wait()
        print(out)


if __name__ == "__main__":
    main()
