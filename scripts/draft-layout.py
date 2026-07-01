#!/usr/bin/env python3
"""Scaffold a draft layout.json from context.video_notes (Gemini's structured read of the talk).

This is a batch helper — for one-off, high-polish sketchnotes the skill has Claude author the layout
by hand. For many talks at once, this produces a solid, consistent draft you can spot-fix:
condenses the talk to <=12 sections, cycles hues, maps a relevant lucide icon per section, and
attaches a few real quotes. Speaker portraits + slide figures are added by the other scripts.

Usage: python3 draft-layout.py --context work/<id>/context.json --out work/<id>/layout.json
       [--event "My Conf 2026"] [--brand "Acme"]

--event names the conference/series so it can be stripped from the video title and used in the
subtitle; --brand sets the footer name. Both are optional and default to empty (brand-agnostic).
"""
import argparse, json, re, sys
from pathlib import Path

HUES = ["teal", "indigo", "purple", "magenta"]
MOTIFS = ["bot", "cloud", "git-branch", "workflow", "radar", "network", "shield", "database", "eye", "activity"]
SKIP_TITLES = ("welcome", "introduction", "intro", "sponsor", "thank", "agenda", "roadmap", "outline", "wrap", "closing", "q&a", "questions")

# keyword -> lucide icon (first match wins); all verified to exist in lucide-static
ICON_RULES = [
    (r"fail|error|risk|challenge|problem|break|hallucinat", "triangle-alert"),
    (r"secur|identit|permission|auth|govern|complian|responsib|trust", "shield"),
    (r"trace|telemetr|observ|monitor", "git-branch"),
    (r"eval|judge|test|experiment|rubric|grade|score", "scale"),
    (r"spec|requirement|plan|checklist", "list-checks"),
    (r"feedback|signal|discover|detect", "radar"),
    (r"cost|budget|token|pricing|econom", "dollar-sign"),
    (r"cloud|fleet|infra|kubernetes|sandbox|deploy|scal|infrastructure", "cloud"),
    (r"orchestrat|workflow|pipeline|loop|process", "workflow"),
    (r"open.?source|oss|donat|fork|community", "git-fork"),
    (r"data scien|dataset|data layer|analytics", "database"),
    (r"memory|reason|learn|brain|intelligen", "brain"),
    (r"voice|audio|speech", "mic"),
    (r"vision|future|next|bet|invest|wave|vc|venture", "sparkles"),
    (r"reinforcement|rl|train|compute|ray", "cpu"),
    (r"build|ship|product|deploy|optimi", "rocket"),
    (r"agent|worker|fleet|crew|multi", "bot"),
    (r"identity|people|team|everyone|user", "users"),
]


def pick_icon(title, points):
    for src in (title, " ".join(points)):      # prefer the section title, then the points
        t = src.lower()
        for pat, icon in ICON_RULES:
            if re.search(pat, t):
                return icon
    return "sparkles"


def drop_danglers(s):
    while s.split() and s.split()[-1].lower() in ("with", "and", "for", "the", "to", "a", "of", "in", "on", "using", "an", "that", "as", "is", "are"):
        s = s.rsplit(" ", 1)[0].rstrip(" ,;:—-")
    return s


def clean_bullet(p):
    p = re.sub(r"\s+", " ", (p or "").strip()).rstrip(".")
    # "Label: explanation" → keep the crisp label when it's short
    if ":" in p:
        lead = p.split(":")[0].strip()
        if 6 <= len(lead) <= 46:
            return lead
    p = re.split(r"(?<=[.!?]) ", p)[0]          # first sentence
    if len(p) > 56:
        cut = p[:56]
        p = drop_danglers(cut[:cut.rfind(" ")].rstrip(" ,;:—-"))
    return p


def trim(s, n):
    s = (s or "").strip()
    if len(s) <= n:
        return s
    cut = s[:n]
    sp = cut.rfind(" ")
    return (cut[:sp] if sp > n * 0.6 else cut).rstrip(" ,;:—-") + ""


def short_title(full):
    # titles are often "Talk | Company | Event"; keep only the leading talk title
    head = full.split("|")[0].strip()
    for sep in ("—", "–", ":"):              # cut at the first em-dash / en-dash / colon break
        if sep in head:
            head = head.split(sep)[0].strip()
    if len(head) > 58:                        # trim to a word boundary, then drop dangling connectors
        cut = head[:58]
        head = cut[:cut.rfind(" ")].rstrip(" ,;:—-")
    while head.split() and head.split()[-1].lower() in ("with", "and", "for", "the", "to", "a", "of", "in", "on", "using"):
        head = head.rsplit(" ", 1)[0].rstrip(" ,;:—-")
    return head


def company(full, event=""):
    parts = [p.strip() for p in full.split("|")]
    # parts like [title, company, event]; the company is the middle one. Drop the event part
    # (matches --event, if given) so it isn't mistaken for the company.
    ev = event.lower().strip()
    mids = [p for p in parts[1:] if p and not (ev and (ev in p.lower() or p.lower() in ev))]
    return mids[0] if mids else ""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--context", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--max", type=int, default=12)
    ap.add_argument("--event", default="", help="conference/series name (subtitle + stripped from title)")
    ap.add_argument("--brand", default="", help="footer name (e.g. the channel/org)")
    a = ap.parse_args()

    ctx = json.loads(Path(a.context).read_text())
    meta = ctx.get("meta", {})
    vn = ctx.get("video_notes")
    if not vn:
        sys.exit(f"{a.context} has no video_notes (run video-notes.py first)")

    struct = vn.get("structure", [])
    # drop low-value sections (welcome/sponsors/etc), then cap to --max
    kept = [s for s in struct if not any(k in (s.get("title", "").lower()) for k in SKIP_TITLES)]
    if not kept:
        kept = struct
    kept = kept[: a.max]

    quotes = [q.get("text", "").strip() for q in vn.get("quotes", []) if q.get("text")]
    # place up to 3 quotes on evenly-spaced sections
    qslots = {}
    if quotes and kept:
        picks = quotes[:3]
        idxs = [0, len(kept) // 2, len(kept) - 1][: len(picks)]
        for i, q in zip(sorted(set(idxs)), picks):
            qslots[i] = trim(q, 88)

    sections = []
    for i, s in enumerate(kept):
        points = [p for p in (s.get("points") or []) if p.strip()]
        pts = [clean_bullet(p) for p in points[:3]]
        pts = [b for b in pts if b] or [trim(s.get("title", ""), 56)]
        sections.append({
            "n": i + 1,
            "header": drop_danglers(trim(s.get("title", f"Part {i+1}"), 40)),
            "hue": HUES[i % len(HUES)],
            "icon": pick_icon(s.get("title", ""), points),
            "bullets": pts,
            "quote": qslots.get(i),
        })

    co = company(meta.get("title", ""), a.event)
    subtitle = " · ".join(x for x in (co, a.event) if x)
    layout = {
        "title": short_title(meta.get("title", "Talk")),
        "subtitle": subtitle,
        "source": {"url": meta.get("url"), "channel": meta.get("channel"), "duration": meta.get("duration_string")},
        "layout": "grid",
        "canvas": {"theme": "dark", "aspect": "16:9", "cols": 4 if len(sections) > 6 else 3},
        "sections": sections,
        "footer": {"left": "", "center": "", "right": a.brand},
        "decor": {"density": "light", "seed": 7, "motifs": MOTIFS},
    }
    Path(a.out).write_text(json.dumps(layout, ensure_ascii=False, indent=2))
    print(f"✓ {a.out} — {len(sections)} sections, title “{layout['title']}”")


if __name__ == "__main__":
    main()
