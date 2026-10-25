"""Video 013 (brand-v2, format: myth, told as the dopamine loop — BRAND.md §0c): "The State Pension is enough to
live on" — half true. On your own, the full new State Pension falls over £1,300 a year short of the Pensions UK
Minimum retirement standard; a couple on two full State Pensions clears their Minimum. (figures checked 25 Oct 2026)

gov.uk/new-state-pension/what-youll-get: the full new State Pension is £241.30 a week (2026/27).
gov.uk/income-tax-rates: the standard Personal Allowance is £12,570 (so a State Pension of £12,547.60 a year with
  no other income pays no income tax: after-tax = before-tax).
Pensions UK (trading name of the Pensions and Lifetime Savings Association), Retirement Living Standards, press
  release 3 June 2026 (pensionsuk.org.uk) and retirementlivingstandards.org.uk: a Minimum retirement lifestyle costs
  £13,900 a year for a one-person household and £22,500 for two people (after tax; outside London; rent and
  mortgage payments not included; council tax and household bills included). Calculated by the Centre for
  Research in Social Policy, Loughborough University.
Assumptions: a year = 52 weeks; full new State Pension each; no other income; you own your home outright (no rent
  or mortgage); outside London.
"""
from motion import *  # noqa: F401,F403
from brand import *  # noqa: F401,F403

BRAND = True
COVER = dict(words=("PENSION", "ENOUGH?"), highlight=1, hero="Old man", left="Shopping cart",
             right="House with garden", particles="Coin")

# ---- figures (checked 25 Oct 2026) -------------------------------------------------------------------------
SP_WK = 241.30            # full new State Pension, £ a week, 2026/27 (gov.uk)
WEEKS = 52
PA = 12_570               # Personal Allowance 2026/27 (gov.uk)
MIN_ONE = 13_900          # Pensions UK Minimum, one-person household, £ a year after tax, no housing costs
MIN_TWO = 22_500          # Pensions UK Minimum, two-person household
MOD_ONE = 32_700          # Moderate, one person (description only)

SP = SP_WK * WEEKS
assert round(SP, 2) == 12_547.60
assert SP < PA                                         # no income tax on it alone: after-tax = gross
assert 12_500 <= SP < 12_600                           # "about £12,500"
GAP_ONE = MIN_ONE - SP
assert round(GAP_ONE, 2) == 1_352.40
assert 1_300 < GAP_ONE < 1_400                         # "over £1,300 a year short"
SP_TWO = 2 * SP
assert round(SP_TWO, 2) == 25_095.20
assert SP_TWO > 25_000                                 # "over £25,000"
SPARE_TWO = SP_TWO - MIN_TWO
assert round(SPARE_TWO, 2) == 2_595.20 and SPARE_TWO > 0   # "a couple clears it"
assert MIN_TWO < 2 * MIN_ONE                           # a couple needs less than double: £22,500 vs £27,800
assert 2 * MIN_ONE == 27_800
SHARE_MOD = SP / MOD_ONE                               # description: covers about 38% of Moderate
assert round(SHARE_MOD * 100) == 38

STAMP_SP = "GOV.UK · 2026/27 RATES · CHECKED 25 OCT 2026"
STAMP_RLS = "PENSIONS UK · RETIREMENT LIVING STANDARDS · CHECKED 25 OCT 2026"


def s_hook(L, t):  # sentence 0 · risk
    cover_hook(L, t, gbp(round(GAP_ONE)), sub="a year short, on your own", number_at=tk(0, "£1,300"),
               kicker="FULL STATE PENSION · 2026/27")


def s_myth(L, t):  # sentence 1 · question: the claim
    beat(L, "myth", t, S(1) - 0.1)
    a = ramp(t, S(1) + 0.1, 0.3)
    L.emoji("old_woman", W / 2, 470, 140, t, S(1), bounce=True)
    L.text("“The State Pension is", W / 2, 640, 60, Wt, a)
    L.text("enough to live on”", W / 2, 720, 60, Wt, a)
    verdict_stamp(L, "HALF TRUE", W / 2, 900, t, tk(1, "live") + 0.2, "gold", size=96)


def s_need(L, t):  # sentence 2 · twist 1a: what one person needs
    beat(L, "truth", t, S(2) - 0.1)
    L.emoji("shopping_cart", W / 2, 480, 150, t, S(2), bounce=True)
    L.text("THE BASICS, ONE PERSON", W / 2, 640, 40, M, ramp(t, tk(2, "one"), 0.25), weight="ExtraBold")
    big_number(L, gbp(MIN_ONE), W / 2, 760, t, at=tk(2, "£13,900"), size=150, color=Wt)
    L.text("A YEAR · NO RENT OR MORTGAGE", W / 2, 880, 36, Wt, ramp(t, tk(2, "basics."), 0.25))
    checked(L, "PENSIONS UK · JUNE 2026 · CHECKED 25 OCT 2026", W / 2, 970, t, tk(2, "£13,900") + 0.4)


def s_pays(L, t):  # sentences 3-4 · twist 1b + rehook
    beat(L, "truth", t, S(3) - 0.1, sub="THE GAP", sub_at=tk(3, "£12,500."))
    value_card(L, W / 2, 500, 820, t, S(3), "receipt", "BASICS, ONE PERSON", gbp(MIN_ONE), color=Wt,
               value_at=S(3) + 0.1, sub="Pensions UK Minimum, a year")
    value_card(L, W / 2, 680, 820, t, tk(3, "State"), "bank", "FULL STATE PENSION", gbp(round(SP)), color=G,
               value_at=tk(3, "£12,500."), sub="full rate, 52 weeks")
    chip(L, "SHORT " + gbp(round(GAP_ONE)) + " A YEAR", W / 2, 850, t, tk(3, "£12,500.") + 0.35, "red", 44,
         emoji="warning")
    checked(L, STAMP_SP, W / 2, 950, t, tk(3, "£12,500.") + 0.6)
    a = ramp(t, S(4), 0.25)
    if a > 0:
        L.emoji("thinking_face", W / 2, 1080, 110, t, S(4), bounce=True)


def s_couple_need(L, t):  # sentence 5 · question 2: a couple
    beat(L, "catch", t, S(5) - 0.1, sub="WHEN IT IS TRUE", sub_at=S(5) + 0.2)
    L.emoji("old_man", W / 2 - 85, 500, 150, t, tk(5, "couple"), bounce=True)
    L.emoji("old_woman", W / 2 + 85, 500, 150, t, tk(5, "couple") + 0.15, bounce=True)
    L.text("THE BASICS, A COUPLE", W / 2, 660, 40, M, ramp(t, tk(5, "needs"), 0.25), weight="ExtraBold")
    big_number(L, gbp(MIN_TWO), W / 2, 780, t, at=tk(5, "£22,500"), size=150, color=Wt)
    chip(L, "NOT DOUBLE " + gbp(2 * MIN_ONE), W / 2, 910, t, tk(5, "same."), "gold", 36)


def s_couple_pays(L, t):  # sentences 6-7 · twist 2 + answer
    beat(L, "catch", t, S(6) - 0.1, sub="TWO FULL STATE PENSIONS", sub_at=S(6) + 0.2)
    versus(L, t,
           dict(title="ALONE", label=gbp(round(SP)) + " VS " + gbp(MIN_ONE), value="-" + gbp(round(GAP_ONE)),
                color=RED, start=tk(7, "Alone,"), at=tk(7, "don't."), tone="red", emoji="old_man"),
           dict(title="COUPLE", label=gbp(round(SP_TWO)) + " VS " + gbp(MIN_TWO), value="+" + gbp(round(SPARE_TWO)),
                color=G, start=S(6), at=tk(6, "£25,000."), tone="green", emoji="old_woman"),
           cy=600, h=320)
    L.text("A YEAR, AFTER THE BASICS", W / 2, 800, 34, M, ramp(t, tk(7, "clears"), 0.25), weight="ExtraBold")
    caveat(L, t, tk(7, "don't.") - 0.2,
           ["Pensions UK Minimum: after tax, outside London, no rent or mortgage.",
            "Full new State Pension each, no other income. Not financial advice."], cy=900, size=24)


def s_loop(L, t):  # sentence 8: loop line back into sentence 0
    loop_close(L, t, 8, comment="FAIR OR NOT? COMMENT")


SCENES = [(0, 0), (1, 1), (2, 2), (3, 4), (5, 5), (6, 7), (8, 8)]
DRAW = [s_hook, s_myth, s_need, s_pays, s_couple_need, s_couple_pays, s_loop]


def events():
    ev = [{"t": tk(0, "£1,300") + 0.05, "kind": "boom"},
          {"t": tk(1, "live") + 0.2, "kind": "boom"},
          {"t": tk(2, "£13,900"), "kind": "pop"},
          {"t": tk(3, "£12,500."), "kind": "pop"},
          {"t": tk(3, "£12,500.") + 0.35, "kind": "boom"},
          {"t": tk(5, "£22,500"), "kind": "pop"},
          {"t": tk(6, "£25,000."), "kind": "coin"},
          {"t": tk(7, "don't."), "kind": "boom"}]
    return scene_events(ev)
