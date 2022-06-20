# user_admin/urls.py
from django.urls import path
from . import views

app_name = 'user_admin'

urlpatterns = [
    path('member/',views.member_list, name='member'),
    path('member/<int:pk>/',views.member_profile, name='propfile'),
    path('member/<int:pk>/delete/',views.member_delete, name='member_delete'),
]