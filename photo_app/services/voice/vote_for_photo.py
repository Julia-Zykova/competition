from django import forms
from models_app.models import Voice, Photo, CustomUser
from service_objects.services import ServiceWithResult
from service_objects.fields import ModelField


class VoteForPhotoService(ServiceWithResult):

    photo = forms.IntegerField()
    user = ModelField(CustomUser)
    
    def process(self):
        if self.is_valid():
            self.result = self._voice
        return self

    @property
    def _photo(self):
        return Photo.objects.get(id=self.cleaned_data['photo'])

    @property
    def _voice(self):
        try:
            obj = Voice.objects.get(photo=self._photo)
            obj.delete()
        except Voice.DoesNotExist:
            obj = Voice.objects.create(
                photo=self._photo,
                user=self.cleaned_data['user'],
                )        
    