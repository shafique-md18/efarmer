from django.urls import re_path
from .views import ProductCategoryListView, ProductDetailView

app_name = 'products'
urlpatterns = [
    re_path(r'^category/(?P<slug>[\w-]+)/$', ProductCategoryListView.as_view(), name="product_category_list"),
    re_path(r'^product/(?P<slug>[\w-]+)/$', ProductDetailView.as_view(), name="product_detail"),
]