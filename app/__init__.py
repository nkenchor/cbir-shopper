from flask import Flask
from flask_cors import CORS
from app.application.api.api import api  # This imports the Blueprint

# Your other imports
import app.application.services.yolo_services.yolo_loader as yolo
import app.application.services.yolo_services.yolo_loader as yolo_loader
import app.application.services.retrieval_services.google_vector_loader as google_loader
import app.application.services.resnet_services.resnet_loader as resnet_loader
from app.infrastructure.utilities.database_utils import setup_db
from app.application.services.retrieval_services import google_vector_loader as google_loader


from flasgger import Swagger

def download_models():
    # Model downloading logic
    print("Downloading Yolo model...")
    yolo_loader.get_or_load_yolo_model()
    print("Downloading Google Word2Vec models...")
    google_loader.get_or_load_nlp_model()
    print("Downloading Resnet models...")
    resnet_loader.get_or_load_resnet_models()
    google_loader.LOADED_MODEL = google_loader.load_google_model()

def create_app():
    app = Flask(__name__)
    CORS(app)
    Swagger(app)
    app.register_blueprint(api)  # Register the blueprint
   
    # Set up the database
    setup_db()
    # Download and train models
    download_models()
  

    return app

