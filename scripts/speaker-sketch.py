#!/usr/bin/env python3
"""Phase B — per-speaker sketch portraits.

Pipeline (all Gemini, no ffmpeg needed when a thumbnail exists):
  1. Gemini vision reads the video THUMBNAIL → main speakers (name, role, face bounding box).
  2. PIL crops each headshot from the thumbnail.
  3. Gemini 2.5 Flash Image ("Nano Banana") redraws each crop as a hand-drawn sketch portrait —
     single-color pink line art on transparent background, so it reads on light OR dark canvas.
  4. Saves portraits to assets/speakers/ + a manifest, and merges `speakers` into context.json.

Usage:
  python3 speaker-sketch.py --context work/context.json [--thumb work/thumb.jpg]
      [--out-dir assets/speakers] [--model-vision gemini-2.5-flash]
      [--model-image gemini-2.5-flash-image] [--max 4] [--no-merge] [--quiet]

Requires GEMINI_API_KEY + `pip install google-genai Pillow`.
"""
import argparse, io, json, os, re, sys, urllib.request
from pathlib import Path

V_MODEL = os.environ.get("GEMINI_VISION_MODEL", "gemini-2.5-flash")
I_MODEL = os.environ.get("GEMINI_IMAGE_MODEL", "gemini-2.5-flash-image")

DETECT = """This is a YouTube thumbnail for a talk. Identify the MAIN SPEAKERS pictured — real people
shown as headshot photos, usually captioned with their name and title. For each, return their name,
a concise role/title (e.g. "Founder · CEO"), and the bounding box of their head/face photo.
Return ONLY JSON: {"speakers":[{"name":"","role":"","box_2d":[ymin,xmin,ymax,xmax]}]}
box_2d is normalized to 0-1000 as [ymin, xmin, ymax, xmax]. Exclude logos and non-people. """

SKETCH = """Redraw the person in this photo as a hand-drawn SKETCHNOTE portrait.
Show ONLY the head and shoulders — omit hands, cups, drinks, logos, jewellery, and any background
objects. Center the face with roughly square framing and a little margin.
Use loose, confident, single-weight contour lines in BLACK ink only, on a plain solid WHITE background.
No shading, no greyscale, no colour, no fills, no photographic texture, no checkerboard — just clean
hand-drawn black ink line art, the way a sketchnote artist dashes off a quick portrait. Keep the
likeness recognizable (hairstyle, glasses, facial hair, expression).
Do NOT draw any border, box, or frame around the portrait."""


def slug(s):
    return re.sub(r"[^a-z0-9]+", "-", (s or "speaker").lower()).strip("-") or "speaker"


def keyout_bg(im):
    """Make the white/checkerboard background transparent, keeping the black ink line art.
    Keys out near-white pixels; dark lines survive."""
    from PIL import Image
    im = im.convert("RGB")
    px = im.load()
    out = Image.new("RGBA", im.size)
    op = out.load()
    W, H = im.size
    for y in range(H):
        for x in range(W):
            r, g, b = px[x, y]
            if r > 185 and g > 185 and b > 185:    # near-white bg → transparent
                op[x, y] = (0, 0, 0, 0)
            else:                                  # keep dark line art (as near-black)
                op[x, y] = (min(r, 40), min(g, 40), min(b, 40), 255)
    bbox = out.getbbox()                           # trim transparent margins to the line art
    return out.crop(bbox) if bbox else out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--context", required=True)
    ap.add_argument("--thumb", default=None)
    ap.add_argument("--out-dir", default=None)
    ap.add_argument("--model-vision", default=V_MODEL)
    ap.add_argument("--model-image", default=I_MODEL)
    ap.add_argument("--max", type=int, default=4)
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
        sys.exit(f"missing dep ({e}) — `pip install google-genai Pillow`.")

    ctx_path = Path(a.context)
    ctx = json.loads(ctx_path.read_text())
    meta = ctx.get("meta", {})
    root = ctx_path.parent.parent if ctx_path.parent.name == "work" else Path.cwd()
    out_dir = Path(a.out_dir) if a.out_dir else root / "assets" / "speakers"
    out_dir.mkdir(parents=True, exist_ok=True)

    # --- thumbnail ---
    thumb_path = Path(a.thumb) if a.thumb else ctx_path.parent / "thumb.jpg"
    if not thumb_path.exists():
        url = meta.get("thumbnail")
        if not url:
            sys.exit("no thumbnail (pass --thumb or ensure context.meta.thumbnail).")
        if not a.quiet:
            print(f"• downloading thumbnail {url}", file=sys.stderr)
        urllib.request.urlretrieve(url, thumb_path)
    img = Image.open(thumb_path).convert("RGB")
    W, H = img.size

    client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

    # --- 1. detect speakers ---
    if not a.quiet:
        print(f"• {a.model_vision}: detecting speakers in thumbnail …", file=sys.stderr)
    det = client.models.generate_content(
        model=a.model_vision,
        contents=[types.Part.from_bytes(data=thumb_path.read_bytes(), mime_type="image/jpeg"),
                  types.Part(text=DETECT)],
        config=types.GenerateContentConfig(response_mime_type="application/json", temperature=0),
    )
    m = re.search(r"\{[\s\S]*\}", det.text or "")
    speakers = (json.loads(m.group(0)) if m else {}).get("speakers", [])[: a.max]
    if not speakers:
        sys.exit("no speakers detected in the thumbnail.")
    if not a.quiet:
        print(f"  found: {', '.join(s.get('name', '?') for s in speakers)}", file=sys.stderr)

    # --- 2 + 3. crop + stylize each ---
    manifest = []
    for s in speakers:
        name, role = s.get("name", "Speaker"), s.get("role", "")
        box = s.get("box_2d") or [0, 0, 1000, 1000]
        ymin, xmin, ymax, xmax = box
        # normalized 0-1000 → pixels, with ~12% padding
        x0, y0, x1, y1 = xmin / 1000 * W, ymin / 1000 * H, xmax / 1000 * W, ymax / 1000 * H
        pw, ph = (x1 - x0) * 0.12, (y1 - y0) * 0.12
        crop = img.crop((max(0, int(x0 - pw)), max(0, int(y0 - ph)),
                         min(W, int(x1 + pw)), min(H, int(y1 + ph))))
        buf = io.BytesIO(); crop.save(buf, format="PNG")

        if not a.quiet:
            print(f"• {a.model_image}: sketching {name} …", file=sys.stderr)
        res = client.models.generate_content(
            model=a.model_image,
            contents=[types.Part.from_bytes(data=buf.getvalue(), mime_type="image/png"),
                      types.Part(text=SKETCH)],
        )
        png = None
        for part in (res.candidates[0].content.parts if res.candidates else []):
            if getattr(part, "inline_data", None) and part.inline_data.data:
                png = part.inline_data.data
                break
        if not png:
            print(f"  ⚠ no image returned for {name}; skipping", file=sys.stderr)
            continue
        portrait = out_dir / f"{slug(name)}.png"
        keyout_bg(Image.open(io.BytesIO(png))).save(portrait)
        manifest.append({"name": name, "role": role, "portrait": str(portrait)})
        if not a.quiet:
            print(f"  ✓ {portrait}", file=sys.stderr)

    if not manifest:
        sys.exit("no portraits generated.")
    (ctx_path.parent / "speakers.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2))
    if not a.no_merge:
        ctx["speakers"] = manifest
        ctx_path.write_text(json.dumps(ctx, ensure_ascii=False, indent=2))
        print(f"✓ merged {len(manifest)} speakers into {ctx_path}")
    print("✓ portraits in " + str(out_dir))


if __name__ == "__main__":
    main()
