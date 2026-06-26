# Nitya Narasimhan — visual technique analysis (from real sketchnotes)

Direct visual analysis of 7 of her sketchnotes pulled from `cloud-skills.dev/gallery`
(originals + 2000px copies in `research/nitya-samples/`). Goal: **learn her transferable
technique** — composition, hierarchy, navigation, color logic — *not* copy her hand-drawn style.
Companion to `nitya-narasimhan-sketchnotes.md` (her stated process); this is what the images
actually show.

## Samples analyzed (deliberately spanning her range)
| File | Content | Layout it demonstrates | Aspect |
|---|---|---|---|
| `AI-001-prompt-engineering` | Concept explainer, 7 topics | **Modular grid** (8 cells) | 16:9 |
| `AI-005-azureai-agents-service` | Deep dive, 25 Q&As | **Dense modular grid** (5×5) | 1:1 |
| `MSBuild-2022-SatyaKeynote` | 2-hr keynote | **Numbered popcorn / path** | ~8:7 |
| `DAPR-1-Overview` | Tech/product overview | **Freeform radial w/ central anchor** | 4:3 |
| `Codeland-KelseyHightower` | Fireside interview | **Conversation flow** (speech-bubble Q&A) | 1:1 |
| `Azure-0-FundamentalsPaths` | Learning journey | **Path / road map** (dark bg) | 2:1 |
| `VisualizeIT-StorytellingForTech` | Her meta-talk on visual notes | **Hybrid** (boxes → toolkit path + zine) | 4:3 |

---

## 1. Composition — she never lets the eye get lost

- **Title block anchors the top-left** (occasionally top-center). Oversized hand-lettered display
  word(s) in a box/banner, with a **small "anchor" illustration** directly beneath establishing the
  topic (e.g. prompt-engineering shows a little classroom scene; DAPR shows a "DAPR 1.0 IS HERE" mini-poster).
  → The title is a *graphic*, not just text.
- **Explicit reading order, every time.** She picks a navigation system up front and commits to it:
  - **Numbers** (1→7, 1→10, 1→25) on every section. The viewer always knows where to start and what's next.
  - **Bold arrows in a contrasting accent color** (usually orange/red) physically draw the path between nodes.
  - No piece relies on "just scan around" — there's always a skeleton.
- **Edge-to-edge density is fine *because* the scaffold is strong.** The keynote and 25-cell agent
  notes are extremely dense, yet readable — the grid + numbering + banners impose order so density
  never becomes chaos. **The lesson: earn density with structure, don't avoid it.**

→ **For the generator:** choose the navigation system from content shape, then enforce it rigidly —
numbered sections + accent-colored flow arrows + a title-graphic top-left. Density is acceptable
*only* once that scaffold exists.

## 2. Layout is chosen by the **shape of the content** (the key takeaway)

She doesn't have one layout — she has a repertoire, and matches it to structure:

| If the content is… | She uses… | Examples |
|---|---|---|
| An enumerable list of topics / chapters | **Modular grid**, one cell per topic, identical cell template | prompt-eng (7), agents (25) |
| A long talk with many themes | **Numbered popcorn**: big numbered nodes snaking across, arrows between | Satya keynote (10 nodes for a 2-hr talk) |
| A single concept/product with parts radiating from a core | **Freeform radial** around a central anchor/mascot | DAPR (robot mascot in center) |
| A sequential journey / curriculum | **Path / winding road** with lettered or numbered stops | Azure Fundamentals (Parts 1–6, steps A–F) |
| An interview / narrative | **Conversation flow**: speaker portrait + speech-bubble Q&A linked by arrows | Kelsey Hightower |

→ **For the generator:** this maps almost 1:1 onto our best-practices "layout decision rule."
YouTube **chapters → modular grid**; a keynote with no chapters but many topics → **popcorn**;
a single-concept video → **radial**; a tutorial/how-to → **path**. Make layout a function of the
extracted structure, not a fixed template.

## 3. The repeating **cell template** — what makes her grids work

In the grid pieces every cell is the *same* structure, which is exactly why 25 cells stay legible:

```
┌─────────────────────────────┐
│ [①] NUMBERED COLOR BANNER    │  ← knockout (white) text on a solid color fill = the skeleton
│  ┌───────────────┐          │
│  │ small diagram / │  host   │  ← 1 domain icon or mini-diagram + the recurring host character
│  │ icon cluster    │  avatar │
│  └───────────────┘          │
│  ✓ takeaway bullet           │  ← 2–4 checkmark bullets = the "so what", never a transcript
│  ✓ takeaway bullet           │
└─────────────────────────────┘
```

- **Header = numbered banner, knockout text on solid color.** Scanning just the banners gives you
  the whole outline. This is her hierarchy level 1.
- **Body = one small visual** (icon cluster / mini-diagram), level 2.
- **Footer of each cell = checkmark takeaway bullets**, level 3 — she always extracts conclusions.
- A **question often *is* the header** ("What is an AI agent?", "How do I build complex workflows?").
  Q-as-section is a great fit for talk content.

→ **For the generator:** define a single cell component (banner + icon slot + ≤4 bullets) and reuse it.
Consistency of the cell is the readability mechanism. Force a per-cell takeaway so output is insight,
not transcript.

## 4. Recurring **host character** = rhythm + identity

- A single consistent avatar (a woman in a pink top at a screen/desk) **appears in nearly every cell**
  of the AI notes. It gives visual rhythm, a sense of a narrator, and instant brand recognition across
  her whole catalog.
- For interviews she instead draws the **actual speaker's portrait** as the anchor.

→ **For the generator:** a recurring simple "host" motif across sections adds cohesion and brand.
For Arize this could be the **pink "a" mark** as a recurring glyph, or a tiny consistent mascot.
Cheap to template, high payoff for cohesion.

## 5. Color is **functional, never decorative**

- **Light cream/paper background is the default**; she flips to a **dark background only when she wants
  the palette to read as a "map"** (Azure Fundamentals path on near-black, neon-bright nodes). Deliberate.
- **Color codes meaning / grouping**, not mood:
  - Azure Fundamentals: each "Part" gets its **own hue**; a topic keeps its color wherever it recurs.
  - "Security" / one theme = one consistent color throughout a piece.
- **One accent reserved purely for flow** — the orange/red arrows pop *because* they're the only thing
  in that color, so the reading path separates from the content.
- **Knockout text (white on solid color)** for all section headers.
- Per piece the working palette is small (≈3–5 functional colors + background) — matches both the
  general sketchnote rule and Arize's "accent sparingly."

→ **For the generator (maps cleanly onto Arize tokens):** ink/dark linework + lettering;
**one accent (Arize pink `#EA338A`) reserved for flow arrows + emphasis**; assign teal `#008394`,
indigo `#7582FF`, purple `#8B4FD4` as the **per-section/group hue codes**; knockout text on banners.
Default to light canvas `#F9F9FA`; offer dark `#121221` as a "map" variant.

## 6. Visual vocabulary she leans on

- **Containers:** rounded boxes (default), ribbon/flag **banners** for headers, **speech bubbles** for
  quotes/asides. Clouds are rare.
- **Connectors:** bold accent arrows for primary flow; thin/dotted trails for secondary links.
- **Bullets:** **green checkmarks** for takeaways/benefits; numbered chips for steps.
- **Icons:** small, **literal, domain-specific** — DB cylinders, gears, GitHub octocat, language logos
  (Java/Go/Python/PHP/.NET as little tags), padlocks for security, a robot for "runtime." ~2–3 per section.
- **People:** simple expressive stick/blob figures; the recurring avatar; real portraits for interviews.
- **Emphasis:** size, knockout, underline, and **boxing the one key phrase** per section.

→ **For the generator:** maintain a reusable **domain-icon library** (cloud/AI/eng vocabulary) plus a
small set of container + arrow + bullet primitives. Map transcript nouns → icons; one boxed key phrase
per section; checkmark bullets for the takeaways.

## 7. How she condenses a long talk (our exact problem)

- **A 2-hour keynote → ~10 numbered nodes.** Each node = one theme: a banner + a couple of bullets +
  one icon. *Everything else is omitted.* She captures **concepts and perspective, never a transcript.**
- Each unit still ends on a **takeaway/"so what."**
- The hard page (or cell) budget is what *forces* the condensing — the constraint is the feature.

→ **For the generator:** set a **hard budget** (N sections; each = banner + icon + ≤4 bullets) and make
the LLM fit the talk into it. Budget-first is how she gets signal over noise.

## 8. Consistent **footer band** (provenance + brand)

Every piece ends with a fixed footer: **source URL** (e.g. `aka.ms/...`) on the left ·
**"Sketchnotes by @nitya / @sketchthedocs"** center · **gallery URL** (`*.sketchthedocs.dev`) right.
Attribution, provenance, and brand in one strip.

→ **For the generator:** template a footer = **source video URL · "generated by …" · Arize brand mark**.
Good provenance and on-brand by default.

---

## What to take vs. leave

**Take (technique):** layout-by-content-shape; rigid navigation (numbers + accent arrows); the repeating
cell template (banner → icon → takeaway bullets); question-as-header; functional color coding with one
flow-accent; recurring host motif; hard budget to force condensing; provenance footer; "end every unit
on a takeaway, not a transcript."

**Leave (her personal style):** her specific hand-lettering, the pink-top avatar, her exact icon drawings,
her palette. We render in **Arize's** voice and palette — her *structure* is the transferable asset.

## Sources
- Gallery: https://cloud-skills.dev/  (images under `https://cloud-skills.dev/gallery/`)
- Samples saved locally: `research/nitya-samples/` (full-res) and `research/nitya-samples/small/` (2000px)
- Her process notes: `research/nitya-narasimhan-sketchnotes.md`
