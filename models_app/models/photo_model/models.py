from django.db import models
# TODO:  импорты ниже не нужны
from django.utils import timezone

from ..user_model.models import CustomUser


class Photo(models.Model):
	STATUSES = (
		('in_moderation', 'на модерации'),
		('approve', 'одобрено'),
		('on_deleted', 'на удалении'),
	)

	title = models.CharField(max_length=50)
	author = models.ForeignKey('CustomUser', on_delete=models.CASCADE, related_name='photos',
							   blank = True, null=True)
	# TODO: Хочу чтобы тут работало немного по-другому я хочу в папке media видеть к какому объекту относится эта картинка
	#  ( что-то типо /media/photo/002/image - значит что это изображение относится к фото у которого идентификатор 1)
	image = models.ImageField(upload_to='images')
	description = models.CharField(max_length=220)
	file = models.FileField(upload_to='files') # типо /media/photo/002/file/
	pub_date = models.DateTimeField(auto_now_add=True)
	#mod_status = models.CharField(max_length=50,choices=STATUSES, default='на модерации')
	is_deleted = models.BooleanField(default=False)

	class Meta:
		verbose_name = 'Фото'
		verbose_name_plural = 'Фото'
		ordering = ['author',
					'pub_date',
					'title']

#TODO: ЧТо будет если фото удалят?
