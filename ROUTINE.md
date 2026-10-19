# Daily run: make and publish one Short

The channel: **Pound for Pound** — UK money, explained with data. One YouTube Short a day,
published at **16:00 Europe/London** (the channel's best hour every day, per Metricool).
The owner wants this fully hands-off: make the video, publish it, report back. No questions to the owner
unless something is broken.

## 0. Set up
```bash
git clone --depth 1 https://github.com/theeconomistai1/pound-for-pound /home/claude/pound-for-pound   # if not already there
cd /home/claude/pound-for-pound && pipeline/setup_assets.sh
```

## 1. Pick the topic
Take the first `todo` line in `topics.md`. Next video number = highest `videos/NNN-*` folder + 1.

## 2. Research (every time)
Check every rule, rate, allowance and threshold against an official source today (gov.uk, HMRC, ONS,
Bank of England, MoneyHelper, NS&I, FCA) with web search / fetch. UK rules change at Budgets and in April.
Compute every number in code (inside `scenes.py`), never by hand. If a figure can't be verified,
mark the topic `blocked: <reason>`, take the next one.

## 3. Write `videos/NNN-slug/`
Copy the structure of `videos/001-five-pounds-a-day/` and make it new — new script, new data, new visuals:
- **spec.json** — 11–16 short sentences, 35–50 seconds at speed 1.15, voice `bf_emma`.
  Sentence 1 is the hook and states the payoff ("{£5|Five pounds} a day could grow to …").
  Write numbers as `{shown|spoken}` with the spoken part in words. British spelling.
  Second-to-last sentence: a plain caveat when the video illustrates investing, tax or debt.
  Last sentence: a follow call, worded differently each day.
- **scenes.py** — `from vidlib import *`, one scene per sentence, defines `draw`, `events`, `shakes`, `NO_PUNCH`.
  Visual rules: big text visible from frame 0; key numbers in YELLOW with `glow_text`; count-ups for money;
  charts in GROWTH (green) / PAID (orange) with direct labels; content between y=300 and y=1150
  (captions sit at ~1300, YouTube's buttons cover the right edge below that); one sound cue per scene change,
  pop/coin/boom on reveals. Vary the scene types from recent videos (stamps, bars, timelines, versus splits,
  counters, checklists) so no two videos look templated.
- **meta.json** — title (≤100 chars, ends with `#shorts`), description (key numbers, assumptions, sources as
  plain URLs, "General education, not financial advice.", "Music and sound effects: original, made for this channel.",
  4–5 hashtags), tags (6–10), assumptions, sources.

## 4. Build and check
```bash
pipeline/build.sh videos/NNN-slug
python3 -I pipeline/make.py videos/NNN-slug stills 0.05,3,8,14,20,26,32,40
```
- If tts prints `MISSING`, reword the spoken text or add the word to `EXTRA` in `pipeline/tts.py`.
- Read every still: no overlapping or clipped text, numbers match meta.json, caveat readable. Fix and rebuild.
- Do not publish a video with a wrong number or broken frame. Report it instead.

## 5. Publish
1. Host the file for a few minutes on the `upload` branch (releases and branch deletion are blocked for
   cloud sessions, so this branch is reused and emptied each time):
   ```bash
   U=$(mktemp -d) && cd "$U" && git init -q && git checkout -q --orphan upload
   cp /home/claude/pound-for-pound/videos/NNN-slug/build/video.mp4 video-NNN.mp4
   git add video-NNN.mp4 && git -c user.name=Claude -c user.email=noreply@anthropic.com commit -qm "Temporary upload of video NNN"
   git push -q -f https://github.com/theeconomistai1/pound-for-pound upload:upload
   ```
   Media URL: `https://raw.githubusercontent.com/theeconomistai1/pound-for-pound/upload/video-NNN.mp4`
2. Metricool `createScheduledPost`: blogId `7523442`, date today 16:00 Europe/London
   (if that has passed, 10 minutes from now), `info`:
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

## 6. Record
- Mark the topic `done (NNN)` in `topics.md`; commit the video folder (build/ is ignored) and push to `main`.
- Studio page https://claude.ai/artifact/2SbNVqQh6hMzCyCmHzNkaj — with `ArtifactData`, set `videos/<NNN>`:
  `{title, type:"Short", status:"scheduled", publishAt (ISO with offset), durationSec, description, tags, plannerUrl}`.
  If the Artifact tools are unavailable, skip this step.
- Finish with a two-line summary: the video's title and publish time, or what went wrong.
