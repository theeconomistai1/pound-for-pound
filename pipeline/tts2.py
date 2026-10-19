"""Offline British TTS with per-word timings for kinetic captions.

Usage: python3 -I tts2.py <assets_dir> <spec.json> <out.wav> <out_timings.json>

spec.json: {"voice": "bf_emma", "speed": 1.15, "gap": 0.06,
            "sentences": ["{£5|Five pounds} a day could grow ...", ...]}
Markup: plain words are both shown and spoken; {shown|spoken} shows one thing
and says another (numbers, symbols). Timings are per shown token.
"""
import json
import re
import sys
import wave

import numpy as np
import onnxruntime as ort

sys.path.insert(0, __file__.rsplit("/", 1)[0])
from tts import load_lexicon, lookup  # noqa: E402

SR = 24000


def parse(markup):
    toks = []
    for m in re.finditer(r"\{([^|}]*)\|([^}]*)\}|(\S+)", markup):
        if m.group(3) is not None:
            toks.append((m.group(3), m.group(3)))
        else:
            toks.append((m.group(1), m.group(2)))
    return toks


def phon_words(lex, text, missing):
    out = []
    for tok in re.findall(r"[A-Za-z]+(?:'[A-Za-z]+)?|[.,!?;:—-]", text):
        if re.match(r"[A-Za-z]", tok):
            ph = lookup(lex, tok)
            if ph is None:
                missing.add(tok)
                continue
            out.append(ph)
        elif out:
            out[-1] += {"—": ",", "-": ","}.get(tok, tok)
    return out


def speech_span(audio, thr=0.02):
    env = np.convolve(np.abs(audio), np.ones(240) / 240, mode="same")
    idx = np.where(env > thr * env.max())[0]
    if len(idx) == 0:
        return 0, len(audio)
    return int(idx[0]), int(idx[-1])


def main():
    assets, spec_path, out_wav, out_json = sys.argv[1:5]
    spec = json.load(open(spec_path, encoding="utf-8"))
    voice_name, speed, gap = spec.get("voice", "bf_emma"), float(spec.get("speed", 1.1)), float(spec.get("gap", 0.08))

    vocab = json.load(open(f"{assets}/kokoro-onnx/src/kokoro_onnx/config.json"))["vocab"]
    lex = load_lexicon(assets)
    voice = np.load(f"{assets}/voices-v1.0.bin")[voice_name]
    sess = ort.InferenceSession(f"{assets}/kokoro.onnx", providers=["CPUExecutionProvider"])
    tok_name = "input_ids" if "input_ids" in [i.name for i in sess.get_inputs()] else "tokens"

    missing, chunks, timings, t = set(), [], [], 0.0
    silence = np.zeros(int(SR * gap), dtype=np.float32)
    for markup in spec["sentences"]:
        pairs = parse(markup)
        per_tok = [phon_words(lex, spoken, missing) for _, spoken in pairs]
        phon = " ".join(p for words in per_tok for p in words)
        tokens = [vocab[c] for c in phon if c in vocab][:510]
        style = voice[min(len(tokens), len(voice) - 1)]
        audio = sess.run(None, {tok_name: np.array([[0, *tokens, 0]], dtype=np.int64),
                                "style": style.astype(np.float32),
                                "speed": np.array([speed], dtype=np.float32)})[0]
        audio = np.asarray(audio, dtype=np.float32).reshape(-1)
        s0, s1 = speech_span(audio)
        weights = [max(1, sum(len(p) + 1 for p in words)) for words in per_tok]
        total_w = sum(weights)
        span = (s1 - s0) / SR
        cur = t + s0 / SR
        toks = []
        for (shown, _), w in zip(pairs, weights):
            dur = span * w / total_w
            toks.append({"text": shown, "start": round(cur, 3), "end": round(cur + dur, 3)})
            cur += dur
        timings.append({"start": round(t, 3), "end": round(t + len(audio) / SR, 3), "tokens": toks,
                        "text": " ".join(p[0] for p in pairs)})
        chunks += [audio, silence]
        t += (len(audio) + len(silence)) / SR

    if missing:
        print("MISSING\t" + ",".join(sorted(missing)), file=sys.stderr)
    full = np.concatenate(chunks)
    full = full / max(1e-6, np.abs(full).max()) * 0.9
    with wave.open(out_wav, "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes((full * 32767).astype(np.int16).tobytes())
    json.dump({"duration": round(t, 3), "sentences": timings}, open(out_json, "w", encoding="utf-8"),
              ensure_ascii=False, indent=1)
    print("duration", round(t, 2))


if __name__ == "__main__":
    main()
