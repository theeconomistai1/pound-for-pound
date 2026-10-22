"""Video 008 (brand-v2, format: calc): relief at source — £80 paid into a pension becomes £100, the extra a
higher-rate taxpayer claims back, and the £2,880 / £3,600 rule for people with no earnings.
(figures checked 22 Oct 2026, tax year 2026/27, England, Wales and Northern Ireland; Scotland differs)

gov.uk/tax-on-your-private-pension/pension-tax-relief: relief at source in all personal and stakeholder
  pensions and some workplace pensions; higher and additional rate taxpayers claim extra relief (20% on income
  taxed at 40%, 25% on income taxed at 45%) through Self Assessment; non-taxpayers get 20% relief on up to
  £2,880 if they have no earnings; relief on contributions up to 100% of annual earnings.
gov.uk/hmrc-internal-manuals/pensions-tax-manual/ptm044220: member pays £80 net, the scheme claims £20 from
  HMRC, £100 in total; a 40% taxpayer claims the remaining £20 from HMRC.
gov.uk/hmrc-internal-manuals/pensions-tax-manual/ptm044100: the "basic amount" is £3,600 (s190 FA 2004).
gov.uk/income-tax-rates: basic rate 20%, higher rate 40% (£50,271-£125,140), additional rate 45%.
gov.uk/guidance/claim-tax-relief-on-your-private-pension-payments: higher rate taxpayers claim the extra
  (online or by tax return) — it is not added automatically.
"""
from motion import *  # noqa: F401,F403
from brand import *  # noqa: F401,F403

BRAND = True
COVER = dict(words=("£80 IS", "£100"), highlight=1, hero="Jar", fill="Coin", left="Hourglass not done",
             right="Old woman", particles="Coin")

# ---- figures (2026/27, rUK) --------------------------------------------------------------------------------
BASIC, HIGHER, ADDITIONAL = 0.20, 0.40, 0.45
BASIC_AMOUNT = 3_600                      # gross contribution that gets relief with no earnings (PTM044100)

GROSS = 100
PAID = round(GROSS * (1 - BASIC))         # what leaves your account (net of basic-rate relief)
ADDED = GROSS - PAID                      # claimed by the provider
assert (GROSS, PAID, ADDED) == (100, 80, 20)
SHARE_OF_POT = round(ADDED / GROSS * 100)   # 20% of the pot
TOP_UP = round(ADDED / PAID * 100)          # 25% on what you paid
assert (SHARE_OF_POT, TOP_UP) == (20, 25)

EXTRA_HIGHER = round(GROSS * (HIGHER - BASIC))        # claimed back by a 40% taxpayer
COST_HIGHER = PAID - EXTRA_HIGHER
assert (EXTRA_HIGHER, COST_HIGHER) == (20, 60)
EXTRA_ADD = round(GROSS * (ADDITIONAL - BASIC))       # comment-question answer: 25 -> costs £55 (not shown)
assert PAID - EXTRA_ADD == 55

NO_EARN_PAID = round(BASIC_AMOUNT * (1 - BASIC))
NO_EARN_ADDED = BASIC_AMOUNT - NO_EARN_PAID
assert (NO_EARN_PAID, NO_EARN_ADDED) == (2_880, 720)

STAMP = "GOV.UK · PENSION TAX RELIEF · CHECKED 22 OCT 2026"


def s_hook(L, t):  # sentences 0-1
    cover_hook(L, t, gbp(GROSS), sub=f"from {gbp(PAID)} you pay in", number_at=tk(0, "£100"),
               kicker="RELIEF AT SOURCE",
               extra=lambda L, t: chip(L, f"+{gbp(ADDED)} BASIC RATE TAX RELIEF", W / 2, 1170, t, tk(1, "£20"),
                                       "green", 32, emoji="coin"))


def s_maths(L, t):  # sentences 2-3
    beat(L, "maths", t, S(2) - 0.1)
    bar_chart(L, t, S(2), [PAID, GROSS], ["YOU PAY", "IN YOUR POT"], (260, 470, 820, 820), [Wt, G], dur=0.6,
              value_tags={0: (gbp(PAID), Wt, S(2) + 0.3), 1: (gbp(GROSS), G, tk(2, "£100"))})
    timed_line(L, [(gbp(ADDED), C, tk(2, "£20")), ("IS", M, tk(2, "20%")), (f"{SHARE_OF_POT}%", G, tk(2, "20%")),
                   ("OF £100", M, tk(2, "20%"))], W / 2, 960, 64, t)
    timed_line(L, [(gbp(ADDED), C, tk(3, "£80")), ("IS", M, tk(3, "25%")), (f"{TOP_UP}%", G, tk(3, "25%")),
                   ("ON £80", M, tk(3, "25%"))], W / 2, 1060, 64, t)
    checked(L, STAMP, W / 2, 1170, t, tk(3, "25%") + 0.4)


def s_twist(L, t):  # sentence 4
    beat(L, "twist", t, S(4) - 0.1, sub=f"WHAT {gbp(GROSS)} IN YOUR PENSION COSTS", sub_at=S(4) + 0.2)
    versus(L, t,
           dict(title="20% TAXPAYER", label="RELIEF AT SOURCE", value=gbp(PAID), color=Wt,
                start=S(4), at=S(4) + 0.3, emoji="receipt"),
           dict(title="40% TAXPAYER", label=f"+{gbp(EXTRA_HIGHER)} CLAIMED BACK", value=gbp(COST_HIGHER), color=G,
                start=tk(4, "Claim"), at=tk(4, "£60"), tone="green", emoji="briefcase"),
           cy=640, h=380)
    chip(L, f"40% TAX = {round(HIGHER * 100)}% RELIEF IN TOTAL", W / 2, 950, t, tk(4, "£60") + 0.3, "cyan", 30)
    checked(L, "GOV.UK · 2026/27 RATES · CHECKED 22 OCT 2026", W / 2, 1060, t, tk(4, "£60") + 0.5)


def s_miss(L, t):  # sentences 5-6
    beat(L, "miss", t, S(5) - 0.1)
    chip(L, "NOT AUTOMATIC: CLAIM IT YOURSELF", W / 2, 440, t, tk(5, "automatic"), "red", 32, emoji="warning")
    value_card(L, W / 2, 620, 880, t, S(6), "old_woman", "NO EARNINGS? YOU PAY IN", gbp(NO_EARN_PAID), color=Wt,
               value_at=tk(6, "£2,880"), h=140, sub="the most a year")
    value_card(L, W / 2, 785, 880, t, tk(6, "£2,880") + 0.3, "wrapped_gift", "TAX RELIEF ADDED",
               "+" + gbp(NO_EARN_ADDED), color=G, value_at=tk(6, "£720"), h=140, sub="20% basic rate")
    pa = ramp(t, tk(6, "added") - 0.1, 0.25)
    L.text("IN YOUR PENSION", W / 2, 910, 28, M, pa, weight="ExtraBold")
    if pa > 0:
        big_number(L, gbp(BASIC_AMOUNT), W / 2, 1000, t, tk(6, "added"), size=110, alpha=pa)
    checked(L, STAMP, W / 2, 1110, t, tk(6, "added") + 0.3)
    caveat(L, t, tk(6, "added") + 0.5, ["2026/27, England, Wales & NI. General education, not advice."],
           cy=1200, size=26)


def s_loop(L, t):  # sentence 7: the loop line, the picture rebuilds the cover
    loop_close(L, t, 7, comment="45% TAX: £100 COSTS? COMMENT")


SCENES = [(0, 1), (2, 3), (4, 4), (5, 6), (7, 7)]
DRAW = [s_hook, s_maths, s_twist, s_miss, s_loop]


def events():
    ev = [{"t": tk(0, "£100") + 0.05, "kind": "coin"},
          {"t": tk(1, "£20"), "kind": "pop"},
          {"t": tk(2, "20%"), "kind": "pop"}, {"t": tk(3, "25%"), "kind": "pop"},
          {"t": tk(4, "£60"), "kind": "coin"},
          {"t": tk(5, "automatic"), "kind": "boom"},
          {"t": tk(6, "£2,880"), "kind": "pop"}, {"t": tk(6, "£720"), "kind": "coin"}]
    return scene_events(ev)
