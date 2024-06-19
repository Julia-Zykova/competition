from conf.celery import app

from models_app.models import Voice, Comment
from models_app.models.photo.models import Photo

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer


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
def delete_photo(photo_id):
    photo = _photo(photo_id)
    if photo.state == 'on_delete':
        voices = Voice.objects.filter(user=photo.author)
        voices.delete()
        comments = Comment.objects.filter(user=photo.author)
        comments.delete()
        photo.soft_delete()

    else:
        pass


@app.task(task_reject_on_worker_lost=True)
def reject_photo(photo_id):
    photo = _photo(photo_id)
    if photo.state == 'in_moderation':
        photo.reject()
        photo.save()
        _send_message(photo)

        import environ
        env = environ.Env()
        result = reject_photo.apply_async(
            args=[photo.id],
            countdown=int(env('TIME_BEFORE_DELETE_REJECTED_PHOTO'))
        )

    else:
        pass


@app.task(task_reject_on_worker_lost=True)
def delete_rejected_photo(photo_id):
    photo = photo_id
    if photo.state == 'rejected':
        photo.soft_delete()
    else:
        pass
