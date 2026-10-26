"""Video 015 (brand-v2, format: since, told as the dopamine loop — BRAND.md §0c): £100 of cash since January
2010, growing at Bank Rate every day, vs what the same shopping costs today (CPI). (data checked 26 Oct 2026)

Bank Rate changes (Bank of England, "Official Bank Rate history"), checked 26 Oct 2026:
  https://www.bankofengland.co.uk/boeapps/database/Bank-Rate.asp
  0.50% from 5 Mar 2009 ... 3.75% from 18 Dec 2025 (held 18 Jun, 30 Jul, 17 Sep 2026; next decision 5 Nov 2026,
  https://www.bankofengland.co.uk/monetary-policy/the-interest-rate-bank-rate)
CPI index (ONS D7BT, 2015=100), release 21 Oct 2026, latest month Sep 2026:
  https://www.ons.gov.uk/economy/inflationandpriceindices/timeseries/d7bt/mm23
CPI 12-month rate, Sep 2026: 3.5% (ONS bulletin "Consumer price inflation, UK: September 2026"):
  https://www.ons.gov.uk/economy/inflationandpriceindices/bulletins/consumerpriceinflation/september2026
Assumptions: £100 deposited on 1 Jan 2010, earning exactly Bank Rate, interest added daily (rate / 365) and
left in, no tax, to 30 Sep 2026 (the latest CPI month). "Prices" = CPI from Jan 2010 to Sep 2026. Bank Rate is
the Bank of England's benchmark, not a savings account: real accounts paid more or less than it.
"""
from datetime import date, timedelta

from motion import *  # noqa: F401,F403
from brand import *  # noqa: F401,F403

BRAND = True
COVER = dict(words=("CASH", "SHRANK?"), highlight=1, hero="Jar", fill="Coin", left="Calendar", right="Shopping cart",
             particles="Coin")

# ---- data (official, checked 26 Oct 2026) --------------------------------------------------------------------
BANK_RATE = [  # (date changed, % a year) — Bank of England
    (date(2009, 3, 5), 0.50), (date(2016, 8, 4), 0.25), (date(2017, 11, 2), 0.50), (date(2018, 8, 2), 0.75),
    (date(2020, 3, 11), 0.25), (date(2020, 3, 19), 0.10), (date(2021, 12, 16), 0.25), (date(2022, 2, 3), 0.50),
    (date(2022, 3, 17), 0.75), (date(2022, 5, 5), 1.00), (date(2022, 6, 16), 1.25), (date(2022, 8, 4), 1.75),
    (date(2022, 9, 22), 2.25), (date(2022, 11, 3), 3.00), (date(2022, 12, 15), 3.50), (date(2023, 2, 2), 4.00),
    (date(2023, 3, 23), 4.25), (date(2023, 5, 11), 4.50), (date(2023, 6, 22), 5.00), (date(2023, 8, 3), 5.25),
    (date(2024, 8, 1), 5.00), (date(2024, 11, 7), 4.75), (date(2025, 2, 6), 4.50), (date(2025, 5, 8), 4.25),
    (date(2025, 8, 7), 4.00), (date(2025, 12, 18), 3.75),
]
CPI_JAN = {  # ONS D7BT, January of each year
    2010: 87.8, 2011: 91.3, 2012: 94.6, 2013: 97.1, 2014: 99.0, 2015: 99.3, 2016: 99.5, 2017: 101.4,
    2018: 104.4, 2019: 106.3, 2020: 108.2, 2021: 109.0, 2022: 114.9, 2023: 126.4, 2024: 131.5, 2025: 135.4,
    2026: 139.5,
}
CPI_SEP_2026 = 144.1
CPI_RATE_SEP_2026 = 3.5      # % in the 12 months to Sep 2026 (ONS)
START, END = date(2010, 1, 1), date(2026, 9, 30)


def rate_on(d):
    return [r for (c, r) in BANK_RATE if c <= d][-1]


def cash_at(end):
    """£100 from 1 Jan 2010 at Bank Rate, interest added daily, to `end`."""
    v, d = 100.0, START
    while d < end:
        v *= 1 + rate_on(d) / 100 / 365
        d += timedelta(days=1)
    return v


# ---- figures, all computed ------------------------------------------------------------------------------------
CASH_NOW = cash_at(END)                                    # 126.73
CASH_2021 = cash_at(date(2022, 1, 1))                      # 105.53 after 12 years
PRICE_NOW = 100 * CPI_SEP_2026 / CPI_JAN[2010]             # 164.12: what £100 of 2010 shopping costs now
REAL_NOW = CASH_NOW * CPI_JAN[2010] / CPI_SEP_2026         # 77.22: the £127 in 2010 pounds
LOST_PCT = round(100 - REAL_NOW)                           # 23% of buying power gone
RATE_NOW = rate_on(date(2026, 10, 26))
assert round(CASH_NOW) == 127 and round(PRICE_NOW) == 164
assert round(cash_at(date(2026, 10, 26))) == 127           # same figure if counted to today
assert CASH_2021 < 106                                     # "for years, your cash earned almost nothing"
assert round(REAL_NOW) == 77 and LOST_PCT == 23
assert RATE_NOW == 3.75 and RATE_NOW > CPI_RATE_SEP_2026   # "Bank Rate is beating inflation" ...
assert RATE_NOW - CPI_RATE_SEP_2026 <= 0.25                # ... "only just"

# chart: yearly points (x = years since Jan 2010), plotted as value - 80 so the axis isn't mostly empty
YEARS = list(range(2010, 2027))
CASH_PTS = [(y - 2010, cash_at(date(y, 1, 1)) - 80) for y in YEARS] + [(16.75, CASH_NOW - 80)]
PRICE_PTS = [(y - 2010, 100 * CPI_JAN[y] / CPI_JAN[2010] - 80) for y in YEARS] + [(16.75, PRICE_NOW - 80)]

STAMP_BOE = "BANK OF ENGLAND · BANK RATE · CHECKED 26 OCT 2026"
STAMP_ONS = "ONS · CPI, SEP 2026 · CHECKED 26 OCT 2026"


def s_hook(L, t):  # sentence 0 · risk
    cover_hook(L, t, gbp(round(CASH_NOW)), sub="from £100 in 2010", number_at=tk(0, "£127"),
               kicker="CASH AT BANK RATE, 2010 TO NOW")


def s_then(L, t):  # sentence 1 · risk: since when, at what rate, and the deadline
    beat(L, "then", t, S(1) - 0.1, sub="JANUARY 2010", sub_at=tk(1, "2010"))
    value_card(L, W / 2, 520, 860, t, S(1) + 0.1, "bank", "SAVED IN CASH", "£100", value_at=tk(1, "cash"),
               color=Wt, sub="earning Bank Rate, every day")
    chip(L, "NEXT RATE DECISION: 5 NOVEMBER", W / 2, 720, t, tk(1, "reviews"), "red", 36, emoji="calendar")
    checked(L, STAMP_BOE, W / 2, 830, t, tk(1, "month.") - 0.1)


def s_chart(L, t):  # sentences 2-3 · question + twist: the cash line crawls, the price line runs away
    beat(L, "today", t, S(2) - 0.1, sub="2010 TO 2026", sub_at=S(2) + 0.3)
    box = (190, 470, 790, 960)
    ylab = [(20, "£100"), (50, "£130"), (80, "£160")]
    xlab = [(0, "2010"), (8, "2018"), (16, "2026")]
    line_chart(L, t, S(2) + 0.1, 2.4, [(CASH_PTS, G, 8)], box, 17, 95, x_labels=xlab, y_labels=ylab,
               end_tags=[(0, gbp(round(CASH_NOW)), G, S(2) + 2.4, 10)])
    line_chart(L, t, tk(3, "prices"), 2.6, [(PRICE_PTS, RED, 8)], box, 17, 95,
               end_tags=[(0, gbp(round(PRICE_NOW)), RED, tk(3, "£164"), -6)])
    chip(L, "YOUR CASH", 290, 410, t, S(2) + 0.4, "green", 28, emoji="bank")
    chip(L, "PRICES", 800, 410, t, tk(3, "prices"), "red", 28, emoji="shopping_cart")
    checked(L, STAMP_ONS, W / 2, 1070, t, tk(3, "£164") + 0.3)


def s_myth(L, t):  # sentences 4-5 · rehook + question 2
    beat(L, "twist", t, S(4) - 0.1)
    L.emoji("thinking_face", W / 2, 560, 200, t, S(4) + 0.1, bounce=True)
    L.text("EVERYONE SAYS:", W / 2, 760, 44, M, ramp(t, tk(5, "Everyone"), 0.25), weight="ExtraBold")
    chip(L, "CASH ALWAYS LOSES", W / 2, 860, t, tk(5, "always"), "red", 48, emoji="chart_decreasing")


def s_now(L, t):  # sentence 6 · twist 2: right now, Bank Rate beats prices
    beat(L, "RIGHT NOW", t, S(6) - 0.1, tone="green")
    versus(L, t,
           dict(title="BANK RATE", label="TODAY", value=f"{RATE_NOW:.2f}%", color=G, start=S(6) + 0.1,
                at=tk(6, "Bank"), tone="green", emoji="bank"),
           dict(title="INFLATION", label="YEAR TO SEP 2026", value=f"{CPI_RATE_SEP_2026:.1f}%", color=RED,
                start=S(6) + 0.3, at=tk(6, "beating"), emoji="shopping_cart"),
           cy=600, h=320)
    chip(L, "CASH IS WINNING", W / 2, 840, t, tk(6, "beating"), "green", 40, emoji="check_mark_button")
    checked(L, "BANK OF ENGLAND + ONS · CHECKED 26 OCT 2026", W / 2, 940, t, tk(6, "inflation.") - 0.1)


def s_catch(L, t):  # sentence 7 · the answer: the old loss stays
    beat(L, "catch", t, S(7) - 0.1)
    value_card(L, W / 2, 520, 880, t, S(7) + 0.1, "pound_banknote", "YOUR £127 BUYS WHAT", gbp(round(REAL_NOW)),
               color=RED, value_at=tk(7, "buying"), sub="bought in 2010")
    chip(L, f"{LOST_PCT}% OF ITS BUYING POWER GONE", W / 2, 720, t, tk(7, "lost"), "red", 38, emoji="warning")
    caveat(L, t, tk(7, "soon.") - 0.3, ["Bank Rate is a benchmark: real accounts paid more or less.",
                                        "General education, not financial advice."], cy=840, size=26)


def s_loop(L, t):  # sentence 8: loop line back into sentence 0
    loop_close(L, t, 8, comment="STILL KEEP CASH? COMMENT")


SCENES = [(0, 0), (1, 1), (2, 3), (4, 5), (6, 6), (7, 7), (8, 8)]
DRAW = [s_hook, s_then, s_chart, s_myth, s_now, s_catch, s_loop]


def events():
    ev = [{"t": tk(0, "£127") + 0.05, "kind": "coin"},
          {"t": tk(0, "less."), "kind": "boom"},
          {"t": tk(1, "reviews"), "kind": "pop"},
          {"t": tk(3, "£164"), "kind": "boom"},
          {"t": tk(5, "always"), "kind": "pop"},
          {"t": tk(6, "beating"), "kind": "coin"},
          {"t": tk(7, "lost"), "kind": "boom"}]
    return scene_events(ev)
