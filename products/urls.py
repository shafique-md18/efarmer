from django.conf.urls import url
from .views import ProductListView, ProductDetailView


urlpatterns = [
    url(r'^$', ProductListView.as_view(), name="product_list_view"),
    url(r'^(?P<pk>\d+)/$', ProductDetailView.as_view(), name="product_list_view"),
]