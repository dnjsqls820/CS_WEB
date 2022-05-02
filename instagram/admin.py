from encodings import search_function
from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import Photo
# Register your models here.

class PhotoAdmin(admin.ModelAdmin):
    list_display = (
        'writer',
        'content',
        'created',
        'updated',
        'photo_tag',
    )
    search_fields = ('writer','content','writer__user_id',)
    def photo_tag(self, post):
     	# 안전하게 필드명 저장유무를 체크해주자.
        # 필드에 저장된 경로가 없을 경우, url 계산에 실패한다.
        if post.image: 
            # 보안으로 escape 처리가 되어 marksafe를 사용해야함.
            return mark_safe(f'<img src="{post.image.url}" style="width:50px;" />')
        return None
admin.site.register(Photo, PhotoAdmin)

