"""NNN: TODO topic — format: myth (brand-v2; BRAND.md §1). (figures checked DD Mon YYYY)

TODO every official figure with its source; every assumption.
"""
from motion import *  # noqa: F401,F403
from brand import *  # noqa: F401,F403

BRAND = True
COVER = dict(words=("TODO", "MYTH"), highlight=1, hero="TODO", left="TODO", right="TODO", particles="Coin")

# ---- figures --------------------------------------------------------------------------------------------
# TODO


def s_hook(L, t):  # sentence 0
    cover_hook(L, t, "TODO £X", sub="TODO sub-line", number_at=tk(0, "£"), kicker="TODO THE CLAIM")


def s_myth(L, t):  # sentence 1: the myth as people say it, then the stamp
    beat(L, "myth", t, S(1) - 0.1)
    L.text("“TODO THE CLAIM”", W / 2, 600, 58, Wt, ramp(t, S(1), 0.3))
    verdict_stamp(L, "MYTH", W / 2, 820, t, S(1) + 0.9, "red")


def s_truth(L, t):  # sentences 2-3
    beat(L, "truth", t, S(2) - 0.1)
    # timed_line(...) / value_card(...) with the real numbers; checked(L, "GOV.UK · DD MON YYYY", W / 2, 1100, t, ...)


def s_exception(L, t):  # sentences 4-5
    beat(L, "catch", t, S(4) - 0.1)
    # the exception where the claim IS true, with its number; then what to check
    # take_card(L, t, 5, [...]) if the owner gave a take


def s_loop(L, t):  # sentence 6
    loop_close(L, t, 6, comment="TODO SHORT QUESTION? COMMENT")


SCENES = [(0, 0), (1, 1), (2, 3), (4, 5), (6, 6)]
DRAW = [s_hook, s_myth, s_truth, s_exception, s_loop]


def events():
    ev = [{"t": S(1) + 0.9, "kind": "boom"}]  # the stamp
    return scene_events(ev)
