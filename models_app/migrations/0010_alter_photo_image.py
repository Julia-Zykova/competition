# Generated by Django 4.2.4 on 2023-09-11 10:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('models_app', '0009_alter_photo_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='photo',
            name='image',
            field=models.ImageField(upload_to='images/'),
        ),
    ]
