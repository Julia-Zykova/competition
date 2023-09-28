from django.db import models
from models_app.models import BaseModel, DataMixin


def user_directory_path(self, filename):
    
    return 'images/user_{0}/{1}'.format(self.author.id, filename)


class Photo(DataMixin, BaseModel):

	STATUSES = (
		('in_moderation', 'на модерации'),
		('approve', 'одобрено'),
		('on_deleted', 'на удалении'),
	)

	title = models.CharField(max_length=50)
	author = models.ForeignKey('CustomUser', on_delete=models.CASCADE,
		related_name = 'photos',blank = True, null=True)
	image = models.ImageField(upload_to=user_directory_path)
	description = models.CharField(max_length=220)
	pub_date = models.DateTimeField(auto_now_add=True)
	#mod_status = models.CharField(max_length=50,choices=STATUSES, default='на модерации')
	slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL", blank = True, null = True)
	

	class Meta:
		verbose_name = 'Фото'
		verbose_name_plural = 'Фото'
		ordering = ['pub_date', 'title']

	def __str__(self):
		return self.title

