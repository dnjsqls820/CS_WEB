from tabnanny import verbose
from django.db import models
from django.utils import timezone
from datetime import datetime, timedelta
from django.contrib.auth.models import User
from django.urls import reverse
from django.conf import settings
# Create your models here.

class Photo(models.Model):
    writer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user',verbose_name='글쓴이')
    content = models.TextField(blank=True,verbose_name='내용')
    image = models.ImageField(upload_to='instagram/post/%Y%m%d', verbose_name='이미지')
    commits = models.PositiveIntegerField(verbose_name='댓글수', null=True)
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


class Commit(models.Model):
    post = models.ForeignKey(Photo, on_delete=models.CASCADE, verbose_name='포스트')
    writer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, verbose_name='작성자')
    content = models.TextField(verbose_name='댓글내용')
    created = models.DateTimeField(auto_now_add=True, verbose_name='작성일')
    deleted = models.BooleanField(default=False, verbose_name='삭제여부')
    reply = models.IntegerField(verbose_name='답글위치', default=0)

    def __str__(self):
        return self.content

    @property
    def created_string(self):
        time = datetime.now(tz=timezone.utc) - self.created

        if time < timedelta(minutes=1):
            return '방금 전'
        elif time < timedelta(hours=1):
            return str(int(time.seconds / 60)) + '분 전'
        elif time < timedelta(days=1):
            return str(int(time.seconds / 3600)) + '시간 전'
        elif time < timedelta(days=7):
            time = datetime.now(tz=timezone.utc).date() - self.created.date()
            return str(time.days) + '일 전'
        else:
            return False

    class Meta:
        db_table = '인스타그램 댓글'
        verbose_name = '인스타그램 댓글'
        verbose_name_plural = '인스타그램 댓글'