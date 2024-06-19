from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django import forms

from drf.tasks import delete_photo

from models_app.models import Photo
from service_objects.services import ServiceWithResult


class SoftDeletePhotoService(ServiceWithResult):
    photo = forms.IntegerField()

    def process(self) -> ServiceWithResult:
        if self.is_valid():
            self.result = self._soft_delete
        return self

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

        import environ
        env = environ.Env()
        result = delete_photo.apply_async(
            args=[self.cleaned_data['photo']],
            countdown=int(env('TIME_BEFORE_DELETE'))
        )
        return photo
