# Generated by Django 4.2.5 on 2023-10-19 12:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('models_app', '0034_alter_photo_options'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='comment',
        ),
    ]
