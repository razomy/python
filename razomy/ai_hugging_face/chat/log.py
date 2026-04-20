import functools

def load_log(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print("⏳Loading...")
        result = func(*args, **kwargs)
        print("✅Loaded!")
        return result
    return wrapper

def request_log(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print("⏳Request...")
        result = func(*args, **kwargs)
        print("✅Result!")
        return result
    return wrapper
