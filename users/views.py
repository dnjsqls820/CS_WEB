# uesrs/views.py

from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from .decorators import *
from .models import Member
from django.views.generic import View
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from .forms import CsRegisterForm, RegisterForm
from django.views.generic import CreateView
# Create your views here.

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


class CsRegisterView(CreateView):
    model = Member
    template_name = 'users/register_cs.html'
    form_class = CsRegisterForm

    def get(self, request, *args, **kwargs):
        if not request.session.get('agreement', False):
            raise PermissionDenied
        request.session['agreement'] = False
        return super().get(request, *args, **kwargs)

    def get_success_url(self):
        messages.success(self.request, "회원가입 성공.")
        return redirect('users:login')

    def form_valid(self, form):
        self.object = form.save()
        return redirect(self.get_success_url())




# 일반 회원가입
class RegisterView(CsRegisterView):
    template_name = 'users/register.html'
    form_class = RegisterForm