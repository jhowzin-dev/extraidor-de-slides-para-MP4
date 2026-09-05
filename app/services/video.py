import os
import subprocess
import zipfile

from app.config import FFMPEG
from app.services.image import image_hash, images_differ


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
