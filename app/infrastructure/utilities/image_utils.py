import os
import requests
import uuid
from werkzeug.utils import secure_filename
from flask import jsonify, request
from app.infrastructure.utilities import api_utils as utils
from pathlib import Path

# Using pathlib to get the directory of the current file
BASE_DIR = None
# Getting the parent directory of the BASE_DIR
ROOT_DIR = None

# Define directories using the ROOT_DIR
IMAGE_DIR = None
UPLOADED = None
DOWNLOADED = None
SAMPLES = None


def handle_image_upload():
    """
    Handle uploading of image files.
    """
    if 'image' not in request.files:
        return None, jsonify(error="No file part in the request."), 400

    file = request.files['image']

    if file.filename == '':
        return None, jsonify(error="No selected file."), 400

    if file and utils.allowed_file(file.filename):
        file_extension = os.path.splitext(file.filename)[1]
        if file_extension == '.jpeg':
            file_extension = '.jpg'
        filename = str(uuid.uuid4())
        filename_fullname = filename + file_extension
        file_path = os.path.join(UPLOADED, filename_fullname)
        file.save(file_path)
        return filename, file_path, None, None

    return None, jsonify(error="Invalid file type."), 400

def download_image(url, filename):
    """
    Download an image from a URL and saves it to the specified directory.
    """
    response = requests.get(url)
    if response.status_code == 200:
        with open(os.path.join(DOWNLOADED, filename), 'wb') as file:
            for chunk in response.iter_content(1024):
                file.write(chunk)
    else:
        # Handle failure, e.g., log the error or raise an exception
        pass


def fetch_image_from_downloaded():
    """
    Fetch the image from the DOWNLOADED directory based on the filename.
    """
    image_path = Path(DOWNLOADED) 
    if not image_path.exists():
        return None
    return image_path