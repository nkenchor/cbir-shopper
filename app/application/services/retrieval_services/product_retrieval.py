from app.infrastructure.repositories import product_repository

def get_product_by_image(image):
    return product_repository.find_by_image(image)

def search_product_by_keyword(keyword):
    return product_repository.find_by_keyword(keyword)