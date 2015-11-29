# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('otsapp', '0004_auto_20151126_0007'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='user_profile',
            field=models.ForeignKey(related_name='user_profile', to='otsapp.UserProfile'),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2015, 11, 28, 0, 58, 40, 89427)),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='modified_datetime',
            field=models.DateTimeField(default=None, null=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='user',
            field=models.ForeignKey(related_name='user', to=settings.AUTH_USER_MODEL),
        ),
    ]
