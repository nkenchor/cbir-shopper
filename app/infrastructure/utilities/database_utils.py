import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE_PATH = os.path.join(BASE_DIR,'../database','cbir.db')



def setup_db():
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    # Create the table if it doesn't exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS products (
            asin TEXT PRIMARY KEY,
            product_title TEXT,
            product_price REAL,
            product_original_price REAL,
            currency TEXT,
            product_star_rating REAL,
            product_num_ratings INTEGER,
            product_url TEXT,
            product_photo TEXT,
            product_num_offers INTEGER,
            product_minimum_offer_price REAL,
            is_best_seller BOOLEAN,
            is_prime BOOLEAN,
            climate_pledge_friendly BOOLEAN
        )
    ''')
    
    conn.commit()
    conn.close()

def save_product_details_to_db(product_data):
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT OR REPLACE INTO products (
            asin, product_title, product_price, product_original_price, currency, 
            product_star_rating, product_num_ratings, product_url, product_photo, 
            product_num_offers, product_minimum_offer_price, is_best_seller, 
            is_prime, climate_pledge_friendly
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        product_data["asin"], product_data["product_title"], product_data["product_price"],
        product_data["product_original_price"], product_data["currency"],
        product_data["product_star_rating"], product_data["product_num_ratings"],
        product_data["product_url"], product_data["product_photo"],
        product_data["product_num_offers"], product_data["product_minimum_offer_price"],
        product_data["is_best_seller"], product_data["is_prime"],
        product_data["climate_pledge_friendly"]
    ))
    
    conn.commit()
    conn.close()

def get_product_details_from_db(asin):
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row  # This allows us to access the rows as dictionaries
    cursor = conn.cursor()

    cursor.execute('''
        SELECT * FROM products WHERE asin = ?
    ''', (asin,))

    # Fetch one record (since asin is a primary key and unique)
    product_data = cursor.fetchone()

    conn.close()

    # Convert the Row object to a dictionary (optional)
    if product_data:
        return dict(product_data)
    else:
        return None
