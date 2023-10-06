from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from models_app.models import CustomUser, BaseModel, BaseSoftDeleteModel


def user_directory_path(self, filename):
    
    return 'images/user_{0}/{1}'.format(self.author.id, filename)


class Photo(BaseSoftDeleteModel):

	STATUSES = (
		('in_moderation', 'на модерации'),
		('approve', 'одобрено'),
		('on_deleted', 'на удалении'),
	)

	title = models.CharField(max_length=50)
	author = models.ForeignKey('CustomUser', on_delete=models.CASCADE,
		related_name = 'photos',blank = True, null=True)

	
	image = models.ImageField()
	description = models.CharField(max_length=220)
	pub_date = models.DateTimeField(auto_now_add=True)
	#mod_status = models.CharField(max_length=50,choices=STATUSES, default='на модерации')
	
	class Meta:
		verbose_name = 'Фото'
		verbose_name_plural = 'Фото'
		ordering = ['pub_date', 'title']


	
	def __str__(self):
		return self.title


