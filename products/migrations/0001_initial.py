# -*- coding: utf-8 -*-
# Generated by Django 1.11.18 on 2019-03-05 15:22
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import products.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, default='', max_length=30, unique=True, verbose_name='Category')),
                ('slug', models.SlugField(blank=True, null=True, unique=True)),
            ],
            options={
                'verbose_name': 'category',
                'verbose_name_plural': 'categories',
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=120, verbose_name='Product Name')),
                ('brand', models.CharField(default='', max_length=120, verbose_name='Brand')),
                ('size', models.CharField(blank=True, default='', max_length=10, verbose_name='Size')),
                ('stock', models.PositiveIntegerField(default=0, verbose_name='Stock')),
                ('description', models.TextField(blank=True, default='', verbose_name='Description')),
                ('maximum_retail_price', models.DecimalField(decimal_places=2, default=0.0, max_digits=10, verbose_name='Maximum Retail Price')),
                ('selling_price', models.DecimalField(decimal_places=2, default=0.0, max_digits=20, verbose_name='Selling Price')),
                ('image', models.ImageField(default='image_not_available.jpg', upload_to=products.models.path_and_rename, verbose_name='Product Image')),
                ('featured', models.BooleanField(default=False, verbose_name='Add to featured products?')),
                ('slug', models.SlugField(blank=True, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.Category')),
            ],
            options={
                'ordering': ('name',),
            },
        ),
    ]
