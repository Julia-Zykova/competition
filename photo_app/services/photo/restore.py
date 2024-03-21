from django import forms

from models_app.models import Photo
from service_objects.services import ServiceWithResult
from service_objects.fields import ModelField


class RestorePhotoService(ServiceWithResult):
    photo = ModelField(Photo)
    
    def process(self):
        if self.is_valid():
            photo = Photo.objects.filter(id=photo.id)
            photo.restore()

        return self

