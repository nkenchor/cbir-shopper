import os
from app.infrastructure.utilities import image_utils

# Base directory points to utilities, so we navigate two steps back to the main directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

image_utils.UPLOADED = os.path.join(BASE_DIR, '..', 'images', 'uploaded')
image_utils.DOWNLOADED = os.path.join(BASE_DIR, '..', 'images', 'downloaded')