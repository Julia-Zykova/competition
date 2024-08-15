from conf.celery import app


@app.task(task_reject_on_worker_lost=True, name='delete_inactive_users')
def delete_inactive_users():
    from models_app.models import CustomUser

    users = CustomUser.objects.prefetch_related("voices", "comments", "photos").filter(is_active=False)

    for user in users:
        if user.voices.count() == 0 and user.comments.count() == 0 and user.photos.count() == 0:
            user.delete()
