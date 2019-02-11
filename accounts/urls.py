from django.conf.urls import url
from . import views

urlpatterns=[
    url(r'^login/$', views.login_page, name='login_page'),
    url(r'^register/$', views.register_page, name='register_page'),
    url(r'^logout/$', views.logout_user, name='logout_user'),
]