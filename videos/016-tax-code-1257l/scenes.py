"""Video 016 (brand-v2, format: calc, told as the dopamine loop — BRAND.md §0c): what 1257L on your payslip
means, and what a 0T code does to your first pay at a new job. (figures checked 26 Oct 2026)

gov.uk/tax-codes/what-your-tax-code-means: the numbers are your tax-free income from that job; HMRC starts from
  the standard Personal Allowance and replaces the last digit with a letter (e.g. £11,000 -> 1100L).
  L = "entitled to the standard tax-free Personal Allowance"; 0T = "Personal Allowance has been used up" or a
  new job where the employer lacks the details to give you a code; BR = all income from this job at basic rate.
gov.uk/government/publications/p9x-tax-codes/p9x-tax-codes-to-use-from-6-april-2026: "The emergency code is
  1257L for all employees"; the basic Personal Allowance is £12,570 for the whole of the UK in 2026-27.
gov.uk/guidance/changes-to-your-tax-code-when-you-start-a-new-job: without a P45 or starter checklist you "may
  have been given a BR or 0T tax code"; "Your new tax code will make sure any overpayments are paid back to you
  through your pay" (or after the tax year, if your old employer doesn't confirm you've left).
gov.uk/tax-codes/if-youve-paid-too-much-or-too-little-tax: HMRC asks your employer to refund the difference in
  your pay; "You cannot get a refund until HMRC get your income details"; a P45 can help.
gov.uk/tax-codes/emergency-tax-codes: HMRC usually updates your code within 35 days of starting a new job.
gov.uk/government/publications/rates-and-allowances-income-tax/income-tax-rates-and-allowances-current-and-past:
  2026-27 Personal Allowance £12,570; basic rate 20% on the first £37,700 above it.
Assumptions: England, Wales or Northern Ireland rates (Scotland differs), paid monthly, a 0T (or BR) code applied
  on a non-cumulative basis in month 1, monthly pay between £1,047.50 and £3,141.67 (e.g. £2,500 = £30,000 a
  year), no other income or deductions.
"""
from motion import *  # noqa: F401,F403
from brand import *  # noqa: F401,F403

BRAND = True
COVER = dict(words=("TAX CODE", "£210?"), highlight=1, hero="Receipt", left="Briefcase",
             right="Magnifying glass tilted left", particles="Coin")

# ---- figures (gov.uk, checked 26 Oct 2026) ------------------------------------------------------------------
PA = 12_570                       # Personal Allowance 2026-27 (whole UK)
BASIC = 0.20                      # basic rate (England, Wales, NI)
BASIC_BAND = 37_700               # taxable income charged at 20%
CODE = f"{PA // 10}L"             # the number is the allowance with its last digit replaced by a letter
assert CODE == "1257L"
assert PA // 10 * 10 == PA         # 1257 x 10 = £12,570

PAY = 2_500                       # illustration: monthly pay (£30,000 a year)
assert PA / 12 < PAY <= BASIC_BAND / 12      # whole month's taxable pay stays in the 20% band on both codes


def month_tax(pay, allowance_year):  # month-1 / non-cumulative PAYE, basic-rate band only
    taxable = max(0, pay - allowance_year / 12)
    assert taxable <= BASIC_BAND / 12
    return round(taxable * BASIC, 2)


TAX_1257L = month_tax(PAY, PA)
TAX_0T = month_tax(PAY, 0)
EXTRA = round(TAX_0T - TAX_1257L, 2)
assert TAX_1257L == 290.50 and TAX_0T == 500.00
assert EXTRA == round(PA / 12 * BASIC, 2) == 209.50     # the same for any pay in the range above
assert 205 < EXTRA < 210                                  # spoken: "almost £210"
REFUND_DAYS = 35                                          # HMRC usually updates the code within 35 days

STAMP = "GOV.UK · 2026/27 TAX CODES · CHECKED 26 OCT 2026"


def s_hook(L, t):  # sentence 0 · risk
    cover_hook(L, t, gbp(EXTRA, 2), sub="less in your first month's pay", number_at=tk(0, "£210"),
               kicker="NEW JOB · 2026/27")


def s_code(L, t):  # sentences 1-2 · question 1: the tiny code
    beat(L, "THE CODE", t, S(1) - 0.1)
    L.emoji("receipt", W / 2, 520, 150, t, tk(1, "tiny"), bounce=True)
    a = panel(L, W / 2, 790, 760, 280, t, tk(1, "code") - 0.1, "white")
    if a > 0:
        L.text("YOUR PAYSLIP", W / 2, 690, 34, M, a, weight="ExtraBold")
        L.text("NAME: YOU", W / 2 - 200, 760, 36, Wt, a, weight="ExtraBold")
        L.text("TAX CODE:", W / 2 + 120, 760, 36, Wt, a, weight="ExtraBold")
    big_number(L, CODE, W / 2, 860, t, at=tk(2, "1257L"), size=130, color=G)


def s_decode(L, t):  # sentence 3 · twist 1: it's your tax-free allowance
    beat(L, "twist", t, S(3) - 0.1)
    timed_line(L, [("1257", Wt, tk(3, "random")), ("×", M, tk(3, "it's")), ("10", Wt, tk(3, "your"))],
               W / 2, 520, 84, t)
    big_number(L, gbp(PA), W / 2, 700, t, at=tk(3, "£12,570"), size=150, color=G)
    chip(L, "TAX-FREE A YEAR", W / 2, 830, t, tk(3, "tax-free"), "green", 40, emoji="shield")
    chip(L, "L = THE STANDARD ALLOWANCE", W / 2, 930, t, tk(3, "tax-free") + 0.35, "white", 32)
    checked(L, STAMP, W / 2, 1040, t, tk(3, "tax-free") + 0.6)


def s_catch(L, t):  # sentences 4-5 · rehook + question 2: no P45, code 0T
    beat(L, "catch", t, S(4) - 0.1)
    L.emoji("warning", W / 2, 520, 150, t, S(4), bounce=True)
    chip(L, "NEW JOB · NO P45", W / 2, 680, t, tk(5, "P45"), "white", 40, emoji="briefcase")
    big_number(L, "0T", W / 2, 860, t, at=tk(5, "0T"), size=190, color=RED)


def s_versus(L, t):  # sentence 6 · answer: none of your pay is tax-free
    beat(L, "THE MATHS", t, S(6) - 0.1, sub="TAX ON £2,500 IN MONTH ONE", sub_at=S(6))
    versus(L, t,
           dict(title="1257L", label="TAX THIS MONTH", value=gbp(TAX_1257L, 2), color=G,
                start=S(6), at=tk(6, "not"), tone="green", emoji="check_mark_button"),
           dict(title="0T", label="TAX THIS MONTH", value=gbp(TAX_0T, 2), color=RED,
                start=tk(6, "one"), at=tk(6, "pound"), tone="red", emoji="cross_mark"),
           cy=620, h=300)
    chip(L, f"{gbp(EXTRA, 2)} MORE TAX", W / 2, 840, t, tk(6, "tax-free"), "red", 44, emoji="money_with_wings")


def s_miss(L, t):  # sentences 7-8 · rehook + twist 2: it comes back
    beat(L, "miss", t, S(7) - 0.1)
    L.emoji("thinking_face", W / 2, 510, 140, t, S(7), bounce=True)
    value_card(L, W / 2, 720, 700, t, tk(8, "Once"), "coin", "PAID BACK IN YOUR PAY", "+" + gbp(EXTRA, 2),
               value_at=tk(8, "back"))
    caveat(L, t, tk(8, "pay.") , [f"Once your code is fixed: HMRC usually updates it within {REFUND_DAYS} days.",
                                  "Rates for England, Wales and NI. Not financial advice."], cy=880, size=26)


def s_loop(L, t):  # sentence 9: loop line back into sentence 0
    loop_close(L, t, 9, comment="FAIR OR NOT? COMMENT")


SCENES = [(0, 0), (1, 2), (3, 3), (4, 5), (6, 6), (7, 8), (9, 9)]
DRAW = [s_hook, s_code, s_decode, s_catch, s_versus, s_miss, s_loop]


def events():
    ev = [{"t": tk(0, "£210") + 0.05, "kind": "boom"},
          {"t": tk(2, "1257L"), "kind": "pop"},
          {"t": tk(3, "£12,570"), "kind": "coin"},
          {"t": tk(5, "0T"), "kind": "boom"},
          {"t": tk(6, "pound"), "kind": "pop"},
          {"t": tk(8, "back"), "kind": "coin"}]
    return scene_events(ev)
