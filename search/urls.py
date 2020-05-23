from django.urls import re_path
from .views import SearchProductListView

app_name = 'search'
urlpatterns = [
    re_path(r'^$',  SearchProductListView.as_view(), name="query"),
]