# Arize brand notes (for sketchnotes)

Distilled from the **Arize Design System (May 2026)** — `claude.ai/design` project
`019ddf2b-02aa-70c6-9325-e50a8e8ba3a3`. Tokens live in `colors_and_type.css`;
logos in this folder (`arize-logo-light.svg`, `arize-mark.svg`).

> A sketchnote is hand-drawn and playful, so treat this as a **palette + type + voice**
> guide, not pixel-perfect component specs. Borrow the colors, fonts, and tone; render
> them in a loose, hand-drawn style.

## Who Arize is
AI engineering platform for the agent era — "the feedback loop for agents." Gives AI
engineers observability, evaluation, and development tooling in one place.
Surfaces: **AX** (platform), **Phoenix** (OSS), **Alyx** (the AI engineering agent), **ADB** (agent datastore).

## Palette (sketchnote-ready)
Arize is **dark, deliberate, technical**. The pink accent is used *sparingly*.

| Role | Hex | Use in a sketchnote |
|---|---|---|
| Page canvas (dark) | `#121221` | Background if going dark |
| Alt band / near-black | `#0E0D14` | — |
| Light canvas | `#F9F9FA` | Background if going light (likely better for hand-drawn) |
| Ink (text on light) | `#5F5F73` | Primary linework/lettering on light bg |
| Primary text on dark | `#F7F7FC` | Linework/lettering on dark bg |
| **Pink (brand)** | `#EA338A` | **The one signature accent** — highlights, the star, key idea pops |
| Magenta CTA | `#C2266F` | Secondary accent / fills |
| Teal | `#008394` | Links, secondary accent, grouping |
| Indigo | `#7582FF` | Data-viz / diagram accent (dominant in their charts) |
| Purple | `#8B4FD4` | Tertiary accent, agent/graph nodes |

**Sketchnote color rule (from best-practices research):** black/ink + one grey + **one** accent
(pink). Use indigo/teal/purple only when you need 2–3 functional groupings. Accent ≠ decoration.

## Type
- **Rubik** — workhorse (display + body). **Light 300 at large sizes is the signature look.**
- **Stakkat** — punch display font for hero/title moments ("Don't ship vibes"). Use for the sketchnote title.
- **Geist Mono** — technical labels, tags, code, numbers.
- For hand-lettered sketchnote feel, pair a hand-drawn display for the title with Rubik for legible body, or emulate Rubik Light + Stakkat where literal hand-lettering isn't used.

## Voice / tone
Engineer-to-engineer, confident, unfussy. Direct technical README energy, mildly cocky.
- **Sentence case everywhere** — no Title Case, no SHOUTING.
- Short declaratives, often three-item lists: "Observe. Evaluate. Develop."
- Negation hooks: "Don't ship vibes", "No black box eval models."
- **No emoji.** Acronyms exposed, not hidden (RAG, LLM, OTel, eval, span).
- Refer to products by name (Alyx, Phoenix, AX), not "our agent."

Signature phrases: "The feedback loop for agents" · "Don't ship vibes" ·
"One place for development, observability, and evaluation" · "Built on open source & open standards."

## Logos
- `arize-mark.svg` — the pink "a" triangle mark (uses `currentColor`; set fill to pink `#EA338A`).
- `arize-logo-light.svg` — mark + wordmark in near-white `#F7F7FC` (for dark backgrounds).
- Pink mark = `#EA338A`. Drop the mark somewhere on the sketchnote for branding.
