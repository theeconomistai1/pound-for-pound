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
COVER = dict(words=("FREE", "£1,000?"), highlight=1, hero="House with garden", left="Key", right="Warning",
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
QUARTER = "a quarter"  # spoken for 25%
# comment-question answer (not shown): £1,000 in -> £1,250 pot -> £937.50 back
assert (1_000 * (1 + BONUS_RATE)) * (1 - CHARGE_RATE) == 937.5

STAMP = "GOV.UK · LIFETIME ISA · CHECKED 23 OCT 2026"



def s_hook(L, t):  # sentences 0-1: the surprise
    cover_hook(L, t, "+" + gbp(BONUS), sub="...then it takes back even more", number_at=tk(0, "£1,000"),
               kicker="FROM THE GOVERNMENT",
               extra=lambda L, t: chip(L, "THE LIFETIME ISA", W / 2, 1170, t, tk(1, "Lifetime"), "white", 34,
                                       emoji="house"))


def s_deal(L, t):  # sentences 2-3: the deal, one number at a time
    beat(L, "THE DEAL", t, S(2) - 0.1)
    value_card(L, W / 2, 500, 880, t, S(2), "pound_banknote", "YOU SAVE", gbp(PAID), color=Wt,
               value_at=tk(2, "£4,000"), h=150)
    value_card(L, W / 2, 690, 880, t, tk(2, "£1,000") - 0.2, "wrapped_gift", "YOU GET FREE", "+" + gbp(BONUS),
               color=G, value_at=tk(2, "£1,000"), h=150)
    a = ramp(t, tk(3, "amazing"), 0.25)
    if a > 0:
        L.emoji("party_popper", W / 2, 940, 150, t, tk(3, "amazing"), bounce=True)
        L.text("SOUNDS AMAZING?", W / 2, 1090, 56, Wt, a, weight="Black")


def s_catch(L, t):  # sentences 4-6: the catch
    beat(L, "catch", t, S(4) - 0.1)
    a = ramp(t, tk(4, "quarter"), 0.2)
    if a > 0:
        big_number(L, "-25%", W / 2, 560, t, tk(4, "quarter"), size=200, color=RED, alpha=a)
        L.text("OF EVERYTHING YOU TAKE OUT", W / 2, 700, 34, M, a, weight="ExtraBold")
    chip(L, "THE FREE £1,000 + YOUR OWN SAVINGS", W / 2, 850, t, tk(5, "Your"), "red", 32, emoji="warning")


def s_result(L, t):  # sentence 6: the result
    beat(L, "THE RESULT", t, S(6) - 0.1)
    versus(L, t,
           dict(title="YOU SAVED", label="", value=gbp(PAID), color=Wt, start=S(6), at=tk(6, "£4,000"),
                emoji="pound_banknote"),
           dict(title="YOU GET BACK", label="", value=gbp(BACK), color=RED, start=tk(6, "£3,750") - 0.3,
                at=tk(6, "£3,750"), tone="red", emoji="chart_decreasing"),
           cy=620, h=340)
    chip(L, f"{gbp(LOSS)} LESS THAN YOU SAVED", W / 2, 900, t, tk(6, "£3,750") + 0.3, "red", 36)


def s_miss(L, t):  # sentence 7
    beat(L, "miss", t, S(7) - 0.1)
    L.emoji("house", W / 2, 560, 220, t, S(7), bounce=True)
    a = ramp(t, tk(7, "£450,000"), 0.25)
    if a > 0:
        L.text("FIRST HOME OVER", W / 2, 740, 40, M, a, weight="ExtraBold")
        big_number(L, gbp(HOME_CAP), W / 2, 850, t, tk(7, "£450,000"), size=140, alpha=a)
    chip(L, "STILL LOSES 25%", W / 2, 990, t, tk(7, "counts"), "red", 36, emoji="cross_mark")
    checked(L, STAMP, W / 2, 1090, t, tk(7, "counts") + 0.3)
    caveat(L, t, tk(7, "counts") + 0.5, ["No charge from 60 or if terminally ill. General education, not advice."],
           cy=1170, size=24)


def s_loop(L, t):  # sentence 8: loop line back into sentence 1
    loop_close(L, t, 8, comment="£1,000 OUT EARLY: YOU GET? COMMENT")


SCENES = [(0, 1), (2, 3), (4, 5), (6, 6), (7, 7), (8, 8)]
DRAW = [s_hook, s_deal, s_catch, s_result, s_miss, s_loop]


def events():
    ev = [{"t": tk(0, "£1,000") + 0.05, "kind": "coin"},
          {"t": tk(0, "takes"), "kind": "boom"},
          {"t": tk(2, "£4,000"), "kind": "pop"}, {"t": tk(2, "£1,000"), "kind": "coin"},
          {"t": tk(4, "quarter"), "kind": "boom"},
          {"t": tk(6, "£3,750"), "kind": "boom"},
          {"t": tk(7, "£450,000"), "kind": "pop"}]
    return scene_events(ev)
