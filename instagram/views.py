
from django.shortcuts import render, redirect,get_object_or_404
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView, FormMixin
from django.views.generic.detail import DetailView
from django.views.generic.base import View


from .models import Photo, Commit
from django.urls import reverse
import os
from json.decoder import JSONDecodeError
from users.decorators import login_message_required, admin_required
from django.views.decorators.http import require_GET, require_POST
from users.models import Member
#로그인 데코레이터 
from users.decorators import *
from django.utils.decorators import method_decorator
#url
from urllib.parse import urlparse
from django.contrib import messages
from django.http import HttpResponseRedirect,HttpResponseForbidden, JsonResponse
#댓글
from django.core.serializers.json import DjangoJSONEncoder
import json
# Create your views here.

class PhotoList(ListView):
    model = Photo
    template_name_suffix = '_list'
    context_object_name = 'instagram_list'
    fields = ['writer']

@method_decorator(login_message_required, name='dispatch')
class PhotoCreate(CreateView):
    model = Photo
    fields = ['content']
    context_object_name = 'instagram_create'
    template_name_suffix = '_create'
    success_url = 'instagram:photo_list'
    def form_valid(self, form):
        form.instance.writer_id = self.request.user.id
        if form.is_valid():
            form.instance.save()
            return redirect('instagram:photo_list')
        else:
            return self.render_to_response({'form':form})

@method_decorator(login_message_required, name='dispatch')
class PhotoDetail(DetailView):
    model = Photo
    template_name_suffix = '_detail'

    def get_context_data(self, **kwargs):
        # 기본 구현을 호출해 context를 가져온다.
        context = super(PhotoDetail, self).get_context_data(**kwargs)
        # 모든 책을 쿼리한 집합을 context 객체에 추가한다.
        context['commits'] = Commit.objects.all()
        return context

@method_decorator(login_message_required, name='dispatch')
class PhotoUpdate(UpdateView):
    model = Photo
    fields = ['content']
    context_object_name = 'instagram_update'
    template_name_suffix = '_update'
    success_url = '/'

    def dispatch(self, request, *args, **kwargs):
        object = self.get_object()
        if object.writer != request.user:
            messages.warning(request, '수정할 권한이 없습니다.')
            return HttpResponseRedirect('instagram:photo_list')
        else:
            return super(PhotoUpdate, self).dispatch(request, *args, **kwargs)


@method_decorator(login_message_required, name='dispatch')
class PhotoDelete(DeleteView):
    model = Photo
    template_name_suffix = '_delete'
    success_url = '/'

    def dispatch(self, request, *args, **kwargs):
        objects = self.get_object()
        if objects.writer != request.user:
            messages.warning(request, '삭제할 권한이 없습니다.')
            return HttpResponseRedirect('instagram:photo_list')
        else:
            return super(PhotoDelete, self).dispatch(request, *args, **kwargs)

@method_decorator(login_message_required, name='dispatch')
class PhotoLike(View):
    def get(self, request, *args, **kwargs):
        # 로그인 확인
        if not request.user.is_authenticated:
            return HttpResponseForbidden()
        else:
            if 'photo_id' in kwargs:
                photo_id = kwargs['photo_id']
                photo = Photo.objects.get(pk=photo_id)
                user = request.user
                if user in photo.like.all():
                    photo.like.remove(user)
                else:
                    photo.like.add(user)
            referer_url = request.META.get('HTTP_REFERER')
            path = urlparse(referer_url).path
            return HttpResponseRedirect(path)

#내가 작성한 게시글 보기
@login_message_required
@require_GET
def photo_my_list(request):
    photo_list = Photo.objects.filter(writer=request.user.id).order_by('-created')
    context = {
        'photo_list' : photo_list,
    }
    return render(request, 'instagram/photo_mylist.html',context)



#댓글 달기
@login_message_required
def photo_commit(request, pk):
    post = get_object_or_404(Photo, id=pk)
    writer = request.POST.get('writer')
    content = request.POST.get('content')
    reply = request.POST.get('reply')
    if content:
        commit = Commit.objects.create(post=post, writer=request.user,content=content, reply=reply )
        commit_count = Commit.objects.filter(post=pk).exclude(deleted=True).count()
        post.commits = commit_count
        post.save()
        data = {
            'writer':writer,
            'content':content,
            'created': '방금 전',
            'commit_count':commit_count,
            'commit_id': commit.id
        }
        if request.user == post.writer:
            data['self_commit'] = '(글쓴이)'
        # return redirect(reverse('instagram:photo_detail', args=[pk]))
        return HttpResponse(json.dumps(data, cls=DjangoJSONEncoder), content_type="application/json")

#댓글 삭제
@login_message_required
def photo_commit_delete(request, pk):
    post = get_object_or_404(Photo, id=pk)
    commit_id = request.POST.get('commit_id')
    target_commit = Commit.objects.get(pk = commit_id)

    if request.user == target_commit.writer or request.user.level == '1' or request.user.level == '0':
        target_commit.deleted = True
        target_commit.save()
        commit_count = Commit.objects.filter(post=pk).exclude(deleted = True).count()
        post.commits = commit_count
        post.save()
        data = {
            'commit_id':commit_id,
            'commit_count':commit_count
        }
        return HttpResponse(json.dumps(data, cls=DjangoJSONEncoder), content_type="application/json")
