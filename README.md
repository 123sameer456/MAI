# ClipCraft Pro (MAI)

**ClipCraft Pro** is a Flask web app that transforms long videos into short-form social media content automatically. Upload a video and the pipeline transcribes it, finds the best clip-worthy moments, cuts short clips, generates hooks, burns in word-by-word animated subtitles, and writes platform-specific titles and captions for both "serious" (X/LinkedIn/Threads) and "entertainment" (YouTube/Instagram/TikTok/Facebook) platforms.

It also includes tools for AI voiceover generation (ElevenLabs), background music mixing, and Facebook Page publishing.

## About This App

ClipCraft Pro is a one-stop studio for **repurposing long-form video into short-form content**. Instead of manually scrubbing through hours of footage to find the good parts, cutting clips, writing captions for every platform, and adding subtitles by hand, you upload one video and let the app do the whole job.

The core idea is that a single long video — a podcast, interview, webinar, sermon, or vlog — already contains many self-contained "moments" that would perform well as reels, Shorts, and TikToks. The app's job is to **find those moments and package them**. It listens to the video (Whisper), understands which sections form a complete, engaging idea (GPT), then produces a full content kit for each one:

- a **short clip** ready to post,
- a **subtitled version** with the spoken word dynamically highlighted for maximum retention,
- a **hook clip** built around the most attention-grabbing line,
- and **titles, captions, CTAs, and hashtags** written separately for serious platforms (X, LinkedIn, Threads) and entertainment platforms (YouTube, Instagram, TikTok, Facebook).

On top of the automated pipeline, it gives you a hands-on toolkit: generate an AI voiceover with ElevenLabs, mix that voice with background music, drop the mix back onto a video, and schedule the finished result to a Facebook Page — all from the same web interface.

**Who it's for:** creators, social media managers, marketers, and small teams who want to turn a large volume of long video into a steady stream of platform-ready shorts without a manual editing workflow. Everything runs with your own OpenAI and ElevenLabs API keys, and finished assets are served from the app's `static/` folders.

## Features

- **Video transcription** — Extracts audio and transcribes it with OpenAI Whisper (sentence- and word-level timestamps).
- **Clip detection** — Uses GPT to analyze the transcript and pick 60–120s segments that work as standalone reels/shorts (strong hook, single idea, natural stop point).
- **Short clip creation** — Cuts clips with configurable fade-in/fade-out effects via MoviePy.
- **Hook videos** — Selects a strong hook sentence per script and builds speed-adjusted hook clips.
- **Word-highlighted subtitles** — Burns in subtitles with the active word highlighted using word-level Whisper timestamps and PIL (no ImageMagick required).
- **Titles & captions** — Generates two caption sets per clip: serious platforms (no emojis) and entertainment platforms (emojis, CTAs, 9 hashtags).
- **AI voiceover** — Generates speech from text with ElevenLabs and can record/upload custom voice audio.
- **Audio mixing** — Combines voice tracks with background music at adjustable volumes (pydub).
- **Video audio replacement** — Swaps a video's audio track with a mixed audio file, trimming or looping to match length.
- **Facebook publishing** — Uploads/schedules a video with a custom thumbnail to a Facebook Page.
- **YouTube download** — Downloads source videos with `yt-dlp` (cookie-assisted).
- **Summarized video** — Produces condensed versions with randomized effects (speed, zoom, rotation, B&W, fades).
- **Async processing UI** — Background threading with a live progress bar and auto-redirect to results.

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Web | Flask 3, Jinja2 templates, Bootstrap 5, WaveSurfer.js |
| AI | OpenAI (`whisper-1`, `gpt-4o-mini`), ElevenLabs TTS |
| Video/Audio | MoviePy, FFmpeg, pydub, OpenCV, Pillow, NumPy |
| Downloading | yt-dlp, pytube |
| Server | Gunicorn (production), Flask dev server |

## Project Structure

```
MAI/
├── audio.py                     # MoviePy audio-effect experiments (fade, loop, normalize, volume)
├── features                     # (empty placeholder file)
└── video_generation/
    ├── app.py                   # Main Flask app: routes, async pipeline, audio mixing
    ├── step1.py                 # Standalone script version of the processing pipeline
    ├── phase1.py / phase2.py    # Earlier Flask app + Facebook upload helpers
    ├── video_text_semgment.py   # Whisper transcription (sentence-level segments)
    ├── subtitles.py             # Word-level subtitles with highlighted active word
    ├── clip_info.py             # GPT prompt/parse for clip script + time ranges
    ├── short_clips.py           # Cut clips with fade in/out
    ├── hooks_bot.py             # Hook extraction + hook clip creation (+ voice variants)
    ├── title_desciption_bot.py  # GPT titles/captions generator
    ├── system_messages.py       # All system prompts + caption JSON helpers
    ├── mixture.py               # Voice + music combine helper
    ├── elevenlab.py             # ElevenLabs voice generation helper
    ├── summarized_video.py      # Summarized video with random effects
    ├── social_media_downloader.py # YouTube download via yt-dlp
    ├── video_editing.py         # Fade/silence-detection editing experiments
    ├── test.py, simple_bot.py   # Scratch/experiment files
    ├── requirements.txt         # Pinned dependencies
    ├── final_requirements.txt   # Duplicate of requirements.txt
    ├── templates/               # base.html, sixth.html (home), hooks.html, preview.html
    └── static/                  # css, uploads, clips, clips_with_subtitles, hooks,
                                 # background_sound_effects, combined, custom_audio_video,
                                 # title_caption_data.json
```

## Installation

Requires **Python 3.10+** and **FFmpeg** installed on your system (FFmpeg must be on `PATH`).

```bash
cd video_generation
python -m venv venv
venv\Scripts\activate          # Windows
# source venv/bin/activate     # macOS / Linux

pip install -r requirements.txt
```

### API Keys

The code currently hardcodes placeholder keys that must be replaced before running:

- **OpenAI** — `OPENAI_API_KEY` in `clip_info.py`, `hooks_bot.py`, `subtitles.py`, `title_desciption_bot.py`, `video_text_semgment.py`, `test.py`
- **ElevenLabs** — `YOUR_ELEVENLABS_API_KEY` in `app.py`, `elevenlab.py`
- **Facebook** — `FB_PAGE_ACCESS_TOKEN` / `FB_PAGE_ID` in `phase1.py`, `phase2.py`

> **Security note:** These credentials are hardcoded placeholders. Prefer moving them to environment variables (e.g. `os.environ["OPENAI_API_KEY"]`) or a `.env` file before deploying.

## Running the App

```bash
cd video_generation
python app.py
```

The app listens on `http://0.0.0.0:8000`. For production:

```bash
gunicorn -b 0.0.0.0:8000 app:app
```

## Main Routes

| Route | Method | Purpose |
|-------|--------|---------|
| `/` | GET/POST | Upload page; POST starts a background processing task and returns a `task_id` |
| `/progress/<task_id>` | GET | JSON progress (percent + current step) for the polling UI |
| `/results/<task_id>` | GET | Renders the preview gallery once processing completes |
| `/hooks/` | GET/POST | Hook builder: upload/record/text-to-voice audio + background mixing |
| `/preview/` | GET | Gallery of generated clips, hooks, and captions |
| `/combine_audio` | POST | Mixes a voice file with one or more background tracks |
| `/process_video` | POST | Replaces a selected video's audio with the latest combined mix |
| `/download/<filename>` | GET | Downloads a combined audio file |
| `/api/videos/<video_type>` | GET | Lists `hooks`, `clips`, or `clips_with_subtitles` videos as JSON |

## Processing Pipeline

1. **Upload** — Video saved to `static/` and a unique `task_id` is issued.
2. **Transcribe** — Whisper produces sentence segments (and word timestamps for subtitles).
3. **Detect clips** — GPT returns scripts with `start-time` / `end-time`.
4. **Titles & captions** — GPT writes serious + entertainment variants per clip → saved to `static/title_caption_data.json`.
5. **Cut clips** — Fade-in/out short clips written to `static/clips`.
6. **Hooks** — A hook sentence per script is chosen and hook clips are built in `static/hooks`.
7. **Subtitles** — Word-highlighted subtitled clips written to `static/clips_with_subtitles`.
8. **Preview** — Results rendered on `/results/<task_id>` for download/publishing.

All output folders are cleared at the start of each run, so only the most recent job's output is retained.

## Notes

- `requirements.txt` and `final_requirements.txt` are identical duplicates.
- `audio.py` and `video_editing.py` are standalone experiment scripts, not part of the web app.
- `app copy.py` and `step1.py` are earlier/standalone iterations of the pipeline.
- `youtube_cookies.txt` is used by `yt-dlp`; treat it as a secret and do not commit real cookies.
