from django import forms

from models_app.models import Photo
from service_objects.services import ServiceWithResult


class EditPhotoService(ServiceWithResult):
    photo = forms.IntegerField()
    description = forms.CharField(max_length=220, error_messages={
        'max_length': 'Слишком длинное описание.',
        'required': 'Без описания - никак',
    })
    title = forms.CharField(max_length=50, error_messages={
        'max_length': 'Слишком длинный заголовок.',
        'required': 'Вы не можете оставить пустым заголовок',
    })

    def process(self):
        if self.is_valid():
            self.result = self._update_photo
        return self

    @property
    def _update_photo(self):
        photo = Photo.objects.get(id=self.cleaned_data['photo'])
        if self.cleaned_data['title']:
            photo.title = self.cleaned_data['title']
        if self.cleaned_data['description']:
            photo.description = self.cleaned_data['description']
        photo.save()
        return photo
