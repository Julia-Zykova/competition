from split_settings.tools import include


include(
'celery.py',
    'database.py',
    'django.py',
    'django_allauth.py'
    'redis.py',
    'restframework.py',
    'websocket.py',
)
