"""Video 019 (brand-v2, format: since, told as the dopamine loop — BRAND.md §0c): the adult ISA allowance since
ISAs began in April 1999 vs what £7,000 would be if it had kept pace with prices (CPI), and the cash ISA cut from
6 April 2027. (data checked 28 Oct 2026, before the Autumn Budget statement that afternoon)

ISA subscription limits (overall), HMRC:
  1999-00 to 2007-08 £7,000 (cash £3,000); 2008-09 £7,200 ... 2014-15 £11,880 then £15,000 from 1 July 2014;
  2015-16 and 2016-17 £15,240; 2017-18 onward £20,000.
  https://assets.publishing.service.gov.uk/government/uploads/system/uploads/attachment_data/file/737084/Table_9.4_Published_August_2018.pdf
  https://www.gov.uk/government/statistics/annual-savings-statistics-2026/annual-savings-statistics-background-and-methodology
  (Table 1, published 16 Sep 2026: 2017-18 to 2026-27 £20,000)
Cash ISA from 6 April 2027: £12,000 a year for under-65s, £20,000 for 65 and over; overall limit stays £20,000
  (HMRC Tax-free savings newsletter 19, November 2025):
  https://www.gov.uk/government/publications/tax-free-savings-newsletter-19/tax-free-savings-newsletter-19-november-2025
CPI index (ONS D7BT, 2015=100), April of each year + Sep 2026 (latest, released 21 Oct 2026):
  https://www.ons.gov.uk/economy/inflationandpriceindices/timeseries/d7bt
Assumptions: "keeping pace" = the limit uprated by CPI from April of the base year to September 2026 (the latest
CPI month). "Over nine years" = 6 April 2017 to 28 October 2026.
"""
from datetime import date

from motion import *  # noqa: F401,F403
from brand import *  # noqa: F401,F403

BRAND = True
COVER = dict(words=("ISA", "SHRINKING?"), highlight=1, hero="Shield", left="Calendar", right="Scissors",
             particles="Coin")

# ---- data (official, checked 28 Oct 2026) --------------------------------------------------------------------
LIMIT = {y: 7000 for y in range(1999, 2008)}          # HMRC, tax year starting 6 April y
LIMIT.update({2008: 7200, 2009: 7200, 2010: 10200, 2011: 10680, 2012: 11280, 2013: 11520, 2014: 11880,
              2015: 15240, 2016: 15240})
LIMIT.update({y: 20000 for y in range(2017, 2027)})
LIMIT_JUL_2014 = 15000                                 # from 1 July 2014 (NISA)
CASH_ISA_2027_UNDER_65 = 12000                         # from 6 April 2027
CPI_APR = {1999: 72.2, 2000: 72.6, 2001: 73.4, 2002: 74.4, 2003: 75.5, 2004: 76.4, 2005: 77.8, 2006: 79.4,
           2007: 81.6, 2008: 84.0, 2009: 86.0, 2010: 89.2, 2011: 93.2, 2012: 96.0, 2013: 98.3, 2014: 100.1,
           2015: 99.9, 2016: 100.2, 2017: 102.9, 2018: 105.4, 2019: 107.6, 2020: 108.5, 2021: 110.1,
           2022: 120.0, 2023: 130.4, 2024: 133.5, 2025: 138.2, 2026: 142.1}
CPI_SEP_2026 = 144.1

# ---- figures, all computed ------------------------------------------------------------------------------------
LIMIT_NOW = LIMIT[2026]
PRICE_RATIO = CPI_SEP_2026 / CPI_APR[1999]                      # 1.996: "prices have almost doubled"
PACE_1999 = LIMIT[1999] * PRICE_RATIO                            # 13,971: £7,000 kept in step with prices
PACE_2017 = LIMIT[2017] * CPI_SEP_2026 / CPI_APR[2017]           # 28,008: £20,000 kept in step since 2017
FROZEN_YEARS = (date(2026, 10, 28) - date(2017, 4, 6)).days / 365.25   # 9.56
REAL_NOW_2017 = LIMIT_NOW * CPI_APR[2017] / CPI_SEP_2026         # 14,282: today's £20,000 in April-2017 pounds
CASH_CUT = LIMIT_NOW - CASH_ISA_2027_UNDER_65                    # 8,000 less cash ISA room for under-65s
assert LIMIT_NOW == 20000 and LIMIT[1999] == 7000 and CASH_ISA_2027_UNDER_65 == 12000
assert 1.9 < PRICE_RATIO < 2.0                                   # "almost doubled"
assert round(PACE_1999, -3) == 14000 and LIMIT_NOW > PACE_1999   # "about £14,000 ... your limit won"
assert round(PACE_2017, -3) == 28000                             # "about £28,000"
assert 9 < FROZEN_YEARS < 10                                     # "over nine years"
assert CASH_CUT == 8000

# chart: x = years since April 1999, y in £ thousands
LIM_PTS = []
for y in range(1999, 2027):
    v = LIMIT[y] / 1000
    if LIM_PTS and LIM_PTS[-1][1] != v:
        LIM_PTS.append((y - 1999, LIM_PTS[-1][1]))      # step up on 6 April
    LIM_PTS.append((y - 1999, v))
    if y == 2014:
        LIM_PTS += [(15.25, v), (15.25, LIMIT_JUL_2014 / 1000)]
LIM_PTS.append((27.45, LIMIT_NOW / 1000))
PACE_PTS = [(y - 1999, LIMIT[1999] * CPI_APR[y] / CPI_APR[1999] / 1000) for y in range(1999, 2027)]
PACE_PTS.append((27.45, PACE_1999 / 1000))

STAMP_HMRC = "HMRC · ISA LIMITS · CHECKED 28 OCT 2026"
STAMP_ONS = "ONS · CPI, SEP 2026 · CHECKED 28 OCT 2026"
STAMP_2027 = "GOV.UK · FROM 6 APRIL 2027 · CHECKED 28 OCT 2026"


def s_hook(L, t):  # sentence 0 · risk
    cover_hook(L, t, gbp(LIMIT_NOW), sub="a year, tax-free", number_at=tk(0, "£20,000"),
               kicker="THE ISA LIMIT, 1999 TO NOW")


def s_risk(L, t):  # sentence 1 · risk: the deadline
    beat(L, "NEXT APRIL", t, S(1) - 0.1, tone="red")
    L.emoji("calendar", W / 2, 560, 220, t, S(1) + 0.05, bounce=True)
    chip(L, "6 APRIL 2027", W / 2, 760, t, tk(1, "April"), "red", 52, emoji="alarm_clock")
    chip(L, "CASH SAVERS GET LESS", W / 2, 880, t, tk(1, "less"), "white", 38, emoji="bank")


def s_then(L, t):  # sentence 2 · context
    beat(L, "then", t, S(2) - 0.1, sub="APRIL 1999", sub_at=tk(2, "ISAs"))
    value_card(L, W / 2, 560, 860, t, S(2) + 0.1, "shield", "THE FIRST ISA LIMIT", gbp(LIMIT[1999]),
               value_at=tk(2, "£7,000"), color=Wt, sub="a year, tax-free")
    checked(L, STAMP_HMRC, W / 2, 760, t, tk(2, "limit.") - 0.1)


def s_chart(L, t):  # sentences 3-4 · question + twist: prices doubled, the limit beat them
    beat(L, "today", t, S(3) - 0.1, sub="1999 TO 2026", sub_at=S(3) + 0.3)
    box = (190, 480, 800, 960)
    ylab = [(10, "£10K"), (20, "£20K"), (30, "£30K")]
    xlab = [(0, "1999"), (13, "2012"), (27, "2026")]
    line_chart(L, t, S(3) + 0.1, 2.2, [(PACE_PTS, RED, 8)], box, 28, 32, x_labels=xlab, y_labels=ylab,
               end_tags=[(0, "£14K", RED, tk(4, "£14,000"), 8)])
    line_chart(L, t, tk(4, "so"), 1.6, [(LIM_PTS, G, 8)], box, 28, 32,
               end_tags=[(0, "£20K", G, tk(4, "won."), -8)])
    chip(L, "PRICES", 300, 410, t, S(3) + 0.3, "red", 28, emoji="shopping_cart")
    chip(L, "YOUR LIMIT", 790, 410, t, tk(4, "so"), "green", 28, emoji="shield")
    checked(L, STAMP_ONS, W / 2, 1070, t, tk(4, "£14,000") + 0.3)


def s_frozen(L, t):  # sentence 5 · rehook: frozen since 2017
    beat(L, "catch", t, S(5) - 0.1)
    L.emoji("locked", W / 2, 540, 220, t, tk(5, "frozen"), bounce=True)
    chip(L, "£20,000 SINCE APRIL 2017", W / 2, 740, t, tk(5, "frozen"), "white", 44, emoji="calendar")
    chip(L, "OVER 9 YEARS", W / 2, 850, t, tk(5, "nine"), "red", 44, emoji="hourglass_done")


def s_gap(L, t):  # sentences 6-7 · question + twist 2: £20,000 would need to be £28,000
    beat(L, "THE GAP", t, S(6) - 0.1, tone="red")
    versus(L, t,
           dict(title="YOUR LIMIT", label="TODAY", value=gbp(LIMIT_NOW), color=G, start=S(6) + 0.1,
                at=S(6) + 0.2, tone="green", emoji="shield"),
           dict(title="KEEPING PACE", label="SINCE 2017", value=gbp(round(PACE_2017, -3)), color=RED,
                start=tk(7, "Keeping"), at=tk(7, "£28,000"), emoji="chart_increasing"),
           cy=600, h=320)
    chip(L, "PRICES UP OVER 40% SINCE 2017", W / 2, 840, t, S(6) + 0.3, "red", 36, emoji="shopping_cart")
    checked(L, STAMP_ONS, W / 2, 950, t, tk(7, "£28,000") + 0.3)


def s_cut(L, t):  # sentence 8 · answer: the cash ISA cut
    beat(L, "miss", t, S(8) - 0.1)
    L.text("CASH ISA, UNDER 65s", W / 2, 470, 44, M, ramp(t, tk(8, "under"), 0.25), weight="ExtraBold")
    big_number(L, gbp(CASH_ISA_2027_UNDER_65), W / 2, 610, t, at=tk(8, "£12,000"), size=200, color=RED)
    chip(L, "65 AND OVER: STILL £20,000", W / 2, 770, t, tk(8, "cash"), "white", 34, emoji="old_woman")
    checked(L, STAMP_2027, W / 2, 870, t, tk(8, "ISA.") - 0.1)
    caveat(L, t, tk(8, "ISA.") - 0.2, ["Total ISA limit stays £20,000. Rules as at 28 Oct 2026, before the Budget.",
                                      "General education, not financial advice."], cy=1000, size=24)


def s_loop(L, t):  # sentence 9: loop line back into sentence 0
    loop_close(L, t, 9, comment="GENEROUS OR NOT? COMMENT")


SCENES = [(0, 0), (1, 1), (2, 2), (3, 4), (5, 5), (6, 7), (8, 8), (9, 9)]
DRAW = [s_hook, s_risk, s_then, s_chart, s_frozen, s_gap, s_cut, s_loop]

PRICES_UP_2017 = 100 * (CPI_SEP_2026 / CPI_APR[2017] - 1)        # 40.0%
assert PRICES_UP_2017 > 40


def events():
    ev = [{"t": tk(0, "£20,000") + 0.05, "kind": "coin"},
          {"t": tk(0, "shrinking"), "kind": "boom"},
          {"t": tk(1, "April"), "kind": "pop"},
          {"t": tk(2, "£7,000"), "kind": "pop"},
          {"t": tk(4, "won."), "kind": "coin"},
          {"t": tk(5, "frozen"), "kind": "boom"},
          {"t": tk(7, "£28,000"), "kind": "boom"},
          {"t": tk(8, "£12,000"), "kind": "boom"}]
    return scene_events(ev)
