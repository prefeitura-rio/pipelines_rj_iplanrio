import logging
import os

import prefect


def log(msg: str, level: str = "info") -> None:
    """Logs a message to prefect's logger."""
    levels = {
        "debug": logging.DEBUG,
        "info": logging.INFO,
        "warning": logging.WARNING,
        "error": logging.ERROR,
        "critical": logging.CRITICAL,
    }

    if level not in levels:
        raise ValueError(f"Invalid log level: {level}")

    prefect.context.logger.log(levels[level], msg)


def get_env_variable(env: str) -> str:
    """Get an environment variable"""
    if env in os.environ:
        return os.environ[env]
    raise ValueError(f"{env} not found in environment variables")
