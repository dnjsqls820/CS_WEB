from django.shortcuts import render, redirect
from .models import Todo
from users.models import Member
# Create your views here.

def Todo_list(request):
    todo_list = Todo.objects.filter(writer=request.user.id).order_by('-registered_date')
    content = {
        'todo_list': todo_list
    }
    return render(request, 'todo/todo_list.html',content)

def Todo_create(request):
    user = request.session['user_id']
    user_id = Member.objects.get(user_id = user)
    contents = request.POST['Content']
    new_content = Todo(content = contents, writer = user_id)
    new_content = new_content.save()
    return redirect('/Todo')

def Todo_delete(request,pk):
    todo = Todo.objects.get(id=pk)
    if todo.writer == request.user or request.user.level == '1' or request.user.level == '0':
        todo.delete()
        print('완료된 일정 {}가 삭제되었습니다.'.format(todo.content))
        return redirect('/Todo')
    else:
        return redirect('/Todo/' + str(pk))