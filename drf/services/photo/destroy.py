import logging
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django import forms

from typing import Optional
from django.core.exceptions import PermissionDenied

from tasks.delete_photo import delete_photo

from models_app.models import Photo, CustomUser
from service_objects.services import ServiceWithResult
from conf.settings.celery import TIME_BEFORE_DELETE


class SoftDeletePhotoService(ServiceWithResult):
    photo = forms.IntegerField()
    user = forms.IntegerField(required=False)
    custom_validations = ["is_author", ]

    def process(self) -> ServiceWithResult:
        if self.is_valid():
            self.result = self._soft_delete
        return self

    @property
    def _user(self) -> CustomUser:
        return CustomUser.objects.get(id=self.cleaned_data["user"])

    @property
    def _photo(self) -> Photo:
        return Photo.objects.get(id=self.cleaned_data['photo'])

    @property
    def _send_message(self) -> None:
        photo = self._photo
        channel_layer = get_channel_layer()
        users_list = []
        users_list += [comment.get('user_id') for comment in photo.comments.all().values()]
        users_set = set(users_list)
        message = f'Фотография "{photo.title}" отправлена на удаление. Ваши комментарии к нему скоро будут удалены.'

        for user in users_set:
            async_to_sync(channel_layer.group_send)(
                'user_' + str(user),
                {
                    'type': 'user.message',
                    'message': message
                }
            )

    @property
    def _soft_delete(self) -> Photo:
        photo = self._photo
        photo.remove_photo()
        photo.save()

        result = delete_photo.apply_async(
            args=[self.cleaned_data['photo']],
            countdown=TIME_BEFORE_DELETE
        )
        return photo

    def is_author(self) -> Optional[bool]:
        if self._photo.author == self._user:
            return True
        else:
            logging.exception("Удалить фото может только автор", exc_info=True)
            raise PermissionDenied("Вы не можете удалить чужое фото")
