import functools
import time

def load_log(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        print("⏳Loading...")
        result = func(*args, **kwargs)
        end = time.perf_counter()
        print(f"✅Loaded! {end - start:.6f}s")
        return result
    return wrapper

def request_log(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        print("⏳Request...")
        result = func(*args, **kwargs)
        end = time.perf_counter()
        print(f"✅Result! {end - start:.6f}s")
        return result
    return wrapper
