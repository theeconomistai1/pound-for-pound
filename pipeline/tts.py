"""Minimal offline British-English TTS: Kokoro ONNX model + misaki GB lexicon.

Usage: python3 -I tts.py <assets_dir> <text_file> <out.wav> [voice] [speed]
Prints one line per sentence: start_seconds<TAB>end_seconds<TAB>sentence
"""
import json
import re
import sys
import wave

import numpy as np
import onnxruntime as ort

SR = 24000


def load_lexicon(assets):
    lex = {}
    for name in ("gb_silver.json", "gb_gold.json"):  # gold overrides silver
        with open(f"{assets}/misaki/misaki/data/{name}", encoding="utf-8") as f:
            lex.update(json.load(f))
    lex.update(EXTRA)
    return lex


def lookup(lex, word):
    for cand in (word, word.lower(), word.capitalize(), word.upper()):
        if cand in lex:
            entry = lex[cand]
            if isinstance(entry, dict):
                entry = entry.get("DEFAULT") or next(v for v in entry.values() if v)
            return entry
    w = word.lower()
    voiceless = tuple("ptkfθ")
    sibilant = ("s", "z", "ʃ", "ʒ", "ʧ", "ʤ")
    if w.endswith("'s") and w[:-2]:
        base = lookup(lex, w[:-2])
        if base:
            return base + ("ᵻz" if base.endswith(sibilant) else "s" if base.endswith(voiceless) else "z")
    if w.endswith("s") and len(w) > 3:
        for b in (w[:-1], w[:-2] if w.endswith("es") else None):
            base = b and lookup(lex, b)
            if base:
                return base + ("ᵻz" if base.endswith(sibilant) else "s" if base.endswith(voiceless) else "z")
    if w.endswith("ed") and len(w) > 4:
        for b in (w[:-2], w[:-1]):
            base = lookup(lex, b)
            if base:
                return base + ("ᵻd" if base.endswith(("t", "d")) else "t" if base.endswith(voiceless + ("s", "ʃ", "ʧ")) else "d")
    if w.endswith("ing") and len(w) > 5:
        for b in (w[:-3], w[:-3] + "e"):
            base = lookup(lex, b)
            if base:
                return base + "ɪŋ"
    return None


EXTRA = {"ISA": "ˈIsə", "ISAs": "ˈIsəz", "Isa": "ˈIsə"}


def phonemize(lex, text, missing):
    out = []
    for tok in re.findall(r"[A-Za-z]+(?:'[A-Za-z]+)?|[.,!?;:—-]", text):
        if re.match(r"[A-Za-z]", tok):
            ph = lookup(lex, tok)
            if ph is None:
                missing.add(tok)
                continue
            out.append(ph)
        else:
            p = {"—": ",", "-": ","}.get(tok, tok)
            if out:
                out[-1] += p
    return " ".join(out)


def main():
    assets, text_file, out_wav = sys.argv[1:4]
    voice_name = sys.argv[4] if len(sys.argv) > 4 else "bf_emma"
    speed = float(sys.argv[5]) if len(sys.argv) > 5 else 1.0

    with open(f"{assets}/kokoro-onnx/src/kokoro_onnx/config.json") as f:
        vocab = json.load(f)["vocab"]
    lex = load_lexicon(assets)
    voices = np.load(f"{assets}/voices-v1.0.bin")
    voice = voices[voice_name]
    sess = ort.InferenceSession(f"{assets}/kokoro.onnx", providers=["CPUExecutionProvider"])
    names = {i.name: i.type for i in sess.get_inputs()}
    tok_name = "input_ids" if "input_ids" in names else "tokens"
    speed_int = "int" in names.get("speed", "float")

    text = open(text_file, encoding="utf-8").read()
    sentences = [s.strip() for s in re.split(r"(?<=[.!?])\s+", text) if s.strip()]
    missing = set()
    chunks, t = [], 0.0
    pause = np.zeros(int(SR * 0.18), dtype=np.float32)
    for s in sentences:
        ph = phonemize(lex, s, missing)
        tokens = [vocab[c] for c in ph if c in vocab][:510]
        if not tokens:
            continue
        style = voice[min(len(tokens), len(voice) - 1)]
        sp = np.array([round(speed) if speed_int else speed],
                      dtype=np.int32 if speed_int else np.float32)
        audio = sess.run(None, {tok_name: np.array([[0, *tokens, 0]], dtype=np.int64),
                                "style": style.astype(np.float32), "speed": sp})[0]
        audio = np.asarray(audio, dtype=np.float32).reshape(-1)
        print(f"{t:.3f}\t{t + len(audio) / SR:.3f}\t{s}")
        chunks += [audio, pause]
        t += (len(audio) + len(pause)) / SR

    if missing:
        print("MISSING\t" + ",".join(sorted(missing)), file=sys.stderr)
    full = np.concatenate(chunks)
    full = full / max(1e-6, np.abs(full).max()) * 0.9
    with wave.open(out_wav, "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes((full * 32767).astype(np.int16).tobytes())


if __name__ == "__main__":
    main()
