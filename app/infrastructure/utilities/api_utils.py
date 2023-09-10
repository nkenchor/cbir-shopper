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




def fetch_amazon_data_by_keyword(keyword, number_of_pages=10, country="US", category_id="aps"):
    all_results = []  # List to store results from all pages

    headers = {
        "X-RapidAPI-Key": RAPIDAPI_KEY,
        "X-RapidAPI-Host": RAPIDAPI_HOST
    }

    for page_number in range(1, number_of_pages + 1):
        querystring = {
            "query": keyword,
            "page": str(page_number),
            "country": country,
            "category_id": category_id
        }

        try:
            response = requests.request("GET", RAPIDAPI_ENDPOINT, headers=headers, params=querystring)
            response.raise_for_status()  # will raise an HTTPError if the HTTP request returned an unsuccessful status code

            response_json = response.json()

            # If there's an error key in the response, handle it
            if 'error' in response_json:
                error_message = response_json['error']
                print(f"API Error on page {page_number}: {error_message}")
                if "Invalid URL 'None'" in error_message:
                    print("Detected absence of more pages. Terminating the fetch.")
                    break

            # Ensure 'data' and 'products' keys exist in response JSON
            elif 'data' in response_json and 'products' in response_json['data']:
                products = response_json['data']['products']

                if not products:  # if products list is empty, break out of loop
                    print(f"No more products found at page {page_number}. Stopping the fetch.")
                    break

                all_results.extend(products)

        except requests.HTTPError as http_err:
            print(f"HTTP error occurred on page {page_number}: {http_err}")
            # Added this to break out of the loop when an HTTP error occurs
            break
        except Exception as err:
            print(f"An error occurred on page {page_number}: {err}")
            break

    return all_results
