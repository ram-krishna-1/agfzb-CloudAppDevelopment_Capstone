from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
# from .models import related models
from .restapis import get_dealers_from_cf, get_dealer_reviews_from_cf, post_request
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json

# Create your views here.

# Create an `about` view to render a static about page
def about(request):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/about.html', context)

# Create a `contact` view to return a static contact page
def contact(request):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/contact.html', context)

# Create a `login_request` view to handle sign in request
# def login_request(request):
def login_request(request):
    context = {}
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return render(request, 'djangoapp/index.html', context)
        else:
            return render(request, 'djangoapp/index.html', context)
    else:
        return render(request, 'djangoapp/index.html', context)

# Create a `logout_request` view to handle sign out request
# def logout_request(request):
def logout_request(request):
    context = {}
    logout(request)
    return render(request, 'djangoapp/index.html', context)

# Create a `registration_request` view to handle sign up request
# def registration_request(request):
def registration_request(request):
    context = {}
    if request.method == 'GET':
        return render(request, 'djangoapp/registration.html', context)
    elif request.method == 'POST':
        # Get user information from request.POST
        username = request.POST['username']
        password = request.POST['password']
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        user_exist = False
        try:
            User.objects.get(username=username)
            user_exist = True
        except:
            pass
        if not user_exist:
            user = User.objects.create_user(username=username, 
                                            first_name=first_name, 
                                            last_name=last_name,
                                            password=password)
            login(request, user)
            return render(request, 'djangoapp/index.html', context)
        else:
            return render(request, 'djangoapp/index.html', context)

# Update the `get_dealerships` view to render the index page with a list of dealerships
def get_dealerships(request):
    if request.method == "GET":
        context = {}
        url = "https://0c99453f.us-south.apigw.appdomain.cloud/api/dealership"
        # Get dealers from the URL
        dealerships = get_dealers_from_cf(url)
        # Concat all dealer's short name
        context["dealer_list"] = dealerships
        # Return a list of dealer short name
        return render(request, "djangoapp/index.html", context)


# Create a `get_dealer_details` view to render the reviews of a dealer
# def get_dealer_details(request, dealer_id):
# ...
def get_dealer_details(request, dealer_id):
    context = {}
    if request.method == "GET":
        url = "https://0c99453f.us-south.apigw.appdomain.cloud/api/reviews/"
        reviews = get_dealer_reviews_from_cf(url, dealer_id)
        context["review_list"] = reviews
        context["dealer_id"] = dealer_id
# Create a `add_review` view to submit a review
# def add_review(request, dealer_id):
# ...
def add_review(request, dealer_id):
    context = {}
    if request.method =="GET":
        context["dealer_id"] = dealer_id
        return render(request, "/djangoapp/add_review.html", context)
    else:
        if request.user.is_authenticated:
            url = "https://0c99453f.us-south.apigw.appdomain.cloud/api/reviews/"
            review = {}
            review["id"] = random.randInt(12, 1111111)
            review["name"] = request.user.username
            review["dealership"] =  dealer_id
            review["review"] = request.POST["review"]
            if request.POST["purchasecheck"]:
                review["purchase"] = True
                review["purchase_date"] = request.POST["purchasedate"]
            else:
                review["purchase"] = False
            car = CarModel.objects.get(id=int(request.POST['car']))
            review['car_make'] = car.make.name
            review['car_model'] = car.name
            review['car_year'] = car.year
            json_payload = dict()
            json_payload["review"] = review
            json_result = post_request(url, json_payload, dealerId = dealer_id)
            print(json_result)
            return render(request, "djangoapp/add_review.html", context)
        else:
            context["error_message"] = "Unauthorized user. Please Register or Login."
            context["dealer_id"] = dealer_id
            return render(request, "djangoapp/registration.html", context)
