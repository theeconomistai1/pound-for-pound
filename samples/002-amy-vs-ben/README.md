# 002 — Amy vs Ben (new motion-design style, published 19 Oct 2026)

Sample in the format from the owner's brief: navy-to-purple grid background, Nunito Black, green accents and
cyan intermediate results, top bar with progress, karaoke captions (spoken word in green), spring entrances,
cards, 3D emoji (Microsoft Fluent Emoji, MIT licence) and a "your turn" comment question.

Build (assets from pipeline/setup_assets.sh, plus Nunito from github.com/googlefonts/nunito):
```bash
export MOTION_FONT=/path/to/Nunito[wght].ttf MOTION_EMOJI=samples/002-amy-vs-ben/emoji
python3 -I pipeline/tts2.py $P4P_ASSETS samples/002-amy-vs-ben/spec.json build/voice_raw.wav build/timings.json
python3 -I samples/002-amy-vs-ben/render_v3.py <dir-with-build/> events|stills|render
```
Music: audio_mix_v3.py with `--bpm 100 --gain 0.2`.
