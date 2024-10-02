import logging

from prefect import context


def log(message: str, level: str = "info") -> None:
    """Log a message to prefect logger."""
    levels = {
        "debug": logging.DEBUG,
        "info": logging.INFO,
        "warning": logging.WARNING,
        "error": logging.ERROR,
        "critical": logging.CRITICAL,
    }

    if level not in levels:
        msg = f"Invalid log level: {level}"
        raise ValueError(msg)

    context.logger.log(levels[level], message)
