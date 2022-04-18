# users/urls.py

from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('main/', views.index, name = 'main'),
    path('agreement/', views.AgreementView.as_view(), name='agreement'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('csregister/', views.CsRegisterView.as_view(), name='csregister'),
    #메일인증
    path('registerauth/', views.register_success, name='register_success'),
    path('activate/<str:uid64>/<str:token>/', views.activate, name='activate'),
    #로그인
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.logout_view, name='logout'),

]
