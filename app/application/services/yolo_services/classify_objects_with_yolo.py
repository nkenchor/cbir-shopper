import json
from app.application.services.yolo_services import yolo_model_training
from app.application.services.retrieval_services import product_suggestion_service as suggestions

import time


def classify_objects_with_yolo(image_path, confidence_threshold=0.5):
    start_time = time.time()

    # Load the model's state from disk and instantiate the model
    model = yolo_model_training.load_trained_yolo_model()
    results = model(image_path)

    classifications = []
    for image_results in results:
        json_string = image_results.tojson()
        json_results = json.loads(json_string)

        for object in json_results:
            name = object["name"]
            raw_confidence = object["confidence"]
            confidence = "{:.2f}%".format(raw_confidence * 100)

            # Filtering based on confidence
            if raw_confidence < confidence_threshold:
                continue

            bounding_box = object["box"]  # Extracting bounding box

            classification_info = {
                "name": name,
                "confidence": confidence,
                "bounding_box": bounding_box,  # Adding bounding box to the info
                "suggestions": suggestions.get_suggestions(name)
            }
            classifications.append(classification_info)

    # Ranking based on confidence
    classifications.sort(key=lambda x: x['confidence'], reverse=True)

    end_time = time.time()
    latency = end_time - start_time

    return {
        "processing_time_seconds": latency,  # Adding processing time
        "classifications": classifications
    
    }

