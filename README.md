# YouTube → Sketchnote skill

Turn a YouTube video into an engaging, on-brand (Arize) hand-drawn sketchnote — a single 4K image
that distils a talk into a colour-coded grid with speaker portraits, redrawn key slides, and
fact-checking against the source video.

## Quick start

The skill is **`SKILL.md`** — it orchestrates the pipeline end to end. In short:

```bash
cd scripts && npm install && pip install -r requirements.txt   # one-time
# then, per video (see SKILL.md for the full flow):
python3 scripts/extract.py "<youtube-url>" --out work/<slug>/context.json
python3 scripts/video-notes.py --context work/<slug>/context.json
#  …Claude authors work/<slug>/layout.json…
python3 scripts/speaker-sketch.py --context work/<slug>/context.json --out-dir assets/<slug>-speakers
python3 scripts/slide-sketch.py   --context work/<slug>/context.json --layout work/<slug>/layout.json --out-dir assets/<slug>-slides
node scripts/render.mjs work/<slug>/layout.json --out out/<slug>
python3 scripts/validate-video.py --image out/<slug>.png --context work/<slug>/context.json
```

Needs `GEMINI_API_KEY` (video reading, portraits, slide sketches, validation) and, optionally,
`codex` for a second validator. See **`SKILL.md`** for prerequisites and authoring rules,
**`DESIGN.md`** for the rationale, and **`examples/`** for finished output.

## Layout

```
SKILL.md                          # the skill — orchestrates the whole pipeline
scripts/                          # extract / video-notes / speaker-sketch / slide-sketch / render / validate
templates/                        # sketchnote.css + draw.js + doodles.js (brand-agnostic)
design/
  default/                        # generic, committed design system (palette, fonts, pencil logo)
  README.md                       # how design systems work + how to add your own
  <yourbrand>/                    # local, gitignored — drop your palette/logo/voice here
research/
  sketchnotes-best-practices.md   # how sketchnotes work + rules for programmatic generation
  youtube-extraction.md           # how to pull transcript / metadata / visuals from a video
examples/                         # finished sample sketchnotes
```

## Design system (pluggable)
The look is **not** hard-wired to any brand — palette, fonts, logo, and voice come from a design
system under `design/<name>/design.json`. `design/default/` ships in the repo; drop your own brand in
`design/<name>/` (stays local) and pass `--design design/<name>`. See **`design/README.md`**.

## Research summary

### 1. Sketchnote best practices → `research/sketchnotes-best-practices.md`
Synthesized from Mike Rohde, Doug Neill (Verbal to Visual), Eva-Lotta Lamm, Sunni Brown, et al.
Most relevant for programmatic generation:
- **Layout decision rule:** map detected talk structure → layout (linear is the safe default;
  YouTube chapters → modular/grid; single center → radial). Axes: *is there ordering?* and
  *is there a single center?*
- **Multi-pass pipeline** mirrors the human discipline: Structure → Salience → Vocabulary →
  Layout/allocation → Render. Read the *whole* transcript before placing anything (don't go chunk-by-chunk).
- **Hard rules:** one title + 3–7 key-idea clusters + sparse details; typography *is* the
  hierarchy (4 levels, 2–3 type styles); palette = ink + grey + **one** accent; bias to omission.
- **Visual vocabulary:** containers (box/cloud/banner), connectors (arrows), bullets/frames/dividers,
  icons, star/stick people, emphasis. Convention→meaning defaults: banner→title, cloud→soft idea,
  box→fact, thick arrow→trend, looping arrow→cycle.
- Two brief corrections from the agent: Rohde's primitives are the **five basic shapes** (square,
  circle, triangle, line, dot), not a "Five S's"; and his seventh layout is **skyscraper**, not "skeleton."

### 2. YouTube extraction → `research/youtube-extraction.md`
Tooling and an end-to-end pipeline. Headlines:
- **Cascade** captions → subtitles → Whisper; never assume captions exist.
  `youtube-transcript-api` (1.x instance API) first, `yt-dlp --write-auto-subs` next,
  `whisper-cli` (whisper.cpp, Metal-accelerated on this Mac) as fallback.
- **Metadata via yt-dlp** (not the Data API) — only yt-dlp exposes **chapters**, the best
  segment boundaries for sketchnote sections.
- **Visuals:** `yt-dlp` (720p) + `ffmpeg` scene-detect keyframes + `tesseract` OCR to keep
  slide/diagram frames and pull on-screen text.
- Keep **timestamps everywhere** so transcript + chapters + OCR'd text align for the LLM.
- Required tools (`yt-dlp`, `ffmpeg`, `tesseract`, `whisper-cli`, `python3`) are **already installed** locally.

## Design
See **`DESIGN.md`** for the full skill design (4-stage pipeline, layout selector, cell template,
color logic, schema, build plan). Render engine + aesthetic decisions are locked there.

## Status

- ✅ Research + pluggable design system (`research/`, `design/`)
- ✅ `DESIGN.md` — concrete design, knobs resolved
- ✅ **Phase 1 — render (the `grid` layout)**: `scripts/render.mjs` turns a `layout.json` into a
  hand-drawn, on-brand PNG + SVG via rough.js + Playwright. Try it:
  ```bash
  cd scripts && npm install
  node render.mjs sample-grid.layout.json --out ../out/sample-grid
  ```
  Output + a worked example live in `out/`. Schema: `scripts/layout.schema.json`.
- ✅ **Phase 2 — `extract.py`** (transcript/metadata/chapters/visuals → `context.json`).
  Cascade: youtube-transcript-api → yt-dlp srv1 → whisper.cpp. Visuals opt-in via `--with-frames`.
  ```bash
  python3 scripts/extract.py "https://youtu.be/errTnC59gVM" --out work/context.json
  ```
- ✅ **End-to-end proven on a real video** — the Arize Observe 2026 keynote flowed
  extract → structure → render. Worked example: `work/keynote.layout.json` → `out/keynote.png`.
- ✅ **Validator (`scripts/validate.mjs`)** — independent Codex pass that checks the rendered PNG
  back against the video transcript with **no shared context**, emitting `findings.json`
  (`verdict` + issues). Forms a validate → fix → re-render cycle.
  ```bash
  node scripts/validate.mjs --image out/keynote.png --context work/context.json
  ```
- ✅ **Video-grounded validator (`scripts/validate-video.py`)** — Gemini watches the actual
  YouTube video (audio + slides) + the PNG and validates fidelity; reads on-screen text as the
  authoritative source for product names. Same `findings.json` shape. Needs `GEMINI_API_KEY`.
  ```bash
  python3 scripts/validate-video.py --image out/keynote.png --context work/context.json
  ```
- ✅ **Visual richness — Phase A** (see `VISUALS-PLAN.md`): procedural rough.js marginalia
  (sparkles/stars/doodles, seeded, placed only in free zones), container variety (box / **cloud** /
  **speech-bubble** — quotes now render as bubbles), and emphasis. New flags: `--dark`/`--light`
  (**default dark**), `--decor none|light|medium|heavy` (**default light**), `--seed N`; layout fields
  `decor`, `section.container`, `section.emphasis`.
- ✅ **Visual richness — Phase B** (`scripts/speaker-sketch.py`): Gemini vision finds the speakers in
  the video thumbnail → PIL crops the headshots → Gemini 2.5 Flash Image redraws each as a pink
  line-art portrait (bg keyed to transparent, auto-cropped) → composited top-right with name + role.
  Portraits cached in `assets/speakers/`; `layout.speakers` references them.
  ```bash
  python3 scripts/speaker-sketch.py --context work/context.json
  ```
- ✅ **Slide sketches (`scripts/slide-sketch.py`)**: Gemini selects sections with a simple useful
  on-screen visual, ffmpeg grabs the frame, Gemini 2.5 Flash Image redraws it as a small line sketch
  recolored to the section hue, patched into `section.figure`. (Prompted to skip dense flowcharts.)
- ✅ **Layout — borderless grid** (the keeper; popcorn/path/radial/conversation were tried and dropped).
  Sections are borderless clusters (hue banner + section image + bullets + optional quote bubble) on a
  4×3 grid. Output is fixed **16:9, 3840×2160 (4K)** at the default 2× scale (`--scale` adjusts).
  Section images (slide sketches) render large as the focal visual.
- ⬜ Remaining layouts (popcorn / path / radial / conversation)
- ⬜ Phase 3 — write the stage-2 structuring rules into `SKILL.md` so the skill is self-driving
- ⬜ Phase 4 — polish (icon library, dark variant, density balancing, footer-left fix, review loop)
