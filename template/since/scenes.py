"""NNN: TODO topic — format: since (brand-v2; BRAND.md §1). (data checked DD Mon YYYY)

TODO the data series with its source (paste the values below with the URL); every assumption.
"""
from motion import *  # noqa: F401,F403
from brand import *  # noqa: F401,F403

BRAND = True
COVER = dict(words=("SINCE", "TODO"), highlight=1, hero="Hourglass not done", left="Calendar",
             right="Chart increasing", particles="Coin")

# ---- data + figures: paste the official series here, compute everything from it -------------------------
# YEARS = [...] ; VALUES = [...]  # source: TODO URL, checked DD Mon YYYY


def s_hook(L, t):  # sentence 0
    cover_hook(L, t, "TODO £X", sub="TODO sub-line", number_at=tk(0, "£"), kicker="TODO £1,000 IN YEAR")


def s_then(L, t):  # sentence 1
    beat(L, "then", t, S(1) - 0.1)
    # value_card(L, W / 2, 620, 860, t, S(1), "calendar", "TODO 2010", "£1,000", value_at=tk(1, "£"))


def s_path(L, t):  # sentences 2-3
    beat(L, "today", t, S(2) - 0.1)
    # line_chart(L, t, S(2), S(4) - S(2) - 0.3, [([(x, y) ...], G, 7)], (180, 520, 790, 980), xmax, ymax,
    #            x_labels=[...], y_labels=[...], end_tags=[(0, "£TODO", G, tk(3, "£"), 0)])


def s_compare(L, t):  # sentences 4-5
    beat(L, "twist", t, S(4) - 0.1)
    # versus(...) or bar_chart(...) against cash / inflation
    caveat(L, t, S(5), ["Past performance doesn't guarantee future returns.",
                        "General education, not financial advice."], cy=1120)


def s_loop(L, t):  # sentence 6
    loop_close(L, t, 6, comment="TODO TAKE-SIDES QUESTION, e.g. FAIR OR NOT? COMMENT")


SCENES = [(0, 0), (1, 1), (2, 3), (4, 5), (6, 6)]
DRAW = [s_hook, s_then, s_path, s_compare, s_loop]


def events():
    ev = [{"t": tk(0, "£") + 0.1, "kind": "coin"}]
    return scene_events(ev)
