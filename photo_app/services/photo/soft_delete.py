from django import forms

from models_app.models import Photo
from service_objects.services import ServiceWithResult
from service_objects.fields import ModelField


class SoftDeletePhotoService(ServiceWithResult):
    photo = forms.IntegerField()
    
    def process(self):
        if self.is_valid():
            self.result = self._soft_delete
        return self
        

    @property
    def _photo(self):
       return Photo.objects.get(id=self.cleaned_data['photo'])

    @property
    def _soft_delete(self):
        self._photo.soft_delete()