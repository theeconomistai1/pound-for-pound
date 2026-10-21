"""Video 006 (brand-v2, format: calc): the £100k trap — keep 38p of each pound just over £100,000, and how a
pension contribution wins the allowance back. (figures checked 21 Oct 2026, tax year 2026/27, England, Wales
and Northern Ireland; Scotland's income tax bands differ)

gov.uk/income-tax-rates: Personal Allowance £12,570; 20% to £50,270; 40% £50,271-£125,140; 45% above;
  allowance goes down £1 for every £2 of adjusted net income above £100,000, zero at £125,140.
gov.uk/guidance/rates-and-thresholds-for-employers-2026-to-2027: employee Class 1 NI 8% to the UEL (£50,270),
  2% above.
gov.uk/guidance/adjusted-net-income: relief-at-source pension contributions come off net income grossed up
  (what you paid plus basic-rate tax).
gov.uk/tax-on-your-private-pension/pension-tax-relief: relief at source — the provider adds 20%; higher-rate
  relief is claimed on a Self Assessment tax return.
"""
from motion import *  # noqa: F401,F403
from brand import *  # noqa: F401,F403

BRAND = True
COVER = dict(words=("£100K", "TRAP"), highlight=1, hero="Mouse trap", left="Classical building",
             right="Receipt", particles="Coin")

# ---- figures (2026/27, rUK) --------------------------------------------------------------------------------
PA, TAPER_START = 12_570, 100_000
BASIC_BAND = 37_700                     # basic-rate band width -> higher rate above £50,270
UEL = 50_270
BASIC, HIGHER, ADDITIONAL = 0.20, 0.40, 0.45
NI_MAIN, NI_UPPER = 0.08, 0.02
PA_GONE = TAPER_START + 2 * PA
assert PA_GONE == 125_140 and PA + BASIC_BAND == UEL


def allowance(ani):
    return max(0, PA - max(0, ani - TAPER_START) // 2)


def income_tax(income, gross_pension=0):
    """Income tax for a relief-at-source contribution: ANI falls by the gross amount and the basic-rate
    band is extended by it (the 'higher-rate relief')."""
    ani = income - gross_pension
    pa = allowance(ani)
    taxable = max(0, income - pa)
    band = BASIC_BAND + gross_pension
    higher_top = PA_GONE + gross_pension         # 45% on taxable income above £125,140 (limit extended too)
    tax = min(taxable, band) * BASIC
    tax += max(0, min(taxable, higher_top) - band) * HIGHER
    tax += max(0, taxable - higher_top) * ADDITIONAL
    return tax


def employee_ni(income):
    return max(0, min(income, UEL) - PA) * NI_MAIN + max(0, income - UEL) * NI_UPPER


# each extra £1 between £100,000 and £125,140 (checked on a real step, not by hand)
BASE = 110_000
extra_tax = income_tax(BASE + 2) - income_tax(BASE)       # £2 more -> £1 of allowance lost
extra_ni = employee_ni(BASE + 2) - employee_ni(BASE)
TAX_P = round(extra_tax / 2 * 100)                        # 60p per £1
DIRECT_P = round(HIGHER * 100)                            # 40p
LOST_P = TAX_P - DIRECT_P                                 # 20p: half a pound of allowance taxed at 40%
NI_P = round(extra_ni / 2 * 100)                          # 2p
GONE_P = TAX_P + NI_P
KEEP_P = 100 - GONE_P
assert (DIRECT_P, LOST_P, NI_P, GONE_P, KEEP_P) == (40, 20, 2, 62, 38)

# the pension fix: £10,000 gross on a £110,000 salary (relief at source)
SALARY, GROSS = 110_000, 10_000
assert SALARY - GROSS == TAPER_START and allowance(SALARY) == 7_570 and allowance(SALARY - GROSS) == PA
YOU_PAY = GROSS * (1 - BASIC)                              # £8,000 from your bank account
ADDED = GROSS - YOU_PAY                                    # £2,000 added by the provider
CLAIMED = income_tax(SALARY) - income_tax(SALARY, GROSS)   # £4,000 back via Self Assessment
COST = YOU_PAY - CLAIMED
assert (YOU_PAY, ADDED, CLAIMED, COST) == (8_000, 2_000, 4_000, 4_000)
assert round((GROSS - COST) / GROSS * 100) == 60           # 60% relief overall

STAMP = "GOV.UK · 2026/27 RATES · CHECKED 21 OCT 2026"


def s_hook(L, t):  # sentence 0
    cover_hook(L, t, f"{KEEP_P}p", sub="of each £1 just over £100,000", number_at=tk(0, "38p"),
               kicker="EARN JUST OVER £100,000")


def s_maths(L, t):  # sentences 1-3
    beat(L, "maths", t, S(1) - 0.1)
    value_card(L, W / 2, 500, 880, t, S(1), "locked", "TAX-FREE ALLOWANCE", gbp(PA), color=Wt,
               value_at=tk(1, "allowance"), sub="−£1 for every £2 over £100k")
    # one extra pound, split into what goes where
    timed_line(L, [(f"{DIRECT_P}p", RED, tk(2, "40p")), ("+", M, tk(2, "20p")), (f"{LOST_P}p", RED, tk(2, "20p")),
                   ("+", M, tk(3, "2p")), (f"{NI_P}p", RED, tk(3, "2p"))], W / 2, 690, 96, t)
    a = ramp(t, tk(2, "40p") + 0.1, 0.3)
    L.text("TAX", W / 2 - 250, 780, 26, M, a, weight="ExtraBold")
    L.text("LOST ALLOWANCE", W / 2 - 10, 780, 26, M, ramp(t, tk(2, "20p") + 0.1, 0.3), weight="ExtraBold")
    L.text("NI", W / 2 + 255, 780, 26, M, ramp(t, tk(3, "2p") + 0.1, 0.3), weight="ExtraBold")
    pa = panel(L, W / 2, 960, 760, 200, t, tk(3, "62p") - 0.15, "red")
    if pa > 0:
        big_number(L, f"{GONE_P}p GONE", W / 2, 935, t, tk(3, "62p"), size=110, color=RED, alpha=pa)
        L.text(f"YOU KEEP {KEEP_P}p OF EACH £1", W / 2, 1020, 32, Wt, pa, weight="ExtraBold")
    checked(L, STAMP, W / 2, 1150, t, tk(3, "62p") + 0.4)


def s_twist(L, t):  # sentence 4
    beat(L, "twist", t, S(4) - 0.1, sub="TAX-FREE ALLOWANCE", sub_at=S(4) + 0.2)
    versus(L, t,
           dict(title="NO PENSION", label="£110,000 SALARY", value=gbp(allowance(SALARY)), color=RED,
                start=S(4), at=tk(4, "£110"), emoji="briefcase"),
           dict(title="£10K PENSION", label="COUNTS AS £100,000", value=gbp(allowance(SALARY - GROSS)), color=G,
                start=tk(4, "£110") + 0.2, at=tk(4, "back"), tone="green", emoji="bank"),
           cy=640, h=360)
    checked(L, "GOV.UK · ADJUSTED NET INCOME · CHECKED 21 OCT 2026", W / 2, 900, t, tk(4, "back") + 0.4)


def s_miss(L, t):  # sentences 5-6
    beat(L, "miss", t, S(5) - 0.1)
    value_card(L, W / 2, 460, 880, t, S(5), "bank", "IN YOUR PENSION", gbp(GROSS), color=Wt,
               value_at=tk(5, "£10,000"), h=130, sub="relief at source")
    value_card(L, W / 2, 610, 880, t, tk(5, "£10,000") + 0.2, "coin", "20% ADDED BY THE PROVIDER",
               "−" + gbp(ADDED), color=C, h=130, sub="automatic")
    value_card(L, W / 2, 760, 880, t, tk(5, "costs") - 0.2, "receipt", "EXTRA RELIEF CLAIMED",
               "−" + gbp(CLAIMED), color=C, h=130, sub="on your tax return")
    pa = ramp(t, tk(5, "£4,000") - 0.1, 0.25)
    L.text("WHAT IT COSTS YOU", W / 2, 885, 28, M, pa, weight="ExtraBold")
    if pa > 0:
        big_number(L, gbp(COST), W / 2, 975, t, tk(5, "£4,000"), size=120, alpha=pa)
    chip(L, "NOT AUTOMATIC: CLAIM IT ON A TAX RETURN", W / 2, 1110, t, tk(6, "catch"), "red", 28, emoji="warning")
    caveat(L, t, S(6) + 0.6, ["2026/27, England, Wales & NI. General education, not advice."], cy=1200, size=26)


def s_loop(L, t):  # sentence 7: the loop line, the picture rebuilds the cover
    loop_close(L, t, 7, comment="£120K: HOW MUCH? COMMENT")


SCENES = [(0, 0), (1, 3), (4, 4), (5, 6), (7, 7)]
DRAW = [s_hook, s_maths, s_twist, s_miss, s_loop]


def events():
    ev = [{"t": tk(0, "38p") + 0.05, "kind": "coin"},
          {"t": tk(1, "allowance"), "kind": "pop"},
          {"t": tk(2, "40p"), "kind": "pop"}, {"t": tk(2, "20p"), "kind": "pop"}, {"t": tk(3, "2p"), "kind": "pop"},
          {"t": tk(3, "62p"), "kind": "boom"},
          {"t": tk(4, "back"), "kind": "coin"},
          {"t": tk(5, "£4,000"), "kind": "coin"},
          {"t": tk(6, "catch"), "kind": "boom"}]
    return scene_events(ev)
