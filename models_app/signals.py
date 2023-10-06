from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from models_app.models import Photo

@receiver(pre_save, sender=Photo)
def photo_tmp_path(sender, instance, **kwargs):
    if not hasattr(instance,"filename_photo"):
        setattr(instance,"filename_photo", str(instance.image))
        setattr(instance, "image" , None)
        instance.save()

        return instance


@receiver(post_save, sender=Photo)
def photo_new_path(sender, instance, **kwargs):
    if not instance.image:
        id_photo = instance.id
        filename = getattr(instance, "filename_photo")
        setattr(instance,"filename_photo", None)
        new_path = "photo/" + str(id_photo) + "/images/" + filename
        setattr(instance, "image", new_path)
        instance.save()

    return instance
            