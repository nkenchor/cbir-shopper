import requests
# from decouple import config

RAPIDAPI_ENDPOINT = 'https://real-time-amazon-data.p.rapidapi.com/search'
RAPIDAPI_KEY = '91df5b2adcmshb34854cbb25b789p1d5d11jsn6d4b6bc13b42'
RAPIDAPI_HOST = 'real-time-amazon-data.p.rapidapi.com'
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

def fetch_amazon_data_by_keyword(keyword, number_of_pages=10, country="GB", category_id="aps"):
    all_results = []  # List to store results from all pages

    headers = {
        "X-RapidAPI-Key": RAPIDAPI_KEY,
        "X-RapidAPI-Host": RAPIDAPI_HOST
    }

    for page_number in range(1, number_of_pages + 1):
        querystring = {
            "query": keyword,
            "page": str(page_number),  # Convert page number to string
            "country": country,
            "category_id": category_id
        }

        response = requests.get(RAPIDAPI_ENDPOINT, headers=headers, params=querystring)
        
        if response.status_code == 200:
            all_results.extend(response.json())
        else:
            # Optionally, handle failed requests or break out of the loop. 
            # This decision depends on your specific needs.
            pass

    return all_results
