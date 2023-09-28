from django.db import models
from models_app.models import BaseModel


class Comment(BaseModel):

	photo = models.ForeignKey('Photo', on_delete=models.CASCADE, related_name = 'comments')
	user = models.ForeignKey('CustomUser', on_delete=models.CASCADE, verbose_name='Автор', related_name = 'comments')
	text = models.CharField(max_length=200)
	comment = models.ForeignKey ('Comment',on_delete=models.CASCADE,
		verbose_name='Ответ', related_name = 'replies', blank = True, null=True)
	

	class Meta:
		verbose_name = 'Комментарий'
		verbose_name_plural = 'Комментарии'
		ordering = ['user', 'photo']

	def __str__(self):
		return (f'{self.user} прокомментировал фото {self.photo}')