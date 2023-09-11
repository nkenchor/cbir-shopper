import os
from ultralytics import YOLO
from app.infrastructure.utilities.service_utils import ModelDownloader

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Constants for the YOLO model
YOLO_MODEL_NAME = 'yolov8n.pt'
YOLO_MODEL_URL = "https://github.com/ultralytics/assets/releases/download/v0.0.0/yolov8n.pt"
MODEL_PATH = os.path.join(BASE_DIR, 'model', 'pretrained', YOLO_MODEL_NAME)
LOADED_MODEL = None  # Initialize the global model variable

def model_exists():
    return os.path.isfile(MODEL_PATH)

def download_yolo_model(base_directory=BASE_DIR):
    if model_exists():
        print("YOLO model already exists.")
        return

    # Initialize the ModelDownloader
    downloader = ModelDownloader(base_dir=base_directory, model_folder='model/pretrained')
    downloader.download(YOLO_MODEL_NAME, YOLO_MODEL_URL)

def load_pretrained_yolo_model():
    global LOADED_MODEL
    if LOADED_MODEL is None:
        # Load the pre-trained model
        LOADED_MODEL = YOLO(MODEL_PATH)
    return LOADED_MODEL

def get_or_load_yolo_model():
    if not model_exists():
        download_yolo_model()
    return load_pretrained_yolo_model()

if __name__ == "__main__":
    model = get_or_load_yolo_model()
    print("Pre-trained YOLO model loaded successfully!")
