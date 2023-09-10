import os
from flask import jsonify, request,Blueprint 
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
def hello_world():
    return jsonify(message="Hello, this is my CBIR app"), 200

@api.route('/upload_image', methods=['POST'])
def upload_image():
    uuid, file_path, error, code = image_upload.handle_image_upload()
    if error:
        return error, code
    return jsonify(uuid=uuid, message="Image uploaded successfully."), 200


@api.route('/classify_objects_with_resnet/<image_uuid>', methods=['POST'])
def classify_objects_with_resnet(image_uuid):
   
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
    data = request.get_json()
    if not data or 'keyword' not in data:
        return jsonify(error="Keyword is required."), 400
    
    keyword = data['keyword']
    
    
    try:
        results = image_retrieval.search_product_by_keyword(image_uuid, keyword) #uuid is the filename without the extension
        return results
    except Exception as e:
        return jsonify(error=f"Error searching product: {str(e)}"), 500


@api.route('/hybrid_classification/<image_uuid>', methods=['POST'])
def hybrid_classification(image_uuid):
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
    data = request.get_json()
    if not data or 'algo' not in data:
        return jsonify(error="Algorithm is required, like euclidean."), 400
    
    algo = data['algo']
    similar_images = image_retrieval.retrieve_similar_images(image_uuid, UPLOADED, DOWNLOADED,algo)
    return jsonify(similar_images)

