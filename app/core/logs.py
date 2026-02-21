import logging
from logging import Logger
from sys import stdout
import sys
import logging_loki
from app.core import config


def setup_logger():
    if not config.settings.LOG_ENABLED:
        return

    if config.settings.LOG_ENABLED and config.settings.LOG_LOKI_URL == "":
        logging.basicConfig(
            format="{asctime} - {levelname} - {message}",
            style="{",
            datefmt="%Y-%m-%d %H:%M",
        )
        return

    loki_handler = logging_loki.LokiHandler(
        url=config.settings.LOG_LOKI_URL,
        tags={
            "application": config.settings.app_name,
        },
        version="2",
    )

    logger = logging.getLogger(config.settings.app_name)
    logger.setLevel(logging.INFO)

    if config.settings.LOG_LEVEL == config.LogLevels.Debug:
        logger.setLevel(logging.DEBUG)

    # stdout_handler = logging.StreamHandler(stream=sys.stdout)

    logger.addHandler(loki_handler)
    # logger.addHandler(stdout_handler)


def get_logger() -> Logger:
    logger = logging.getLogger(config.settings.app_name)

    return logger
