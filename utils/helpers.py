"""
Helper utility functions
"""
import logging
import time
from typing import Callable, Any
from functools import wraps
from config import RESPONSE_TIMEOUT

logger = logging.getLogger(__name__)


def timed_function(func: Callable) -> Callable:
    """
    Decorator to time function execution and log if it exceeds timeout.

    Args:
        func: Function to time

    Returns:
        Wrapped function
    """

    @wraps(func)
    def wrapper(*args, **kwargs) -> Any:
        start_time = time.time()
        result = func(*args, **kwargs)
        execution_time = time.time() - start_time

        if execution_time > RESPONSE_TIMEOUT:
            logger.warning(
                f"Function {func.__name__} took {execution_time:.2f}s to execute, "
                f"exceeding the {RESPONSE_TIMEOUT}s timeout"
            )

        return result

    return wrapper


def truncate_text(text: str, max_length: int = 4000) -> str:
    """
    Truncate text to maximum length for Telegram messages.

    Args:
        text: Text to truncate
        max_length: Maximum length

    Returns:
        Truncated text
    """
    if len(text) <= max_length:
        return text

    return text[:max_length - 100] + "...\n\n(Response truncated due to length)"
