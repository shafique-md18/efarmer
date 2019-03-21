from django.contrib import admin
from .models import Order


class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_id', 'billing_profile', 'cart', 'status', 'order_total')

admin.site.register(Order, OrderAdmin)
