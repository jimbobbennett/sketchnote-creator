#!/usr/bin/env bash
# One-shot setup for the YouTube → Sketchnote skill.
# Installs the language packages (npm + pip) and the headless browser, then CHECKS for the
# system tools it can't install for you (ffmpeg, node, python3) and prints how to get them.
# It does NOT install system packages or anything with sudo.
set -euo pipefail
cd "$(dirname "$0")/.."   # repo root

echo "• Node deps + headless Chromium …"
( cd scripts && npm install && npx playwright install chromium )

echo "• Python deps …"
pip install -r scripts/requirements.txt

echo
echo "• Required system tools:"
missing=0
check() { if command -v "$1" >/dev/null 2>&1; then echo "  ✓ $1"; else echo "  ✗ $1 — $2"; missing=1; fi; }
check node    "install Node 18+ — https://nodejs.org"
check python3 "install Python 3 — https://python.org"
check ffmpeg  "install ffmpeg — macOS: brew install ffmpeg · Debian/Ubuntu: sudo apt install ffmpeg · Windows: winget install ffmpeg"
check yt-dlp  "should be pip-installed by this script; ensure your pip bin dir is on PATH"

echo
echo "• Optional tools:"
for t in codex whisper-cli tesseract; do
  if command -v "$t" >/dev/null 2>&1; then echo "  ✓ $t"; else echo "  – $t (optional; only needed for the Codex validator / no-caption ASR / --with-frames OCR)"; fi
done

echo
if [ -n "${GEMINI_API_KEY:-}" ]; then echo "  ✓ GEMINI_API_KEY is set"; else echo "  ✗ GEMINI_API_KEY not set — export it (https://aistudio.google.com/apikey)"; missing=1; fi

echo
if [ "$missing" -eq 0 ]; then echo "✓ Setup complete — you're ready to go."; else echo "⚠ Setup finished, but install the missing items above before running the skill."; fi
