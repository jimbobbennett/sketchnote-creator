# Design systems

The sketchnote's look — palette, fonts, logo, voice — is a **pluggable design system**, so this skill
works for anyone, not just Arize. A design system is a folder under `design/<name>/` containing a
`design.json` (and any logo SVGs it references).

- **`design/default/`** ships with the repo — a brand-agnostic palette + free Google fonts + a simple
  pencil logo. Used automatically when you don't pass `--design`.
- **Your own brand** goes in `design/<name>/` and stays **local** (git ignores everything under
  `design/` except `default/` and this README). Point the tools at it with `--design design/<name>`.
  (Arize's lives in `design/arize/`, untracked.)

## `design.json`

```jsonc
{
  "name": "Acme",
  "footerText": "acme",            // optional small text by the footer logo (omit if your logo has a wordmark)
  "defaultTheme": "dark",          // "dark" | "light"
  "accent": "#F2545B",             // the single accent — quote bubbles, checks, emphasis, portrait circles
  "hues": {                        // four section-colour slots (names are fixed; pick any colours)
    "teal": "#2A9D8F", "indigo": "#4C6EF5", "purple": "#7C5CDA", "magenta": "#D6336C"
  },
  "dark":  { "canvas": "#16181D", "ink": "#F2F3F5", "ink2": "#A0A3AD", "grain": "#ffffff08" },
  "light": { "canvas": "#FBFBF9", "ink": "#2E3138", "ink2": "#878A93", "grain": "#00000006" },
  "fonts": {
    "title": "Permanent Marker",   // display/title hand font
    "hand": "Shantell Sans",       // legible hand font for headers + body
    "mono": "Geist Mono",          // labels / footer text
    "googleImport": "Permanent+Marker&family=Shantell+Sans:ital,wght@0,300..800;1,300..800&family=Geist+Mono:wght@400;500"
  },
  "logo": { "dark": "logo.svg", "light": "logo.svg" },  // optional; per-theme. SVGs with currentColor adapt to --ink
  "voice": "One or two sentences describing the writing voice for headers/bullets/quotes."
}
```

## Make your own

1. `cp -r design/default design/mybrand`
2. Edit `design/mybrand/design.json` — set `accent`, the four `hues`, `dark`/`light` tones, `fonts`
   (any Google Fonts; update `googleImport` to match), and `voice`.
3. Drop a logo SVG in the folder and point `logo.dark` / `logo.light` at it (use `currentColor` strokes
   so it adapts to light/dark), or remove `logo` and rely on `footerText`.
4. Render with it: `node scripts/render.mjs <layout.json> --out out/x --design design/mybrand`
   (and pass the same `--design` to `slide-sketch.py` so slide sketches pick up your hues).

The `hues` keys (`teal/indigo/purple/magenta`) are just four colour **slots** — a section's `hue` in
`layout.json` refers to a slot, so any palette works without changing layouts.
