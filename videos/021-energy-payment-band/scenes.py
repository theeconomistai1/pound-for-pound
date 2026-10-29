"""Video 021 (brand-v2, format: news, told as the dopamine loop — BRAND.md §0c): Budget 2026's £100 Household
Energy Payment goes by council tax band, not income. (figures checked 29 Oct 2026)

Budget 2026 (HM Treasury, 28 Oct 2026), gov.uk/government/publications/budget-2026-document/budget-2026-html:
  "a £2.6 billion Household Energy Payment, which will provide a £100 payment ... from January 2027 for households
  in England in council tax bands A-D, supporting up to 20 million households"; "directly provided to up to 20
  million households via the Council Tax system"; "£100 million for English local authorities" to help households
  in bands above A-D; devolved governments get their share via the Barnett formula.
gov.uk/government/news/budget-2026-breathing-space-for-today-hope-for-the-future: "£100 Household Energy Payment
  ... up to 20 million households in bands A to D in England".
gov.uk/guidance/understand-how-council-tax-bands-are-assessed (VOA): England bands are based on the value at
  1 April 1991; band D £68,001 to £88,000, band E £88,001 to £120,000.
Assumptions: the payment as announced on 28 Oct 2026; delivery details are for the government and councils to
  confirm. Scotland, Wales and Northern Ireland get funding for similar support, not this payment.
"""
from motion import *  # noqa: F401,F403
from brand import *  # noqa: F401,F403

BRAND = True
COVER = dict(words=("£100", "BAND?"), highlight=0, hero="House with garden", left="Electric plug",
             right="Light bulb", particles="Coin")

# ---- figures (Budget 2026, HM Treasury, 28 Oct 2026; VOA) -------------------------------------------------
PAYMENT = 100                    # £ per household, bands A-D, England, from January 2027
HOUSEHOLDS = 20_000_000          # "up to 20 million households"
COST = 2_600_000_000             # £2.6bn in total (includes devolved share via Barnett)
COUNCIL_FUND = 100_000_000       # £100m for councils to help households above band D
VALUATION_YEAR = 1991            # England bands use values at 1 April 1991
BAND_D_TOP, BAND_E_TOP = 88_000, 120_000
assert gbp(PAYMENT) == "£100"                             # spoken: "£100" (three times)
assert f"{HOUSEHOLDS // 1_000_000} million" == "20 million"  # spoken: "20 million"
assert str(VALUATION_YEAR) == "1991"                      # spoken: "1991"
assert PAYMENT * HOUSEHOLDS <= COST                       # £2bn of payments within the £2.6bn package
assert BAND_D_TOP < BAND_E_TOP

STAMP = "GOV.UK · BUDGET 2026 · CHECKED 29 OCT 2026"
STAMP_VOA = "GOV.UK · VOA BANDS · CHECKED 29 OCT 2026"


def s_hook(L, t):  # sentence 0 · risk
    cover_hook(L, t, gbp(PAYMENT), sub="for 20 million homes, from January", number_at=tk(0, "£100"),
               kicker="BUDGET 2026 · ENGLAND")


def s_changed(L, t):  # sentence 1 · question: who gets it
    beat(L, "changed", t, S(1) - 0.1, sub="HOUSEHOLD ENERGY PAYMENT", sub_at=S(1) + 0.2)
    L.emoji("house", W / 2, 520, 160, t, S(1), bounce=True)
    L.text("COUNCIL TAX BANDS", W / 2, 690, 46, M, ramp(t, tk(1, "council"), 0.3), weight="ExtraBold")
    for i, b in enumerate("ABCD"):
        chip(L, b, 330 + i * 140, 800, t, tk(1, "bands") + 0.1 * i, "green", 64)
    chip(L, "E · F · G · H", W / 2, 920, t, tk(1, "D.") + 0.2, "red", 40, emoji="cross_mark")
    checked(L, STAMP, W / 2, 1040, t, tk(1, "England") + 0.2)


def s_twist(L, t):  # sentence 2 · twist 1: it goes by band
    beat(L, "twist", t, S(2) - 0.1)
    chip(L, "YOUR INCOME", W / 2, 480, t, tk(2, "income."), "red", 52, emoji="briefcase")
    chip(L, "YOUR ENERGY BILL", W / 2, 620, t, tk(2, "bill."), "red", 52, emoji="light_bulb")
    a = ramp(t, tk(2, "Just"), 0.3)
    L.text("JUST", W / 2, 770, 46, M, a, weight="ExtraBold")
    big_number(L, "YOUR BAND", W / 2, 890, t, at=tk(2, "band."), size=130)


def s_1991(L, t):  # sentences 3-4 · rehook + question 2: the band is from 1991
    beat(L, "who", t, S(3) - 0.1, sub="AND HERE'S THE STRANGE PART", sub_at=S(3) + 0.2)
    L.emoji("thinking_face", W / 2, 520, 150, t, S(3), bounce=True)
    L.text("YOUR HOME'S VALUE IN", W / 2, 680, 44, M, ramp(t, tk(4, "worth"), 0.3), weight="ExtraBold")
    big_number(L, "1991", W / 2, 810, t, at=tk(4, "1991"), size=180)
    chip(L, "BAND D = UP TO £88,000 THEN", W / 2, 960, t, tk(4, "1991") + 0.4, "white", 36, emoji="calendar")
    checked(L, STAMP_VOA, W / 2, 1070, t, tk(4, "1991") + 0.7)


def s_who(L, t):  # sentences 5-6 · twist 2 + answer: small flat vs band E family
    beat(L, "means", t, S(5) - 0.1)
    versus(L, t,
           dict(title="SMALL FLAT", label="BIG EARNER", value=gbp(PAYMENT), color=G, start=S(5),
                at=tk(5, "£100"), tone="green", emoji="man"),
           dict(title="BAND E HOUSE", label="FAMILY", value="£0", color=RED, start=tk(6, "family"),
                at=tk(6, "nothing"), tone="red", emoji="woman"),
           cy=640, h=320)
    chip(L, "UNLESS THE COUNCIL HELPS", W / 2, 890, t, tk(6, "unless"), "gold", 40, emoji="shield")
    caveat(L, t, tk(6, "unless") + 0.3, ["Councils get £100 million to help homes above",
                                         "band D. Not advice."], cy=1000, size=26)


def s_loop(L, t):  # sentence 7: loop line back into sentence 0
    loop_close(L, t, 7, comment="FAIR OR NOT? COMMENT")


SCENES = [(0, 0), (1, 1), (2, 2), (3, 4), (5, 6), (7, 7)]
DRAW = [s_hook, s_changed, s_twist, s_1991, s_who, s_loop]


def events():
    ev = [{"t": tk(0, "£100") + 0.05, "kind": "coin"},
          {"t": tk(1, "bands"), "kind": "pop"},
          {"t": tk(2, "band."), "kind": "boom"},
          {"t": tk(4, "1991"), "kind": "pop"},
          {"t": tk(5, "£100"), "kind": "coin"},
          {"t": tk(6, "nothing"), "kind": "boom"}]
    return scene_events(ev)
