from django.db import models
from django.utils import timezone

from ..user_model.models import CustomUser


class Photo(models.Model):

	STATUSES = (
		('М', 'на модерации'),
		('О', 'одобрено'),
		('У', 'на удалении'),
	)

	title = models.CharField(max_length=50)
	author = models.ForeignKey('CustomUser', on_delete=models.CASCADE, related_name = 'photos',blank = True, null=True)
	image = models.ImageField(upload_to='images')
	description = models.CharField(max_length=220)
	pub_date = models.DateTimeField(auto_now_add=True)
	#mod_status = models.CharField(max_length=50,choices=STATUSES, default='на модерации')
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	class Meta:
		verbose_name = 'Фото'
		verbose_name_plural = 'Фото'
		ordering = ['author','pub_date', 'title']

