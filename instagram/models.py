from tabnanny import verbose
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.conf import settings
# Create your models here.

class Photo(models.Model):
    writer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user',verbose_name='글쓴이')
    content = models.TextField(blank=True,verbose_name='내용')
    image = models.ImageField(upload_to='instagram/post/%Y%m%d', verbose_name='이미지')
    created = models.DateTimeField(auto_now_add= True, verbose_name='생성일')
    updated = models.DateTimeField(auto_now = True, verbose_name='수정일')
    like = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='like_post', blank=True, verbose_name='좋아요')
    def __str__(self):
        return "content : " + self.content


    class Meta:
        ordering = ['-created']
        db_table = '인스타그램'
        verbose_name = '인스타그램'
        verbose_name_plural = '인스타'

    def get_image_url(self):
        return '%s%s'%(settings.MEDIA_URL, self.image)