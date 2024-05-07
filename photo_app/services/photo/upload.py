from django import forms

from models_app.models import Photo, CustomUser
from service_objects.services import ServiceWithResult
from service_objects.fields import ModelField


class UploadPhotoService(ServiceWithResult):

    author = ModelField(CustomUser)
    title = forms.CharField(max_length=50, error_messages={
        'max_length': 'Слишком длинный заголовок.',
        'required': 'Без заголовка - никак',
    })
    image = forms.ImageField()
    description = forms.CharField(max_length=220, widget=forms.Textarea, error_messages={
        'max_length': 'Слишком длинное описание.',
        'required': 'Без описания - никак',
    })

    def process(self):
        if self.is_valid():
            self.result = self._create_photo
            return self

    @property
    def _photo(self):
       return Photo.objects.get(id=self.cleaned_data['photo'])

    @property
    def _create_photo(self):
        return Photo.objects.create(
            title=self.cleaned_data['title'],
            image=self.cleaned_data['image'],
            description=self.cleaned_data['description'],
            author=self.cleaned_data['author'],
        )
