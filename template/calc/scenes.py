"""NNN: TODO topic — format: calc (brand-v2; BRAND.md §1). (figures checked DD Mon YYYY)

TODO every official figure with its source; every assumption.
"""
from motion import *  # noqa: F401,F403
from brand import *  # noqa: F401,F403

BRAND = True
COVER = dict(words=("TODO", "TODO"), highlight=0, hero="£", left="TODO", right="TODO", particles="Coin")

# ---- figures: compute every number here; assert each one against the script's rounded text ------------
# TODO e.g. PA, TAPER_START = 12_570, 100_000 ; FULL_LOSS = TAPER_START + 2 * PA ; assert FULL_LOSS == 125_140


def s_hook(L, t):  # sentences 0-1
    cover_hook(L, t, "TODO £X", sub="TODO sub-line", number_at=tk(0, "£"), kicker="TODO SHORT CONTEXT LINE")


def s_maths(L, t):  # sentences 2-3
    beat(L, "maths", t, S(2) - 0.1)
    # timed_line(L, [("£100,000", Wt, tk(2, "£100,000")), ("+", M, tk(2, "£1")), ("£2", Wt, tk(2, "£2"))], W / 2, 560, 76, t)
    # a = panel(L, W / 2, 860, 760, 230, t, tk(3, "£") - 0.15, "green")
    # big_number(L, "TODO", W / 2, 880, t, tk(3, "£"), size=130, alpha=a)
    # checked(L, "GOV.UK · DD MON YYYY", W / 2, 1060, t, tk(3, "£") + 0.4)


def s_twist(L, t):  # sentence 4
    beat(L, "twist", t, S(4) - 0.1)  # or "catch"
    # value_card(...) / bar_chart(...) / versus(...)


def s_tip(L, t):  # sentences 5-6
    beat(L, "miss", t, S(5) - 0.1)
    # if the owner gave a take: take_card(L, t, 6, ["TODO her line,", "in two short lines"])
    # else: caveat(L, t, S(6), ["Illustration only.", "General education, not financial advice."], cy=1100)


def s_loop(L, t):  # sentence 7: the loop line, the picture rebuilds the cover
    loop_close(L, t, 7, comment="TODO SHORT QUESTION? COMMENT")


SCENES = [(0, 1), (2, 3), (4, 4), (5, 6), (7, 7)]
DRAW = [s_hook, s_maths, s_twist, s_tip, s_loop]


def events():
    ev = [{"t": tk(0, "£") + 0.1, "kind": "coin"}]  # TODO pops on numbers, "boom" on a catch
    return scene_events(ev)
