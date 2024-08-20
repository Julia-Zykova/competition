from split_settings.tools import include

include(
    "django.py",
    "database.py",
    "restframework.py",
    "redis.py",
    "celery.py",
    "django_allauth.py",
    "logger.py",
    "websocket.py",
    "swagger.py",
)
