from datetime import datetime
from datetime import timedelta
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser

from imagekit.models.fields import ImageSpecField
from imagekit.processors import ResizeToFill

from models_app.signals import uploaded_file_path
from .managers import CustomUserManager


class CustomUser(AbstractUser):

    username = None
    date_joined = None
    groups = None
    last_login = None

    first_name = models.CharField(max_length=30, blank = True, null = True)
    last_name =  models.CharField(max_length=150, blank = True, null = True)
    user_photo = models.ImageField(upload_to=uploaded_file_path, blank = True, null = True)
    photo_small =ImageSpecField(source='user_photo',
        processors=[ResizeToFill(30, 30)],format='JPEG', options={'quality': 90})
    photo_medium =ImageSpecField(source='user_photo',
        processors=[ResizeToFill(580,580)],format='JPEG', options={'quality': 90})

    email = models.EmailField(('email address'), unique=True)
    password = models.CharField(max_length=128)

    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = ['password']

    objects = CustomUserManager()

    #@property
    #def token(self):
    #    return self._generate_jwt_token()

    #def get_full_name(self):
    #    return (self.first_name + " " + self.last_name)


    #def _generate_jwt_token(self):
    #    dt = datetime.now() + timedelta(days=1)

    #    token = jwt.encode({
    #        'id': self.pk,
    #        'exp': int(dt.strftime('%s'))
    #    }, settings.SECRET_KEY, algorithm='HS256')

    #    return token.decode('utf-8')

    #def __str__(self):
    #    return self.email

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ['email']