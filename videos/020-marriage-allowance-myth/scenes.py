"""Video 020 (brand-v2, format: myth, told as the dopamine loop — BRAND.md §0c): "Marriage Allowance is just
for low earners." (figures checked 28 Oct 2026)

gov.uk/marriage-allowance (updated 30 Sep 2026): transfer £1,260 of your Personal Allowance to your husband, wife
  or civil partner; "This reduces their tax by up to £252 in the tax year"; you must normally have income below
  your Personal Allowance (usually £12,570); your partner must pay basic-rate Income Tax, "usually ... between
  £12,571 and £50,270" (Scotland: starter, basic or intermediate rate, £12,571 to £43,662); living together
  without being married or in a civil partnership doesn't qualify; "You can backdate your claim to 6 April 2022
  (the 2022 to 2023 tax year)".
taxconfident.campaign.gov.uk/working-life/life-changes/marriage-allowance (HMRC): "You can backdate your claim as
  far back as the last four years"; "up to £252 a year".
gov.uk/income-tax-rates (updated 1 Oct 2026): Personal Allowance £12,570 in 2026/27; and
gov.uk/government/publications/income-tax-personal-allowance-and-the-basic-rate-limit-from-6-april-2022-to-5-april-2026:
  £12,570 in every year 2022/23 to 2025/26, so the transfer (10% of the allowance) is £1,260 in each year.
Assumptions: the lower earner had income below the Personal Allowance and the partner was a basic-rate taxpayer in
  every year claimed; the "up to £1,260" is the maximum over five tax years (2022/23 backdated to 2026/27); under
  the four-year limit, 2022/23 can't be claimed after 5 April 2027. Rules as at 28 Oct 2026 (Budget day: rules
  for later years could change).
"""
from motion import *  # noqa: F401,F403
from brand import *  # noqa: F401,F403
import math

BRAND = True
COVER = dict(words=("MARRIED?", "£1,260"), highlight=1, hero="Ring", left="Woman", right="Man",
             particles="Coin")

# ---- figures (gov.uk / HMRC, checked 28 Oct 2026) ---------------------------------------------------------
PA = 12_570                      # Personal Allowance, 2022/23 to 2026/27 (frozen)
TRANSFER = PA // 10              # Marriage Allowance = 10% of the Personal Allowance, rounded up to £10
assert TRANSFER == 1_257 and math.ceil(PA / 10 / 10) * 10 == 1_260
TRANSFER = 1_260                 # gov.uk figure
BASIC = 0.20                     # tax reducer at the basic rate
PER_YEAR = round(TRANSFER * BASIC)
assert PER_YEAR == 252                                    # spoken: "up to £252 a year"
HIGHER_LIMIT = 50_270            # partner's income limit, England, Wales and NI (basic rate)
SCOT_LIMIT = 43_662              # Scotland (starter, basic or intermediate rate)
assert round(HIGHER_LIMIT, -3) == 50_000                  # spoken: "up to about £50,000"
YEARS = ["2022/23", "2023/24", "2024/25", "2025/26", "2026/27"]   # backdate to 6 April 2022 + this year
assert len(YEARS) == 5 and YEARS[0].startswith("2022")    # spoken: "April 2022"
TOTAL = PER_YEAR * len(YEARS)
assert TOTAL == 1_260                                     # spoken: "up to £1,260" (twice)
OLDEST_DEADLINE = "5 APR 2027"   # four-year limit: 2022/23 (ended 5 Apr 2023) + 4 years

STAMP = "GOV.UK · MARRIAGE ALLOWANCE · CHECKED 28 OCT 2026"
STAMP_HMRC = "HMRC · BACKDATE UP TO 4 YEARS · CHECKED 28 OCT 2026"


def s_hook(L, t):  # sentence 0 · risk
    cover_hook(L, t, gbp(TOTAL), sub="you could be owed, as a couple", number_at=tk(0, "£1,260"),
               kicker="MARRIAGE ALLOWANCE · UK")


def s_myth(L, t):  # sentence 1 · question: the claim
    beat(L, "myth", t, S(1) - 0.1)
    a = ramp(t, S(1) + 0.1, 0.3)
    L.emoji("ring", W / 2, 490, 150, t, S(1), bounce=True)
    L.text("“It's just for", W / 2, 660, 64, Wt, a)
    L.text("low earners”", W / 2, 745, 64, Wt, a)
    verdict_stamp(L, "MYTH", W / 2, 930, t, tk(1, "earners.") + 0.15, "red", size=120)


def s_truth(L, t):  # sentence 2 · twist 1: the partner can earn far more
    beat(L, "truth", t, S(2) - 0.1, sub="YOUR PARTNER CAN EARN UP TO", sub_at=S(2) + 0.2)
    L.emoji("man", W / 2, 520, 140, t, S(2), bounce=True)
    big_number(L, gbp(HIGHER_LIMIT), W / 2, 720, t, at=tk(2, "£50,000"), size=170, color=G)
    chip(L, "A BASIC-RATE TAXPAYER", W / 2, 880, t, tk(2, "£50,000") + 0.3, "white", 36, emoji="briefcase")
    checked(L, STAMP, W / 2, 990, t, tk(2, "£50,000") + 0.6)


def s_how(L, t):  # sentence 3 · answer: you hand over part of your allowance
    beat(L, "truth", t, S(3) - 0.1, sub="HOW IT WORKS", sub_at=S(3) + 0.2)
    versus(L, t,
           dict(title="YOU", label="EARN UNDER", value=gbp(PA), color=Wt, start=S(3), at=tk(3, "allowance?"),
                tone=None, emoji="woman"),
           dict(title="YOUR PARTNER", label="TAX CUT, UP TO", value=gbp(PER_YEAR), color=G,
                start=tk(3, "Their"), at=tk(3, "£252"), tone="green", emoji="man"),
           cy=620, h=300)
    chip(L, "EVERY TAX YEAR", W / 2, 850, t, (tk(3, "£252") + 0.4), "gold", 40, emoji="calendar")
    caveat(L, t, (tk(3, "£252") + 0.4) + 0.2, ["Married or civil partners only. Scotland: partner",
                                       "up to £43,662. Not advice."], cy=960, size=26)


def s_miss(L, t):  # sentences 4-5 · rehook + question 2: the years you never claimed
    beat(L, "catch", t, S(4) - 0.1, sub="THE PART COUPLES MISS", sub_at=S(4) + 0.2)
    L.emoji("hourglass_done", W / 2, 560, 170, t, S(4), bounce=True)
    chip(L, "NEVER CLAIMED?", W / 2, 790, t, tk(5, "Never"), "white", 48, emoji="thinking_face")
    chip(L, "MISSED YEARS: TOO LATE?", W / 2, 900, t, tk(5, "late."), "red", 42, emoji="cross_mark")


def s_back(L, t):  # sentence 6 · twist 2: backdate to April 2022
    beat(L, "twist", t, S(6) - 0.1, sub="BACKDATE YOUR CLAIM TO", sub_at=S(6) + 0.2)
    big_number(L, "6 APRIL 2022", W / 2, 560, t, at=tk(6, "2022"), size=120, color=G)
    for i, y in enumerate(YEARS):
        cx = 170 + i * 185
        st = tk(6, "backdate") + 0.12 * i
        chip(L, y, cx, 760, t, st, "green" if i < 4 else "white", 28)
    L.text("4 PAST YEARS + THIS ONE", W / 2, 860, 34, M, ramp(t, tk(6, "2022"), 0.3), weight="ExtraBold")
    checked(L, STAMP_HMRC, W / 2, 970, t, tk(6, "2022") + 0.4)


def s_total(L, t):  # sentence 7 · answer: up to £1,260, and the oldest year goes
    beat(L, "miss", t, S(7) - 0.1)
    L.text("5 TAX YEARS AT UP TO £252", W / 2, 470, 40, M, ramp(t, S(7), 0.3), weight="ExtraBold")
    big_number(L, gbp(TOTAL), W / 2, 610, t, at=tk(7, "£1,260"), size=190, color=G)
    chip(L, f"2022/23 GOES AFTER {OLDEST_DEADLINE}", W / 2, 810, t, tk(7, "After"), "red", 38,
         emoji="alarm_clock")
    caveat(L, t, tk(7, "oldest"), ["If you qualified in each year. Rules as at",
                                   "28 Oct 2026 (Budget day). Not advice."], cy=930, size=26)


def s_loop(L, t):  # sentence 8: loop line back into sentence 0
    loop_close(L, t, 8, comment="FAIR OR NOT? COMMENT")


SCENES = [(0, 0), (1, 1), (2, 2), (3, 3), (4, 5), (6, 6), (7, 7), (8, 8)]
DRAW = [s_hook, s_myth, s_truth, s_how, s_miss, s_back, s_total, s_loop]


def events():
    ev = [{"t": tk(0, "£1,260") + 0.05, "kind": "coin"},
          {"t": tk(1, "earners.") + 0.15, "kind": "boom"},
          {"t": tk(2, "£50,000"), "kind": "pop"},
          {"t": tk(3, "£252"), "kind": "coin"},
          {"t": tk(5, "late."), "kind": "boom"},
          {"t": tk(6, "2022"), "kind": "pop"},
          {"t": tk(7, "£1,260"), "kind": "coin"},
          {"t": tk(7, "After"), "kind": "boom"}]
    return scene_events(ev)
