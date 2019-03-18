from django.conf.urls import url
from .views import cart_home, cart_update, checkout_home, checkout_address_create


urlpatterns = [
    url(r'^$', cart_home, name='cart'),
    url(r'^update/$', cart_update, name='cart_update'),
    url(r'^checkout/$', checkout_home, name='checkout'),
    url(r'^create-address/', checkout_address_create, name='checkout_address_create'),
]