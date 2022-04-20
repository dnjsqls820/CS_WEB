# uesrs/views.py

from re import I
from django.conf import settings
from django.utils.datastructures import MultiValueDictKeyError
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate, update_session_auth_hash
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError 
from django.utils.decorators import method_decorator
from .decorators import login_message_required, admin_required, logout_message_required
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect, get_object_or_404
# from django.views.decorators.csrf import csrf_exempt
from django.views.generic import CreateView, FormView, TemplateView
from django.views.generic import View
# from django.contrib.auth.views import PasswordResetConfirmView
from .models import Member
from .forms import CsRegisterForm, CustomCsUserChangeForm, RecoveryPwForm, RegisterForm, LoginForm, RecoveryIdFrom, RecoveryPwForm, CustomSetPasswordForm, CustomPasswordChangeForm,CustomUserChangeForm,CheckPasswordForm
from .helper import send_mail
from django.http import HttpResponse
import json
from django.core import serializers
from django.core.serializers.json import DjangoJSONEncoder
from .helper import send_mail, email_auth_num
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

# # 메인화면(로그인 전)
def index(request):

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

# 회원가입 인증메일 발송 안내 창
def register_success(request):
    if not request.session.get('register_auth', False):
        raise PermissionDenied
    request.session['register_auth'] = False

    return render(request, 'users/register_success.html')

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
    # SMTP 메일 인증
    def form_valid(self, form):
        self.object = form.save()

        send_mail(
            '{}님의 회원가입 인증메일 입니다.'.format(self.object.user_id),
            [self.object.email],
            html=render_to_string('users/register_email.html', {
                'user': self.object,
                'uid': urlsafe_base64_encode(force_bytes(self.object.pk)).decode(),
                'domain': self.request.META['HTTP_HOST'],
                'token': default_token_generator.make_token(self.object),
            })
        )
        return redirect(self.get_success_url())
    #'bytes' object has no attribute 'encode' 오류가 나타나면 encode().decode() -> decode()로 변경



# 일반 회원가입
class RegisterView(CsRegisterView):
    template_name = 'users/register.html'
    form_class = RegisterForm

# 프로필
@login_message_required
def profile_view(request):
    if request.method == 'GET':
        return render(request, 'users/profile.html')

# 프로필 수정
@login_message_required
def profile_update_view(request):
    if request.method == 'POST':
        if request.user.department == '컴퓨터공학과':
            user_change_form = CustomCsUserChangeForm(request.POST, instance = request.user)
        else:   
            user_change_form = CustomUserChangeForm(request.POST, instance = request.user)

        if user_change_form.is_valid():
            user_change_form.save()
            messages.success(request, '회원정보가 수정되었습니다.')
            return render(request, 'users/profile.html')
    else:
        if request.user.department == '컴퓨터공학과':
            user_change_form = CustomCsUserChangeForm(instance = request.user)
        else:   
            user_change_form = CustomUserChangeForm(instance = request.user)

        return render(request, 'users/profile_update.html', {'user_change_form':user_change_form})

# 회원탈퇴
@login_message_required
def profile_delete_view(request):
    if request.method == 'POST':
        password_form = CheckPasswordForm(request.user, request.POST)

        if password_form.is_valid():
            request.user.delete()
            logout(request)
            messages.success(request, '회원탈퇴가 완료되었습니다.')
            return redirect('/users/login')
        else:
            password_form = CheckPasswordForm(request.user)
        
        return render(request, 'users/profile_delete.html',{'password_form': password_form})





# 비밀번호 변경
@login_message_required
def password_edit_view(request):
    if request.method == 'POST':
        password_change_form = CustomPasswordChangeForm(request.user, request.POST)
        if password_change_form.is_valid():
            user = password_change_form.save()
            update_session_auth_hash(request,user)
            messages.success(request, "비밀번호를 성공적으로 변겨하였습니다.")
            return redirect('users:profile')
    else:
        password_change_form = CustomPasswordChangeForm(request.user)
    return render(request, 'users/profile_password.html',{'password_change_form': password_change_form})


# 아이디 찾기
@method_decorator(logout_message_required, name='dispatch')
class RecoverIdView(View):
    template_name = 'users/recovery_id.html'
    form = RecoveryIdFrom

    def get(self, request):
        if request.method=='GET':
            form = self.recovery_id(None)
        return render(request, self.template_name, {'form':form,})

# RecoveryIdView와 매핑된 템플릿에서 아이디찾기라는 버튼을 클릭했을 때 요청되는 Ajax함수
def ajax_find_id_view(request):
    name = request.POST.get('name')
    email = request.POST.get('email')
    reuslt_id = Member.objects.get(name=name, email=email)

    return HttpResponse(json.dumps({"result_id": reuslt_id.user_id}, cls=DjangoJSONEncoder), content_type = "application/json")

# 비밀번호 찾기
@method_decorator(logout_message_required, name='dispatch')
class RecoveryPwView(View):
    template_name = 'users/recovery_pw.html'
    recovery_pw = RecoveryPwForm

    def get(self,request):
        if request.method=='GET':
            form = self.recovery_pw(None)
            return render(request, self.template_name, {'form': form,})

# Ajax요청
def ajax_find_pw_view(request):
    user_id = request.POST.get('user_id')
    name = request.POST.get('name')
    email = request.POST.get('email')
    target_user = Member.objects.get(user_id=user_id, name=name, email=email)

    if target_user:
        auth_num = email_auth_num()
        target_user.auth = auth_num
        target_user.save()

        send_mail(
            '비밀번호 찾기 인증메일입니다.',
            [email],
            html=render_to_string('users/recovery_email.html',{
                'auth_num': auth_num,
            }),
        )
    return HttpResponse(json.dump({"result": target_user.user_id}, cls=DjangoJSONEncoder), content_type = "application/json")
    # Ajax로 요청된 값들은 Member모델에서 찾은 후 반환된 targeet_user의 auth필드에 방금 구현한 인증번호 생성함수를 통해
    # auth_num를 저장합니다. 후에 send_mail함수로 인증번호인 auth_num을 담은 메일을 사용자에게 발송합니다.

def auth_confirm_view(request):
    user_id = request.POST.get('user_id')
    input_auth_num = request.POST.get('input_auth_num')
    target_user = Member.objects.get(user_id=user_id, auth=input_auth_num)
    target_user.auth = ""
    target_user.save()
    request.session['auth'] = target_user.user_id

    return HttpResponse(json.dumps({"result": target_user.user_id}, cls=DjangoJSONEncoder), content_type = "application/json")
    # Ajax로 요청된 user_id와 입력된 인증번호인 input_auth_num가 일치하는 쿼리를 Member모델에서 찾아 반환한 후
    # auth 세션을 생성하고 비밀번호를 찾으려는 사용자의 user_id를 세션값으로 생성합니다.

    
    # auth_confirm_view를 통해 Ajax통신이 성공했다면 redirect될 비밀번호 변경창의 view를 입력한다.
@logout_message_required
def auth_pw_reset_view(request):
    if request.method == 'GET':
        if not request.session.get('auth', False):
            raise PermissionDenied
        
    if request.method == 'POST':
        session_user = request.session['auth']
        current_user = Member.objects.get(user_id = session_user)
        login(request, current_user)

        reset_password_form = CustomSetPasswordForm(request.user, request.POST)

        if reset_password_form.is_valid():
            user = reset_password_form.save()
            messages.success(request, "비밀번호 변경완료! 변경된 비밀번호로 로그인 해주세요")
            logout(request)
            return redirect('user:login')
        else:
            logout(request)
            request.session['auth'] = session_user
    else:
        reset_password_form = CustomSetPasswordForm(request.user)
    return render(request, 'users/password_reset.html', {'form': reset_password_form})
    

# 개인정보 동의
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

# 이메일 인증 활성화
def activate(request, uid64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uid64))
        current_user = Member.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, Member.DoesNotExist):
        messages.error(request, uid)
        return redirect('users:login')

    if default_token_generator.check_token(current_user, '메일 인증에 실패하였습니다.'):
        current_user.is_active = True
        current_user.save()

        messages.info(request, '메일 인증이 완료 되었습니다. 회원가입을 축하드립니다!')
        return redirect('users:login')

    # messages.error(request, '메일 인증에 실패했습니다.')
    # return redirect('users:login')

