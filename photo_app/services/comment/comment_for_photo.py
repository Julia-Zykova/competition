from django import forms
from django.contrib.contenttypes.models import ContentType

from models_app.models import Comment, Photo, CustomUser
from service_objects.services import ServiceWithResult
from service_objects.fields import ModelField


class CommentForPhotoService(ServiceWithResult):
    photo = forms.IntegerField(required=False)
    user = ModelField(CustomUser)
    text = forms.CharField(max_length=200, required=True, error_messages={
        'max_length': 'Слишком длинный комментарий.',
        'required': 'Вы не можете оставить пустой комментарий',
    })
    comment = forms.IntegerField(required=False)

    def process(self):
        if self.is_valid():
            self.result = self._comment
        return self

    @property
    def _photo(self):
        photo = Photo.objects.get(id=self.cleaned_data['photo'])
        if photo.state == 'approved':
            return photo
        else:
            raise forms.ValidationError("Вы не можете оставить комментарий к этому фото")

    @property
    def _parent_comment(self):
        return Comment.objects.get(id=self.cleaned_data['comment'])

    @property
    def _comment(self):
        if self.cleaned_data['comment']:
            return Comment.objects.create(
                user=self.cleaned_data['user'],
                text=self.cleaned_data['text'],
                comment=self._parent_comment,
            )
        else:
            return Comment.objects.create(
                user=self.cleaned_data['user'],
                text=self.cleaned_data['text'],
                photo=self._photo,
            )
