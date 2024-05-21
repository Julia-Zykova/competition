import os
import environ

from pathlib import Path


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

env = environ.Env()

# read the .env file
environ.Env.read_env(env_file=str(BASE_DIR) + '/.env')    

SECRET_KEY = env('SECRET_KEY')

DEBUG = env('DEBUG')

ALLOWED_HOSTS = ['*']


INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'daphne',
    'django.contrib.staticfiles',
    'channels',
    'rest_framework',
    'rest_framework.authtoken',
    'widget_tweaks',
    'imagekit',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.vk',

    'models_app.apps.ModelsAppConfig',
    'photo_app.apps.PhotoAppConfig',
    'notifications_app.apps.NotificationsAppConfig',
    'drf.apps.DrfConfig',
]


AUTH_USER_MODEL = 'models_app.CustomUser'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'allauth.account.middleware.AccountMiddleware',
]

ROOT_URLCONF = 'conf.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
        BASE_DIR, 'templates',
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
    ]


WSGI_APPLICATION = 'conf.wsgi.application'
ASGI_APPLICATION = 'conf.asgi.application'


AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LANGUAGE_CODE = 'ru'

TIME_ZONE = 'Europe/Moscow'

USE_I18N = True

USE_TZ = True



STATIC_URL = env('STATIC_URL')

STATIC_ROOT = os.path.join(BASE_DIR,env('STATIC_ROOT'))

MEDIA_URL = env('MEDIA_URL')

MEDIA_ROOT = os.path.join(BASE_DIR,env('MEDIA_ROOT'))

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


ACCOUNT_USER_MODEL_USERNAME_FIELD = None
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_AUTHENTICATION_METHOD = 'email'
SOCIALACCOUNT_AUTO_SIGNUP = True
SOCIALACCOUNT_LOGIN_ON_GET = True
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = 'none'

DJANGO_ACCOUNT_ALLOW_REGISTRATION = True
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'

REDIS_HOST = env('REDIS_HOST')
REDIS_PORT = env('REDIS_PORT')
REDIS_URL = f'redis://{REDIS_HOST}:{REDIS_PORT}'

CELERY_BROKER_TRANSPORT_OPTIONS = {'visibility_timeout': int(env('VISIBILITY_TIMEOUT'))}
BROKER_URL = REDIS_URL + "/0"
CELERY_RESULT_BACKEND = REDIS_URL + "/0"

CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts": [(REDIS_HOST, int(REDIS_PORT))],
        },
    },
}