from conf.celery import app
from models_app.models import Photo


def _photo(photo_id):
    return Photo.objects.get(id=photo_id)


@app.task(task_reject_on_worker_lost=True)
def delete_rejected_photo(photo_id):
    photo = _photo(photo_id)
    if photo.state == 'rejected' and photo.is_deleted is not True:
        photo.soft_delete()
    else:
        pass
