from django import forms

from models_app.models import Photo
from service_objects.services import ServiceWithResult
from service_objects.fields import ModelField


class SoftDeletePhotoService(ServiceWithResult):
    photo = ModelField(Photo)
    
    def process(self):
        if self.is_valid():
            Photo.objects.get(id=photo.id).soft_delete()

        return self

