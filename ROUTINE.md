# Scheduled run: make and publish one Short for one slot

The channel: **Pound for Pound** — UK money, explained with data. **Two YouTube Shorts a day**, at
**10:00** (morning slot) and **16:00** (afternoon slot) Europe/London — the channel's best morning and
afternoon hours, per Metricool. Each scheduled run makes ONE video for the slot named in its prompt.
The owner wants this fully hands-off: make the video, publish it, report back. No questions to the owner
unless something is broken.

## 0. Set up
```bash
git clone --depth 1 https://github.com/theeconomistai1/pound-for-pound /home/claude/pound-for-pound   # if not already there
cd /home/claude/pound-for-pound && pipeline/setup_assets.sh
```

## 1. Is the slot already booked?
Metricool `getScheduledPosts` (brandId 7523442, timezone Europe/London, extendedRange true) for today.
If a YouTube post is already booked within 30 minutes of this run's slot, stop: report "slot already booked"
with its title. (The owner or another session may have made it by hand.)

## 2. Pick the topic
Take the first `todo` line in `topics.md`. Next video number = highest `NNN` across `videos/NNN-*` and
`samples/NNN-*` + 1. The topics are UK versions of the most-watched personal finance themes: make our own
version — own script, own maths, own examples. Never copy another creator's script, footage, music or
thumbnails, and never use clips of real people (copyright claims, "reused content", no ad money).

## 3. Research (every time)
Check every rule, rate, allowance and threshold against an official source today (gov.uk, HMRC, ONS,
Bank of England, MoneyHelper, NS&I, FCA) with web search / fetch. UK rules change at Budgets and in April.
Compute every number in code (inside `scenes.py`), never by hand. If a figure can't be verified,
mark the topic `blocked: <reason>`, take the next one.

## 4. Write `videos/NNN-slug/` in the house style
Template: `videos/003-child-benefit-invested/` (also `samples/002-amy-vs-ben/`). Engine: `pipeline/motion.py`.
- **spec.json** — 14–20 short sentences, 60–90 seconds at speed 1.1, gap 0.1, voice `bf_emma`.
  Story shape: **hook with the payoff number** (sentence 1–2) → **real-life example** with people, prices or
  everyday objects → **the maths, step by step** → **the twist / why** → **one extra tip people miss** →
  **"Your turn" comment question** (never show its answer) → **plain caveat** → **follow / like call**
  (worded differently each time). Write numbers as `{shown|spoken}` with the spoken part in words. British spelling.
- **scenes.py** — `from motion import *`; define `SCENES` (sentence ranges), `DRAW` (one function per scene,
  `draw(L, t)`), `events()`. Use the components: `L.badge`, `L.price_card`, `L.card(verified_at=…)`,
  `L.math_line` (token-by-token), `L.emoji` (3D emoji in `assets/emoji/`), `L.arrow`, count-ups, and a
  supersampled chart like `chart()` in 003. Every element appears on the timestamp of the word that names it
  (`tk(sentence, "word")`). Colours: green = key results, cyan = in-between results, white = inputs,
  muted = labels. Content between y=250 and y=1100; captions sit at y≈1190; keep the bottom 250px empty;
  keep labels off chart lines. Vary scene types between videos (cards, versus cards, timelines, charts,
  checklists, challenges, calculators) so no two videos look templated.
- **meta.json** — title (≤100 chars, curiosity + the number, one or two emoji, ends with `#shorts`),
  description (key numbers, assumptions, sources as plain URLs or gov.uk paths, the comment question,
  "General education, not financial advice.", "Music and sound effects: original, made for this channel.",
  4–5 hashtags), tags (6–10), assumptions, sources, slot.

## 5. Build and check
```bash
pipeline/build_v3.sh videos/NNN-slug
python3 -I pipeline/make_v3.py videos/NNN-slug stills 0.05,4,10,18,26,34,42,50,58,66,74,82
```
- If tts prints `MISSING`, reword the spoken text or add the word to `EXTRA` in `pipeline/tts.py`.
- Read every still: no overlapping or clipped text, nothing on top of chart lines, numbers match meta.json,
  caveat readable. Fix and re-render stills; rebuild once fixed.
- Do not publish a video with a wrong number or broken frame. Report it instead.

## 6. Publish
1. Host the file for a few minutes on the `upload` branch (releases and branch deletion are blocked for
   cloud sessions, so this branch is reused and emptied each time):
   ```bash
   U=$(mktemp -d) && cd "$U" && git init -q && git checkout -q --orphan upload
   cp /home/claude/pound-for-pound/videos/NNN-slug/build/video.mp4 video-NNN.mp4
   git add video-NNN.mp4 && git -c user.name=Claude -c user.email=noreply@anthropic.com commit -qm "Temporary upload of video NNN"
   git push -q -f https://github.com/theeconomistai1/pound-for-pound upload:upload
   ```
   Media URL: `https://raw.githubusercontent.com/theeconomistai1/pound-for-pound/upload/video-NNN.mp4`
2. Metricool `createScheduledPost`: blogId `7523442`, date today at the run's slot (10:00 or 16:00
   Europe/London; if that has passed, 10 minutes from now), `info`:
   `providers [{"network":"youtube"}]`, `media [<URL>]`, `text` = description, `autoPublish true`, `draft false`,
   `publicationDate {"dateTime": "...", "timezone": "Europe/London"}`,
   `youtubeData {"title", "type":"short", "privacy":"public", "madeForKids":false, "isAiGeneratedContent":true,
   "category":"EDUCATION", "tags"}`.
   Check the response: `media` must now point at `static.metricool.com` (Metricool keeps its own copy).
3. Empty the upload branch straight away so the file is no longer in the repository:
   ```bash
   cd "$U" && git checkout -q --orphan empty && git rm -q --cached video-NNN.mp4 && rm -f video-NNN.mp4
   git -c user.name=Claude -c user.email=noreply@anthropic.com commit -q --allow-empty -m "Clear temporary upload"
   git push -q -f https://github.com/theeconomistai1/pound-for-pound empty:upload
   ```

## 7. Record
- Mark the topic `done (NNN)` in `topics.md`; commit the video folder (build/ is ignored) and push to `main`
  (`git fetch origin main && git rebase origin/main` first — the other slot's run may have pushed).
- Studio page https://claude.ai/artifact/2SbNVqQh6hMzCyCmHzNkaj — with `ArtifactData`, set `videos/short-NNN`:
  `{title, type:"Short", status:"scheduled", publishAt (ISO with offset), durationSec, description, tags, plannerUrl}`.
  Also check earlier posts with Metricool `getScheduledPosts` (extendedRange true, last 2 days): for each that is
  PUBLISHED on YouTube, update its row to `status:"published"` and `youtubeUrl` (the post's `publicUrl`).
  If the Artifact tools are unavailable, skip this step.
- Finish with a two-line summary: the video's title and publish time, or what went wrong.

## Older style
Videos 001 used `pipeline/build.sh` + `vidlib.py` (yellow-on-violet, kinetic captions). New videos use the
house style above.
