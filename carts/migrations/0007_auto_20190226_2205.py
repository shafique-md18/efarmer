# -*- coding: utf-8 -*-
# Generated by Django 1.11.18 on 2019-02-26 16:35
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('carts', '0006_remove_cart_subtotal'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='total',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=20),
        ),
    ]