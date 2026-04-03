import functools
import inspect
from typing import Callable

from loguru import logger


def log_function(func: Callable) -> Callable:
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        signature = inspect.signature(func)
        bound_args = signature.bind(*args, **kwargs)
        bound_args.apply_defaults()

        logger.debug(
            f"Start calling: {func.__name__} with arguments: {dict(bound_args.arguments)}"
        )

        try:
            result = func(*args, **kwargs)
            return result
        except Exception as e:
            logger.exception("Exception occurred:")
            raise

    return wrapper
