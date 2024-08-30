from conf.settings.django import env

CELERY_BROKER_TRANSPORT_OPTIONS = {"visibility_timeout": int(env("VISIBILITY_TIMEOUT"))}
BROKER_URL = "redis://" + env("REDIS_HOST") + ":" + env("REDIS_PORT") + "/0"
CELERY_RESULT_BACKEND = "redis://" + env("REDIS_HOST") + ":" + env("REDIS_PORT") + "/0"
broker_connection_retry_on_startup = True
CELERY_BEAT_SCHEDULER = "django_celery_beat.schedulers:DatabaseScheduler"

TIME_BEFORE_DELETE = env("TIME_BEFORE_DELETE", cast=int)
