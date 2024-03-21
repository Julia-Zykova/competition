from django import forms

from models_app.models import Photo
from service_objects.services import ServiceWithResult

class EditPhotoService(ServiceWithResult):
    photo = forms.IntegerField()
    description = forms.CharField(max_length=220) 
    title = forms.CharField(max_length=50)

    def process(self):
        if self.is_valid():
            self.result = self._update_photo
        return self

    @property
    def _photo(self):
       return Photo.objects.filter(id=self.cleaned_data['photo'])

    @property
    def _update_photo(self):
        self._photo.update(
            title = self.cleaned_data['title'],
            description = self.cleaned_data['description'],
            ) 
        return self