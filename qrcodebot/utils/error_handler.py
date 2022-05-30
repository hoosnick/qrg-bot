from typing import Callable
from loguru import logger


def error_handler(func: Callable):
    def inner_function(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except Exception as e:
            logger.debug(f'{type(e).__name__}: {e}')

    return inner_function
