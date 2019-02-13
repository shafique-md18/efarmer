# -*- coding: utf-8 -*-
# Generated by Django 1.11.18 on 2019-02-13 14:24
from __future__ import unicode_literals

from django.db import migrations, models
import products.models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0012_auto_20190213_1932'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='image',
            field=models.ImageField(default='image_not_available.jpg', upload_to=products.models.path_and_rename),
        ),
    ]
