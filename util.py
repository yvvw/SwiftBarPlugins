import time
from collections.abc import Callable


def retry(times: int, fn: Callable):
    available_exec_times = times
    while True:
        available_exec_times -= 1
        try:
            return fn()
        except Exception as err:
            if available_exec_times == 0:
                raise err
            time.sleep(0.1 * (times - available_exec_times))
