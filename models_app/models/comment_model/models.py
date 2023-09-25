from django.db import models
from django.utils import timezone

# TODO: Не нужно
from ..user_model.models import CustomUser
from ..photo_model.models import Photo


class Comment(models.Model):
	photo = models.ForeignKey('Photo', on_delete=models.CASCADE, blank=True, null=True)  #TODO: related_name?
	user = models.ForeignKey('CustomUser', on_delete=models.CASCADE, verbose_name='Пользователь') #TODO: related_name?
	text = models.CharField(max_length=200)
	comment = models.ForeignKey('Comment', on_delete=models.CASCADE, blank=True, null=True, verbose_name='reply') # TODO: почему не просто comment ? related_name?

	class Meta:
		verbose_name = 'Комментарий'
		verbose_name_plural = 'Комментарии'
		ordering = ['user', 'photo']



