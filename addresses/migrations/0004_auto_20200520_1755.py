# -*- coding: utf-8 -*-
# Generated by Django 1.11.23 on 2020-05-20 12:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('addresses', '0003_auto_20190305_2208'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='country',
            field=models.CharField(choices=[('india', 'India')], default='india', max_length=20),
        ),
    ]
