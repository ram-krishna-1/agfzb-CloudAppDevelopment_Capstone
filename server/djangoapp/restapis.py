import requests
import json
from .models import CarDealer, DealerReview
from requests.auth import HTTPBasicAuth


# Create a `get_request` to make HTTP GET requests
# e.g., response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
#                                     auth=HTTPBasicAuth('apikey', api_key))
def get_request(url, api_key=None, **kwargs):
    print(kwargs)
    print("GET from {} ".format(url))
    try:
        # Call get method of requests library with URL and parameters
        if api_key:
            # Basic authentication GET
            response = requests.get(url, params=kwargs, headers={'Content-Type': 'application/json'},
                                    auth=HTTPBasicAuth('apikey', api_key))
        else:
            # no authentication GET
            response = requests.get(url, params=kwargs, headers={'Content-Type': 'application/json'})
    except:
        # If any error occurs
        print("Network exception occurred")
    print(response.content)
    status_code = response.status_code
    print("With status {} ".format(status_code))
    json_data = json.loads(response.text)
    return json_data

# Create a `post_request` to make HTTP POST requests
# e.g., response = requests.post(url, params=kwargs, json=payload)
def post_request(url, json_payload, **kwargs):
    response = requests.post(url, headers={'Content-Type': 'application/json'},
                                json=json_payload, params=kwargs)
    json_data = json.loads(response.text)
    return json_data

# Create a get_dealers_from_cf method to get dealers from a cloud function
# def get_dealers_from_cf(url, **kwargs):
# - Call get_request() with specified arguments
# - Parse JSON results into a CarDealer object list
def get_dealers_from_cf(url, **kwargs):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url)
    if json_result:
        # Get the row list in JSON as dealers
        dealers = json_result["docs"]
        # For each dealer object
        for dealer in dealers:
            # Get its content in `doc` object
            # Create a CarDealer object with values in `doc` object
            dealer_obj = CarDealer(address=dealer["address"], city=dealer["city"], full_name=dealer["full_name"],
                                   id=dealer["id"], lat=dealer["lat"], long=dealer["long"],
                                   short_name=dealer["short_name"],
                                   st=dealer["st"], zip=dealer["zip"])
            results.append(dealer_obj)
    return results

# Create a get_dealer_reviews_from_cf method to get reviews by dealer id from a cloud function
# def get_dealer_by_id_from_cf(url, dealerId):
# - Call get_request() with specified arguments
# - Parse JSON results into a DealerView object list
def get_dealer_reviews_from_cf(url, dealerId):
    results = []
    json_result = get_request(url, dealerId = dealerId)
    if json_result:
        reviews = json_result["docs"]
        for review_s in reviews:
            if ((hasattr(review_s, "car_make") and hasattr(review_s, "car_model")) and (hasattr(review_s, "car_year") and hasattr(review_s, "purchase_date"))):
                    review_obj = DealerReview(car_make=review_s['car_make'], car_model=review_s['car_model'], 
                    car_year=review_s['car_year'], id=review_s['id'], dealership=review_s['dealership'], 
                    name=review_s['name'], purchase=review_s['purchase'], purchase_date=review_s['purchase_date'], 
                    review=review_s['review'], sentiment="")
            else:
                review_obj = DealerReview(car_make=" ", car_model=" ", 
                car_year=" ", id=review_s['id'], dealership=review_s['dealership'], 
                name=review_s['name'], purchase=review_s['purchase'], purchase_date=" ", 
                review=review_s['review'], sentiment="")
            review_obj.sentiment = analyze_review_sentiments(review_obj.review)
            results.append(review_obj)
            
    return results
# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
# def analyze_review_sentiments(text):
# - Call get_request() with specified arguments
# - Get the returned sentiment label such as Positive or Negative
def analyze_review_sentiments(text):
    url = "https://api.us-south.natural-language-understanding.watson.cloud.ibm.com/instances/4bfdb9c2-53cf-424d-b139-abb85dc9f88b"
    api_key = "4EwlFUVv7C2gkPYoFPZOnmYsW-yoDOWf4BGYxe2SAsTP"
    params = dict()
    params["text"] = text
    params["version"] = "2021-03-25"
    params["features"] = {'sentiment': True}
    params["return_analyzed_text"] = True
    return get_request(url, api_key, **params).get("sentiment").get("document").get("label")


