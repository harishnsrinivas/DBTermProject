# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('otsapp', '0002_Added modified time for transactions'),
    ]

    operations = [
        migrations.CreateModel(
            name='Manager',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('user_profile', models.ForeignKey(to='otsapp.UserProfile')),
            ],
        ),
        migrations.AlterField(
            model_name='transaction',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2015, 11, 25, 18, 18, 46, 637603)),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='status',
            field=models.IntegerField(choices=[(b'Success', 1), (b'Canceled', 0), (b'Pending', 2)]),
        ),
    ]
