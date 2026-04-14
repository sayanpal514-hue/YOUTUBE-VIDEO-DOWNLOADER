# YouTube Downloader — Local Web App

A clean, modern YouTube downloader with a web UI, powered by Flask + yt-dlp.

## Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Install FFmpeg (Required for 1080p/4K and MP3)
- **Windows**: `winget install ffmpeg` (Remember to **restart VS Code** after installing)
- **Mac**: `brew install ffmpeg`
- **Linux**: `sudo apt install ffmpeg`

### 3. Run the App
```bash
python app.py
```
Then open your browser at: **http://localhost:5000**

## Features
-   **High Quality**: Download video in 4K, 1080p, 720p, etc.
-   **Audio Extraction**: Save as MP3 (320kbps) or M4A.
-   **Live Progress**: Real-time progress bar and status updates.
-   **Bot Bypass**: Integrated mobile user-agents and client spoofing.
-   **Proxy Support**: Support for `PROXY_URL` environment variables.

## Bot Detection (Important)
If you get a "Sign in to confirm you're not a bot" error:
1.  Export your `cookies.txt` from YouTube (using a browser extension).
2.  Place it in the project root.
3.  The app will automatically detect and use it.

---
*Note: This app is for legal personal use only.*
