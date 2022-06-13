from django.contrib import admin
from .models import Todo
# Register your models here.

class TodoAdmin(admin.ModelAdmin):
    list_display = (
        'writer',
        'content'
        )
    search_fields = ('content','writer')
admin.site.register(Todo, TodoAdmin)