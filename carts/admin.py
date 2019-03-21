from django.contrib import admin
from .models import Cart


class CartAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'total', 'active')

admin.site.register(Cart, CartAdmin)
