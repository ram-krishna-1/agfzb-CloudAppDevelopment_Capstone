from django.db import models
from django.utils.timezone import now


# Create your models here.

# <HINT> Create a Car Make model `class CarMake(models.Model)`:
# - Name
# - Description
# - Any other fields you would like to include in car make model
# - __str__ method to print a car make object
class CarMake(models.Model):
    name = models.CharField(null = False, max_length = 60)
    description = models.TextField()
    def __str__(self):
        return "Name: " + self.name + " Description: " + self.description

# <HINT> Create a Car Model model `class CarModel(models.Model):`:
# - Many-To-One relationship to Car Make model (One Car Make has many Car Models, using ForeignKey field)
# - Name
# - Dealer id, used to refer a dealer created in cloudant database
# - Type (CharField with a choices argument to provide limited choices such as Sedan, SUV, WAGON, etc.)
# - Year (DateField)
# - Any other fields you would like to include in car model
# - __str__ method to print a car make object
class CarModel(models.Model):
    id = models.AutoField(primary_key=True)
    make = models.ForeignKey(CarMake, on_delete=models.CASCADE)
    dealer_id = models.IntegerField(null=False)
    name = models.CharField(null=False, max_length=50)
    year = models.DateField()

    SUV = 'SUV'
    SEDAN = 'Sedan'
    WAGON = 'WAGON'
    TYPES = [
        (SUV, 'suv'),
        (SEDAN, 'sedan'),
        (WAGON, 'wagon'),
    ]

    type = models.CharField(
        null=False,
        max_length=20,
        choices=TYPES,
        default=SEDAN
    )

    def __str__(self):
        return self.make.name + " " + \
               self.name + ", " + \
               str(self.year.year) + "(" + \
               "DealerID: " + str(self.dealer_id) + ")"
# <HINT> Create a plain Python class `CarDealer` to hold dealer data
class CarDealer:

    def __init__(self, address, city, full_name, id, lat, long, short_name, st, zip):
        # Dealer address
        self.address = address
        # Dealer city
        self.city = city
        # Dealer Full Name
        self.full_name = full_name
        # Dealer id
        self.id = id
        # Location lat
        self.lat = lat
        # Location long
        self.long = long
        # Dealer short name
        self.short_name = short_name
        # Dealer state
        self.st = st
        # Dealer zip
        self.zip = zip

    def __str__(self):
        return "Dealer name: " + self.full_name

# <HINT> Create a plain Python class `DealerReview` to hold review data
class DealerReview(object):
    def __init__(self, dealership=None, name=None, purchase=None, review=None, purchase_date=None, car_make=None, car_model=None, car_year=None):
        self.car_make = car_make
        self.car_model = car_model
        self.car_year = car_year
        self.id = id
        self.dealership = dealership
        self.name = name
        self.purchase = purchase
        self.purchase_date = purchase_date
        self.review = review
        self.sentiment = None
    
    def __str__(self):
        return "Review: " + self.review + ", Sentiment: " + self.sentiment
