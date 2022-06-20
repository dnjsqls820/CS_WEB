from django.shortcuts import render, redirect
from users.models import Member
from django.contrib import messages
from Todo.models import Todo
from free.models import Free

# Create your views here.

#회원관리
def member_list(request):
    if request.user.level == '0' or request.user.level == '1':
        member_list = Member.objects.all()
        content = {
            'member_list':member_list,
        }
    return render(request, 'user_admin/member.html', content)

def member_profile(request,pk):
    member_list = Member.objects.filter(id=pk)
    content = { 'member_list':member_list}
    return render(request, 'user_admin/member_profile.html', content)


def member_delete(request,pk):
    member = Member.objects.filter(id=pk)
    member.delete()
    messages.success(request, "회원탈퇴가 완료되었습니다.")
    return redirect('/user_admin/')
