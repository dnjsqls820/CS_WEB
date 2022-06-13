from django.db import models
from django.conf import settings
from datetime import datetime,timedelta
from django.utils import timezone
# Create your models here.

class Todo(models.Model):
    writer = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE, verbose_name='작성자')
    content = models.CharField(max_length=255, verbose_name='내용')
    registered_date = models.DateTimeField(auto_now_add=True, verbose_name='등록시간')






    @property
    def created_string(self):
        time = datetime.now(tz=timezone.utc) - self.registered_date

        if time < timedelta(minutes=1):
            return '방금 전'
        elif time < timedelta(hours=1):
            return str(int(time.seconds / 60)) + '분 전'
        elif time < timedelta(days=1):
            return str(int(time.seconds / 3600)) + '시간 전'
        elif time < timedelta(days=7):
            time = datetime.now(tz=timezone.utc).date() - self.registered_date.date()
            return str(time.days) + '일 전'
        else:
            return False