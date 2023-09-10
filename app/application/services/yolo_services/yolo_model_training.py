import shutil
from ultralytics import YOLO
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
YOLOTRAINED = os.path.join(BASE_DIR, 'model', 'trained', 'yolo_trained.pt')
YOLOPRETRAINED = os.path.join(BASE_DIR, 'model', 'pretrained', 'yolov8n.pt')
TRAINED_MODEL = None  # Initialize the global model variable


def train_yolo_model(pretrained_path=YOLOPRETRAINED, data_path="coco128.yaml", epochs=3):
    """
    Function to train a YOLO model.
    
    Args:
        pretrained_path (str): Path to a pretrained model.
        data_path (str): Path to data for training.
        epochs (int): Number of training epochs.
    
    Returns:
        None
    """
    global TRAINED_MODEL
    
    # Load a pretrained model
    model = YOLO(pretrained_path) 

    # Train the model
    model.train(data=data_path, epochs=epochs)

    # Save the trained model's state to disk
    exported_model_path = model.export()
    shutil.move(exported_model_path, YOLOTRAINED)
    TRAINED_MODEL = model  # Save the model to the global variable


def load_trained_yolo_model():
    global TRAINED_MODEL
    if TRAINED_MODEL is None:
        # Load the trained model
        TRAINED_MODEL = YOLO(YOLOTRAINED)
    return TRAINED_MODEL
    

if __name__ == "__main__":
    train_yolo_model()
