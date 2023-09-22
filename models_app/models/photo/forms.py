from django import forms

from .models import Photo

class UploadPhotoForm(forms.ModelForm):

	#title = forms.CharField(max_length=50)
	#image = forms.ImageField(label='Photo',required=False)
	#description = forms.CharField(max_length=220)
	#author = forms.ModelChoiceField()
	#pub_date = forms.DateTimeField()


	class Meta:
		model = Photo
		fields = ['title', 'image', 'description']
		
	