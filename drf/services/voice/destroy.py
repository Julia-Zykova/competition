from typing import Optional

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django import forms
from service_objects.fields import ModelField
from service_objects.services import ServiceWithResult

from models_app.models import CustomUser, Photo, Voice


class DestroyVoiceService(ServiceWithResult):
    photo = forms.IntegerField()
    user = ModelField(CustomUser)

    def process(self) -> ServiceWithResult:
        if self.is_valid():
            self.result = self._delete_voice
        return self

    @property
    def _photo(self) -> Photo:
        return Photo.objects.get(id=self.cleaned_data["photo"])

    @property
    def _get_voice(self) -> Optional[Voice]:
        try:
            obj = Voice.all_objects.get(user=self.cleaned_data["user"], photo=self._photo)
            return obj
        except Voice.DoesNotExist:
            return None

    @property
    def _delete_voice(self) -> None:
        obj = self._get_voice
        if obj:
            self._send_message
            return obj.soft_delete()
        else:
            raise Voice.DoesNotExist

    @property
    def _send_message(self) -> None:
        channel_layer = get_channel_layer()
        author = self._photo.author
        sum_voices = self._photo.voices.count() - 1
        message = (
            f'Пользователь {self.cleaned_data["user"]} убрал свой голос с вашего фото "{self._photo.title}". '
            f"Всего голосов: {sum_voices}."
        )

        return async_to_sync(channel_layer.group_send)(
            "user_" + str(author.id), {"type": "user.message", "message": message}
        )
