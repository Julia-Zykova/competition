import environ

DATABASES = {
    'default': env.db()
}