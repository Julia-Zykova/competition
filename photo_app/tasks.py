from datetime import datetime
from conf.celery import app
from models_app.models import Voice, Comment
from models_app.models.photo.models import Photo


@app.task
def delete_photo(photo_id):
    photo = Photo.objects.get(id=photo_id)
    if photo.state == 'on_delete':
        voices = Voice.objects.filter(user=photo.author)
        voices.delete()
        comments = Comment.objects.filter(user=photo.author)
        comments.delete()
        photo.soft_delete()
    else:
        pass
