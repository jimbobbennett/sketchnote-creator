#!/usr/bin/env python3
"""Independent video-grounded validation: check a rendered sketchnote against the
ACTUAL source video using Gemini (which natively watches YouTube video + audio).

Unlike the Codex validator (transcript + image), Gemini sees the real video — so it
reads on-screen slide text (authoritative spelling for product names like PXI / Signal),
diagrams, demos, and numbers the transcript never captures. It is given only the video
and the sketchnote image — no layout.json or reasoning — so it judges with no shared context.

Usage:
  python3 validate-video.py --image <sketchnote.png> --context <context.json>
            [--url <youtube_url>] [--out findings.json] [--model gemini-2.5-pro] [--quiet]

Requires: GEMINI_API_KEY in env, `pip install google-genai`. Video must be PUBLIC.
Exit code: 0 = pass, 3 = revise, 2 = tooling error.
"""
import argparse, json, os, re, sys
from pathlib import Path

DEFAULT_MODEL = os.environ.get("GEMINI_MODEL", "gemini-2.5-pro")

SCHEMA_DESC = """Return ONLY a JSON object with exactly this shape:
{
  "verdict": "pass" | "revise",
  "summary": "<one-paragraph overall judgement>",
  "issues": [
    {
      "severity": "high" | "medium" | "low",
      "type": "accuracy" | "hallucination" | "name-casing" | "missing" | "readability" | "other",
      "location": "<where on the sketchnote: title / cell N / a quote>",
      "problem": "<what is wrong, quoting the sketchnote text>",
      "evidence": "<what the VIDEO actually shows/says, incl. on-screen text + timestamp if known>",
      "suggested_fix": "<concrete correction>"
    }
  ],
  "missing_key_points": ["<important point shown/said in the video but absent from the sketchnote>"],
  "strengths": ["<what the sketchnote got right>"]
}
Set verdict to "revise" if there is any high- or medium-severity issue, otherwise "pass"."""


def build_prompt(title):
    return f"""You are independently fact-checking a SKETCHNOTE (a hand-drawn visual summary) of a
video talk. You have exactly two inputs and no other context: the source VIDEO (attached) and the
SKETCHNOTE image (attached). Judge the sketchnote SOLELY on whether it faithfully and accurately
represents the video. The video is titled: "{title}".

You can watch the real video — audio AND visuals. Use that fully:
- Read ON-SCREEN TEXT (slides, titles, UI, captions baked into frames). For any product / feature /
  company / person NAME on the sketchnote, the spelling SHOWN ON SCREEN in the video is authoritative.
  Flag any name on the sketchnote that disagrees with how it appears on screen, and give the correct
  form. (Spoken audio alone can be ambiguous for names; trust the slides.)
- Check visual claims, diagrams, demos, and any on-screen numbers — not just what is spoken.

Read the sketchnote image carefully (title, every numbered cell's header + bullets, any quotes, the
footer) and report:
1. accuracy   — is every statement on the sketchnote supported by the video? Flag unsupported,
                exaggerated, contradicted, or mis-attributed claims.
2. hallucination — claims, numbers, names, or features not present in the video at all.
3. name-casing — product/feature/company/people names spelled or cased incorrectly vs the video.
4. missing    — important points from the video the sketchnote omits (list in missing_key_points).
5. readability — any sketchnote text that is garbled, cut off, or incoherent as rendered.

Quote the sketchnote text you are flagging in each issue. {SCHEMA_DESC}"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--image", required=True)
    ap.add_argument("--context", required=True)
    ap.add_argument("--url", default=None, help="YouTube URL (defaults to context.meta.url)")
    ap.add_argument("--out", default=None)
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

    ctx = json.loads(Path(a.context).read_text())
    meta = ctx.get("meta", {})
    url = a.url or meta.get("url")
    if not url:
        sys.exit("no YouTube URL (pass --url or ensure context.meta.url is set).")
    out_path = Path(a.out) if a.out else Path(a.context).parent / "findings-video.json"
    png = Path(a.image).read_bytes()

    if not a.quiet:
        print(f"• Gemini ({a.model}) watching {url}\n  validating: {a.image}", file=sys.stderr)

    client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
    parts = [
        types.Part(file_data=types.FileData(file_uri=url)),          # the actual video
        types.Part.from_bytes(data=png, mime_type="image/png"),       # the sketchnote
        types.Part(text=build_prompt(meta.get("title", ""))),
    ]
    try:
        resp = client.models.generate_content(
            model=a.model,
            contents=[types.Content(role="user", parts=parts)],
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                temperature=0,
            ),
        )
    except Exception as e:
        sys.exit(f"Gemini request failed: {e}")

    raw = resp.text or ""
    mjson = re.search(r"\{[\s\S]*\}", raw)
    try:
        findings = json.loads(mjson.group(0) if mjson else raw)
    except Exception:
        sys.exit("could not parse Gemini output as JSON:\n" + raw[:1000])

    out_path.write_text(json.dumps(findings, ensure_ascii=False, indent=2))

    # ---- report ----
    sev = {"high": "🔴", "medium": "🟠", "low": "🟡"}
    issues = findings.get("issues", [])
    print("\n──────────── VIDEO VALIDATION (Gemini) ────────────")
    print(f"verdict: {str(findings.get('verdict','?')).upper()}   ({len(issues)} issue{'' if len(issues)==1 else 's'})")
    print(findings.get("summary", ""))
    for i in issues:
        print(f"\n{sev.get(i.get('severity'),'•')} [{i.get('severity')}/{i.get('type')}] {i.get('location')}")
        print(f"   problem : {i.get('problem')}")
        print(f"   evidence: {i.get('evidence')}")
        print(f"   fix     : {i.get('suggested_fix')}")
    if findings.get("missing_key_points"):
        print("\nmissing key points:")
        for k in findings["missing_key_points"]:
            print("   - " + k)
    print(f"\n✓ findings written to {out_path}")
    print("───────────────────────────────────────────────────")
    sys.exit(0 if findings.get("verdict") == "pass" else 3)


if __name__ == "__main__":
    main()
