from django import forms

from models_app.models import Photo
from service_objects.services import ServiceWithResult
from service_objects.fields import ModelField


class RenamePhotoService(ServiceWithResult):
    photo = ModelField(Photo)
    new_title = forms.CharField(max_length=50)  
    
    def process(self):
        if self.is_valid():
            old_title = photo.title
            photo.title = self.cleaned_data['new_title'] 
            photo.save()

        return self