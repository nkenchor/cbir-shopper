import os
from app.infrastructure.utilities import image_utils

from pathlib import Path

# Using pathlib to get the directory of the current file
BASE_DIR = Path(__file__).parent

# Define directories using parent for clarity instead of '..'
UPLOADED = BASE_DIR.parent / 'images' / 'uploaded'
DOWNLOADED = BASE_DIR.parent / 'images' / 'downloaded'

# Convert to absolute paths
UPLOADED = UPLOADED.resolve()
DOWNLOADED = DOWNLOADED.resolve()