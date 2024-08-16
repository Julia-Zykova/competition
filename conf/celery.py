import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'conf.settings')
app = Celery('conf')
app.config_from_object('django.conf:settings')
# Load task modules from all registered Django app configs. 

app.autodiscover_tasks()


@app.task(task_reject_on_worker_lost=True, name='delete_inactive_users')
def delete_inactive_users():
    from models_app.models import CustomUser

    users = CustomUser.objects.prefetch_related("voices", "comments", "photos").filter(is_active=False)

    for user in users:
        if user.voices.count() == 0 and user.comments.count() == 0 and user.photos.count() == 0:
            user.delete()


app.conf.beat_schedule = {
    'delete_inactive_users': {
        'task': 'delete_inactive_users',
        'schedule': crontab(hour=9, minute=57),
    },
}
app.conf.timezone = 'Europe/Moscow'
