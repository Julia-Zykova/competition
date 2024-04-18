from django import forms

from models_app.models import Photo
from service_objects.services import ServiceWithResult



class RestorePhotoService(ServiceWithResult):
    photo = forms.IntegerField()
    
    def process(self):
        if self.is_valid():
            self.result = self._restore_photo
        return self

    @property
    def _restore_photo(self):
        photo = Photo.objects.get(id=self.cleaned_data['photo'])
        if photo.state == 'on_delete': 
            photo.recover()
            photo.save()