from typing import Callable
from loguru import logger


def error_handler(func: Callable):
    def inner_function(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except BaseException as e:
            logger.exception(e)

    return inner_function
