from django import forms

from .models import Photo

class UploadPhotoForm(forms.ModelForm):

	class Meta:
		model = Photo
		fields = ['title', 'image', 'description', 'author']
		
	