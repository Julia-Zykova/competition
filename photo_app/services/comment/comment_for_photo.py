from django import forms
from django.contrib.contenttypes.models import ContentType

from models_app.models import Comment, Photo, CustomUser
from service_objects.services import ServiceWithResult
from service_objects.fields import ModelField


class CommentForPhotoService(ServiceWithResult):

    photo = forms.IntegerField(required=False)
    user = ModelField(CustomUser)
    text = forms.CharField(max_length=200)
    comment = forms.IntegerField(required=False)
    
    def process(self):
        if self.is_valid():
            self.result = self._comment
        return self

    @property
    def _photo(self):
        return Photo.objects.get(id=self.cleaned_data['photo'])

    @property
    def _parent_comment(self):
        return Comment.objects.get(id=self.cleaned_data['comment'])

    @property
    def _comment(self):
        if self.cleaned_data['comment']:
            return Comment.objects.create(
                user = self.cleaned_data['user'],
                text = self.cleaned_data['text'],
                comment = self._parent_comment,
                )
        else:
            return Comment.objects.create(
                user = self.cleaned_data['user'],
                text = self.cleaned_data['text'],
                photo=self._photo,
                )
        
