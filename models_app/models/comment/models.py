from django.db import models
from django.utils import timezone

from ..user.models import CustomUser
from ..photo.models import Photo



class Comment(models.Model):

	photo = models.ForeignKey('Photo', on_delete=models.CASCADE, related_name = 'comments')
	user = models.ForeignKey('CustomUser', on_delete=models.CASCADE, verbose_name='author', related_name = 'comments')
	text = models.CharField(max_length=200)
	reply = models.ForeignKey (
		'Comment',on_delete=models.CASCADE, verbose_name='reply', related_name = 'replies', blank = True, null=True)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	class Meta:
		verbose_name = 'Комментарий'
		verbose_name_plural = 'Комментарии'
		ordering = ['user', 'photo']

	def __str__(self):
		return (f'{self.user} прокомментировал фото {self.photo}')