# Generated by Django 4.2.4 on 2023-09-08 12:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('models_app', '0006_alter_photo_mod_status'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='photo',
            options={'ordering': ['author', 'pub_date', 'title'], 'verbose_name': 'Фото', 'verbose_name_plural': 'Фото'},
        ),
        migrations.RemoveField(
            model_name='photo',
            name='mod_status',
        ),
    ]
