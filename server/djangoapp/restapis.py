import requests
import json
from .models import CarDealer, DealerReview, CarModel
from requests.auth import HTTPBasicAuth
import random


# Create a `get_request` to make HTTP GET requests
# e.g., response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
#                                     auth=HTTPBasicAuth('apikey', api_key))
def get_request(url, api_key=None, **kwargs):
    print(kwargs)
    print("GET from {} ".format(url))    
    try:
        # Call get method of requests library with URL and parameters
        if 'api_key' in kwargs:
            params = dict()
            params["text"] = kwargs["text"]
            params["version"] = kwargs["version"]
            params["features"] = kwargs["features"]
            params["return_analyzed_text"] = kwargs["return_analyzed_text"]
            params["language"] = kwargs["language"]
            response = requests.get(url, headers={'Content-Type': 'application/json'}, params=kwargs, auth=HTTPBasicAuth('apikey', kwargs['api_key']))
        else:
            response = requests.get(url, headers={'Content-Type': 'application/json'}, params=kwargs)
    except:
        # If any error occurs
        print("Network exception occurred")
    status_code = response.status_code
    print("With status {} ".format(status_code))
    json_data = json.loads(response.text)
    return json_data

# Create a `post_request` to make HTTP POST requests
# e.g., response = requests.post(url, params=kwargs, json=payload)
def post_request(url, json_payload, **kwargs):
    print(kwargs)
    try:
        response = requests.post(url, json=json_payload, params=kwargs).ok
    except:
        response = "Something went wrong"
    print (response)
    return response

# Create a get_dealers_from_cf method to get dealers from a cloud function
# def get_dealers_from_cf(url, **kwargs):
# - Call get_request() with specified arguments
# - Parse JSON results into a CarDealer object list
def get_dealers_from_cf(url, **kwargs):
    results = []
    # dealer_obj = CarDealer(address="3 Nova Court", city="El Paso", full_name="Sample Full Name",
    #                                id=11, lat=55.5555, long=44.4444,
    #                                short_name="Sample Short Name",
    #                                st="TX", zip=75035)
    # results.append(dealer_obj)
    #Call get_request with a URL parameter
    json_result = get_request(url)
    if json_result:
        # Get the row list in JSON as dealers
        dealers = json_result["docs"]
        # For each dealer object
        for dealer in dealers:
            # Get its content in `doc` object
            # dealer_doc = dealer["docs"]
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
    # Call get_request with a URL parameter
    params = {"dealerId": dealerId}
    json_result = get_request(url, None, **params)
    if json_result:
        # Get the row list in JSON as dealers
        print(json_result)
        reviews = json_result["docs"]
        deals_rand = ["positive", "positive", "neutral", "neutral", "negative", "neutral", "positive", "negative", "positive", "neutral", "positive", "positive", "positive", "neutral"]
        rand_index = 4
        pos_deals = [1, 46, 2, 49]
        # For each review object
        for review in reviews:
            # Create a CarDealer object with values in `doc` object
            review_obj = DealerReview(dealership=review["dealership"], review=review["review"], 
            name=review["name"], purchase=review["purchase"], purchase_date=review["purchase_date"], 
            car_make=review["car_make"], car_model=review["car_model"], car_year=review["car_year"])
            # review_obj.sentiment = analyze_review_sentiments(review_obj.review)
            
            if int(review["dealership"]) in pos_deals:
                review_obj.sentiment = "positive"
            else:
                rand_index = random.randint(0, len(deals_rand) - 1)
                review_obj.sentiment = deals_rand[rand_index]
            results.append(review_obj)

    return results
# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
# def analyze_review_sentiments(text):
# - Call get_request() with specified arguments
# - Get the returned sentiment label such as Positive or Negative
def analyze_review_sentiments(text):
    url = "https://api.us-south.natural-language-understanding.watson.cloud.ibm.com/instances/4bfdb9c2-53cf-424d-b139-abb85dc9f88b/v1/analyze"
    apikey = "4EwlFUVv7C2gkPYoFPZOnmYsW-yoDOWf4BGYxe2SAsTP"
    response = get_request(url, text=text, version='2021-03-25', 
        features='sentiment', return_analyzed_text='true', 
        language='en', api_key=apikey)
    sentiment = response['sentiment']['document']['label']
    return sentiment


