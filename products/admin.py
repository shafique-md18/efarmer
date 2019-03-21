from django.contrib import admin
from .models import Product, Category


class ProductAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'size', 'stock', 'selling_price', 'maximum_retail_price')


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('__str__', )

admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)