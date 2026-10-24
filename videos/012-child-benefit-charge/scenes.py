"""Video 012 (brand-v2, format: calc, told as the dopamine loop — BRAND.md §0c): the High Income Child Benefit
Charge — one parent on £80,000 pays back all the Child Benefit; two parents on £50,000 each keep it all; and
stopping the claim loses National Insurance credits. (figures checked 24 Oct 2026)

gov.uk/child-benefit/what-youll-get: £27.05 a week for the eldest or only child, £17.90 a week for each
  additional child (2026/27 rates).
gov.uk/child-benefit-tax-charge: you may pay the charge if your (or your partner's) adjusted net income is over
  £60,000 (tax years from 2024 to 2025); 1% of your Child Benefit for every £200 over £60,000; over £80,000
  you pay it all back. If both partners are over, whoever has the higher income pays.
gov.uk/child-benefit-tax-charge/stop-child-benefit: opting out of payments keeps you registered, so you still get
  National Insurance credits, which count towards your State Pension.
gov.uk/child-benefit: NI credits come automatically if you claim Child Benefit and your child is under 12;
  "If you choose not to get Child Benefit payments, you should still make a claim to get the other advantages."
Assumptions: a year = 52 weeks; "earn" = adjusted net income; the neighbours each have £50,000 adjusted net
  income; the parent at home has a child under 12 and doesn't earn enough to pay NI.
"""
from motion import *  # noqa: F401,F403
from brand import *  # noqa: F401,F403

BRAND = True
COVER = dict(words=("CHILD", "BENEFIT?"), highlight=1, hero="Baby", left="Receipt", right="Warning",
             particles="Coin")

# ---- figures (gov.uk, checked 24 Oct 2026) -----------------------------------------------------------------
ELDEST_WK, OTHER_WK = 27.05, 17.90       # Child Benefit, £ a week, 2026/27
START, FULL = 60_000, 80_000              # HICBC: starts over £60,000, all paid back over £80,000
STEP = 200                                # 1% of the benefit for every £200 over £60,000
WEEKS = 52

TWO_KIDS_WK = ELDEST_WK + OTHER_WK
TWO_KIDS = TWO_KIDS_WK * WEEKS
assert round(TWO_KIDS_WK, 2) == 44.95
assert round(TWO_KIDS, 2) == 2_337.40
assert 2_300 < TWO_KIDS < 2_400                       # "over £2,300"
assert START + 100 * STEP == FULL                     # 100 steps of 1% = all of it at £80,000


def charge(income, benefit):
    pct = min(100, max(0, (income - START) // STEP))  # whole £200 steps over the threshold
    return benefit * pct / 100


assert charge(80_000, TWO_KIDS) == TWO_KIDS           # one earner on £80,000: all goes back
NEXT_DOOR = (50_000, 50_000)
assert sum(NEXT_DOOR) == 100_000                      # "£100,000 together"
assert all(charge(x, TWO_KIDS) == 0 for x in NEXT_DOOR)  # "keep every penny": neither is over £60,000
assert all(x == sum(NEXT_DOOR) / 2 < START for x in NEXT_DOOR)  # "two on half each never cross it"
EXTRA_PER_200 = TWO_KIDS / 100                        # description: each £200 over costs £23.37 with two kids
assert round(EXTRA_PER_200, 2) == 23.37
assert round(charge(70_000, TWO_KIDS), 2) == 1_168.70  # description: halfway, £70,000 -> half back

STAMP = "GOV.UK · 2026/27 RATES · CHECKED 24 OCT 2026"


def s_hook(L, t):  # sentence 0 · risk
    cover_hook(L, t, gbp(FULL), sub="and all your Child Benefit goes back", number_at=tk(0, "£80,000"),
               kicker="THIS TAX YEAR, 2026/27")


def s_cost(L, t):  # sentence 1 · risk: the stake
    beat(L, "THE STAKE", t, S(1) - 0.1, tone="red")
    L.emoji("baby", W / 2 - 90, 520, 150, t, tk(1, "Two"), bounce=True)
    L.emoji("baby", W / 2 + 90, 520, 150, t, tk(1, "Two") + 0.15, bounce=True)
    L.text("CHILD BENEFIT, TWO KIDS", W / 2, 680, 40, M, ramp(t, tk(1, "That's"), 0.25), weight="ExtraBold")
    big_number(L, gbp(round(TWO_KIDS)), W / 2, 800, t, at=tk(1, "£2,300"), size=150, color=G)
    L.text("A YEAR", W / 2, 920, 40, Wt, ramp(t, tk(1, "year."), 0.25))
    checked(L, STAMP, W / 2, 1020, t, tk(1, "£2,300") + 0.4)


def s_next_door(L, t):  # sentences 2-3 · question 1: how do they keep it?
    beat(L, "THE NEIGHBOURS", t, S(2) - 0.1)
    versus(L, t,
           dict(title="YOU", label="ONE EARNER: £80,000", value="£0", color=RED, start=S(2),
                at=tk(2, "keep"), tone="red", emoji="man"),
           dict(title="NEXT DOOR", label="£50,000 + £50,000", value=gbp(round(TWO_KIDS)), color=G,
                start=tk(2, "two"), at=tk(2, "all."), tone="green", emoji="woman"),
           cy=600, h=340)
    L.text("CHILD BENEFIT KEPT", W / 2, 810, 34, M, ramp(t, tk(2, "keep"), 0.25), weight="ExtraBold")
    a = ramp(t, tk(3, "Wait"), 0.2)
    if a > 0:
        L.emoji("thinking_face", W / 2, 960, 130, t, tk(3, "Wait"), bounce=True)
        L.text("WAIT, HOW?", W / 2, 1100, 56, Wt, a, weight="Black")


def s_twist(L, t):  # sentences 4-5 · twist 1: it's each parent, not the household
    beat(L, "twist", t, S(4) - 0.1)
    chip(L, "EACH PARENT, NOT THE HOUSEHOLD", W / 2, 450, t, tk(4, "each"), "gold", 38, emoji="warning")
    L.text("THE CHARGE STARTS AT", W / 2, 570, 38, M, ramp(t, tk(5, "starts"), 0.25), weight="ExtraBold")
    big_number(L, gbp(START), W / 2, 680, t, at=tk(5, "£60,000"), size=140, color=Wt)
    chip(L, "ONE INCOME, NOT TWO ADDED", W / 2, 800, t, tk(5, "£60,000") + 0.3, "white", 30)
    chip(L, "PARENT 1: £50,000", W / 2 - 200, 890, t, tk(5, "half"), "green", 28, emoji="check_mark_button")
    chip(L, "PARENT 2: £50,000", W / 2 + 170, 890, t, tk(5, "half") + 0.15, "green", 28,
         emoji="check_mark_button")
    checked(L, "GOV.UK · CHILD BENEFIT CHARGE · CHECKED 24 OCT 2026", W / 2, 1010,
            t, tk(5, "never"))
    caveat(L, t, tk(5, "cross"), ["1% back for every £200 over £60,000. All of it over £80,000."], cy=1100, size=26)


def s_mistake(L, t):  # sentences 6-7 · rehook + question 2: the "fix"
    beat(L, "THE BIGGER MISTAKE", t, S(6) - 0.1, tone="red")
    L.emoji("cross_mark", W / 2, 540, 180, t, tk(7, "stop"), bounce=True)
    chip(L, "STOP CLAIMING?", W / 2, 740, t, tk(7, "stop"), "red", 56)
    L.text("TO DODGE THE CHARGE", W / 2, 860, 40, M, ramp(t, tk(7, "dodge"), 0.25), weight="ExtraBold")


def s_credits(L, t):  # sentence 8 · twist 2: the State Pension cost
    beat(L, "miss", t, S(8) - 0.1)
    L.emoji("old_woman", W / 2, 520, 170, t, tk(8, "parent"), bounce=True)
    chip(L, "NATIONAL INSURANCE CREDITS LOST", W / 2, 700, t, tk(8, "loses"), "red", 36, emoji="warning")
    L.text("THEY COUNT TOWARDS THE STATE PENSION", W / 2, 800, 34, Wt, ramp(t, tk(8, "State"), 0.25))
    checked(L, "GOV.UK · CHILD BENEFIT · CHECKED 24 OCT 2026", W / 2, 900, t, tk(8, "State") + 0.3)
    caveat(L, t, tk(8, "Pension.") - 0.2, ["Opting out of payments keeps you registered, and the credits.",
                                          "Child under 12. General education, not financial advice."],
           cy=1000, size=24)


def s_loop(L, t):  # sentence 9: loop line back into sentence 0
    loop_close(L, t, 9, comment="FAIR OR NOT? COMMENT")


SCENES = [(0, 0), (1, 1), (2, 3), (4, 5), (6, 7), (8, 8), (9, 9)]
DRAW = [s_hook, s_cost, s_next_door, s_twist, s_mistake, s_credits, s_loop]


def events():
    ev = [{"t": tk(0, "£80,000") + 0.05, "kind": "boom"},
          {"t": tk(1, "£2,300"), "kind": "pop"},
          {"t": tk(2, "all."), "kind": "coin"},
          {"t": tk(4, "each"), "kind": "boom"},
          {"t": tk(5, "£60,000"), "kind": "pop"},
          {"t": tk(6, "bigger"), "kind": "boom"},
          {"t": tk(8, "loses"), "kind": "boom"}]
    return scene_events(ev)
