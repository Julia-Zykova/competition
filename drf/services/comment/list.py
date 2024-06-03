from django import forms

from service_objects.services import ServiceWithResult
from models_app.models import Comment, Photo


class ListCommentsService(ServiceWithResult):
    photo = forms.IntegerField(required=False)

    def process(self):
        if self.is_valid():
            self.result = self._get_queryset
        return self

    @property
    def _photo(self):
        photo = Photo.objects.get(id=self.cleaned_data['photo'])
        return photo

    @property
    def _get_queryset(self):
        return Comment.objects.filter(photo=self._photo)
