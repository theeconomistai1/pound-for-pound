#!/usr/bin/env bash
# Fetch the offline voice model, pronunciation dictionary and fonts into $P4P_ASSETS.
# Everything comes from GitHub, which cloud sessions can reach. Safe to re-run.
set -euo pipefail
A="${P4P_ASSETS:-$HOME/.p4p-assets}"
mkdir -p "$A"
cd "$A"
[ -d misaki ] || git clone -q --depth 1 https://github.com/hexgrad/misaki.git
[ -d kokoro-onnx ] || git clone -q --depth 1 https://github.com/thewh1teagle/kokoro-onnx.git
REL=https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0
[ -s kokoro.onnx ] || curl -sSL --retry 3 -o kokoro.onnx "$REL/kokoro-v1.0.int8.onnx"
[ -s voices-v1.0.bin ] || curl -sSL --retry 3 -o voices-v1.0.bin "$REL/voices-v1.0.bin"
# Nunito (house-style font for motion.py videos).
if [ ! -f "nunito/fonts/variable/Nunito[wght].ttf" ]; then
  rm -rf nunito
  git clone -q --depth 1 --filter=blob:none --sparse https://github.com/googlefonts/nunito.git nunito
  (cd nunito && git sparse-checkout set fonts/variable)
fi
# Inter font (older videos): use the system copy if present, otherwise download it.
if [ ! -f /usr/share/fonts/opentype/inter/Inter-Black.otf ] && [ ! -f fonts/Inter-Black.otf ]; then
  mkdir -p fonts
  curl -sSL --retry 3 -o inter.zip https://github.com/rsms/inter/releases/download/v4.0/Inter-4.0.zip
  python3 -c "import zipfile,sys;z=zipfile.ZipFile('inter.zip');[open('fonts/'+n.split('/')[-1],'wb').write(z.read(n)) for n in z.namelist() if n.endswith('.otf') and '/Inter-' in n and 'Display' not in n]"
fi
python3 -c "import onnxruntime, scipy, PIL, numpy" || { echo "missing python packages: onnxruntime scipy pillow numpy" >&2; exit 1; }
command -v ffmpeg >/dev/null || { echo "ffmpeg missing" >&2; exit 1; }
echo "assets ready in $A"
