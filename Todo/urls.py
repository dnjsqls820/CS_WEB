from django.conf import settings

from django.urls import path
from . import views
from django.contrib import messages
from django.shortcuts import redirect


app_name = 'Todo'

def protected_file(request, path, document_root=None):
    messages.error(request, "접근 불가")
    return redirect('/')

urlpatterns = [
    path('', views.Todo_list, name='todo_list'),
    path('create/', views.Todo_create, name='todo_create'),
    path('<int:pk>/delete/', views.Todo_delete, name='todo_delete'),
]