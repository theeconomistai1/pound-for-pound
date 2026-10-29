"""022: Budget 2026 raises tax on savings interest to 24% from April 2027, yet the Personal Savings Allowance
keeps most basic-rate savers tax-free; cross into the higher-rate band and it halves to £500 — format: calc
(brand-v2; BRAND.md §1, told as the dopamine loop §0c). (figures checked 29 Oct 2026)

gov.uk/government/publications/budget-2026-overview-of-tax-legislation-and-rates-ootlar/annex-a-rates-and-allowances
  2026-27 vs 2027-28: savings basic rate 20% -> 24%, savings higher rate 40% -> 44%, additional 45% -> 49%;
  Personal Allowance £12,570 both years; basic rate band £1 to £37,700 both years;
  Personal Savings Allowance £1,000 (basic rate) and £500 (higher rate) both years; starting rate for savings 0%,
  limit £5,000 both years.
gov.uk/government/publications/budget-2026-overview-of-tax-legislation-and-rates-ootlar/budget-2026-overview-of-tax-legislation-and-rates-ootlar
  para 1.1: savings basic 24%, higher 44%, additional 49% for 2027 to 2028; "take effect from 6 April 2027"; UK-wide.
gov.uk/government/publications/budget-2026-document/budget-2026-html (3.9, para 74-75):
  Budget 2025 raised savings and property income rates by two points; Budget 2026 adds "a further two percentage
  points"; "84% of income tax payers will be unaffected"; "basic rate taxpayers would need over £25,000 in savings
  in addition to any ISA savings before paying tax".
gov.uk/government/publications/changes-to-tax-rates-for-property-savings-dividend-income (Budget 2025): savings
  basic 20% -> 22% etc. from April 2027; "it is only the rates of tax charged that will change".
gov.uk/government/publications/income-tax-personal-savings-allowance/income-tax-personal-savings-allowance:
  allowance £1,000, or £500 with "higher rate income" (income charged at the higher rate "or would be but for the
  operation of this new savings nil rate"), nil with additional rate income; income within the allowance "will
  still count towards their basic or higher rate limits".
Assumptions: England, Wales and Northern Ireland bands (savings income uses UK rates everywhere, but Scottish
  taxpayers' bands differ); interest outside ISAs; 'tip you over' example = £50,000 salary + £1,000 interest.
"""
from motion import *  # noqa: F401,F403
from brand import *  # noqa: F401,F403

BRAND = True
COVER = dict(words=("SAVINGS", "TAX HIKE?"), highlight=1, hero="Jar", fill="Coin", left="Classical building",
             right="Calendar", particles="Coin")

# ---- figures (gov.uk, Budget 2026, checked 29 Oct 2026) -------------------------------------------------
NOW_BASIC, NOW_HIGHER = 20, 40                    # savings rates 2026-27
B25_RISE, B26_RISE = 2, 2                         # Budget 2025 + Budget 2026, each two percentage points
NEW_BASIC, NEW_HIGHER, NEW_ADD = 24, 44, 49       # savings rates 2027-28 (Annex A, from 6 April 2027)
assert NOW_BASIC + B25_RISE + B26_RISE == NEW_BASIC          # spoken: "24%"
assert NOW_HIGHER + B25_RISE + B26_RISE == NEW_HIGHER        # spoken: "44%"
PSA_BASIC, PSA_HIGHER, PSA_ADD = 1_000, 500, 0    # Personal Savings Allowance, unchanged in 2027-28
assert PSA_HIGHER * 2 == PSA_BASIC                # spoken: "quietly halves"
NEED = 25_000                                     # Budget 2026 para 75: "over £25,000 in savings"
RATE_ILLUS = 0.04                                 # illustration: the interest rate at which £25,000 earns £1,000
assert round(NEED * RATE_ILLUS) == PSA_BASIC
UNAFFECTED = 84                                   # % of income tax payers unaffected (Budget 2026 para 74)
assert UNAFFECTED > 50                            # spoken: "Not for most."
PA, BASIC_BAND = 12_570, 37_700
HRT = PA + BASIC_BAND
assert HRT == 50_270                              # higher-rate threshold (England, Wales, NI)
SRS_LIMIT = 5_000


def savings_tax(salary, interest, basic_rate, higher_rate):
    """Tax on savings interest for an employee (non-savings income = salary), PA not tapered (< £100,000)."""
    non_sav_taxable = max(0, salary - PA)
    total_taxable = non_sav_taxable + interest
    higher_income = total_taxable > BASIC_BAND               # some income would be charged at the higher rate
    psa = PSA_HIGHER if higher_income else PSA_BASIC
    srs = max(0, SRS_LIMIT - non_sav_taxable)
    band_left = max(0, BASIC_BAND - non_sav_taxable)
    tax, used = 0.0, 0
    for amount, rate in ((min(interest, srs), 0), (min(max(0, interest - srs), psa), 0)):
        used += amount
    rest = interest - used
    # nil-rate amounts use up the basic rate band first; what's left is taxed at the band it falls in
    basic_left = max(0, band_left - used)
    tax = min(rest, basic_left) * basic_rate / 100 + max(0, rest - basic_left) * higher_rate / 100
    return psa, round(tax, 2)


# You and a friend: £1,000 interest each (≈ £25,000 at 4%)
INTEREST = 1_000
assert savings_tax(30_000, INTEREST, NEW_BASIC, NEW_HIGHER) == (1_000, 0)       # basic rate: nothing to pay
P_HI, T_HI = savings_tax(60_000, INTEREST, NEW_BASIC, NEW_HIGHER)
assert (P_HI, T_HI) == (500, 220.0)              # higher rate from April 2027: £500 taxed at 44%
# 'it can tip you over': £50,000 salary + £1,000 interest = £51,000, over £50,270
TIP_SALARY = 50_000
assert TIP_SALARY < HRT < TIP_SALARY + INTEREST
P_TIP, T_TIP = savings_tax(TIP_SALARY, INTEREST, NEW_BASIC, NEW_HIGHER)
assert P_TIP == 500 and T_TIP == 220.0           # the salary alone is basic rate, yet the allowance halves

STAMP = "GOV.UK · BUDGET 2026 · CHECKED 29 OCT 2026"


def s_hook(L, t):  # sentence 0 · risk
    cover_hook(L, t, f"{NEW_BASIC}%", sub="tax on savings interest · basic rate", number_at=tk(0, "24%"),
               kicker="BUDGET 2026 · FROM 6 APRIL 2027")


def s_question(L, t):  # sentence 1 · question: so savers lose out?
    beat(L, "THE BUDGET", t, S(1) - 0.1)
    versus(L, t,
           dict(title="NOW · 2026/27", label="SAVINGS TAX", value=f"{NOW_BASIC}%", color=Wt, start=S(1),
                at=S(1) + 0.2, tone=None, emoji="calendar"),
           dict(title="FROM APRIL 2027", label="SAVINGS TAX", value=f"{NEW_BASIC}%", color=RED,
                start=S(1) + 0.15, at=tk(1, "hit."), tone="red", emoji="chart_increasing"),
           cy=620, h=300)
    L.emoji("thinking_face", W / 2, 900, 130, t, tk(1, "hit."), bounce=True)
    checked(L, STAMP, W / 2, 1060, t, tk(1, "hit.") + 0.3)


def s_twist(L, t):  # sentence 2 · twist 1: the first £1,000 stays tax-free
    beat(L, "twist", t, S(2) - 0.1)
    chip(L, "NOT FOR MOST", W / 2, 470, t, S(2), "green", 44, emoji="check_mark_button")
    a = panel(L, W / 2, 720, 780, 280, t, tk(2, "first") - 0.15, "green")
    big_number(L, gbp(PSA_BASIC), W / 2, 700, t, at=tk(2, "£1,000"), size=170, color=G, alpha=a)
    chip(L, "OF INTEREST · TAX-FREE", W / 2, 810, t, tk(2, "tax-free."), "white", 36, emoji="shield")
    caveat(L, t, tk(2, "tax-free.") + 0.2, ["Personal Savings Allowance · basic rate"], cy=950, size=30)


def s_need(L, t):  # sentence 3 · answer: over £25,000 before you pay any
    beat(L, "maths", t, S(3) - 0.1)
    value_card(L, W / 2, 560, 800, t, S(3), "bank", "SAVED OUTSIDE AN ISA", f"OVER {gbp(NEED)}", color=G,
               value_at=tk(3, "£25,000"))
    chip(L, f"£1,000 INTEREST A YEAR AT {round(RATE_ILLUS * 100)}%", W / 2, 760, t, tk(3, "ISA,"), "white", 34,
         emoji="coin")
    chip(L, "TAX TO PAY: £0", W / 2, 880, t, tk(3, "any."), "green", 42)


def s_catch(L, t):  # sentences 4-5 · rehook + question 2: something halves
    beat(L, "catch", t, S(4) - 0.1)
    L.emoji("warning", W / 2, 560, 170, t, S(4), bounce=True)
    chip(L, f"HIGHER RATE · OVER {gbp(HRT)}", W / 2, 800, t, tk(5, "higher-rate"), "red", 40, emoji="briefcase")
    chip(L, "SOMETHING HALVES", W / 2, 920, t, tk(5, "halves."), "white", 38)


def s_halve(L, t):  # sentence 6 · twist 2: £500, the rest at 44%
    beat(L, "twist", t, S(6) - 0.1, sub="TAX-FREE INTEREST A YEAR", sub_at=S(6))
    versus(L, t,
           dict(title="BASIC RATE", label="TAX-FREE", value=gbp(PSA_BASIC), color=G, start=S(6),
                at=S(6) + 0.2, tone="green", emoji="woman"),
           dict(title="HIGHER RATE", label="TAX-FREE", value=gbp(PSA_HIGHER), color=RED, start=S(6) + 0.15,
                at=tk(6, "£500."), tone="red", emoji="man"),
           cy=600, h=300)
    chip(L, f"THE REST TAXED AT {NEW_HIGHER}%", W / 2, 830, t, tk(6, "44%."), "red", 42, emoji="receipt")
    caveat(L, t, tk(6, "44%.") + 0.3, [f"{NEW_HIGHER}% = savings higher rate from 6 April 2027 (now {NOW_HIGHER}%)."],
           cy=950, size=26)


def s_miss(L, t):  # sentence 7 · answer: your interest counts as income
    beat(L, "miss", t, S(7) - 0.1)
    value_card(L, W / 2, 500, 760, t, S(7), "briefcase", "SALARY", gbp(TIP_SALARY), color=Wt,
               value_at=S(7) + 0.2)
    value_card(L, W / 2, 680, 760, t, tk(7, "interest"), "coin", "+ SAVINGS INTEREST", gbp(INTEREST), color=Wt,
               value_at=tk(7, "income"))
    chip(L, f"TOTAL {gbp(TIP_SALARY + INTEREST)} · OVER {gbp(HRT)}", W / 2, 860, t, tk(7, "tip"), "red", 36,
         emoji="warning")
    caveat(L, t, tk(7, "over.") + 0.1, ["England, Wales & NI bands. Interest outside ISAs.",
                                         "Rules as at 29 Oct 2026. Not advice."], cy=1000, size=26)


def s_loop(L, t):  # sentence 8: loop line back into sentence 0
    loop_close(L, t, 8, comment="FAIR OR NOT? COMMENT")


SCENES = [(0, 0), (1, 1), (2, 2), (3, 3), (4, 5), (6, 6), (7, 7), (8, 8)]
DRAW = [s_hook, s_question, s_twist, s_need, s_catch, s_halve, s_miss, s_loop]


def events():
    ev = [{"t": tk(0, "24%") + 0.05, "kind": "boom"},
          {"t": tk(2, "£1,000"), "kind": "coin"},
          {"t": tk(3, "£25,000"), "kind": "pop"},
          {"t": tk(5, "halves."), "kind": "boom"},
          {"t": tk(6, "£500."), "kind": "pop"},
          {"t": tk(6, "44%."), "kind": "boom"},
          {"t": tk(7, "tip"), "kind": "pop"}]
    return scene_events(ev)
