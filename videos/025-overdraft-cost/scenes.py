"""025: £500 left in an arranged overdraft for a year costs about £100 at the average rate — about the same as a
credit card; and since April 2020 going past your limit can't cost more than your arranged rate — format: calc
(brand-v2; BRAND.md §1, told as the dopamine loop §0c). (figures checked 31 Oct 2026)

bankofengland.co.uk/statistics/money-and-credit/2026/september-2026 (published 29 October 2026):
  "The effective interest rate on interest-charging overdrafts increased by 52 basis points, to 20.79% in September."
  "The effective rate on interest-charging credit cards increased slightly in September, to 21.71% from 21.55%."
  "The effective rate on new personal loans to individuals decreased to 9.85% in September from 9.96% in August."
fca.org.uk/news/press-releases/millions-customers-together-save-nearly-1billion-due-overdraft-rule-changes (2023):
  pricing rules in force from April 2020: firms "stop charging fixed fees for overdraft borrowing" and "charge no
  more for an unarranged overdraft than an arranged one"; before, "unarranged borrowing was priced by a £2.50 daily
  fee" (one example) and "some banks were charging more than 80% APR" on arranged overdrafts.
fca.org.uk/data/changes-overdraft-charges: from April 2020 banks "can only charge ... a simple annual interest
  rate ... without additional fees and charges".
Assumptions: a steady £500 balance for 12 months (31 Oct 2026 to 31 Oct 2027) at the September 2026 average
  effective rate on interest-charging overdrafts; no interest-free buffer. Your own bank's rate will differ.
"""
from motion import *  # noqa: F401,F403
from brand import *  # noqa: F401,F403

BRAND = True
COVER = dict(words=("OVERDRAFT", "£100?"), highlight=1, hero="Credit card", left="Jack-o-lantern",
             right="Calendar", particles="Coin")

# ---- figures (Bank of England Money and Credit, September 2026; FCA; checked 31 Oct 2026) ----------------
OD_RATE = 20.79        # % effective rate, interest-charging overdrafts, Sept 2026
CARD_RATE = 21.71      # % effective rate, interest-charging credit cards, Sept 2026
LOAN_RATE = 9.85       # % effective rate, new personal loans, Sept 2026 (description only)
BALANCE = 500          # illustrative overdrawn balance, held for a year
COST = round(BALANCE * OD_RATE / 100, 2)
assert COST == 103.95                         # exact, in the description
assert round(COST, -2) == 100                 # spoken: "about £100"
assert 20 < OD_RATE < 22 and 20 < CARD_RATE < 22.5   # spoken: "both average just over a fifth a year"
assert abs(CARD_RATE - OD_RATE) < 1           # spoken: "about the same as a credit card"
CARD_COST = round(BALANCE * CARD_RATE / 100, 2)
assert CARD_COST == 108.55
FCA_YEAR = 2020                               # spoken: "Since April 2020"

STAMP_BOE = "BANK OF ENGLAND · SEPT 2026 · CHECKED 31 OCT 2026"
STAMP_FCA = "FCA RULES · SINCE APRIL 2020 · CHECKED 31 OCT 2026"


def pct(v):
    return f"{v:.1f}%"


def s_hook(L, t):  # sentence 0 · risk
    cover_hook(L, t, gbp(round(COST, -2)), sub="interest on £500 overdrawn for a year", number_at=tk(0, "£100."),
               kicker="AT THE AVERAGE OVERDRAFT RATE")


def s_question(L, t):  # sentence 1 · question: it's cheaper than a card, surely?
    beat(L, "maths", t, S(1) - 0.1)
    value_card(L, W / 2, 540, 780, t, S(1), "bank", "YOUR OVERDRAFT", gbp(BALANCE), color=Wt,
               value_at=S(1) + 0.2, sub="the bank's safety cushion?")
    L.emoji("thinking_face", W / 2, 820, 140, t, tk(1, "cheaper"), bounce=True)
    chip(L, "CHEAPER THAN A CARD?", W / 2, 990, t, tk(1, "credit"), "white", 40, emoji="credit_card")


def s_twist(L, t):  # sentences 2-3 · twist 1: about the same as a credit card
    beat(L, "twist", t, S(2) - 0.1, sub="AVERAGE RATE · SEPT 2026", sub_at=S(2))
    versus(L, t,
           dict(title="OVERDRAFT", label="AVERAGE RATE", value=pct(OD_RATE), color=RED, start=S(2),
                at=tk(2, "overdraft"), tone="red", emoji="bank"),
           dict(title="CREDIT CARD", label="AVERAGE RATE", value=pct(CARD_RATE), color=RED, start=S(2) + 0.15,
                at=tk(2, "card."), tone="red", emoji="credit_card"),
           cy=620, h=300)
    checked(L, STAMP_BOE, W / 2, 900, t, tk(2, "card.") + 0.2)


def s_fifth(L, t):  # sentence 3 · answer: both just over a fifth a year
    beat(L, "maths", t, S(3) - 0.1)
    a = panel(L, W / 2, 640, 800, 340, t, S(3), "red")
    big_number(L, "A FIFTH", W / 2, 600, t, at=tk(3, "a fifth"), size=170, color=RED, alpha=a)
    chip(L, "A YEAR · OVERDRAFTS AND CARDS", W / 2, 740, t, tk(3, "year."), "white", 34, emoji="calendar")
    caveat(L, t, tk(3, "year.") + 0.1, ["Average effective rates, September 2026: 20.79% and 21.71%."],
           cy=900, size=28)


def s_catch(L, t):  # sentences 4-5 · rehook + question 2: going past your limit
    beat(L, "catch", t, S(4) - 0.1)
    L.emoji("face_screaming_in_fear", W / 2, 560, 170, t, S(4), bounce=True)
    chip(L, "PAST YOUR LIMIT", W / 2, 790, t, tk(5, "past"), "red", 46, emoji="cross_mark")
    chip(L, "BEFORE 2020: DAILY FEES", W / 2, 910, t, tk(5, "far"), "white", 38, emoji="alarm_clock")


def s_rule(L, t):  # sentence 6 · twist 2: no more than your arranged rate
    beat(L, "twist", t, S(6) - 0.1, sub="SINCE APRIL 2020", sub_at=S(6))
    versus(L, t,
           dict(title="ARRANGED", label="CHARGED AT", value="YOUR RATE", color=Wt, start=S(6),
                at=S(6) + 0.2, tone=None, emoji="check_mark_button"),
           dict(title="PAST THE LIMIT", label="CHARGED AT", value="NO MORE", color=G, start=S(6) + 0.15,
                at=tk(6, "arranged"), tone="green", emoji="shield"),
           cy=620, h=300)
    checked(L, STAMP_FCA, W / 2, 900, t, tk(6, "rate.") + 0.1)


def s_miss(L, t):  # sentence 7 · answer: no daily fees, one interest rate
    beat(L, "miss", t, S(7) - 0.1)
    chip(L, "NO DAILY FEES", W / 2, 520, t, S(7), "green", 52, emoji="cross_mark")
    chip(L, "JUST ONE INTEREST RATE", W / 2, 680, t, tk(7, "one"), "white", 46, emoji="receipt")
    caveat(L, t, tk(7, "rate.") + 0.1, ["Average rates: Bank of England, September 2026.",
                                         "Your bank's rate will differ. Not advice."], cy=860, size=28)


def s_loop(L, t):  # sentence 8: loop line back into sentence 0
    loop_close(L, t, 8, comment="SAFETY NET OR TRAP? COMMENT")


SCENES = [(0, 0), (1, 1), (2, 2), (3, 3), (4, 5), (6, 6), (7, 7), (8, 8)]
DRAW = [s_hook, s_question, s_twist, s_fifth, s_catch, s_rule, s_miss, s_loop]


def events():
    ev = [{"t": tk(0, "£100.") + 0.05, "kind": "boom"},
          {"t": tk(1, "cheaper"), "kind": "pop"},
          {"t": tk(2, "card."), "kind": "boom"},
          {"t": tk(3, "a fifth"), "kind": "pop"},
          {"t": tk(5, "far"), "kind": "boom"},
          {"t": tk(6, "arranged"), "kind": "coin"},
          {"t": tk(7, "one"), "kind": "pop"}]
    return scene_events(ev)
