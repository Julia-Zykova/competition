from django import forms
from service_objects.services import ServiceWithResult

from models_app.models import Comment


class DeleteCommentService(ServiceWithResult):
    comment = forms.IntegerField()

    def process(self):
        if self.is_valid():
            self.result = self._delete
        return self

    @property
    def _comment(self):
        return Comment.objects.get(id=self.cleaned_data["comment"])

    @property
    def _delete(self):
        if not self._comment.comments.get_queryset():
            self._comment.delete()
        else:
            pass
