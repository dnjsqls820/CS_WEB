# instagram/urls.py
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

from .views import PhotoList,PhotoDetail, PhotoDelete, PhotoCreate, PhotoLike, PhotoUpdate
from django.contrib import messages
from django.shortcuts import redirect


app_name = 'instagram'

# def protected_file(request, path, document_root=None):
#     messages.error(request, "접근 불가")
#     return redirect('/')

urlpatterns = [
    path('', PhotoList.as_view(), name='photo_list'),
    path('create/', PhotoCreate.as_view(), name='photo_create'),
    path('mylist/', views.photo_my_list, name='photo_mylist'),
    path('detail/<int:pk>', PhotoDetail.as_view(), name='photo_detail'),
    path('update/<int:pk>/', PhotoUpdate.as_view(), name='photo_update'),
    path('delete/<int:pk>/', PhotoDelete.as_view(), name='photo_delete'),
    path('like/<int:photo_id>/', PhotoLike.as_view(), name='photo_like'),
    
    path('<int:pk>/commit/writer', views.photo_commit, name='commit_write'),
    path('<int:pk>/commit/delete', views.photo_commit_delete, name='commit_delete')
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)