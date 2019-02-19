from django.conf.urls import url
from .views import ProductListView, ProductDetailView


urlpatterns = [
    url(r'^category/(?P<slug>[\w-]+)/$', ProductListView.as_view(), name="product_list"),
    url(r'^product/(?P<slug>[\w-]+)/$', ProductDetailView.as_view(), name="product_detail"),
]