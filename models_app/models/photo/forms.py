from django import forms

from .models import Photo

class UploadPhotoForm(forms.ModelForm):
    title = forms.CharField(
        max_length=50,
        error_messages={
        'max_length': 'Слишком длинный заголовок.','required': 'Без заголовка - никак'
        })
    description = forms.CharField(max_length=220, widget = forms.Textarea(attrs={'rows':8, 'cols':70}))
    
    class Meta:
        model = Photo
        fields = ['title', 'image', 'description', 'author']
        
    