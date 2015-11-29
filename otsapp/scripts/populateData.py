import django
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(os.path.curdir))))
os.environ['DJANGO_SETTINGS_MODULE'] = 'OTS.settings'
django.setup()

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
    Rating.objects.create(level=0, commission_rate_cash=10, commission_rate_oil=5);
    Rating.objects.create(level=1, commission_rate_cash=5, commission_rate_oil=2);

    # Populating oil data
    Oil.objects.create(current_unit_price=3.78)

    # Populating data for location
    Location.objects.create(street="231 mccallum blvd", zipcode="75252", city="Dallas", state="Texas")
    Location.objects.create(street="532 mccallum blvd", zipcode="67205", city="Wichita", state="Kansas")
    Location.objects.create(street="2454 mccallum blvd", zipcode="76071", city="Newark", state="New Jersey")
    Location.objects.create(street="23461 mccallum blvd", zipcode="11218", city="Brooklyn", state="New York")

     # populating data for trader
    Trader.objects.create(user_profile=UserProfile.objects.get(user__username="trader1"))
    Trader.objects.create(user_profile=UserProfile.objects.get(user__username="trader2"))
    Trader.objects.create(user_profile=UserProfile.objects.get(user__username="trader3"))
    Trader.objects.create(user_profile=UserProfile.objects.get(user__username="trader4"))

    # populating data for client
    Client.objects.create(user_profile=UserProfile.objects.get(user__username="chandni"), mobile="4697768542", telephone="9724467318", money=500.000,
                          oil=50, rating=Rating.objects.get(level=0), location=Location.objects.get(zipcode="75252"))
    Client.objects.create(user_profile=UserProfile.objects.get(user__username="gitanjali"), mobile="9136781547", telephone="7858864392", money=300.000,
                          oil=40, rating=Rating.objects.get(level=0), location=Location.objects.get(zipcode="67205"))
    Client.objects.create(user_profile=UserProfile.objects.get(user__username="srija"), mobile="8629683617", telephone="9739982651", money=450.000,
                          oil=70, rating=Rating.objects.get(level=0), location=Location.objects.get(zipcode="76071"))
    Client.objects.create(user_profile=UserProfile.objects.get(user__username="harish"), mobile="2124436717", telephone="7180764831", money=700.000,
                          oil=90, rating=Rating.objects.get(level=0), location=Location.objects.get(zipcode="11218"))

    # populating data for manager
    Manager.objects.create(user_profile=UserProfile.objects.get(user__username="manager"))

if __name__== "__main__":
    populateData()
