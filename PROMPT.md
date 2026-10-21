# Prompts to give Claude

The method lives in this repo (`BRAND.md`, `ROUTINE.md`, `pipeline/`, `template/`), so a prompt only has to
point at it. Turn on the Metricool connector in the chat when you want it booked.

## 1. Make one Short now

```
Make one YouTube Short for my channel Pound for Pound (UK money, explained with data).

Repo: theeconomistai1/pound-for-pound — attach it with push access and clone it to /home/claude/pound-for-pound.
Read BRAND.md and ROUTINE.md and follow them: brand-v2 (20–40 s, loop line, format rotation), UK-specific,
every figure verified against an official source today, qa.py must PASS.

Topic: [your topic — or "the next one in topics.md"]
Format: [calc | myth | since | news — or "your choice"]
My take (optional): [one line in your own words]
Book it: [for my review at HH:MM today | don't book, just send me the video]

Send me the review sheet and the video when it's ready.
```

## 2. Reply to a review sheet (in the run's chat)

- `approve`
- `change line 3 to: …`
- `my take: …` (added before the loop line, shown on a MY TAKE card)
- `reject: <reason>`

## 3. Use your own voice

Record each sentence of the script as its own clip (phone voice memo is fine), name them `01`, `02`, … in order
and attach them in the run's chat with "use my voice". Claude puts them in `videos/NNN-slug/voice/` and rebuilds.

## 4. The scheduled tasks

- Morning (07:45 for 10:00) and afternoon (12:47 for 16:00): prepare one Short each, booked for your review.
- Monday morning: the weekly performance check (`WEEKLY.md`).
Edit `ROUTINE.md`, `BRAND.md`, `topics.md`, `formats.json` or `pillars.json` to change what they do.

## 5. Change the brand

```
In theeconomistai1/pound-for-pound, change the brand kit (pipeline/brand.py and BRAND.md): [what to change].
Re-render samples/v2-myth-pay-rise, run qa.py, and send me the contact sheet before pushing to main.
```
