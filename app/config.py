from pathlib import Path

BASE_DIR = Path(__file__).parent.parent

UPLOAD_FOLDER = str(BASE_DIR / "uploads")
OUTPUT_FOLDER = str(BASE_DIR / "outputs")
MAX_CONTENT_LENGTH = 2 * 1024 * 1024 * 1024  # 2GB
FFMPEG = "ffmpeg"
