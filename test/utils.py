import os.path
import sys


def get_text_from_test_data(file):
    pre_path = os.path.join(os.path.dirname(__file__), 'test_data')
    with open(os.path.join(pre_path, file), mode='r', encoding="utf-8") as f:
        return f.read()


def silence_stderr(f):
    def new_f(*args, **kwargs):
        real_stderr = sys.stderr
        sys.stderr = open(os.devnull, 'w')
        try:
            return f(*args, **kwargs)
        finally:
            sys.stderr.close()
            sys.stderr = real_stderr

    return new_f