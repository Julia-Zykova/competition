from django import forms

from service_objects.fields import ModelField
from service_objects.services import ServiceWithResult

from models_app.models import Voice, Photo, Comment, CustomUser


class IsOwnerService(ServiceWithResult):
    user = ModelField(CustomUser)
    photo = forms.IntegerField()
    comment = forms.IntegerField(required=False)
    voice = forms.IntegerField(required=False)

    def process(self) -> ServiceWithResult:
        if self.is_valid():
            self.result = self.is_owner
        return self

    @property
    def _photo(self) -> Photo:
        return Photo.objects.get(id=self.cleaned_data['photo'])

    @property
    def _voice(self) -> bool:
        try:
            obj = Voice.objects.get(id=self.cleaned_data['voice'])
            return True
        except Voice.DoesNotExist:
            return False

    @property
    def _comment(self) -> bool:
        try:
            obj = Comment.objects.get(id=self.cleaned_data['comment'])
            return True
        except Comment.DoesNotExist:
            return False

    @property
    def is_owner(self) -> bool:
        if self.cleaned_data['voice'] and self._voice:
            owner = CustomUser.objects.get(voices=self.cleaned_data['voice'])
        elif self.cleaned_data['comment'] and self._comment:
            owner = CustomUser.objects.get(comments=self.cleaned_data['comment'])
        else:
            owner = CustomUser.objects.get(photos=self.cleaned_data['photo'])

        return owner.auth_token.key == self.cleaned_data['user'].auth_token.key
