#!/usr/bin/env python3
"""Extract a YouTube video into context.json for the sketchnote skill.

Pipeline (fail-soft cascade):
  1. metadata + chapters  -> yt-dlp --dump-single-json (only yt-dlp exposes chapters)
  2. transcript           -> youtube-transcript-api  ->  yt-dlp srv1 captions  ->  whisper.cpp
  3. visuals (opt-in)     -> yt-dlp 720p + ffmpeg scene keyframes + tesseract OCR

Usage:
  python3 extract.py <url|id> [--out context.json] [--lang en]
                     [--with-frames] [--cookies-from-browser safari]
                     [--whisper-model /path/ggml-large-v3.bin]
"""
import argparse, glob, html, json, os, re, subprocess, sys, tempfile
import xml.etree.ElementTree as ET
from pathlib import Path


def run(cmd, **kw):
    return subprocess.run(cmd, capture_output=True, text=True, **kw)


def vid_id(url_or_id):
    m = re.search(r"(?:v=|youtu\.be/|/shorts/|/embed/)([A-Za-z0-9_-]{11})", url_or_id)
    if m:
        return m.group(1)
    return url_or_id if re.fullmatch(r"[A-Za-z0-9_-]{11}", url_or_id) else None


# ---------- 1. metadata ----------
def get_metadata(url, cookies):
    cmd = ["yt-dlp", "--skip-download", "--dump-single-json", "--no-warnings"]
    if cookies:
        cmd += ["--cookies-from-browser", cookies]
    cmd.append(url)
    p = run(cmd)
    if p.returncode != 0:
        sys.exit("metadata failed (try --cookies-from-browser, or `yt-dlp -U`):\n" + p.stderr[-600:])
    j = json.loads(p.stdout)
    chapters = [
        {"start": c.get("start_time"), "end": c.get("end_time"), "title": c.get("title")}
        for c in (j.get("chapters") or [])
    ]
    meta = {
        "id": j.get("id"),
        "url": j.get("webpage_url") or url,
        "title": j.get("title"),
        "channel": j.get("channel") or j.get("uploader"),
        "description": (j.get("description") or "")[:4000],
        "duration": j.get("duration"),
        "duration_string": j.get("duration_string"),
        "upload_date": j.get("upload_date"),
        "thumbnail": j.get("thumbnail"),
        "tags": (j.get("tags") or [])[:25],
    }
    return meta, chapters


# ---------- 2. transcript ----------
def transcript_via_api(vid, langs):
    try:
        from youtube_transcript_api import YouTubeTranscriptApi
    except ImportError:
        return None
    try:
        ytt = YouTubeTranscriptApi()
        fetched = ytt.fetch(vid, languages=langs)  # 1.x instance API
        return [{"start": round(s.start, 2), "dur": round(s.duration, 2), "text": s.text.strip()}
                for s in fetched if s.text.strip()]
    except Exception as e1:
        try:  # legacy static API
            from youtube_transcript_api import YouTubeTranscriptApi as Y
            data = Y.get_transcript(vid, languages=langs)
            return [{"start": round(d["start"], 2), "dur": round(d["duration"], 2), "text": d["text"].strip()}
                    for d in data if d["text"].strip()]
        except Exception as e2:
            print(f"  transcript-api unavailable: {e1}", file=sys.stderr)
            return None


def transcript_via_ytdlp(url, langs, cookies, workdir):
    """srv1 captions = clean, de-duplicated phrase lines (no rolling-duplicate problem)."""
    base = os.path.join(workdir, "subs")
    want = ",".join(langs + [f"{l}-orig" for l in langs])
    cmd = ["yt-dlp", "--skip-download", "--write-auto-subs", "--write-subs",
           "--sub-langs", want, "--sub-format", "srv1",
           "-o", base + ".%(ext)s", "--no-warnings"]
    if cookies:
        cmd += ["--cookies-from-browser", cookies]
    cmd.append(url)
    run(cmd)
    files = glob.glob(base + "*")
    if not files:
        return None
    # prefer a manual/non "-orig" track if present
    files.sort(key=lambda f: ("orig" in f, f))
    try:
        root = ET.fromstring(Path(files[0]).read_text(encoding="utf-8"))
    except ET.ParseError:
        return None
    segs = []
    for t in root.findall("text"):
        txt = html.unescape((t.text or "")).replace("\n", " ").strip()
        if not txt:
            continue
        segs.append({"start": round(float(t.get("start", 0)), 2),
                     "dur": round(float(t.get("dur", 0)), 2), "text": txt})
    return segs or None


def transcript_via_whisper(url, cookies, workdir, model):
    if not model or not os.path.exists(model):
        print("  whisper skipped: no --whisper-model file provided", file=sys.stderr)
        return None
    cmd = ["yt-dlp", "-x", "--audio-format", "wav", "--postprocessor-args", "-ar 16000 -ac 1",
           "-o", os.path.join(workdir, "audio.%(ext)s"), "--no-warnings"]
    if cookies:
        cmd += ["--cookies-from-browser", cookies]
    cmd.append(url)
    run(cmd)
    audio = os.path.join(workdir, "audio.wav")
    if not os.path.exists(audio):
        return None
    out = os.path.join(workdir, "whisper")
    run(["whisper-cli", "-m", model, "-f", audio, "-oj", "-of", out])
    jf = out + ".json"
    if not os.path.exists(jf):
        return None
    data = json.load(open(jf))
    segs = []
    for t in data.get("transcription", []):
        off = t.get("offsets", {})
        txt = (t.get("text") or "").strip()
        if txt:
            segs.append({"start": round(off.get("from", 0) / 1000.0, 2),
                         "dur": round((off.get("to", 0) - off.get("from", 0)) / 1000.0, 2),
                         "text": txt})
    return segs or None


# ---------- 3. visuals (opt-in) ----------
def extract_frames_ocr(url, cookies, workdir):
    try:
        import pytesseract
        from PIL import Image
    except ImportError:
        print("  --with-frames needs `pip install pytesseract Pillow`; skipping", file=sys.stderr)
        return []
    vcmd = ["yt-dlp", "-f", "bv*[height<=720]+ba/b[height<=720]",
            "-o", os.path.join(workdir, "video.%(ext)s"), "--no-warnings"]
    if cookies:
        vcmd += ["--cookies-from-browser", cookies]
    vcmd.append(url)
    run(vcmd)
    vids = glob.glob(os.path.join(workdir, "video.*"))
    if not vids:
        return []
    fdir = os.path.join(workdir, "frames")
    os.makedirs(fdir, exist_ok=True)
    run(["ffmpeg", "-i", vids[0], "-vf", "select='gt(scene,0.4)',showinfo",
         "-vsync", "vfr", "-frame_pts", "true", os.path.join(fdir, "f_%05d.png")])
    onscreen = []
    for fp in sorted(glob.glob(os.path.join(fdir, "*.png"))):
        try:
            txt = pytesseract.image_to_string(Image.open(fp))
        except Exception:
            continue
        if len(txt.split()) > 15:  # text-heavy => likely a slide/diagram
            onscreen.append({"frame": os.path.basename(fp), "text": re.sub(r"\s+\n", "\n", txt).strip()})
    return onscreen


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("url")
    ap.add_argument("--out", default="context.json")
    ap.add_argument("--lang", default="en")
    ap.add_argument("--with-frames", action="store_true")
    ap.add_argument("--cookies-from-browser", default=None)
    ap.add_argument("--whisper-model", default=os.environ.get("WHISPER_MODEL"))
    ap.add_argument("--keep-workdir", action="store_true")
    a = ap.parse_args()

    vid = vid_id(a.url)
    url = a.url if a.url.startswith("http") else f"https://www.youtube.com/watch?v={vid}"
    langs = [a.lang]
    cookies = a.cookies_from_browser

    print(f"• metadata for {vid} …")
    meta, chapters = get_metadata(url, cookies)
    print(f"  “{meta['title']}” — {meta['channel']} — {meta.get('duration_string')} — chapters: {len(chapters)}")

    workdir = tempfile.mkdtemp(prefix="sketchnote-")
    print("• transcript …")
    transcript, src = None, None
    for fn, label in [
        (lambda: transcript_via_api(vid, langs), "youtube-transcript-api"),
        (lambda: transcript_via_ytdlp(url, langs, cookies, workdir), "yt-dlp/srv1"),
        (lambda: transcript_via_whisper(url, cookies, workdir, a.whisper_model), "whisper"),
    ]:
        transcript = fn()
        if transcript:
            src = label
            break
    if not transcript:
        sys.exit("  could not obtain a transcript (no captions; pass --whisper-model for ASR)")
    words = sum(len(s["text"].split()) for s in transcript)
    print(f"  {len(transcript)} segments, ~{words} words, via {src}")

    onscreen = []
    if a.with_frames:
        print("• frames + OCR …")
        onscreen = extract_frames_ocr(url, cookies, workdir)
        print(f"  kept {len(onscreen)} text-heavy frames")

    context = {
        "meta": meta,
        "chapters": chapters,
        "transcript": transcript,
        "transcript_source": src,
        "onscreen": onscreen,
    }
    Path(a.out).parent.mkdir(parents=True, exist_ok=True)
    Path(a.out).write_text(json.dumps(context, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"✓ wrote {a.out}")
    if not a.keep_workdir:
        import shutil
        shutil.rmtree(workdir, ignore_errors=True)
    else:
        print(f"  workdir: {workdir}")


if __name__ == "__main__":
    main()
