# Generated by Django 4.2.5 on 2023-10-04 06:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('models_app', '0025_voice_unique_voice'),
    ]

    operations = [
        migrations.AddField(
            model_name='photo',
            name='is_deleted',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='voice',
            name='is_deleted',
            field=models.BooleanField(default=False),
        ),
    ]