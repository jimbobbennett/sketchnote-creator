# sketchnote-creator

Turn a YouTube talk into a single, hand-drawn **sketchnote** — a 4K (3840×2160) image that distils the
video into a colour-coded grid of sections, with sketch portraits of the speakers, redrawn key slides,
and a quick fact-check against the source video. The look is driven by a **pluggable design system**, so
it works for any brand (a generic one ships in the repo).

## Examples

*The Future of AI Agents* — Arize Observe 2026 keynote ([watch](https://youtu.be/errTnC59gVM)):

![Sketchnote of the Arize Observe 2026 keynote, The Future of AI Agents](examples/keynote-arize-observe-2026.png)

*Harnessing User Feedback at ChatGPT Scale* — OpenAI, Stuart Sy ([watch](https://youtu.be/c1xPkDi-038)):

![Sketchnote of the OpenAI talk, Harnessing User Feedback at ChatGPT Scale](examples/openai-feedback-chatgpt-scale.png)

Both were generated end-to-end and rendered with the (local) Arize design system; run without `--design`
for the generic look. More in [`examples/`](examples/).

## How it works

It's built to run as a **[Claude Code](https://claude.com/claude-code) skill** ([`SKILL.md`](SKILL.md)):
Claude orchestrates a set of scripts and does the editorial work (writing the layout) in the middle.

```
extract.py ─► Gemini video-notes ─► author layout.json ─► speaker-sketch.py
 (transcript)   (watches the video)      (the editorial step)    (portraits)
                                                                      │
 out/<slug>.png ◄── render.mjs ◄── slide-sketch.py ◄─────────────────┘
 (4K PNG + SVG)     (rough.js)      (redraws key slides)
       │
       └─► validate-video.py (Gemini) + validate.mjs (Codex) ─► fix layout.json ─► re-render
```

- **extract** — transcript + metadata (captions → subtitles → Whisper fallback).
- **video-notes** — Gemini watches the actual video for structure, on-screen product names, diagrams, speakers.
- **layout.json** — the section-by-section plan (done by Claude per `SKILL.md`, or hand-authored).
- **speaker-sketch / slide-sketch** — Gemini 2.5 Flash Image draws speaker portraits and redraws simple slides.
- **render** — `rough.js` + headless Chromium (Playwright) produce the 4K hand-drawn grid (PNG + SVG).
- **validate** — Gemini (watches the video) and optionally Codex fact-check the result; fix and re-render.

## Prerequisites

You provide these yourself (the setup step installs the rest):

- **[`ffmpeg`](https://ffmpeg.org)** — the one system binary the installer can't fetch (macOS: `brew install ffmpeg`, Debian/Ubuntu: `sudo apt install ffmpeg`, Windows: `winget install ffmpeg`).
- **Node 18+** and **Python 3**.
- **`GEMINI_API_KEY`** in the environment — Gemini reads the video and draws the portraits/slide sketches and validates. Without it you can still render from a hand-written transcript + layout, but you lose the video reading, portraits, slide sketches, and the video validator.
- **Optional:** [`codex`](https://github.com/openai/codex) CLI (a second, transcript-based validator); `whisper.cpp` (`whisper-cli`) or `openai-whisper` for videos with no captions; `tesseract` only for `extract.py --with-frames`.

`yt-dlp` is installed for you via pip (it's in `requirements.txt`).

## Setup

```bash
git clone https://github.com/jimbobbennett/sketchnote-creator.git
cd sketchnote-creator
./scripts/setup.sh            # npm + pip deps, headless Chromium, then checks system tools
export GEMINI_API_KEY=...     # https://aistudio.google.com/apikey
```

`setup.sh` installs the Node and Python packages and the headless browser, then reports whether
`ffmpeg`/`node`/`python3`/`GEMINI_API_KEY` are present (it does **not** install system packages or use
sudo). Or run the steps yourself: `(cd scripts && npm install && npx playwright install chromium) && pip install -r scripts/requirements.txt`.

## Usage

### As a Claude Code skill (recommended)
Open this repo in Claude Code and ask it to sketchnote a video, e.g.
*"make a sketchnote of https://youtu.be/…"*. Claude follows [`SKILL.md`](SKILL.md): it runs the
scripts, writes the layout, renders, validates, and shows you the result.

### Manually
Pick a short `<slug>` for the video, then:

```bash
python3 scripts/extract.py "<youtube-url>" --out work/<slug>/context.json
python3 scripts/video-notes.py   --context work/<slug>/context.json
# author work/<slug>/layout.json  (see scripts/layout.schema.json + scripts/sample-grid.layout.json)
python3 scripts/speaker-sketch.py --context work/<slug>/context.json --out-dir assets/<slug>-speakers
python3 scripts/slide-sketch.py   --context work/<slug>/context.json --layout work/<slug>/layout.json --out-dir assets/<slug>-slides
node    scripts/render.mjs        work/<slug>/layout.json --out out/<slug>
python3 scripts/validate-video.py --image out/<slug>.png --context work/<slug>/context.json
```

The middle step — `layout.json` — is the creative one (title, sections, bullets, quotes, icons). It's
what the skill writes for you; to do it by hand, follow the schema (`scripts/layout.schema.json`) and the
worked sample (`scripts/sample-grid.layout.json`).

**`render.mjs` flags:** `--design design/<name>` (palette/fonts/logo; default `design/default`),
`--light` (default theme is dark), `--decor none|light|medium|heavy` (default `light`),
`--seed N`, `--scale N` (default 2 → 4K), `--no-svg`. Pass the same `--design` to `slide-sketch.py`.

Output: `out/<slug>.png` (4K 16:9) + `out/<slug>.svg`, self-contained (portraits/slides embedded).

## Design system

Palette, fonts, logo, and voice come from `design/<name>/design.json`. `design/default/` ships in the
repo and is used unless you pass `--design`. To brand it for yourself, copy `design/default/` to
`design/<name>/`, edit the JSON, and pass `--design design/<name>`. Anything you add under `design/`
(other than `default/`) stays local and untracked. Full format + walkthrough — including **pulling a
design system from [claude.ai/design](https://claude.ai/design)** via Claude Code — in
[`design/README.md`](design/README.md).

## Project layout

```
SKILL.md         the skill — orchestrates the whole pipeline
scripts/         extract · video-notes · speaker-sketch · slide-sketch · render · validate · validate-video
templates/       sketchnote.css + draw.js + doodles.js  (brand-agnostic; design tokens injected at render)
design/          default/ (generic, committed) + README.md (how to add your own brand)
research/        background notes on sketchnoting + video extraction
examples/        finished sample sketchnotes
DESIGN.md        design rationale and decisions
```
