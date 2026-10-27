"""Video 017 (brand-v2, format: myth, told as the dopamine loop — BRAND.md §0c): "Minimum payments are fine".
Pay only the minimum on a £2,000 credit card balance at the typical UK rate and a year later you still owe over
£1,750, having paid almost £600, most of it interest. It keeps the card up to date, but keep it up for 18 months
and the FCA calls it persistent debt: the card company must step in. (figures checked 27 Oct 2026)

Bank of England, Money and Credit - August 2026 (published 29 Sep 2026):
  bankofengland.co.uk/statistics/money-and-credit/2026/august-2026 — "The effective rate on interest-charging
  credit cards increased in August, to 21.55% from 21.45%." Used as the typical APR.
Minimum payment: a common UK formula is interest + 1% of the balance (with a floor), e.g. Nationwide
  (nationwide.co.uk/credit-cards/help/minimum-payments): "any overdue charges and interest owed, plus 1% of the
  remaining statement balance (or £25, whichever is greater)". Lenders' formulas vary.
FCA persistent debt (fca.org.uk/publication/documents/help-for-consumers-who-are-in-persistent-credit-card-debt.pdf
  and customer-persistent-debt-infographic.pdf; rules in force since 1 Mar 2018, FCA press release): persistent
  debt = paid more in interest, fees and charges than repaid of the borrowing over 18 months; the provider must
  contact you and offer help; reminder at 27 months; at 36 months options to repay faster, or forbearance.
Assumptions: £2,000 balance, no new spending, no fees; APR 21.55% turned into a monthly rate
  (1.2155^(1/12) - 1 = 1.64%); each month the minimum = that month's interest + 1% of the balance (£25 floor,
  which never bites in the first 18 months); payments always on time.
"""
from motion import *  # noqa: F401,F403
from brand import *  # noqa: F401,F403

BRAND = True
COVER = dict(words=("MINIMUM", "TRAP?"), highlight=1, hero="Credit card", left="Warning",
             right="Hourglass not done", particles="Coin")

# ---- figures (checked 27 Oct 2026) -------------------------------------------------------------------------
BAL0 = 2_000              # starting balance, £
APR = 0.2155              # BoE effective rate on interest-charging credit cards, August 2026
CAP_PCT = 0.01            # minimum = interest + 1% of the balance
FLOOR = 25                # minimum floor, £ (Nationwide example)
PD_MONTHS = 18            # FCA persistent-debt window

R = (1 + APR) ** (1 / 12) - 1
assert round(R * 100, 2) == 1.64


def run(months):
    bal, interest, capital, mins = BAL0, 0.0, 0.0, []
    for _ in range(months):
        i = bal * R
        pay = max(i + CAP_PCT * bal, FLOOR)
        mins.append(pay)
        interest += i
        capital += pay - i
        bal -= pay - i
    return bal, interest, capital, mins


BAL12, INT12, CAP12, MINS12 = run(12)
assert round(BAL12, 2) == 1_772.77 and BAL12 > 1_750           # "still owe over £1,750"
PAID12 = INT12 + CAP12
assert round(PAID12, 2) == 599.80 and 590 < PAID12 < 600        # "almost £600"
assert round(INT12, 2) == 372.56 and round(CAP12, 2) == 227.23
assert INT12 > PAID12 / 2                                       # "most of it was interest"
assert round(MINS12[0], 2) == 52.79                             # first minimum (description)
BAL18, INT18, CAP18, MINS18 = run(PD_MONTHS)
assert min(MINS18) > FLOOR                                      # the floor never bites in 18 months
assert INT18 > CAP18                                            # persistent debt: more interest than capital
assert round(INT18, 2) == 542.66 and round(CAP18, 2) == 330.97


def payoff():
    bal, interest, m = BAL0, 0.0, 0
    while bal > 0.005:
        i = bal * R
        pay = min(max(i + CAP_PCT * bal, FLOOR), bal + i)
        interest += i
        bal = bal + i - pay
        m += 1
    return m, interest


PAYOFF_M, PAYOFF_INT = payoff()
assert PAYOFF_M == 135 and round(PAYOFF_INT, 2) == 2_271.23     # description: over 11 years, ~£2,271 interest

STAMP_BOE = "BANK OF ENGLAND · AUG 2026 RATE · CHECKED 27 OCT 2026"
STAMP_FCA = "FCA · PERSISTENT DEBT RULES · CHECKED 27 OCT 2026"


def s_hook(L, t):  # sentence 0 · risk
    cover_hook(L, t, "£1,750+", sub="still owed, a year later", number_at=tk(0, "£1,750."),
               kicker="£2,000 ON A CREDIT CARD · MINIMUM ONLY")


def s_myth(L, t):  # sentence 1 · question: the claim
    beat(L, "myth", t, S(1) - 0.1)
    a = ramp(t, S(1) + 0.1, 0.3)
    L.emoji("credit_card", W / 2, 480, 150, t, S(1), bounce=True)
    L.text("“Minimum payments", W / 2, 650, 62, Wt, a)
    L.text("are fine”", W / 2, 730, 62, Wt, a)
    verdict_stamp(L, "MYTH", W / 2, 910, t, tk(1, "fine.") + 0.15, "red", size=120)


def s_paid(L, t):  # sentences 2-3 · context + twist 1
    beat(L, "truth", t, S(2) - 0.1, sub="YEAR ONE", sub_at=S(2) + 0.2)
    L.emoji("receipt", W / 2, 470, 120, t, S(2), bounce=True)
    L.text("YOU PAY IN 12 MONTHS", W / 2, 590, 40, M, ramp(t, S(2) + 0.1, 0.25), weight="ExtraBold")
    big_number(L, gbp(round(PAID12)), W / 2, 700, t, at=tk(2, "£600."), size=150, color=Wt)
    value_card(L, W / 2 - 215, 900, 400, t, tk(3, "interest,"), "fire", "INTEREST", gbp(round(INT12)),
               color=RED, value_at=tk(3, "interest,"), h=150)
    value_card(L, W / 2 + 215, 900, 400, t, tk(3, "debt."), "chart_decreasing", "OFF YOUR DEBT",
               gbp(round(CAP12)), color=G, value_at=tk(3, "debt."), h=150)
    checked(L, STAMP_BOE, W / 2, 1040, t, tk(3, "debt.") + 0.4)
    caveat(L, t, tk(3, "interest,") + 0.3, ["Typical rate 21.55% APR · minimum = interest + 1%"], cy=1110, size=26)


def s_strange(L, t):  # sentences 4-5 · rehook + question 2: when it IS true
    beat(L, "catch", t, S(4) - 0.1, sub="WHEN IT IS TRUE", sub_at=S(5))
    L.emoji("thinking_face", W / 2, 520, 150, t, S(4), bounce=True)
    chip(L, "NO MISSED PAYMENT", W / 2, 720, t, tk(5, "up"), "green", 48, emoji="check_mark_button")
    chip(L, "NO LATE FEE", W / 2, 820, t, tk(5, "date.") , "green", 48, emoji="shield")


def s_persistent(L, t):  # sentences 6-7 · twist 2 + answer
    beat(L, "catch", t, S(6) - 0.1, sub="THE REGULATOR'S VIEW", sub_at=S(6) + 0.2)
    L.emoji("calendar", W / 2, 470, 120, t, S(6), bounce=True)
    big_number(L, "18 MONTHS", W / 2, 620, t, at=tk(6, "18"), size=130, color=Wt)
    L.text("MORE INTEREST THAN DEBT REPAID", W / 2, 720, 38, M, ramp(t, tk(6, "regulator"), 0.25),
           weight="ExtraBold")
    chip(L, "PERSISTENT DEBT", W / 2, 810, t, tk(6, "persistent"), "red", 54, emoji="warning")
    chip(L, "YOUR CARD COMPANY MUST STEP IN", W / 2, 920, t, tk(7, "step"), "gold", 38, emoji="bell")
    checked(L, STAMP_FCA, W / 2, 1020, t, tk(7, "step") + 0.4)


def s_loop(L, t):  # sentence 8: loop line back into sentence 0
    loop_close(L, t, 8, comment="FINE OR NOT? COMMENT")


SCENES = [(0, 0), (1, 1), (2, 3), (4, 5), (6, 7), (8, 8)]
DRAW = [s_hook, s_myth, s_paid, s_strange, s_persistent, s_loop]


def events():
    ev = [{"t": tk(0, "£1,750.") + 0.05, "kind": "boom"},
          {"t": tk(1, "fine.") + 0.15, "kind": "boom"},
          {"t": tk(2, "£600."), "kind": "pop"},
          {"t": tk(3, "interest,"), "kind": "boom"},
          {"t": tk(5, "up"), "kind": "coin"},
          {"t": tk(6, "18"), "kind": "pop"},
          {"t": tk(6, "persistent"), "kind": "boom"}]
    return scene_events(ev)
