import os
from celery import Celery
from celery.schedules import crontab


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'conf.settings')
app = Celery('conf')
app.config_from_object('django.conf:settings')
# Load task modules from all registered Django app configs. 
app.autodiscover_tasks()

app.conf.beat_schedule = {
    # Executes every Monday morning at 7:30 a.m.
    'add-every-day': {
        'task': 'tasks.delete_inactive_users',
        'schedule': crontab(hour=13, minute=50),
    },
}
app.conf.timezone = 'Europe/Moscow'
