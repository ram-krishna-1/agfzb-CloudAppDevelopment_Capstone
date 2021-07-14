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
    make = models.ForeignKey(CarMake, on_delete = models.CASCADE)
    name = models.CharField(null = False, max_length = 60)
    dealer_id = models.IntegerField(null = False)
    year = models.DateField()

    SUV = "suv"
    SEDAN = "sedan"
    WAGON = "wagon"
    Car_Types = [
        (SEDAN, "Sedan"),
        (SUV, "SUV"),
        (WAGON, "Wagon")
    ]
    type = models.CharField(null = False, max_length = 30, choices = Car_Types, default = SEDAN)
    def __str__(self):
        return 'Name: ' + self.name + ' dealer id: ' + str(self.dealer_id) + ' type: ' + self.type + ' year: ' + str(self.year)
# <HINT> Create a plain Python class `CarDealer` to hold dealer data


# <HINT> Create a plain Python class `DealerReview` to hold review data
