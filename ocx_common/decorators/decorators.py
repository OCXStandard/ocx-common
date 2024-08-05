#  Copyright (c) 2024.  OCX Consortium https://3docx.org. See the LICENSE
"""Reusable decorators"""

# System imports
import time

# Third party imports
from loguru import logger


def timer(func):
    """@timer decorator"""

    def wrapper(*args, **kwargs):
        # start the timer
        start_time = time.time()
        # call the decorated function
        result = func(*args, **kwargs)
        # remeasure the time
        end_time = time.time()
        # compute the elapsed time and print it
        execution_time = end_time - start_time
        print(f"Execution time: {execution_time} seconds")
        # return the result of the decorated function execution
        return result

    # return reference to the wrapper function
    return wrapper


def exception_handler(func, exception_to_raise: BaseException):
    """@exception_handler decorator"""

    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            # Handle the exception
            print(f"An exception occurred: {str(e)}")
            logger.exception(f"An exception occurred: {str(e)}")
            # Optionally, perform additional error handling or logging
            # Reraise the exception if needed
            raise exception_to_raise from e

    return wrapper


def debugger(func):
    """@debug decorator"""

    def wrapper(*args, **kwargs):
        # print the function name and arguments
        print(f"Calling {func.__name__} with args: {args} kwargs: {kwargs}")
        # call the function
        result = func(*args, **kwargs)
        # print the results
        print(f"{func.__name__} returned: {result}")
        logger.debug(f"{func.__name__} returned: {result}")
        return result

    return wrapper


def memoize(func):
    """@memoize decorator"""
    cache = {}

    def wrapper(*args, **kwargs):
        if args in cache:
            return cache[args]
        else:
            result = func(*args)
            cache[args] = result
            return result

    return wrapper
