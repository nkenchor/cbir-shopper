
import os
from flask import jsonify, request
from app.infrastructure.utilities import api_utils as utils
import uuid
from werkzeug.utils import secure_filename

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOADED = os.path.join(BASE_DIR, '../../../../images','uploaded')
def handle_image_upload():
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
        return filename,file_path, None, None

    return None, jsonify(error="Invalid file type."), 400