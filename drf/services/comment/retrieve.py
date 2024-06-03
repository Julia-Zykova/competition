from django import forms

from service_objects.services import ServiceWithResult

from drf.serializers import CommentRetrieveSerializer
from models_app.models import Comment


class RetrieveCommentService(ServiceWithResult):
    comment = forms.IntegerField()

    def process(self):
        if self.is_valid():
            self.result = self._comment
        return self

    @property
    def _comment(self):
        return Comment.objects.get(id=self.cleaned_data['comment'])
