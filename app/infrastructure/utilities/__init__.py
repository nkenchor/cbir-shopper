import os
from app.infrastructure.utilities import image_utils

from pathlib import Path

# Using pathlib to get the directory of the current file
BASE_DIR = Path(__file__).parent
# Getting the parent directory of the BASE_DIR
ROOT_DIR = BASE_DIR.parent
print(ROOT_DIR)
# Define directories using the ROOT_DIR
image_utils.IMAGE_DIR = ROOT_DIR / 'images'
image_utils.UPLOADED = image_utils.IMAGE_DIR / 'uploaded'
image_utils.DOWNLOADED = image_utils.IMAGE_DIR / 'downloaded'
image_utils.SAMPLES = image_utils.IMAGE_DIR / 'samples'

# Ensure directories exist or create them
for dir_path in [image_utils.UPLOADED, image_utils.DOWNLOADED, image_utils.SAMPLES]:
    dir_path.mkdir(parents=True, exist_ok=True)

# Convert to absolute paths
image_utils.UPLOADED = image_utils.UPLOADED.resolve()
image_utils.DOWNLOADED = image_utils.DOWNLOADED.resolve()