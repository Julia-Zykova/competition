from django import forms

from models_app.models import Photo, Comment, Voice
from service_objects.services import ServiceWithResult


class ListOfPhotoService(ServiceWithResult):

	CHOICES = (
		(1, 'pub_date'),
		(2, '-pub_date'),
		(3, '-voices'),
		(4, 'voices'),
		(5, '-comments'),
		(6, 'comments')
		)

	sort = forms.ChoiceField(required=False, choices=CHOICES)
	search = forms.CharField(min_length = 3,max_length = 30, required=False)
	page = forms.IntegerField(min_value = 1)
	
	
	def process(self):
		sort = self.cleaned_data['sort']
		search = self.cleaned_data['search']
		page = self.cleaned_data['page']
		
