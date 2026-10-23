"""Video 011 (brand-v2, format: since): the full new State Pension since 2016 vs the tax-free Personal
Allowance — it has nearly caught up. (data checked 23 Oct 2026)

Full new State Pension, a week:
  2016/17 £155.65 — DWP "Benefit and pension rates from 6 April 2016",
    https://assets.publishing.service.gov.uk/government/uploads/system/uploads/attachment_data/file/524117/benefit-and-pension-rates-from-6-april-2016.pdf
  2026/27 £241.30 — https://www.gov.uk/government/publications/benefit-and-pension-rates-2026-to-2027/proposed-benefit-and-pension-rates-2026-to-2027
Personal Allowance:
  2016/17 £11,000 — https://www.gov.uk/government/publications/tax-and-tax-credit-rates-and-thresholds-for-2016-17/tax-and-tax-credit-rates-and-thresholds-for-2016-17
  2026/27 £12,570 — https://www.gov.uk/income-tax-rates ; held at £12,570 to 5 April 2031:
    https://www.gov.uk/government/publications/maintaining-income-tax-and-equivalent-national-insurance-contributions-thresholds-until-5-april-2031
CPI index (ONS D7BT, 2015=100): Apr 2016 100.2, Sep 2026 144.1 (release 21 Oct 2026),
  https://www.ons.gov.uk/economy/inflationandpriceindices/timeseries/d7bt/mm23
Triple lock: "increases annually by the highest of inflation, average earnings growth or 2.5%",
  https://www.gov.uk/government/news/huge-income-boost-for-millions-of-pensioners-and-working-people
Pledge: Budget 2025 (para 4.167) — pensioners whose sole income is the basic or new State Pension without
  increments won't have to pay small amounts of tax via Simple Assessment from 2027-28; Exchequer Secretary
  (Jan 2026): they "will not have to pay income tax over this Parliament"; details due at the Budget on
  28 Oct 2026. House of Commons Library CBP-10250 (22 Sep 2026),
  https://researchbriefings.files.parliament.uk/documents/CBP-10250/CBP-10250.pdf
Assumptions: a year = 52 weeks; "prices" = CPI from April 2016 to Sep 2026 (latest month).
"""
from motion import *  # noqa: F401,F403
from brand import *  # noqa: F401,F403

BRAND = True
COVER = dict(words=("PENSION", "TAXED?"), highlight=1, hero="Old man", left="Hourglass not done", right="Receipt",
             particles="Coin")

# ---- data (official, checked 23 Oct 2026) ------------------------------------------------------------------
SP_2016, SP_NOW = 155.65, 241.30          # full new State Pension, £ a week
PA_2016, PA_NOW = 11_000, 12_570          # Personal Allowance
CPI_2016, CPI_NOW = 100.2, 144.1          # ONS D7BT, Apr 2016 and Sep 2026
WEEKS = 52

# ---- figures, all computed ---------------------------------------------------------------------------------
SP16_Y = SP_2016 * WEEKS                   # 8,093.80
SPN_Y = SP_NOW * WEEKS                     # 12,547.60
GAP16 = PA_2016 - SP16_Y                   # 2,906.20 -> "nearly £3,000"
GAP_NOW = PA_NOW - SPN_Y                   # 22.40 -> "just £22"
SP_UP = round((SP_NOW / SP_2016 - 1) * 100)
CPI_UP = round((CPI_NOW / CPI_2016 - 1) * 100)
assert round(SP16_Y, 2) == 8_093.80 and round(SPN_Y, 2) == 12_547.60
assert 2_800 < GAP16 < 3_000                                   # "nearly £3,000"
assert round(GAP_NOW, 2) == 22.40 and round(GAP_NOW) == 22    # "just £22"
assert (SP_UP, CPI_UP) == (55, 44)
RISE_NEEDED = GAP_NOW / SPN_Y * 100        # 0.18%: any rise above this crosses the line
assert RISE_NEEDED < 2.5                   # even the triple lock's 2.5% floor crosses it

STAMP_RATES = "GOV.UK · 2016/17 & 2026/27 RATES · CHECKED 23 OCT 2026"


def s_hook(L, t):  # sentence 0
    cover_hook(L, t, gbp(round(GAP_NOW)), sub="a year from being taxed", number_at=tk(0, "£22"),
               kicker="FULL NEW STATE PENSION")


def s_then(L, t):  # sentence 1
    beat(L, "then", t, S(1) - 0.1, sub="2016/17, A YEAR", sub_at=tk(1, "2016"))
    versus(L, t,
           dict(title="STATE PENSION", label="FULL NEW RATE", value=gbp(SP16_Y), color=Wt, start=S(1),
                at=tk(1, "2016"), emoji="old_man"),
           dict(title="TAX-FREE", label="PERSONAL ALLOWANCE", value=gbp(PA_2016), color=G, start=S(1) + 0.2,
                at=tk(1, "2016") + 0.3, tone="green", emoji="receipt"),
           cy=620, h=340)
    chip(L, "NEARLY £3,000 BELOW THE LINE", W / 2, 880, t, tk(1, "£3,000"), "cyan", 34)
    checked(L, STAMP_RATES, W / 2, 980, t, tk(1, "£3,000") + 0.4)


def s_today(L, t):  # sentences 2-3
    beat(L, "today", t, S(2) - 0.1, sub="SINCE APRIL 2016", sub_at=S(2) + 0.2)
    bar_chart(L, t, S(2) + 0.1, [SP_UP, CPI_UP], ["STATE PENSION", "PRICES"], (260, 470, 820, 860), [G, RED],
              dur=0.7, stagger=tk(3, "Prices") - S(2) - 0.25, label_size=28,
              value_tags={0: (f"+{SP_UP}%", G, tk(2, "55%")), 1: (f"+{CPI_UP}%", RED, tk(3, "44%"))})
    checked(L, "GOV.UK · ONS CPI · CHECKED 23 OCT 2026", W / 2, 990, t, tk(3, "44%") + 0.3)


def s_lock(L, t):  # sentence 4
    beat(L, "THE TRIPLE LOCK", t, S(4) - 0.1)
    L.emoji("locked", W / 2, 510, 170, t, S(4), bounce=True)
    L.text("THE HIGHEST OF", W / 2, 660, 40, M, ramp(t, tk(4, "highest"), 0.25), weight="ExtraBold")
    for (label, word, x, tone) in (("PRICES", "prices", 270, "white"), ("WAGES", "wages", 540, "white"),
                                   ("2.5%", "two", 810, "gold")):
        chip(L, label, x, 760, t, tk(4, word), tone, 44)


def s_twist(L, t):  # sentences 5-6
    beat(L, "twist", t, S(5) - 0.1)
    value_card(L, W / 2, 480, 880, t, S(5), "locked", "TAX-FREE ALLOWANCE", gbp(PA_NOW), color=Wt,
               value_at=tk(5, "Frozen"), h=150, sub="frozen until 2031")
    value_card(L, W / 2, 660, 880, t, S(6), "old_man", "STATE PENSION, A YEAR", gbp(round(SPN_Y)), color=G,
               value_at=tk(6, "rise"), h=150, sub=f"full new rate · just {gbp(round(GAP_NOW))} below")
    chip(L, "ONE MORE RISE = OVER THE LINE", W / 2, 850, t, tk(6, "crosses"), "red", 34, emoji="warning")
    checked(L, "GOV.UK · 2026/27 RATES · CHECKED 23 OCT 2026", W / 2, 950, t, tk(6, "crosses") + 0.4)


def s_good(L, t):  # sentence 7
    beat(L, "THE GOOD NEWS", t, S(7) - 0.1)
    L.emoji("shield", W / 2, 510, 170, t, S(7), bounce=True)
    L.text("STATE PENSION YOUR ONLY INCOME?", W / 2, 680, 42, Wt, ramp(t, tk(7, "only"), 0.25))
    chip(L, "NO TAX TO PAY, SAYS THE GOVERNMENT", W / 2, 780, t, tk(7, "won't"), "green", 34,
         emoji="check_mark_button")
    checked(L, "COMMONS LIBRARY · BUDGET 2025 · CHECKED 23 OCT 2026", W / 2, 880, t, tk(7, "tax.") - 0.2)
    caveat(L, t, tk(7, "tax.") + 0.1, ["Details due in the Budget, 28 Oct 2026. New State Pension, no extras.",
                                       "General education, not financial advice."], cy=990, size=24)


def s_loop(L, t):  # sentence 8: loop line back into sentence 1
    loop_close(L, t, 8, comment="TAX IT? YES OR NO? COMMENT")


SCENES = [(0, 0), (1, 1), (2, 3), (4, 4), (5, 6), (7, 7), (8, 8)]
DRAW = [s_hook, s_then, s_today, s_lock, s_twist, s_good, s_loop]


def events():
    ev = [{"t": tk(0, "£22") + 0.05, "kind": "boom"},
          {"t": tk(1, "£3,000"), "kind": "pop"},
          {"t": tk(2, "55%"), "kind": "coin"}, {"t": tk(3, "44%"), "kind": "pop"},
          {"t": tk(4, "prices"), "kind": "pop"}, {"t": tk(4, "wages"), "kind": "pop"},
          {"t": tk(4, "two"), "kind": "pop"},
          {"t": tk(5, "Frozen"), "kind": "boom"},
          {"t": tk(6, "crosses"), "kind": "boom"},
          {"t": tk(7, "won't"), "kind": "coin"}]
    return scene_events(ev)
