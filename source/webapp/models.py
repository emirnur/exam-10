from django.contrib.auth.models import User
from django.db import models


class File(models.Model):
    sign = models.CharField(max_length=200, verbose_name='Подпись')
    file = models.FileField(upload_to='uploads', verbose_name='Файл')
    author = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE,
                             verbose_name='Пользователь', related_name='file_author')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    def __str__(self):
        return self.sign

