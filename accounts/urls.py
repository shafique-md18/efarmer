from django.urls import re_path
from . import views

# app_name = 'accounts'
urlpatterns=[
    re_path(r'^login/$', views.login_page, name='login_page'),
    re_path(r'^register/$', views.register_page, name='register_page'),
    re_path(r'^logout/$', views.logout_user, name='logout_user'),
    re_path(r'^my-account/$', views.my_account, name='my_account'),
]