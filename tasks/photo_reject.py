from conf.celery import app

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

from models_app.models import Photo
from tasks.delete_photo_after_reject import delete_rejected_photo


def _photo(photo_id):
    return Photo.objects.get(id=photo_id)


def _send_message(photo):
    channel_layer = get_channel_layer()
    author = photo.author

    message = f'Ваше фото "{photo.title}" было отклонено'
    async_to_sync(channel_layer.group_send)(
        'user_' + str(author.id),
        {
            'type': 'user.message',
            'message': message
        }
    )


@app.task(task_reject_on_worker_lost=True)
def reject_photo(photo_id):
    photo = _photo(photo_id)
    if photo.state == 'in_moderation':
        photo.reject()
        photo.save()
        _send_message(photo)
        import environ
        env = environ.Env()
        result = delete_rejected_photo.apply_async(
            args=[photo_id], countdown=int(env("TIME_BEFORE_DELETE_REJECTED_PHOTO"))
        )

    else:
        pass
