"""NNN: TODO one-line topic — brand-v1 template (see BRAND.md, worked example samples/005-penny-challenge).
(figures checked DD Mon YYYY)

TODO: every official figure with its source, e.g.
ISA allowance 2026/27: £20,000 a year (gov.uk/individual-savings-accounts, checked 20 Oct 2026).
TODO: every assumption, e.g. 7% a year after fees, compounded monthly.
"""
from motion import *  # noqa: F401,F403
from brand import *  # noqa: F401,F403

BRAND = True  # renders with the locked brand frame, captions and loop

# Cover = frame 0 and the loop target: 1-2 words (highlight the one that carries the hook) over a scene that
# fits the subject. Objects are Fluent emoji folder names (BRAND.md §3). No "$" objects (Money bag etc.).
COVER = dict(words=("TODO", "TODO"), highlight=0, hero="£", left="TODO e.g. Calendar", right="TODO e.g. Coin",
             particles="Coin")  # optional: fill="Coin" (fills a hero container such as "Jar"), env="plain"

# ---- figures: compute every number shown or said here, never by hand -----------------------------------
# TODO e.g.
# TOTAL = ...
# assert f"{TOTAL:,.2f}" == "667.95"   # pin each spoken number to the script so a wrong figure cannot ship


def gbp2(v):
    return f"£{v:,.2f}"


# ---- scenes: one per beat. Sentence indices match spec.json -----------------------------------------------
def s_hook(L, t):
    # Frame 0 = the clean cover. After 0.45 s the scene dims, the cover words move up and the payoff lands.
    cover_hook(L, t, "£TODO", sub="TODO short sub-line", number_at=tk(0, "£"), kicker="TODO SHORT CONTEXT LINE",
               extra=lambda L, t: chip(L, "TODO OPEN LOOP", W / 2, 1180, t, S(1), "red", 30, emoji="warning"))


def s_example(L, t):
    beat(L, "example", t, S(2) - 0.1)
    # TODO e.g. value cards, a versus, or a small chart. Each element on its word:
    # value_card(L, W / 2, 520, 860, t, tk(2, "Day") - 0.1, "calendar", "DAY 1", "1p", value_at=tk(2, "1p"))


def s_maths(L, t):
    beat(L, "maths", t, S(4) - 0.1)
    # TODO e.g.
    # timed_line(L, [("365", Wt, tk(4, "365")), ("×", M, tk(4, "366")), ("366", Wt, tk(4, "366"))], W / 2, 580, 80, t)
    # a = panel(L, W / 2, 935, 760, 230, t, tk(5, "£") - 0.15, "green")
    # big_number(L, "£667.95", W / 2, 955, t, tk(5, "£"), size=130, alpha=a)
    # checked(L, "GOV.UK · 20 OCT 2026", W / 2, 1140, t, tk(5, "£") + 0.45)


def s_catch(L, t):
    beat(L, "catch", t, S(6) - 0.1)  # or beat(L, "twist", ...)
    # TODO e.g. bar_chart(...) with a red value_tag on the surprising bar


def s_miss(L, t):
    beat(L, "miss", t, S(7) - 0.1)
    # TODO e.g. versus(L, t, dict(...), dict(...), cy=715)


def s_levelup(L, t):
    beat(L, "levelup", t, S(10) - 0.1, sub="TODO ASSUMPTION LINE")
    # TODO e.g. line_chart(...)
    caveat(L, t, S(11), ["Illustration only. TODO assumptions,", "Investments can fall as well as rise."], cy=1110)


def s_turn(L, t):
    your_turn(L, t, 12, ["TODO QUESTION,", "TODO LINE 2:"], "= £?", hint="TODO hint, never the answer")


def s_share(L, t):
    share_close(L, t, 13, ["TODO the friend who", "TODO needs this"])


SCENES = [(0, 1), (2, 3), (4, 5), (6, 6), (7, 9), (10, 11), (12, 12), (13, 13)]
DRAW = [s_hook, s_example, s_maths, s_catch, s_miss, s_levelup, s_turn, s_share]


def events():
    ev = [{"t": tk(0, "£") + 0.1, "kind": "coin"}]
    # TODO pops on numbers: ev.append({"t": tk(si, "£3.65"), "kind": "pop"}); "boom" on a catch; "coin" on big wins
    return scene_events(ev)
