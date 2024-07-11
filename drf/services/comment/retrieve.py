from django import forms

from service_objects.services import ServiceWithResult

from models_app.models import Comment


class RetrieveCommentService(ServiceWithResult):
    comment = forms.IntegerField()

    def process(self) -> ServiceWithResult:
        if self.is_valid():
            self.result = self._comment
        return self

    @property
    def _comment(self) -> Comment:
        return Comment.objects.get(id=self.cleaned_data['comment'])
