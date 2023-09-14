# Generated by Django 4.2.4 on 2023-09-08 11:41

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('models_app', '0004_alter_photo_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='photo',
            name='author',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
