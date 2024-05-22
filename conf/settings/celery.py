import environ

env = environ.Env()

CELERY_BROKER_TRANSPORT_OPTIONS = {'visibility_timeout': int(env('VISIBILITY_TIMEOUT'))}
BROKER_URL = "redis://" + env('REDIS_HOST') + ":" + env('REDIS_PORT') + "/0"
CELERY_RESULT_BACKEND = "redis://" + env('REDIS_HOST') + ":" + env('REDIS_PORT') + "/0"
