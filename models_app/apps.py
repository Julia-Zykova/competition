from django.apps import AppConfig


class ModelsAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'models_app'

    def ready(self):
        from models_app.signals import skip_saving_file, save_file
        from django.db.models.signals import pre_save, post_save
        from models_app.models import Photo

        
        pre_save.connect(skip_saving_file, sender=Photo)
        post_save.connect(save_file, sender=Photo)

