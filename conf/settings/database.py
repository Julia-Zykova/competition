import environ
SOCIAL_AUTH_JSONFIELD_ENABLED = True
env = environ.Env()
DATABASES = {
    'default': env.db()
}