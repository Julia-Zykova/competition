from django import forms

from models_app.models import Photo
from service_objects.services import ServiceWithResult


class EditPhotoService(ServiceWithResult):
    photo = forms.IntegerField()
    description = forms.CharField(max_length=220, required=False)
    title = forms.CharField(max_length=50, required=False)

    def process(self) -> ServiceWithResult:
        if self.is_valid():
            self.result = self._update_photo
        return self

    @property
    def _photo(self) -> Photo:
        return Photo.objects.get(id=self.cleaned_data['photo'])

    @property
    def _update_photo(self) -> Photo:
        photo = self._photo
        if self.cleaned_data['title']:
            photo.title = self.cleaned_data['title']
        if self.cleaned_data['description']:
            photo.description = self.cleaned_data['description']
        photo.save()
        return photo
