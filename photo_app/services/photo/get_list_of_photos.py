from django import forms
from django.db.models.query import QuerySet
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

    @property
    def _get_photos_state(self):
        return Photo.objects.exclude(state__in=['rejected', 'in_moderation'])

    @property
    def _get_photos_sum_voices_comments(self):
        return self._get_photos_state.annotate(
            sum_voices=Count("voices", filter=Q(voices__is_deleted=False)),
            sum_comments=Count("comments")
        )

    @property
    def _sort_by(self) -> QuerySet[Photo]:
        orderby = self.cleaned_data['orderby']
        if orderby == 'voices':
            return self._get_photos_sum_voices_comments.order_by('sum_voices', '-pub_date')
        elif orderby == '-voices':
            return self._get_photos_sum_voices_comments.order_by('-sum_voices', '-pub_date')
        elif orderby == 'comments':
            return self._get_photos_sum_voices_comments.order_by('sum_comments', '-pub_date')
        elif orderby == '-comments':
            return self._get_photos_sum_voices_comments.order_by('-sum_comments', '-pub_date')
        else:
            return self._get_photos_sum_voices_comments.order_by(orderby)

    @property
    def _search(self):
        orderbysearch = self.cleaned_data['orderbysearch']
        if orderbysearch:
            return self._get_photos_state.filter(
                Q(title__icontains=orderbysearch) |
                Q(description__icontains=orderbysearch) |
                Q(author__email__icontains=orderbysearch)
            )

    @property
    def _personal_list(self) -> QuerySet[Photo]:
        personal_list = self.cleaned_data['personal_list']
        if personal_list:
            return Photo.objects.filter(
                author=self.cleaned_data['user'],
                state__in=['in_moderation', 'approved', 'on_delete']
            )

    @property
    def _personal_filter(self) -> QuerySet[Photo]:
        return Photo.objects.filter(author=self.cleaned_data['user'], state=self.cleaned_data['personal_filter'])

    @property
    def _get_queryset(self) -> QuerySet[Photo]:

        if self.cleaned_data['orderby']:
            return self._sort_by
        elif self.cleaned_data['orderbysearch']:
            return self._search
        elif self.cleaned_data['personal_list']:
            if self.cleaned_data['personal_filter']:
                return self._personal_filter
            else:
                return self._personal_list

        else:
            return self._get_photos_state

    @property
    def _get_page(self):

        qs = self._get_queryset
        p = Paginator(qs, 8)

        page_number = self.cleaned_data['page']

        if page_number is None:
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
            "page_obj": page_obj,
            "page_number": page_number,
            "personal_list": self.cleaned_data['personal_list'],
            "personal_filter": self.cleaned_data['personal_filter']
        }
