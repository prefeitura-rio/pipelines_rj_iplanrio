import logging
import os

import prefect


def get_env_variable(name: str) -> str:
    """Get an environment variable by name."""
    if name not in os.environ:
        msg = f"Environment variable {name} not found"
        raise ValueError(msg)

    return os.environ[name]


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

    prefect.context.logger.log(levels[level], message)
