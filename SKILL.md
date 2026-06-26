---
name: youtube-to-sketchnote
description: Turn a YouTube video into a hand-drawn, on-brand Arize sketchnote (4K PNG + SVG). Pulls the transcript + metadata, uses Gemini to watch the actual video (slides, on-screen product names, speakers), has Claude author a structured layout, generates sketch portraits of the speakers and hand-drawn versions of key slides, renders a borderless 4×3 grid with rough.js, and fact-checks the result against the video with Codex + Gemini. Use when someone wants a sketchnote, visual summary, or one-page recap of a YouTube talk/video.
---

# YouTube → Sketchnote

Turn a YouTube talk into a single hand-drawn, Arize-branded sketchnote. The pipeline is:

```
extract.py ─► Gemini video-notes ─► Claude authors layout.json ─► speaker-sketch.py
   (transcript)   (watches video)        (the editorial work)        (portraits)
                                                                          │
   out/<slug>.png ◄── render.mjs ◄── slide-sketch.py ◄──────────────────┘
   (4K PNG + SVG)     (rough.js)      (redraws key slides)
        │
        └─► validate-video.py (Gemini) + validate.mjs (Codex) ─► fix layout.json ─► re-render
```

Claude does the **authoring + adjudication**; the scripts do extraction, image generation, rendering, and validation. Read `DESIGN.md` for the full rationale and `assets/brand/arize-brand-notes.md` for the brand.

## Prerequisites

- **CLIs:** `yt-dlp`, `ffmpeg`, `node` (18+), `python3`. `codex` (optional, for the second validator) with `codex login`.
- **Keys:** `GEMINI_API_KEY` in the environment (Gemini reads the video, draws portraits/slides, validates). Without it the skill still works from the transcript alone, minus video-grounded notes, portraits, and slide sketches.
- **Install once:**
  ```bash
  cd scripts && npm install            # playwright, roughjs, handlebars, lucide-static
  pip install -r scripts/requirements.txt
  npx playwright install chromium      # if Chromium isn't already cached
  ```

## Steps

Pick a short `<slug>` for the video (e.g. `openai-feedback`). Work in `work/<slug>/`, write assets to `assets/<slug>-*`, output to `out/<slug>.{png,svg}`.

### 1. Extract transcript + metadata
```bash
python3 scripts/extract.py "<youtube-url>" --out work/<slug>/context.json
```
Cascade: youtube-transcript-api → yt-dlp subs → whisper.cpp (`--whisper-model` for ASR). `--with-frames` is rarely needed now that Gemini reads the video. If you hit bot-detection, add `--cookies-from-browser safari`.

### 2. Gemini video-notes (the eyes)
```bash
python3 scripts/video-notes.py --context work/<slug>/context.json
```
Gemini watches the video and merges `video_notes` into `context.json`: the real section structure (with timestamps), **on-screen product/feature names** (authoritative spelling), diagrams, on-screen numbers, and quotes. Skip only if no `GEMINI_API_KEY`.

### 3. Author `work/<slug>/layout.json`  ← Claude's main job
Read the whole `context.json` (transcript + `video_notes`) and the transcript skim, then write a layout. **Do not transcribe — distil.** Rules:

- **Schema:** `scripts/layout.schema.json`. Validate against it mentally before rendering.
- **Sections:** 8–12, one idea each, in the talk's narrative order. `layout: "grid"`, `canvas: {theme: "dark", aspect: "16:9", cols: 4}` (4×3 fills 16:9; use 3 cols only for ≤9 sections).
- **Per section:** `header` ≤ ~6 words (a question or punchy phrase); **2–3 bullets that are takeaways, not transcript**; at most one `quote` (verbatim, memorable — these become speech bubbles, so use 3–4 across the whole sketchnote, not every cell).
- **Hue** per section from `teal | indigo | purple | magenta` — colour-code by theme group (e.g. problem = teal, solution = indigo/purple, the pivot/keystone = magenta). Pink is reserved for accents, never a section hue.
- **Icon:** a `lucide` icon name relevant to the section (verify it exists in `scripts/node_modules/lucide-static/icons/`).
- **decor:** `{density: "light", seed: <int>, motifs: [~10 lucide names relevant to the video's topic]}`. Light density keeps it sparse.

### 4. Speaker portraits
```bash
python3 scripts/speaker-sketch.py --context work/<slug>/context.json --out-dir assets/<slug>-speakers
```
Gemini finds the speakers in the thumbnail and draws each as a pink-circle line portrait. Read `work/<slug>/speakers.json` and add a `speakers: [{name, role, portrait}]` array to `layout.json` (keep `role` short, e.g. `"OpenAI · MTS"`).

### 5. Slide sketches (selective)
```bash
python3 scripts/slide-sketch.py --context work/<slug>/context.json --layout work/<slug>/layout.json --out-dir assets/<slug>-slides
```
Gemini picks only sections with a **simple, useful** on-screen visual (it skips dense flowcharts), redraws each as a small line sketch recoloured to the section hue, and patches `section.figure` into the layout. Sections without a figure keep their lucide icon.

### 6. Render (4K)
```bash
node scripts/render.mjs work/<slug>/layout.json --out out/<slug>
```
Borderless-feel grid with subtle hand-drawn borders, 3840×2160. Flags: `--light` (light theme), `--decor none|light|medium|heavy`, `--seed N`, `--no-svg`, `--scale N`. View the PNG and sanity-check legibility/overflow.

### 7. Validate, then fix → re-render
```bash
python3 scripts/validate-video.py --image out/<slug>.png --context work/<slug>/context.json   # Gemini, watches the video
node scripts/validate.mjs --image out/<slug>.png --context work/<slug>/context.json            # Codex, transcript + image (optional)
```
Both emit schema-validated `findings.json` (`verdict` + issues). On `revise`, apply the **real** fixes to `layout.json`, re-render, and re-validate. Then show the final PNG/SVG.

## Authoring judgement (encode these — they recur)

- **Product/feature/company names:** trust the **on-screen spelling** from `video_notes` over the auto-caption transcript (captions mangle names — e.g. "Pixie" is really **PXI**, "Alex" is **Alyx**). When unsure, web-search to confirm casing. See the `arize-product-names` memory for Arize's own names (AX, Phoenix, PXI, Alyx, OpenInference, ADB, Signal).
- **"Observe '26" vs "2026":** the on-screen logo reads `observe '26` (stylised), but it's a 2026 event — the canonical YouTube title says "Arize Observe 2026". **Keep the canonical title; override the validator's branding flag.** Don't write "Observe '26".
- **Privacy / safety caveats:** if a speaker stresses a caveat (opt-in, PII stripped, no-black-box, etc.), keep it — it's easy to drop when condensing and the validators reliably flag it.
- **Arize voice:** sentence case everywhere, no emoji, short declaratives, expose acronyms. Refer to products by name. (`assets/brand/arize-brand-notes.md`.)

## Output
`out/<slug>.png` (4K 16:9) + `out/<slug>.svg`. Self-contained — portraits and slide sketches are embedded. Show the user the PNG and a one-line note on what the validators found/fixed.
