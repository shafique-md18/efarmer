"""efarmer URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static

from django.conf.urls import include, url
from django.contrib import admin
from . import views


urlpatterns = [
    url(r'^$', views.home_page, name='home'),
    url(r'^admin/', admin.site.urls),
    url(r'^contact/$', views.contact_page, name='contact'),
    url(r'^accounts/', include('accounts.urls')),
    url(r'^products/', include('products.urls', namespace='products')),
    url(r'^search/', include('search.urls', namespace='search')),
    url('^cart/', include('carts.urls', namespace='carts')),
]

# serve the static files in development env.
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
