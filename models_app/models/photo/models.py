from django.db import models
from imagekit.models.fields import ImageSpecField
from imagekit.processors import ResizeToFill, ResizeToFit

from models_app.signals import uploaded_file_path
from models_app.models import CustomUser, BaseSoftDeleteModel

#Не могу удалить, вылезает ошибка в миграции 0022
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
	
	image = models.ImageField(upload_to=uploaded_file_path)
	photo_small =ImageSpecField(source='image',
		processors=[ResizeToFill(480, 480)],format='JPEG', options={'quality': 90})
	
	photo_big = ImageSpecField(source='image',
		processors=[ResizeToFit(391,520, False, mat_color="#A4C0BF")],format='JPEG', options={'quality': 100})
	description = models.CharField(max_length=220)
	pub_date = models.DateTimeField(auto_now_add=True)
	#mod_status = models.CharField(max_length=50,choices=STATUSES, default='на модерации')
	
	class Meta:
		verbose_name = 'Фото'
		verbose_name_plural = 'Фото'
		ordering = ['-pub_date', 'title']

	
	def __str__(self):
		return self.title


