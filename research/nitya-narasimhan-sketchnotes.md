# Nitya Narasimhan — Sketchnoting Research

Research compiled June 2026 to inform an auto-sketchnote-from-YouTube tool. Findings
are drawn from Nitya's own posts, talk decks, and project sites. Where a point is
**her specific recommendation**, the source is cited inline. Where something is general
sketchnote lore she merely references, it is flagged as such. Gaps are called out
explicitly rather than invented.

> A recurring "→ For the generator" callout translates her practice into concrete
> behavior for our auto-generation tool.

---

## 1. Who she is and her connection to sketchnoting

- **Nitya Narasimhan, PhD** (Computer Engineering). 25+ years across industry, startups,
  academia, and community. Self-described "Creative Technologist." At the time of her
  core sketchnoting content she was in Developer Relations at Microsoft (Azure
  Advocates / Developer Relations Regional PM, North America). [nitya.dev, dev.to/azure]
- She runs three "personas," one of which is the sketchnoting brand:
  - **Nitya** — career/tech/parenting/community writing.
  - **SketchTheDocs** — "visual storytelling bringing tools like sketchnoting, visual
    puzzles, hand-drawn illustrations, and more, to make complex concepts easier to
    understand and recall for visual learners." [nitya.dev]
  - **In30Days** — month-long learning sprints.
- **What she sketchnotes:** technical/developer content — Azure services, AI/ML
  (prompt engineering, fine-tuning, model selection, Azure AI agents), .NET, Flutter,
  GoLang, Playwright, Microsoft Build keynotes, DAPR, cloud-native architecture,
  sustainability, plus soft-skills topics (technical storytelling, livestreaming).
  [cloud-skills.dev]
- **Where she publishes:**
  - **sketchthedocs.dev** — the project hub.
  - **cloud-skills.dev** — the actual gallery, "a sketchnotes repository for all things
    Cloud Computing and Azure," 40+ visual guides organized alphabetically by prefix
    (AI-, Azure-, etc.), each a thumbnail linking to a full-res single-page image.
  - **@sketchthedocs** on Twitter/X — each sketchnote posted with: hi-res drawing link,
    a time-lapse/replay of the drawing being created, and a blog post with detail.
  - **DEV (dev.to/azure, dev.to/nitya)**, Speaker Deck, and the **#VisualizeIT** workshop
    series (Microsoft Reactor + Azure Advocates).
  - GitHub: `github.com/sketchthedocs` and `github.com/nitya`.

→ For the generator: her published artifact is consistently **one full-resolution
single-page image per topic** plus a short replay animation. That is the output shape
to target.

---

## 2. Her process / methodology

Her clearest articulation is a **three-stage skill progression** (from the "Sketch The
Docs" deck):

1. **Practice handwriting** — "slow & steady." Legible lettering first.
2. **Work on pacing** — "live notes capture." Keeping up in real time.
3. **Refactor for impact** — "leaves spaces, fill in after." Lay down structure live,
   then go back and polish/decorate.

The **session flow she teaches** (Sketchnoting 101 deck):

1. **Pick a target** from one of three content types:
   - a documentation page (a *concept*),
   - a tutorial (a *learning* unit),
   - a video (a *talk*).
2. **Choose a layout** before drawing:
   - **Freeform** — single page, words + images, focus on pacing/structure/clarity, OR
   - **Zine** — an **8-panel grid on a single sheet** (8-cell comic), a more constrained,
     guided composition.
3. **Capture in real time** with words + images; leave space; **refactor afterward**.

Her stated mental model: sketchnoting is **"Rapid Capture of concepts or ideas, often
in real-time,"** combining words and images "to create visual interest, clarify ideas,
and aid recall." The repeatable structure is *layout-first, then capture, then refactor.*

She also frames the value as cognitive, not decorative: "the act of writing something
down helps your brain remember it and gives it context for recall," and a sketchnote
"reduce[s] long talks or pages of text to a simple sheet with visual cues that anyone
can understand." [dev.to/azure]

→ For the generator: mirror **layout-first**. Decide freeform vs. fixed grid (zine)
*before* placing content. The zine's **8-cell grid is a directly implementable
template** — segment a talk into 8 beats, one per cell. The "leave space, fill in after"
stage maps to a two-pass render: (1) place structure/text, (2) decorate with icons,
color, and connectors.

---

## 3. Her tools

- **Hardware/app:** **iPad + Procreate.** This is consistently her digital tool. She
  values Procreate because "you can do a lot of things with brushes, textures and inks,
  and it allows you to apply algorithms to smooth any lines so it looks fairly neat."
  [dev.to/azure]
- **Paper-first for learning:** she explicitly tells beginners to **start on paper**:
  "Grab paper (or index cards) and a pen. Color pens/pencils are optional bonuses."
  Workshop materials list: "Lots of paper, pens, and a few color markers or pencils."
  Digital comes *after* the paper foundation. [Sketchnoting 101 deck; VisualizeIT]
- **Fonts:** she names **Monoton (Google Fonts)** as an example of a large block title
  font. General guidance: vary font style for emotion/context and font size for
  hierarchy. [Sketchnoting 101 / Sketch The Docs decks]
- **Icons:** **The Noun Project** for inspiration and attribution. [decks]
- **Colors:** she does **not** publish a fixed hex palette. Her rule is **pick 2–3
  colors**, use a background color for separation, reinforce connections via color, and
  **consider color-blind accessibility.** (See §7 — no shared swatch kit found.)

→ For the generator: the digital equivalents of her toolkit are concrete: a **block
display font for titles** (Monoton-style), a clean handwriting/marker font for body,
an **icon set keyed to a domain vocabulary** (Noun-Project-style line icons), and a
**constrained 2–3 color palette + one background tint**, with contrast checked for
accessibility.

---

## 4. Her specific best-practice tips and advice

Direct, attributable advice (her words / her decks):

- **"It's About Ideas Not Art!"** — her central tenet. "Sketchnoting (and visual
  storytelling) are not about art and perfection; they are about ideas and
  perspectives." [dev.to/azure]
- **"You don't need to be an artist! It's your perspective that makes this unique."**
- **"Practice is everything!" / "Practice! Try out three simple targets to practice
  first steps!"** (concept, tutorial, talk).
- **Copy / trace to learn.** She leans on Austin Kleon — "nothing is original. We are
  all simply building on other people's ideas" — and explicitly recommends **tracing
  icons and fonts** from existing examples to build skill. [dev.to/azure]
- **Build a personal vocabulary cheatsheet:** for **icons** ("build visual vocabulary
  for your domain," recognizability over artistry) and for **people** ("build a postures
  cheatsheet"). [Sketch The Docs deck]
- **The three-word mindset for sharing:** **"Be Fearless. Imperfections are fine. Be
  Visible. Share your work! Be Persistent. Practice everyday."** [Sketchnoting 101 deck]
- **"#sketchercise" your mind** — spend a few minutes each morning doodling something
  fun/whimsical as warm-up. [VisualizeIT workshop]
- **Why it works for *developer* content specifically** (her three arguments):
  1. **Inclusivity** — visuals transcend language barriers.
  2. **Familiarity** — web/tech already has visual metaphors to borrow (spiders, routes,
     home pages, visitors).
  3. **Engagement** — "visual notes often have more visibility and engagement than
     written ones." [dev.to/azure — Visual Storytelling for WebDevs]
- Supporting "why" stats she cites (general claims, not her original research): ~65% of
  people are visual learners; brain processes visuals far faster than text; ~90% recall
  accuracy within 72 hours. Treat as motivational framing, not hard data.

→ For the generator: bake in **"ideas not art"** as a design constraint — favor clear
structure and legible labels over rendering fidelity. The **domain-icon vocabulary** and
**reusable character/posture set** are exactly the kind of asset libraries the tool
should maintain and reuse across videos for visual consistency.

---

## 5. Her visual style characteristics

From her toolkit breakdown (Sketch The Docs / Sketchnoting 101 decks) and the
cloud-skills.dev gallery. She organizes the craft into a named **toolkit** — the most
useful framework she's published:

| Element | Her guidance |
|---|---|
| **Fonts** | Large block font for the **title**; vary style to convey emotion/context; vary size for **priority/hierarchy**. |
| **Layouts** | Drive narrative flow; act as design patterns; add implicit constraints. Grid for zines; simple layout for freeform. |
| **Navigation** | Draw **arrows and trails** to guide the viewer between non-adjacent regions; inspiration from **games and maps**. |
| **Quotes** | Listen with intent for a **representative phrase**; showcase it prominently. |
| **Icons** | Build a **domain visual vocabulary**; recognizability over artistry; 2–3 keyword icons per section. |
| **People/Figures** | Faces create "a sense of belonging"; stick figures / gesture drawings; keep a **postures cheatsheet**; a "you" character / panel for personal perspective. |
| **Colors** | **2–3 colors**; background color for **separation**; reinforce connections; **color-blind accessibility**. |
| **Containers** | Panels/frames to group and separate content (especially the zine's character containers). |

Layout/structure patterns she favors:

- **Single page = whole talk.** Everything condenses to one sheet.
- **Two canonical layouts:** freeform single page, or the **8-cell zine grid**.
- **Title treatment:** a prominent block-font header anchoring the page.
- **Connectors over chaos:** explicit arrows/trails to show flow between ideas.
- **Gallery consistency:** across 40+ guides the format is standardized (comparable
  dimensions/complexity), which is itself a deliberate style choice for discoverability.

Note: I could not extract her exact recurring color palette or a signature
title-banner template from text sources — those live in the images themselves on
cloud-skills.dev / @sketchthedocs. To pin down her real palette and header style,
inspect a sample of those images directly (see Sources).

→ For the generator: the toolkit table is essentially a **render spec**. Each row maps
to a generation step: title (block font) → section containers → per-section icons
(2–3 keywords) → a pulled quote → connector arrows showing flow → a recurring "host"
character → 2–3 color palette with a separating background.

---

## 6. How she sketchnotes from talks / videos specifically

- **Real-time is the goal, but staged.** Her progression explicitly builds toward "live
  notes capture," and she defines sketchnoting as capture "often in real-time." But the
  refactor stage ("leave spaces, fill in after") means the polished artifact is
  **finished after** the live pass. So: capture structure live, decorate later.
- **Video is one of her three explicit target types** (alongside docs pages and
  tutorials) — in Sketchnoting 101 she cites video content (historically Channel 9 / MS
  Learn videos) as a sketchnoting source. So sketchnoting *from video* is squarely her
  established use case.
- **The "Chalk The Talk" segment** of her VisualizeIT workshop is specifically about
  **"visualizing talk flow & slides"** — i.e., turning a talk's structure into a visual.
  "Scene To Zine" is the companion segment that maps a talk into the 8-panel zine.
- **Condensing — what to include:** her selection heuristics are the toolkit elements
  applied as filters: pick **2–3 keywords per section** (→ icons), find **one
  representative quote** to feature, and use **layout/containers** to bound how much
  fits. The page constraint (one sheet, or 8 cells) forces omission. She doesn't
  transcribe; she captures *concepts and perspective.*

Note on real-time vs. after for video: she does not publish a strict rule that video
sketchnotes must be live. For a *recording* (our case) the staged approach — pause,
structure, decorate — is fully consistent with what she teaches, since the live
constraint is a skill exercise, not a requirement of the medium.

→ For the generator: this is the strongest validation of the whole concept — **video →
single-page sketchnote is exactly her workflow.** Implement condensing as: segment the
transcript into beats → per beat extract 2–3 keywords (→ icons) + at most one quotable
line → enforce a hard page/cell budget that forces omission → lay out with connectors
showing flow. The 8-beat zine is the cleanest target for a fixed-length video.

---

## 7. Reusable templates, color systems, or "sketchnote kits"

- **The zine (8-cell grid) is the one concrete, reusable template** she teaches — a
  single sheet divided into 8 panels. This is directly implementable.
- **The "toolkit" framework** (fonts / layouts / navigation / quotes / icons / people /
  colors / containers) is her reusable *method*, used across talks and posts — treat it
  as the spec, not a downloadable asset.
- **No published fixed color system / hex palette.** Her color guidance is a *rule*
  ("pick 2–3 colors, use background for separation, mind accessibility"), not a shared
  swatch set. If a brand palette is needed, it must be inferred from her images or
  defined fresh.
- **No public downloadable Procreate brush pack / template file found** in these
  sources. She points learners to general resources rather than her own kit.
- **Resources she points people to** (referenced, not authored by her):
  - *The Sketchnote Handbook* / *Workbook* and lessons — **Mike Rohde**
  - *The Doodle Revolution* — **Sunni Brown**
  - *Creative Lettering* — **Jenny Doh**
  - *Steal Like an Artist* / *On Creativity* — **Austin Kleon**
  - **illustrated.dev** — **Maggie Appleton**
  - Anthropomorphism / drawing characters — **Denise Yu**
  - *Sketchnote Lessons* — **Sacha Chua**
  - *Hand-Drawn Maps* — **Helen Cann**
  - **The Noun Project** (icons), **Google Fonts** (e.g., Monoton)
  - **LetsSketchTech** conference archive (talks)

→ For the generator: ship a built-in **8-cell zine template** as a first-class layout.
Maintain our own **domain-icon library** (Noun-Project-style) and a **default 2–3 color
accessible palette** since she provides none to copy. Her toolkit list is the feature
checklist.

---

## 8. Best quotes (attributable)

- "It's About Ideas Not Art!" — sketchthedocs / dev.to
- "Sketchnoting (and visual storytelling) are not about art and perfection; they are
  about ideas and perspectives." — dev.to/azure
- "You don't need to be an artist! It's your perspective that makes this unique." — deck
- "Rapid Capture of concepts or ideas, often in real-time." — Sketchnoting 101 deck
- "Be Fearless. Imperfections are fine. Be Visible. Share your work! Be Persistent.
  Practice everyday." — Sketchnoting 101 deck
- "The act of writing something down helps your brain remember it and gives it context
  for recall." — dev.to/azure
- On copying (quoting Austin Kleon): "nothing is original. We are all simply building on
  other people's ideas." — dev.to/azure
- Process: "practice handwriting (slow & steady)" → "work on pacing (live notes
  capture)" → "refactor for impact (leaves spaces, fill in after)." — Sketch The Docs deck

---

## Sources

Primary (her own):
- Sketch The Docs project — https://sketchthedocs.dev
- Visual guides gallery — https://cloud-skills.dev
- Her site / bio & personas — https://nitya.dev and https://nitya.dev/tags/sketchthedocs/
- Deck: *Sketch The Docs: Visual Storytelling for Developers* — https://speakerdeck.com/nitya/sketch-the-docs-visual-storytelling-for-developers
- Deck: *Sketchnoting 101: Getting Started With Visual Storytelling* — https://speakerdeck.com/nitya/sketchnoting-101-getting-started-with-visual-storytelling
- Deck: *SketchTheDocs: How Visual Storytelling Can Improve Your Learning & Communication Skills* — https://speakerdeck.com/nitya/sketchthedocs-how-visual-storytelling-can-improve-your-learning-and-communication-skills
- Post: *About #SketchTheDocs* — https://dev.to/azure/about-sketchthedocs-3ld9
- Post: *Visual Storytelling For WebDevs: Create Sketchnotes!* — https://dev.to/azure/visual-storytelling-for-webdevs-create-sketchnotes-2e00
- Post: *A Visual Guide To: Visual Storytelling* — https://dev.to/azure/a-visual-guide-to-visual-storytelling-4l2h
- Workshop writeup: *#VisualizeIT Workshop 3: "Sketch The Docs, Chalk The Talk"* — https://dev.to/letssketchtech/visualizeit-workshop-3-sketch-the-docs-chalk-the-talk-nitya-narasimhan-197f
- Twitter/X stream (hi-res + replays) — https://twitter.com/sketchthedocs
- GitHub — https://github.com/sketchthedocs and https://github.com/nitya
- Illustrated Guide to Fusion Dev — https://sketchthedocs.github.io/ig-fusion-dev/
- Visual puzzles / Visualize-It — https://aka.ms/visual/absee, https://aka.ms/visualize-it, https://visualize-it.dev

Secondary / context:
- Embedded.fm interview (Ep. 378) — https://embedded.fm/episodes/378
- Rebecca Jackson, *Sketching the docs at Microsoft MVP Summit* — https://rebeccajlj.com/2021/04/10/sketching-the-docs-at-microsoft-mvp-summit/

Resources she recommends (third-party): Mike Rohde (Sketchnote Handbook/Workbook),
Sunni Brown (Doodle Revolution), Jenny Doh (Creative Lettering), Austin Kleon, Maggie
Appleton (illustrated.dev), Denise Yu, Sacha Chua, Helen Cann, The Noun Project, Google
Fonts (Monoton).

### Caveats / thin spots
- No public **fixed color palette / hex system** or **downloadable Procreate brush/template
  kit** of hers was found — only her *rules* (2–3 colors, background separation,
  accessibility). Her actual palette must be read off the images on cloud-skills.dev.
- She doesn't state a hard rule that **video sketchnotes must be live**; the staged
  capture-then-refactor approach is what generalizes to recordings.
- The motivational stats (65% visual learners, 90% recall) are claims she repeats, not
  her own research — use as framing, not evidence.
- To extract her exact **title-banner style and signature palette**, the next step is
  to visually inspect 5–10 images directly from cloud-skills.dev / @sketchthedocs (text
  scraping can't surface those).
