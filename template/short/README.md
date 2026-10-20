# Short template (brand-v1)

1. `cp -r template/short videos/NNN-slug` (NNN = next number across `videos/` and `samples/`).
2. Write `spec.json` first (beats in BRAND.md §1), then voice it so you have real word timings:
   `python3 -I pipeline/tts2.py ~/.p4p-assets videos/NNN-slug/spec.json videos/NNN-slug/build/voice_raw.wav videos/NNN-slug/build/timings.json`
3. Fill `scenes.py`: compute every figure at the top, then one scene per beat with the brand blocks.
   Every element appears on its word: `tk(sentence_index, "word")`.
4. Fill `meta.json` (title, description with every number said, first_comment, tags, assumptions, sources).
5. `KEEP_VOICE=1 pipeline/build_v3.sh videos/NNN-slug` then `python3 -I pipeline/qa.py videos/NNN-slug`
   until `RESULT: PASS`, and read `build/contact.png`.

Worked example: `samples/005-penny-challenge/`.
