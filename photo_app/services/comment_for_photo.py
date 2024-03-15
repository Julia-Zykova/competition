from django import forms

from models_app.models import Comment, Photo, CustomUser
from service_objects.services import ServiceWithResult
from service_objects.fields import ModelField


class VoteForPhotoService(ServiceWithResult):

	photo = ModelField(Photo)
	user = ModelField(CustomUser)
	text = forms.CharField(max_length=200)
	
	def process(self):
		if self.is_valid():
			photo = self.cleaned_data['photo']
			user = self.cleaned_data['user']
			text = self.cleaned_data['text']

			comment = Comment.objects.create(
				photo=photo,
				user=user,
				text=text,			
				)

		return comment
