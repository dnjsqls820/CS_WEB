# users/admin.py

from encodings import search_function
from django.contrib import admin
from .models import Member
from django.contrib.auth.models import Group

# Register your models here.
class UserAdmin(admin.ModelAdmin):
    list_display = (
        'user_id',
        'name',
        'student_id',
        'grade',
        'circles',
        'department',
        'level',
        'date_joined'
        )
    search_fields = ('user_id','name','student_id', 'department')

admin.site.register(Member, UserAdmin)
admin.site.unregister(Group) # Admin페이지의 GROUP삭제