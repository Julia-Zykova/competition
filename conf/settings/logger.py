import logging.config
import environ

env = environ.Env()

logging.basicConfig(
    filename=env("LOG_FILE_NAME"),
    level=getattr(logging, env("LOG_LEVEL")),
    format=env("LOG_FORMAT"),
    datefmt=env("LOG_DATETIME_FORMAT"),
)

# LOGGING_CONFIG = None
#
# LOGGING = {
#     "version": 1,
#     "disable_existing_loggers": False,
#     "handlers": {
#         "file": {
#             "level": env("LOG_LEVEL"),
#             "class": "logging.FileHandler",
#             "filename": env("LOG_FILE_NAME"),
#         },
#     },
#     "root": {
#         "handlers": ["console"],
#         "level": env("LOG_LEVEL_ROOT"),
#     },
#     "loggers": {
#         "django": {
#             "handlers": ["file"],
#             "level": env("LOG_LEVEL"),
#             "propagate": True,
#         },
#     },
# }
#
# logging.config.dictConfig(LOGGING)
