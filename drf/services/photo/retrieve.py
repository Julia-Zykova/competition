import logging
from typing import Optional

from django import forms
from django.db.models.query import QuerySet
from models_app.models import Photo, CustomUser, Comment
from service_objects.services import ServiceWithResult

from django.core.exceptions import PermissionDenied


class DetailPhotoService(ServiceWithResult):
    photo = forms.IntegerField()
    user = forms.IntegerField(required=False)
    com_size = forms.IntegerField(required=False)
    custom_validations = ["is_author", ]

    def process(self) -> ServiceWithResult:
        if self.is_valid():
            self.run_custom_validations()
            self.result = {"photo": self._photo, "comments": self._comments}
        return self

    @property
    def _user(self) -> CustomUser:
        return CustomUser.objects.get(id=self.cleaned_data["user"])

    @property
    def _photo(self) -> Photo:
        return Photo.objects.select_related("author").prefetch_related("comments").get(id=self.cleaned_data["photo"])

    @property
    def _comments(self) -> QuerySet[Comment]:
        if self.cleaned_data["com_size"]:
            return self._photo.comments.order_by("-created_at")[:self.cleaned_data["com_size"]]
        else:
            return self._photo.comments.order_by("-created_at")[:3]

    def is_author(self) -> Optional[bool]:
        if self._photo.state == "in_moderation":
            if self._photo.author == self._user:
                return True
            else:
                logging.exception("Фото в статусе 'на модерации' может просматривать только автор", exc_info=True)
                raise PermissionDenied("Фото в статусе 'на модерации' может просматривать только автор")
