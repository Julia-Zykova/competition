import logging
import environ

env = environ.Env()

logging.basicConfig(
    filename=env("LOG_FILE_NAME"),
    level=getattr(logging, env("LOG_LEVEL")),
    format=env("LOG_FORMAT"),
    datefmt=env("LOG_DATETIME_FORMAT"),
)
