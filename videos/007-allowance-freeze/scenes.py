"""Video 007 (brand-v2, format: since): the Personal Allowance since 2010 vs prices — it beat inflation until
2021, then the freeze. (data checked 22 Oct 2026)

Personal Allowance (standard / under-65s):
  2010-11 £6,475  — Finance Act 2010 s.1, https://www.legislation.gov.uk/ukpga/2010/13/section/1/notes/data.htm
  2021-22 £12,570 — SI 2021/111 art.3(a), https://legislation.gov.uk/uksi/2021/111/made
  2026-27 £12,570 — https://www.gov.uk/income-tax-rates (basic rate 20% on £12,571-£50,270, rUK)
  kept at £12,570 to 5 April 2031 — https://www.gov.uk/government/publications/maintaining-income-tax-and-equivalent-national-insurance-contributions-thresholds-until-5-april-2031
    (published 26 Nov 2025: "from 6 April 2028 to 5 April 2031")
CPI index (ONS D7BT, 2015=100), https://www.ons.gov.uk/economy/inflationandpriceindices/timeseries/d7bt/mm23
  release 21 Oct 2026, latest month Sep 2026. April = start of each tax year.
Assumptions: "kept in line with prices" = the allowance scaled by CPI from the April it was set to Sep 2026
(the latest CPI month). The £776 is the basic-rate (20%) tax on the extra £3,880, for someone earning at least
£16,450 in England, Wales or Northern Ireland; it ignores National Insurance and other thresholds.
"""
from motion import *  # noqa: F401,F403
from brand import *  # noqa: F401,F403

BRAND = True
COVER = dict(words=("ALLOWANCE", "FROZEN"), highlight=1, hero="Ice", left="Receipt", right="Calendar",
             particles="Snowflake")

# ---- data (official) --------------------------------------------------------------------------------------
PA_2010, PA_2021, PA_NOW = 6_475, 12_570, 12_570
FROZEN_UNTIL = 2031
BASIC = 0.20
CPI = {  # ONS D7BT, checked 22 Oct 2026
    (2010, 4): 89.2,
    (2021, 4): 110.1, (2022, 4): 120.0, (2022, 10): 126.2, (2023, 4): 130.4, (2023, 10): 132.0,
    (2024, 4): 133.5, (2024, 10): 135.0, (2025, 4): 138.2, (2025, 10): 139.8, (2026, 4): 142.1,
    (2026, 9): 144.1,
}
LATEST = (2026, 9)

# ---- figures, all computed --------------------------------------------------------------------------------
IF_PRICES_2010 = PA_2010 * CPI[LATEST] / CPI[(2010, 4)]        # 10,460.3
IF_PRICES_2021 = PA_2021 * CPI[LATEST] / CPI[(2021, 4)]        # 16,451.8
R2010 = int(round(IF_PRICES_2010, -1))
R2021 = int(round(IF_PRICES_2021, -1))
GAP = R2021 - PA_NOW                                           # on the rounded figure, as said
TAX = round(GAP * BASIC)
EXACT_TAX = (IF_PRICES_2021 - PA_NOW) * BASIC
assert (R2010, R2021, GAP, TAX) == (10_460, 16_450, 3_880, 776)
assert abs(EXACT_TAX - TAX) < 1                                # 776.36 unrounded
assert PA_NOW / PA_2010 > 1.9                                  # "nearly doubled"
assert PA_NOW > IF_PRICES_2010                                 # beat prices since 2010

STAMP = "GOV.UK · LEGISLATION.GOV.UK · ONS CPI · CHECKED 22 OCT 2026"


def s_hook(L, t):  # sentence 0
    cover_hook(L, t, gbp(TAX), sub="a year, from the frozen allowance", number_at=tk(0, "£776"),
               kicker="BASIC-RATE TAXPAYERS")


def s_then(L, t):  # sentence 1
    beat(L, "then", t, S(1) - 0.1)
    value_card(L, W / 2, 560, 880, t, S(1), "calendar", "TAX-FREE ALLOWANCE · 2010", gbp(PA_2010), color=Wt,
               value_at=tk(1, "£6"), sub="2010-11 tax year")
    checked(L, "LEGISLATION.GOV.UK · FINANCE ACT 2010 · CHECKED 22 OCT 2026", W / 2, 720, t, tk(1, "£6") + 0.4)


def s_path(L, t):  # sentences 2-3
    beat(L, "today", t, S(2) - 0.1)
    vals = [PA_2010, R2010, PA_NOW]
    bar_chart(L, t, S(2), vals, ["2010", "2010 + PRICES", "2021-2031"], (170, 520, 910, 1010),
              [M, C, G], dur=0.8, stagger=0.0, vmax=13_500,
              value_tags={0: (gbp(PA_2010), Wt, S(2) + 0.2), 1: (gbp(R2010), C, tk(2, "£10")),
                          2: (gbp(PA_NOW), G, tk(3, "£12"))})
    chip(L, f"FROZEN UNTIL {FROZEN_UNTIL}", W / 2, 1110, t, tk(3, "froze"), "cyan", 32, emoji="locked")
    checked(L, STAMP, W / 2, 1200, t, tk(3, "2031") + 0.3)


def s_twist(L, t):  # sentences 4-5
    beat(L, "twist", t, S(4) - 0.1, sub="SINCE APRIL 2021", sub_at=S(4) + 0.2)
    keys = sorted(CPI)[1:]
    x = lambda k: (k[0] - 2021) + (k[1] - 4) / 12
    BASE = 10_000                    # the chart's baseline is £10k (labelled), so the gap is readable
    prices = [(x(k), PA_2021 * CPI[k] / CPI[(2021, 4)] - BASE) for k in keys]
    frozen = [(0, PA_NOW - BASE), (x(LATEST), PA_NOW - BASE)]
    xmax = x(LATEST)
    line_chart(L, t, S(4) + 0.1, 1.6, [(frozen, G, 7), (prices, RED, 7)], (190, 480, 760, 880), xmax, 7_500,
               x_labels=[(0, "2021"), (xmax, "2026")],
               y_labels=[(0, "£10k"), (5_000, "£15k")],
               end_tags=[(1, gbp(R2021), RED, tk(4, "£16"), -10), (0, gbp(PA_NOW), G, S(4) + 1.2, 18)])
    L.text("KEPT UP WITH PRICES", 400, 455, 26, RED, ramp(t, S(4) + 1.0, 0.3), weight="ExtraBold")
    timed_line(L, [(gbp(GAP), Wt, tk(5, "£3")), ("× 20%", M, tk(5, "20%")), ("=", M, tk(5, "20%") + 0.3),
                   (gbp(TAX), RED, tk(5, "20%") + 0.5)], W / 2, 1040, 76, t)
    caveat(L, t, S(5) + 1.2, ["Basic-rate taxpayer, England, Wales & NI. CPI to Sep 2026.",
                              "General education, not financial advice."], cy=1160, size=26)


def s_loop(L, t):  # sentence 6
    loop_close(L, t, 6, comment="AT 40% TAX: HOW MUCH? COMMENT")


SCENES = [(0, 0), (1, 1), (2, 3), (4, 5), (6, 6)]
DRAW = [s_hook, s_then, s_path, s_twist, s_loop]


def events():
    ev = [{"t": tk(0, "£776") + 0.05, "kind": "coin"},
          {"t": tk(1, "£6"), "kind": "pop"},
          {"t": tk(2, "£10"), "kind": "pop"},
          {"t": tk(3, "£12"), "kind": "coin"},
          {"t": tk(3, "froze"), "kind": "boom"},
          {"t": tk(4, "£16"), "kind": "pop"},
          {"t": tk(5, "£3"), "kind": "pop"},
          {"t": tk(5, "20%") + 0.5, "kind": "boom"}]
    return scene_events(ev)
