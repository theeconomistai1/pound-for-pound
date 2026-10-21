"""Sample (brand-v2, format: myth): "A pay rise can leave you worse off" — mostly a myth.
(figures checked 21 Oct 2026, tax year 2026/27, England, Wales and Northern Ireland)

gov.uk/income-tax-rates: Personal Allowance £12,570; basic rate 20% to £50,270; higher rate 40% from £50,271;
  Personal Allowance falls £1 for every £2 over £100,000, zero at £125,140.
gov.uk/national-insurance-rates-letters: employee Class 1 (category A) 8% up to the Upper Earnings Limit, 2% above.
gov.uk/child-benefit-tax-charge: charge starts over £60,000 (1% per £200), all repaid over £80,000.
"""
from motion import *  # noqa: F401,F403
from brand import *  # noqa: F401,F403

BRAND = True
COVER = dict(words=("PAY RISE", "MYTH"), highlight=1, hero="£", left="Briefcase", right="Receipt",
             particles="Coin")

# ---- figures ---------------------------------------------------------------------------------------------
HIGHER_FROM = 50_270      # higher rate applies above this
HIGHER_RATE = 0.40
NI_ABOVE_UEL = 0.02
TAPER_START = 100_000
PA = 12_570
PA_GONE = TAPER_START + 2 * PA
HICBC_FROM, HICBC_ALL = 60_000, 80_000
EXTRA = 1.00
TAX_ON_EXTRA = EXTRA * HIGHER_RATE
NI_ON_EXTRA = EXTRA * NI_ABOVE_UEL
KEEP = EXTRA - TAX_ON_EXTRA - NI_ON_EXTRA
assert round(KEEP * 100) == 58 and PA_GONE == 125_140
# £100,000-£125,140: each extra £1 also loses 50p of allowance taxed at 40% -> 60% income tax (+2% NI)
TRAP_RATE = HIGHER_RATE + 0.5 * HIGHER_RATE
assert round(TRAP_RATE * 100) == 60


def s_hook(L, t):  # sentence 0
    cover_hook(L, t, f"{round(KEEP * 100)}p", sub="of every £1 over the line", number_at=tk(0, "58p"),
               kicker="£1 OVER THE HIGHER-RATE LINE")


def s_myth(L, t):  # sentence 1
    beat(L, "myth", t, S(1) - 0.1)
    a = ramp(t, S(1) + 0.1, 0.3)
    L.text("“A pay rise can push you", W / 2, 560, 56, Wt, a)
    L.text("into a higher band and", W / 2, 636, 56, Wt, a)
    L.text("leave you worse off”", W / 2, 712, 56, Wt, a)
    verdict_stamp(L, "MYTH", W / 2, 930, t, tk(1, "worse") + 0.3, "red")


def s_truth(L, t):  # sentences 2-3
    beat(L, "truth", t, S(2) - 0.1)
    # a pound split into what goes where
    x0, x1, y = 160, 920, 640
    a = ramp(t, S(2), 0.3)
    track, _ = rrect_sprite(x1 - x0, 90, 20, (255, 255, 255, 22), (255, 255, 255, 70), 2)
    L.put(track, (x0 + x1) / 2, y, a)
    segs = [(KEEP, G, "YOU KEEP", f"{round(KEEP * 100)}p", tk(3, "58p")),
            (TAX_ON_EXTRA, RED, "INCOME TAX", f"{round(TAX_ON_EXTRA * 100)}p", tk(2, "40%")),
            (NI_ON_EXTRA, C, "NI", f"{round(NI_ON_EXTRA * 100)}p", tk(3, "2%"))]
    x = x0
    for i, (v, col, lab, val, at) in enumerate(segs):
        w = (x1 - x0) * v
        p = ease(ramp(t, at - 0.1, 0.4))
        if p > 0:
            bar, _ = rrect_sprite(max(8, int(w * p)), 90, 20 if i == 0 else 6, col + (255,))
            L.put(bar, x + w * p / 2, y)
            q = clamp(spring(t, at) * 1.3)
            if i < 2:
                L.text(val, x + w / 2, y - 100, 64 if i == 0 else 52, col, q)
                L.text(lab, x + w / 2, y + 90, 26, M, q, weight="ExtraBold")
            else:
                L.text(val, x1 - 10, y - 100, 40, col, q)
                L.text(lab, x1 - 10, y + 90, 26, M, q, weight="ExtraBold")
        x += w
    L.text("OF EACH £1 ABOVE £50,270", W / 2, 470, 34, Wt, ramp(t, tk(2, "£50,270"), 0.3))
    checked(L, "GOV.UK · 2026/27 RATES · CHECKED 21 OCT 2026", W / 2, 960, t, tk(3, "58p") + 0.3)


def s_trap(L, t):  # sentences 4-5
    beat(L, "catch", t, S(4) - 0.1, sub="WHERE IT REALLY BITES", sub_at=S(4) + 0.2)
    value_card(L, W / 2, 560, 880, t, tk(4, "£100,000") - 0.1, "warning", "£100,000 TO £125,140",
               f"{round(TRAP_RATE * 100)}% tax", color=RED, value_at=tk(4, "disappear"),
               sub="allowance tapers away")
    value_card(L, W / 2, 760, 880, t, tk(5, "Child") - 0.1, "baby", "CHILD BENEFIT CHARGE",
               "£60,000", color=RED, value_at=tk(5, "£60,000"), sub="all repaid by £80,000")
    caveat(L, t, S(5) + 0.4, ["2026/27 rates, England, Wales and NI. Scotland differs.",
                              "General education, not financial advice."], cy=930)


def s_loop(L, t):  # sentence 6
    loop_close(L, t, 6, comment="WOULD YOU TAKE IT? COMMENT")


SCENES = [(0, 0), (1, 1), (2, 3), (4, 5), (6, 6)]
DRAW = [s_hook, s_myth, s_truth, s_trap, s_loop]


def events():
    ev = [{"t": tk(0, "58p") + 0.05, "kind": "coin"}, {"t": tk(1, "worse") + 0.3, "kind": "boom"},
          {"t": tk(2, "40%"), "kind": "pop"}, {"t": tk(3, "58p"), "kind": "coin"},
          {"t": tk(4, "disappear"), "kind": "pop"}, {"t": tk(5, "£60,000"), "kind": "pop"}]
    return scene_events(ev)
