# -*- coding: utf-8 -*-
# Generated by Django 1.11.18 on 2019-03-05 16:37
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('addresses', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='address',
            name='full_name',
            field=models.CharField(default='', max_length=120),
        ),
    ]
