from audioop import reverse

import jwt
from datetime import datetime
from datetime import timedelta
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser

from conf import settings
from imagekit.models.fields import ImageSpecField
from imagekit.processors import ResizeToFill

from models_app.signals import uploaded_file_path

from .managers import CustomUserManager


class CustomUser(AbstractUser):
    username = None
    date_joined = None
    groups = None
    last_login = None

    first_name = models.CharField(max_length=30, blank=True, null=True)
    last_name = models.CharField(max_length=150, blank=True, null=True)
    user_photo = models.ImageField(upload_to=uploaded_file_path, blank=True, null=True)

    email = models.EmailField(('email address'), unique=True)
    password = models.CharField(max_length=128)

    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = ['password']

    objects = CustomUserManager()

    def get_full_name(self):
        if self.first_name and self.last_name:
            return self.first_name + " " + self.last_name

    def get_absolute_url(self):
        return reverse('photo_app:personal_account', kwargs={'pk': self.id})

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ['email']
