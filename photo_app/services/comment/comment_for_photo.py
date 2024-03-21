from django import forms

from models_app.models import Comment, Photo, CustomUser
from service_objects.services import ServiceWithResult
from service_objects.fields import ModelField


class CommentForPhotoService(ServiceWithResult):

    photo = forms.IntegerField()
    user = ModelField(CustomUser)
    text = forms.CharField(max_length=200)
    #как отобразить ответ на другой комментарий?
    
    def process(self):
        if self.is_valid():
            self.result = self._comment
        return self

    @property
    def _photo(self):
        return Photo.objects.get(id=self.cleaned_data['photo'])

    @property
    def _comment(self):
        Comment.objects.create(
            photo = self._photo,
            user = self.cleaned_data['user'],
            text = self.cleaned_data['text'],          
            )
        return self
