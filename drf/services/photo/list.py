from django import forms
from django.db.models.query import QuerySet

from django.db.models import Count, Q

from models_app.models.photo.models import Photo
from models_app.models.user.models import CustomUser

from service_objects.services import ServiceWithResult
from service_objects.fields import ModelField

from functools import lru_cache, cached_property


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
        return self

    @cached_property
    @lru_cache
    def _get_photos_state(self):
        return (Photo.objects.exclude(state__in=['rejected', 'in_moderation'])
                .select_related("author"))

    @cached_property
    @lru_cache
    def _get_photos_sum_voices_comments(self):
        return self._get_photos_state.prefetch_related("voices__is_deleted").annotate(
            sum_voices=Count("voices", filter=Q(voices__is_deleted=False)),
            sum_comments=Count("comments")
        )

    @cached_property
    @lru_cache
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

    @cached_property
    @lru_cache
    def _search(self):
        orderbysearch = self.cleaned_data['orderbysearch']
        if orderbysearch:
            return self._get_photos_state.filter(
                Q(title__icontains=orderbysearch) |
                Q(description__icontains=orderbysearch) |
                Q(author__email__icontains=orderbysearch)
            )

    @cached_property
    @lru_cache
    def _personal_list(self) -> QuerySet[Photo]:
        personal_list = self.cleaned_data['personal_list']
        if personal_list:
            return Photo.objects.select_related("author").filter(
                author=self.cleaned_data['user'],
                state__in=['in_moderation', 'approved', 'on_delete']
            )

    @cached_property
    @lru_cache
    def _personal_filter(self) -> QuerySet[Photo]:
        personal_filter = self.cleaned_data['personal_filter']
        if personal_filter:
            return Photo.objects.select_related("author").filter(author=self.cleaned_data['user'],
                                                                 state=personal_filter)

    @cached_property
    @lru_cache
    def _get_queryset(self) -> QuerySet[Photo]:
        if self.cleaned_data['orderby']:
            return self._sort_by
        elif self.cleaned_data['orderbysearch']:
            return self._search
        elif self.cleaned_data['personal_list']:
            return self._personal_list
        elif self.cleaned_data['personal_filter']:
            self._personal_filter
        else:
            return self._get_photos_state
