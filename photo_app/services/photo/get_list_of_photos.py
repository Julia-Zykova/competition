from django import forms

from django.db.models import Count, Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from models_app.models.photo.models import Photo
from models_app.models.user.models import CustomUser

from service_objects.services import ServiceWithResult
from service_objects.fields import ModelField


class ListOfPhotoService(ServiceWithResult):
    CHOICES = (
        ('pub_date', 'pub_date'),
        ('-pub_date', '-pub_date'),
        ('-voices', '-voices'),
        ('voices', 'voices'),
        ('-comments', '-comments'),
        ('comments', 'comments')
    )

    orderby = forms.ChoiceField(required=False, choices=CHOICES, initial='-pub_date')
    orderbysearch = forms.CharField(min_length=3, max_length=30, required=False)
    page = forms.IntegerField(min_value=1, initial=1, required=False)
    personal_list = forms.BooleanField(initial=False, required=False)
    personal_filter = forms.CharField(required=False)
    user = ModelField(CustomUser, required=False)

    def process(self):
        if self.is_valid():
            self.result = self._get_page
        return self

    def get_queryset(self):

        qs = Photo.objects.exclude(state__in=['rejected', 'in_moderation'])

        orderby = self.cleaned_data['orderby']
        if orderby:
            if orderby in ['voices', 'comments']:
                qs = Photo.objects.exclude(state__in=['rejected', 'in_moderation']) \
                    .annotate(sum=Count(orderby)) \
                    .order_by('sum', '-pub_date')
            elif orderby in ['-voices', '-comments']:
                qs = Photo.objects.exclude(state__in=['rejected', 'in_moderation']) \
                    .annotate(sum=Count(orderby[1:])) \
                    .order_by('-sum', '-pub_date')
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

    @property
    def _get_page(self):

        qs = self.get_queryset()
        p = Paginator(qs, 8)
        page_number = self.cleaned_data['page']
        if page_number == None:
            page_number = self.fields['page'].initial

        try:
            page_obj = p.get_page(page_number)  # returns the desired page object
        except PageNotAnInteger:
            # if page_number is not an integer then assign the first page
            page_obj = p.page(1)
        except EmptyPage:
            # if page is empty then return last page
            page_obj = p.page(p.num_pages)

        return {
            "page_number": page_number, "page_obj": page_obj,
            "personal_list": self.cleaned_data['personal_list'],
            "personal_filter": self.cleaned_data['personal_filter']
        }
