from django.urls import re_path
from .views import (
    cart_home, cart_update, checkout_home, checkout_address_create,
    create_order,
)

app_name = 'carts'
urlpatterns = [
    re_path(r'^$', cart_home, name='cart'),
    re_path(r'^update/$', cart_update, name='cart_update'),
    re_path(r'^checkout/$', checkout_home, name='checkout'),
    re_path(r'^create-address/$', checkout_address_create, name='checkout_address_create'),
    re_path(r'^create-order/$', create_order, name='create_order'),
]