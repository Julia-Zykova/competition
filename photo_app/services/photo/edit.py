from django import forms
from service_objects.services import ServiceWithResult

from models_app.models import Photo


class EditPhotoService(ServiceWithResult):
    photo = forms.IntegerField()
    description = forms.CharField(
        max_length=220,
        error_messages={
            "max_length": "Слишком длинное описание.",
            "required": "Без описания - никак",
        },
    )
    title = forms.CharField(
        max_length=50,
        error_messages={
            "max_length": "Слишком длинный заголовок.",
            "required": "Вы не можете оставить пустым заголовок",
        },
    )

    def process(self):
        if self.is_valid():
            self.result = self._update_photo
        return self

    @property
    def _photo(self):
        return Photo.objects.filter(id=self.cleaned_data["photo"])

    @property
    def _update_photo(self):
        return self._photo.update(
            title=self.cleaned_data["title"],
            description=self.cleaned_data["description"],
        )
