from django.conf.urls import url
from .views import cart_home, cart_update


urlpatterns = [
    url(r'^$', cart_home, name='cart'),
    url(r'^cartupdate/$', cart_update, name='cart_update'),
]