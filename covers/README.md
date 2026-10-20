# Cover gallery

One cover per video: frame 0 of the Short (see BRAND.md §3). Scheduled runs add `NNN.jpg` here.
Covers for videos published before covers existed were made with `pipeline/cover.py`:

| Video | Words (highlight) | Palette | Scene |
|---|---|---|---|
| 001 | **£5** DAILY | ember | hero Hot beverage · left Calendar · right Chart increasing · particles Coin |
| 002 | START **EARLY** | plum | hero Hourglass not done · left Woman · right Man · particles Coin |
| 003 | **CHILD** BENEFIT | ocean | hero Baby · left Graduation cap · right Chart increasing · particles Coin |
| 004 | **MILLIONAIRE** | royal | hero £ · left Trophy · right Gem stone · particles Coin |
| 005 (sample) | **1p** CHALLENGE | emerald | hero Jar filled with Coin · left Calendar · right Pound banknote · particles Coin |

e.g. `python3 -I pipeline/cover.py covers/001.jpg --words "£5" "DAILY" --highlight 0 --theme ember --hero "Hot beverage" --left "Calendar" --right "Chart increasing" --particles "Coin"`
