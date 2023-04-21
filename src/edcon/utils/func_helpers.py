"""Helper functions used to call other functions."""

import time
from collections.abc import Callable


def func_sequence(func: Callable[[bool], None],
                  arg_list: list = True, delay: float = 0.1):
    """Performs a toggling sequence on a provided toggle function

    Parameter:
        func (Callable): function that is called sequentially with arg from arg_list
        delay (float): delay to use between calls of func
    """
    for arg in arg_list:
        func(arg)

        # Wait for trigger
        time.sleep(delay)
