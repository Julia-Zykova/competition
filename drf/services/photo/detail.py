from django import forms
from models_app.models import Photo
from service_objects.services import ServiceWithResult


class DetailPhotoService(ServiceWithResult):
    photo = forms.IntegerField()

    def process(self):
        if self.is_valid():
            self.result = {'photo': self._photo, 'comments': self._comments}
        return self

    @property
    def _photo(self):
        return Photo.objects.get(id=self.cleaned_data['photo'])

    @property
    def _comments(self):
        photo = self._photo
        return photo.comments.order_by('-created_at')[:3]
