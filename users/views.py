# uesrs/views.py

from django.conf import settings
from django.utils.datastructures import MultiValueDictKeyError
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate, update_session_auth_hash
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .decorators import login_message_required, admin_required, logout_message_required
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect, get_object_or_404
# from django.views.decorators.csrf import csrf_exempt
from django.views.generic import CreateView, FormView, TemplateView
from django.views.generic import View
# from django.contrib.auth.views import PasswordResetConfirmView
from .models import Member
from .forms import CsRegisterForm, RegisterForm, LoginForm
from django.http import HttpResponse
import json
from django.core import serializers
from django.core.serializers.json import DjangoJSONEncoder
from .helper import send_mail
from django.urls import reverse_lazy, reverse
from django.http import HttpResponseRedirect, Http404
from django.forms.utils import ErrorList
from django.views.decorators.http import require_GET, require_POST
from django.core.exceptions import PermissionDenied

from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text
from django.contrib.auth.tokens import default_token_generator
from datetime import datetime
# Create your views here.

# 메인화면(로그인 전)
def index(request):
    # ip = get_ip(request)
    # if ip is not None:
    #     print (ip)
    # else:
    #     print ("IP FIND ERROR")

    return render(request, 'users/index.html')

# # 메인화면(로그인 후)
# @login_message_required
# def main_view(request):
#     notice_list = Notice.objects.order_by('-id')[:5]
#     calendar_property = [x.event_id for x in Calender.objects.all() if x.d_day == False]
#     calendar_list = Calender.objects.exclude(event_id__in=calendar_property).order_by('start_date')[:5]
#     free_list = Free.objects.filter(category='정보').order_by('-id')[:5]
#     anonymous_list = sorted(Anonymous.objects.all(), key=lambda t: t.like_count, reverse=True)[:5]

#     context = {
#         'notice_list' : notice_list,
#         'calendar_list' : calendar_list,
#         'free_list' : free_list,
#         'anonymous_list' : anonymous_list,
#     }
#     return render(request, 'users/main.html', context)

# 로그인
# @method_decorator(logout_message_required, name='dispatch')
class LoginView(FormView):
    template_name = 'users/login.html'
    form_class = LoginForm
    success_url = '/users/main/'

    def form_valid(self, form):
        user_id = form.cleaned_data.get("user_id")
        password = form.cleaned_data.get("password")
        user = authenticate(self.request, username=user_id, password = password)

        if user is not None:
            self.request.session['user_id'] = user_id
            login(self.request, user)
            remember_session = self.request.POST.get('remember_session', False)
            if remember_session:
                settings.SESSION_EXPIRE_AT_BROWSER_CLOSE = False

        return super().form_valid(form)

# 로그아웃
def logout_view(request):
    logout(request)
    return redirect('/')







# SMTP 메일 인증 
def form_valid(self, form):
    self.object = form.save()

    send_mail(
        '{}님의 회원가입 인증메일 입니다.'.format(self.object.user_id),
        [self.object.email],
        html=render_to_string('users/register_email.html', {
            'user': self.object,
            'uid': urlsafe_base64_encode(force_bytes(self.object.pk)).encode().decode(),
            'domain': self.request.META['HTTP_HOST'],
            'token': default_token_generator.make_token(self.object),
        }),
    )
    return redirect(self.get_success_url())
# 이메일 인증 활성화
def activate(request, uid64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uid64))
        current_user = Member.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, Member.DoesNotExist, ValidationErr):
        messages.error(request, '메일 인증에 실패했습니다.')
        return redirect('users:login')

    if default_token_generator.check_token(current_user, token):
        current_user.is_active = True
        current_user.save()

        messages.info(request, '메일 인증이 완료 되었습니다. 회원가입을 축하드립니다!')
        return redirect('users:login')
    messages.error(request, '메일 인증에 실패했습니다.')
    return redirect('users:login')

def get_success_url(self):
    self.request.session['register_auth'] = True
    messages.success(self.request, '회원님이 입력한 Email 주소로 인증 메일이 발송되었습니다. 인증 후 로그인이 가능합니다.')
    return reverse('users:register_success')
# 회원가입 인증메일 발송 안내 창
def register_success(request):
    if not request.session.get('register_auth', False):
        raise PermissionDenied
    request.session['register_auth'] = False
    
    return render(request, 'users/register_success.html')

# @method_decorator(logout_message_required, name='dispatch')
class AgreementView(View):
    def get(self, request, *agrs, **kwargs):
        request.session['agreement'] = False
        return render(request, 'users/agreement.html')

    def post(self, request, *agrs, **kwargs):
        if request.POST.get('agreement1', False) and request.POST.get('agreement2', False):
            request.session['agreement'] = True

            if request.POST.get('csregister') == 'csregister':
                return redirect('/users/csregister/')
            else:
                return redirect('/users/register/')
        else:
            messages.info(request,"약관에 모두 동의해주세요")
            return render(request, 'users/agreement.html')

# 컴공 회원가입
class CsRegisterView(CreateView):
    model = Member
    template_name = 'users/register_cs.html'
    form_class = CsRegisterForm

    def get(self, request, *args, **kwargs):
        if not request.session.get('agreement', False):
            raise PermissionDenied
        request.session['agreement'] = False

        url = settings.LOGIN_REDIRECT_URL
        if request.user.is_authenticated:
            return HttpResponseRedirect(url)
        return super().get(request, *args, **kwargs)

    def get_success_url(self):
        # messages.success(self.request, "회원가입 성공.")
        self.request.session['register_auth'] = True
        messages.success(self.request, '회원님의 입력한 Email 주소로 인증 메일이 발송되었습니다. 인증 후 로그인이 가능합니다.')
        # return settings.LOGIN_URL
        return reverse('users:register_success')

    def form_valid(self, form):
        self.object = form.save()

        # 회원가입 인증 메일 발송
        # ISSUE - https 통신오류 -> http 프로토콜 수정
        send_mail(
            '[호남대학교 컴퓨터공학부 RE:BORN] {}님의 회원가입 인증메일 입니다.'.format(self.object.user_id),
            [self.object.email],
            html=render_to_string('users/register_email.html', {
                'user': self.object,
                'uid': urlsafe_base64_encode(force_bytes(self.object.pk)).encode().decode(),
                'domain': self.request.META['HTTP_HOST'],
                'token': default_token_generator.make_token(self.object),
            }),
        )
        return redirect(self.get_success_url())




# 일반 회원가입
class RegisterView(CsRegisterView):
    template_name = 'users/register.html'
    form_class = RegisterForm


