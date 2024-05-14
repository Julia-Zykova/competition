from django import forms

from photo_app.services.comment.show_comments import ShowCommentsService
from service_objects.services import ServiceWithResult, ServiceOutcome


class DetailPhotoService(ServiceWithResult):
    photo = forms.IntegerField()
    page = forms.IntegerField(min_value=1, initial=1, required=False)

    def process(self):
        if self.is_valid():
            self.result = {
                'outcome_comments': self._comments
            }
        return self

    @property
    def _comments(self):
        outcome = ServiceOutcome(
            ShowCommentsService, {
                'photo': self.cleaned_data['photo'], 'page': self.cleaned_data['page'], 'detail_photo': True
            })
        return outcome.result
