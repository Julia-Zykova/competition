from django import forms
from django.db.models.query import QuerySet

from django.db.models import Count, Q

from models_app.models.photo.models import Photo
from models_app.models.user.models import CustomUser

from service_objects.services import ServiceWithResult
from service_objects.fields import ModelField

from django.http import HttpResponseBadRequest


class ListPhotoService(ServiceWithResult):
    CHOICES = (
        ('pub_date', 'pub_date'),
        ('-pub_date', '-pub_date'),
        ('-voices', '-voices'),
        ('voices', 'voices'),
        ('-comments', '-comments'),
        ('comments', 'comments')
    )
    personal_filter_choices = {
        'in_moderation': 'На модерации',
        'approved': 'Одобрено',
        'on_delete': 'На удалении',
    }
    orderby = forms.ChoiceField(required=False, choices=CHOICES, initial='-pub_date')
    orderbysearch = forms.CharField(min_length=3, max_length=30, required=False)
    personal_list = forms.BooleanField(initial=False, required=False)
    personal_filter = forms.ChoiceField(required=False, choices=personal_filter_choices)
    user = ModelField(CustomUser, required=False)

    def process(self) -> ServiceWithResult:
        if self.is_valid():
            self.result = self._get_queryset
        else:
            raise HttpResponseBadRequest
        return self

    @property
    def _get_queryset(self) -> QuerySet[Photo]:

        qs = Photo.objects.exclude(state__in=['rejected', 'in_moderation'])
        orderby = self.cleaned_data['orderby']

        if orderby:
            if orderby in ['voice', 'comments']:
                qs = Photo.objects.exclude(state__in=['rejected', 'in_moderation']) \
                    .annotate(sum=Count(orderby)) \
                    .order_by('sum')
            elif orderby in ['-voice', '-comments']:
                qs = Photo.objects.exclude(state__in=['rejected', 'in_moderation']) \
                    .annotate(sum=Count(orderby[1:])) \
                    .order_by('-sum')
            else:
                qs = Photo.objects.exclude(state__in=['rejected', 'in_moderation']) \
                    .order_by(orderby)

        orderbysearch = self.cleaned_data['orderbysearch']
        if orderbysearch:
            qs = Photo.objects.filter(
                Q(title__icontains=orderbysearch) |
                Q(description__icontains=orderbysearch) |
                Q(author__email__icontains=orderbysearch)
            ).exclude(state__in=['rejected', 'in_moderation'])

        personal_list = self.cleaned_data['personal_list']
        if personal_list:
            qs = Photo.objects.filter(
                author=self.cleaned_data['user'],
                state__in=['in_moderation', 'approved', 'on_delete']
            )

        personal_filter = self.cleaned_data['personal_filter']
        if personal_filter:
            qs = Photo.objects.filter(author=self.cleaned_data['user'], state=personal_filter)

        return qs


