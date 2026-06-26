# Plan: richer visuals — beyond ordered boxes

Goal: move the output from a clean **grid of bordered boxes** toward Nitya-style pages that are
**alive** — spot illustrations, a recurring character/mascot, varied containers (clouds, banners,
speech bubbles), weaving hand-drawn connectors, sparkles/emphasis marks, and highlight washes — while
keeping it legible, on-brand, and deterministic. The boxes become *one* container type among many, and
the strict grid becomes *one* layout among several.

Grounded in `research/nitya-narasimhan-visual-analysis.md`: her density reads as rich, not chaotic,
because a strong scaffold (numbers + arrows + consistent rhythm) carries decoration on top. So we add
richness **as layers on top of structure**, not by removing structure.

## What's missing today (current renderer)
- Every section is the same bordered rectangle. No container variety.
- One small icon per cell; no larger focal illustrations, no people/characters, no metaphors.
- No connectors between cells, no marginalia (sparkles, arrows, bursts, underlines, doodles).
- Strict equal grid; no size variation, no hero anchor, no free-form placement.

## The four layers we'll add
1. **Marginalia** — small non-semantic hand-drawn flourishes: sparkles, stars, emphasis bursts,
   curved arrows, dotted trails, underline swooshes, brackets, `!`/`?` marks, corner doodles.
2. **Containers** — per section, choose: box · cloud · banner ribbon · speech bubble · sticky note ·
   torn-paper · *borderless* (header + underline only). Mix them for rhythm.
3. **Figures & spot illustrations** — a larger focal visual per ~3rd section, a recurring host/mascot,
   and (optional) hand-drawn people. Metaphors, not just UI glyphs.
4. **Connectors & composition** — hand-drawn arrows/trails that link related sections and carry the
   reading order; variable module sizes (a hero cell); a title anchor illustration; eventually
   non-grid layouts (radial / popcorn / path).

## Where the assets come from (recommended mix)
- **Procedural via rough.js** for all of layer 1 + most of layer 2. Sparkles, arrows, bursts, banners,
  clouds, bubbles, dividers are simple paths — rough.js draws them hand-style, in our exact palette,
  seeded for stable-but-varied output, infinite and zero-license-risk. This is the workhorse.
- **Curated CC0 sets** for object/metaphor focal illustrations:
  - **Open Doodles** (CC0) — loose hand-drawn object/scene illustrations.
- **Real-speaker sketches (no generic character).** Decision: do NOT add a generic mascot/host. Instead,
  when feasible, extract the video's **main speakers** (names + roles from Gemini `video_notes`, which
  already reads the on-screen "Name, Title" lower-thirds) and a representative **frame** of each
  (ffmpeg at a timestamp Gemini supplies), then **stylize the frame into a sketch portrait** (posterize
  + edge + the existing `#roughen` filter) for a small "speakers" credit. If speakers can't be reliably
  isolated, add no character at all. → Phase B feature (`scripts/speaker-sketch.py`).
- **Roughen-filtered Lucide** (already in place) continues for precise domain icons (database, shield…).
- *Not* AI-generated assets for v1: consistency, licensing, and text-in-image risks outweigh the speed.
  (Could revisit for a one-time, vetted metaphor set later.)

All three render through the same SVG pipeline + the existing `#roughen` filter so they share one hand.

## Implementation phases

### Phase A — Visual vocabulary library (stays in the grid) ⟵ start here
Biggest richness-per-effort, no layout-engine work.
- `templates/doodles.js`: a procedural rough.js library exporting `drawSparkle/star/burst/arrow/
  trail/swoosh/bracket/bang/divider`, plus container drawers `box/cloud/banner/bubble/sticky/underline`.
- Extend `render.mjs` + draw step so each section can specify `container` and `emphasis`, and so a
  **decoration pass** sprinkles seeded marginalia into whitespace + draws a few accent arrows between
  related cells (from `flow`, optional). Deterministic per-render seed.
- **Highlight washes**: rough.js `hachure` fill in a hue tint behind a key phrase / focal icon.
- **Title anchor**: a small spot illustration beside the title.
- Schema additions: `section.container`, `section.emphasis`, `section.figure`, top-level
  `decor: {density: none|light|medium, seed}`.
- Guardrails: decoration never overlaps text (place in measured gaps); density budget; legibility first.

### Phase B — Figures, characters & focal illustrations
- Wire **Open Peeps** + **Open Doodles** into `assets/figures/`; a small curated, tagged subset
  (host, audience, robot, cloud, magnifier, gears, rocket, brain, chart…). `section.figure: "<tag>"`.
- A **recurring host motif** placed with rhythm (title + a few cells) for cohesion — Nitya's signature.
- Larger focal illustration in ~1-in-3 sections instead of the small corner icon.

### Phase C — Break the grid (new layouts)
- A light **layout engine**: `radial` (center anchor + spokes), `popcorn` (jittered nodes + numbered
  arrow path), `path` (winding spline with stops). Compute module positions, then draw rough
  connectors between measured anchor points (we already measure rects).
- **Variable module sizes** (hero cell spanning 2 cols; small satellite notes) even within grid.
- Hook into the existing layout selector so content shape picks the layout (chapters→grid,
  keynote→popcorn, single concept→radial, tutorial→path).

### Phase D — Composition polish & control
- Decoration-density knob, collision avoidance, seeded variation, dark-mode parity for every new asset,
  and a validator note so Codex/Gemini judge *clutter & legibility*, not just facts.

## Risks / principles
- **Clutter is the enemy.** Every added phase ships with a density budget and a "legibility first" rule;
  decoration is subordinate to the content scaffold.
- **Stay on-brand.** Arize is serious/engineer-to-engineer — favor restrained, confident marginalia over
  cutesy. (This is why "include hand-drawn people?" is a real choice — see questions.)
- **Determinism.** Seed all randomness so a re-render is stable; vary by section index, not RNG that
  breaks the Workflow-style resume.

## Suggested sequencing
Phase A first (richest payoff, no engine work) → review on the keynote → then B or C depending on taste.
