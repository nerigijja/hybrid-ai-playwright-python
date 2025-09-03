import time
from functools import wraps
from loguru import logger

def rerun_on_fail(times=1, delay_sec=1):
    def deco(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            last_err = None
            for i in range(times+1):
                try:
                    return fn(*args, **kwargs)
                except Exception as e:
                    last_err = e
                    logger.warning(f"Retry {i+1}/{times} after failure: {e}")
                    time.sleep(delay_sec)
            raise last_err
        return wrapper
    return deco
