from django import forms
from django.db.models.query import QuerySet
from service_objects.services import ServiceWithResult

from models_app.models import Comment


class ListCommentsService(ServiceWithResult):
    photo = forms.IntegerField(required=False)

    def process(self) -> ServiceWithResult:
        if self.is_valid():
            self.result = self._get_queryset
        return self

    @property
    def _get_queryset(self) -> QuerySet[Comment]:
        return Comment.objects.filter(photo__id=self.cleaned_data["photo"])
