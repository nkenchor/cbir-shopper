import os
from flask import jsonify, request,Blueprint
from flask_cors import cross_origin

from app.application.services.retrieval_services import image_retrieval as image_retrieval
from app.application.services.resnet_services import classify_objects_with_resnet  as resnet_classification
from app.application.services.yolo_services import identify_objects_with_yolo  as yolo_identification
from app.application.services.yolo_services import classify_objects_with_yolo  as yolo_classification
from app.application.services.yolo_services import yolo_model_training as yolo_model_training
from app.application.services.retrieval_services import image_upload as image_upload
from app.application.services.resnet_services import feature_extraction_with_resnet as feature_extraction
from werkzeug.utils import secure_filename
import glob



api = Blueprint('api', __name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOADED = os.path.join(BASE_DIR, '../../../images','uploaded')
DOWNLOADED = os.path.join(BASE_DIR, '../../../images','downloaded')

@api.route('/', methods=['GET'])
@cross_origin()
def hello_world():
    """
    This is the hello world endpoint
    ---
    responses:
      200:
        description: Returns a hello message
    """
    return jsonify(message="Hello, this is my CBIR app"), 200

@api.route('/upload_image', methods=['POST'])
def upload_image():
    """
    Upload an image for further processing
    ---
    tags:
      - Image Processing
    consumes:
      - multipart/form-data
    parameters:
      - in: formData
        name: image
        type: file
        required: true
        description: The image to upload.
    responses:
      200:
        description: Image uploaded successfully
        schema:
          type: object
          properties:
            uuid:
              type: string
              description: Unique identifier for the uploaded image
            message:
              type: string
              description: Success message
      default:
        description: Unexpected error
        schema:
          type: object
          properties:
            error:
              type: string
              description: Error message
    """
    uuid, file_path, error, code = image_upload.handle_image_upload()
    if error:
        return error, code
    return jsonify(uuid=uuid, message="Image uploaded successfully."), 200



@api.route('/classify_objects_with_resnet/<image_uuid>', methods=['POST'])
def classify_objects_with_resnet(image_uuid):
    """
    Classify objects within an uploaded image using ResNet
    ---
    tags:
      - Image Classification
    parameters:
      - in: path
        name: image_uuid
        type: string
        required: true
        description: The unique identifier for the uploaded image.
      - in: body
        name: body
        description: Optional body content (if any needed).
        schema:
          type: object
          properties:
            attribute_name:
              type: string
              description: Description of the attribute (modify as needed).
    responses:
      200:
        description: Classification results
        schema:
          type: array
          items:
            type: object
            properties:
              class_name:
                type: string
                description: Name of the identified object
              confidence:
                type: number
                format: float
                description: Confidence score for the identified object
      404:
        description: Image not found for the provided UUID
        schema:
          type: object
          properties:
            error:
              type: string
              description: Error message
      500:
        description: Unexpected error
        schema:
          type: object
          properties:
            error:
              type: string
              description: Error message
    """
    file_paths = glob.glob(os.path.join(UPLOADED, f"{image_uuid}.*"))
    if not file_paths:
        return jsonify(error="Image not found for the provided UUID."), 404
    file_path = file_paths[0]  # Since UUID is unique, there should be only one match
    
    try:
        classifications = resnet_classification.classify_objects_with_resnet(file_path)
        return jsonify(classifications)
    except Exception as e:
        return jsonify(error=f"Error processing image: {str(e)}"), 500

@api.route('/classify_objects_with_yolo/<image_uuid>', methods=['POST'])
def classify_objects_with_yolo(image_uuid):
    """
    Classify objects within an uploaded image using YOLO
    ---
    tags:
      - Image Classification
    parameters:
      - in: path
        name: image_uuid
        type: string
        required: true
        description: The unique identifier for the uploaded image.
    responses:
      200:
        description: Classification results using YOLO
        schema:
          type: array
          items:
            type: object
            properties:
              class_name:
                type: string
                description: Name of the identified object
              confidence:
                type: number
                format: float
                description: Confidence score for the identified object
      404:
        description: Image not found for the provided UUID
        schema:
          type: object
          properties:
            error:
              type: string
              description: Error message
      500:
        description: Unexpected error
        schema:
          type: object
          properties:
            error:
              type: string
              description: Error message
    """
    file_paths = glob.glob(os.path.join(UPLOADED, f"{image_uuid}.*"))
    if not file_paths:
        return jsonify(error="Image not found for the provided UUID."), 404
    file_path = file_paths[0]  # Since UUID is unique, there should be only one match

    try:
        classifications = yolo_classification.classify_objects_with_yolo(file_path)
        return jsonify(classifications)
    except Exception as e:
        return jsonify(error=f"Error processing image: {str(e)}"), 500


@api.route('/identify_objects_with_yolo/<image_uuid>', methods=['POST'])
def identify_objects_with_yolo(image_uuid):
    """
    Identify objects within an uploaded image using YOLO
    ---
    tags:
      - Object Identification
    parameters:
      - in: path
        name: image_uuid
        type: string
        required: true
        description: The unique identifier for the uploaded image.
    responses:
      200:
        description: Identification results using YOLO
        schema:
          type: array
          items:
            type: object
            properties:
              class_name:
                type: string
                description: Name of the identified object
              confidence:
                type: number
                format: float
                description: Confidence score for the identified object
      404:
        description: Image not found for the provided UUID
        schema:
          type: object
          properties:
            error:
              type: string
              description: Error message
      500:
        description: Unexpected error
        schema:
          type: object
          properties:
            error:
              type: string
              description: Error message
    """
    file_paths = glob.glob(os.path.join(UPLOADED, f"{image_uuid}.*"))
    if not file_paths:
        return jsonify(error="Image not found for the provided UUID."), 404
    file_path = file_paths[0]  # Since UUID is unique, there should be only one match

    try:
        classifications = yolo_identification.identify_objects_with_yolo(file_path)
        return jsonify(classifications=classifications), 200
    except Exception as e:
        return jsonify(error=f"Error processing image: {str(e)}"), 500

@api.route('/search_product/<image_uuid>', methods=['POST'])
def search_product(image_uuid):
    """
    Search for a product using an uploaded image's UUID and a keyword
    ---
    tags:
      - Product Search
    parameters:
      - in: path
        name: image_uuid
        type: string
        required: true
        description: The unique identifier for the uploaded image.
      - in: body
        name: body
        required: true
        description: Search parameters including keyword and number of pages.
        schema:
          type: object
          properties:
            keyword:
              type: string
              description: The keyword to use in the search.
              required: true
            pages:
              type: integer
              description: Number of pages to be searched.
              required: true
    responses:
      200:
        description: Search results based on the keyword and pages
        schema:
          type: array
          items:
            type: object
            properties:
              # Adjust these properties based on the structure of your results
              product_name:
                type: string
                description: Name of the product found in the search
              product_image:
                type: string
                description: URL or path of the product image
              product_price:
                type: string
                description: Price of the product
              product_description:
                type: string
                description: Description of the product
      400:
        description: Required parameters (keyword or pages) not provided
        schema:
          type: object
          properties:
            error:
              type: string
              description: Error message
      500:
        description: Unexpected error during the search
        schema:
          type: object
          properties:
            error:
              type: string
              description: Error message
    """
    data = request.get_json()
    if not data or 'keyword' not in data:
        return jsonify(error="Keyword is required."), 400
    if not data or 'pages' not in data:
        return jsonify(error="Pages is required."), 400
    
    keyword = data['keyword']
    no_of_pages = data['pages']
    
    try:
        results = image_retrieval.search_product_by_keyword(image_uuid, keyword, no_of_pages)  # uuid is the filename without the extension
        return results
    except Exception as e:
        return jsonify(error=f"Error searching product: {str(e)}"), 500


@api.route('/hybrid_classification/<image_uuid>', methods=['POST'])
def hybrid_classification(image_uuid):
    """
    Perform a hybrid classification using YOLO and ResNet
    ---
    tags:
      - Hybrid Classification
    parameters:
      - in: path
        name: image_uuid
        type: string
        required: true
        description: The unique identifier for the uploaded image.
    responses:
      200:
        description: Hybrid classification results using YOLO and ResNet
        schema:
          type: array
          items:
            type: object
            properties:
              class_name:
                type: string
                description: Name of the identified object
              confidence:
                type: number
                format: float
                description: Confidence score for the identified object
              source:
                type: string
                description: Source of classification (YOLO or ResNet)
      404:
        description: Image not found for the provided UUID
        schema:
          type: object
          properties:
            error:
              type: string
              description: Error message
      500:
        description: Unexpected error
        schema:
          type: object
          properties:
            error:
              type: string
              description: Error message
    """
    file_paths = glob.glob(os.path.join(UPLOADED, f"{image_uuid}.*"))
    if not file_paths:
        return jsonify(error="Image not found for the provided UUID."), 404
    file_path = file_paths[0]  # Since UUID is unique, there should be only one match

    try:
        yolo_results = yolo_classification.classify_objects_with_yolo(file_path)
        resnet_results = resnet_classification.classify_objects_with_resnet(file_path)

        yolo_classifications = yolo_results['classifications']
        
        resnet_classifications = [r for r in resnet_results['classifications'] if float(r["confidence"].strip('%')) > 40]

        ensemble_results = []

        for result in yolo_classifications:
            result["source"] = "YOLO"
            ensemble_results.append(result)

        for result in resnet_classifications:
            result["source"] = "ResNet"
            ensemble_results.append(result)

        return jsonify(classifications=ensemble_results), 200
    except Exception as e:
        return jsonify(error=f"Error processing image: {str(e)}"), 500



@api.route('/retrieve_similar_images/<image_uuid>', methods=['POST'])
def retrieve_similar_images(image_uuid):
    """
    Retrieve images similar to the provided image UUID based on a specified algorithm
    ---
    tags:
      - Image Retrieval
    parameters:
      - in: path
        name: image_uuid
        type: string
        required: true
        description: The unique identifier for the uploaded image.
      - in: body
        name: body
        required: true
        description: The algorithm type to be used for similarity check.
        schema:
          type: object
          properties:
            algo:
              type: string
              description: The algorithm to use for similarity check, e.g., euclidean.
              required: true
    responses:
      200:
        description: Similarity results based on the algorithm
        schema:
          type: array
          items:
            type: object
            properties:
              # You might need to adjust these properties based on the actual structure of your similar_images response
              image:
                type: string
                description: Path or identifier of the similar image
              similarity_score:
                type: number
                format: float
                description: Similarity score based on the provided algorithm
      400:
        description: Algorithm not provided in the request
        schema:
          type: object
          properties:
            error:
              type: string
              description: Error message
      500:
        description: Unexpected error during processing
        schema:
          type: object
          properties:
            error:
              type: string
              description: Error message
    """
    data = request.get_json()
    if not data or 'algo' not in data:
        return jsonify(error="Algorithm is required, like euclidean."), 400
    
    algo = data['algo']
    similar_images = image_retrieval.retrieve_similar_images(image_uuid, UPLOADED, DOWNLOADED, algo)
    return jsonify(similar_images)


