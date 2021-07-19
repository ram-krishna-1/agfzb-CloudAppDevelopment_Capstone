from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
# from .models import related models
from . import models
# from .restapis import related methods
from . import restapis
from .models import CarModel
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
    # if request.method == "GET":
        context = {}
        url = "https://0c99453f.us-south.apigw.appdomain.cloud/api/dealership"
        # Get dealers from the URL
        dealerships = get_dealers_from_cf(url)
        # dealerships = "Hello Value"
        # Concat all dealer's short name
        context["dealership_list"] = dealerships
        # context["dealership_list"] = "Hello Value"
        # context["hello_key"] = dealerships
        dealer_names = ' '.join([dealer.short_name for dealer in dealerships])
        # Return a list of dealer short name
        return render(request, "djangoapp/index.html", context)
        # return HttpResponse(dealer_names)


# Create a `get_dealer_details` view to render the reviews of a dealer
# def get_dealer_details(request, dealer_id):
# ...
def get_dealer_details(request, dealer_id):
    context = {}
    if request.method == "GET":
        url = "https://0c99453f.us-south.apigw.appdomain.cloud/api/dealership"
        dealership = get_dealers_from_cf(url, id=dealer_id)[0]
        url = "https://0c99453f.us-south.apigw.appdomain.cloud/api/reviews/"
        dealer_reviews = get_dealer_reviews_from_cf(url, dealer_id)
        context["reviews_list"] = dealer_reviews
        context["dealer_id"] = dealer_id
        context["dealer_name"] = dealership.full_name
        return render(request, 'djangoapp/dealer_details.html', context)
# Create a `add_review` view to submit a review
# def add_review(request, dealer_id):
# ...
def add_review(request, dealer_id):
    context = {}
    if request.method == "GET":
        context["dealer_id"] = dealer_id
        context["cars"] = models.CarModel.objects.filter(dealer_id = dealer_id)
        return render(request, 'djangoapp/add_review.html', context)

    if request.method == "POST":
        user = request.user
        if not user.is_authenticated:
            context["error_message"] = "Please login at first"
            context["dealer_id"] = dealer_id
            print("Not logged in!")
            return redirect("/djangoapp/login", context)
        review = {}
        review["id"] = 0
        review["name"] = request.user.first_name + " " + request.user.last_name
        review["dealership"] = dealer_id
        review["review"] = request.POST["review"]
        review["purchase"] = request.POST.get("purchasecheck") == 'on'
        if request.POST.get("purchasecheck") == 'on':
            review["purchase_date"] = request.POST["purchasedate"]
            car_num = request.POST["car"]
            print(car_num)
            car = models.CarModel.objects.get(pk=car_num)
            review["car_make"] = car.make.name
            review["car_model"] = car.name
            review["car_year"]= car.year.strftime("%Y")
        json_payload = {}
        json_payload["review"] = review
        print(json_payload)
        result = restapis.post_request("https://0c99453f.us-south.apigw.appdomain.cloud/api/reviews", json_payload, dealerId=dealer_id)
        print("POST request result: ", result)
        if result == True:
            context["success_message"] = "Review submitted!"
            print("Success")
        else:
            context["error_message"] = "ERROR: Review not submitted."
            print("Failed")
        context["dealer_id"] = dealer_id
        return redirect("/djangoapp/dealer/" + str(dealer_id), context)
