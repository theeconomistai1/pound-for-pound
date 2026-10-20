# Prompts to give Claude

The brand and the method live in this repo (`BRAND.md`, `ROUTINE.md`, `pipeline/brand.py`, `template/short/`),
so a prompt only has to point at them. Turn on the Metricool connector in the chat when you want it published.

## 1. Make one Short now (any topic)

```
Make one YouTube Short for my channel Pound for Pound (UK money, explained with data).

Repo: theeconomistai1/pound-for-pound — attach it with push access and clone it to /home/claude/pound-for-pound.
Read BRAND.md and ROUTINE.md and follow them exactly: brand-v1 template (template/short, worked example
samples/005-penny-challenge), every figure verified against an official source today, qa.py must PASS.

Topic: [your topic — or "the next todo in topics.md"]
Send-this-to line: [who should viewers send it to — or "your choice"]
Publish: [today at HH:MM Europe/London | in Metricool for my review only | don't publish, just send me the video]

Send me the finished video and the contact sheet when it's ready.
```

## 2. Steer a video (optional brief — paste under the prompt above)

```
Hook number: [e.g. £667.95 from 1p a day]
Open loop (sentence 2): [e.g. But most people quit in December.]
Real-life example: [people, prices or objects]
The catch / twist: [the surprise]
One thing people miss: [the tip]
Your turn question: [has a number answer; Claude never shows it]
Send this to: [a specific person and why]
```

## 3. The daily scheduled tasks

Two scheduled tasks run every day (07:45 for the 10:00 slot, 12:47 for the 16:00 slot). Each one clones the
repo, follows `ROUTINE.md` for its slot and reports two lines back. Nothing to paste — edit `ROUTINE.md`,
`BRAND.md` or `topics.md` to change what they do, and add topics as `- todo — ...` lines in `topics.md`.

## 4. Change the brand

```
In theeconomistai1/pound-for-pound, change the brand kit (pipeline/brand.py and BRAND.md): [what to change].
Keep every rule in BRAND.md §2. Re-render samples/005-penny-challenge, run qa.py, and send me the
contact sheet before pushing to main.
```
