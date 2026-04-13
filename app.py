from flask import Flask, request, jsonify, send_file, render_template_string
import yt_dlp
import os
import threading
import uuid
import json

app = Flask(__name__)

DOWNLOAD_DIR = os.path.join(os.path.dirname(__file__), "downloads")
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

# Track download progress per job
progress_store = {}

HTML = open(os.path.join(os.path.dirname(__file__), "index.html")).read()

@app.route("/")
def index():
    return render_template_string(HTML)


@app.route("/info", methods=["POST"])
def get_info():
    data = request.json
    url = data.get("url", "").strip()
    if not url:
        return jsonify({"error": "No URL provided"}), 400
    try:
        ydl_opts = {"quiet": True, "no_warnings": True, "skip_download": True}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
        return jsonify({
            "title": info.get("title", "Unknown"),
            "duration": info.get("duration", 0),
            "channel": info.get("uploader", "Unknown"),
            "thumbnail": info.get("thumbnail", ""),
            "formats": [
                {"format_id": f["format_id"], "ext": f.get("ext"), "height": f.get("height"), "abr": f.get("abr")}
                for f in info.get("formats", [])
            ]
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/download", methods=["POST"])
def download():
    data = request.json
    url = data.get("url", "").strip()
    fmt = data.get("format", "mp4")
    quality = data.get("quality", "1080")
    job_id = str(uuid.uuid4())
    progress_store[job_id] = {"status": "starting", "percent": 0, "filename": None, "error": None}

    def run():
        try:
            is_audio = fmt in ("mp3", "m4a")
            out_template = os.path.join(DOWNLOAD_DIR, f"{job_id}-----%(title)s.%(ext)s")

            def progress_hook(d):
                if d["status"] == "downloading":
                    raw = d.get("_percent_str", "0%").strip().replace("%", "")
                    try:
                        progress_store[job_id]["percent"] = float(raw)
                    except:
                        pass
                    progress_store[job_id]["status"] = "downloading"
                elif d["status"] == "finished":
                    progress_store[job_id]["percent"] = 100
                    progress_store[job_id]["status"] = "processing"

            if is_audio:
                ydl_opts = {
                    "format": "bestaudio/best",
                    "outtmpl": out_template,
                    "postprocessors": [{
                        "key": "FFmpegExtractAudio",
                        "preferredcodec": fmt,
                        "preferredquality": "320" if fmt == "mp3" else "256",
                    }],
                    "progress_hooks": [progress_hook],
                    "quiet": True,
                    "ffmpeg_location": os.path.dirname(__file__),
                }
            else:
                height_map = {"4k": 2160, "1080": 1080, "720": 720, "480": 480, "360": 360}
                h = height_map.get(quality.lower(), 1080)
                ydl_opts = {
                    "format": f"bestvideo[height<={h}][ext={fmt}]+bestaudio[ext=m4a]/bestvideo[height<={h}]+bestaudio/best[height<={h}]",
                    "outtmpl": out_template,
                    "merge_output_format": fmt,
                    "progress_hooks": [progress_hook],
                    "quiet": True,
                    "ffmpeg_location": os.path.dirname(__file__),
                }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])

            # Find the output file
            for f in os.listdir(DOWNLOAD_DIR):
                if f.startswith(job_id):
                    progress_store[job_id]["filename"] = f
                    break
            progress_store[job_id]["status"] = "done"
        except Exception as e:
            progress_store[job_id]["status"] = "error"
            progress_store[job_id]["error"] = str(e)

    threading.Thread(target=run, daemon=True).start()
    return jsonify({"job_id": job_id})


@app.route("/progress/<job_id>")
def progress(job_id):
    return jsonify(progress_store.get(job_id, {"status": "not_found"}))


@app.route("/file/<job_id>")
def serve_file(job_id):
    info = progress_store.get(job_id)
    if not info or not info.get("filename"):
        return "File not found", 404
    path = os.path.join(DOWNLOAD_DIR, info["filename"])
    dl_name = info["filename"]
    if "-----" in dl_name:
        dl_name = dl_name.split("-----", 1)[1]
    return send_file(path, as_attachment=True, download_name=dl_name)


if __name__ == "__main__":
    print("\nYouTube Downloader running at: http://localhost:5000\n")
    app.run(debug=False, port=5000)
