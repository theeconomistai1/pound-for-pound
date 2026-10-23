"""Video 010 (brand-v2, format: calc): the Lifetime ISA bonus vs the 25% withdrawal charge — £4,000 paid in,
£1,000 bonus, £5,000 pot, an early (unauthorised) withdrawal of the whole pot returns £3,750.
(figures checked 23 Oct 2026)

gov.uk/lifetime-isa/summary: up to £4,000 a year until 50; the government adds a 25% bonus, up to £1,000 a
  year; counts toward the £20,000 ISA allowance (2026 to 2027).
gov.uk/lifetime-isa/withdrawing-money-from-your-lifetime-isa: 25% charge for any withdrawal other than a first
  home costing £450,000 or less (12+ months after the first payment, through a conveyancer, with a mortgage),
  age 60 or over, or terminal illness. gov.uk's own example: £800 saved + £200 bonus = £1,000; withdrawing it
  all costs £250, leaving £750 — the same 25%-of-the-whole-pot maths used here.
gov.uk/guidance/lifetime-isa-withdrawal-charges-and-charge-free-withdrawals (HMRC, for providers): the 25%
  charge applies to the amount withdrawn.
HM Treasury First Time Buyer ISA consultation (June 2026): the LISA is to be replaced by a new First Time
  Buyer ISA (no launch date); until then LISA holders keep saving under the existing rules; no change proposed
  to the LISA withdrawal charge.
Assumption: no interest or investment growth, the whole pot withdrawn, bonus already paid in.
"""
from motion import *  # noqa: F401,F403
from brand import *  # noqa: F401,F403

BRAND = True
COVER = dict(words=("LISA", "PENALTY"), highlight=1, hero="House with garden", left="Key", right="Warning",
             particles="Coin")

# ---- figures (gov.uk, checked 23 Oct 2026) -----------------------------------------------------------------
BONUS_RATE = 0.25          # government bonus on what you pay in
CHARGE_RATE = 0.25         # withdrawal charge on the amount withdrawn
LIMIT = 4_000              # most you can pay in each tax year
BONUS_CAP = 1_000          # most bonus a year
HOME_CAP = 450_000         # first-home price limit
FREE_AGE = 60              # charge-free withdrawals from 60

PAID = LIMIT
BONUS = round(PAID * BONUS_RATE)
assert BONUS == BONUS_CAP == 1_000
POT = PAID + BONUS
assert POT == 5_000
CHARGE = round(POT * CHARGE_RATE)
assert CHARGE == 1_250
BACK = POT - CHARGE
assert BACK == 3_750
LOSS = PAID - BACK
assert LOSS == 250
LOSS_PCT = LOSS / PAID * 100
assert f"{LOSS_PCT:.2f}%" == "6.25%"
assert CHARGE == BONUS + LOSS                       # takes back the bonus, plus £250 of your own money
assert (HOME_CAP, FREE_AGE) == (450_000, 60)
# gov.uk's own worked example uses the same maths: £800 + £200 bonus, charge £250, back £750
assert (800 + 800 * BONUS_RATE) * (1 - CHARGE_RATE) == 750
# comment-question answer (not shown): £1,000 in -> £1,250 pot -> £937.50 back
assert (1_000 * (1 + BONUS_RATE)) * (1 - CHARGE_RATE) == 937.5

STAMP = "GOV.UK · LIFETIME ISA · CHECKED 23 OCT 2026"


def s_hook(L, t):  # sentences 0-1
    cover_hook(L, t, gbp(BACK), sub=f"from {gbp(PAID)} paid in", number_at=tk(0, "£3,750"),
               kicker="LIFETIME ISA, TAKEN OUT EARLY",
               extra=lambda L, t: chip(L, f"{gbp(LOSS)} LESS THAN YOU PAID IN", W / 2, 1170, t, tk(1, "£250"),
                                       "red", 32, emoji="chart_decreasing"))


def s_maths(L, t):  # sentences 2-3
    beat(L, "maths", t, S(2) - 0.1)
    value_card(L, W / 2, 470, 880, t, S(2), "pound_banknote", "YOU PAY IN", gbp(PAID), color=Wt,
               value_at=S(2) + 0.2, h=140, sub="the most a year")
    value_card(L, W / 2, 640, 880, t, tk(2, "25%"), "wrapped_gift", "25% GOVERNMENT BONUS", "+" + gbp(BONUS),
               color=C, value_at=tk(2, "£1,000"), h=140, sub="up to £1,000 a year")
    a = panel(L, W / 2, 900, 760, 230, t, tk(3, "pot") - 0.15, "green")
    L.text("IN YOUR POT", W / 2, 830, 30, M, a, weight="ExtraBold")
    if a > 0:
        big_number(L, gbp(POT), W / 2, 925, t, tk(3, "£5,000"), size=130, alpha=a)
    checked(L, STAMP, W / 2, 1100, t, tk(3, "£5,000") + 0.4)


def s_twist(L, t):  # sentences 4-5
    beat(L, "twist", t, S(4) - 0.1, sub="25% OF THE WHOLE POT", sub_at=tk(4, "whole"))
    timed_line(L, [("25%", RED, tk(4, "25%")), ("OF", M, tk(4, "charge")), (gbp(POT), G, tk(4, "whole")),
                   ("=", M, tk(4, "£1,250")), ("-" + gbp(CHARGE), RED, tk(4, "£1,250"))], W / 2, 440, 66, t)
    bar_chart(L, t, S(4) + 0.2, [PAID, POT, BACK], ["YOU PAID", "POT", "YOU GET"], (200, 560, 880, 900),
              [Wt, G, RED], dur=0.6, stagger=0.15,
              value_tags={0: (gbp(PAID), Wt, S(4) + 0.4), 1: (gbp(POT), G, S(4) + 0.6),
                          2: (gbp(BACK), RED, tk(4, "£1,250") + 0.2)})
    chip(L, f"BONUS {gbp(BONUS)} + {gbp(LOSS)} OF YOUR OWN", W / 2, 1020, t, tk(5, "bonus"), "red", 30,
         emoji="warning")
    a = ramp(t, tk(5, "6.25%"), 0.25)
    L.text(f"{gbp(LOSS)} = {LOSS_PCT:.2f}% OF {gbp(PAID)}", W / 2, 1120, 40, G, a, weight="Black")
    checked(L, STAMP, W / 2, 1200, t, tk(5, "6.25%") + 0.4)


def s_miss(L, t):  # sentences 6-7
    beat(L, "miss", t, S(6) - 0.1)
    value_card(L, W / 2, 470, 880, t, S(6), "house", "NO CHARGE: FIRST HOME UP TO", gbp(HOME_CAP), color=G,
               value_at=tk(6, "£450,000"), h=140)
    value_card(L, W / 2, 640, 880, t, tk(6, "£450,000") + 0.3, "old_woman", "NO CHARGE: FROM AGE", str(FREE_AGE),
               color=G, value_at=tk(6, "60"), h=140)
    chip(L, f"FIRST HOME OVER {gbp(HOME_CAP)}? 25% CHARGE", W / 2, 820, t, tk(7, "price"), "red", 30,
         emoji="cross_mark")
    checked(L, STAMP, W / 2, 930, t, tk(7, "charge"))
    caveat(L, t, tk(7, "charge") + 0.3, ["Also charge-free if terminally ill. Assumes no growth.",
                                         "General education, not financial advice."], cy=1050, size=26)


def s_loop(L, t):  # sentence 8: the loop line, the picture rebuilds the cover
    loop_close(L, t, 8, comment="£1,000 IN, ALL OUT EARLY: YOU GET? COMMENT")


SCENES = [(0, 1), (2, 3), (4, 5), (6, 7), (8, 8)]
DRAW = [s_hook, s_maths, s_twist, s_miss, s_loop]


def events():
    ev = [{"t": tk(0, "£3,750") + 0.05, "kind": "pop"},
          {"t": tk(1, "£250"), "kind": "boom"},
          {"t": tk(2, "£1,000"), "kind": "coin"}, {"t": tk(3, "£5,000"), "kind": "coin"},
          {"t": tk(4, "£1,250"), "kind": "boom"}, {"t": tk(5, "6.25%"), "kind": "pop"},
          {"t": tk(6, "£450,000"), "kind": "pop"}, {"t": tk(6, "60"), "kind": "pop"},
          {"t": tk(7, "price"), "kind": "boom"}]
    return scene_events(ev)
