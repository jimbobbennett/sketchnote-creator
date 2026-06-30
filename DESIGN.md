# YouTube → Sketchnote skill — design

> **Note:** this is the original design rationale, written when the tool was Arize-first. The look is
> now driven by a **pluggable design system** (see `design/README.md`); the Arize palette/logos are a
> local, gitignored drop-in (`design/arize/`) and are **not** part of this repo. References below to
> `assets/brand/` and Arize-specific colours/voice are historical — the generic defaults live in
> `design/default/`.

Concrete design rolling up the four research docs:
- `research/youtube-extraction.md` — how to get transcript / metadata / visuals
- `research/sketchnotes-best-practices.md` — the genre's rules + programmatic-generation guidance
- `research/nitya-narasimhan-sketchnotes.md` — her stated process
- `research/nitya-narasimhan-visual-analysis.md` — her transferable technique (from real images)
- `assets/brand/` — Arize palette, type, voice, logos

## Decisions (locked)
- **Render engine:** LLM emits structured `layout.json` → code lays it out as HTML+SVG → headless
  Chromium (Playwright) screenshots to PNG. Deterministic, brand-exact, handles dense layouts.
- **Aesthetic:** **hand-drawn sketchy** — `rough.js` wobbly strokes/fills + a hand-lettered webfont,
  with the **Arize palette** applied to that sketchy hand. Fun first, brand colors throughout.

## Environment (verified 2026-06-26)
Already present: `yt-dlp`, `ffmpeg`, `tesseract`, `whisper-cli`, `python3`, `node v24`, `npm`,
and **Playwright Chromium is already cached** (`~/Library/Caches/ms-playwright`). Remaining setup is
just npm packages (`playwright`, `roughjs`, `handlebars`) and Python libs (`youtube-transcript-api`,
`pytesseract`, `Pillow`).

---

## Architecture — 4 stages

```
 ┌── 1. EXTRACT ──────┐   ┌── 2. STRUCTURE ────┐   ┌── 3. RENDER ───────┐   ┌─ 4. REVIEW ─┐
 │ extract.py (Python)│   │ Claude (the skill) │   │ render.mjs (Node)  │   │ validate (no ctx)│
 │ yt-dlp + captions  │──►│ context.json →     │──►│ layout.json →      │──►│ • Codex: txt+PNG │
 │ cascade + frames   │   │ layout.json        │   │ HTML+SVG(rough.js) │   │ • Gemini: vid+PNG│
 │ + OCR → context.json│  │ (schema-validated) │   │ → Playwright → PNG │   │ → findings.json  │
 └────────────────────┘   └────────────────────┘   └────────────────────┘   └────────┬─────────┘
                               ▲                                                       │ verdict=revise
                               └──────────────── fix layout.json, re-render ◄──────────┘
```

The **intelligence (stage 2) is Claude itself** executing the skill — it reads `context.json`,
applies the layout-selection + condensing rules below, and writes `layout.json`. No separate API call.
Stages 1 and 3 are deterministic scripts. Stage 4 is an **independent** model (Codex) with no shared
context, forming a validate → fix → re-render cycle.

### Stage 1 — Extract (`scripts/extract.py`)
From `youtube-extraction.md`. Cascade, fail-soft, assemble one bundle:
1. **Metadata + chapters** via `yt-dlp --skip-download --write-info-json` (only yt-dlp exposes chapters).
2. **Transcript** cascade: `youtube-transcript-api` (manual → auto) → `yt-dlp` subs → **whisper.cpp** on
   downloaded audio. Always keep timestamps.
3. **Visuals (optional, if slide/diagram-heavy or `--with-frames`):** `yt-dlp` 720p → `ffmpeg` scene-detect
   keyframes → `tesseract` OCR; keep text-heavy frames (>15 words), perceptual-hash de-dupe.
4. Emit **`context.json`**: `{meta, chapters[], transcript[{start,dur,text}], onscreen[{t,text,frame}]}`.

Flags: `--cookies-from-browser safari` fallback for bot-detection; `--with-frames` to opt into the
heavier visual pass; `yt-dlp -U` reminder in error path.

### Stage 2 — Structure (Claude, guided by `SKILL.md`)
Read the whole `context.json` (never chunk-by-chunk — best-practices "reframe at the end"), then run the
mental passes **Structure → Salience → Vocabulary → Layout → allocate**, and emit `layout.json`.

**Layout selector** (Nitya's "layout = shape of content", merged with best-practices rule):

| Signal in `context.json` | `layout` | Notes |
|---|---|---|
| Chapters present, 3–12, enumerable topics | `grid` | one cell per chapter; **default when chapters exist** |
| No chapters, one long talk, many themes | `popcorn` | ~6–10 numbered nodes + flow arrows |
| Single concept, parts radiate from a core | `radial` | central anchor/glyph, sections around it |
| Sequential tutorial / how-to / journey | `path` | numbered stops along a winding road |
| Interview / fireside / Q&A | `conversation` | speaker anchor + speech-bubble Q&A |
| Fallback | `grid` (chapters) or `popcorn` | linear is the safe default |

**Condensing rules (the constraint is the feature):**
- **Hard budget:** 3–12 sections (grid) / ≤10 nodes (popcorn). A 2-hr talk → ~10 nodes.
- Per section: **header ≤6 words** (a question works great — "What is X?"), **≤4 takeaway bullets**,
  **≤1 boxed quote**, **1 icon** from the library.
- Bullets are **takeaways/the "so what", never transcript**. Every section ends on a conclusion.
- Map transcript+OCR nouns → icon names from the library; one boxed key phrase per section.

**Product-name verification (required step).** Auto-captions and ASR routinely mangle product,
brand, and feature names — e.g. this keynote's transcript said *"Pixie"* but the product is
**PXI** (Phoenix Intelligence), and *"Alex"* for Arize's **Alyx**. Before finalizing `layout.json`:
1. Scan the transcript + on-screen text for likely **proper nouns / product / feature / company
   names** (capitalized terms, repeated jargon, anything that looks branded).
2. **Web-search each candidate** to confirm the correct spelling and casing (check the vendor's own
   site/docs/GitHub). Note that Arize favors specific casing — `AX`, `Phoenix`, `Alyx`, `PXI`,
   `OpenInference`, `ADB`, `Signal` (see the `arize-product-names` memory / `assets/brand`).
3. Correct every occurrence in headers, bullets, and quotes. When a name can't be confirmed, prefer
   a verified alternative or drop it rather than print a guessed name.
This runs in stage 2 (Claude has web search) and its corrections flow straight into `layout.json`.

### Stage 3 — Render (`scripts/render.mjs`, Node)
`layout.json` → Handlebars HTML + inline SVG, drawn with **rough.js**, screenshotted by **Playwright**.

- **Sketchy primitives via rough.js:** every container, banner ribbon, divider, arrow, checkmark bullet,
  and underline is a rough.js shape (hand-drawn wobble, hachure/marker fills).
- **Icons:** small domain-icon library (`assets/icons/`, a Lucide subset — Lucide is the design system's
  own icon substitute) rendered through an **SVG roughen filter** (`feTurbulence` + `feDisplacementMap`)
  so clean line icons read as hand-drawn. rough.js primitives for anything not in the set.
- **Type:** hand-lettered webfont for **title + headers** (candidate: **Shantell Sans** — variable, modern,
  legible hand font; or Caveat for a looser look). Body/bullets in a **legible** hand font at readable size.
  *(Knob: headers hand-lettered always; body legibility is the tension — see open questions.)*
- **Color = function** (Arize tokens, from `nitya-narasimhan-visual-analysis.md` §5):
  - canvas `--bg-0 #121221` (**default — Arize is dark-first**) / `--bg-light-0 #F9F9FA` (light variant via `--light`)
  - linework + body ink `--fg-ink #5F5F73` (light) / `--fg-1 #F7F7FC` (dark)
  - **one accent = Arize pink `#EA338A`**, reserved for **flow arrows + emphasis only**
  - per-section **hue codes** cycled from {teal `#008394`, indigo `#7582FF`, purple `#8B4FD4`, magenta `#C2266F`}
  - **knockout** (canvas-color) header text on solid hue banners
- **Footer:** the **full-color Arize logo** (pink mark + wordmark — `arize-logo-pink-black.svg` on
  light, `-pink-white.svg` on dark), bottom-right, above a hand-drawn rule. No source URL, no
  attribution text, no top-corner mark. The logo is the only branding.
- **Output:** PNG at high res (e.g. 2× device scale). Aspect per layout: grid 16:9 or 1:1, popcorn 4:3,
  path 2:1, radial/conversation 1:1.

### Stage 4 — Validate (independent, Codex) → `scripts/validate.mjs`
An adversarial fidelity pass run by a **different model with no shared context**. Codex sees only the
rendered **PNG** and a **ground-truth transcript** built from `context.json` — never our `layout.json`
or reasoning — so it can catch what the drafting model is blind to.

```
node scripts/validate.mjs --image out/<name>.png --context work/context.json --out work/findings.json
```

- Invokes `codex exec -s read-only --skip-git-repo-check -i <png> --output-schema <schema> -o <out>`.
- Codex reads the image (title, every cell, quotes, footer) and checks against the transcript for:
  **accuracy** (every claim supported), **hallucination**, **name-casing**, **missing** key points,
  **readability**. Emits schema-validated `findings.json`: `{verdict, summary, issues[], missing_key_points[], strengths[]}`.
- **Crucial nuance baked into the prompt:** the transcript is auto-generated and misspells proper
  nouns, so Codex judges *meaning* against the transcript but defers to *real-world* spelling for
  product/feature/company/people names (it must flag, not copy, transcript name errors). This is why
  it correctly accepted **PXI** even though the transcript said "Pixie."
- Exit code: `0` = pass, `3` = revise. **The cycle:** on `revise`, Claude applies the suggested fixes
  to `layout.json`, re-renders (stage 3), and re-validates until pass. `missing_key_points` are
  advisory — omissions are often intentional given the hard section budget; Claude decides.
- Then surface the final PNG/SVG to the user.

**Prereq:** `codex` CLI on PATH + a working `codex login`.

#### Stage 4b — Video-grounded validation (Gemini) → `scripts/validate-video.py`
A second, stronger independent validator that **watches the actual video** (Gemini natively ingests a
public YouTube URL — audio + visuals). Same `findings.json` shape, same cycle.

```
python3 scripts/validate-video.py --image out/<name>.png --context work/context.json
```

- Gemini sees the real video + the sketchnote PNG (no layout/reasoning). It **reads on-screen slide
  text as the authoritative source for product names**, and checks visual claims/diagrams/numbers the
  transcript can't carry. Prereq: `GEMINI_API_KEY` + `pip install google-genai`; video must be public.
- Complementary to Codex: Codex = different-model cross-check on substance (cheap, text); Gemini =
  fidelity against what's actually on screen. **Proven:** on the keynote, Gemini read the 02:41 slide
  and corrected the harness list to *Hermes, OpenClaw, Cursor* — an error neither Claude nor Codex
  could catch from the transcript alone, and flagged the missing "AX Agent Improvement Loop" diagram.

---

## `layout.json` schema (sketch)

```jsonc
{
  "title": "Prompt engineering fundamentals",
  "subtitle": "from <channel>",                 // sentence case, Arize voice, no emoji
  "source": { "url": "...", "channel": "...", "duration": "PT15M" },
  "layout": "grid",                              // grid|popcorn|radial|path|conversation
  "canvas": { "theme": "light", "aspect": "16:9", "cols": 4 },
  "sections": [
    {
      "n": 1,
      "header": "Core concepts",                 // ≤6 words; a question is ideal
      "hue": "teal",                             // section group color
      "icon": "brain",                           // from assets/icons library
      "bullets": ["Prompt vs tokenization", "Instruction-tuned LLMs"],  // ≤4 takeaways
      "quote": null                              // optional, ≤1 boxed phrase
    }
  ],
  "flow": [[1,2],[2,3]],                         // arrows (popcorn/path/radial)
  "footer": { "left": "<source url>", "right": "arize" }
}
```
A `scripts/layout.schema.json` enforces the budgets (max sections, max bullets, header length).

## Proposed repo layout
```
SKILL.md                      # trigger + the stage-2 structuring instructions + layout rules
scripts/
  extract.py                  # stage 1
  render.mjs                  # stage 3 (rough.js + Playwright)
  layout.schema.json
  package.json                # playwright, roughjs, handlebars
templates/
  sketchnote.hbs              # HTML skeleton per layout
  sketchnote.css              # sketchy + Arize tokens
assets/
  brand/  (existing)          # colors_and_type.css, logos, brand-notes
  fonts/  (hand font + Rubik/Stakkat as needed)
  icons/  (Lucide subset → roughened at render time)
research/ (existing)
samples/                      # generated examples for regression/eyeballing
```

## "Fun & engaging" checklist (baked into stage 2/3)
Recurring host glyph · personality in the subtitle (Arize voice) · visual metaphors via domain icons ·
one boxed punch-quote per section · consistent cell rhythm · sketchy hand throughout · color that *codes*
meaning so the page reads as a map, not a wall of text.

## Build plan (phased)
1. **Skeleton + render first** — hardcode a sample `layout.json`, build `render.mjs` + templates, get one
   good-looking hand-drawn PNG in each layout. (Render is the riskiest unknown; de-risk it first.)
2. **Extract** — `extract.py` happy path (captions + chapters) → `context.json`; add whisper + frames/OCR fallbacks.
3. **Structure** — write the stage-2 rules into `SKILL.md`; wire end-to-end on a captioned, chaptered video.
4. **Polish** — icon library, host glyph, dark variant, density auto-balancing, review loop.
5. **SKILL.md finalize** — triggers, args (`<url> [--dark] [--with-frames] [--layout ...]`), setup notes.

## Knobs — RESOLVED (2026-06-26)
1. **Body legibility vs. hand-lettering** → *legible* hand font (**Shantell Sans**) for body/headers,
   looser hand (**Permanent Marker**) for the title. Sketchy-but-readable.
2. **Icon sourcing** → **roughen-filtered Lucide** to start; review after the first render.
3. **Output** → emit **both PNG and SVG**.
4. **Frames/OCR** → **opt-in** (`--with-frames`); captions+chapters carry most videos.
5. **Where the skill lives** → **this repo**, standalone.
```
