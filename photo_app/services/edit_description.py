from django import forms

from models_app.models import Photo
from service_objects.services import ServiceWithResult
from service_objects.fields import ModelField


class EditDescriptionPhotoService(ServiceWithResult):
    photo = ModelField(Photo)
    new_description = forms.CharField(max_length=220) 
    
    def process(self):
        if self.is_valid():
            old_description = photo.description
            photo.description = self.cleaned_data['new_description'] 
            photo.save()
            
        return self