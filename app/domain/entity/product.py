class Product:
    def __init__(self, 
                 id, 
                 product_title, 
                 product_price, 
                 product_original_price, 
                 currency, 
                 product_star_rating, 
                 product_num_ratings, 
                 product_url, 
                 product_photo, 
                 product_num_offers,
                 product_minimum_offer_price,
                 is_best_seller,
                 is_prime,
                 climate_pledge_friendly):
        
        self.id = id
        self.product_title = product_title
        self.product_price = product_price
        self.product_original_price = product_original_price
        self.currency = currency
        self.product_star_rating = product_star_rating
        self.product_num_ratings = product_num_ratings
        self.product_url = product_url
        self.product_photo = product_photo
        self.product_num_offers = product_num_offers
        self.product_minimum_offer_price = product_minimum_offer_price
        self.is_best_seller = is_best_seller
        self.is_prime = is_prime
        self.climate_pledge_friendly = climate_pledge_friendly
