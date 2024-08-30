from django import forms
from django.db.models.query import QuerySet
from service_objects.services import ServiceWithResult

from models_app.models import Comment


class PatchCommentService(ServiceWithResult):
    comment = forms.IntegerField()
    text = forms.CharField(
        max_length=200,
        error_messages={
            "max_length": "Слишком длинный комментарий.",
            "required": "Вы не можете оставить пустой комментарий",
        },
    )

    def process(self) -> ServiceWithResult:
        if self.is_valid():
            self.result = self._update_comment
        return self

    @property
    def _comment(self) -> QuerySet[Comment]:
        return Comment.objects.filter(id=self.cleaned_data["comment"])

    @property
    def _update_comment(self) -> int:
        return self._comment.update(
            text=self.cleaned_data["text"],
        )
