# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('otsapp', '0003_auto_20151125_1818'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='client',
            name='first_name',
        ),
        migrations.RemoveField(
            model_name='client',
            name='last_name',
        ),
        migrations.RemoveField(
            model_name='manager',
            name='first_name',
        ),
        migrations.RemoveField(
            model_name='manager',
            name='last_name',
        ),
        migrations.RemoveField(
            model_name='trader',
            name='first_name',
        ),
        migrations.RemoveField(
            model_name='trader',
            name='last_name',
        ),
        migrations.AlterField(
            model_name='transaction',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2015, 11, 26, 0, 7, 57, 628785)),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='user_type',
            field=models.IntegerField(choices=[(b'Client', 0), (b'Trader', 1), (b'Manager', 2)]),
        ),
    ]
