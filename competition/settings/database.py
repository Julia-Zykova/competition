import environ
SOCIAL_AUTH_JSONFIELD_ENABLED = True
DATABASES = {
    'default': env.db()
}