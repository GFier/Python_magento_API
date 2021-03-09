import functools, time, requests

def correct_server_response(func):
    @functools.wraps(func)
    def wrapper_decorator(*args, **kwargs):
        non_stop = True
        count_error = 0
        while non_stop:
            value = None
            try:
                value = func(*args, **kwargs)
                if value is not None:
                    non_stop = False
                else:
                    print('Bad Response from server', flush = True)
                    count_error += 1
                if count_error > 3:
                    value = []
                    non_stop = False
            except requests.exceptions.ConnectionError:
                print('Connection Error retrying after 30 seconds timesleep', flush = True)
                time.sleep(30)
        return value
    return wrapper_decorator


def timer(func):
    @functools.wraps(func)
    def wrapper_timer(*args, **kwargs):
        start_time = time.perf_counter()    # 1
        value = func(*args, **kwargs)
        end_time = time.perf_counter()      # 2
        run_time = end_time - start_time    # 3
        print(f"Finished {func.__name__!r} in {run_time:.4f} secs", flush = True)
        return value
    return wrapper_timer

def conection_aborted(func):
    @functools.wraps(func)
    def wrapper_decorator(*args, **kwargs):
        non_stop = True
        while non_stop:
            try:
                func(*args, **kwargs)
                non_stop = False
            except requests.exceptions.ConnectionError:
                print('Connection Error retrying after 30 seconds timesleep', flush = True)
                time.sleep(30)
        return value
    return wrapper_decorator
