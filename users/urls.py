# users/urls.py

from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('',views.index, name = 'index'),
    #메인
    path('main/', views.main_view, name = 'main'),
    #회원가입
    path('agreement/', views.AgreementView.as_view(), name='agreement'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('csregister/', views.CsRegisterView.as_view(), name='csregister'),
    #메일인증
    path('registerauth/', views.register_success, name='register_success'),
    path('activate/<str:uid64>/<str:token>/', views.activate, name='activate'),
    #로그인
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.logout_view, name='logout'),
    #프로필
    path('profile/', views.profile_view, name='profile'),
    path('profile/post', views.profile_post_view, name='profile_post'),
    path('profile/comment', views.profile_comment_view, name='profile_comment'),
    path('profile/update/', views.profile_update_view, name='profile_update'),
    path('profile/delete/', views.profile_delete_view, name='profile_delete'),
    path('profile/password', views.password_edit_view, name='password_edit'),
    #아이디 찾기
    path('recovery/id', views.RecoverIdView.as_view(), name='recovery_id'),
    path('recovery/id/find', views.ajax_find_id_view, name='ajax_id'),
    #비밀번호 찾기
    path('recovery/pw/', views.RecoveryPwView.as_view(), name='recovery_pw'),
    path('recovery/pw/find/', views.ajax_find_pw_view, name='ajax_pw'),
    path('recovery/pw/auth/', views.auth_confirm_view, name='recovery_auth'),
    path('recovery/pw/reset/', views.auth_pw_reset_view, name='recovery_pw_reset'),
    
]
