from django.shortcuts import render, redirect
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, DeleteView
from django.views.generic.detail import DetailView
from django.views.generic.base import View
from .models import Photo
from users.decorators import login_message_required, admin_required
from users.models import Member

from urllib.parse import urlparse
from django.contrib import messages
from django.http import HttpResponseRedirect,HttpResponseForbidden
# Create your views here.

class PhotoList(ListView):
    model = Photo
    template_name_suffix = '_list'
    context_object_name = 'instagram_list'
    fields = ['writer']



# def free_write_view(request):
#     if request.method == "POST":
#         form = PhotoWriterForm(request.POST)
#         user = request.session['user_id']
#         user_id = Member.objects.get(user_id = user)
        
#         if form.is_valid():
#             free = form.save(commit = False)
#             free.writer = user_id

#             free.save()
#             return redirect('instagram:photo_list')
#     else:
#         form = PhotoWriterForm()
#     return render(request, "instagram/photo_create.html", {'form': form})

class PhotoCreate(CreateView):
    model = Photo
    fields = ['content']
    context_object_nmae = 'instagram_create'
    template_name_suffix = '_create'
    success_url = '/'
    def form_valid(self, form):
        form.instance.writer_id = self.request.user.id
        if form.is_valid():
            form.instance.save()
            return redirect('instagram:photo_list')
        else:
            return self.render_to_response({'form':form})


class PhotoDetail(DetailView):
    model = Photo
    template_name_suffix = '_detail'

class PhotoDelete(DeleteView):
    model = Photo
    template_name_suffix = '_delete'
    success_url = '/'

    def dispatch(self, request, *args, **kwargs):
        objects = self.get_object()
        if objects.writer != request.user:
            messages.warning(request, '삭제할 권한이 없습니다.')
            return HttpResponseRedirect('/')
        else:
            return super(PhotoDelete, self).dispatch(request, *args, **kwargs)

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
