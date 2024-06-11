from django import forms

from models_app.models import Photo
from service_objects.services import ServiceWithResult


class RestorePhotoService(ServiceWithResult):
    photo = forms.IntegerField()
    custom_validations = ["is_on_delete", ]

    def process(self) -> ServiceWithResult:
        if self.is_valid():
            self.run_custom_validations()
            self.result = self._restore_photo
        return self

    @property
    def _photo(self) -> Photo:
        return Photo.objects.get(id=self.cleaned_data['photo'])

    @property
    def _restore_photo(self) -> Photo:
        self._photo.recover()
        self._photo.save()
        return self._photo

    def is_on_delete(self) -> bool:
        if self._photo.state == 'on_delete':
            return True
        else:
            return False
