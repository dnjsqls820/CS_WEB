# notice/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.decorators import method_decorator
from django.views.generic import View, ListView, DetailView, FormView, CreateView
from .models import Notice
from users.decorators import login_message_required, admin_required
from django.db.models import Q
from django.contrib import messages
from django.urls import reverse
from .forms import NoticeWriteForm
from users.models import Member
import mimetypes
from mimetypes import guess_type
import os
import re
from django.http import HttpResponse, HttpResponseRedirect, Http404
from urllib.parse import quote
import urllib
from django.conf import settings

# Create your views here.

# 게시글 리스트
class NoticeListView(ListView):
    model = Notice
    paginate_by = 10
    template_name = 'notice/notice_list.html'
    context_object_name = 'notice_list'

    def get_queryset(self):
        notice_list = Notice.objects.order_by('-id')
        return notice_list

# 페이지네이션 커스텀
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        paginator = context['paginator']
        page_numbers_range = 5
        max_index = len(paginator.page_range)

        page = self.request.GET.get('page')
        current_page = int(page) if page else 1

        start_index = int((current_page - 1)/ page_numbers_range)
        end_index = start_index + page_numbers_range
        if end_index >= max_index:
            end_index = max_index

        page_range = paginator.page_range[start_index:end_index]
        context['page_range'] = page_range


        #선택한 검색타입을 계속 유지
        search_keyword = self.request.GET.get('q','')
        search_type = self.request.GET.get('type','')

        if len(search_keyword) > 1:
            context['q'] = search_keyword
        context['type'] = search_type
        return context
#게시글 작성
@login_message_required
@admin_required
def notice_write_view(request):
    if request.method == 'POST':
        form = NoticeWriteForm(request.POST)
        user = request.session['user_id']
        user_id = Member.objects.get(user_id = user)

        if form.is_valid():
            notice = form.save(commit = False)
            notice.writer = user_id
            notice.save()
            return redirect('notice:notice_list')
    else:
        form = NoticeWriteForm()

    return render(request, 'notice/notice_write.html', {'form': form})
# 게시글 검색기능
def get_queryset(self):
    search_keyword = self.request.GET.get('q','')
    search_type = self.reqeust.GET.get('type', '')
    notice_list = Notice.objects.order_by('-id')

    if search_keyword:
        if len(search_keyword) > 1:
            if search_type == 'all':
                search_notice_list = notice_list.filter(Q (title__icontains=search_keyword) | Q (content__icontains=search_keyword) | Q (writer__user_id__icontains=search_keyword))
            elif search_type == 'title_content':
                search_notice_list = notice_list.filter(Q (title__icontains=search_keyword) | Q (content__icontains=search_keyword))
            elif search_type == 'title':
                search_notice_list = notice_list.filter(title__icontains=search_keyword)
            elif search_type == 'content':
                search_notice_list = notice_list.filter(content__icontains=search_keyword)
            elif search_type =='writer':
                search_notice_list = notice_list.filter(writer__user_id__icontains=search_keyword)
            
            return search_notice_list
        else:
            messages.error(self.request, '검색어는 2글자 이상 입력해주세요.')
    return notice_list


# 게시글 자세히보기 
@login_message_required
def notice_detail_view(request, pk):
    notice = get_object_or_404(Notice,  pk=pk)
    session_cookie = request.session['user_id']
    cookie_name = F'notice_hits:{session_cookie}'
    context = {
        'notice': notice,
    }
    response = render(request, 'notice/notice_detail.html', context)
    
    #조회수 증가
    if request.COOKIES.get(cookie_name) is not None:
        cookies = request.COOKIES.get(cookie_name)
        cookies_list = cookies.split('|')
        if str(pk) not in cookies_list:
            response.set_cookie(cookie_name, cookies + f'|{pk}', expires=None)
            notice.hits += 1
            notice.save()
            return response
    else:
        response.set_cookie(cookie_name, pk, expires=None)
        notice.hits += 1
        notice.save()
        return response
    return render(request, 'notice/notice_detail.html',context)