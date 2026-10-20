# Pound for Pound — brand book (brand-v1.1)

One look for every Short. The look is **code**, not a description: `pipeline/brand.py` draws the frame,
logo, beat chips, cover, hook, end cards, captions and the loop, so every video comes out the same — while
`pipeline/cover.py` gives each one its own cover and the palette changes with every video. A video opts in
with `BRAND = True` in its `scenes.py`. Worked example: `samples/005-penny-challenge/`. Blank template:
`template/short/`. QA: `python3 -I pipeline/qa.py <video_dir>` must print `RESULT: PASS`.

**Promise:** UK money, explained with data. Every number is computed in code and every rule, rate or
allowance is checked against an official source on the day the video is made.

---

## 1. The format: one "Money Maths" Short, 45–60 seconds

Every Short follows the same beats in the same order, with the same beat chips, so viewers learn the format.

| # | Beat | Sentences | What is said | On screen (block in `brand.py`) |
|---|------|-----------|--------------|------------------------------|
| 1 | **Cover + hook** | 1–2 | Sentence 1 states the **payoff number**. Sentence 2 opens a loop ("But most people quit in December.") | `cover_hook()` — frame 0 is the cover; then the payoff number lands |
| 2 | **The example** | 1–2 | Real people, prices or everyday objects | `beat("example")` + cards / chart |
| 3 | **The maths** | 1–2 | Step by step, short | `beat("maths")` + `timed_line()` + `big_number()` + `checked()` |
| 4 | **The catch** or **The twist** | 1–2 | The surprise | `beat("catch")` (red) or `beat("twist")` (green) |
| 5 | **One thing people miss** | 1–3 | The practical tip | `beat("miss")` |
| 6 | Level up *(optional)* | 1 | The bigger picture (invest it, 10 years on…) | `beat("levelup")` + `line_chart()` |
| 7 | Caveat | 1, short | "Illustration only. Investments can fall as well as rise." (whenever there is risk or an assumption) | `caveat()` |
| 8 | **Your turn** | 1 | A question with a number answer. **Never show the answer.** | `your_turn()` |
| 9 | **Send this to** | 1, always last | "Send this to the friend who …" — then the video loops | `share_close()` |

Budget: **11–16 sentences**, voice `bf_emma`, speed **1.15**, gap **0.08** → 45–60 s. Over 65 s, cut words.

## 2. Built-in viral mechanics (do not remove)

1. **Frame 0 is the cover.** A full-bleed scene that fits the subject + one or two huge words, one
   highlighted — the same picture on the channel grid, in the feed and at the loop. After 0.45 s the scene
   dims, the words move up and the giant payoff number lands. Saved as `build/cover.png` / `cover.jpg`.
2. **Voice starts at 0.0 s** with the payoff number in sentence 1. No intro, no "hi guys", no logo sting first.
3. **Open loop in sentence 2** ("…here's why", "most people get this wrong") so viewers stay for the answer.
4. **Visible progress**: progress bar + fixed beat chips tell viewers where they are and that it's short.
5. **Everything appears on its spoken word** (`tk(sentence, "word")`). Never a static slide.
6. **One payoff per beat**, in green, big. Inputs white, in-between results cyan, costs red.
7. **Comment question** with a definite number answer (people comment to prove they got it).
8. **Share line last, naming a specific person** — the friend, partner, flatmate, parent, colleague who needs
   it. Shares come from giving the viewer a *reason* and a *recipient*. The first comment repeats it.
9. **Seamless loop**: the last 0.5 s dissolves into frame 0, and the share line leads straight back into the
   hook, so replays feel natural.
10. **Trust stamp**: `checked("GOV.UK · 20 OCT 2026")` when an official figure appears (or
    `"MATHS CHECKED · <date>"` for pure arithmetic). This is the brand's signature.

## 3. Visual identity

### Cover (every video)
- **Words:** one or two, max ~11 characters each, Anton, huge (auto-fitted to 860 px wide). Plain word =
  white with a black outline; **highlighted word** = the palette's highlight colour (yellow or red) with a
  white outline and black edge. Highlight the word that carries the hook: **1p** CHALLENGE, START **EARLY**,
  **CHILD** BENEFIT, **MILLIONAIRE**, **£5** DAILY.
- **Scene:** `COVER = dict(words=(...), highlight=0, hero=..., left=..., right=..., particles=..., fill=..., env=...)`
  - `hero` — the big sharp subject: a Fluent emoji folder name, or `"£"` (the gold pound sign)
  - `left` / `right` — supporting objects, blurred behind for depth · `particles` — small objects scattered
    (usually `"Coin"`) · `fill` — fills a container hero (`hero="Jar", fill="Coin"`) · `env` — `"city"`
    (night skyline, default) or `"plain"`
  - Objects that fit common topics: savings → Jar + Coin, Calendar · investing → Chart increasing, £ ·
    pensions → Old man / Old woman, Hourglass not done · home/mortgage/rent → House with garden, Key ·
    cards/debt → Credit card, Warning, Chains · tax/payslip → Receipt, Classical building · cars → Automobile,
    Key · family → Baby, Woman, Man · energy → Electric plug, Light bulb · wedding → Ring, Wedding · shopping →
    Shopping cart, Shopping bags · coffee/habits → Hot beverage. Any of the ~1,600 names at
    github.com/microsoft/fluentui-emoji/tree/main/assets works.
  - **Never** objects showing "$" (Money bag, Money with wings, Dollar banknote, Heavy dollar sign): use
    `"£"`, Pound banknote or Coin. No real people, logos or brands.

### Daily palette (changes with every video)
Background, glow and accents rotate by video number, so the two daily Shorts never share a colour:
005 emerald → 006 royal → 007 ember → 008 plum → 009 ocean → 010 wine → 011 graphite → 012 magenta → 013
emerald… (`spec.json` `"theme"` can override; `classic` is the old navy). The **roles** never change: accent
= key results and the spoken caption word; in-between results; red-ish = costs; muted = labels; white =
inputs. The logo coin stays green on every palette.

### Fixed elements

| Element | Spec |
|---|---|
| Canvas | 1080 × 1920, 30 fps, H.264 CRF 18, AAC 192k, loudness −14 LUFS |
| Background | The day's palette: dark-to-rich vertical gradient, 60 px grid at 4 %, slow glow in the palette colour |
| Logo | Green coin with an ink "£" (`logo_sprite`), top-left with the wordmark **POUND FOR POUND** and tagline *UK MONEY · EXPLAINED WITH DATA* |
| Episode | `#NNN` pill top-right (from the folder name) |
| Font | Nunito Black (headlines, numbers), Nunito ExtraBold (labels); Anton for the cover words only. |
| Colours | By role, from the day's palette (see above): accent = key result · in-between · white = inputs · muted = labels · red-ish = costs |
| Beat chip | Pill at y = 305: THE EXAMPLE · THE MATHS · THE CATCH (red) · THE TWIST (green) · ONE THING PEOPLE MISS · LEVEL UP (green) · YOUR TURN (green) · SEND THIS TO (green) |
| Captions | Karaoke, 60 px Nunito Black with shadow, spoken word green, centred at y = 1365, max 840 px wide |
| Motion | Spring entrances, 0.35 s scene dissolves, numbers pulse when spoken, emoji idle bob |
| Emoji | 3D Fluent emoji from `assets/emoji/` only (MIT licence) |
| Sound | Original synth bed (100 bpm, ducked under the voice), whoosh into each scene, pop on numbers, coin on big wins, boom on a catch, the **brand sting** (three rising bells) on the share card |

### Layout grid and safe zones (YouTube hides the top ~120 px, the bottom ~300 px and a button column on the right)

```
y   0–120   hidden by the app
y 120–235   logo bar + episode + progress            (brand_bar — automatic)
y 276–334   beat chip                                (beat())
y 370–1240  CONTENT ZONE                             x 70–1010; below y 900 keep x < 960
y 1310–1420 captions                                 (automatic)
y 1480–1920 keep empty (title, channel, description overlay)
```
`qa.py` fails the video if anything lands in a hidden zone, if the font lacks a character (→ ✓ ↓ show as boxes:
use words or `L.arrow`), or if frame 0 is empty.

## 4. Words

- British spelling, plain English, short sentences (≤ 20 spoken words). Numbers as `{£667.95|six hundred and
  sixty seven pounds, ninety five}`.
- **Hook formulas** (sentence 1 = the claim with the number; on screen = 1–2 headline lines + the number).
  `<X>` = a figure you compute and verify for that video — never reuse a number from this list:
  - *The number:* "One penny today, two tomorrow, and by New Year's Eve you'll have £667.95." (005)
  - *Then vs now:* "£100 from <year> buys what £<X> bought back then."
  - *You vs them:* "Two friends earn the same. One ends up £<X> richer."
  - *The trap:* "Earn £<X> and part of your next pay rise is taxed at <X>%."
  - *The mistake:* "Paying the minimum on a £<X> credit card takes <X> years."
  - *The challenge:* "Save £<X> in <X> days with <X> envelopes."
- **Sentence 2 (open loop):** "But most people quit in December." · "Here's the bit nobody tells you." ·
  "And it gets worse."
- **Share line** (always last, a specific person + why): "Send this to the friend who says pennies don't
  matter." · "…to anyone who just got a pay rise." · "…to your partner before you book the wedding." ·
  "…to the friend still paying 40% on an overdraft."
- **Title:** ≤ 100 characters, the number + curiosity, one or two emoji, ends `#shorts`.
  e.g. "1p a Day Becomes £667.95… Why Most People Quit in December 😱 #shorts"
- **First comment** (`meta.json` → `first_comment`): the share prompt again + "every number checked".
- Never: "hit like", "smash subscribe", promises of returns, "guaranteed", another creator's script, real
  people's clips, numbers we can't source.

## 5. What may change between videos

Each video has its own cover and the next palette in the rotation. Inside the content zone each video should *look* fresh: pick different blocks (value cards, versus cards,
bar chart, line chart, checklist, calculator, timeline) and different emoji. The frame, logo, fonts, colour roles,
beat chips, cover style, hook layout, end cards, captions, sounds and loop never change. A new block may be added to
`brand.py` when a topic needs it — in the brand colours, and then it's available to every video.

## 6. Block reference (`from brand import *`)

| Block | Use |
|---|---|
| `cover_hook(L, t, number, sub=, number_at=, kicker=, extra=)` | Scene 1 for videos with a `COVER` (all new ones). `kicker` = one short context line under the cover words. `extra(L, t)` adds one late element (e.g. a red chip on sentence 2). |
| `hook(L, t, lines, number, sub=, emoji=, number_at=, stamp=, extra=)` | Older scene-1 layout without a cover. |
| `beat(L, key, t, start, sub=, sub_at=)` | Beat chip. Keys: `example maths catch twist miss levelup turn share`, or free text. |
| `chip(L, label, cx, cy, t, start, tone, size, emoji=, outline=)` | Any pill. Tones: green white red cyan gold. |
| `checked(L, "GOV.UK · 20 OCT 2026", cx, cy, t, start)` | Trust stamp. |
| `panel(L, cx, cy, w, h, t, start, tone=)` | Glass card; tone gives a coloured glowing border. Returns alpha. |
| `value_card(L, cx, cy, w, t, start, emoji, label, value, color=, value_at=, sub=)` | Emoji + label + big value. |
| `versus(L, t, left, right, cy=, h=)` | Two cards + VS coin. Keep above y 900. |
| `timed_line(L, [(text, colour, at), …], cx, cy, size, t)` | Maths line, each token on its own word. |
| `big_number(L, s, cx, cy, t, at=, size=, color=)` | Hero number with glow; pulses at `at`. |
| `bar_chart(L, t, start, values, labels, box, colors, value_tags=)` | Vertical bars. |
| `line_chart(L, t, start, dur, series, box, xmax, ymax, x_labels=, y_labels=, end_tags=)` | Growth lines; end labels sit right of the line ends (leave ~200 px). |
| `caveat(L, t, start, lines, cy=)` | Small muted caveat text. |
| `your_turn(L, t, si, lines, answer_shape=, hint=)` | Comment scene. |
| `share_close(L, t, si, lines)` | Final scene: SEND THIS TO + who + arrow + logo/follow. |
| `scene_events(extra)` | Standard whooshes + brand sting; add pops/coins on numbers. |

Motion primitives from `motion.py` (`L.text`, `L.emoji`, `L.arrow`, `L.math_line`, `spring`, `ramp`, `ease`,
`S(i)`, `tk(i, "word")`) are available for custom drawing inside the content zone.
