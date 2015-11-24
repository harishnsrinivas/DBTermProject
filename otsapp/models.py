from django.db import models
from django.contrib.auth.models import User

from datetime import datetime


class UserProfile(models.Model):

    CLIENT = 0
    TRADER = 1
    MANAGER = 2

    USER_TYPES = (
        ("Client", CLIENT),
        ("Trader", TRADER)
    )

    user_type = models.IntegerField(choices=USER_TYPES)
    user = models.ForeignKey(User)


class Rating(models.Model):
    LEVEL_SILVER = 0
    LEVEL_GOLD = 1

    RATING_LEVELS = (
        ("Silver", LEVEL_SILVER),
        ("Gold", LEVEL_GOLD),
    )

    level = models.SmallIntegerField(choices=RATING_LEVELS)
    commission_rate_cash = models.IntegerField()
    commission_rate_oil = models.IntegerField()


class Location(models.Model):
    street = models.CharField(max_length=100)
    zipcode = models.CharField(max_length=5)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)


class Client(models.Model):
    user_profile = models.ForeignKey(UserProfile)
    mobile = models.CharField(max_length=10)
    telephone = models.CharField(max_length=10)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    money = models.DecimalField(max_digits=10, decimal_places=3)
    oil = models.DecimalField(max_digits=10, decimal_places=3)
    rating = models.ForeignKey(Rating)
    location = models.ForeignKey(Location)


class Trader(models.Model):
    user_profile = models.ForeignKey(UserProfile)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)


class Oil(models.Model):
    current_unit_price = models.DecimalField(max_digits=10, decimal_places=3)


class Transaction(models.Model):
    BUY = 0
    SELL = 1
    TN_TYPES = (
        ("Buy", BUY),
        ("Buy", SELL),
    )

    STATUS_REJECT = 0
    STATUS_SUCCESS = 1
    STATUS_OPTIONS = (
        ("Success", STATUS_SUCCESS),
        ("Reject", STATUS_REJECT)
    )

    COMM_CASH = 0
    COMM_OIL = 1
    COMMISSION_TYPES = (
        ("Cash", COMM_CASH),
        ("Oil", COMM_OIL)
    )

    client = models.ForeignKey(Client)
    trader = models.ForeignKey(Trader)
    tn_type = models.IntegerField(choices=TN_TYPES)
    oil_barrel = models.DecimalField(max_digits=10, decimal_places=3)
    oil_unit_rate = models.DecimalField(max_digits=10, decimal_places=3)
    tn_cost = models.DecimalField(max_digits=10, decimal_places=3)
    date = models.DateTimeField(default=datetime.utcnow())
    modified_datetime = models.DateTimeField(default=None)
    status = models.IntegerField(choices=STATUS_OPTIONS)
    comm_type = models.IntegerField(choices=COMMISSION_TYPES)
    comm_value = models.DecimalField(max_digits=10, decimal_places=3)
