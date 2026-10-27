"""Video 018 (brand-v2, format: calc, told as the dopamine loop — BRAND.md §0c): Plan 2 vs Plan 5 student
loans on the same salary. (figures checked 27 Oct 2026)

gov.uk/government/publications/payroll-technical-specifications-student-loans/collection-of-student-loans-from-6-april-2026:
  thresholds from 6 April 2026: Plan 2 £29,385, Plan 5 £25,000 a year; deduction rate 9%; periodic threshold =
  annual threshold / number of periods; deductions are rounded down to the whole pound (HMRC payroll rules).
gov.uk/repaying-your-student-loan/what-you-pay: Plan 2 £29,385 (£2,448 a month), Plan 5 £25,000 (£2,083 a month);
  "9% of your income over the threshold"; worked examples round the monthly repayment down to the pound.
gov.uk/government/publications/student-loans-a-guide-to-terms-and-conditions/student-loans-a-guide-to-terms-and-conditions-2026-to-2027:
  Plan 2 = courses started 1 September 2012 to 31 July 2023; Plan 5 = undergraduate courses on or after 1 August
  2023 (England); Plan 2 cancelled 30 years, Plan 5 40 years after you're due to start repaying.
gov.uk/government/news/student-loans-interest-rates-and-repayment-threshold-announcement--7 (10 Aug 2026) and
gov.uk/guidance/how-interest-is-calculated-plan-2: 1 Sep 2026 - 31 Aug 2027 RPI 4.1%; Plan 5 = RPI (4.1%);
  Plan 2 after study = RPI at or below £29,385, rising on a sliding scale to RPI + 3% at £52,885, capped at 6%.
Assumptions: English student loans, paid monthly, £36,000 a year (£3,000 a month), no other income, both in
  repayment; Plan 2 sister started uni before 1 August 2023, Plan 5 sister in autumn 2023.
"""
from motion import *  # noqa: F401,F403
from brand import *  # noqa: F401,F403
import math

BRAND = True
COVER = dict(words=("SAME PAY", "£400 MORE?"), highlight=1, hero="Graduation cap", left="Woman", right="Girl",
             particles="Coin")

# ---- figures (gov.uk, checked 27 Oct 2026) ------------------------------------------------------------------
P2, P5 = 29_385, 25_000            # repayment thresholds from 6 April 2026
RATE = 0.09                        # 9% of income over the threshold, both plans
SALARY = 36_000                    # illustration: same salary for both sisters
MONTH = SALARY / 12
assert MONTH == 3_000


def monthly(threshold):  # HMRC payroll: periodic threshold rounded down to the penny, deduction to the pound
    pt = math.floor(threshold / 12 * 100) / 100
    return math.floor(max(0, MONTH - pt) * RATE)


M2, M5 = monthly(P2), monthly(P5)
Y2, Y5 = M2 * 12, M5 * 12
DIFF = Y5 - Y2
assert (M2, M5) == (49, 82) and (Y2, Y5) == (588, 984) and DIFF == 396
ANNUAL_DIFF = round((P2 - P5) * RATE, 2)          # same for any salary at or above the Plan 2 threshold
assert ANNUAL_DIFF == 394.65
assert 390 <= DIFF < 400 and 390 <= ANNUAL_DIFF < 400  # spoken: "almost £400"
assert round(P2, -3) == 29_000 and 29_000 < P2 < 30_000  # spoken: "nearly £30,000"
WRITE_OFF_2, WRITE_OFF_5 = 30, 40
assert WRITE_OFF_5 - WRITE_OFF_2 == 10              # spoken: "ten years longer"
RPI = 4.1
LOWER, UPPER = 29_385, 52_885                       # Plan 2 sliding-scale thresholds
I5 = RPI
I2 = round(min(6.0, RPI + 3 * (SALARY - LOWER) / (UPPER - LOWER)), 1)
assert I5 == 4.1 and I2 == 4.9 and I5 < I2          # spoken: "Her interest is a bit lower"

STAMP = "GOV.UK · 2026/27 STUDENT LOANS · CHECKED 27 OCT 2026"


def s_hook(L, t):  # sentence 0 · risk
    cover_hook(L, t, gbp(DIFF), sub="more a year, on the same pay", number_at=tk(0, "£400"),
               kicker="STUDENT LOANS · ENGLAND")


def s_same(L, t):  # sentence 1 · question: everything's the same
    beat(L, "SAME PAY", t, S(1) - 0.1)
    versus(L, t,
           dict(title="YOU", label="SALARY", value=gbp(SALARY), color=Wt, start=S(1), at=tk(1, "job."),
                tone=None, emoji="woman"),
           dict(title="YOUR SISTER", label="SALARY", value=gbp(SALARY), color=Wt, start=S(1) + 0.15,
                at=tk(1, "job."), tone=None, emoji="graduation_cap"),
           cy=620, h=300)
    chip(L, "SAME DEGREE", W / 2, 840, t, tk(1, "degree."), "white", 36, emoji="graduation_cap")
    chip(L, "SAME LOAN COMPANY", W / 2, 950, t, tk(1, "company."), "white", 36, emoji="bank")


def s_plan(L, t):  # sentence 2 · twist 1: she's on the newer plan
    beat(L, "twist", t, S(2) - 0.1)
    chip(L, "STARTED UNI · AUTUMN 2023", W / 2, 520, t, tk(2, "2023"), "cyan", 38, emoji="calendar")
    big_number(L, "PLAN 5", W / 2, 720, t, at=tk(2, "newer"), size=170, color=RED)
    chip(L, "YOURS: PLAN 2", W / 2, 900, t, tk(2, "plan."), "white", 36)


def s_maths(L, t):  # sentence 3 · answer: where repayments start
    beat(L, "maths", t, S(3) - 0.1, sub="9% OF PAY ABOVE THE LINE", sub_at=S(3))
    versus(L, t,
           dict(title="PLAN 5 · HER", label="STARTS AT", value=gbp(P5), color=RED, start=S(3),
                at=tk(3, "£25,000"), tone="red", emoji="woman"),
           dict(title="PLAN 2 · YOU", label="STARTS AT", value=gbp(P2), color=G, start=tk(3, "Yours"),
                at=tk(3, "£30,000"), tone="green", emoji="woman"),
           cy=600, h=300)
    chip(L, f"{gbp(M5)} vs {gbp(M2)} A MONTH ON {gbp(SALARY)}", W / 2, 830, t, tk(3, "£30,000") + 0.3,
         "white", 34, emoji="receipt")
    checked(L, STAMP, W / 2, 940, t, tk(3, "£30,000") + 0.6)


def s_catch(L, t):  # sentences 4-5 · rehook + question 2: what's left gets wiped
    beat(L, "catch", t, S(4) - 0.1)
    L.emoji("hourglass_done", W / 2, 560, 170, t, S(4), bounce=True)
    chip(L, "WHAT'S LEFT GETS WIPED", W / 2, 800, t, tk(5, "wiped."), "gold", 42, emoji="check_mark_button")


def s_years(L, t):  # sentence 6 · twist 2: ten years longer
    beat(L, "twist", t, S(6) - 0.1, sub="YEARS UNTIL IT'S WIPED", sub_at=S(6))
    bar_chart(L, t, S(6), [WRITE_OFF_2, WRITE_OFF_5], ["YOU · PLAN 2", "HER · PLAN 5"],
              (260, 500, 820, 960), [G, RED], dur=0.6, vmax=42,
              value_tags={0: (f"{WRITE_OFF_2} YEARS", G, tk(6, "thirty")),
                          1: (f"{WRITE_OFF_5} YEARS", RED, tk(6, "ten"))})
    chip(L, "+10 YEARS", W / 2, 1100, t, tk(6, "longer."), "red", 44, emoji="calendar")


def s_miss(L, t):  # sentence 7 · answer: lower interest, longer loan
    beat(L, "miss", t, S(7) - 0.1)
    value_card(L, W / 2, 560, 760, t, S(7), "chart_increasing", "HER INTEREST · PLAN 5", f"{I5}%",
               color=G, value_at=tk(7, "lower."))
    value_card(L, W / 2, 740, 760, t, tk(7, "interest"), "chart_increasing", "YOURS · PLAN 2", f"{I2}%",
               color=Wt, value_at=tk(7, "lower."))
    caveat(L, t, tk(7, "longer."), ["Interest from 1 Sep 2026, on £36,000 a year.",
                                    "England. Rules as at 27 Oct 2026. Not advice."], cy=900, size=26)


def s_loop(L, t):  # sentence 8: loop line back into sentence 0
    loop_close(L, t, 8, comment="FAIR OR NOT? COMMENT")


SCENES = [(0, 0), (1, 1), (2, 2), (3, 3), (4, 5), (6, 6), (7, 7), (8, 8)]
DRAW = [s_hook, s_same, s_plan, s_maths, s_catch, s_years, s_miss, s_loop]


def events():
    ev = [{"t": tk(0, "£400") + 0.05, "kind": "boom"},
          {"t": tk(2, "newer"), "kind": "boom"},
          {"t": tk(3, "£25,000"), "kind": "pop"},
          {"t": tk(3, "£30,000"), "kind": "pop"},
          {"t": tk(5, "wiped."), "kind": "coin"},
          {"t": tk(6, "ten"), "kind": "boom"},
          {"t": tk(7, "lower."), "kind": "coin"}]
    return scene_events(ev)
