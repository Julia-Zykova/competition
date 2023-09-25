from django.db import models

# TODO:  импорты ниже не нужны

from django.utils import timezone

class Voice(models.Model):
	photo = models.ForeignKey('models_app.Photo', on_delete=models.CASCADE, related_name = "voices")
	user = models.ForeignKey('CustomUser', on_delete=models.CASCADE, related_name = "voices",
							 blank = True,
							 null=True)	# TODO: кажется автор голоса всегда должен существовать
	is_deleted = models.BooleanField(default=False)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	class Meta:
		verbose_name = 'Голос'
		verbose_name_plural = 'Голоса'
		ordering = ['photo', 'user']


# TODO: что будет если голос удалят попытаются удалить?