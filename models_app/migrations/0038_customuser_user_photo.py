# Generated by Django 5.0.2 on 2024-03-04 10:43

import models_app.signals
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('models_app', '0037_alter_comment_options_alter_comment_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='user_photo',
            field=models.ImageField(blank=True, null=True, upload_to=models_app.signals.uploaded_file_path),
        ),
    ]