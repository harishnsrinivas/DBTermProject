# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('mobile', models.CharField(max_length=10)),
                ('telephone', models.CharField(max_length=10)),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('money', models.DecimalField(max_digits=10, decimal_places=3)),
                ('oil', models.DecimalField(max_digits=10, decimal_places=3)),
            ],
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('street', models.CharField(max_length=100)),
                ('zipcode', models.CharField(max_length=5)),
                ('city', models.CharField(max_length=50)),
                ('state', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Oil',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('current_unit_price', models.DecimalField(max_digits=10, decimal_places=3)),
            ],
        ),
        migrations.CreateModel(
            name='Rating',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('level', models.SmallIntegerField(choices=[(b'Silver', 0), (b'Gold', 1)])),
                ('commission_rate_cash', models.IntegerField()),
                ('commission_rate_oil', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Trader',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('tn_type', models.IntegerField(choices=[(b'Buy', 0), (b'Buy', 1)])),
                ('oil_barrel', models.DecimalField(max_digits=10, decimal_places=3)),
                ('oil_unit_rate', models.DecimalField(max_digits=10, decimal_places=3)),
                ('tn_cost', models.DecimalField(max_digits=10, decimal_places=3)),
                ('date', models.DateTimeField(default=datetime.datetime(2015, 11, 14, 21, 24, 52, 34625))),
                ('status', models.IntegerField(choices=[(b'Success', 1), (b'Reject', 0)])),
                ('comm_type', models.IntegerField(choices=[(b'Cash', 0), (b'Oil', 1)])),
                ('comm_value', models.DecimalField(max_digits=10, decimal_places=3)),
                ('client', models.ForeignKey(to='otsapp.Client')),
                ('trader', models.ForeignKey(to='otsapp.Trader')),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('user_type', models.IntegerField(choices=[(b'Client', 0), (b'Trader', 1)])),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='trader',
            name='user_profile',
            field=models.ForeignKey(to='otsapp.UserProfile'),
        ),
        migrations.AddField(
            model_name='client',
            name='location',
            field=models.ForeignKey(to='otsapp.Location'),
        ),
        migrations.AddField(
            model_name='client',
            name='rating',
            field=models.ForeignKey(to='otsapp.Rating'),
        ),
        migrations.AddField(
            model_name='client',
            name='user_profile',
            field=models.ForeignKey(to='otsapp.UserProfile'),
        ),
    ]
