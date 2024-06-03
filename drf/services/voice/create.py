from asgiref.sync import async_to_sync
from django import forms
from models_app.models import Voice, Photo, CustomUser
from service_objects.services import ServiceWithResult
from service_objects.fields import ModelField
from channels.layers import get_channel_layer


class CreateVoiceService(ServiceWithResult):
    photo = forms.IntegerField()
    user = ModelField(CustomUser)
    custom_validations = ["is_vote", "is_approved"]

    def process(self):
        if self.is_valid():
            self.run_custom_validations()
            self.result = self._voice
        return self

    @property
    def _photo(self):
        return Photo.objects.get(id=self.cleaned_data['photo'])

    @property
    def _voice(self):
        channel_layer = get_channel_layer()
        author = self._photo.author

        obj = Voice.objects.create(
            photo=self._photo,
            user=self.cleaned_data['user'],
        )
        sum_voices = self._photo.voices.count()
        message = (f'Пользователь {self.cleaned_data["user"]} проголосовал за ваше фото "{self._photo.title}". '
                   f'Всего голосов: {sum_voices}.')

        async_to_sync(channel_layer.group_send)(
            'user_' + str(author.id),
            {
                'type': 'user.message',
                'message': message
            }
        )
        return obj

    def is_vote(self):
        try:
            obj = Voice.objects.get(user=self.cleaned_data["user"], photo=self._photo)
            return False
        except Voice.DoesNotExist:
            return True

    def is_approved(self):
        if self._photo.state != 'approved':
            raise forms.ValidationError("Вы не можете поставить голос к этому фото")
        else:
            return True
