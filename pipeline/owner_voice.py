"""Use the owner's own recorded voice instead of the synthetic one.

  python3 -I pipeline/owner_voice.py <video_dir>

<video_dir>/voice/ holds one recording per sentence of spec.json, in order: 01.m4a, 02.m4a, … (any format ffmpeg
reads: m4a, mp3, wav, ogg, webm). Record each sentence on its own, in a quiet room, phone 20-30 cm away; a short
pause before and after is fine (it is trimmed). Writes build/voice_raw.wav + build/timings.json in the same shape
as tts2.py, so build_v3.sh, the captions and the scenes work unchanged. Word timings inside a sentence are spread
by syllable count (sentence boundaries are exact), which is close enough for karaoke captions.
"""
import glob
import json
import os
import re
import subprocess
import sys
import wave

import numpy as np

SR = 24000


def parse(markup):
    toks = []
    for m in re.finditer(r"\{([^|}]*)\|([^}]*)\}|(\S+)", markup):
        toks.append((m.group(3), m.group(3)) if m.group(3) is not None else (m.group(1), m.group(2)))
    return toks


def syllables(text):
    n = 0
    for w in re.findall(r"[A-Za-z']+", text):
        n += max(1, len(re.findall(r"[aeiouy]+", w.lower())) - (1 if w.lower().endswith("e") and len(w) > 3 else 0))
    return max(1, n)


def load(path):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-ac", "1", "-ar", str(SR), "-f", "f32le", "-"],
                         check=True, capture_output=True).stdout
    return np.frombuffer(raw, dtype=np.float32).copy()


def trim(audio, thr=0.03, pad=0.06):
    env = np.convolve(np.abs(audio), np.ones(480) / 480, mode="same")
    idx = np.where(env > thr * env.max())[0]
    if len(idx) == 0:
        return audio
    a, b = max(0, idx[0] - int(pad * SR)), min(len(audio), idx[-1] + int(pad * SR))
    return audio[a:b]


def main():
    video_dir = sys.argv[1]
    spec = json.load(open(os.path.join(video_dir, "spec.json"), encoding="utf-8"))
    files = sorted(f for f in glob.glob(os.path.join(video_dir, "voice", "*")) if not f.endswith(".md"))
    ss = spec["sentences"]
    if len(files) != len(ss):
        sys.exit(f"need {len(ss)} recordings (one per sentence), found {len(files)} in {video_dir}/voice/")
    gap = np.zeros(int(float(spec.get("gap", 0.08)) * SR + 0.12 * SR), dtype=np.float32)
    chunks, timings, t = [], [], 0.0
    for path, sentence in zip(files, ss):
        audio = trim(load(path))
        audio = audio / max(1e-6, np.abs(audio).max()) * 0.9
        pairs = parse(sentence)
        weights = [syllables(spoken) + 0.5 for _, spoken in pairs]
        span, cur, toks = len(audio) / SR, t, []
        for (shown, _), w in zip(pairs, weights):
            dur = span * w / sum(weights)
            toks.append({"text": shown, "start": round(cur, 3), "end": round(cur + dur, 3)})
            cur += dur
        timings.append({"start": round(t, 3), "end": round(t + span, 3), "tokens": toks,
                        "text": " ".join(p[0] for p in pairs), "voice": os.path.basename(path)})
        chunks += [audio, gap]
        t += (len(audio) + len(gap)) / SR
    full = np.concatenate(chunks)
    b = os.path.join(video_dir, "build")
    os.makedirs(b, exist_ok=True)
    with wave.open(os.path.join(b, "voice_raw.wav"), "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes((np.clip(full, -1, 1) * 32767).astype(np.int16).tobytes())
    json.dump({"duration": round(t, 3), "sentences": timings, "voice": "owner"},
              open(os.path.join(b, "timings.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("owner voice, duration", round(t, 2))


if __name__ == "__main__":
    main()
