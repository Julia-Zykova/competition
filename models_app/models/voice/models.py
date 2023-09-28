from django.db import models
from models_app.models import BaseModel, DataMixin


class Voice(DataMixin, BaseModel):

	photo = models.ForeignKey('Photo', on_delete=models.CASCADE,
		related_name = "voices")

	user = models.ForeignKey('CustomUser', on_delete=models.CASCADE,
		related_name = "voices", blank = True)	

	
	class Meta:
		verbose_name = 'Голос'
		verbose_name_plural = 'Голоса'
		ordering = ['photo', 'user']

		constraints = [
			models.UniqueConstraint(fields = ['photo', 'user'], name = 'unique_voice')
		]

	def __str__(self):
		return (f'{self.user} проголосовал за - {self.photo}')