# YouTube Downloader — Local Web App

A fully working YouTube downloader with a web UI, powered by Flask + yt-dlp.

## Requirements

- Python 3.7+
- ffmpeg (for merging video+audio and audio conversion)

## Setup

### 1. Install Python dependencies
```bash
pip install flask yt-dlp
```

### 2. Install ffmpeg

**Windows:**
```
winget install ffmpeg
# or download from https://ffmpeg.org/download.html
```

**Mac:**
```bash
brew install ffmpeg
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt install ffmpeg
```

### 3. Run the app
```bash
python app.py
```

Then open your browser at: **http://localhost:5000**

## Features

- Download video in MP4 or WebM at 360p / 480p / 720p / 1080p / 4K
- Download audio as MP3 (320/192/128kbps) or M4A (256/128kbps)
- Live progress bar during download
- One-click "Save file" button when done
- Fetches video title, channel, thumbnail before downloading

## Files

- `app.py` — Flask backend (API routes + serves HTML)
- `index.html` — Frontend UI
- `downloads/` — Downloaded files are saved here (auto-created)

## Notes

- Downloaded files are stored in the `downloads/` folder next to `app.py`
- The app runs locally — your downloads never leave your machine
- yt-dlp is updated frequently; run `pip install -U yt-dlp` if a site breaks
