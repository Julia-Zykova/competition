import logging.config

import environ

from conf.settings.django import BASE_DIR

env = environ.Env()

LOG_REQUEST_ID_HEADER = "HTTP_X_REQUEST_ID"
GENERATE_REQUEST_ID_IF_NOT_IN_HEADER = True


LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "filters": {
        "require_debug_true": {
            "()": "django.utils.log.RequireDebugTrue",
        },
        "request_id": {
            "()": "log_request_id.filters.RequestIDFilter",
        },
    },
    "formatters": {
        "verbose": {
            "format": "%(levelname)s - %(asctime)s - %(request_id)s - %(module)s - %(funcName)s: %(message)s",
            "datefmt": env("LOG_DATETIME_FORMAT"),
        },
        "rich": {
            "format": "%(request_id)s %(message)s",
            "datefmt": "[%X]",
        },
    },
    "handlers": {
        "console": {
            "level": getattr(logging, env("LOG_LEVEL_CONSOLE", default="DEBUG")),
            "class": "rich.logging.RichHandler",
            "filters": ["require_debug_true", "request_id"],
            "formatter": "rich",
        },
        "file": {
            "level": "INFO",
            "class": "logging.FileHandler",
            "filters": ["request_id"],
            "filename": BASE_DIR + env("LOG_FILE_NAME", default="/default.log"),
            "formatter": "verbose",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": getattr(logging, env("LOG_LEVEL_ROOT", default="WARNING")),
    },
    "loggers": {
        "django": {
            "handlers": ["console"],
            "propagate": True,
        },
        "django.request": {
            "handlers": ["console", "file"],
            "level": getattr(logging, env("LOG_LEVEL_REQUEST", default="WARNING")),
            "propagate": False,
        },
        "django.db.backends": {
            "level": getattr(logging, env("LOG_LEVEL_DB", default="DEBUG")),
            "handlers": [
                "console",
            ],
            "propagate": False,
        },
        "myproject.custom": {
            "handlers": ["console", "file"],
            "level": getattr(logging, env("LOG_LEVEL_CUSTOM", default="WARNING")),
        },
    },
}
