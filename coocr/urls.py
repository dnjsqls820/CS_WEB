from unicodedata import name
from django.contrib import admin
from django.urls import path, include
from . import views
app_name = "coocr"
urlpatterns = [
    path('', views.home, name='coocr'),
    path('coocr_upload',views.coocr_upload, name='coocr_upload'),
    path('search', views.search, name='search'),
]

from django.conf.urls.static import static
from django.conf import settings

urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)