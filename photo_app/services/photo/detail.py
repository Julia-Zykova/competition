from django import forms
from django.http import HttpResponse, JsonResponse
from django.urls import reverse_lazy
from django.db.models import Count, Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.exceptions import ValidationError

from models_app.models.photo.models import Photo
from models_app.models.comment.models import Comment

from photo_app.services.comment.show_comments import ShowCommentsService
from service_objects.services import ServiceWithResult, ServiceOutcome
from service_objects.fields import ModelField

class DetailPhotoService(ServiceWithResult):
    
    photo = forms.IntegerField()
    page = forms.IntegerField(min_value = 1, initial = 1, required = False)

    def process(self):
        if self.is_valid():
            self.result = {
            'outcome_comments': self._comments
            }   
        return self     

    @property
    def _photo(self):
        return Photo.objects.get(id = self.cleaned_data['photo'])

    @property
    def _comments(self):
        outcome = ServiceOutcome(
            ShowCommentsService, {
            'photo': self.cleaned_data['photo'], 'page': self.cleaned_data['page'], "detail_photo": True
            })
        return outcome.result

