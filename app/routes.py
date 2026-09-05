import os
import uuid

from flask import Blueprint, render_template, request, jsonify, send_file, send_from_directory

from app.config import UPLOAD_FOLDER, OUTPUT_FOLDER
from app.services.video import extract_slides, create_zip

main = Blueprint("main", __name__)


@main.route("/")
def index():
    return render_template("index.html")


@main.route("/extract", methods=["POST"])
def extract():
    if "video" not in request.files:
        return jsonify({"error": "Nenhum arquivo enviado"}), 400

    video = request.files["video"]
    if not video.filename:
        return jsonify({"error": "Arquivo inválido"}), 400

    job_id = str(uuid.uuid4())[:8]
    job_upload = os.path.join(UPLOAD_FOLDER, f"{job_id}_{video.filename}")
    job_output = os.path.join(OUTPUT_FOLDER, job_id)

    video.save(job_upload)

    try:
        interval = int(request.form.get("interval", 8))
    except (ValueError, TypeError):
        interval = 8

    slide_count = extract_slides(job_upload, job_output, interval)

    if slide_count == 0:
        return jsonify({"error": "Nenhum slide detectado"}), 400

    zip_path = os.path.join(OUTPUT_FOLDER, f"{job_id}.zip")
    create_zip(job_output, zip_path)

    slides = sorted([f for f in os.listdir(job_output) if f.startswith("slide_") and f.endswith(".png")])

    return jsonify({
        "job_id": job_id,
        "slide_count": slide_count,
        "slides": slides
    })


@main.route("/slide/<job_id>/<filename>")
def serve_slide(job_id, filename):
    return send_from_directory(os.path.join(OUTPUT_FOLDER, job_id), filename)


@main.route("/download/<job_id>")
def download(job_id):
    zip_path = os.path.join(OUTPUT_FOLDER, f"{job_id}.zip")
    if not os.path.exists(zip_path):
        return jsonify({"error": "Arquivo não encontrado"}), 404
    return send_file(zip_path, as_attachment=True, download_name=f"slides_{job_id}.zip")
