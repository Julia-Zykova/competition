import environ

from conf.settings.redis import REDIS_URL

env = environ.Env()

CELERY_BROKER_TRANSPORT_OPTIONS = {'visibility_timeout': int(env('VISIBILITY_TIMEOUT'))}
BROKER_URL = REDIS_URL + "/0"
CELERY_RESULT_BACKEND = REDIS_URL + "/0"