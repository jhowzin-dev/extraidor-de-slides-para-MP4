import os
import uuid
import zipfile
import subprocess
from pathlib import Path
from flask import Flask, render_template, request, jsonify, send_file, send_from_directory
from PIL import Image

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = str(Path(__file__).parent / "uploads")
app.config["OUTPUT_FOLDER"] = str(Path(__file__).parent / "outputs")
app.config["MAX_CONTENT_LENGTH"] = 2 * 1024 * 1024 * 1024

FFMPEG = "ffmpeg"

def get_duration(video_path):
    result = subprocess.run(
        [FFMPEG, "-i", video_path, "-f", "null", "-"],
        capture_output=True, text=True
    )
    for line in result.stderr.splitlines():
        if "Duration" in line:
            parts = line.split("Duration:")[1].split(",")[0].strip()
            h, m, s = parts.split(":")
            return float(h) * 3600 + float(m) * 60 + float(s)
    return 0

def extract_frame(video_path, seconds, output_path):
    cmd = [
        FFMPEG, "-ss", str(seconds), "-i", video_path,
        "-frames:v", "1", "-q:v", "2", output_path, "-y"
    ]
    subprocess.run(cmd, capture_output=True, timeout=30)

def image_hash(path):
    with Image.open(path) as img:
        img = img.resize((80, 45)).convert("L")
        pixels = list(img.getdata())
        avg = sum(pixels) / len(pixels)
        return tuple(1 if p > avg else 0 for p in pixels)

def images_differ(h1, h2, threshold=0.08):
    if h1 is None:
        return True
    diff = sum(a != b for a, b in zip(h1, h2)) / len(h1)
    return diff > threshold

def extract_slides(video_path, output_dir, interval=8):
    os.makedirs(output_dir, exist_ok=True)
    temp_frame = os.path.join(output_dir, "_temp.png")
    duration = get_duration(video_path)
    prev_hash = None
    slide_num = 0
    t = 0

    while t < duration:
        try:
            extract_frame(video_path, t, temp_frame)
            if os.path.exists(temp_frame):
                curr_hash = image_hash(temp_frame)
                if images_differ(prev_hash, curr_hash):
                    slide_num += 1
                    dest = os.path.join(output_dir, f"slide_{slide_num:03d}.png")
                    os.rename(temp_frame, dest)
                    prev_hash = curr_hash
                else:
                    os.remove(temp_frame)
        except Exception:
            pass
        t += interval

    return slide_num

def create_zip(source_dir, zip_path):
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for file in sorted(os.listdir(source_dir)):
            if file.startswith("slide_") and file.endswith(".png"):
                zf.write(os.path.join(source_dir, file), file)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/extract", methods=["POST"])
def extract():
    if "video" not in request.files:
        return jsonify({"error": "Nenhum arquivo enviado"}), 400

    video = request.files["video"]
    if not video.filename:
        return jsonify({"error": "Arquivo inválido"}), 400

    job_id = str(uuid.uuid4())[:8]
    job_upload = os.path.join(app.config["UPLOAD_FOLDER"], f"{job_id}_{video.filename}")
    job_output = os.path.join(app.config["OUTPUT_FOLDER"], job_id)

    video.save(job_upload)

    try:
        interval = int(request.form.get("interval", 8))
    except (ValueError, TypeError):
        interval = 8

    slide_count = extract_slides(job_upload, job_output, interval)

    if slide_count == 0:
        return jsonify({"error": "Nenhum slide detectado"}), 400

    zip_path = os.path.join(app.config["OUTPUT_FOLDER"], f"{job_id}.zip")
    create_zip(job_output, zip_path)

    slides = sorted([f for f in os.listdir(job_output) if f.startswith("slide_") and f.endswith(".png")])

    return jsonify({
        "job_id": job_id,
        "slide_count": slide_count,
        "slides": slides
    })

@app.route("/slide/<job_id>/<filename>")
def serve_slide(job_id, filename):
    return send_from_directory(os.path.join(app.config["OUTPUT_FOLDER"], job_id), filename)

@app.route("/download/<job_id>")
def download(job_id):
    zip_path = os.path.join(app.config["OUTPUT_FOLDER"], f"{job_id}.zip")
    if not os.path.exists(zip_path):
        return jsonify({"error": "Arquivo não encontrado"}), 404
    return send_file(zip_path, as_attachment=True, download_name=f"slides_{job_id}.zip")

if __name__ == "__main__":
    os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)
    os.makedirs(app.config["OUTPUT_FOLDER"], exist_ok=True)
    app.run(debug=True, host="0.0.0.0", port=5000)
