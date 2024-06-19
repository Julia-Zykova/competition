from django import forms

from .models import Photo


class UploadPhotoForm(forms.ModelForm):
    title = forms.CharField(
        max_length=50,
        error_messages={
            'max_length': 'Слишком длинный заголовок. Максимально - 50 знаков', 'required': 'Без заголовка - никак'
        })
    description = forms.CharField(
        max_length=220,
        error_messages={
            'max_length': 'Слишком длинное описание. Максимально - 220 знаков', 'required': 'Описание обязательно'
        })

    image = forms.ImageField(error_messages={
        'required': 'Фотография является обязательным полем'
    })

    class Meta:
        model = Photo
        fields = ['author', 'title', 'description', 'image']
