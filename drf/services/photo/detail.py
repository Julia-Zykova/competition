from django import forms
from models_app.models import Photo, CustomUser
from service_objects.services import ServiceWithResult
from service_objects.fields import ModelField
from django.core.exceptions import PermissionDenied


class DetailPhotoService(ServiceWithResult):
    photo = forms.IntegerField()
    user = ModelField(CustomUser)
    com_size = forms.IntegerField()
    custom_validations = ["is_author", ]

    def process(self):
        if self.is_valid():
            self.run_custom_validations()
            self.result = {"photo": self._photo, "comments": self._comments}
        return self

    @property
    def _photo(self):
        return Photo.objects.get(id=self.cleaned_data["photo"])

    @property
    def _comments(self):
        photo = self._photo
        return photo.comments.order_by("-created_at")[:self.cleaned_data["com_size"]]

    def is_author(self):
        if self._photo.state == "in_moderation":
            if self._photo.author == self.cleaned_data["user"]:
                return True
            else:
                raise PermissionDenied("Фото в статусе 'на модерации' может просматривать только автор")
