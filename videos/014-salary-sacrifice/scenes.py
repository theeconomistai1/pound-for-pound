"""Video 014 (brand-v2, format: calc, told as the dopamine loop — BRAND.md §0c): salary sacrifice vs paying
into a pension the usual way. £1,000 into your pension costs a basic-rate employee £800 of take-home pay the
usual way (income tax relief only), but £720 by salary sacrifice (no income tax AND no National Insurance).
From April 2029 the National Insurance part is capped at £2,000 a year. (figures checked 25 Oct 2026)

gov.uk/guidance/rates-and-thresholds-for-employers-2026-to-2027: employee Class 1 NI 8% between the primary
  threshold (£12,570 a year) and the upper earnings limit (£50,270), 2% above; employer 15% above £5,000;
  income tax (England) 20% basic rate on the first £37,700 above the £12,570 Personal Allowance.
gov.uk/hmrc-internal-manuals/pensions-tax-manual/ptm044220 (relief at source): a basic-rate taxpayer pays £80,
  the scheme claims £20 from HMRC, £100 goes in. Net pay (PTM044230) gives the same income-tax-only relief.
gov.uk/workplace-pensions/what-you-your-employer-and-the-government-pay: with salary sacrifice "you and your
  employer pay less tax and National Insurance".
gov.uk/guidance/salary-sacrifice-and-the-effects-on-paye: cash pay can't go below the National Minimum Wage;
  it can affect statutory pay and earnings-related benefits.
legislation.gov.uk/ukpga/2026/15 (NIC (Employer Pensions Contributions) Act 2026, Royal Assent 29 Apr 2026):
  from the 2029-30 tax year, salary sacrificed into a pension above a £2,000-a-year limit is treated as
  earnings for NI. gov.uk "Changes to salary sacrifice for pensions from April 2029": the first £2,000 stays
  NI-free; above it employer and employee NI is due; still exempt from income tax; "Most employees making
  typical contributions will not be affected."
Assumptions: an employee taxed at the basic rate in England, Wales or Northern Ireland, earning between £12,570
  and £50,270 (e.g. £35,000), whose employer offers salary sacrifice and pays the whole sacrificed amount in.
"""
from motion import *  # noqa: F401,F403
from brand import *  # noqa: F401,F403

BRAND = True
COVER = dict(words=("£1,000", "FOR £720?"), highlight=1, hero="Scissors", left="Briefcase",
             right="Hourglass not done", particles="Coin")

# ---- figures (gov.uk / legislation.gov.uk, checked 25 Oct 2026) --------------------------------------------
PA, UEL = 12_570, 50_270          # Personal Allowance = NI primary threshold; basic-rate limit = NI UEL
BASIC_TAX = 0.20                  # income tax, basic rate (England, Wales, NI)
EE_NI = 0.08                      # employee Class 1 NI between £12,570 and £50,270
ER_NI = 0.15                      # employer NI (description only)
CAP = 2_000                       # NI-free salary sacrifice a year, from 6 April 2029
CAP_YEAR = 2029
SALARY = 35_000                   # illustration: inside the basic-rate / 8% NI band
assert PA < SALARY - 1_000 and SALARY <= UEL

IN_PENSION = 1_000
TAX_SAVED = IN_PENSION * BASIC_TAX
NI_SAVED = IN_PENSION * EE_NI
USUAL_COST = IN_PENSION - TAX_SAVED                 # relief at source / net pay: income tax relief only
SACRIFICE_COST = IN_PENSION - TAX_SAVED - NI_SAVED  # salary sacrifice: no income tax and no NI


def take_home(gross):  # employee take-home in the 20% / 8% band (only differences matter here)
    return gross - max(0, gross - PA) * BASIC_TAX - max(0, gross - PA) * EE_NI


assert round(take_home(SALARY) - take_home(SALARY - IN_PENSION), 2) == SACRIFICE_COST == 720
assert round(TAX_SAVED) == 200 and round(NI_SAVED) == 80
assert USUAL_COST == 800 and USUAL_COST - SACRIFICE_COST == NI_SAVED
assert IN_PENSION < CAP                              # "swap under £2,000 a year, and nothing changes"
ER_SAVED = IN_PENSION * ER_NI
assert ER_SAVED == 150                               # description: the employer saves £150 NI too
HIGHER_COST = IN_PENSION * (1 - 0.40 - 0.02)         # description: higher-rate, 40% tax + 2% NI
assert round(HIGHER_COST) == 580
OVER = 3_000                                         # description: £3,000 swapped from 2029 -> NI on £1,000
assert (OVER - CAP) * EE_NI == 80

STAMP = "GOV.UK · 2026/27 RATES · CHECKED 25 OCT 2026"


def s_hook(L, t):  # sentence 0 · risk
    cover_hook(L, t, gbp(SACRIFICE_COST), sub="for £1,000 in your pension", number_at=tk(0, "£720"),
               kicker="BASIC-RATE TAXPAYER · 2026/27")


def s_usual(L, t):  # sentence 1 · risk: the usual way costs more, this tax year
    beat(L, "THE USUAL WAY", t, S(1) - 0.1, tone="red")
    L.emoji("receipt", W / 2, 530, 160, t, tk(1, "Pay"), bounce=True)
    L.text("£1,000 INTO YOUR PENSION", W / 2, 690, 42, M, ramp(t, tk(1, "usual"), 0.25), weight="ExtraBold")
    L.text("COSTS YOUR TAKE-HOME", W / 2, 750, 42, M, ramp(t, tk(1, "tax"), 0.25), weight="ExtraBold")
    big_number(L, gbp(USUAL_COST), W / 2, 880, t, at=tk(1, "£800"), size=170, color=RED)
    caveat(L, t, tk(1, "£800") + 0.3, ["Income tax relief only: £200 back on £1,000."], cy=1020, size=28)


def s_versus(L, t):  # sentences 2-3 · question 1: same pension, different price + rehook
    beat(L, "THE MATHS", t, S(2) - 0.1)
    versus(L, t,
           dict(title="USUAL WAY", label="£1,000 IN THE PENSION", value=gbp(USUAL_COST), color=RED,
                start=S(2), at=tk(2, "pension"), tone="red", emoji="receipt"),
           dict(title="THE OTHER WAY", label="£1,000 IN THE PENSION", value=gbp(SACRIFICE_COST), color=G,
                start=tk(2, "same"), at=tk(2, "different"), tone="green", emoji="briefcase"),
           cy=590, h=320)
    chip(L, "SAME POT. DIFFERENT PRICE.", W / 2, 810, t, tk(2, "different"), "white", 36)
    a = ramp(t, tk(3, "Here's"), 0.2)
    if a > 0:
        L.emoji("thinking_face", W / 2, 960, 120, t, tk(3, "Here's"), bounce=True)
        L.text("HERE'S THE STRANGE PART", W / 2, 1100, 48, Wt, a, weight="Black")


def s_twist(L, t):  # sentences 4-5 · twist 1: salary sacrifice skips National Insurance too
    beat(L, "twist", t, S(4) - 0.1)
    chip(L, "SALARY SACRIFICE", W / 2, 440, t, tk(4, "Give"), "gold", 44, emoji="briefcase")
    L.text("YOU GIVE UP £1,000 OF PAY.", W / 2, 540, 36, Wt, ramp(t, tk(4, "pay,"), 0.25), weight="ExtraBold")
    L.text("YOUR BOSS PAYS IT INTO YOUR PENSION.", W / 2, 595, 36, Wt, ramp(t, tk(4, "boss"), 0.25),
           weight="ExtraBold")
    value_card(L, W / 2 - 225, 760, 430, t, tk(5, "taxed"), "check_mark_button", "NO INCOME TAX",
               "+" + gbp(TAX_SAVED), value_at=tk(5, "taxed"))
    value_card(L, W / 2 + 225, 760, 430, t, tk(5, "National"), "check_mark_button", "NO NATIONAL INS.",
               "+" + gbp(NI_SAVED), value_at=tk(5, "Insurance"))
    checked(L, STAMP, W / 2, 900, t, tk(5, "too."))


def s_cap(L, t):  # sentences 6-7 · rehook + question 2: the cap
    beat(L, "catch", t, S(6) - 0.1)
    L.emoji("calendar", W / 2, 520, 160, t, tk(7, "From"), bounce=True)
    big_number(L, f"APRIL {CAP_YEAR}", W / 2, 720, t, at=tk(7, "2029"), size=130, color=Wt)
    chip(L, "THE NI BREAK GETS A CAP", W / 2, 860, t, tk(7, "cap."), "red", 40, emoji="locked")
    checked(L, "LEGISLATION.GOV.UK · NIC ACT 2026 · CHECKED 25 OCT 2026", W / 2, 970, t, tk(7, "cap.") + 0.3)


def s_under(L, t):  # sentence 8 · twist 2: under £2,000 a year, nothing changes
    beat(L, "miss", t, S(8) - 0.1)
    L.text("SWAP UNDER", W / 2, 470, 44, M, ramp(t, tk(8, "Swap"), 0.25), weight="ExtraBold")
    big_number(L, gbp(CAP), W / 2, 600, t, at=tk(8, "£2,000"), size=170, color=G)
    L.text("A YEAR", W / 2, 720, 44, Wt, ramp(t, tk(8, "year,"), 0.25), weight="ExtraBold")
    chip(L, "NOTHING CHANGES", W / 2, 830, t, tk(8, "nothing"), "green", 44, emoji="shield")
    caveat(L, t, tk(8, "changes") + 0.1, ["Above £2,000, NI is due on the extra. Still no income tax.",
                                          "General education, not financial advice."], cy=960, size=26)


def s_loop(L, t):  # sentence 9: loop line back into sentence 0
    loop_close(L, t, 9, comment="WOULD YOU SWAP? COMMENT")


SCENES = [(0, 0), (1, 1), (2, 3), (4, 5), (6, 7), (8, 8), (9, 9)]
DRAW = [s_hook, s_usual, s_versus, s_twist, s_cap, s_under, s_loop]


def events():
    ev = [{"t": tk(0, "£720") + 0.05, "kind": "coin"},
          {"t": tk(1, "£800"), "kind": "boom"},
          {"t": tk(2, "different"), "kind": "pop"},
          {"t": tk(5, "taxed"), "kind": "coin"},
          {"t": tk(5, "Insurance"), "kind": "coin"},
          {"t": tk(7, "cap."), "kind": "boom"},
          {"t": tk(8, "£2,000"), "kind": "pop"},
          {"t": tk(8, "nothing"), "kind": "coin"}]
    return scene_events(ev)
