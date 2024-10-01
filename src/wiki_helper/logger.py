import logging


def setup_logger() -> logging.Logger:
    logging.basicConfig(level=logging.INFO)

    logging.config.dictConfig(
        {
            "version": 1,
            "disable_existing_loggers": False,
            "handlers": {
                "console": {
                    "class": "logging.StreamHandler",
                    "formatter": "default",
                    "level": "INFO",
                },
            },
            "formatters": {
                "default": {
                    "format": "%(asctime)s %(levelname)s %(lineno)d:%(filename)s(%(process)d) - %(message)s",
                },
            },
            "loggers": {
                "": {
                    "handlers": ["console"],
                    "level": "INFO",
                },
                "httpx": {
                    "level": "WARNING",
                    "handlers": ["console"],
                    "propagate": False,
                },
                "wikipediaapi": {
                    "level": "WARNING",
                    "handlers": ["console"],
                    "propagate": False,
                },
                "chromadb": {
                    "level": "WARNING",
                    "handlers": ["console"],
                    "propagate": False,
                },
                "llama_index": {
                    "level": "WARNING",
                    "handlers": ["console"],
                    "propagate": False,
                },
            },
        }
    )

    logger = logging.getLogger(__name__)
    logger.info("Logger configured successfully.")

    return logger
