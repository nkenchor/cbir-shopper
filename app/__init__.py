from flask import Flask
from app.application.api.api import api  # This imports the Blueprint

# Your other imports
import app.application.services.yolo_services.yolo_model_training as yolo
import app.application.services.yolo_services.download_yolo_model as download_yolo_model
import app.application.services.retrieval_services.load_google_vector as download_suggestion_model
import app.application.services.resnet_services.download_resnet_model as download_resnet_model
from app.infrastructure.utilities.database_utils import setup_db


def download_models():
    # Model downloading logic
    print("Downloading Yolo model...")
    download_yolo_model.download_yolo_model()
    print("Downloading Google Word2Vec models...")
    download_suggestion_model.download_googlenews_vector()
    print("Downloading Resnet models...")
    download_resnet_model.download_resnet_models()

def create_app():
    app = Flask(__name__)
    app.register_blueprint(api)  # Register the blueprint
    # Set up the database
    setup_db()
    # Download and train models
    download_models()
    print("Starting the YOLO training process...")
    yolo.train_yolo_model()
    print("Finished the YOLO training process.")

    return app

