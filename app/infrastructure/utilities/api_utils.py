import requests
from decouple import config

RAPIDAPI_ENDPOINT = config('RAPIDAPI_ENDPOINT')
RAPIDAPI_KEY = config('RAPIDAPI_KEY')
RAPIDAPI_HOST = config('RAPIDAPI_HOST')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def fetch_amazon_data_from_api(image):
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'x-rapidapi-host': RAPIDAPI_HOST,
        'x-rapidapi-key': RAPIDAPI_KEY
    }
    
    response = requests.post(RAPIDAPI_ENDPOINT, headers=headers, data={'image': image})
    
    if response.status_code == 200:
        return response.json()
    else:
        return None

def fetch_amazon_data_by_keyword(keyword, page="10", country="GB", category_id="aps"):
    querystring = {
        "query": keyword,
        "page": page,
        "country": country,
        "category_id": category_id
    }
    
    headers = {
        "X-RapidAPI-Key": RAPIDAPI_KEY,
        "X-RapidAPI-Host": RAPIDAPI_HOST
    }

    response = requests.get(RAPIDAPI_ENDPOINT, headers=headers, params=querystring)
    
    if response.status_code == 200:
        return response.json()
    else:
        return None