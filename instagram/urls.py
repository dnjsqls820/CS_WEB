# instagram/urls.py
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views
from django.contrib import messages
from django.shortcuts import redirect


app_name = 'instagram'

def protected_file(request, path, document_root=None):
    messages.error(request, "접근 불가")
    return redirect('/')

urlpatterns = [
    # path('', views.PostListView.as_view(), name='post_list'),
]

urlpatterns += static(settings.MEDIA_URL, protected_file, document_root=settings.MEDIA_ROOT)