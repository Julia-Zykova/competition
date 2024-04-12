from django.db import models
from django.urls import reverse
from imagekit.models.fields import ImageSpecField
from imagekit.processors import ResizeToFill, ResizeToFit
from django_fsm import FSMField, transition

from models_app.signals import uploaded_file_path
from models_app.models import CustomUser, BaseSoftDeleteModel
from models_app.models.comment.models import Comment


STATES = ('На модерации', 'Одобрено', 'Отклонено', 'На удалении')
STATES = list(zip(STATES, STATES))

class Photo(BaseSoftDeleteModel):

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
    state = FSMField(default=STATES[0], choices=STATES,blank = True, null=True)

    
    @transition(field=state, source='На модерации', target='Одобрено')
    def approve(self):
        pass
    
    @transition(field=state, source='На модерации', target='Отклонено')
    def reject(self):
        pass

    @transition(field=state, source=['Одобрено', 'Отклонено'], target='На удалении')
    def remove(self):
        pass

    @transition(field=state, source='На удалении',target='На модерации')
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