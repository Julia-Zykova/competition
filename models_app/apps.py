from django.apps import AppConfig


class ModelsAppConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "models_app"

    def ready(self):
        from django.db.models.signals import post_save, pre_save

        from models_app.models import Photo
        from models_app.signals import create_auth_token, save_file, skip_saving_file

        pre_save.connect(skip_saving_file, sender=Photo)
        post_save.connect(save_file, sender=Photo)

        from django.conf import settings

        post_save.connect(create_auth_token, sender=settings.AUTH_USER_MODEL)
