
import json
from app.application.services.yolo_services import yolo_model_training as yolo_model_training

def identify_objects_with_yolo(image_path):
    """
    Function to perform object detection using a trained YOLO model and return bounding boxes.
    
    Args:
        image_path (str): Path to the input image.
    
    Returns:
        list: List of bounding boxes.
    """
    # Load the model's state from disk and instantiate the model
    model = yolo_model_training.TRAINED_MODEL
    # Predict on an image
    results = model(image_path)

    bounding_boxes = []
    for image_results in results:
        json_string = image_results.tojson()
        json_results = json.loads(json_string)

        for detection in json_results:
            bounding_box = detection["box"]
            bounding_boxes.append(bounding_box)
    return bounding_boxes

