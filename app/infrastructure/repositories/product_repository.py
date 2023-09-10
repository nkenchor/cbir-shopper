from app.infrastructure.utilities import api_utils
from app.domain.entity import product
def find_by_image(image):
    data = api_utils.fetch_amazon_data_from_api(image)
    if data:
        return product.Product(
            id=data["id"],
            name=data["name"],
            description=data["description"],
            image_url=data["image_url"]
        )
    return None

def find_by_keyword(keyword):
    response_data = api_utils.fetch_amazon_data_by_keyword(keyword)
    products = []
    
    if response_data and response_data.get('status') == 'OK':
        for product_data in response_data['data'].get('products', []):
            product_instance = product.Product(
                id=product_data.get("asin"),
                product_title=product_data.get("product_title"),
                product_price=product_data.get("product_price"),
                product_original_price=product_data.get("product_original_price"),
                currency=product_data.get("currency"),
                product_star_rating=product_data.get("product_star_rating"),
                product_num_ratings=product_data.get("product_num_ratings"),
                product_url=product_data.get("product_url"),
                product_photo=product_data.get("product_photo"),
                product_num_offers=product_data.get("product_num_offers"),
                product_minimum_offer_price=product_data.get("product_minimum_offer_price"),
                is_best_seller=product_data.get("is_best_seller"),
                is_prime=product_data.get("is_prime"),
                climate_pledge_friendly=product_data.get("climate_pledge_friendly")
            )
            products.append(product_instance)
    
    return products


