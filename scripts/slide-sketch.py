#!/usr/bin/env python3
"""Per-section slide sketches — pull the slide that matches each box and redraw it hand-drawn.

Pipeline:
  1. Gemini watches the video + reads the layout's section headers → for each section, the timestamp
     of the most representative SLIDE (diagram/chart/UI/title), or none for talking-head sections.
  2. yt-dlp downloads the video once (720p, cached); ffmpeg grabs the frame at each timestamp.
  3. Gemini 2.5 Flash Image redraws each frame as a simple hand-drawn line diagram.
  4. Background keyed to transparent and lines RECOLORED to the section's hue (so they read on the
     dark canvas), saved to assets/slides/, and `section.figure` is patched into the layout.

Sections with no good slide keep their lucide icon (graceful fallback).

Usage:
  python3 slide-sketch.py --context work/context.json --layout work/keynote.layout.json
      [--video work/video.mp4] [--cookies-from-browser safari]
      [--model-vision gemini-2.5-pro] [--model-image gemini-2.5-flash-image] [--quiet] [--no-merge]

Requires GEMINI_API_KEY, google-genai, Pillow, yt-dlp, ffmpeg. Public videos only.
"""
import argparse, glob, io, json, os, re, subprocess, sys
from pathlib import Path

V_MODEL = os.environ.get("GEMINI_VISION_MODEL", "gemini-2.5-pro")
I_MODEL = os.environ.get("GEMINI_IMAGE_MODEL", "gemini-2.5-flash-image")

SKETCH = """Redraw the key visual from this video frame as a SMALL, SIMPLE hand-drawn sketchnote spot
illustration — the kind of quick little drawing that sits next to a heading. Reduce it to a few clean
shapes and at most one or two very short labels. If the slide is busy, ABSTRACT it down to a single
simple icon-like sketch that captures the idea — do not reproduce a full flowchart or architecture
diagram. Loose, confident BLACK ink line art on a plain solid WHITE background. No colour, no fills,
no shading, no checkerboard, no border or frame, no speaker-camera inset."""


def run(cmd):
    return subprocess.run(cmd, capture_output=True, text=True)


def _loads(s):
    """json.loads, tolerating LLM quirks like trailing commas before } or ]."""
    try:
        return json.loads(s)
    except Exception:
        return json.loads(re.sub(r",(\s*[}\]])", r"\1", s))


def first_json(txt):
    """Parse the first balanced JSON object from a model response (tolerates trailing data + commas)."""
    txt = (txt or "").strip()
    try:
        return _loads(txt)
    except Exception:
        pass
    start = txt.find("{")
    if start < 0:
        raise ValueError("no JSON object in response")
    depth = 0
    for i in range(start, len(txt)):
        if txt[i] == "{":
            depth += 1
        elif txt[i] == "}":
            depth -= 1
            if depth == 0:
                return _loads(txt[start:i + 1])
    raise ValueError("unbalanced JSON in response")


def hex_rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def keyout_recolor(im, hexcolor):
    """White bg → transparent; keep line art and recolor it to the section hue."""
    from PIL import Image
    im = im.convert("RGB")
    px = im.load()
    out = Image.new("RGBA", im.size)
    op = out.load()
    cr, cg, cb = hex_rgb(hexcolor)
    W, H = im.size
    for y in range(H):
        for x in range(W):
            r, g, b = px[x, y]
            if r > 185 and g > 185 and b > 185:
                op[x, y] = (0, 0, 0, 0)
            else:
                op[x, y] = (cr, cg, cb, 255)
    bbox = out.getbbox()
    return out.crop(bbox) if bbox else out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--context", required=True)
    ap.add_argument("--layout", required=True)
    ap.add_argument("--out-dir", default=None)
    ap.add_argument("--design", default="design/default", help="design system dir (for section hues)")
    ap.add_argument("--video", default=None)
    ap.add_argument("--cookies-from-browser", default=None)
    ap.add_argument("--model-vision", default=V_MODEL)
    ap.add_argument("--model-image", default=I_MODEL)
    ap.add_argument("--no-merge", action="store_true")
    ap.add_argument("--quiet", action="store_true")
    a = ap.parse_args()

    if not os.environ.get("GEMINI_API_KEY"):
        sys.exit("GEMINI_API_KEY not set.")
    try:
        from google import genai
        from google.genai import types
        from PIL import Image
    except ImportError as e:
        sys.exit(f"missing dep ({e}) — pip install google-genai Pillow")

    ctx = json.loads(Path(a.context).read_text())
    url = ctx.get("meta", {}).get("url")
    layout_path = Path(a.layout)
    layout = json.loads(layout_path.read_text())
    sections = layout.get("sections", [])
    for s in sections:                 # clean slate — clear any figures from a previous run
        s.pop("figure", None)
    root = Path.cwd()
    try:
        design = json.loads((Path(a.design) / "design.json").read_text())
        HUES, CYCLE = design["hues"], list(design["hues"])
    except Exception:
        sys.exit(f"could not read design system at {a.design}/design.json (--design)")
    out_dir = Path(a.out_dir) if a.out_dir else root / "assets" / "slides"
    out_dir.mkdir(parents=True, exist_ok=True)
    workdir = Path(a.context).parent

    client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

    # 1. align sections → slide timestamps
    sec_list = "\n".join(f'{s.get("n", i + 1)}. {s.get("header", "")} — {"; ".join(s.get("bullets", []))}'
                         for i, s in enumerate(sections))
    prompt = f"""This video is a talk. Below are the sections of a one-page summary sketchnote made from it.
For EACH section, decide whether the video shows a SMALL, SIMPLE visual that would make a nice little
spot illustration beside that heading — e.g. a simple diagram with only a few elements, a single small
chart, a product logo/mark, or a clean conceptual graphic.
SET has_slide=false (skip) when the only visuals are: dense flowcharts, large/busy architecture
diagrams, multi-box system diagrams, text-heavy slides, or plain talking-head shots. Be SELECTIVE —
only pick a slide when it is genuinely simple and useful at thumbnail size. Quality over coverage; it's
fine if only a few sections qualify. Give the timestamp (seconds) of the simplest, most iconic frame.

Sections:
{sec_list}

Return ONLY JSON: {{"sections":[{{"n":<int>,"has_slide":<bool>,"simple":<bool>,"timestamp_seconds":<number>,"caption":"<the simple visual>"}}]}}"""
    if not a.quiet:
        print(f"• {a.model_vision}: aligning {len(sections)} sections to slides …", file=sys.stderr)
    det = client.models.generate_content(
        model=a.model_vision,
        contents=[types.Content(role="user", parts=[
            types.Part(file_data=types.FileData(file_uri=url)),
            types.Part(text=prompt)])],
        config=types.GenerateContentConfig(response_mime_type="application/json", temperature=0),
    )
    parsed = first_json(det.text)
    secs = parsed if isinstance(parsed, list) else parsed.get("sections", [])
    aligned = {s["n"]: s for s in secs if s.get("has_slide") and s.get("simple", True)}
    if not aligned:
        sys.exit("Gemini found no slide-bearing sections.")
    if not a.quiet:
        print(f"  slides for sections: {sorted(aligned)}", file=sys.stderr)

    # 2. ensure video downloaded
    video = a.video
    if not video:
        existing = glob.glob(str(workdir / "video.*"))
        if existing:
            video = existing[0]
        else:
            if not a.quiet:
                print("• yt-dlp: downloading 720p video (once) …", file=sys.stderr)
            cmd = ["yt-dlp", "-f", "bv*[height<=720]+ba/b[height<=720]",
                   "-o", str(workdir / "video.%(ext)s"), "--no-warnings"]
            if a.cookies_from_browser:
                cmd += ["--cookies-from-browser", a.cookies_from_browser]
            cmd.append(url)
            run(cmd)
            existing = glob.glob(str(workdir / "video.*"))
            if not existing:
                sys.exit("video download failed (try --cookies-from-browser).")
            video = existing[0]

    # 3 + 4. grab frame, redraw, recolor per section
    patched = 0
    for i, s in enumerate(sections):
        n = s.get("n", i + 1)
        info = aligned.get(n)
        if not info:
            continue
        ts = float(info.get("timestamp_seconds", 0))
        hue = HUES.get(s.get("hue") or CYCLE[i % len(CYCLE)], next(iter(HUES.values())))
        frame = workdir / f"slide_{n}.png"
        run(["ffmpeg", "-y", "-loglevel", "error", "-ss", str(ts), "-i", video, "-frames:v", "1", str(frame)])
        if not frame.exists():
            print(f"  ⚠ no frame for section {n}", file=sys.stderr)
            continue
        if not a.quiet:
            print(f"• {a.model_image}: sketching slide for §{n} '{s.get('header','')}' @ {int(ts)}s", file=sys.stderr)
        res = client.models.generate_content(
            model=a.model_image,
            contents=[types.Part.from_bytes(data=frame.read_bytes(), mime_type="image/png"),
                      types.Part(text=SKETCH)],
        )
        png = None
        for part in (res.candidates[0].content.parts if res.candidates else []):
            if getattr(part, "inline_data", None) and part.inline_data.data:
                png = part.inline_data.data
                break
        if not png:
            print(f"  ⚠ no sketch returned for §{n}", file=sys.stderr)
            continue
        portrait = out_dir / f"section-{n}.png"
        keyout_recolor(Image.open(io.BytesIO(png)), hue).save(portrait)
        s["figure"] = str(portrait)
        patched += 1
        if not a.quiet:
            print(f"  ✓ {portrait}", file=sys.stderr)

    if not patched:
        sys.exit("no slide sketches generated.")
    if not a.no_merge:
        layout_path.write_text(json.dumps(layout, ensure_ascii=False, indent=2))
        print(f"✓ patched {patched} sections with figures in {layout_path}")
    print("✓ slide sketches in " + str(out_dir))


if __name__ == "__main__":
    main()
