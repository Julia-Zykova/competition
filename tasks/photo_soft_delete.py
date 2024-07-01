from conf.celery import app

from models_app.models import Voice, Comment
from models_app.models.photo.models import Photo


def _photo(photo_id):
    return Photo.objects.get(id=photo_id)


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
