import os


def get_env_variable(name: str) -> str:
    """Get an environment variable by name."""
    if name not in os.environ:
        msg = f"Environment variable {name} not found"
        raise ValueError(msg)

    return os.environ[name]
