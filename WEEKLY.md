# Weekly performance check (Mondays)

Goal: keep the formats that hold viewers and drop the ones that don't (BRAND.md §8).

1. Clone the repo (push access) to /home/claude/pound-for-pound.
2. Metricool `getAnalyticsDataByMetrics`, brandId 7523442, the **last 28 days** (Europe/London), metrics
   `YTVP17` title, `YTVP04` video id, `YTVP05` url, `YTVP02` published, `YTVP06` views, `YTVP08` average view
   duration (s), `YTVP07` watch minutes, `YTVP09` likes, `YTVP11` comments, `YTVP12` shares.
3. Match each video to `videos/NNN-*/meta.json` by title → `format`, `pillar`, `durationSec` (older videos without
   a format count as `legacy`). Average % viewed = average view duration ÷ duration (loops can push it over 100%).
4. Per format: number of videos, median average % viewed, median views, shares and comments per 1,000 views.
   Compute in code and save the table to `reports/<YYYY>-W<ww>.md` with the raw rows.
5. Decide, only for formats with at least 3 videos in the window:
   - switch a format **off** in `formats.json` if its median % viewed is below 70% of the channel median **and**
     its shares per 1,000 views are below the channel median; never leave fewer than two formats on;
   - switch a format back **on** if it has been off for 4 weeks (re-test it).
   Write the reasons in the report. Commit `formats.json` and the report; push to `main`.
6. Final message (reaches the owner's phone), five lines: best format, weakest format, what changed in
   `formats.json`, the week's top Short (views, % viewed), and: "Viewed vs swiped away is only in YouTube Studio
   (Content → Shorts → a Short → Analytics → Audience retention). Reply with this week's numbers, or ask Claude
   to read them with the browser."
