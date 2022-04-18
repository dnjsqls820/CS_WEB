# uesrs/views.py

from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from .decorators import *
from .models import Member
from django.views.generic import View
from django.contrib import messages
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