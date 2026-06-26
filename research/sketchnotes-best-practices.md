# Sketchnotes: A Practical Reference for Auto-Generation

Reference material synthesized from the recognized authorities in visual note-taking — Mike Rohde (*The Sketchnote Handbook* / *Workbook*), Doug Neill (Verbal to Visual), Eva-Lotta Lamm, Sunni Brown (*The Doodle Revolution*), Sketchnote Army, and reputable practitioner-educators. Purpose: to inform a tool/skill that auto-generates sketchnotes from YouTube videos. Every section ends with **→ For the generator** notes that translate principle into implementable rules.

The single most important sentence in this whole document, repeated by every authority: **a sketchnote is about ideas, not art.** Optimize for idea fidelity, clarity of structure, and a point of view — never illustrative polish.

---

## 1. What a sketchnote IS, and its core purpose

**Definition (Mike Rohde, verbatim):** "Sketchnotes are rich visual notes created from a mix of handwriting, drawings, hand-lettering, shapes, and visual elements like arrows, boxes, and lines." ([rohdesign.com/sketchnotes](https://rohdesign.com/sketchnotes))

Rohde coined "sketchnoting" around 2006 as a personal technique for capturing conference talks; it grew into a broad practice for comprehension and retention.

**The core principle — "Ideas, Not Art":**
- The goal is to "capture ideas in an interesting way. There is no need to get hung up on drawing skills." Rohde avoids the word "art" because it "carries lots of baggage" — implying only fine art is valid. ([Spark Creativity](https://nowsparkcreativity.com/2018/08/046-sketchnotes-are-awesome-with-mike.html); [Creative Market](https://creativemarket.com/blog/how-to-sketchnote-an-interview-with-mike-rohde))
- "You don't need to be an artist. You don't need to draw well." ([rohdesign.com/sketchnotes](https://rohdesign.com/sketchnotes))
- "It's all about the ideas and... the structure of getting the concepts down, and if then on top of it you could make it look beautiful, well, that's a nice thing to have, but it's not a requirement." ([The Informed Life, ep. 90](https://theinformed.life/2022/06/19/episode-90-mike-rohde/))
- The test of a good sketchnote is whether it "effectively captures ideas" — not how it looks. ([Creative Market](https://creativemarket.com/blog/how-to-sketchnote-an-interview-with-mike-rohde))

**Why it works — dual coding theory.** The brain processes verbal and visual information through separate channels, so "capturing ideas in both words and pictures uses more of your brain, helping you better understand and remember those ideas." Retention rises from roughly 10% (text only) to about 65% (words + images combined). ([LearningMole](https://learningmole.com/sketchnoting-visual-note-taking-for-understanding/); [Shopify](https://www.shopify.com/partners/blog/sketchnoting-101-tips-for-improving-your-visual-vocabulary))

**Core purpose = constraint-forced synthesis.** Rohde's origin story: switching to a small Moleskine "forced [him] to become more deliberate about what [he] captured" — analyzing on the fly instead of deferring it. The limited space "forces you to listen, decide what matters, and capture only the big ideas." ([Creative Market](https://creativemarket.com/blog/how-to-sketchnote-an-interview-with-mike-rohde); [rohdesign.com/sketchnotes](https://rohdesign.com/sketchnotes))

**→ For the generator:** A finite canvas is a feature, not a limitation. Budget output to a fixed visual real estate so the synthesis layer is forced to select and compress rather than transcribe. Judge results on idea capture and legibility, not rendering quality.

---

## 2. Structural / layout patterns

The canonical taxonomy comes from Rohde: **seven patterns — linear, radial, vertical, path, modular, skyscraper, popcorn** ([rohdesign.com/handbook](https://rohdesign.com/handbook); [Derek Bruff review](https://derekbruff.org/2013/08/01/summer-reading-the-sketchnote-handbook-by-mike-rohde/)). Practitioners (Sketchy Ideas, Presto Sketching, Verbal to Visual) extend it with grid, columns, flowchart, storyboard/comic, central-image, metaphor-container, and pre-drawn "skeleton" templates.

**The governing principle (every source): the layout is a container that should echo the inherent structure of the content.** "The choice of overarching structure aligns perfectly with the content of the sketchnote itself." ([Verbal to Visual](https://verbaltovisual.com/visual-thinking-structures-outside-inspiration/))

| Pattern | Description | Suits | How to detect/decide |
|---|---|---|---|
| **Linear** | One continuous sequence, the way you read a page | Fixed step-by-step procedures, timelines, how-to | Strong ordinals + temporal connectives ("first… then… finally"), single unbranching thread, impersonal. **Safe default.** |
| **Radial / mind-map** | Central element with spokes radiating to subtopics | One core topic, several sub-ideas in no required order | One high-centrality entity recurs throughout; subtopics reference the hub but not each other |
| **Vertical / column** | (a) single top-to-bottom flow; (b) 2–3 parallel lanes | Comparisons, panel discussions, parallel topics on shared dimensions | 2–3 parallel entities described along the same attributes ("versus", "whereas", "on the other hand") → columns |
| **Path** | A winding visual route (U, zig-zag, spiral) the eye follows | Stories, journeys, "from X to Y", case studies, evolution over time | Like linear but narrative voice: first-person story + temporal arc. Good when you must commit before seeing the full arc |
| **Popcorn** | Scattered self-contained chunks, no enforced flow | No clear structure — Q&A, AMAs, topic-hopping interviews | No hub, no order, no count; disconnected independent points |
| **Modular / grid** | Page divided into boxed/gridded sections | Equal-weight categorized topics, especially a clean N (4 or 6) | Discrete equal chunks, countable. YouTube chapter markers of similar length are a strong signal |
| **Skyscraper** | Tall stacked vertical blocks (building floors) | Sequential/stacked content in portrait/tall format | Sequential or stacked hierarchy + portrait aspect ratio |
| **Skeleton (template)** | Structure drawn in advance, filled as content arrives | Known recurring formats, framework-driven talks ("5 pillars of…") | Title/series matches a fixed framework with a fixed N. **Most directly useful for a generator.** |

Variant overlays worth supporting: **central image / portrait** (one person/product is the whole subject); **metaphor container** (a dominant governing metaphor — iceberg, mountain, bridge, map — overlaid on a base layout); **flowchart** (conditional branching, "if… then"); **circular/cyclical** (loops, feedback); **storyboard/comic** (scene-based narrative).

### Decision rule (the key deliverable)

Classify the talk's dominant discourse structure first, then map to layout. Evaluate top-to-bottom, take the first match (ordered by specificity):

| If the talk's structure is… | Choose |
|---|---|
| A known recurring/templated format (fixed N named in title) | **Skeleton** |
| One central concept with unordered sub-ideas | **Radial** |
| A single dominant person/product subject | **Central image** |
| Governed by one strong metaphor | **Metaphor container** (overlay) |
| A comparison of parallel subjects on shared dimensions | **Columns** (or 2×2 **grid** if two axes) |
| A decision/branching process | **Flowchart** |
| A cycle/loop | **Circular** |
| A narrative/journey ("from X to Y") | **Path** (or **Storyboard** if scene-based) |
| A fixed step-by-step procedure/timeline | **Linear** (**Skyscraper** if portrait) |
| Independent equal chunks, countable (clean N) | **Modular / grid** |
| Independent chunks, no order/hub/count | **Popcorn** |
| Unknown / none of the above | **Linear** (safe default) |

**The two axes that separate most patterns:** (a) *Is there ordering/sequence?* (b) *Is there a single center?* — Center + ordered → path/linear; center + unordered → radial; no center + ordered → linear/columns; no center + unordered → popcorn/grid.

**Practical notes:** Grid vs. popcorn is decided purely by tidiness (countable equal chunks → grid). Path vs. linear is decided by narrative voice. Layouts combine — treat metaphor/central-image as overlays on a base. Failure is graceful: even a "wrong" layout just yields a more unique sketchnote. ([Sketchy Ideas](https://sketchyideas.co/sketchnote-layouts-the-ultimate-guide/); [Presto Sketching](https://prestosketching.com/blog/2021/01/14/a-guide-to-sketchnote-layouts/))

> Note: "Skeleton" is not one of Rohde's named seven (his seventh is **skyscraper**). It is the well-documented pre-drawn template practice, included here because it is the single most applicable pattern for an auto-generator.

---

## 3. Core visual vocabulary

### 3.0 The visual alphabet (build this primitive layer first)

Every authority agrees all icons decompose into a handful of primitives — treat this layer as atomic.

- **Rohde's 5 basic shapes:** square, circle, triangle, line, dot. "Icons are built from the five basic shapes." Canonical example: house = square (base) + triangle (roof) + rectangle (door). ([rohdesign.com/handbook](https://rohdesign.com/handbook))
- **Sunni Brown's 12-element visual alphabet** (most formal): six *flows* (point/dot, line, arc, angle, spiral, loop) + six *forms* (oval, eye, triangle, rectangle, house, cloud) — "the fundamental building blocks for drawing everything in the known universe." ([A List Apart](https://alistapart.com/article/the-miseducation-of-the-doodle/); [Bookey](https://www.bookey.app/book/the-doodle-revolution))
- **Doug Neill's icon "algorithms":** each icon = a repeatable draw-order recipe of primitives, improving "accuracy, consistency, and speed." ([Verbal to Visual](https://verbaltovisual.com/an-introduction-to-visual-note-taking/))

**→ For the generator:** Model the asset library as primitives → composed icons (each icon = an ordered list of primitive shapes + tags + a meaning string). This yields a consistent hand-drawn style and lets you synthesize novel icons.

### 3.1 Containers (group/enclose related content)

"Enclosing words in shapes brings structure and emphasis." ([Core77](https://www.core77.com/posts/19678/sketchnotes-101-the-basics-of-visual-note-taking-19678))

| Container | Conventional use |
|---|---|
| **Box / rectangle** | Hard fact, defined chunk, dates/times. Default neutral grouping |
| **Rounded box** | Softer grouping — a concept rather than a hard datum |
| **Cloud / thought bubble** | Soft/fuzzy idea, definition, future goal, internal thought |
| **Speech bubble** | A quote, something said aloud |
| **Banner / ribbon** | Titles and headings — the strongest title device |
| **Scroll** | Decorative title/quote variant (banner alternative) |
| **Burst / sound-effect container** | Exclamations, attention-grabbing callouts |

Consensus mapping: **banner = title, cloud = soft idea/definition, speech bubble = quote, box = hard fact.** ([Medium: Visual Thinking at Work](https://medium.com/visual-thinking-at-work/sketchnotes-a-guide-to-visual-note-taking-a0d8221604dc); [Wikipedia](https://en.wikipedia.org/wiki/Sketchnoting))

### 3.2 Connectors & arrows (relate chunks; show flow/sequence)

Containers *group*; connectors *relate*. They "guide the viewer through the sketchnote" and indicate relationships, cause-effect, and passage of time. ([Core77](https://www.core77.com/posts/19678/sketchnotes-101-the-basics-of-visual-note-taking-19678))

| Connector | Communicates |
|---|---|
| Straight arrow | Direct flow, A → B, next step |
| Curved arrow | Softer/indirect connection; routes around layout |
| Looping/circular arrow | Cycle, repetition, feedback loop |
| Dashed/dotted arrow | Weak, tentative, or implied connection |
| **Thick arrow** | A big trend / major movement |
| **Thin arrow** | An ordinary sequence / step |
| Plain line | Simple association, no direction |
| Double line | Stronger/structural connection |
| Bracket | Groups a set of items and labels them collectively |

Rule: "A thick arrow means a big trend; a thin arrow means a sequence." ([Sacha Chua](https://sachachua.com/blog/2013/08/sketchnote-lessons-arrows-and-connectors/))

### 3.3 Bullets & lists

Use a *consistent* shape per list; switch shape to signal a different category/level.
- **Shape bullets** (dot, circle, square, dash) — unordered items
- **Star bullets** — high-importance / key takeaways
- **Icon bullets** — small relevant pictogram for semantically typed lists
- **Numbered** — ordered/sequential steps (pair with connectors)
- **Checkboxes** — tasks, action items
([A List Apart](https://alistapart.com/article/the-miseducation-of-the-doodle/); [Noun Project](https://blog.thenounproject.com/an-introduction-to-sketchnoting-with-jen-giffen/))

### 3.4 Frames & dividers (segment the page)

- **Section dividers** — horizontal rules: plain, double, dotted, zig-zag, wavy, beaded, flourish
- **Frames/borders** — outer page frame or per-section frames; single (light) vs. double (stronger)
- **Layout frameworks** — 2×2 matrix, Venn, continuum/spectrum, timeline, grid, columns, radial (choose from content shape)

Caution (Lamm): frames and color "can make elements stand out, but the emphasis should be on key content rather than structural elements." ([Eva-Lotta Lamm](https://www.evalotta.net/blog/2013/3/25/entries-from-the-sketchnotes-challenge-part-3); [UX Mastery](https://uxmastery.com/sketchnoting-101-how-to-create-awesome-visual-notes/))

### 3.5 Icons / pictograms (the reusable library)

Icons are "recognizable, not realistic." Build a personal icon bank organized by domain, each stored as a repeatable draw-recipe. The **Noun Project** is the most-cited backing library for non-drawers. ([Core77](https://www.core77.com/posts/19678/sketchnotes-101-the-basics-of-visual-note-taking-19678); [Sketchy Ideas icon bank](https://sketchyideas.co/sketchnote-icon-bank/); [Noun Project](https://blog.thenounproject.com/an-introduction-to-sketchnoting-with-jen-giffen/))

Common icon → meaning table (assemble into a default lookup):

| Icon | Meaning | Icon | Meaning |
|---|---|---|---|
| Lightbulb | Idea, insight | Clock/hourglass | Time, deadline |
| Gear/cog | Process, mechanism | Tree/sprout | Growth |
| Brain | Thinking, cognition | Flame | Passion, energy |
| Heart | Love, "loved it" | Rocket | Launch, speed |
| Star | Importance, highlight | Trophy | Win, achievement |
| Arrow | Flow, direction | Handshake | Agreement, partnership |
| Wall/brick | Obstacle | $ / coin | Money |
| Lightning bolt | Problem | Question mark | Open question |
| Flag | Milestone | Checkmark in box | Decision, done |
| Target + arrow | Goal achieved | Fork in road | Choice |

([CHANGE JOURNAL](https://changejournal.com/en/blogs/sketchnote-symbole); [Shopify](https://www.shopify.com/partners/blog/sketchnoting-101-tips-for-improving-your-visual-vocabulary))

### 3.6 People figures (relatability, emotion, action)

- **Star people** — five-pointed-star body (head + four limbs); fastest full-body figure
- **Stick figures** — circle head + line limbs; pose = action
- **Faces** — circle + minimal features; **expression is driven entirely by eyebrow angle + mouth curve** (the highest-leverage emotion control: vary two parameters)

Rule: figures are for agents, emotions, and actions. Pose = action; face = emotion. Keep them generic/iconic. Rohde teaches drawing a person with a purpose or emotion "in under 10 seconds." ([rohdesign.com/handbook](https://rohdesign.com/handbook); [A List Apart](https://alistapart.com/article/the-miseducation-of-the-doodle/))

### 3.7 Emphasis techniques (visual hierarchy)

In rough order of strength:

| Technique | How / when |
|---|---|
| Size / scale | Biggest = title/key idea; scale to importance |
| Weight / bold | Block print, bold strokes, bubble/outlined letters, ALL CAPS |
| Color (accent) | Sparingly — 1 accent, 2 max; clarity over aesthetics |
| Underline / highlight | Single accent color to lift a concept off the page |
| Shading / hatching | Grey fills or hatching for depth |
| Drop shadow / 3D | Grey line to the right + bottom of a box = instant 3D pop |
| Callouts | Speech bubbles / decorated containers draw focus |
| Exploding star / burst | Spiky burst around a word = high-energy emphasis ("NEW!", key stat) |

Overarching layout principle: **C.R.A.P. — Contrast, Repetition, Alignment, Proximity.** Proximity groups related chunks; repetition keeps icon/bullet style consistent; contrast (size/weight/color) drives the emphasis hierarchy; alignment keeps the page readable. ([Core77](https://www.core77.com/posts/19678/sketchnotes-101-the-basics-of-visual-note-taking-19678))

---

## 4. Typography

### 4.1 Why hand-lettering matters

The point is **personality and authenticity over mechanical perfection**. Rohde: "The lettering shouldn't look perfect at all, but rather be something personal and unique" — the goal is to *avoid a computer-generated appearance*. ([Neuland](https://www.neuland.com/en/sketchnote-lettering/))

**→ For the generator:** Use hand-drawn / marker-style fonts (irregular, slightly imperfect, uniform marker-weight stroke), never a clean system font. The key encodable property is *deliberate imperfection*. Pair a hand-drawn display font with a hand-drawn body font to preserve authenticity while allowing hierarchy.

### 4.2 The 2–3 type styles rule + four-level hierarchy

Use **2–3 type styles total per sketchnote**, applied consistently — consistency makes notes "easier to process and skim afterwards." ([Type Thursday: Eva-Lotta Lamm](https://medium.com/type-thursday/an-opportunity-to-play-an-interview-with-sketchnoting-author-eva-lotta-lamm-a2cfa1ab453d))

| Level | Treatment |
|---|---|
| **Title** | Largest; bold/compressed display style; often ALL CAPS; embellished (banner/underline/shadow) |
| **Heading** | Large/medium; ALL CAPS or distinct style; light embellishment |
| **Body** | Normal size, plain hand-lettering, **mixed case** for readability |
| **Caption / side note** | Smallest, "discreet," possibly script/italic to read as secondary |

Lamm frames lettering itself as the encoder of importance: styling says "this is important... this is a side note... this is only a thought... this is a hard fact."

### 4.3 Techniques and legibility

- **ALL CAPS for short headers/keywords only** — never multi-line body runs (hurts readability)
- **Emphasis ramp** (escalating, Rohde): regular → italic/script → ALL CAPS → bold-compressed
- **Drive hierarchy primarily with size and weight**; case and style-switch are secondary
- **Headline embellishments** (underline, banner, drop shadow) only on Title/Heading levels
- **Legibility is the floor, hierarchy is the goal, decoration comes last** — experiment with decorative lettering only "when you know you're on top of the visual hierarchy" ([Type Thursday](https://medium.com/type-thursday/an-opportunity-to-play-an-interview-with-sketchnoting-author-eva-lotta-lamm-a2cfa1ab453d))
- Enforce a **baseline grid / cap-height per level** for consistent sizing
- **Blur/squint test:** clear dark/light zones and a standout focal element should survive blurring ([Sketch Academy Tip #9](https://sketchacademy.com/sketchnote-tip-9-contrast-is-your-friend/))

---

## 5. Color

### 5.1 Limited palette — and why

**Palette = black base + grey neutral + 1–2 accents (default to 1).** "A limited palette removes distraction and gives your sketch a built-in sense of harmony." Color is an enhancement, not the substance — "you don't have to use color right away." ([Urban Sketch Course](https://www.urbansketchcourse.com/blog/two-colours-one-sketch-limited-palette-tonal-values/); [Sacha Chua](https://sachachua.com/blog/2013/09/sketchnote-lesson-using-color/))

### 5.2 Color for FUNCTION, not decoration (most emphasized principle)

Every color must do a job:
- **Emphasis/hierarchy:** "Put the 'pop' only where you want the eye to land."
- **Categorization:** assign colors fixed meanings (e.g. one color for source material, another for your own connections). ([Verbal to Visual](https://verbaltovisual.com/sketchnote-a-book))
- **Consistency builds a personal "code":** reuse the same colors with the same logic every time. ([Sketch Academy Tip #5](https://sketchacademy.com/sketchnote-tip-5-color-like-a-pro/))

### 5.3 Specific recommendations

- **One dominant accent per sketchnote**, applied only to what should pop. Optionally derive it from the video's brand/topic.
- **"Lighter and brighter" accents only** — dark fills look "heavy, dark, muddy" and hurt readability.
- **Grey is reserved for shadows/shading**, not content.
- **Keep all linework black**, including outlines around light-filled shapes, so colored elements stay legible.

### 5.4 Shadows / shading for depth

- **Grey markers** for shadows; **drop shadows** on headers/boxes/icons (consistent single light direction)
- **Hatching / cross-hatching** — line density controls value (closer = darker)
- **Three-value model:** paper-white / mid-grey / deep shadow

### 5.5 Process order — color is always the final pass

1. **Black linework** (content, lettering, icons, frames) — the structural layer
2. **Grey shadows/shading** — establish depth consistently before color
3. **Accent color last** — applied only to functional highlights

([Neuland](https://www.neuland.com/en/sketchnote-lettering/); [Sketch Academy](https://sketchacademy.com/sketchnote-tip-5-color-like-a-pro/); [Ink Factory](https://inkfactorystudio.com/blog/color-markers-for-sketchnoting/); [Tonal Value Tool](https://tonalvaluetool.com/blog/shading-techniques-for-beginners-mastering-light-and-shadow))

---

## 6. Hierarchy of information — signal over noise

Three tiers, driven by typography scale and visual weight: **title → key ideas (headings) → supporting details.** ([rohdesign.com/sketchnotes](https://rohdesign.com/sketchnotes))

**The selection rule (compression):** Rohde's governing question — "What's the big idea? How do I compress it? How do I simplify it... so that when I look at it again, all those memories come back?" The filter metaphor: "tuning an antenna to certain ideas" — when an idea resonates, capture it; if not, let it go. ([The Informed Life](https://theinformed.life/2022/06/19/episode-90-mike-rohde/))

**Deciding what to leave out:** Sketchnotes are *not transcription* — "there is no way to capture every single word, and you don't want to." A sketchnote is a memory prompt: "you'll be amazed how much detail you remember with just a couple of words and a doodle." Capture "only as much detail as *you* need." ([Your Visual Journal](https://yourvisualjournal.com/how-to-sketchnote/); [Airship](https://airship.store/blogs/take-note/dimeo-post3))

**→ For the generator:**
- Three-tier extraction: exactly **one title** (the thesis), **a few key ideas/section headers**, **sparse supporting details** only where they make a key idea memorable.
- Encode hierarchy visually — largest/boldest lettering for the title, medium for key ideas, small for details. **Typography *is* the hierarchy.**
- Bias aggressively toward omission. The whole value is the discarded 90%. Use the space budget as a hard constraint that forces ranking. Items below threshold are **dropped, not shrunk.**

---

## 7. The process — making a sketchnote from a video

The recorded-video case has a decisive advantage over live sketchnoting: **you can do a structure pass before drawing.** This maps almost 1:1 to a multi-pass LLM pipeline.

1. **Listen first / "caching."** Listen before drawing; for video, rewind/replay freely and pause at ~3–5 min intervals to consolidate. Rohde holds ideas mentally, sensing where the speaker is going, before committing. ([Derek Bruff](https://derekbruff.org/2013/08/01/summer-reading-the-sketchnote-handbook-by-mike-rohde/); [Live Sketchnoting Pro Tips](https://medium.com/design-bootcamp/live-sketchnoting-pro-tips-for-designers-405965cd518c))
2. **Detect the speaker's structure → layout skeleton.** Verbal cues like "I'm going to tell you about three things" and numbered enumerations tell you how to allocate space. Recorded talks usually map to Linear/Vertical. ([Airship](https://airship.store/blogs/take-note/dimeo-post3))
3. **Identify the big ideas, not the details.** "Sketchnotes should represent the big ideas and include only as much detail as you need."
4. **Reframe at the end.** The synthesized idea often crystallizes late: "there is an opportunity to take the idea and reframe it... that might not come until the end, after you've taken in all the ideas." Don't generate linearly chunk-by-chunk — the late-arriving synthesis is core to the method. ([The Informed Life](https://theinformed.life/2022/06/19/episode-90-mike-rohde/))
5. **Prepare visual vocabulary up front.** For an unfamiliar topic, brainstorm likely terms and pre-map icons before processing — reduces "invent-on-the-fly" load. Pre-place fixed elements (title, speaker, handles). ([Airship](https://airship.store/blogs/take-note/dimeo-post3))
6. **Draft, then refine; foundation before polish.** "It's so important to get the foundation right. You can't go to the next level when the foundation isn't set." Lamm's documented workflow mapped **timestamps → speaker points → visual decisions** in a spreadsheet before producing the clean version. Color/emphasis added in the refinement pass, once priorities are known. ([The Informed Life](https://theinformed.life/2022/06/19/episode-90-mike-rohde/); [Eva-Lotta Lamm](https://www.evalotta.net/blog/2022/11/18/learn-to-sketchnote-behind-the-scenes-of-my-domestika-course))

### The recommended pipeline (maps the human discipline to an LLM architecture)
1. **Structure pass** — ingest transcript → extract outline (sections, enumerations, cues) → choose layout pattern (§2).
2. **Salience pass** — rank ideas into big-idea / sub-point / detail. This is both your hierarchy *and* your density filter.
3. **Vocabulary pass** — map concepts to your icon lexicon + harvest the speaker's own visual language (§8).
4. **Layout / allocation pass** — assign space proportional to importance and section count.
5. **Render pass** — draw with consistent style; **apply color/emphasis last**, to hierarchy roles only.

### Density guidance
- Treat density as a tunable parameter with a hard ceiling.
- Default for a ~30–45 min talk: one page, **~3–7 major idea clusters**, each with a heading + 1 icon + 2–4 terse sub-points.
- Two legitimate density modes: **standalone/shareable** = wordier, more explanatory (for non-attendees); **recap/aesthetic** = more visual, fewer words (brain fills gaps).
- Leave deliberate whitespace; reality-check density midway so you neither overflow nor run out.

---

## 8. What makes them fun and engaging

**Personality and a point of view are the differentiator.** Rohde: "sketchnoting... is something that you do for yourself, and you can put some of your personality and your opinion into the ideas that you're capturing." The "diaristic" quality — voice, emphasis, reactions — is what makes one delightful rather than boring. **A delightful sketchnote signals a point of view about which ideas matter; a boring one is a uniform, evenly-weighted transcript.** ([ImageThink](https://www.imagethink.net/sketchnoting-ask-the-expert-fireside-chat-with-mike-rhode/))

**Specific engagement levers** ([Your Visual Journal](https://yourvisualjournal.com/how-to-sketchnote/)):
- **Headlines that stand out** — larger letters, color, underlining
- **Consistent recurring style** — one figure approach, one accent palette, one heading treatment, repeated throughout. Consistency reads as polish; inconsistency reads as scattered
- **Borders and dividers** to section the page
- **Depth/dimension** — grey shadows
- **Whitespace / breathing room** — lets the brain process faster and leaves room for additions

**"Your style is fine."** Imperfect, personal style is a feature. Self-judgment "is a quick way to suck all the fun and whimsy out of sketchnoting."

### Visual metaphors (turning abstract ideas concrete)

- **Why it works:** analogical reasoning — understand an abstract concept by linking it to a concrete one (lightbulb = idea, lock = security).
- **Highest-signal technique — listen for the speaker's own visual language.** Sunni Brown: speech is full of latent visual metaphors ("rabbit hole," "spitball") — capture those *literally*. This is the most "human" metaphor source. ([Bookey: Doodle Revolution](https://www.bookey.app/book/the-doodle-revolution))
- **Generation technique:** place a common element in an unusual environment; key off color/shape/textural similarity between source and target. ([Fiveable](https://fiveable.me/visual-storytelling/unit-7/creating-visual-metaphors/study-guide/Luv5IuOCGRBuNHcN))
- **Standard vocabulary:** growth = plant/sprout; obstacle = wall; time = clock/hourglass; idea = lightbulb; problem = lightning bolt; choice = fork in road; connection = chain/link (full table in §3.5).

**→ For the generator:** Maintain a curated metaphor lexicon (concept → icon) for fast, consistent mapping. Add a pass that scans the transcript for already-visual language and draws it literally. Reserve novel blended metaphors for the few genuinely abstract big ideas — **don't iconify every noun.**

---

## 9. Common mistakes / anti-patterns

| Anti-pattern | Why it fails |
|---|---|
| **Transcribing / capturing everything** | Sketchnotes aren't transcription; you can't and shouldn't capture every word |
| **Too many colors (esp. body text)** | "Rookie mistake." Black ink for most words; reserve color for headings, borders, drawings, callouts |
| **Overcrowding / no whitespace** | Clutter hurts readability; whitespace separates ideas |
| **Perfectionism / self-judgment** | Kills the fun; it's about process and volume |
| **Inconsistent style** | Reads as scattered/unprofessional; consistency reads as quality |
| **No hierarchy** | Everything competes, nothing stands out |
| **Decoration over meaning** | Tone back connectors/structure to give room to actual content; structure serves meaning, not ornament |
| **Coloring before priorities are known** | Add color last, once takeaways are identified |
| **Unstructured popcorn placement** | Random arrangement can be "very difficult to follow" |

([Your Visual Journal](https://yourvisualjournal.com/how-to-sketchnote/); [Airship](https://airship.store/blogs/take-note/dimeo-post3); [Sketchnote Army](https://sketchnotearmy.com/blog/2014/6/4/verbal-to-visual-doug-neill.html))

**→ For the generator:** Enforce hard caps — limited palette (1–2 accents + black), a minimum whitespace ratio, a density ceiling per page. Build hierarchy *first* as data; let visual weight follow it. Apply color last, only to designated roles.

---

## 10. Programmatic generation — consolidated guidance

**Architecture: multi-pass, not linear chunk-by-chunk.**
1. **Structure pass** — read the *whole* transcript → thesis + outline + enumerations → pick layout via the §2 decision rule.
2. **Salience pass** — rank into title / key ideas / details; this is hierarchy *and* density filter; drop sub-threshold items.
3. **Vocabulary pass** — map concepts to icon lexicon + harvest speaker's own visual language.
4. **Layout/allocation pass** — space proportional to importance and section count; enforce whitespace + density ceiling.
5. **Render pass** — consistent style; black linework → grey shadows → accent color (last).

**Data model:**
- **Primitives** (atomic): Rohde's 5 shapes + Brown's 12 flows/forms — the shape grammar.
- **Icons:** each = ordered recipe of primitives + tags + meaning string → searchable, domain-tagged bank (Noun Project as fallback).
- **Containers / connectors / bullets / dividers / frameworks:** parameterized templates with the convention→semantics mappings as default selection heuristics (banner→title, cloud→soft idea, box→fact; thick arrow→trend, looping arrow→cycle).
- **People:** parametric face (2 params: brow + mouth) + star/stick body (pose param).
- **Emphasis:** a salience pass assigning size/weight/color/shadow/callout from importance score, capped at ≤2 colors.

**Hard rules to encode:**
- Layout from detected structure (§2 decision table).
- Exactly one title; 3–7 key-idea clusters; sparse details. Typography *is* the hierarchy (4 levels, 2–3 type styles, hand-drawn fonts).
- Palette: black + grey + 1 accent (2 max), accent only for functional pops; "lighter and brighter"; linework always black.
- Render order: linework → grey shadows → color last.
- Consistency everywhere (one figure style, one palette, one heading treatment) — this is what reads as quality.
- Bias to omission; the value is the discarded 90%. Drop, don't shrink.
- Ideas, not art.

---

## Sources

**Mike Rohde:** [What Are Sketchnotes](https://rohdesign.com/sketchnotes) · [The Sketchnote Handbook](https://rohdesign.com/handbook) · [The Informed Life ep.90](https://theinformed.life/2022/06/19/episode-90-mike-rohde/) · [Creative Market interview](https://creativemarket.com/blog/how-to-sketchnote-an-interview-with-mike-rohde) · [Derek Bruff Handbook review](https://derekbruff.org/2013/08/01/summer-reading-the-sketchnote-handbook-by-mike-rohde/) · [ImageThink fireside chat](https://www.imagethink.net/sketchnoting-ask-the-expert-fireside-chat-with-mike-rhode/) · [Neuland lettering](https://www.neuland.com/en/sketchnote-lettering/)

**Doug Neill / Verbal to Visual:** [Intro to visual note-taking](https://verbaltovisual.com/an-introduction-to-visual-note-taking/) · [Visual thinking structures](https://verbaltovisual.com/visual-thinking-structures-outside-inspiration/) · [How to sketchnote a book](https://verbaltovisual.com/sketchnote-a-book)

**Eva-Lotta Lamm:** [Type Thursday interview](https://medium.com/type-thursday/an-opportunity-to-play-an-interview-with-sketchnoting-author-eva-lotta-lamm-a2cfa1ab453d) · [Choreography of Sketching](https://medium.com/@evalottchen/the-choreography-of-sketching-b21f8ba644e) · [Behind the scenes / Domestika](https://www.evalotta.net/blog/2022/11/18/learn-to-sketchnote-behind-the-scenes-of-my-domestika-course) · [Sketchnotes Challenge feedback](https://www.evalotta.net/blog/2013/3/25/entries-from-the-sketchnotes-challenge-part-3)

**Sunni Brown:** [The Miseducation of the Doodle (A List Apart)](https://alistapart.com/article/the-miseducation-of-the-doodle/) · [Doodle Revolution summary](https://www.bookey.app/book/the-doodle-revolution)

**Layouts:** [Sketchy Ideas — Layouts guide](https://sketchyideas.co/sketchnote-layouts-the-ultimate-guide/) · [Presto Sketching — Layouts](https://prestosketching.com/blog/2021/01/14/a-guide-to-sketchnote-layouts/)

**Visual vocabulary / process / mistakes:** [Core77 — Sketchnotes 101](https://www.core77.com/posts/19678/sketchnotes-101-the-basics-of-visual-note-taking-19678) · [Medium — Visual Thinking at Work](https://medium.com/visual-thinking-at-work/sketchnotes-a-guide-to-visual-note-taking-a0d8221604dc) · [Sacha Chua — Arrows & connectors](https://sachachua.com/blog/2013/08/sketchnote-lessons-arrows-and-connectors/) · [Sacha Chua — Using color](https://sachachua.com/blog/2013/09/sketchnote-lesson-using-color/) · [UX Mastery](https://uxmastery.com/sketchnoting-101-how-to-create-awesome-visual-notes/) · [Noun Project — Jen Giffen](https://blog.thenounproject.com/an-introduction-to-sketchnoting-with-jen-giffen/) · [Sketchy Ideas — Icon bank](https://sketchyideas.co/sketchnote-icon-bank/) · [Shopify — Sketchnoting 101](https://www.shopify.com/partners/blog/sketchnoting-101-tips-for-improving-your-visual-vocabulary) · [Your Visual Journal](https://yourvisualjournal.com/how-to-sketchnote/) · [Airship — from recorded video](https://airship.store/blogs/take-note/dimeo-post3) · [Live Sketchnoting Pro Tips](https://medium.com/design-bootcamp/live-sketchnoting-pro-tips-for-designers-405965cd518c) · [Sketch Academy Tip #5](https://sketchacademy.com/sketchnote-tip-5-color-like-a-pro/) · [Sketch Academy Tip #9](https://sketchacademy.com/sketchnote-tip-9-contrast-is-your-friend/) · [Ink Factory — color markers](https://inkfactorystudio.com/blog/color-markers-for-sketchnoting/) · [CHANGE JOURNAL — symbols](https://changejournal.com/en/blogs/sketchnote-symbole) · [Wikipedia — Sketchnoting](https://en.wikipedia.org/wiki/Sketchnoting)

> **Source caveat:** the deepest step-by-step instruction (Rohde's *Handbook*/*Workbook* lettering & layout chapters, Brown's *Doodle Revolution*, Lamm's & Neill's courses) lives in paid books and gated courses. The free authoritative pages and detailed secondary summaries cited above corroborate every principle here and are mutually consistent; for definitive specifics the books remain the primary source. Two terminology corrections worth keeping: there is no "Five S's" framework — Rohde's canonical primitive set is the **five basic shapes**; and his seventh layout is **skyscraper**, not "skeleton" (skeleton = the documented pre-drawn template practice).
