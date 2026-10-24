# Pound for Pound — brand book (brand-v2)

One look, several formats, a human in the loop. The look is **code**: `pipeline/brand.py` draws the frame,
logo, beat chips, cover, hook, loop ending and captions; `pipeline/cover.py` gives each video its own cover;
the palette changes with every video. Templates: `template/calc`, `template/myth`, `template/since`,
`template/news`. Worked example: `samples/v2-myth-pay-rise/`. QA: `python3 -I pipeline/qa.py <video_dir>`
must print `RESULT: PASS`.

**Promise:** UK money, explained with data. Every number is computed in code, every rule, rate or allowance is
checked against an official source on the day.

**Why it's built this way (monetisation).** YouTube's Partner Program policy (updated July 2026) won't
monetise channels with too much *generic, repetitive or template-based* content, *distressing* content, or
*AI personas* (AI-made likenesses of real people) on sensitive topics such as finance. YouTube judges how
content is made and whether it adds value, not AI use itself. So: UK-specific topics with our own maths and
data, rotating formats, the owner's own take when she adds one, no presenter or persona, honest disclosure.

---

## 0. Simple and gripping (the owner's rule, 23 Oct 2026 — this wins over anything below)

The owner's feedback: earlier videos had too much maths and were hard to follow. Every Short now is a tiny
**story with a surprise**, not a worked calculation. Viewers should *feel* something (surprise, "that's not
fair", relief) and want to see the end.

1. **Hook in the first 2 seconds: a surprise or a contradiction**, not a sum. Make the viewer think "wait,
   what?". Good: "The government gives you £1,000… then takes back even more." · "Earn £1 more, and you
   could lose £600." · "This pension trick gives you £20 for free." Bad: "Pay £4,000 in, take it out early,
   and get back £3,750." (correct, but it's a sum). The hook must still be true and match the video.
2. **Open a loop, close it late.** The hook raises a question; the full answer lands in the last third.
   Add a re-hook every 5–8 seconds: "Sounds amazing, right?" · "But here's the catch." · "And it gets worse."
3. **Maximum 5 different numbers said aloud** (fewer is better), round and friendly (£1,000, a quarter,
   half). No decimals, no percentages of percentages, no equations said aloud. Every other figure goes in the
   description and the fact sheet — still verified.
4. **One idea per sentence, ≤ 14 spoken words**, everyday words, talk to "you" ("your £4,000"). Short
   reaction lines are good ("Sounds amazing, right?" · "Not just the bonus. Your own money too.").
5. **One thing on screen at a time**: one big number, or two cards side by side (before / after, you save /
   you get back). No formula lines, no bar charts with more than 2 bars, no blocks of small text (except the
   one-line caveat).
6. **Emotion beats**: the deal (😀) → the catch (😱) → the result in pounds (what *you* lose or gain) → the
   thing people miss → loop. Use emoji and sound (coin on a win, boom on a loss) to carry the feeling.
7. **Cover words tease, they don't explain**: FREE **£1,000?** · **60%** TAX? · PENSION **TRICK**.
8. **Title = curiosity + the number**, e.g. "The Government Gives You £1,000… Then Takes Back £1,250 😱🏠".
   Never a claim the video doesn't back up (no "guaranteed", no fake urgency).

Still true from the rules below: every number checked on the day, education not advice, no persona, no spoken
calls to action, loop ending, 20–40 s (aim for 25–35 s). `qa.py` warns when a script breaks rules 3–4: treat
those warnings as failures and fix them. Worked example: `videos/010-lisa-withdrawal-charge`.

## 0b. Three questions before you make it (the owner's rule, 23 Oct 2026)

Answer these **before writing the script**, not after a video flops, and write the answers into `meta.json` →
`brief` (template: `template/<format>/meta.json`). If you can't give a good answer, the video will be weak:
find a sharper angle, or skip the topic. `qa.py` fails a video without a full brief.

**1. Why would people watch to the end?** (`brief.why_watch`)
- `hook` — the first second: what makes a thumb stop? (a surprise, a contradiction, a loss)
- `curiosity` — "what happens next?": the question the hook opens, and where in the video it's answered
  (late, in the last third)
- `tempo` — rhythm: the picture changes every 5–8 s, a re-hook line every 5–8 s, no slow stretches
- `feeling` — the emotion the video runs on: shock, "that's not fair", relief, smugness ("I knew it")

**2. Why would they comment or share?** Watching alone isn't enough: comments and shares push a video further,
so give people something to talk about.
- Comment (`brief.why_comment`):
  - `take_sides` — the moment in the video where viewers pick a side (fair or not? would you or wouldn't
    you?). Show it on screen in the loop scene as the comment chip, e.g. `comment="FAIR OR NOT? COMMENT"`.
  - `debate` — what reasonable people will disagree about
  - `something_to_say` — the easy reply ("I nearly did this", "my bank never told me")
  - `see_yourself` — who watches and thinks "that's me" (first-time buyer, someone near £100k, a new parent)
- Share (`brief.why_share`):
  - `send_to` — "I have to send this to…" a specific person (becomes the 📩 line)
  - `memorable_line` — one quotable line the video says word for word, ≤ 12 words
    ("The government gives you £1,000… then takes back even more.")
  - `thats_me` — the "this is so me" moment
  - `short_and_clear` — the whole point in one sentence a friend would get; 25–35 s

**3. Why would they follow the account?** (`brief.why_follow`) Copying a trend can get views but doesn't earn
follows; originality does. Every video must add to the channel's reason to stick around:
- **The promise:** the UK money small print nobody tells you, in 30 seconds, every number checked on GOV.UK.
- **The rituals viewers learn to expect:** the cover question (FREE **£1,000?**), the GOV.UK CHECKED stamp,
  the loop that never quite ends, and **"fair or not?"**: every video ends with viewers taking a side.
- Say how this video fits that promise and what it sets up next (a related trap, the other side of the
  rule, a myth that follows on). Never a spoken "follow" (no calls to action).

The comment question (meta.json `comment_question`) is a **take-sides or about-you** question, not a quiz:
"Is a 25% charge on your own money fair?" · "Would you still open one?" · "Which one are you?" Never ask for or
give advice.

---

## 0c. The dopamine loop (the owner's rule, 24 Oct 2026 — the script skeleton for every format)

A casino keeps you at the table by making you *wait*, not by letting you win: the brain lights up while it waits
to see whether the reward comes. A Short does the same: **every answer opens a new question.** Every script is
built from four steps, and the steps run as a loop **at least twice** (about one loop every 12–20 s; a 30–40 s
Short = 2 loops):

| Step | In the casino | In the Short | Rules |
|---|---|---|---|
| **1 · risk** | the bet that sits you down | the viewer cares | In the first 3 seconds it is clear **who** could lose **what**, **by when**: a person the viewer sides with ("you", "your mum", or a named illustrative person — never a narrator persona), something to lose (money, a bonus, a home), and a deadline ("next April", "by 5 April", not "one day"). Sentence 1 still carries the number. |
| **2 · question** | "what's the next card?" | "what happens now?" forms in their head | Don't ask it — give one piece of information too few so the viewer asks it. **One question at a time.** Delay the answer, but let them feel it's coming. |
| **3 · twist** | the card you didn't expect | they expect A, they see B | "Everyone thinks ___. Actually ___." Opposite of the expected cause · the bad thing turns out good (or the praised thing is the problem) · the obvious answer was the wrong place to look. A twist is never a lie: it must not contradict anything said earlier — viewers should think "how did I miss that?", not "I was tricked". |
| **4 · rehook** | the next hand, dealt at once | a new question opens before the old one closes | No gap after an answer. Bridges: "But that wasn't the real problem." · "Here's the strange part:" · "And that's where it changes." · "But there was a catch." · "Very few people notice this:" · "The second mistake costs more." |

The **loop line** (the last sentence, §2.6) is the final rehook: it hands the viewer straight back to the risk in
sentence 1.

**In spec.json** label each sentence with its step, in order: `"steps": ["risk", "question", "twist", "rehook",
…, "loop"]` (other labels allowed for a plain fact: `"answer"`, `"context"`). `qa.py` FAILs a script whose
`steps` don't match the sentences, or that has no `risk` in the first two sentences, fewer than two
`question`→`twist` loops, no `rehook` between them, or a last step other than `loop`.

**In meta.json → brief** add `loops`: one entry per loop, `{"question": …, "twist": "Everyone thinks … Actually
…", "new_question": …}`, plus `risk: {"who", "stake", "deadline"}`. Write them before the script (step 2.4).

**Check before publishing** (also in the summary sheet): in the first 3 s, is it clear who could lose what? Is
there one single, clear question in the viewer's head? Does every twist agree with what was said before? Does it
flow read aloud — shorten any sentence you stumble on.

This runs inside §0 (max 5 numbers, ≤ 14 words a sentence, 20–40 s) and the formats below: the format decides
*what* the video is about, the loop decides *how the script is told*.

---

## 1. Formats (rotate — never the same format twice in a row)

Every Short is **20–40 seconds, 6–10 sentences** (voice `bf_emma`, speed 1.15, gap 0.08). Sentence 1 carries
the payoff number, so the hook lands in the first 1–2 seconds. The **last sentence is the loop line**: it hands
over into sentence 1 (ends on ":" "," or "…"), and the picture rebuilds the cover, so the replay feels like
one continuous video. No spoken calls to action.

| Format | Use it for | Beats (sentences) | Template |
|---|---|---|---|
| **calc** — the number | A UK rule turned into one surprising, exact figure | cover + payoff (0–1) → THE MATHS (2–3) → THE TWIST / THE CATCH (4) → ONE THING PEOPLE MISS (5–6) → loop line (7) | `template/calc` |
| **myth** — myth-bust | A common money belief that's wrong (or only half right) for UK rules | cover + claim (0) → THE MYTH + stamp (1) → THE TRUTH with numbers (2–3) → THE CATCH: when it *is* true (4–5) → loop line (6) | `template/myth` |
| **since** — "£X since…" | Official data over time: £1,000 since 2010, the Personal Allowance since 2010, the State Pension since 2016… | cover + result (0) → BACK THEN (1) → TODAY with a line chart (2–3) → THE TWIST vs cash/inflation + caveat (4–5) → loop line (6) | `template/since` |
| **news** — explainer | A UK change in the last few days: Budget, Bank Rate decision, energy price cap, tax-year changes | cover + change (0) → WHAT CHANGED + source stamp (1) → WHO IT AFFECTS with a worked example (2–3) → WHAT IT MEANS (4) → loop line (5) | `template/news` |

The weekly performance check (`WEEKLY.md`) can switch a format off in `formats.json` when it underperforms.

## 2. Built-in mechanics (do not remove)

1. **Frame 0 is the cover** — a full-bleed scene that fits the subject + one or two huge words, one
   highlighted. After 0.45 s the scene dims, the words move up and the payoff number lands (`cover_hook`).
2. **Voice starts at 0.0 s** with the payoff number. No intro, no greeting, no logo sting first.
3. **Visible progress**: progress bar + fixed beat chips.
4. **Everything appears on its spoken word** (`tk(sentence, "word")`). Never a static slide.
5. **One payoff per beat**, in the accent colour, big.
6. **Loop ending** (`loop_close`): the last line runs into the first while the cover rebuilds; the final
   0.5 s blends into frame 0.
7. **Trust stamp**: `checked("GOV.UK · 2026/27 RATES · CHECKED 21 OCT 2026")` whenever an official figure
   appears. The brand's signature.
8. **Comment question** (a take-sides or about-you question, §0b) and **share prompt** (a specific person)
   live in the first comment and the description; the loop scene shows the take-sides question as a chip.

## 3. Visual identity

### Cover (every video)
- **Words:** one or two, max ~11 characters each, Anton, huge (auto-fitted to 860 px). Plain word = white with
  a black outline; **highlighted word** = the palette's highlight colour with a white outline and black edge.
  Highlight the word that carries the hook: PAY RISE **MYTH**, **60%** TAX, START **EARLY**, **CHILD** BENEFIT.
- **Scene:** `COVER = dict(words=(...), highlight=0, hero=..., left=..., right=..., particles=..., fill=..., env=...)`
  - `hero` — the big sharp subject: a Fluent emoji folder name, or `"£"` (the gold pound sign)
  - `left` / `right` — supporting objects, blurred behind · `particles` — small objects scattered (usually
    `"Coin"`) · `fill` — fills a container hero (`hero="Jar", fill="Coin"`) · `env` — `"city"` or `"plain"`
  - Objects that fit common topics: savings → Jar + Coin, Calendar · investing → Chart increasing, £ ·
    pensions → Old man / Old woman, Hourglass not done · home/mortgage/rent → House with garden, Key ·
    cards/debt → Credit card, Warning, Chains · tax/payslip → Receipt, Classical building, Briefcase · cars →
    Automobile, Key · family → Baby, Woman, Man · energy → Electric plug, Light bulb · wedding → Ring, Wedding ·
    shopping → Shopping cart, Shopping bags · coffee/habits → Hot beverage. Any of the ~1,600 names at
    github.com/microsoft/fluentui-emoji/tree/main/assets works.
  - **Never** objects showing "$" (Money bag, Money with wings, Dollar banknote, Heavy dollar sign). No real
    people, logos or brands. Illustrated, never photo-realistic.

### Palette (changes with every video)
Rotates by video number so the two daily Shorts never share a colour: emerald → royal → ember → plum → ocean →
wine → graphite → magenta (`spec.json` `"theme"` overrides; `classic` is the old navy). The **roles** never
change: accent = key results and the spoken caption word; in-between results; red-ish = costs; muted = labels;
white = inputs. The logo coin stays green on every palette.

### Fixed elements

| Element | Spec |
|---|---|
| Canvas | 1080 × 1920, 30 fps, H.264 CRF 18, AAC 192k, loudness −14 LUFS |
| Background | The video's palette: dark-to-rich gradient, 60 px grid at 4 %, slow glow |
| Logo | Green coin with an ink "£", top-left with **POUND FOR POUND** and *UK MONEY · EXPLAINED WITH DATA* |
| Episode | `#NNN` pill top-right |
| Font | Nunito Black / ExtraBold; Anton for the cover words only |
| Beat chips (y = 305) | THE MATHS · THE TWIST · THE CATCH · ONE THING PEOPLE MISS · THE MYTH · THE TRUTH · BACK THEN · TODAY · WHAT CHANGED · WHO IT AFFECTS · WHAT IT MEANS · MY TAKE |
| Captions | Karaoke, 60 px, spoken word in the accent colour, centred at y = 1365, max 840 px wide |
| Motion | Spring entrances, 0.35 s scene dissolves, numbers pulse when spoken |
| Sound | Original synth bed (ducked), whoosh per scene, pop on numbers, coin on wins, boom on a catch or myth stamp, brand sting on the loop scene |

### Layout grid and safe zones
```
y   0–120   hidden by the app
y 120–235   logo bar + episode + progress            (automatic)
y 276–334   beat chip                                (beat())
y 370–1240  CONTENT ZONE                             x 70–1010; below y 900 keep x < 960
y 1310–1420 captions                                 (automatic)
y 1480–1920 keep empty (title, channel, description overlay)
```
`qa.py` fails the video if anything lands in a hidden zone, if the font lacks a character (→ ✓ ↓ show as boxes:
use words or `L.arrow`), or if frame 0 is empty.

## 4. Words

- **UK-specific, our own work.** ISAs, pensions, the tax year, the Budget, National Insurance, student loans,
  Child Benefit, council tax, the price cap, Bank Rate. Our own calculations and official data. Never remake
  another creator's video; if a topic has no UK-specific angle, don't make it.
- **Education, not advice.** Explain rules, numbers and what to check — never "you should buy/sell X", no
  return promises, no "guaranteed".
- **No persona.** No AI presenter, avatar or character; the narrator never claims to be a person or an expert.
  The only "I" on the channel is the owner's own take (`take_card`, label MY TAKE), in her words.
- British spelling, plain English, ≤ 14 spoken words a sentence (§0). Numbers as `{£50,270|fifty thousand, two
  hundred and seventy pounds}`.
- **Hook formulas** (surprise first — see §0; `<X>` = a figure verified for that video):
  *calc* "The government gives you £<X>… then takes back even more." · "Earn £1 more, and you could lose
  £<X>." · *myth* "Everyone says <belief>. It's wrong." · *since* "In <year>, £<X> bought this. Today it buys
  that." · *news* "From <date>, <thing> changes — and it's <good/bad> news for you."
- **Loop lines** (hand over into sentence 1): "So next time someone turns down a pay rise because of tax,
  remember:" · "Which is why, from April," · "And that's the real reason that"
- **Title:** ≤ 100 characters, the number + curiosity, one or two emoji, ends `#shorts`.
- **First comment:** the comment question + "📩 Send this to <a specific person>" + "Every number is checked
  against official sources." If the pillar has a full video (`pillars.json`), add "Full video: <url>".

## 5. What may change between videos

Each video has its own cover, the next palette and a format different from the last one. Inside the content
zone pick different blocks (value cards, versus, bar chart, line chart, stamps, timelines) and emoji. The frame,
logo, fonts, colour roles, beat chips, cover style, captions, sounds and loop ending never change. New blocks may
be added to `brand.py` in the brand colours.

## 6. Block reference (`from brand import *`)

| Block | Use |
|---|---|
| `cover_hook(L, t, number, sub=, number_at=, kicker=, extra=)` | Scene 1. `kicker` = one short context line under the cover words. |
| `loop_close(L, t, si, comment=)` | Last scene: the loop line, the cover rebuilds; optional comment chip. |
| `verdict_stamp(L, "MYTH", cx, cy, t, start, tone=)` | Rubber-stamp verdict: MYTH / FALSE / TRUE / HALF TRUE. |
| `take_card(L, t, si, lines, label="MY TAKE")` | The owner's own take, gold-edged quote card. |
| `beat(L, key, t, start, sub=, sub_at=)` | Beat chip. Keys: `maths twist catch miss myth truth then today changed who means take`, or free text. |
| `chip(L, label, cx, cy, t, start, tone, size, emoji=, outline=)` | Any pill. Tones: green white red cyan gold. |
| `checked(L, "GOV.UK · …", cx, cy, t, start)` | Trust stamp. |
| `panel(L, cx, cy, w, h, t, start, tone=)` | Glass card. Returns alpha. |
| `value_card(L, cx, cy, w, t, start, emoji, label, value, color=, value_at=, sub=)` | Emoji + label + big value. |
| `versus(L, t, left, right, cy=, h=)` | Two cards + VS coin. Keep above y 900. |
| `timed_line(L, [(text, colour, at), …], cx, cy, size, t)` | Maths line, each token on its own word. |
| `big_number(L, s, cx, cy, t, at=, size=, color=)` | Hero number with glow. |
| `bar_chart(...)`, `line_chart(...)` | Charts (see docstrings). |
| `caveat(L, t, start, lines, cy=)` | Small muted caveat text. |
| `scene_events(extra)` | Standard whooshes + brand sting; add pops/coins/booms on words. |
| `hook`, `your_turn`, `share_close` | Older (brand-v1, 45–60 s) layouts — not used for new videos. |

## 7. The owner's input

- **Videos publish automatically** at their slot (no approval step — the owner's choice). The fact sheet and
  `qa.py` are the safety net.
- **Summary sheet** (the run's final message): title, slot, the full script, every number with how it was worked
  out and its source (`meta.json` → `facts`), the Metricool link. She can change or cancel it before the slot.
- **Her own take:** she can reply with a line; it goes in as a sentence before the loop line + `take_card`.
- **Her own voice** (optional): per-sentence recordings replace the synthetic voice (ROUTINE.md §9).
- **Disclosure:** YouTube "altered or synthetic content" on (`isAiGeneratedContent: true`), TikTok `isAigc`,
  Instagram `isAiGenerated`, whenever the voice is synthetic.

## 8. Measure

`WEEKLY.md`: every Monday, average % viewed and engagement per format from Metricool; formats that
underperform are switched off in `formats.json`. "Viewed vs swiped away" is only in YouTube Studio — the owner
reads it there (Content → Shorts → Analytics) or asks Claude to read it with the browser.
