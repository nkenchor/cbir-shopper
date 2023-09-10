from app.infrastructure.utilities.service_utils import ModelDownloader
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

YOLO_MODEL_NAME = 'yolov8n.pt'
YOLO_MODEL_URL = "https://github.com/ultralytics/assets/releases/download/v0.0.0/yolov8n.pt"
MODEL_PATH = os.path.join(BASE_DIR, 'model', 'pretrained', YOLO_MODEL_NAME)

def model_exists():
    return os.path.isfile(MODEL_PATH)

def download_yolo_model(base_directory=BASE_DIR):
    if model_exists():
        print("YOLO model already exists.")
        return

    # Initialize the ModelDownloader
    downloader = ModelDownloader(base_dir=base_directory, model_folder='model/pretrained')
    downloader.download(YOLO_MODEL_NAME, YOLO_MODEL_URL)
