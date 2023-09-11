import os
import numpy as np
import tensorflow as tf
import json
import time
from app.application.services.retrieval_services import product_suggestion_service as suggestions
from app.application.services.resnet_services.resnet_loader import BASE_DIR, load_resnet_101_model

RESNETMODEL_101_PATH = os.path.join(BASE_DIR, 'model', 'pretrained', 'resnet101_weights_tf_dim_ordering_tf_kernels.h5')
RESNETCLASSINDEX = os.path.join(BASE_DIR, 'model', 'data', 'imagenet_class_index.json')

def classify_objects_with_resnet(image_path, confidence_threshold=0.3):
    start_time = time.time()

    RESNET_101_MODEL = load_resnet_101_model()
    if RESNET_101_MODEL is None:
        raise ValueError("Model has not been initialized. Download and load the model first.")

    img = tf.keras.preprocessing.image.load_img(image_path, target_size=(224, 224))
    img_array = tf.keras.preprocessing.image.img_to_array(img)
    expanded_img_array = np.expand_dims(img_array, axis=0)
    preprocessed_img = tf.keras.applications.resnet.preprocess_input(expanded_img_array)

    predictions = RESNET_101_MODEL.predict(preprocessed_img)
    decoded_objects = decode_objects_with_resnet(predictions, top=5)

    # Filter results based on confidence_threshold
    filtered_objects = [obj for obj in decoded_objects[0] if obj[2] >= confidence_threshold]

    # Sort by confidence
    sorted_objects = sorted(filtered_objects, key=lambda x: x[2], reverse=True)

    classifications = [{
        "name": object[1],
        "confidence": "{:.2f}%".format(float(object[2] * 100)),
        "suggestions": suggestions.get_suggestions(object[1]),
        "bounding_box": []  # Adding an empty bounding_box for consistency
    } for object in sorted_objects]

    end_time = time.time()
    latency = end_time - start_time

    return {
        "processing_time_seconds": latency,
        "classifications": classifications
        
    }



def decode_objects_with_resnet(preds, top=5):
    with open(RESNETCLASSINDEX, 'r') as f:
        CLASS_INDEX = json.load(f)

    results = []
    for pred in preds:
        top_indices = pred.argsort()[-top:][::-1]
        result = [tuple(CLASS_INDEX[str(i)]) + (pred[i],) for i in top_indices]
        results.append(result)
    return results
