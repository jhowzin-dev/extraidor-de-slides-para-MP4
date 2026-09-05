import os

from flask import Flask

from app.config import UPLOAD_FOLDER, OUTPUT_FOLDER, MAX_CONTENT_LENGTH
from app.routes import main


def create_app():
    app = Flask(__name__)
    app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
    app.config["OUTPUT_FOLDER"] = OUTPUT_FOLDER
    app.config["MAX_CONTENT_LENGTH"] = MAX_CONTENT_LENGTH

    app.register_blueprint(main)

    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)

    return app
