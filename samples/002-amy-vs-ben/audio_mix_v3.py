"""Original music bed + sound effects, ducked under the voice.

Usage: python3 -I audio_mix.py <voice_processed_44k.wav> <events.json> <duration_s> <out.wav> [--seed N]

events.json: [{"t": 4.2, "kind": "whoosh"|"pop"|"coin"|"boom"|"crash"}, ...]
Everything here is synthesised from scratch, so it is free of copyright claims.
"""
import json
import sys
import wave

import numpy as np
from scipy.signal import butter, sosfilt

SR = 44100
rng = np.random.default_rng(int(sys.argv[sys.argv.index("--seed") + 1]) if "--seed" in sys.argv else 7)


def hz(midi):
    return 440.0 * 2 ** ((midi - 69) / 12)


def lp(x, f, order=2):
    return sosfilt(butter(order, f, "low", fs=SR, output="sos"), x)


def hp(x, f, order=2):
    return sosfilt(butter(order, f, "high", fs=SR, output="sos"), x)


def bp(x, lo, hi, order=2):
    return sosfilt(butter(order, [lo, hi], "band", fs=SR, output="sos"), x)


def env(n, attack, decay):
    t = np.arange(n) / SR
    a = np.clip(t / max(attack, 1e-4), 0, 1)
    return a * np.exp(-np.maximum(t - attack, 0) / decay)


def saw(f, n, phase=0.0):
    t = np.arange(n) / SR
    return 2 * ((f * t + phase) % 1.0) - 1


def add(buf, sig, start):
    i = int(start * SR)
    if i >= len(buf):
        return
    j = min(len(buf), i + len(sig))
    buf[i:j] += sig[: j - i]


# ---- instruments --------------------------------------------------------------
def kick():
    n = int(0.35 * SR)
    t = np.arange(n) / SR
    f = 45 + 110 * np.exp(-t / 0.035)
    ph = 2 * np.pi * np.cumsum(f) / SR
    click = hp(rng.standard_normal(n), 2000) * env(n, 0.0005, 0.004) * 0.3
    return (np.sin(ph) * env(n, 0.001, 0.16) + click) * 0.9


def clap():
    n = int(0.25 * SR)
    x = bp(rng.standard_normal(n), 900, 5000)
    e = env(n, 0.001, 0.07)
    for d in (0.010, 0.022):  # flam
        k = int(d * SR)
        e[k:] += env(n - k, 0.001, 0.05) * 0.6
    return x * e * 0.45


def hat(open_=False):
    n = int((0.18 if open_ else 0.05) * SR)
    x = hp(rng.standard_normal(n), 7000)
    return x * env(n, 0.0005, 0.06 if open_ else 0.012) * 0.22


def crash():
    n = int(1.8 * SR)
    x = hp(rng.standard_normal(n), 4000)
    return x * env(n, 0.002, 0.6) * 0.25


def bass_note(midi, dur):
    n = int(dur * SR)
    f = hz(midi)
    x = 0.6 * saw(f, n) + 0.4 * np.sin(2 * np.pi * f * np.arange(n) / SR)
    x = lp(x, 420)
    return x * env(n, 0.004, dur * 0.7) * 0.55


def pad_chord(midis, dur):
    n = int(dur * SR)
    x = np.zeros(n)
    for m in midis:
        for det in (-0.12, 0.0, 0.12):
            x += saw(hz(m + det), n, rng.random())
    x = lp(x / (len(midis) * 3), 2200)
    a = np.clip(np.arange(n) / (0.02 * SR), 0, 1)
    return x * a * 0.22


def pluck(midi, dur=0.22):
    n = int(dur * SR)
    f = hz(midi)
    x = 0.5 * saw(f, n) + 0.5 * np.sign(np.sin(2 * np.pi * f * np.arange(n) / SR))
    x = lp(x, 3200)
    return x * env(n, 0.002, 0.07) * 0.16


# ---- sound effects ------------------------------------------------------------
def whoosh():
    n = int(0.45 * SR)
    x = rng.standard_normal(n)
    out = np.zeros(n)
    seg = n // 12
    for k in range(12):  # sweep the band upwards
        lo = 300 * (1.25 ** k)
        sl = slice(k * seg, (k + 1) * seg if k < 11 else n)
        out[sl] = bp(x, lo, min(lo * 3, 16000))[sl]
    t = np.arange(n) / n
    return out * np.sin(np.pi * t) ** 1.5 * 0.35


def pop():
    n = int(0.09 * SR)
    t = np.arange(n) / SR
    f = 420 + 700 * np.exp(-t / 0.015)
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * env(n, 0.001, 0.03) * 0.5


def coin():
    n = int(0.9 * SR)
    t = np.arange(n) / SR
    out = np.zeros(n)
    for start, f in ((0.0, 1975.5), (0.075, 2637.0)):
        k = int(start * SR)
        tt = t[: n - k]
        tone = np.sin(2 * np.pi * f * tt) + 0.35 * np.sin(2 * np.pi * f * 2.76 * tt) + 0.2 * np.sin(2 * np.pi * f * 5.4 * tt)
        out[k:] += tone * np.exp(-tt / 0.28)
    return out * 0.18


def boom():
    n = int(1.0 * SR)
    t = np.arange(n) / SR
    f = 30 + 70 * np.exp(-t / 0.08)
    body = np.sin(2 * np.pi * np.cumsum(f) / SR) * env(n, 0.002, 0.45)
    noise = lp(rng.standard_normal(n), 900) * env(n, 0.001, 0.12) * 0.5
    return (body + noise) * 0.8


SFX = {"whoosh": lambda: whoosh() * 0.6, "pop": pop, "coin": coin, "boom": boom, "crash": crash}


# ---- arrangement ----------------------------------------------------------------
def music(duration, bpm=124):
    beat = 60 / bpm
    n = int((duration + 1.5) * SR)
    drums, bass, pad, lead = (np.zeros(n) for _ in range(4))
    prog = [(57, [69, 72, 76]), (53, [65, 69, 72]), (48, [67, 72, 76]), (55, [67, 71, 74])]  # Am F C G
    bars = int(np.ceil((duration + 1) / (4 * beat)))
    K, C = kick(), clap()
    for b in range(bars):
        root, chord = prog[b % 4]
        t0 = b * 4 * beat
        pad_part = pad_chord([m - 12 for m in chord], 4 * beat)
        add(pad, pad_part, t0)
        for i in range(8):  # eighth-note bass, octave bounce
            add(bass, bass_note(root - 24 + (12 if i % 2 else 0), beat / 2 * 0.9), t0 + i * beat / 2)
        for i in range(16):  # sixteenth arpeggio
            if b == 0 and i < 4:
                continue
            note = chord[[0, 1, 2, 1][i % 4]] + (12 if (i // 4) % 2 else 0)
            add(lead, pluck(note), t0 + i * beat / 4)
        for i in range(4):
            add(drums, K, t0 + i * beat)
            if i in (1, 3):
                add(drums, C, t0 + i * beat)
            add(drums, hat(open_=(i == 3)), t0 + i * beat + beat / 2)
            add(drums, hat() * 0.5, t0 + i * beat + beat * 0.75)
    # sidechain pump on pad and bass from the kick grid
    t = np.arange(n) / SR
    phase = (t % beat) / beat
    pump = 0.35 + 0.65 * np.clip(phase / 0.45, 0, 1) ** 0.8
    left = drums + bass * pump + pad * pump + lead * 0.8
    right = drums + bass * pump + pad * pump * 0.95 + np.roll(lead, int(0.012 * SR)) * 0.8
    st = np.stack([left, right], axis=1)[: int(duration * SR)]
    # fade the last second
    fade = int(1.0 * SR)
    st[-fade:] *= np.linspace(1, 0, fade)[:, None]
    return st


def read_wav(path):
    with wave.open(path) as w:
        assert w.getframerate() == SR, "voice must be 44.1 kHz"
        x = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float64) / 32768
        if w.getnchannels() == 2:
            x = x.reshape(-1, 2).mean(axis=1)
    return x


def main():
    voice_path, events_path, duration, out = sys.argv[1], sys.argv[2], float(sys.argv[3]), sys.argv[4]
    v = read_wav(voice_path)
    n = int(duration * SR)
    voice = np.zeros(n)
    voice[: min(n, len(v))] = v[:n]

    bpm = float(sys.argv[sys.argv.index('--bpm') + 1]) if '--bpm' in sys.argv else 124
    m = music(duration, bpm)
    m = m / np.abs(m).max()

    # duck the music under speech
    e = np.convolve(np.abs(voice), np.ones(int(0.05 * SR)) / (0.05 * SR), mode="same")
    active = np.clip(e / (0.25 * e.max() + 1e-9), 0, 1)
    active = np.convolve(active, np.ones(int(0.12 * SR)) / (0.12 * SR), mode="same")
    base = float(sys.argv[sys.argv.index('--gain') + 1]) if '--gain' in sys.argv else 0.30
    music_gain = base * (1 - 0.55 * active)

    sfx = np.zeros(n)
    for ev in json.load(open(events_path)):
        add(sfx, SFX[ev["kind"]](), ev["t"])

    mix_l = voice + m[:, 0] * music_gain + sfx
    mix_r = voice + m[:, 1] * music_gain + sfx
    st = np.stack([mix_l, mix_r], axis=1)
    st = st / np.abs(st).max() * 0.95
    with wave.open(out, "wb") as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes((st * 32767).astype(np.int16).tobytes())


if __name__ == "__main__":
    main()
