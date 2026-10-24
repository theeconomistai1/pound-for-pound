# Scheduled run: make and publish one Short for one slot

The channel: **Pound for Pound** — UK money, explained with data. Two Shorts a day, at **10:00** and **16:00**
Europe/London. Each scheduled run makes ONE video for the slot named in its prompt and **schedules it to publish
automatically** at that slot (the owner chose no approval step, 21 Oct 2026). Read `BRAND.md` first (brand-v2) —
including *why*: YouTube won't monetise generic, repetitive or template-based channels, so every video must be
UK-specific, our own maths and data, and a different format from the last one. With no human check before
publishing, the fact sheet and `qa.py` are the safety net: never publish a number you couldn't verify.

Don't ask the owner questions mid-run. Finish, publish, and send the summary sheet (§7).

## 0. Set up
```bash
git clone --depth 1 https://github.com/theeconomistai1/pound-for-pound /home/claude/pound-for-pound   # if not already there
cd /home/claude/pound-for-pound && pipeline/setup_assets.sh
```

## 1. Is the slot already booked?
Metricool `getScheduledPosts` (brandId 7523442, timezone Europe/London, extendedRange true) for today. If a
YouTube post is already booked within 30 minutes of this run's slot, stop and
report "slot already booked" with its title.

## 2. Pick the topic
Lines in `topics.md` look like `- todo · <format> · <pillar> — <topic>` (optional `· sample: <path>`,
`· from: YYYY-MM-DD` for news).
1. **News first:** if a UK money event happened in the last 2 days (Budget or fiscal event, Bank of England rate
   decision, Ofgem price cap announcement, new tax year), make a `news` video about it — add the line if missing.
   A `news` line with `from:` is only taken on/after that date and within 3 days of the event.
2. Otherwise take the first `todo` line whose format (a) is not the format of the last video in `videos/` (its
   `spec.json` `format`) and (b) is `true` in `formats.json`.
3. Never remake another creator's video. If a topic has no UK-specific angle, mark it
   `skipped: not UK-specific` and take the next.
4. **Answer the three questions first** (BRAND.md §0b): why would people watch to the end, why would they
   comment or share, why would they follow? Write them as `brief` in meta.json before the script. If there's
   no good answer, find a sharper angle; if there still isn't one, mark the topic `skipped: weak angle — <why>`
   and take the next.
   Then plan the **dopamine loop** (BRAND.md §0c): `brief.risk` (who · stake · deadline) and `brief.loops`
   (at least two: question → twist → new question).
5. Next video number = highest `NNN` in `videos/` + 1. If the line names a `sample:`, copy that folder to
   `videos/NNN-slug` as the starting point and re-verify everything.

## 3. Research (every time)
Check every rule, rate, allowance and threshold against an official source today (gov.uk, HMRC, ONS, Bank of
England, MoneyHelper, NS&I, FCA, Ofgem, OBR) with web search / fetch. For `since` videos, take the data series
from the official source and paste it into `scenes.py` with its URL. Compute every number in code (`scenes.py`),
never by hand, and `assert` each spoken figure against its rounded text. If a figure can't be verified, mark the
topic `blocked: <reason>` and take the next. Record every number in `meta.json` → `facts`.

## 4. Write `videos/NNN-slug/` (brand-v2)
`cp -r template/<format> videos/NNN-slug`, then:
- **spec.json** — `format`, 6–10 sentences, **20–40 seconds** at speed 1.15, gap 0.08, voice `bf_emma`.
  Sentence 1 = the surprise hook, with a number (BRAND.md §0: simple and gripping — max 5 numbers said, no
  decimals or equations, ≤ 14 words a sentence, a re-hook every 5–8 s). Follow the format's beats (BRAND.md §1), told as the dopamine loop (BRAND.md §0c): risk in the
  first 3 s, at least two question → twist loops joined by a rehook, and `"steps"` labelling every sentence. **Last sentence = the loop line**,
  ending on a hand-over (":" "," or "…") that runs into sentence 1. No spoken calls to action (like, follow,
  share, comment, send). Education, not advice; no persona (BRAND.md §4). Numbers as `{shown|spoken}`.
  Voice it straight away for real word timings:
  `python3 -I pipeline/tts2.py ~/.p4p-assets videos/NNN-slug/spec.json videos/NNN-slug/build/voice_raw.wav videos/NNN-slug/build/timings.json`
- **scenes.py** — `COVER` (one or two words, the hook word highlighted, a scene that clearly fits the subject,
  no "$" objects), `cover_hook` first, `loop_close` last, the format's blocks between. Every element on its word
  (`tk(sentence, "word")`). A `checked(...)` stamp on official figures. Vary blocks and emoji from recent videos.
- **meta.json** — `brief` (written first, step 2.4; every field answered), `format`, `pillar`, title (≤100 chars, the number + curiosity, one or two emoji, ends
  `#shorts`), description (every number said, sources as URLs or gov.uk paths, the comment question, the
  "📩 Send this to …" line, assumptions, "General education, not financial advice.", "Music and sound effects:
  original, made for this channel.", 4–5 hashtags), `comment_question`, `first_comment`, tags (6–10),
  `facts` (every number in the script: figure exactly as written, how, source, checked date), assumptions,
  sources, `review` (`status: "scheduled"`). If `pillars.json` has a URL for the pillar, add
  "Full video: <url>" to the description and first comment.

## 5. Build and check
```bash
KEEP_VOICE=1 pipeline/build_v3.sh videos/NNN-slug     # drop KEEP_VOICE=1 if spec.json changed since voicing
python3 -I pipeline/qa.py videos/NNN-slug             # must end RESULT: PASS; fix every WARN that cites BRAND.md §0 or §0b
```
- If tts prints `MISSING`, reword the spoken text or add the word to `EXTRA` in `pipeline/tts.py`.
- `qa.py` checks length (20–40 s), sentence count, format rotation, the hook, the loop line, the fact sheet,
  safe zones on every quarter-second, glyphs, the cover and meta.json. Fix every FAIL.
- Read `build/contact.png`: the cover reads at a glance and fits the topic; no overlapping or clipped text;
  numbers match `facts`; the last frame matches frame 0. Fix and rebuild.
- Never book a video with a wrong number or a broken frame. Report it instead.

## 6. Publish (scheduled, automatic)
1. Host the file for a few minutes on the `upload` branch (releases and branch deletion are blocked for cloud
   sessions, so this branch is reused and emptied each time):
   ```bash
   U=$(mktemp -d) && cd "$U" && git init -q && git checkout -q --orphan upload
   cp /home/claude/pound-for-pound/videos/NNN-slug/build/video.mp4 video-NNN.mp4
   git add video-NNN.mp4 && git -c user.name=Claude -c user.email=noreply@anthropic.com commit -qm "Temporary upload of video NNN"
   git push -q -f https://github.com/theeconomistai1/pound-for-pound upload:upload
   ```
   Media URL: `https://raw.githubusercontent.com/theeconomistai1/pound-for-pound/upload/video-NNN.mp4`
2. Metricool `getBrandSettings`: note the connected networks (`networksData`). Build `info` for every connected
   one of YouTube / TikTok / Instagram / Facebook: `providers`, `media [<URL>]`, `text` = description,
   `firstCommentText` = `first_comment`, `draft false`, `publicationDate {"dateTime": "<today> 10:00:00 or
   16:00:00", "timezone": "Europe/London"}` (if the slot has passed: 30 minutes from now),
   `youtubeData {"title", "type":"short", "privacy":"public", "madeForKids":false, "isAiGeneratedContent":true,
   "category":"EDUCATION", "tags"}`, and if connected `tiktokData {"title": <title without #shorts>,
   "privacyOption":"PUBLIC_TO_EVERYONE", "isAigc":true}`, `instagramData {"type":"REEL", "showReelOnFeed":true,
   "isAiGenerated":true}`, `facebookData {"type":"REEL", "title": <title without #shorts>}`.
   (Set the AI flags to false only for a video voiced by the owner with no synthetic voice.)
3. `createScheduledPost` with that `info` and **`autoPublish true`**. If the call is rejected because of
   `firstCommentText` or one network, retry once without that part and say so in the summary. Check the
   response: `media` must point at `static.metricool.com`. Keep the `plannerUrl`.
4. Empty the upload branch straight away:
   ```bash
   cd "$U" && git checkout -q --orphan empty && git rm -q --cached video-NNN.mp4 && rm -f video-NNN.mp4
   git -c user.name=Claude -c user.email=noreply@anthropic.com commit -q --allow-empty -m "Clear temporary upload"
   git push -q -f https://github.com/theeconomistai1/pound-for-pound empty:upload
   ```
   Cover upload is OFF (frame 0 is the cover). When the owner confirms her channel can set Shorts thumbnails,
   host `build/cover.jpg` next to the video and pass it as `videoThumbnailUrl`.

## 7. Record and report
- Add `"durationSec"` (from `build/timings.json` total) to meta.json. Copy `build/cover.jpg` to `covers/NNN.jpg`.
  Mark the topic `done (NNN)` in `topics.md`. Commit the video
  folder and the cover (build/ is ignored); `git fetch origin main && git rebase origin/main`; push to `main`.
- Studio page https://claude.ai/artifact/2SbNVqQh6hMzCyCmHzNkaj — with `ArtifactData`, set `videos/short-NNN`:
  `{title, type:"Short", format, status:"scheduled", publishAt (ISO with offset),
  durationSec, description, tags, plannerUrl}`. Also check posts from the last 2 days with `getScheduledPosts`
  (extendedRange true): published ones → `status:"published"`, `youtubeUrl` (the post's `publicUrl`). If the Artifact tools are unavailable, skip the studio page.
- **The final message is the summary sheet** (it reaches the owner's phone). Keep it in this order:
  1. `SCHEDULED: <title> — publishes <slot>, <format>, <seconds> s`.
  2. The script, numbered.
  3. Every number: figure — how — source link.
  4. The loops in one line each (question → twist), then the cover words, the comment question, and the brief in three lines: **Watch:** <hook + feeling> ·
     **Comment/share:** <take-sides moment + who they send it to> · **Follow:** <why_follow>.
  5. The Metricool `plannerUrl`. If the pillar has a full video in `pillars.json`: "Set it as this Short's
     Related video in YouTube Studio once it's live."
  6. "It publishes automatically. To change it before then, reply here with **change** <line> to <text>,
     **my take:** <your line>, or **cancel**."

## 8. If the owner replies (in the run's chat, or a new one)
- **change …** / **my take: …** before the slot → edit spec.json (a take becomes one sentence before the loop
  line, shown with `take_card`), re-voice, rebuild, `qa.py` PASS, re-host the file, `updateScheduledPost` with the
  new media (same uuid, full original content otherwise), empty the upload branch, push, send a new summary.
  After it has published, the video can't be swapped: say so and offer to make a corrected follow-up.
- **cancel** before the slot → `updateScheduledPost` → `draft true`, mark the topic `cancelled (NNN): <reason>`,
  set the studio row to `status:"cancelled"`. After publishing: she can delete or hide it in YouTube Studio.

## 9. The owner's own voice (optional)
If `videos/NNN-slug/voice/` holds her recordings (`01.m4a`, `02.m4a`, … one per sentence, in order), the build
uses them instead of the synthetic voice (`pipeline/owner_voice.py`; see its docstring). Then set
`review.owner_voice true`, and the AI-content flags may be false if nothing else in the video is synthetic.

## Older styles
Video 001: `pipeline/build.sh` + `vidlib.py`. Videos 002–004: pre-brand house style. brand-v1 (45–60 s, share
line last): `samples/005-penny-challenge`. From now on every video is brand-v2.
