"""Video 023 (brand-v2, format: news, told as the dopamine loop — BRAND.md §0c): Budget 2026 scraps the planned
cut of the cash ISA limit to £12,000 for under-65s; it stays £20,000. The same Budget raises the tax rates on
savings interest outside ISAs from April 2027. (figures checked 30 Oct 2026)

Budget 2025 OOTLAR, 2.3 (gov.uk/government/publications/budget-2025-overview-of-tax-legislation-and-rates-ootlar/
  budget-2025-overview-of-tax-legislation-and-rates-ootlar): "the annual ISA cash limit will be set at £12,000"
  within "the overall annual ISA limit of £20,000"; "Savers over the age of 65 will continue to be able to save up
  to £20k in a cash ISA each year"; "ahead of commencement in April 2027".
Budget 2026 document, 3.9 (gov.uk/government/publications/budget-2026-document/budget-2026-html): "the government
  has decided not to reduce the cash ISA limit, so that it remains at £20,000"; a new ISA incentive for
  first-time stocks and shares ISA investors to be explored with industry.
Budget 2026 OOTLAR, 2.5 (gov.uk/government/publications/budget-2026-overview-of-tax-legislation-and-rates-ootlar/
  budget-2026-overview-of-tax-legislation-and-rates-ootlar): "retain the cash ISA limit at £20,000 for all savers
  over 18 years old from April 2027"; secondary legislation to be laid in November 2026.
  1.1: "the savings basic rate will be 24%, the savings higher rate will be 44%, and the savings additional rate
  will be 49%" ... "from 6 April 2027" (today 20% / 40% / 45%).
gov.uk/individual-savings-accounts: "In the 2026 to 2027 tax year, the maximum you can save in ISAs is £20,000."
"""
from motion import *  # noqa: F401,F403
from brand import *  # noqa: F401,F403

BRAND = True
COVER = dict(words=("CASH ISA", "U-TURN"), highlight=1, hero="Classical building", left="Party popper",
             right="Calendar", particles="Coin")

# ---- figures (HM Treasury: Budget 2025 and Budget 2026 OOTLAR; Budget 2026 document) ------------------------
ISA_LIMIT = 20_000               # overall annual ISA limit, and the cash ISA limit kept by Budget 2026
PLANNED_CASH_LIMIT = 12_000      # Budget 2025 plan for under-65s from April 2027 (now scrapped)
AGE = 65                         # 65 and over were exempt from the planned cut
LOST_ROOM = ISA_LIMIT - PLANNED_CASH_LIMIT
SAVINGS_BASIC_NOW, SAVINGS_BASIC_2027 = 20, 24     # % on savings interest above allowances, from 6 April 2027
SAVINGS_HIGHER_NOW, SAVINGS_HIGHER_2027 = 40, 44
PSA_BASIC = 1_000                # Personal Savings Allowance, basic-rate taxpayers (caveat only)
assert LOST_ROOM == 8_000 and gbp(LOST_ROOM) == "£8,000"    # spoken: "£8,000"
assert gbp(ISA_LIMIT) == "£20,000"                          # spoken: "£20,000"
assert gbp(PLANNED_CASH_LIMIT) == "£12,000"                 # shown
assert str(AGE) == "65"                                     # spoken: "65s"
assert SAVINGS_BASIC_2027 > SAVINGS_BASIC_NOW and SAVINGS_HIGHER_2027 > SAVINGS_HIGHER_NOW

STAMP = "GOV.UK · BUDGET 2026 · CHECKED 30 OCT 2026"
STAMP_RATES = "GOV.UK · SAVINGS RATES 2027/28 · CHECKED 30 OCT 2026"


def s_hook(L, t):  # sentence 0 · risk
    cover_hook(L, t, gbp(LOST_ROOM), sub="of cash ISA room, from April 2027", number_at=tk(0, "£8,000"),
               kicker="UNDER 65 · CASH ISA")


def s_changed(L, t):  # sentences 1-2 · question + twist 1: the cut is scrapped
    beat(L, "changed", t, S(1) - 0.1, sub="BUDGET 2026 · 28 OCT", sub_at=S(1) + 0.2)
    L.emoji("party_popper", W / 2, 500, 150, t, S(1), bounce=True)
    chip(L, "PLANNED: " + gbp(PLANNED_CASH_LIMIT), W / 2, 660, t, tk(2, "scrapped"), "red", 50,
         emoji="cross_mark")
    L.text("STAYS AT", W / 2, 790, 46, M, ramp(t, tk(2, "stays"), 0.3), weight="ExtraBold")
    big_number(L, gbp(ISA_LIMIT), W / 2, 910, t, at=tk(2, "£20,000"), size=170)
    checked(L, STAMP, W / 2, 1080, t, tk(2, "£20,000") + 0.5)


def s_strange(L, t):  # sentences 3-4 · rehook + question 2: savings tax rises outside ISAs
    beat(L, "who", t, S(3) - 0.1, sub="HERE'S THE STRANGE PART", sub_at=tk(3, "But"))
    L.emoji("thinking_face", W / 2, 510, 150, t, S(3), bounce=True)
    L.text("TAX ON SAVINGS INTEREST", W / 2, 680, 44, M, ramp(t, tk(4, "tax"), 0.3), weight="ExtraBold")
    chip(L, "OUTSIDE ISAs", W / 2, 780, t, tk(4, "outside"), "white", 44, emoji="chart_increasing")
    chip(L, f"BASIC RATE {SAVINGS_BASIC_NOW}% NOW", W / 2 - 215, 900, t, tk(4, "outside") + 0.3, "white", 30)
    chip(L, f"{SAVINGS_BASIC_2027}% FROM APRIL 2027", W / 2 + 215, 900, t, tk(4, "outside") + 0.6, "red", 30)
    checked(L, STAMP_RATES, W / 2, 1020, t, tk(4, "outside") + 0.9)


def s_means(L, t):  # sentences 5-6 · twist 2 + answer: the ISA is worth more now
    beat(L, "means", t, S(5) - 0.1)
    big_number(L, "MORE VALUABLE", W / 2, 470, t, at=tk(5, "valuable"), size=96)
    versus(L, t,
           dict(title="OUTSIDE AN ISA", label="TAX RATE", value="RISES", color=RED, start=S(6),
                at=tk(6, "rises"), tone="red", emoji="chart_increasing"),
           dict(title="INSIDE AN ISA", label="TAX", value="£0", color=G, start=tk(6, "Inside"),
                at=tk(6, "zero"), tone="green", emoji="shield"),
           cy=720, h=300)
    caveat(L, t, tk(6, "zero") + 0.3, [f"Most basic-rate savers still pay nothing on their first",
                                       f"{gbp(PSA_BASIC)} of interest. Not advice."], cy=960, size=26)


def s_loop(L, t):  # sentence 7: loop line back into sentence 0
    loop_close(L, t, 7, comment="RIGHT CALL? COMMENT")


SCENES = [(0, 0), (1, 2), (3, 4), (5, 6), (7, 7)]
DRAW = [s_hook, s_changed, s_strange, s_means, s_loop]


def events():
    ev = [{"t": tk(0, "£8,000") + 0.05, "kind": "boom"},
          {"t": tk(2, "scrapped"), "kind": "pop"},
          {"t": tk(2, "£20,000"), "kind": "coin"},
          {"t": tk(4, "outside"), "kind": "boom"},
          {"t": tk(5, "valuable"), "kind": "pop"},
          {"t": tk(6, "zero"), "kind": "coin"}]
    return scene_events(ev)
