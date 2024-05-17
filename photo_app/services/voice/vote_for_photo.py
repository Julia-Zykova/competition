from asgiref.sync import async_to_sync
from django import forms
from models_app.models import Voice, Photo, CustomUser
from service_objects.services import ServiceWithResult
from service_objects.fields import ModelField
from channels.layers import get_channel_layer


class VoteForPhotoService(ServiceWithResult):
    photo = forms.IntegerField()
    user = ModelField(CustomUser)

    def process(self):
        if self.is_valid():
            self.result = self._voice
        return self

    @property
    def _photo(self):
        photo = Photo.objects.get(id=self.cleaned_data['photo'])
        if photo.state == 'approved':
            return photo
        else:
            raise forms.ValidationError("Вы не можете поставить голос к этому фото")

    @property
    def _voice(self):
        channel_layer = get_channel_layer()
        author = self._photo.author

        try:
            obj = Voice.objects.get(user=self.cleaned_data["user"], photo=self._photo)
            obj.delete()
            sum_voices = self._photo.voices.count()
            message = (
                f'Пользователь {self.cleaned_data["user"]} убрал свой голос с вашего фото "{self._photo.title}". '
                f'Всего голосов: {sum_voices}.')

        except Voice.DoesNotExist:
            obj = Voice.objects.create(
                photo=self._photo,
                user=self.cleaned_data['user'],
            )
            sum_voices = self._photo.voices.count()
            message = (f'Пользователь {self.cleaned_data["user"]} проголосовал за ваше фото "{self._photo.title}". '
                       f'Всего голосов: {sum_voices}.')

        finally:
            async_to_sync(channel_layer.group_send)(
                'user_' + str(author.id),
                {
                    'type': 'user.message',
                    'message': message
                }
            )

        return obj
