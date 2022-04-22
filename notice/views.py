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
import os
import re
from django.http import HttpResponse, Http404
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

        #상단고정
        notice_fixed = Notice.objects.filter(top_fixed=True).order_by('-registered_date')
        context['notice_fixed'] = notice_fixed
        #선택한 검색타입을 계속 유지
        search_keyword = self.request.GET.get('q','')
        search_type = self.request.GET.get('type','')

        if len(search_keyword) > 1:
            context['q'] = search_keyword
        context['type'] = search_type
        return context

        
#공지사항 작성 + 파일명 저장
@login_message_required
@admin_required
def notice_write_view(request):
    if request.method == 'POST':
        form = NoticeWriteForm(request.POST, request.FILES)
        user = request.session['user_id']
        user_id = Member.objects.get(user_id = user)

        if form.is_valid():
            notice = form.save(commit = False)
            notice.writer = user_id
            if request.FILES:
                if 'upload_files' in request.FILES.keys():
                    notice.filename = request.FILES['upload_files'].name
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

#게시글 수정
@login_message_required
def notice_edit_view(request, pk):
    notice = Notice.objects.get(id=pk)
    if request.method == "POST":
        if(notice.writer == request.user or request.user.level == '0'):
            file_change_check = request.POST.get('fileChange', False)
            file_check = request.POST.get('upload_files-clear', False)

            if file_check or file_change_check:
                os.remove(os.path.join(settings.MEDAI_ROOT, notice.upload_files.path))

            form = NoticeWriteForm(request.POST, request.FILES, instance=notice)
            if form.is_valid():
                notice = form.save(commit = False)
                if request.FILES:
                    if 'upload_files' in request.FILES.keys():
                        notice.filename = request.FILES['upload_files'].name
                notice.save()
                messages.success(request, "수정되었습니다.")
                return redirect('/notice/'+str(pk))
    else:
        notice = Notice.objects(id=pk)
        if notice.writer == request.user or request.level == '0':
            form = NoticeWriteForm(instance=notice)
            context = {
                'form' : form,
                'edit' : '수정하기',
            }
            if notice.filename and notice.upload_files:
                context['filename'] = notice.filename
                context['file_url'] = notice.upload_files.url
            return render(request, 'notice/notice_writer.html', context)
        else:
            messages.error(request, '본인 게시글이 아닙니다.')
            return redirect('/notice/'+str(pk))

# 게시글 삭제
@login_message_required
def notice_delete_view(request,pk):
    notice = Notice.objects.get(id=pk)
    if notice.writer == request.user or request.user.level == '0':
        notice.delete()
        messages.success(request, '삭제되었습니다.')
        return redirect('/notice/')
    else:
        messages.error(request, '본인 게시글이 아닙니다.')
        return redirect('/notice/'+str(pk))
# 게시글 자세히보기 
@login_message_required
def notice_detail_view(request, pk):
    notice = get_object_or_404(Notice,  pk=pk)
    session_cookie = request.session['user_id']
    cookie_name = F'notice_hits:{session_cookie}'
    # 본인 게시글 확인
    if request.user == notice.writer:
        notice_auth = True
    else:
        notice_auth = False
    context = {
        'notice': notice,
        'noitce_auth' : notice_auth,
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


#한글명 첨부파일 다운로드
@login_message_required
def notice_download_view(request, pk):
    notice = get_object_or_404(Notice, pk=pk)
    url = notice.upload_files.url[1:]
    file_url = urllib.parse.unquote(url)

    if os.path.exists(file_url):
        with open(file_url, 'rb') as fh:
            quote_file_url = urllib.parse.quote(notice.filename.encode('utf-8'))
            response = HttpResponse(fh.read(), content_type=mimetypes.guess_type(file_url)[0])
            response['Content-Disposition'] = 'attachment;filename*=UTF-8\'\'%s' % quote_file_url
            return response
        raise Http404