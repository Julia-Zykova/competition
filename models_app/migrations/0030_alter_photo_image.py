# Generated by Django 4.2.5 on 2023-10-04 12:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('models_app', '0029_alter_photo_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='photo',
            name='image',
            field=models.ImageField(upload_to='photo/'),
        ),
    ]
