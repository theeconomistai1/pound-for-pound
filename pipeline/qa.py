"""Brand QA for one Short: script rules, safe zones, cover frame, metadata, and a contact sheet to eyeball.

  python3 -I pipeline/qa.py <video_dir>

Needs <video_dir>/build/timings.json (run the build first, or at least tts2.py). Writes:
  build/cover.png    frame 0 = the cover (also cover.jpg), which is also the loop target
  build/contact.png  frame 0, the end of every scene, and the loop frame, on one sheet
Prints PASS / WARN / FAIL lines and exits 1 if anything FAILs. Fix every FAIL before publishing.
"""
import json
import os
import re
import sys

import numpy as np
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import motion as Mo  # noqa: E402

SEEN = set()  # every string drawn, for the glyph check
_text_sprite = Mo.text_sprite


def _recording_text_sprite(s, *a, **k):
    SEEN.add(s)
    return _text_sprite(s, *a, **k)


Mo.text_sprite = _recording_text_sprite  # before brand / scenes import it
import brand as Br  # noqa: E402
import make_v3  # noqa: E402

results = []


def report(level, msg):
    results.append(level)
    print(f"{level:4}  {msg}")


def spoken(sentence):
    return re.sub(r"\{[^|}]*\|([^}]*)\}", r"\1", sentence)


FORMATS = ("calc", "myth", "since", "news")
CTA = re.compile(r"^(send this|follow|like|subscribe|hit |smash|share this|comment )", re.I)


def shown_numbers(spec):
    text = " ".join(re.sub(r"\{([^|}]*)\|[^}]*\}", r"\1", s) for s in spec["sentences"])
    return sorted({x.rstrip(".,") for x in re.findall(r"£[\d,]+(?:\.\d+)?[KkMm]?|\d[\d,]*(?:\.\d+)?%?p?", text)
                   if any(ch.isdigit() for ch in x)})


def check_script(spec, video_dir):
    ss = spec["sentences"]
    n = len(ss)
    (report("PASS", f"{n} sentences") if 6 <= n <= 10 else
     report("WARN" if n <= 12 else "FAIL", f"{n} sentences (brand-v2: 6-10 for a 20-40 s Short)"))
    fmt = spec.get("format")
    if fmt not in FORMATS:
        report("FAIL", f"spec.json needs \"format\": one of {FORMATS}")
    else:
        prev = previous_format(video_dir)
        (report("WARN", f"same format as the previous video ({fmt}) — rotate formats") if prev == fmt else
         report("PASS", f"format {fmt} (previous video: {prev or 'n/a'})"))
    if re.search(r"[£%]|\d", ss[0]):
        report("PASS", "hook sentence carries the payoff number")
    else:
        report("FAIL", "sentence 1 must contain the payoff number (the hook)")
    last = spoken(ss[-1]).strip()
    if CTA.search(last):
        report("FAIL", "the last line is a call to action — it must be the loop line that runs into sentence 1 "
                       "(put share/comment prompts in the first comment)")
    elif last.endswith((".", "!")):
        report("WARN", "loop line ends with a full stop — end on a hand-over (':' ',' or '…') into sentence 1")
    else:
        report("PASS", "ends on a loop line")
    if spec.get("format") in ("calc", "since") and not any(
            re.search(r"illustration|can fall|not financial advice|may get back less|past performance", s, re.I)
            for s in ss):
        report("WARN", "no spoken caveat — keep one on screen at least (caveat() block) for anything about investing")
    long = [i for i, s in enumerate(ss) if len(spoken(s).split()) > 20]
    if long:
        report("WARN", f"long sentences (>20 spoken words): {long}")
    # Simple & gripping (BRAND.md §0, owner's request 23 Oct 2026)
    busy = [i for i, s in enumerate(ss) if len(spoken(s).split()) > 16]
    if busy:
        report("WARN", f"sentences over 16 spoken words: {busy} — one idea per sentence (BRAND.md §0)")
    nums = shown_numbers(spec)
    (report("PASS", f"{len(nums)} different numbers said") if len(nums) <= 5 else
     report("WARN", f"{len(nums)} different numbers said ({', '.join(nums)}) — max 5; keep the rest in the "
                    "description (BRAND.md §0)"))
    if any(re.search(r"\d\.\d", re.sub(r"\{([^|}]*)\|[^}]*\}", r"\1", x)) for x in ss):
        report("WARN", "a decimal is said in the video — round it or keep it in the description (BRAND.md §0)")


def previous_format(video_dir):
    here = os.path.basename(os.path.normpath(video_dir))
    root = os.path.dirname(os.path.dirname(os.path.abspath(video_dir)))
    best = None
    for d in sorted(os.listdir(os.path.join(root, "videos"))):
        if d < here and os.path.exists(os.path.join(root, "videos", d, "spec.json")):
            best = json.load(open(os.path.join(root, "videos", d, "spec.json"), encoding="utf-8")).get("format")
    return best


def check_timing():
    total = Mo.T["total"]
    first = Mo.T["sentences"][0]["start"]
    if 20 <= total <= 40:
        report("PASS", f"length {total:.1f}s")
    elif total <= 45:
        report("WARN", f"length {total:.1f}s (brand-v2: 20-40 s)")
    else:
        report("FAIL", f"length {total:.1f}s — cut to 20-40 s")
    (report("PASS", f"voice starts at {first:.2f}s") if first <= 0.35 else
     report("FAIL", f"voice starts late ({first:.2f}s) — the hook must land in the first 1-2 seconds"))
    # tempo and rhythm + short and clear (BRAND.md §0b)
    if total > 35:
        report("WARN", f"length {total:.1f}s — short and clear: aim for 25-35 s (BRAND.md §0b)")
    sc = Mo.SCENE.SCENES
    slow = []
    for k, (a, _) in enumerate(sc):
        end = Mo.S(sc[k + 1][0]) if k + 1 < len(sc) else total
        if end - Mo.S(a) > 8.5:
            slow.append(f"scene {k + 1} ({end - Mo.S(a):.1f}s)")
    (report("WARN", f"slow scenes: {', '.join(slow)} — change the picture every 5-8 s (BRAND.md §0b)") if slow else
     report("PASS", "tempo: every scene is 8.5 s or shorter"))


def check_layout():
    total = Mo.T["total"]
    zones = {
        "above the beat chip (y<255)": (slice(0, 255), slice(0, Mo.W)),
        "bottom overlay (y>1480)": (slice(Br.CLEAR_Y, Mo.H), slice(0, Mo.W)),
        "left edge (x<40)": (slice(0, Mo.H), slice(0, 40)),
        "right edge (x>1040)": (slice(0, Mo.H), slice(1040, Mo.W)),
        "button column (x>975, y>900)": (slice(900, Mo.H), slice(975, Mo.W)),
    }
    hits = {}
    Br.DRAW_COVER_BG = False  # the cover scene is meant to fill the frame; lint what sits on top of it
    for t in np.arange(0, total, 0.25):
        a = np.asarray(Br._content(float(t)))[..., 3]
        for name, (ys, xs) in zones.items():
            if (a[ys, xs] > 60).sum() > 30:
                hits.setdefault(name, []).append(round(float(t), 2))
        if t % 1.0 < 0.01:
            cap = Mo.Layer()
            Br.captions(cap, float(t), Mo.GROUPS)
            ca = np.asarray(cap.im)[..., 3]
            if (ca[:, :90] > 60).sum() + (ca[:, 990:] > 60).sum() > 30:
                hits.setdefault("captions too wide", []).append(round(float(t), 2))
    if not hits:
        report("PASS", "safe zones clear on every frame checked (every 0.25s)")
    for name, ts in hits.items():
        report("FAIL", f"content in {name} at t={ts[:8]}{' …' if len(ts) > 8 else ''}")
    a0 = np.asarray(Br._content(0.0))[..., 3]
    filled = (a0 > 60).mean()
    Br.DRAW_COVER_BG = True
    (report("PASS", f"frame 0 shows the hook ({filled * 100:.1f}% of the frame)") if filled > 0.02 else
     report("FAIL", "frame 0 is nearly empty — the hook must be fully visible on the first frame"))


def check_cover():
    c = getattr(Mo.SCENE, "COVER", None)
    if not c:
        report("FAIL", "no COVER in scenes.py — every Short opens on its cover (BRAND.md §3)")
        return
    words = list(c.get("words", ()))
    if not 1 <= len(words) <= 2:
        report("FAIL", f"cover must have one or two words, not {len(words)}: {words}")
    elif any(len(w) > 11 for w in words):
        report("WARN", f"long cover word {words} — shorter words read better on a phone grid")
    else:
        report("PASS", f"cover: {' '.join(words)} (highlight: {words[c.get('highlight', 0)] if c.get('highlight', 0) >= 0 else 'none'}) on the {Br.THEME_KEY} palette")
    import cover as Cv
    for name in filter(None, (c.get("hero"), c.get("left"), c.get("right"), c.get("particles"))):
        try:
            Cv.obj(name, 64)
        except Exception as e:  # noqa: BLE001
            report("FAIL", f"cover object {name!r} not found: {e}")


def check_glyphs():
    """Characters the font cannot draw render as empty boxes. Every drawn string is checked."""
    try:
        from fontTools.ttLib import TTFont
    except ImportError:
        report("WARN", "fontTools not installed (pip install fonttools) — glyph check skipped; look for boxes")
        return
    cmap = TTFont(Mo.FONT).getBestCmap()
    bad = sorted({ch for s in SEEN for ch in s if ord(ch) not in cmap and not ch.isspace()})
    if bad:
        report("FAIL", f"characters missing from the font (they show as boxes): {bad} — reword or draw them")
    else:
        report("PASS", f"all {len(SEEN)} on-screen strings use characters the font has")


def check_meta(video_dir, spec):
    path = os.path.join(video_dir, "meta.json")
    if not os.path.exists(path):
        report("FAIL", "no meta.json")
        return
    m = json.load(open(path, encoding="utf-8"))
    title = m.get("title", "")
    (report("PASS", f"title {len(title)} chars") if len(title) <= 100 and title.endswith("#shorts") else
     report("FAIL", "title must be <= 100 characters and end with #shorts"))
    d = m.get("description", "")
    for need in ("General education, not financial advice.", "Music and sound effects: original, made for this channel."):
        if need not in d:
            report("FAIL", f"description is missing: {need!r}")
    for key in ("comment_question", "first_comment", "pillar"):
        if not m.get(key):
            report("WARN", f"meta.json has no {key}")
    tags = m.get("tags", [])
    (report("PASS", f"{len(tags)} tags") if 6 <= len(tags) <= 10 else report("WARN", f"{len(tags)} tags (aim 6-10)"))
    # fact sheet: every number in the script must be listed with how it was worked out and its source
    facts = m.get("facts") or []
    listed = " ".join(str(f.get("figure", "")) for f in facts)
    nums = shown_numbers(spec)
    missing = [x for x in nums if x not in listed]
    if not facts:
        report("FAIL", "meta.json has no facts list (figure, how, source, checked) — the owner reviews from it")
    elif missing:
        report("FAIL", f"numbers in the script missing from meta.facts: {missing}")
    else:
        bad = [f.get("figure") for f in facts if not (f.get("how") and f.get("source") and f.get("checked"))]
        (report("FAIL", f"facts without how/source/checked: {bad}") if bad else
         report("PASS", f"fact sheet covers all {len(nums)} numbers in the script"))
    not_in_desc = [x for x in nums if x not in d and len(x) > 2]
    if not_in_desc:
        report("WARN", f"numbers said in the video but not in the description: {not_in_desc}")


BRIEF = {  # BRAND.md §0b: answered BEFORE the script is written
    "why_watch": ("hook", "curiosity", "tempo", "feeling"),
    "why_comment": ("take_sides", "debate", "something_to_say", "see_yourself"),
    "why_share": ("send_to", "memorable_line", "thats_me", "short_and_clear"),
}


def _norm(x):
    return re.sub(r"[^a-z0-9£%]+", " ", x.lower()).strip()


def check_brief(video_dir, spec):
    path = os.path.join(video_dir, "meta.json")
    if not os.path.exists(path):
        return
    m = json.load(open(path, encoding="utf-8"))
    b = m.get("brief")
    if not isinstance(b, dict):
        report("FAIL", "meta.json has no brief — answer why watch / comment / share / follow BEFORE writing the "
                       "script (BRAND.md §0b)")
        return
    weak = []
    for group, keys in BRIEF.items():
        g = b.get(group) or {}
        for k in keys:
            v = str(g.get(k, "")).strip()
            if len(v) < 10 or "TODO" in v:
                weak.append(f"{group}.{k}")
    v = str(b.get("why_follow", "")).strip()
    if len(v) < 10 or "TODO" in v:
        weak.append("why_follow")
    if weak:
        report("FAIL", f"brief answers missing or too thin: {weak} — no good answer means a weak video: "
                       "sharpen the angle or pick another topic (BRAND.md §0b)")
    else:
        report("PASS", "brief: why watch, why comment, why share and why follow all answered")
    shown = _norm(" ".join(re.sub(r"\{([^|}]*)\|[^}]*\}", r"\1", x) for x in spec["sentences"]))
    said = _norm(" ".join(spoken(x) for x in spec["sentences"]))
    line = _norm(str((b.get("why_share") or {}).get("memorable_line", "")))
    if line and line not in shown and line not in said:
        report("FAIL", "brief.why_share.memorable_line must be a line the video actually says, word for word")
    elif line and len(line.split()) > 12:
        report("WARN", "memorable line is over 12 words — make it short enough to quote (BRAND.md §0b)")
    yous = sum(1 for x in spec["sentences"] if re.search(r"\byou(r|'re|'ll|'d)?\b", spoken(x), re.I))
    (report("PASS", f"talks to 'you' in {yous} sentences") if yous >= 2 else
     report("WARN", "the script hardly says 'you/your' — viewers need to see themselves in it (BRAND.md §0b)"))
    q = m.get("comment_question", "")
    if re.search(r"\b(how much|how many)\b", q, re.I) or re.match(r"\s*(what is|what's|what does)\b", q, re.I):
        report("WARN", "the comment question is a quiz with one answer — ask one people take sides on or answer "
                       "about themselves (BRAND.md §0b)")
    src = open(os.path.join(video_dir, "scenes.py"), encoding="utf-8").read()
    if "TODO" in src:
        report("FAIL", "scenes.py still has TODO placeholders")
    if not re.search(r"loop_close\([^)]*comment=", src):
        report("WARN", "the loop scene has no take-sides chip — loop_close(..., comment=\"FAIR OR NOT? COMMENT\") "
                       "(BRAND.md §0b)")


STEP_NAMES = ("risk", "question", "twist", "rehook", "answer", "context", "loop")
BRIDGE = re.compile(r"^(but|and|here's|here is|the twist|the catch|so|very few|the second|now|then|wait|sure|plot twist)\b", re.I)


def check_loop(video_dir, spec):
    """The dopamine loop (BRAND.md §0c): risk -> question -> twist -> rehook, at least twice."""
    st = spec.get("steps")
    ss = spec["sentences"]
    if not isinstance(st, list) or len(st) != len(ss):
        report("FAIL", "spec.json needs \"steps\": one label per sentence (risk / question / twist / rehook / "
                       "answer / context / loop) — the dopamine loop (BRAND.md §0c)")
        return
    bad = [x for x in st if x not in STEP_NAMES]
    if bad:
        report("FAIL", f"unknown steps {bad} — use {STEP_NAMES}")
        return
    if "risk" not in st[:2]:
        report("FAIL", "no risk in the first two sentences — who could lose what, by when (BRAND.md §0c step 1)")
    if st[-1] != "loop":
        report("FAIL", "the last step must be the loop line")
    loops, open_q, rehook_between = 0, False, True
    for x in st:
        if x == "question":
            open_q = True
        elif x == "twist" and open_q:
            if loops and not rehook_between:
                break
            loops += 1
            open_q, rehook_between = False, False
        elif x == "rehook":
            rehook_between = True
    (report("PASS", f"dopamine loop: {loops} question -> twist loops, joined by a rehook") if loops >= 2 else
     report("FAIL", f"only {loops} complete loop(s) — need at least two question -> twist loops with a rehook "
                    "between them (BRAND.md §0c)"))
    weak = [i for i, x in enumerate(st) if x == "rehook" and not BRIDGE.search(spoken(ss[i]).strip())]
    if weak:
        report("WARN", f"rehook sentences {weak} don't open on a bridge ('But…', 'Here's the strange part:') — "
                       "BRAND.md §0c step 4")
    for i, x in enumerate(st):
        if x == "question" and spoken(ss[i]).strip().endswith("?") and len(spoken(ss[i]).split()) > 6:
            report("WARN", f"sentence {i} asks the big question out loud — give one fact too few and let the "
                           "viewer ask it (BRAND.md §0c step 2)")
    m = json.load(open(os.path.join(video_dir, "meta.json"), encoding="utf-8")) if os.path.exists(
        os.path.join(video_dir, "meta.json")) else {}
    b = m.get("brief") or {}
    r = b.get("risk") or {}
    lp = b.get("loops") or []
    thin = [k for k in ("who", "stake", "deadline") if len(str(r.get(k, ""))) < 4 or "TODO" in str(r.get(k, ""))]
    thin += [f"loops[{i}].{k}" for i, l in enumerate(lp) for k in ("question", "twist", "new_question")
             if len(str(l.get(k, ""))) < 8 or "TODO" in str(l.get(k, ""))]
    if len(lp) < 2:
        thin.append("loops (need 2)")
    (report("FAIL", f"brief.risk / brief.loops missing or thin: {thin} (BRAND.md §0c)") if thin else
     report("PASS", "brief: risk (who, stake, deadline) and both loops planned"))


def contact_sheet(video_dir):
    b = os.path.join(video_dir, "build")
    total = Mo.T["total"]
    times = [0.0]
    sc = Mo.SCENE.SCENES
    for k, (a, _) in enumerate(sc):
        start = Mo.S(a)
        end = Mo.S(sc[k + 1][0]) if k + 1 < len(sc) else total - Br.LOOP
        times.append(max(start + 0.5, end - 0.45))
    times.append(total - 0.05)
    im0 = make_v3.FRAME(0.0)
    im0.save(os.path.join(b, "cover.png"))
    im0.save(os.path.join(b, "cover.jpg"), quality=92)
    tw, th = 360, 640
    cols = 5
    rows = (len(times) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * tw + (cols + 1) * 12, rows * (th + 40) + 12), (8, 8, 16))
    for i, t in enumerate(times):
        im = make_v3.FRAME(t).resize((tw, th), Image.LANCZOS)
        x, y = 12 + (i % cols) * (tw + 12), 12 + (i // cols) * (th + 40)
        sheet.paste(im, (x, y))
        lab = Mo.text_sprite(f"{t:.1f}s", 22, (200, 200, 220), "ExtraBold")
        sheet.paste(lab, (x, y + th + 2), lab)
    out = os.path.join(b, "contact.png")
    sheet.save(out)
    report("INFO", f"contact sheet: {out} — read it: no clipped or overlapping text, numbers match meta.json")


def main():
    video_dir = sys.argv[1]
    mod = make_v3.load(video_dir)
    if not getattr(mod, "BRAND", False):
        sys.exit("this video does not use the brand kit (BRAND = True)")
    spec = json.load(open(os.path.join(video_dir, "spec.json"), encoding="utf-8"))
    check_script(spec, video_dir)
    check_timing()
    check_cover()
    check_layout()
    check_glyphs()
    check_meta(video_dir, spec)
    check_brief(video_dir, spec)
    check_loop(video_dir, spec)
    contact_sheet(video_dir)
    if "FAIL" in results:
        print("RESULT: FAIL — fix the lines above before publishing")
        sys.exit(1)
    print("RESULT: PASS" + (" (with warnings)" if "WARN" in results else ""))


if __name__ == "__main__":
    main()
