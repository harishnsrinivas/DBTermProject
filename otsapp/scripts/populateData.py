import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(os.path.curdir))))
os.environ['DJANGO_SETTINGS_MODULE'] = 'OTS.settings'


from django.db import models
from django.contrib.auth.models import User

from otsapp.models import UserProfile, Location, Rating,\
    Client, Trader, Manager, Oil


def populateData():

    # Populating data for user objects

    User.objects.create_user(username="chandni", first_name="Chandni",
                        last_name="Shankar", password="123456")
    User.objects.create_user(username="gitanjali", first_name="Gitanjali",
                        last_name="Hoige", password="123456")
    User.objects.create_user(username="srija", first_name="Srija",
                        last_name="Temburni", password="123456")
    User.objects.create_user(username="harish", first_name="Harish",
                        last_name="Srinivas", password="123456")


    User.objects.create_user(username="trader1", first_name="Trader1",
                        last_name="Trader1", password="123456")
    User.objects.create_user(username="trader2", first_name="Trader2",
                        last_name="Trader2", password="123456")
    User.objects.create_user(username="trader3", first_name="Trader3",
                        last_name="Trader3", password="123456")
    User.objects.create_user(username="trader4", first_name="Trader4",
                        last_name="Trader4", password="123456")
    User.objects.create_user(username="manager", first_name="Manager",
                        last_name="Manager", password="123456")
    
    # Populating data for user profile entries

    UserProfile.objects.create(user_type=0, user=User.objects.get(username="chandni"))
    UserProfile.objects.create(user_type=0, user=User.objects.get(username="gitanjali"))
    UserProfile.objects.create(user_type=0, user=User.objects.get(username="srija"))
    UserProfile.objects.create(user_type=0, user=User.objects.get(username="harish"))
    UserProfile.objects.create(user_type=1, user=User.objects.get(username="trader1"))
    UserProfile.objects.create(user_type=1, user=User.objects.get(username="trader2"))
    UserProfile.objects.create(user_type=1, user=User.objects.get(username="trader3"))
    UserProfile.objects.create(user_type=1, user=User.objects.get(username="trader4"))
    UserProfile.objects.create(user_type=2, user=User.objects.get(username="manager"))

    # Populating data for rating
    Rating.objects.create(level=0, commission_rate_cash=5, commission_rate_oil=2);
    Rating.objects.create(level=1, commission_rate_cash=10, commission_rate_oil=5);

    # Populating oil data
    Oil.objects.create(current_unit_price=3.78)

    # Populating data for location
    Location.objects.create(street="231 mccallum blvd", zipcode="75252", city="Dallas", state="Texas")
    Location.objects.create(street="532 mccallum blvd", zipcode="67205", city="Wichita", state="Kansas")
    Location.objects.create(street="2454 mccallum blvd", zipcode="76071", city="Newark", state="New Jersey")
    Location.objects.create(street="23461 mccallum blvd", zipcode="11218", city="Brooklyn", state="New York")


if __name__== "__main__":
    populateData()