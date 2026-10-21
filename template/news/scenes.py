"""NNN: TODO topic — format: news (brand-v2; BRAND.md §1). (checked DD Mon YYYY against TODO official source)

TODO what changed, the official source URL and its date; every assumption in the worked example.
"""
from motion import *  # noqa: F401,F403
from brand import *  # noqa: F401,F403

BRAND = True
COVER = dict(words=("TODO", "TODO"), highlight=0, hero="Classical building", left="Calendar", right="Receipt",
             particles="Coin")

# ---- figures --------------------------------------------------------------------------------------------
# OLD, NEW = ..., ...  # source: TODO, announced DD Mon YYYY, takes effect DD Mon YYYY


def s_hook(L, t):  # sentence 0
    cover_hook(L, t, "TODO £X", sub="TODO from DD MONTH", number_at=tk(0, "£"), kicker="TODO WHAT CHANGES")


def s_changed(L, t):  # sentence 1
    beat(L, "changed", t, S(1) - 0.1)
    # versus(L, t, dict(title="BEFORE", value="£OLD", color=Wt, start=S(1)), dict(title="FROM DD MON", value="£NEW", ...))
    # checked(L, "GOV.UK · DD MON YYYY", W / 2, 1000, t, S(1) + 0.6)


def s_who(L, t):  # sentences 2-3
    beat(L, "who", t, S(2) - 0.1)
    # value_card(...) worked example with numbers


def s_means(L, t):  # sentence 4
    beat(L, "means", t, S(4) - 0.1)
    # what to check (education, not advice); take_card(...) if the owner gave a take


def s_loop(L, t):  # sentence 5
    loop_close(L, t, 5, comment="TODO SHORT QUESTION? COMMENT")


SCENES = [(0, 0), (1, 1), (2, 3), (4, 4), (5, 5)]
DRAW = [s_hook, s_changed, s_who, s_means, s_loop]


def events():
    ev = [{"t": tk(0, "£") + 0.1, "kind": "pop"}]
    return scene_events(ev)
