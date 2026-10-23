"""Video 009 (brand-v2, format: myth): "Premium Bonds beat a savings account" — half true.
(figures checked 23 Oct 2026)

NS&I October 2026 draw (nsandi.com press release PR261001): prize fund rate 4.35%, odds 21,000 to 1 per £1 Bond,
  137,483,797,618 eligible Bonds, 6,546,849 prizes worth £498,378,775; prizes by value below (PRIZES).
NS&I PR260818: 4.35% / 21,000 to 1 from the September 2026 draw; Direct Saver 3.75% gross/AER from 18 Aug 2026.
nsandi.com/products/direct-saver: Direct Saver 3.75% gross/AER, variable, interest taxable.
gov.uk/apply-tax-free-interest-on-savings: Personal Savings Allowance £1,000 basic rate, £500 higher rate, £0 additional.
gov.uk changes-to-tax-rates-for-property-savings-dividend-income: savings income taxed 20/40/45% now, 22/42/47% from April 2027.
"""
from motion import *  # noqa: F401,F403
from brand import *  # noqa: F401,F403

BRAND = True
COVER = dict(words=("PREMIUM", "BONDS"), highlight=1, hero="Ticket", left="Calendar", right="Game die",
             particles="Coin")

# ---- figures (NS&I October 2026 draw) -------------------------------------------------------------------
ELIGIBLE = 137_483_797_618
PRIZES = {1_000_000: 2, 100_000: 96, 50_000: 191, 25_000: 382, 10_000: 957, 5_000: 1_914, 1_000: 19_934,
          500: 59_802, 100: 2_371_145, 50: 2_371_145, 25: 1_721_281}
N_PRIZES = sum(PRIZES.values())
FUND = sum(v * n for v, n in PRIZES.items())
assert N_PRIZES == 6_546_849 and FUND == 498_378_775            # NS&I's published totals
RATE = FUND * 12 / ELIGIBLE                                      # annual prize fund rate
assert round(RATE * 100, 2) == 4.35
ODDS = ELIGIBLE / N_PRIZES
assert round(ODDS / 1000) == 21                                  # 21,000 to 1
P_WIN = N_PRIZES / ELIGIBLE                                      # chance one £1 Bond wins in one draw
HOLD, DRAWS = 1_000, 12
P_NOTHING = (1 - P_WIN) ** (HOLD * DRAWS)                        # £1,000 = 1,000 Bonds, 12 monthly draws
assert round(P_NOTHING * 100) == 56
SMALL = sum(v * n for v, n in PRIZES.items() if v < 1_000)
RATE_SMALL = SMALL * 12 / ELIGIBLE                               # the rate paid by prizes under £1,000
assert round(RATE_SMALL * 100, 1) == 3.7
JACKPOTS = PRIZES[1_000_000]
assert JACKPOTS == 2
SAVER = 0.0375                                                   # NS&I Direct Saver, gross/AER, taxable
assert RATE_SMALL < SAVER
HIGHER = 0.40
PSA_HIGHER = 500
SAVER_NET = SAVER * (1 - HIGHER)
assert round(SAVER_NET * 100, 2) == 2.25
EXP_PRIZES = P_WIN * HOLD * DRAWS                                # ~0.57 prizes a year on £1,000
MAX_HOLD = 50_000
Q_ANSWER = P_WIN * MAX_HOLD * DRAWS                               # comment answer (not shown): ~28.6
assert round(Q_ANSWER) == 29


def pct(x, nd):
    return f"{x * 100:.{nd}f}%"


def s_hook(L, t):  # sentence 0
    cover_hook(L, t, f"{round(P_NOTHING * 100)}%", sub="chance £1,000 wins nothing all year",
               number_at=tk(0, "56%"), kicker="£1,000 IN PREMIUM BONDS · 12 DRAWS")


def s_myth(L, t):  # sentence 1
    beat(L, "myth", t, S(1) - 0.1)
    a = ramp(t, S(1) + 0.1, 0.3)
    L.text("“Premium Bonds pay", W / 2, 510, 60, Wt, a)
    L.text(pct(RATE, 2) + ", beating", W / 2, 590, 60, Wt, a)
    L.text("savings”", W / 2, 670, 60, Wt, a)
    verdict_stamp(L, "HALF TRUE", W / 2, 790, t, tk(1, "beating") + 0.4, "gold", size=90)
    checked(L, "NS&I · OCTOBER 2026 DRAW · CHECKED 23 OCT 2026", W / 2, 1040, t, tk(1, "4.35%") + 0.3)


def s_truth(L, t):  # sentences 2-4
    beat(L, "truth", t, S(2) - 0.1, sub="4.35% IS AN AVERAGE", sub_at=tk(2, "average"))
    value_card(L, W / 2, 520, 820, t, S(2) + 0.1, "trophy", "HEADLINE PRIZE RATE",
               pct(RATE, 2), color=Wt, value_at=tk(2, "average"), sub=f"incl. {JACKPOTS} x £1m jackpots a month")
    value_card(L, W / 2, 700, 820, t, tk(3, "Without"), "wrapped_gift", "PRIZES UNDER £1,000",
               pct(RATE_SMALL, 1), color=G, value_at=tk(3, "3.7%"), sub="£25 to £500 prizes only")
    value_card(L, W / 2, 880, 820, t, tk(4, "below"), "bank", "NS&I DIRECT SAVER",
               pct(SAVER, 2), color=C, value_at=tk(4, "3.75%"), sub="easy access, taxable interest")
    checked(L, "NSANDI.COM · CHECKED 23 OCT 2026", W / 2, 1080, t, tk(4, "3.75%") + 0.3)


def s_catch(L, t):  # sentences 5-6
    beat(L, "catch", t, S(5) - 0.1, sub="WHEN IT IS TRUE", sub_at=S(5) + 0.2)
    versus(L, t,
           dict(title="DIRECT SAVER", label="AFTER 40% TAX", value=pct(SAVER_NET, 2), color=RED,
                start=tk(6, "Pay"), at=tk(6, "2.25%"), emoji="receipt"),
           dict(title="PREMIUM BONDS", label="PRIZES TAX FREE", value=pct(RATE_SMALL, 1),
                color=G, start=tk(5, "prizes"), at=tk(5, "free"), emoji="wrapped_gift"),
           cy=640, h=300)
    caveat(L, t, tk(6, "becomes") + 0.3,
           [f"40% taxpayer, interest above the £{PSA_HIGHER} allowance.",
            "Savings tax rises to 42% from April 2027.",
            "General education, not financial advice."], cy=880, size=26)


def s_loop(L, t):  # sentence 7
    loop_close(L, t, 7, comment="£50K IN BONDS: PRIZES A YEAR? COMMENT")


SCENES = [(0, 0), (1, 1), (2, 4), (5, 6), (7, 7)]
DRAW = [s_hook, s_myth, s_truth, s_catch, s_loop]


def events():
    ev = [{"t": tk(0, "56%") + 0.05, "kind": "pop"}, {"t": tk(1, "beating") + 0.4, "kind": "boom"},
          {"t": tk(2, "£1"), "kind": "coin"}, {"t": tk(3, "3.7%"), "kind": "pop"},
          {"t": tk(4, "3.75%"), "kind": "pop"}, {"t": tk(5, "free"), "kind": "coin"},
          {"t": tk(6, "2.25%"), "kind": "boom"}]
    return scene_events(ev)
