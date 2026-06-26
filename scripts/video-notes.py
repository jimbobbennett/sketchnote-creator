#!/usr/bin/env python3
"""Gemini video-notes extractor — the "eyes" of the pipeline.

Gemini natively watches the YouTube video (audio + visuals) and returns structured
notes that Claude (the author) uses alongside the transcript to build the sketchnote.
This captures what the transcript can't: slide/section structure, on-screen text,
diagrams/frameworks, on-screen numbers, and AUTHORITATIVE product-name spellings.

Usage:
  python3 video-notes.py --context work/context.json [--url <youtube>]
            [--out work/video_notes.json] [--no-merge] [--model gemini-2.5-pro] [--quiet]

By default it both writes video_notes.json AND merges the notes into context.json
under `video_notes`. Requires GEMINI_API_KEY + `pip install google-genai`. Public videos only.
"""
import argparse, json, os, re, sys
from pathlib import Path

DEFAULT_MODEL = os.environ.get("GEMINI_MODEL", "gemini-2.5-pro")

PROMPT = """You are watching a recorded talk to produce STRUCTURED NOTES that another author will
use to create a one-page sketchnote summary. Extract faithfully from the video — both the AUDIO and
the ON-SCREEN visuals. Read slides, titles, and UI text carefully: the on-screen spelling and casing
of any name is AUTHORITATIVE (spoken audio is often ambiguous for product names).

Return ONLY a JSON object with this exact shape:
{
  "onscreen_title": "<the talk's title as shown on screen, or '' if none>",
  "structure": [
    {
      "start": "<mm:ss>",
      "title": "<the slide / section / topic title>",
      "points": ["<concise key point made here>"],
      "onscreen_text": ["<notable labels, product names, or text visible on the slide>"]
    }
  ],
  "product_names": [
    { "name": "<exact correct spelling & casing as shown on screen>", "what": "<one-line: what it is>" }
  ],
  "diagrams": [
    { "start": "<mm:ss>", "name": "<diagram or framework name>", "describes": "<what it shows / its parts>" }
  ],
  "numbers": [
    { "value": "<e.g. 10,000>", "what": "<what it measures>", "start": "<mm:ss>" }
  ],
  "quotes": [
    { "text": "<short, memorable line, lightly cleaned>", "start": "<mm:ss>" }
  ]
}

Guidance:
- `structure`: be comprehensive — one entry per distinct slide / topic, in order. This is the talk's
  real outline and the most valuable output.
- `product_names`: list every product, feature, company, or tool name shown, with its on-screen spelling.
- `diagrams`: capture any framework/architecture/flow diagram and name its components.
- Keep everything grounded in what is actually shown or said. Do not invent."""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--context", required=True)
    ap.add_argument("--url", default=None)
    ap.add_argument("--out", default=None)
    ap.add_argument("--no-merge", action="store_true")
    ap.add_argument("--model", default=DEFAULT_MODEL)
    ap.add_argument("--quiet", action="store_true")
    a = ap.parse_args()

    if not os.environ.get("GEMINI_API_KEY"):
        sys.exit("GEMINI_API_KEY not set in environment.")
    try:
        from google import genai
        from google.genai import types
    except ImportError:
        sys.exit("google-genai not installed — `pip install google-genai`.")

    ctx_path = Path(a.context)
    ctx = json.loads(ctx_path.read_text())
    url = a.url or ctx.get("meta", {}).get("url")
    if not url:
        sys.exit("no YouTube URL (pass --url or ensure context.meta.url is set).")
    out_path = Path(a.out) if a.out else ctx_path.parent / "video_notes.json"

    if not a.quiet:
        print(f"• Gemini ({a.model}) extracting video notes from {url} …", file=sys.stderr)

    client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
    parts = [
        types.Part(file_data=types.FileData(file_uri=url)),
        types.Part(text=PROMPT),
    ]
    try:
        resp = client.models.generate_content(
            model=a.model,
            contents=[types.Content(role="user", parts=parts)],
            config=types.GenerateContentConfig(response_mime_type="application/json", temperature=0),
        )
    except Exception as e:
        sys.exit(f"Gemini request failed: {e}")

    raw = resp.text or ""
    mjson = re.search(r"\{[\s\S]*\}", raw)
    try:
        notes = json.loads(mjson.group(0) if mjson else raw)
    except Exception:
        sys.exit("could not parse Gemini output as JSON:\n" + raw[:1000])

    out_path.write_text(json.dumps(notes, ensure_ascii=False, indent=2))
    if not a.quiet:
        print(f"  structure: {len(notes.get('structure', []))} sections · "
              f"names: {len(notes.get('product_names', []))} · "
              f"diagrams: {len(notes.get('diagrams', []))} · "
              f"numbers: {len(notes.get('numbers', []))} · "
              f"quotes: {len(notes.get('quotes', []))}", file=sys.stderr)

    if not a.no_merge:
        ctx["video_notes"] = notes
        ctx_path.write_text(json.dumps(ctx, ensure_ascii=False, indent=2))
        print(f"✓ merged into {ctx_path} (context.video_notes)")
    print(f"✓ wrote {out_path}")


if __name__ == "__main__":
    main()
