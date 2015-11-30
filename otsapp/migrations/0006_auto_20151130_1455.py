# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('otsapp', '0005_changes to rating entries and schema change for transaction table'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2015, 11, 30, 14, 55, 44, 944627)),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='status',
            field=models.IntegerField(choices=[(b'Approved', 1), (b'Canceled', 0), (b'Pending', 2)]),
        ),
    ]
