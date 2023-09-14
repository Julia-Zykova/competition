from django.db import models
from django.utils import timezone

from ..user_model.models import CustomUser
from ..photo_model.models import Photo



class Comment(models.Model):

	photo = models.ForeignKey('Photo', on_delete=models.CASCADE)
	user = models.ForeignKey('CustomUser', on_delete=models.CASCADE, verbose_name='author')
	text = models.CharField(max_length=200)
	reply = models.ForeignKey ('Comment',on_delete=models.CASCADE, verbose_name='reply')
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	class Meta:
		verbose_name = 'Комментарий'
		verbose_name_plural = 'Комментарии'
		ordering = ['user', 'photo']