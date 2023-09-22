from django.db import models
from django.utils import timezone

from django.contrib.auth.models import AbstractUser
from .managers import CustomUserManager


class CustomUser(AbstractUser):

    username = None
    date_joined = None
    groups = None
    last_login = None

    first_name = models.CharField(max_length=30)
    last_name =  models.CharField(max_length=150)

    email = models.EmailField(('email address'), unique=True)
    password = models.CharField(max_length=128)

    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = ['first_name', 'last_name', 'password']

    objects = CustomUserManager()

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ['email']