"""Video 024 (brand-v2, format: myth, told as the dopamine loop — BRAND.md §0c): "Overpaying your mortgage always
wins." (figures checked 30 Oct 2026)

Bank of England, Money and Credit - September 2026 (published 29 Oct 2026),
  https://www.bankofengland.co.uk/statistics/money-and-credit/2026/september-2026 and
  https://www.bankofengland.co.uk/statistics/effective-interest-rates/2026/september-2026 :
  "The rate on the outstanding stock of mortgages was 4.03% in September" (effective rate, individuals,
  secured loans, outstanding) · effective rate on "new time deposits with banks and building societies increased
  to 4.42% in September" · newly drawn mortgages 4.63%.
gov.uk Budget 2026 OOTLAR Annex A (rates and allowances), https://www.gov.uk/government/publications/
  budget-2026-overview-of-tax-legislation-and-rates-ootlar/annex-a-rates-and-allowances : savings basic rate 20%
  in 2026 to 2027, 24% in 2027 to 2028; higher 40% -> 44%; additional 45% -> 49%; Personal Savings Allowance
  £1,000 (basic rate) / £500 (higher rate), unchanged. Also gov.uk "Income Tax — changes to tax rates for property
  and savings income" (published 29 Oct 2026): 24% savings basic rate from the 2027 to 2028 tax year.
MoneyHelper, "Should you pay off your mortgage early?": lenders often allow overpayments of up to 10% a year
  without a charge; normal overpayments can't be drawn back (flexible / offset mortgages can).
Assumptions: £10,000 lump sum (illustrative); the mortgage costs the average outstanding rate (4.03%) and the
  savings deal pays the average new fixed-term deposit rate (4.42%); interest saved by overpaying in year one is
  approximated as 4.03% of £10,000 (about £403); the saver is a basic-rate taxpayer who has already used the £1,000
  Personal Savings Allowance, with no starting-rate band; no early repayment charge; interest outside an ISA.
"""
from motion import *  # noqa: F401,F403
from brand import *  # noqa: F401,F403

BRAND = True
COVER = dict(words=("OVERPAY", "MYTH?"), highlight=1, hero="House with garden", left="Key", right="Classical building",
             particles="Coin")

# ---- figures (Bank of England / gov.uk, checked 30 Oct 2026) --------------------------------------------
LUMP = 10_000                    # illustrative lump sum
MORT_RATE = 0.0403               # BoE: effective rate, outstanding mortgages, Sep 2026
SAVE_RATE = 0.0442               # BoE: effective rate, new time deposits, Sep 2026
TAX_NOW, TAX_2027 = 0.20, 0.24   # savings basic rate 2026/27 -> 2027/28 (Budget 2026)
PSA_BASIC = 1_000

OVERPAY_SAVES = round(LUMP * MORT_RATE)                   # 403
assert OVERPAY_SAVES == 403 and round(OVERPAY_SAVES, -2) == 400      # spoken: "about £400 a year"
INTEREST = round(LUMP * SAVE_RATE)                        # 442
assert INTEREST == 442                                    # spoken: "£442"
NET_2027 = round(LUMP * SAVE_RATE * (1 - TAX_2027))       # 335.92 -> 336
assert NET_2027 == 336                                    # spoken: "keeps just £336"
NET_NOW = round(LUMP * SAVE_RATE * (1 - TAX_NOW), 2)      # 353.60 (description only)
assert NET_NOW == 353.6
NET_HIGHER_2027 = round(LUMP * SAVE_RATE * (1 - 0.44), 2)  # 247.52 (description only)
assert NET_HIGHER_2027 == 247.52
assert INTEREST > OVERPAY_SAVES > NET_2027                # twist 1: saving wins gross; twist 2: overpaying wins

STAMP_BOE = "BANK OF ENGLAND · SEPT 2026 · CHECKED 30 OCT 2026"
STAMP_GOV = "GOV.UK · BUDGET 2026 · CHECKED 30 OCT 2026"


def s_hook(L, t):  # sentence 0 · risk
    cover_hook(L, t, gbp(LUMP), sub="spare cash: mortgage or savings?", number_at=tk(0, "£10,000"),
               kicker="MORTGAGE OVERPAYMENTS · UK")


def s_myth(L, t):  # sentence 1 · question: the claim
    beat(L, "myth", t, S(1) - 0.1)
    a = ramp(t, S(1) + 0.1, 0.3)
    L.emoji("house", W / 2, 500, 150, t, S(1), bounce=True)
    L.text("“Overpaying always", W / 2, 670, 62, Wt, a)
    L.text("wins”", W / 2, 752, 62, Wt, a)
    verdict_stamp(L, "MYTH?", W / 2, 930, t, tk(1, "wins.") + 0.15, "red", size=120)


def s_overpay(L, t):  # sentence 2 · answer: overpaying saves about £400 a year
    beat(L, "truth", t, S(2) - 0.1, sub="OVERPAY £10,000", sub_at=S(2) + 0.2)
    L.emoji("house", W / 2, 520, 160, t, S(2), bounce=True)
    L.text("INTEREST SAVED A YEAR", W / 2, 680, 40, M, ramp(t, S(2) + 0.3, 0.3), weight="ExtraBold")
    big_number(L, "ABOUT £400", W / 2, 810, t, at=tk(2, "£400"), size=150, color=Wt)


def s_versus(L, t):  # sentence 3 · twist 1: savings pays more than the mortgage costs
    beat(L, "truth", t, S(3) - 0.1, sub="£10,000 FOR ONE YEAR", sub_at=S(3) + 0.2)
    versus(L, t,
           dict(title="OVERPAY", label="INTEREST SAVED", value="£400", color=Wt, start=S(3),
                at=S(3) + 0.1, tone=None, emoji="house"),
           dict(title="SAVE IT", label="INTEREST EARNED", value=gbp(INTEREST), color=G,
                start=tk(3, "average"), at=tk(3, "£442"), tone="green", emoji="bank"),
           cy=600, h=300)
    chip(L, "MORTGAGE 4.03% · NEW FIXED SAVINGS 4.42%", W / 2, 820, t, tk(3, "£442") + 0.3, "white", 30)
    checked(L, STAMP_BOE, W / 2, 900, t, tk(3, "£442") + 0.5)


def s_catch(L, t):  # sentences 4-5 · rehook + question 2: the tax
    beat(L, "catch", t, S(4) - 0.1, sub="THE PART PEOPLE MISS", sub_at=S(4) + 0.2)
    L.emoji("receipt", W / 2, 540, 170, t, S(4), bounce=True)
    chip(L, "TAX-FREE SAVINGS ALLOWANCE USED?", W / 2, 760, t, tk(5, "allowance?"), "white", 38,
         emoji="thinking_face")
    chip(L, "INTEREST GETS TAXED", W / 2, 870, t, tk(5, "taxed."), "red", 44, emoji="warning")


def s_net(L, t):  # sentence 6 · twist 2: £442 becomes £336
    beat(L, "twist", t, S(6) - 0.1, sub="FROM APRIL 2027, BASIC RATE", sub_at=S(6) + 0.2)
    timed_line(L, [(gbp(INTEREST), Wt, S(6) + 0.2), ("minus 24% tax", RED, tk(6, "basic-rate"))], W / 2, 500, 56, t)
    big_number(L, gbp(NET_2027), W / 2, 680, t, at=tk(6, "£336"), size=200, color=G)
    L.text("NOW LESS THAN THE £400 YOU SAVE", W / 2, 850, 36, M, ramp(t, tk(6, "£336") + 0.3, 0.3),
           weight="ExtraBold")
    checked(L, STAMP_GOV, W / 2, 950, t, tk(6, "£336") + 0.5)


def s_locked(L, t):  # sentence 7 · answer: overpaying wins, but the money is locked away
    beat(L, "miss", t, S(7) - 0.1)
    verdict_stamp(L, "HALF TRUE", W / 2, 520, t, S(7) + 0.2, "gold", size=90)
    L.emoji("locked", W / 2, 720, 150, t, tk(7, "locked"), bounce=True)
    chip(L, "USUALLY CAN'T TAKE IT BACK", W / 2, 870, t, tk(7, "locked"), "red", 40)
    caveat(L, t, tk(7, "away.") , ["Averages; your rates differ. Most lenders allow 10% a",
                                   "year penalty-free. Not advice."], cy=960, size=26)


def s_loop(L, t):  # sentence 8: loop line back into sentence 0
    loop_close(L, t, 8, comment="OVERPAY OR SAVE? COMMENT")


SCENES = [(0, 0), (1, 1), (2, 2), (3, 3), (4, 5), (6, 6), (7, 7), (8, 8)]
DRAW = [s_hook, s_myth, s_overpay, s_versus, s_catch, s_net, s_locked, s_loop]


def events():
    ev = [{"t": tk(0, "£10,000") + 0.05, "kind": "pop"},
          {"t": tk(1, "wins.") + 0.15, "kind": "boom"},
          {"t": tk(2, "£400"), "kind": "pop"},
          {"t": tk(3, "£442"), "kind": "coin"},
          {"t": tk(5, "taxed."), "kind": "boom"},
          {"t": tk(6, "£336"), "kind": "boom"},
          {"t": S(7) + 0.2, "kind": "pop"}]
    return scene_events(ev)
