# YouTube Video Content Extraction — Technical Reference for the Sketchnote Skill

Reference material for a macOS (darwin/zsh/Python) skill that turns a YouTube video into a sketchnote. Current as of mid-2026. All commands assume Homebrew and Python 3 are available.

> **Local environment note (verified 2026-06-26):** `yt-dlp`, `ffmpeg`, `tesseract`,
> `whisper-cli` (whisper.cpp), and `python3` are all already installed on this machine.

---

## 0. One-time setup

```bash
# Core tools
brew install yt-dlp ffmpeg tesseract
brew install tesseract-lang        # extra OCR language packs (optional)

# Python libs
pip install -U yt-dlp youtube-transcript-api pytesseract Pillow
# Whisper fallback (see §1.3) — pick one:
brew install whisper-cpp           # recommended on Apple Silicon
# or: pip install faster-whisper
# or: pip install -U openai-whisper
```

Note: on Apple Silicon, Homebrew binaries live in `/opt/homebrew/bin`. If `pytesseract` can't find the engine, set `pytesseract.pytesseract.tesseract_cmd = "/opt/homebrew/bin/tesseract"`. Keep `yt-dlp` bleeding-edge (`yt-dlp -U` or `pip install -U yt-dlp`) — it breaks frequently against YouTube changes (see §5).

---

## 1. Getting the transcript / captions

This is the single most important input. Try the cheap path first (existing captions), fall back to ASR only when needed.

### 1.1 `youtube-transcript-api` (Python) — primary path

Install: `pip install youtube-transcript-api`

Important: the library went through a **1.x API rewrite**. The old static `YouTubeTranscriptApi.get_transcript(video_id)` is gone. Current usage is instance-based with `.fetch()` / `.list()`:

```python
from youtube_transcript_api import YouTubeTranscriptApi

ytt = YouTubeTranscriptApi()

# Fetch with language preference (priority list)
fetched = ytt.fetch("VIDEO_ID", languages=["en", "en-US"])

for snip in fetched:
    print(snip.start, snip.duration, snip.text)   # timestamped snippets

raw = fetched.to_raw_data()   # list[{"text","start","duration"}] — JSON-friendly
```

Timestamps come built in (`start`, `duration` in seconds) — exactly what you want to map transcript segments to chapters/keyframes.

Listing and choosing manual vs auto-generated captions:

```python
tlist = ytt.list("VIDEO_ID")
t = tlist.find_manually_created_transcript(["en"])   # prefer human captions
# or .find_generated_transcript(["en"]) for auto-captions
# or .find_transcript(["de","en"]) for either, by priority

# Translate (server-side) if only another language exists
en = t.translate("en").fetch()
```

CLI form (handy for quick scripting):

```bash
youtube_transcript_api VIDEO_ID --languages en --format json > transcript.json
youtube_transcript_api --list-transcripts VIDEO_ID
```

Formatters are built in: `JSONFormatter`, `TextFormatter`, `SRTFormatter`, `WebVTTFormatter`.

**Limitations / gotchas:**
- Uses **undocumented YouTube endpoints** — can break when YouTube changes things.
- **IP blocking**: cloud/datacenter IPs (AWS, GCP, CI) get blocked aggressively. On a local Mac you're usually fine; from a server you'll need residential proxies. The lib has first-class proxy support (`WebshareProxyConfig`, `GenericProxyConfig`).
- **No captions → it raises** (`NoTranscriptFound` / `TranscriptsDisabled`). That's your signal to fall back to Whisper.
- **Age-restricted videos**: need auth; cookie auth in this lib is currently fragile. For those, prefer yt-dlp with browser cookies.
- Pass the **video ID, not the URL**.

Source: https://github.com/jdepoix/youtube-transcript-api

### 1.2 `yt-dlp` for subtitles — robust alternative

yt-dlp is more resilient than the transcript API and shares the same cookie/proxy escape hatches you'll already use for audio/video. Use it to grab subtitles without downloading the video:

```bash
# What's available?
yt-dlp --list-subs "URL"

# Manual subs only, English, as SRT, no video download
yt-dlp --write-subs --sub-langs en --sub-format srt --skip-download "URL"

# Auto-generated captions (most videos have these even without manual subs)
yt-dlp --write-auto-subs --sub-langs en --sub-format vtt --skip-download "URL"

# Both manual + auto in one go
yt-dlp --write-subs --write-auto-subs --sub-langs "en.*" --skip-download "URL"
```

`vtt` and `srt` both carry timestamps. SRT is the easiest to parse into `(start, end, text)` tuples; VTT is the native YouTube format. Convert with `--convert-subs srt`.

Source: https://github.com/yt-dlp/yt-dlp

### 1.3 Fallback: no captions → download audio + Whisper ASR

When neither manual nor auto captions exist, transcribe locally.

Step 1 — pull audio only:

```bash
yt-dlp -x --audio-format mp3 -o "audio.%(ext)s" "URL"
# For Whisper, 16kHz mono wav is ideal:
yt-dlp -x --audio-format wav --postprocessor-args "-ar 16000 -ac 1" -o "audio.%(ext)s" "URL"
```

Step 2 — transcribe. **All three runtimes use the same OpenAI Whisper weights, so accuracy is identical for a given model size (e.g. `large-v3`). You're choosing a runtime, not a model.**

| Runtime | Install | Best for | Notes |
|---|---|---|---|
| **whisper.cpp** | `brew install whisper-cpp` | **Recommended on macOS / Apple Silicon** | Metal + Core ML acceleration, no Python dep, lowest memory. ~10× real-time for large-v3 on recent M-series. |
| **faster-whisper** | `pip install faster-whisper` | NVIDIA GPUs | CTranslate2 + int8; ~4× throughput, ~40% less VRAM. **CPU/CUDA only — no Metal on Mac**, so slower on Apple Silicon than whisper.cpp. |
| **openai-whisper** | `pip install openai-whisper` | Reference / simplicity | Pure PyTorch reference impl; slowest, heaviest. Easiest to script. |

whisper.cpp invocation (gives timestamped SRT/VTT/JSON — keep the timestamps):

```bash
# Download a model once (whisper.cpp ships a download script).
# large-v3 or medium.en are good picks
whisper-cli -m ggml-large-v3.bin -f audio.wav -osrt -oj
# -osrt → audio.wav.srt   -oj → JSON with word/segment timestamps
```

faster-whisper (Python, timestamped):

```python
from faster_whisper import WhisperModel
model = WhisperModel("large-v3", device="cpu", compute_type="int8")
segments, info = model.transcribe("audio.mp3", word_timestamps=True)
for s in segments:
    print(s.start, s.end, s.text)
```

**Tradeoffs to encode in the skill:** prefer existing captions always (free, instant, exact on-screen wording). Whisper costs minutes of compute per video and can mis-spell proper nouns/jargon — but it produces clean, well-punctuated text (often *better* reading quality than YouTube auto-captions) and works on any video. Pick `medium.en`/`large-v3` for quality, `small`/`base` for speed on long videos.

Sources: https://codersera.com/blog/faster-whisper-vs-whisper-cpp-speech-to-text-2026/ , https://modal.com/blog/choosing-whisper-variants

---

## 2. Video metadata

### 2.1 yt-dlp — no API key, richest source

```bash
# Dump everything to stdout as JSON (one line)
yt-dlp --skip-download --dump-json "URL" > meta.json

# Or write <id>.info.json alongside
yt-dlp --skip-download --write-info-json "URL"
```

Key fields in the JSON: `title`, `uploader` / `channel`, `channel_id`, `description`, `duration` (seconds), `upload_date`, `view_count`, `like_count`, `tags`, `categories`, `thumbnails` (array), and crucially **`chapters`** — an array of `{start_time, end_time, title}`. yt-dlp parses chapters out of the description/markers, which the official API does **not** expose.

Thumbnails:

```bash
yt-dlp --skip-download --write-thumbnail "URL"        # best thumbnail
yt-dlp --skip-download --write-all-thumbnails "URL"   # every resolution
```

### 2.2 YouTube Data API v3 — optional, needs a key

`videos.list` returns: `snippet` (title, description, channelTitle, tags, thumbnails), `contentDetails.duration` (ISO-8601, e.g. `PT15M33S`), `statistics` (viewCount, likeCount, commentCount). An **API key alone is sufficient** for these public reads; OAuth is only needed for private/owner data and writes. The default daily quota is 10,000 units; `videos.list` costs 1 unit per call — effectively free at this scale. **It does NOT return chapters.**

**Recommendation:** use **yt-dlp for metadata** — no key to manage, and it's the only way to get chapters, which are the best natural segment boundaries for a sketchnote (see §3.4). Reach for the Data API only if the skill already has a key and you want official channel/stat data.

Sources: https://developers.google.com/youtube/v3/docs/videos , https://github.com/yt-dlp/yt-dlp

---

## 3. Extracting useful visuals / graphics

Sketchnotes benefit from real diagrams, slides, and on-screen text — not just the talking-head transcript.

### 3.1 Get the video (when you need frames)

```bash
# Cap resolution to keep it fast — 720p is plenty for frame/OCR extraction
yt-dlp -f "bv*[height<=720]+ba/b[height<=720]" -o "video.%(ext)s" "URL"
```

### 3.2 Keyframe extraction with ffmpeg

**Scene-change detection** (best for slide decks / diagram-heavy talks — fires on cut/slide changes):

```bash
ffmpeg -i video.mp4 -vf "select='gt(scene,0.4)',showinfo" -vsync vfr frame_%04d.png
```
Threshold `0.3`–`0.5`: lower = more frames, higher = only big changes. Tune per content type.

**Interval sampling** (one frame every N seconds — predictable count for long videos):

```bash
ffmpeg -i video.mp4 -vf "fps=1/10" frame_%04d.png   # one frame / 10s
```

**I-frames only** (cheap, decode-light, roughly tracks scene changes):

```bash
ffmpeg -skip_frame nokey -i video.mp4 -vsync vfr -frame_pts true keyframe_%04d.png
```

**Frame at a specific chapter timestamp** (combine with §2 chapter data — grab one representative frame per chapter):

```bash
ffmpeg -ss 00:03:25 -i video.mp4 -frames:v 1 chapter_03.png
```

Source: https://ffmpeg.org/ffmpeg-filters.html

### 3.3 Detect slides / text-heavy frames with OCR

Run extracted frames through Tesseract to (a) recover on-screen text and (b) *score* which frames are slide-like (lots of text) vs talking-head (little text), so you keep only the informative ones.

```bash
brew install tesseract           # engine
pip install pytesseract Pillow   # python wrapper
```

```python
import pytesseract
from PIL import Image

text = pytesseract.image_to_string(Image.open("frame_0007.png"))
# Heuristic: more than ~15 words ⇒ likely a slide/diagram worth keeping
if len(text.split()) > 15:
    keep(frame, text)
```

CLI equivalent: `tesseract frame_0007.png stdout`. Captured slide text feeds straight into the LLM as extra structure, and the chosen frames can become visual reference for the sketchnote.

De-dupe near-identical slides with a perceptual hash (`pip install imagehash`) before OCR to cut cost.

Source: https://pypi.org/project/pytesseract/

### 3.4 Use chapters as segment boundaries

Chapters from §2.1 are the cleanest way to segment a video into topics. For each `{start_time, end_time, title}`: slice the transcript to that window, grab one keyframe near the midpoint, and OCR it. This gives the LLM a tidy per-topic bundle and naturally maps onto sketchnote sections.

---

## 4. Going from raw transcript to structured outline (LLM step)

The extraction code's job is to assemble the richest possible context block; the LLM does the structuring. Hand the LLM, in priority order:

1. **Metadata header** — title, channel, duration, description (orients the model on topic/tone).
2. **Chapter list** (if present) — already a human-authored outline; let it drive sketchnote sections.
3. **Timestamped transcript** — keep timestamps so the model can attribute quotes/points and align to chapters. Either captions or Whisper output.
4. **On-screen text per segment** — OCR'd slide/diagram text, tagged with timestamps so the model can merge spoken + written content (slides often contain the key terms/diagram labels the speaker glosses over).

Ask the LLM to emit: title, 3–7 top-level topics (ideally aligned to chapters), 2–4 key points per topic, notable quotes (with timestamps), and any diagram/visual cues surfaced by OCR. That structured outline is the direct input to the sketchnote layout.

---

## 5. Practical gotchas

- **Bot detection ("Sign in to confirm you're not a bot")** is the #1 failure mode in 2025–2026. YouTube reads yt-dlp's open source and patches against it; fixes last days-to-weeks. Mitigations:
  - `yt-dlp --cookies-from-browser safari` (or `chrome`/`firefox`) — sends a logged-in session; Firefox cookies are often the most reliable. Or export a `cookies.txt` and use `--cookies cookies.txt`.
  - `--sleep-interval 5 --max-sleep-interval 15` to throttle and avoid tripping detection. Sessions tend to invalidate after ~20–50 downloads.
  - Avoid VPN/datacenter IPs — they're flagged; use the regular ISP connection or residential proxies.
  - Client spoofing via `--extractor-args` exists but is a moving target; **always run the latest yt-dlp** (`yt-dlp -U`) before trusting any workaround.
- **PO tokens / JS runtime**: some formats now require a JS runtime (e.g. Deno) for PO-token generation. Install a JS runtime and pass `--extractor-args` per current yt-dlp docs if you hit "requires PO token" errors.
- **Age-restricted / members-only / region-locked**: need cookies from a logged-in (and entitled) account. Use yt-dlp `--cookies-from-browser`. The transcript API can't handle these reliably.
- **No captions at all**: the transcript API raises; detect and fall through to Whisper (§1.3).
- **Live streams / premieres**: no usable transcript until processed; chapters/duration may be absent.
- **Legal / ToS**: downloading is contrary to YouTube's Terms of Service. For a sketchnote skill, lean toward the **captions + metadata path** (lighter footprint) and treat full video/audio download as the fallback. Respect copyright — a sketchnote is transformative/commentary, but don't redistribute the source media. Document this in the skill.
- **What breaks**: yt-dlp extractor changes (update first, always), the transcript API's undocumented endpoints, and IP/cookie session expiry. Build retries and a captions→subs→Whisper cascade so one failure doesn't kill the run.

Sources: https://github.com/yt-dlp/yt-dlp/issues/15865 , https://tornadoapi.io/blog/sign-in-to-confirm-you-are-not-a-bot

---

## 6. Recommended end-to-end pipelines

Set a reusable cookie flag once: `COOKIES="--cookies-from-browser safari"` (or your browser). Add `--sleep-interval 5` on bulk runs.

### (a) Video WITH captions — the fast path (no video download)

```bash
VID="VIDEO_ID"; URL="https://www.youtube.com/watch?v=$VID"

# 1. Metadata + chapters (no key needed)
yt-dlp --skip-download --write-info-json $COOKIES -o "%(id)s" "$URL"

# 2. Captions — try manual first
youtube_transcript_api $VID --languages en --format json > transcript.json
#    (or, more robust, via yt-dlp:)
# yt-dlp --write-subs --write-auto-subs --sub-langs "en.*" --sub-format srt \
#        --skip-download $COOKIES -o "%(id)s" "$URL"

# 3. (Optional) thumbnail as a free visual
yt-dlp --skip-download --write-thumbnail $COOKIES -o "%(id)s" "$URL"

# 4. (Optional, for diagrams) download 720p, sample slide frames + OCR — see (b) steps 3–5
```
Feed `transcript.json` + chapters from `<id>.info.json` to the LLM (§4). Fast, light, no ToS-heavy media download. Add the visual steps only if the video is slide/diagram-heavy.

### (b) Video WITHOUT captions — the full path

```bash
VID="VIDEO_ID"; URL="https://www.youtube.com/watch?v=$VID"

# 1. Metadata + chapters
yt-dlp --skip-download --write-info-json $COOKIES -o "%(id)s" "$URL"

# 2. Audio → 16kHz mono wav for Whisper
yt-dlp -x --audio-format wav --postprocessor-args "-ar 16000 -ac 1" \
       $COOKIES -o "audio.%(ext)s" "$URL"

# 3. Transcribe locally (Apple Silicon → whisper.cpp), timestamped SRT + JSON
whisper-cli -m ggml-large-v3.bin -f audio.wav -osrt -oj

# 4. Video for visuals (cap at 720p)
yt-dlp -f "bv*[height<=720]+ba/b[height<=720]" $COOKIES -o "video.%(ext)s" "$URL"

# 5. Scene-change keyframes
ffmpeg -i video.mp4 -vf "select='gt(scene,0.4)'" -vsync vfr frame_%04d.png

# 6. OCR each frame; keep text-heavy (slide) frames
python ocr_filter.py frame_*.png > onscreen_text.json   # uses pytesseract, >15-word heuristic
```
Feed Whisper transcript (with timestamps) + chapters + `onscreen_text.json` to the LLM (§4).

---

## Sources
- youtube-transcript-api: https://github.com/jdepoix/youtube-transcript-api
- yt-dlp: https://github.com/yt-dlp/yt-dlp — bot-detection issues: https://github.com/yt-dlp/yt-dlp/issues/15865
- Whisper runtime comparison: https://codersera.com/blog/faster-whisper-vs-whisper-cpp-speech-to-text-2026/ , https://modal.com/blog/choosing-whisper-variants
- ffmpeg filters: https://ffmpeg.org/ffmpeg-filters.html
- Tesseract / pytesseract: https://formulae.brew.sh/formula/tesseract , https://pypi.org/project/pytesseract/
- YouTube Data API v3: https://developers.google.com/youtube/v3/docs/videos
- 2026 yt-dlp guide / bot-detection: https://www.devkantkumar.com/blog/yt-dlp-ultimate-guide-2026/ , https://tornadoapi.io/blog/sign-in-to-confirm-you-are-not-a-bot

---

**Key takeaways for building the skill:** (1) Cascade captions → subtitles → Whisper; never assume captions exist. (2) Use yt-dlp (not the Data API) for metadata because only it returns **chapters**, the best segment boundaries. (3) On macOS use **whisper.cpp** for ASR (Metal-accelerated, no Python dep). (4) Keep **timestamps** everywhere so transcript, chapters, and OCR'd slide text all align for the LLM. (5) Always `yt-dlp -U` and have a `--cookies-from-browser` fallback — bot detection is the most common breakage.
