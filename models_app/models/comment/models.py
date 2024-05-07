from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models

from models_app.models import BaseModel


class Comment(BaseModel):
    comment = models.ForeignKey('Comment', on_delete=models.CASCADE,
                                verbose_name='Ответ', related_name='comments', blank=True, null=True)
    photo = models.ForeignKey('Photo', on_delete=models.CASCADE, related_name='comments', blank=True, null=True)
    user = models.ForeignKey('CustomUser', blank=True, null=True, on_delete=models.CASCADE, verbose_name='Автор',
                             related_name='comments')
    text = models.CharField(max_length=200)

    def __str__(self):
        return self.text

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ["created_at"]
