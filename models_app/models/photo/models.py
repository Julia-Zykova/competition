from django.db import models
from django.urls import reverse
from imagekit.models.fields import ImageSpecField
from imagekit.processors import ResizeToFill, ResizeToFit
from django_fsm import FSMField, transition

from models_app.signals import uploaded_file_path
from models_app.models import CustomUser, BaseSoftDeleteModel
from models_app.models.comment.models import Comment


STATES = {
    'in_moderation': 'На модерации',
    'approved': 'Одобрено',
    'rejected': 'Отклонено',
    'on_delete': 'На удалении',
}
    

class Photo(BaseSoftDeleteModel):

    photo = models.ForeignKey ('Photo',on_delete=models.CASCADE,
        verbose_name='Фото', related_name = 'photos', blank = True, null=True)
    title = models.CharField(max_length=50)
    author = models.ForeignKey('CustomUser', on_delete=models.CASCADE,
        related_name = 'photos', blank = True, null=True)
    
    image = models.ImageField(upload_to=uploaded_file_path)
    photo_small =ImageSpecField(source='image',
        processors=[ResizeToFill(480, 480)],format='JPEG', options={'quality': 90})
    
    photo_big = ImageSpecField(source='image',
        processors=[ResizeToFit(391,520, False, mat_color="#A4C0BF")],format='JPEG', options={'quality': 100})
    description = models.CharField(max_length=220)
    pub_date = models.DateTimeField(auto_now_add=True)
    state = FSMField(default='in_moderation', choices=STATES)

    #@property
    #def photo_big(self):
    #    photo = self.images.order_by("created_at")[0]
    #    return photo.photo_big
    

    
    @transition(field=state, source='in_moderation', target='approved')
    def approve(self):
        pass
    
    @transition(field=state, source='in_moderation', target='rejected')
    def reject(self):
        pass

    @transition(field=state, source=['approved','rejected'], target='on_delete')
    def remove_photo(self):
        pass

    @transition(field=state, source='on_delete',target='in_moderation')
    def recover(self):
        pass


    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('photo_app:detail', kwargs={'pk': self.id})

    class Meta:
        verbose_name = 'Фото'
        verbose_name_plural = 'Фото'
        ordering = ['-pub_date', 'title']