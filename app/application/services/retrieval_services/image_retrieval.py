import os
import numpy as np
import requests
import os
import glob
from app.application.services.resnet_services import feature_extraction_with_resnet as feature_extraction
from flask import jsonify
from app.application.services.retrieval_services import product_retrieval
from app.infrastructure.utilities import database_utils as db 
# Define a directory to store downloaded images
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DOWNLOADED = os.path.join(BASE_DIR, '../../../../images','downloaded')


def download_image(url, filename):
    """Downloads an image from a URL and saves it with the given filename."""
    response = requests.get(url)
    if response.status_code == 200:
        with open(os.path.join(DOWNLOADED, filename), 'wb') as file:
            for chunk in response.iter_content(1024):
                file.write(chunk)
    else:
        # Handle failure, e.g., log the error or raise an exception
        pass

def search_product_by_keyword(filename,keyword):
    if not keyword:
        return jsonify(error="Keyword is required."), 400
    
    products = product_retrieval.search_product_by_keyword(keyword)

    if products:
        products_response = []
        for product in products:
            # Download the image
            image_filename = f"{filename}.{product.id}.jpg"  # assuming images are in JPG format
            download_image(product.product_photo, image_filename)
            
            # Construct the product data with the local image path
            product_data = {
                "asin": product.id,
                "product_title": product.product_title,
                "product_price": product.product_price,
                "product_original_price": product.product_original_price,
                "currency": product.currency,
                "product_star_rating": product.product_star_rating,
                "product_num_ratings": product.product_num_ratings,
                "product_url": product.product_url,
                "product_photo": os.path.join(DOWNLOADED, image_filename),  # Update to local path
                "product_num_offers": product.product_num_offers,
                "product_minimum_offer_price": product.product_minimum_offer_price,
                "is_best_seller": product.is_best_seller,
                "is_prime": product.is_prime,
                "climate_pledge_friendly": product.climate_pledge_friendly
            }
            
            db.save_product_details_to_db(product_data)  # Save the product to the database
            products_response.append(product_data)

        return jsonify(products_response), 200
    else:
        return jsonify(error="No products found."), 404



def retrieve_similar_images(image_uuid, uploaded_dir, downloaded_dir, metric="euclidean"):
    uploaded_image_path = os.path.join(uploaded_dir, f"{image_uuid}.*")
    uploaded_image_path = glob.glob(uploaded_image_path)[0]
    uploaded_image_features = feature_extraction.extract_features(uploaded_image_path)
    
    image_scores = {}
    image_similarities = {}  # To store similarity scores
    relevant_images = [img for img in os.listdir(downloaded_dir) if img.startswith(image_uuid) and img.endswith((".jpg", ".jpeg", ".png"))]
    
    for image_file in relevant_images:
        current_image_path = os.path.join(downloaded_dir, image_file)
        current_image_features = feature_extraction.extract_features(current_image_path)
        
        if metric == "euclidean":
            distance = feature_extraction.euclidean_distance(uploaded_image_features, current_image_features)
    
        elif metric == "cosine":
            distance = 1 - feature_extraction.cosine_similarity(uploaded_image_features, current_image_features)  # converting similarity to distance
            
        elif metric == "manhattan":
            distance = feature_extraction.manhattan_distance(uploaded_image_features, current_image_features)

        elif metric == "minkowski":
            p_value = 3  # or whatever value you want for p
            distance = feature_extraction.minkowski_distance(uploaded_image_features, current_image_features, p=p_value)
            
        elif metric == "mahalanobis":
            inv_cov_matrix = ...  # You'll need to determine this ahead of time.
            distance = feature_extraction.mahalanobis_distance(uploaded_image_features, current_image_features, inv_cov_matrix)
            
        elif metric == "hamming":
            distance = feature_extraction.hamming_distance(uploaded_image_features, current_image_features)
            
        elif metric == "chi_square":
            distance = feature_extraction.chi_square_distance(uploaded_image_features, current_image_features)

        elif metric == "histogram_intersection":
            distance = 1 - feature_extraction.histogram_intersection(uploaded_image_features, current_image_features)  # converting similarity to distance

        else:
            raise ValueError(f"Unsupported metric: {metric}")
 
        
        similarity_score = np.exp(-distance) * 100  # Exponential transformation to get similarity score
        # image_scores[image_file] = distance
        image_similarities[image_file] = similarity_score

   # Sort images based on similarity scores (descending because higher score means more similarity)
    sorted_images = sorted(image_similarities.keys(), key=lambda x: image_similarities[x], reverse=True)
    
    # Retrieve product details for the top 10 similar images
    top_products = []
    for img_file in sorted_images[:10]:
        # Extract the ASIN from the filename format
        asin = os.path.splitext(img_file)[0].split(".")[-1]
        product_data = db.get_product_details_from_db(asin)
        if product_data:  # Checking if data exists
            product_data['similarity_score'] = float(image_similarities[img_file])  # Add the similarity score to the product data
            top_products.append(product_data)
    
    # Sort top_products by similarity_score
    top_products = sorted(top_products, key=lambda x: x['similarity_score'], reverse=True)
    
    return top_products  # Return top 10 similar products' details

