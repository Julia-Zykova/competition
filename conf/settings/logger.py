import logging.config
import environ

from conf.settings.django import BASE_DIR

env = environ.Env()


LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "{levelname} - {asctime} - {module} - {funcName}: {message}",
            "datefmt": env("LOG_DATETIME_FORMAT"),
            "style": "{",
        },
        "simple": {
            "format": "{levelname} {message}",
            "datefmt": env("LOG_DATETIME_FORMAT"),
            "style": "{",
        },
    },
    "filters": {
        "require_debug_true": {
            "()": "django.utils.log.RequireDebugTrue",
        },
    },
    "handlers": {
        "console": {
            "level": "INFO",
            "filters": ["require_debug_true"],
            "class": "logging.StreamHandler",
            "formatter": "simple",
        },
        "file": {
            "level": "INFO",
            "class": "logging.FileHandler",
            "filename": BASE_DIR + env("LOG_FILE_NAME"),
            "formatter": "verbose",
        },
    },
    "root": {
            "handlers": ["console"],
            "level": getattr(logging, env("LOG_LEVEL_ROOT")),
    },
    "loggers": {
        "django": {
            "handlers": ["console"],
            "propagate": True,
        },
        "django.request": {
            "handlers": ["console", "file"],
            "level": getattr(logging, env("LOG_LEVEL_REQUEST")),
            "propagate": False,
        },
        "myproject.custom": {
            "handlers": ["console", "file"],
            "level": getattr(logging, env("LOG_LEVEL_CUSTOM")),
        },
    },
}