from django.conf.urls import url
from .views import ProductCategoryListView, ProductDetailView


urlpatterns = [
    url(r'^category/(?P<slug>[\w-]+)/$', ProductCategoryListView.as_view(), name="product_category_list"),
    url(r'^product/(?P<slug>[\w-]+)/$', ProductDetailView.as_view(), name="product_detail"),
]