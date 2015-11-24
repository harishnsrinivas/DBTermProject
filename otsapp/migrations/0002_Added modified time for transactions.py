# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('otsapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='modified_datetime',
            field=models.DateTimeField(default=None),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2015, 11, 14, 22, 13, 47, 957248)),
        ),
    ]
