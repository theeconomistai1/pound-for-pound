# Scheduled run: make and publish one Short for one slot

The channel: **Pound for Pound** — UK money, explained with data. **Two YouTube Shorts a day**, at
**10:00** (morning slot) and **16:00** (afternoon slot) Europe/London — the channel's best morning and
afternoon hours, per Metricool. Each scheduled run makes ONE video for the slot named in its prompt.
The owner wants this fully hands-off: make the video, publish it, report back. No questions to the owner
unless something is broken. Every Short uses the brand template (brand-v1): read `BRAND.md` before writing.

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
Take the first `todo` line in `topics.md`. Next video number = highest `NNN` in `videos/NNN-*` + 1
(sample 002 was published as 002; sample 005 is the brand template's worked example of the next topic). The topics are UK versions of the most-watched personal finance themes: make our own
version — own script, own maths, own examples. Never copy another creator's script, footage, music or
thumbnails, and never use clips of real people (copyright claims, "reused content", no ad money).
If `samples/` already holds a brand-v1 example of this topic (e.g. `samples/005-penny-challenge` for the 1p
challenge), copy it to `videos/NNN-slug` as the starting point, re-check every figure, and publish it as NNN.

## 3. Research (every time)
Check every rule, rate, allowance and threshold against an official source today (gov.uk, HMRC, ONS,
Bank of England, MoneyHelper, NS&I, FCA) with web search / fetch. UK rules change at Budgets and in April.
Compute every number in code (inside `scenes.py`), never by hand. If a figure can't be verified,
mark the topic `blocked: <reason>`, take the next one.

## 4. Write `videos/NNN-slug/` with the brand template (brand-v1)
Read `BRAND.md` first — it is the brand book and it is not optional. Then:
`cp -r template/short videos/NNN-slug` (worked example: `samples/005-penny-challenge/`).
- **spec.json** — 11–16 short sentences, **45–60 seconds** at speed 1.15, gap 0.08, voice `bf_emma`.
  Beats, in this order: **hook** (sentence 1 = the payoff number; sentence 2 opens a loop) → **the example**
  (people, prices, everyday objects) → **the maths** → **the catch / the twist** → **one thing people miss** →
  optional **level up** → short **caveat** → **"Your turn."** comment question with a number answer (never show
  it) → **"Send this to …"** naming a specific person (always the last sentence; no "like and follow").
  Write numbers as `{shown|spoken}` with the spoken part in words. British spelling. Voice it straight away
  (`pipeline/tts2.py`, see `template/short/README.md`) so scenes use real word timings.
- **scenes.py** — `from motion import *`, `from brand import *`, `BRAND = True`. Compute every number at the top
  (and `assert` each spoken figure against its rounded text). Set the **`COVER`** (BRAND.md §3): one or two
  words with the hook word highlighted, and a `hero` / `left` / `right` / `particles` scene that clearly fits
  the subject — no "$" objects. Scene 1 is `cover_hook(...)`. The background palette rotates automatically.
  One scene per beat, built from the brand blocks:
  `hook`, `beat`, `value_card`, `versus`, `timed_line`, `big_number`, `bar_chart`, `line_chart`, `checked`,
  `caveat`, `your_turn`, `share_close` (reference in BRAND.md §6). Every element appears on the word that names
  it (`tk(sentence, "word")`). Show a `checked("GOV.UK · <date>")` stamp when an official figure appears. Keep
  the frame identical; vary only the content blocks and emoji between videos. Don't use characters the font
  lacks (→ ✓ ↓): use words or `L.arrow`.
- **meta.json** — title (≤100 chars, the number + curiosity, one or two emoji, ends `#shorts`), description
  (every number said in the video, assumptions, sources as plain URLs or gov.uk paths, the "Your turn" question,
  the "Send this to" line, "General education, not financial advice.", "Music and sound effects: original, made
  for this channel.", 4–5 hashtags), `first_comment` (the share prompt again + "every number checked"),
  tags (6–10), assumptions, sources, slot.

## 5. Build and check
```bash
KEEP_VOICE=1 pipeline/build_v3.sh videos/NNN-slug     # drop KEEP_VOICE=1 if spec.json changed since voicing
python3 -I pipeline/qa.py videos/NNN-slug             # must end RESULT: PASS
```
- If tts prints `MISSING`, reword the spoken text or add the word to `EXTRA` in `pipeline/tts.py`.
- `qa.py` checks the script shape, length, that the voice starts at 0 s, frame 0 shows the hook, every safe
  zone on every quarter-second, missing glyphs and meta.json. Fix every FAIL; act on WARNs where sensible.
- Read `build/contact.png` (frame 0 = the cover, the end of every scene, the loop frame). The cover must read
  at a glance on a phone grid and the scene must obviously match the topic; no overlapping or clipped text,
  nothing on top of chart lines, numbers match meta.json, caveat readable. For a closer look:
  `python3 -I pipeline/make_v3.py videos/NNN-slug stills 3,10,20`. Re-render after fixes.
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
2. Metricool `getBrandSettings`: note which networks are connected (`networksData` keys: `youtubeData`,
   `tiktokData`, `instagramData`, `facebookData`). Post the same video to **every connected one** of those in
   one `createScheduledPost`: blogId `7523442`, date today at the run's slot (10:00 or 16:00 Europe/London; if
   that has passed, 10 minutes from now), `info`:
   `providers` = `[{"network":"youtube"}]` plus `tiktok` / `instagram` / `facebook` if connected,
   `media [<URL>]`, `text` = description, `firstCommentText` = meta `first_comment`, `autoPublish true`,
   `draft false`, `publicationDate {"dateTime": "...", "timezone": "Europe/London"}`,
   `youtubeData {"title", "type":"short", "privacy":"public", "madeForKids":false, "isAiGeneratedContent":true,
   "category":"EDUCATION", "tags"}`, and only for connected networks:
   `tiktokData {"title": <title without #shorts>, "privacyOption":"PUBLIC_TO_EVERYONE", "isAigc":true}`,
   `instagramData {"type":"REEL", "showReelOnFeed":true, "isAiGenerated":true}`,
   `facebookData {"type":"REEL", "title": <title without #shorts>}`.
   If the call is rejected because of `firstCommentText` or one network, retry once without that part and say
   so in the report. **Cover upload: OFF.** (Frame 0 is the cover, which YouTube can use.) When the owner
   confirms the channel can set Shorts thumbnails, switch this to ON: host `build/cover.jpg` on the upload
   branch next to the video and pass its URL as `videoThumbnailUrl`. Check the response: `media` must now point at `static.metricool.com` (Metricool keeps its
   own copy).
3. Empty the upload branch straight away so the file is no longer in the repository:
   ```bash
   cd "$U" && git checkout -q --orphan empty && git rm -q --cached video-NNN.mp4 && rm -f video-NNN.mp4
   git -c user.name=Claude -c user.email=noreply@anthropic.com commit -q --allow-empty -m "Clear temporary upload"
   git push -q -f https://github.com/theeconomistai1/pound-for-pound empty:upload
   ```

## 7. Record
- Copy `build/cover.jpg` to `covers/NNN.jpg` (the cover gallery).
- Mark the topic `done (NNN)` in `topics.md`; commit the video folder and the cover (build/ is ignored) and push to `main`
  (`git fetch origin main && git rebase origin/main` first — the other slot's run may have pushed).
- Studio page https://claude.ai/artifact/2SbNVqQh6hMzCyCmHzNkaj — with `ArtifactData`, set `videos/short-NNN`:
  `{title, type:"Short", status:"scheduled", publishAt (ISO with offset), durationSec, description, tags, plannerUrl}`.
  Also check earlier posts with Metricool `getScheduledPosts` (extendedRange true, last 2 days): for each that is
  PUBLISHED on YouTube, update its row to `status:"published"` and `youtubeUrl` (the post's `publicUrl`).
  If the Artifact tools are unavailable, skip this step.
- Finish with a two-line summary: the video's title and publish time, or what went wrong.

## Older styles
Video 001 used `pipeline/build.sh` + `vidlib.py` (yellow-on-violet, kinetic captions). Videos 002–004 used the
pre-brand house style (`motion.frame`, no `BRAND = True`). From 005 every video uses brand-v1 (`BRAND.md`).
