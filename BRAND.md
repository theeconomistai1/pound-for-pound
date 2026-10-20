# Pound for Pound — brand book (brand-v1)

One look for every Short. The look is **code**, not a description: `pipeline/brand.py` draws the frame,
logo, beat chips, hook, end cards, captions and the loop, so every video comes out the same. A video opts in
with `BRAND = True` in its `scenes.py`. Worked example: `samples/005-penny-challenge/`. Blank template:
`template/short/`. QA: `python3 -I pipeline/qa.py <video_dir>` must print `RESULT: PASS`.

**Promise:** UK money, explained with data. Every number is computed in code and every rule, rate or
allowance is checked against an official source on the day the video is made.

---

## 1. The format: one "Money Maths" Short, 45–60 seconds

Every Short follows the same beats in the same order, with the same beat chips, so viewers learn the format.

| # | Beat | Sentences | What is said | On screen (block in `brand.py`) |
|---|------|-----------|--------------|------------------------------|
| 1 | **Hook** | 1–2 | Sentence 1 states the **payoff number**. Sentence 2 opens a loop ("But most people quit in December.") | `hook()` — fully visible on frame 0 |
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

1. **Frame 0 is the hook.** Headline + giant green payoff number are on screen on the very first frame — no
   fade-in. It is also the cover frame (`build/thumb.png`) and the loop target.
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

## 3. Visual identity (locked)

| Element | Spec |
|---|---|
| Canvas | 1080 × 1920, 30 fps, H.264 CRF 18, AAC 192k, loudness −14 LUFS |
| Background | Navy → purple vertical gradient (`#0E1430` → `#2A2A6E`), 60 px grid at 4 %, slow purple glow |
| Logo | Green coin with an ink "£" (`logo_sprite`), top-left with the wordmark **POUND FOR POUND** and tagline *UK MONEY · EXPLAINED WITH DATA* |
| Episode | `#NNN` pill top-right (from the folder name) |
| Font | Nunito Black (headlines, numbers), Nunito ExtraBold (labels). Nothing else. |
| Colours | Green `#9BE15D` = key result · Cyan `#4FC3F7` = in-between · White = inputs · Muted `#8A93B8` = labels · Red `#FF7070` = costs/losses · Gold `#FFCD56` = rare "record" highlight |
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

Inside the content zone each video should *look* fresh: pick different blocks (value cards, versus cards,
bar chart, line chart, checklist, calculator, timeline) and different emoji. The frame, colours, font, beat
chips, hook layout, end cards, captions, sounds and loop never change. A new block may be added to
`brand.py` when a topic needs it — in the brand colours, and then it's available to every video.

## 6. Block reference (`from brand import *`)

| Block | Use |
|---|---|
| `hook(L, t, lines, number, sub=, emoji=, number_at=, stamp=, extra=)` | Scene 1. `lines` ≤ 2 × 22 chars. `extra(L, t)` adds one late element (e.g. a red chip on sentence 2). |
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
