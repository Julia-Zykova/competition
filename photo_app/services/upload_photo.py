from django import forms

from models_app.models import Photo, CustomUser
from service_objects.services import ServiceWithResult
from service_objects.fields import ModelField


class UploadPhotoService(ServiceWithResult):
    author = ModelField(CustomUser)

    title = forms.CharField(max_length=50)
    image = forms.ImageField()
    description = forms.CharField(max_length=220)

    
    def process(self):
        if self.is_valid():
            title = self.cleaned_data['title']
            image = self.cleaned_data['image']
            description = self.cleaned_data['description']
            author = self.cleaned_data['author']
        
            photo = Photo.objects.create(
                title=title,
                image = image,
                description = description,
                author = author,
                ) 
           
            
        return self


   

