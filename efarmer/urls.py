from django.conf import settings
from django.conf.urls.static import static
from django.urls import re_path, path, include
from django.contrib import admin
from . import views


urlpatterns = [
    re_path(r'^$', views.home_page, name='home'),
    re_path(r'^admin/', admin.site.urls),
    re_path(r'^contact/$', views.contact_page, name='contact'),
    re_path(r'^accounts/', include('accounts.urls')),
    re_path(r'^products/', include('products.urls')),
    re_path(r'^search/', include('search.urls')),
    re_path(r'^cart/', include('carts.urls'))
]

# serve the static files in development env.
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
