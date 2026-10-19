#!/usr/bin/env bash
# Build one video end to end: voice -> sound cues -> voice polish -> music mix -> render.
# Usage: pipeline/build.sh videos/NNN-slug
set -euo pipefail
V="$1"
P="$(cd "$(dirname "$0")" && pwd)"
A="${P4P_ASSETS:-$HOME/.p4p-assets}"
[ -f "$A/fonts/Inter-Black.otf" ] && export P4P_FONTS="$A/fonts/"
B="$V/build"
mkdir -p "$B"
python3 -I "$P/tts2.py" "$A" "$V/spec.json" "$B/voice_raw.wav" "$B/timings.json"
TOTAL=$(python3 -I "$P/make.py" "$V" events)
ffmpeg -v error -y -i "$B/voice_raw.wav" -af "highpass=f=75,equalizer=f=220:t=q:w=1:g=-2,equalizer=f=3200:t=q:w=1.2:g=3.5,equalizer=f=9000:t=h:w=2000:g=2,acompressor=threshold=-20dB:ratio=3.5:attack=4:release=90:makeup=4,aresample=44100" -ar 44100 "$B/voice_44k.wav"
python3 -I "$P/audio_mix.py" "$B/voice_44k.wav" "$B/events.json" "$TOTAL" "$B/mix_raw.wav"
ffmpeg -v error -y -i "$B/mix_raw.wav" -af "loudnorm=I=-14:TP=-1.2:LRA=9" -ar 44100 "$B/mix.wav"
python3 -I "$P/make.py" "$V" render
