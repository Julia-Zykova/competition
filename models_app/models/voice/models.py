from django.db import models
from django.utils import timezone

from ..user.models import CustomUser
from ..photo.models import Photo


class Voice(models.Model):

	photo = models.ForeignKey('Photo', on_delete=models.CASCADE, related_name = "voices")
	user = models.ForeignKey('CustomUser', on_delete=models.CASCADE, blank = True)	
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	class Meta:
		verbose_name = 'Голос'
		verbose_name_plural = 'Голоса'
		ordering = ['photo', 'user']

	def __str__(self):
		return (f'{self.user} проголосовал за - {self.photo}')