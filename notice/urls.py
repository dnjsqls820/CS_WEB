# notice/urls.py
# URL경로 입력으로 media 파일 접근 제한
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import path
from . import views

app_name = 'notice'

urlpatterns = [
    path('', views.NoticeListView.as_view(), name='notice_list'),
    path('<int:pk>/', views.notice_detail_view, name = 'notice_detail'),
    path('<int:pk>/edit', views.notice_edit_view, name='notice_edit'),
    path('<int:pk>/delete/', views.notice_delete_view, name= 'notice_delete'),
    path('write/', views.notice_write_view, name='notice_write'),
    path('download/<int:pk>', views.notice_download_view, name = 'notice_download'),
]


#URL경로 입력media 파일 접근 제한
def protected_file(request, path, document_root=None):
    messages.error(request, '접근 불가')
    return redirect('/')
urlpatterns += static(settings.MEDIA_URL, protected_file, document_root=settings.MEDIA_ROOT)