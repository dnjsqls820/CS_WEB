# instagram/urls.py
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from .views import PhotoList, PhotoDelete, PhotoDetail, PhotoCreate, PhotoLike
from django.contrib import messages
from django.shortcuts import redirect


app_name = 'instagram'

# def protected_file(request, path, document_root=None):
#     messages.error(request, "접근 불가")
#     return redirect('/')

urlpatterns = [
    path('', PhotoList.as_view(), name='photo_list'),
    path('create/', PhotoCreate.as_view(), name='photo_create'),
    path('delete/<int:pk>', PhotoDelete.as_view(), name='photo_delete'),
    path('detail/<int:pk>', PhotoDetail.as_view(), name='photo_detail'),
    path('like/<int:photo_id>/', PhotoLike.as_view(), name='photo_like'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)